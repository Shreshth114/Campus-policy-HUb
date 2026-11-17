"""LLM extracts quote-bound rules; Decimal comparisons determine condition statuses."""
import asyncio
from decimal import Decimal,InvalidOperation
import hashlib
import json
import re
from pathlib import Path
from src.institutions import current,workspace_path
from src.authority import get_registry,source_hash,eligible_sources
from src.store import get_collection
from src.persistence import write_json,INDEX_LOCK
from src.llm import get_llm_client, ProviderUnavailableError
from src.prompts import RULE_EXTRACTION_PROMPT,FACT_EXTRACTION_PROMPT,ELIGIBILITY_EXPLANATION_PROMPT

_RULE_LOCK=asyncio.Lock()
OPERATORS={'>=':lambda a,b:a>=b,'>':lambda a,b:a>b,'<=':lambda a,b:a<=b,'<':lambda a,b:a<b,'==':lambda a,b:a==b,'!=':lambda a,b:a!=b}
RELATIONS={'>=':r'>=|≥|at least|minimum|not less than|shall be|mandatory|required',
           '<=':r'<=|≤|at most|maximum|not more than|up\s*to|upto|not exceed',
           '>':r'(?<![<>=])>(?!=)|more than|above|exceed','<':r'(?<![<>=])<(?!=)|less than|below','==':r'(?<![<>=])==(?!=)|exactly|equal to','!=':r'!=|not equal'}
WORDS={'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}

_CANDIDATE_RULE_PATTERN = re.compile(
    r'\d|%|\b(?:percent|percentage|semesters?|credits?|months?|weeks?|days?|hours?|years?|cgpa|sgpa|gpa|marks?|grade\s+[A-Z]|grades|rs\.?|inr|\$)\b',
    re.IGNORECASE,
)
_RULE_OPERATOR_PATTERN = re.compile(
    r'\b(?:at\s+least|minimum|at\s+most|maximum|less\s+than|greater\s+than|more\s+than|exceed|not\s+exceed|not\s+less|within|mandatory|required|shall\s+not|must\s+not|must|shall|equal\s+to)\b',
    re.IGNORECASE,
)


def is_rule_candidate(text: str) -> bool:
    """Pre-filter chunks before sending to LLM for rule extraction."""
    if not text or len(text.split()) < 10:
        return False
    return bool(_CANDIDATE_RULE_PATTERN.search(text) and _RULE_OPERATOR_PATTERN.search(text))

def number(value):
    if isinstance(value,bool):raise ValueError('Boolean is not a numeric fact')
    try:result=Decimal(str(value))
    except (InvalidOperation,ValueError):raise ValueError('Expected a finite number')
    if not result.is_finite():raise ValueError('Expected a finite number')
    return result

def numeric_mentions(text,words=False):
    values=[number(n) for n in re.findall(r'(?<![\w.])[+-]?\d+(?:\.\d+)?(?![\w.])',text)]
    if words:values.extend(Decimal(v) for k,v in WORDS.items() if re.search(r'\b'+k+r'\b',text,re.I))
    return values

def subject(value):return re.sub(r'\s+','_',str(value).strip().casefold())[:100]

def unit(value):return {'percent':'%','percentage':'%','per cent':'%'}.get(str(value).strip().casefold(),str(value).strip().casefold())

def parse_json(text):
    text = text.strip()
    m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if m:
        text = m.group(1).strip()
    elif text.startswith(('[','{')):
        pass
    elif '{' in text:
        first = text.find('{')
        last = text.rfind('}')
        if first != -1 and last > first:
            text = text[first:last + 1]
    text = re.sub(r',\s*([\]}])', r'\1', text)
    return json.loads(text, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Nonfinite JSON value')))

def validate_rule(raw,chunk):
    try:
        quote=raw['verbatim_quote'];op=raw['operator'];value=number(raw['value'])
        if not isinstance(quote,str) or not quote.strip() or quote not in chunk['text'] or op not in OPERATORS:return None
        if value not in numeric_mentions(quote) or not re.search(RELATIONS[op],quote,re.I):return None
        if not isinstance(raw.get('subject'),str) or not raw['subject'].strip():return None
        for key in ('applies_to','deadline','penalty'):
            if raw.get(key) and (not isinstance(raw[key],str) or raw[key] not in quote):return None
        exceptions=raw.get('exceptions') or []
        if not isinstance(exceptions,list) or any(not isinstance(e,str) or e not in quote for e in exceptions):return None
        normalized_unit=unit(raw.get('unit',''))
        if normalized_unit=='%':
            if not re.search(r'%|percent|per cent',quote,re.I):return None
        elif normalized_unit and normalized_unit not in quote.casefold():
            # A generic count is acceptable only when the counted subject is stated.
            stem=subject(raw['subject']).removesuffix('_count').replace('_',' ')
            if normalized_unit!='count' or stem not in quote.casefold():return None
        tokens=[t for t in subject(raw['subject']).split('_') if t not in {'count','percentage','percent','threshold','requirement'}]
        if tokens and not any(re.search(r'\b'+re.escape(t)+r's?\b',quote,re.I) for t in tokens):return None
        if not exceptions and re.search(r'\bexcept|\bunless|subject to|provided that',quote,re.I):return None
        result={k:raw.get(k) for k in ('applies_to','deadline','penalty')}
        result.update(subject=subject(raw['subject']),operator=op,value=str(value),unit=unit(raw.get('unit','')),exceptions=exceptions,
                      verbatim_quote=quote,chunk_id=chunk['chunk_id'],document=chunk['doc_title'],document_id=chunk['doc_id'],
                      version_id=chunk['version_id'],page=chunk['page'],workspace_id=current().workspace_id,
                      effective_date=chunk.get('effective_date'),issuing_authority=chunk.get('issuing_authority'))
        result['rule_id']=hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()[:24]
        return result
    except (KeyError,TypeError,ValueError):return None

def _cache():
    try:return json.loads((workspace_path('processed')/'rules.json').read_text())
    except (OSError,ValueError):return {}

def _key(entry):
    from src.config import PROVIDERS,LLM_PRIMARY
    model=PROVIDERS[LLM_PRIMARY].get('model')
    return hashlib.sha256(json.dumps([current().workspace_id,entry['doc_id'],entry['file_hash'],RULE_EXTRACTION_PROMPT,model]).encode()).hexdigest()

def document_entry(did,version=None):
    entry=get_registry().get(did)
    if not entry or entry['extraction_status']=='removed':raise ValueError('Document not found in this workspace')
    if version and version!=entry['version_id']:
        entry=next((v for v in entry.get('history',[]) if v.get('version_id')==version and v.get('source_path')),None)
        if not entry:raise ValueError('Document version not found')
    if not Path(entry['source_path']).resolve().is_relative_to(current().raw.resolve()):raise ValueError('Foreign source path')
    if source_hash(entry['source_path'])!=entry['file_hash']:raise ValueError('Source changed; replace the document before extracting rules')
    return entry

def chunks_for(entry):
    records=get_collection().get(where={'$and':[current().filter,{'doc_id':entry['doc_id']},{'version_id':entry['version_id']}]},include=['documents','metadatas'])
    chunks=[{'chunk_id':cid,'text':text,**meta,'effective_date':entry.get('effective_date'),'issuing_authority':entry.get('issuing_authority')} for cid,text,meta in zip(records['ids'],records['documents'],records['metadatas'])]
    if chunks or get_registry()[entry['doc_id']]['version_id']==entry['version_id']:return chunks
    # Historical originals are read for explicit comparison, never student retrieval.
    from src.ingest import extract_pages,_doc_title_from_path
    from src.chunking import chunk_text
    path=Path(entry['source_path']);title=_doc_title_from_path(path)
    for page,text,parser in extract_pages(path):
        if len(text.strip())<20:continue
        from src.chunking import chunk_personal
        prepared=chunk_personal(text,entry['doc_id'],title,entry['file_hash'],str(path),page) if entry.get('extraction_profile')=='personal_v2' else chunk_text(text,entry['doc_id'],title,entry['file_hash'],str(path))
        for chunk in prepared:
            index=len(chunks)
            cid=hashlib.sha256(f"{current().scope_id}|{entry['doc_id']}|{entry['version_id']}|{chunk.section}|{index}".encode()).hexdigest()
            chunks.append({'chunk_id':cid,'text':chunk.text,'doc_id':entry['doc_id'],'doc_title':title,'version_id':entry['version_id'],'page':page,
                           'effective_date':entry.get('effective_date'),'issuing_authority':entry.get('issuing_authority')})
    return chunks


def rules_for(entry):
    chunks={c['chunk_id']:c for c in chunks_for(entry)}
    return [valid for r in _cache().get(_key(entry),{}).get('rules',[]) if r.get('chunk_id') in chunks and (valid:=validate_rule(r,chunks[r['chunk_id']]))]

def list_rules():
    result=[]
    for did in eligible_sources():
        entry=document_entry(did);result.extend(rules_for(entry))
    return result

RULE_EXTRACTION_TIMEOUT = 120.0
RULE_EXTRACTION_PAUSE = 2.0
EXTRACTION_STATE_VERSION = 2


def extraction_complete(cached):
    return bool(cached and cached.get('state_version')==EXTRACTION_STATE_VERSION and cached.get('partial') is False)


async def extract_rules(document_id=None,version_id=None):
    if not current().personal:raise ValueError('Personal workspace required')
    if _RULE_LOCK.locked():
        return {'status':'busy','documents':0,'rules':0,'discarded':0,'cached_documents':0,
                'errors':[{'error':'ExtractionBusy','message':'Another rule extraction is running. Wait for it to finish before retrying.'}]}
    try:
        async with asyncio.timeout(RULE_EXTRACTION_TIMEOUT):
            return await _extract_rules(document_id,version_id)
    except TimeoutError:
        message='Extraction time limit reached. Completed batches are saved; retry to resume. Comparison has not run.'
        path=workspace_path('processed')/'rules_activity.json'
        try:activity=json.loads(path.read_text())
        except (OSError,ValueError):activity={}
        write_json(path,{**activity,'status':'partial','message':message})
        return {'status':'partial','documents':0,'rules':0,'discarded':0,'cached_documents':0,
                'errors':[{'error':'ExtractionTimeout','message':message}]}


async def _extract_rules(document_id,version_id):
    async with _RULE_LOCK:
        entries=[document_entry(document_id,version_id)] if document_id else [document_entry(did) for did in eligible_sources()]
        summary={'status':'complete','documents':0,'rules':0,'discarded':0,'cached_documents':0,'errors':[],
                 'total_chunks_evaluated':0,'chunks_sent':0}
        for entry in entries:
            chunks=await asyncio.to_thread(chunks_for,entry)
            if not chunks:
                summary['errors'].append({'document':entry['doc_title'],'error':'No indexed extractable text for this version'})
                summary['status']='partial';continue
            key=_key(entry);cache=_cache();saved=cache.get(key,{})
            if extraction_complete(saved):
                summary['rules']+=len(rules_for(entry));summary['cached_documents']+=1;continue
            candidates=[c for c in chunks if is_rule_candidate(c['text'])]
            summary['total_chunks_evaluated']+=len(chunks)
            # Only explicitly completed batches from this exact file/prompt/model
            # cache key can be skipped. Legacy partial rules are preserved, but
            # legacy completion flags cannot prove that every batch ran.
            completed=set(saved.get('completed_chunk_ids',[])) if saved.get('state_version')==EXTRACTION_STATE_VERSION else set()
            completed &= {c['chunk_id'] for c in candidates}
            remaining=[c for c in candidates if c['chunk_id'] not in completed]
            summary['chunks_sent']+=len(remaining)
            accepted={r['rule_id']:r for r in rules_for(entry)}
            def persist(partial=True):
                cache=_cache();cache[key]={'state_version':EXTRACTION_STATE_VERSION,'document_id':entry['doc_id'],
                    'rules':list(accepted.values()),'file_hash':entry['file_hash'],'workspace_id':current().workspace_id,
                    'partial':partial,'completed_chunk_ids':sorted(completed)}
                write_json(workspace_path('processed')/'rules.json',cache)
            persist()  # Cancellation/provider failure must never leave a complete cache.
            discarded=0;failed=False
            for offset in range(0,len(remaining),3):
                batch=remaining[offset:offset+3];lookup={c['chunk_id']:c for c in batch}
                write_json(workspace_path('processed')/'rules_activity.json',{
                    'status':'running','document':entry['doc_title'],'processed_chunks':len(completed),
                    'total_chunks':len(candidates),'extracted_rules':len(accepted),
                    'message':f'Processed {len(completed)}/{len(candidates)} candidate chunks; {len(accepted)} validated rules.'})
                if offset:await asyncio.sleep(RULE_EXTRACTION_PAUSE)
                try:
                    response=await get_llm_client().chat(messages=[{'role':'system','content':RULE_EXTRACTION_PROMPT},
                        {'role':'user','content':json.dumps([{'chunk_id':c['chunk_id'],'text':c['text']} for c in batch])}],
                        max_tokens=1600,temperature=0)
                    if getattr(response,'finish_reason',None)=='length':raise ValueError('Incomplete model response')
                    rows=parse_json(response.text).get('rules',[])
                    if not isinstance(rows,list):raise ValueError('Expected rule list')
                    for raw in rows:
                        chunk=lookup.get(raw.get('chunk_id')) if isinstance(raw,dict) else None
                        valid=validate_rule(raw,chunk) if chunk else None
                        if valid:accepted[valid['rule_id']]=valid
                        else:discarded+=1
                    completed.update(lookup)
                except Exception as exc:
                    # The unified client already bounds its transport retries.
                    # Do not sleep through arbitrary Retry-After values here.
                    error={'document':entry['doc_title'],'error':type(exc).__name__,
                           'message':'Rule extraction interrupted. Completed batches are saved; retry to resume.'}
                    if isinstance(exc,ProviderUnavailableError):
                        error['message']='AI provider unavailable. Completed batches are saved; retry to resume.'
                    summary['errors'].append(error);failed=True
                persist()
                if failed:break
            if document_entry(entry['doc_id'],entry['version_id'] if version_id else None)['version_id']!=entry['version_id']:
                raise ValueError('Document replaced during rule extraction; retry')
            persist(partial=failed)
            summary['rules']+=len(accepted);summary['discarded']+=discarded
            if failed:
                summary['status']='partial';break
            summary['documents']+=1
        write_json(workspace_path('processed')/'rules_activity.json',{
            **summary,'message':('Extraction incomplete. Retry to resume saved batches.' if summary['errors'] else
                                f"Extraction complete: {summary['rules']} rules validated from {summary['documents']} document(s).")})
        return summary

async def parse_facts(text):
    rules=list_rules();allowed={r['subject']:{'subject':r['subject'],'unit':r['unit']} for r in rules}
    if not allowed:return {'facts':[],'confirmation_required':True,'message':'Extract source rules first; no facts or verdict are assumed.'}
    response=await get_llm_client().chat(messages=[{'role':'system','content':FACT_EXTRACTION_PROMPT},{'role':'user','content':json.dumps({'student_text':text,'allowed_fields':list(allowed.values())})}],max_tokens=700,temperature=0)
    proposed=parse_json(response.text).get('facts',[]);facts=[]
    for raw in proposed:
        try:
            key=subject(raw['subject']);quote=raw['quote'];value=number(raw['value'])
            if key in allowed and isinstance(quote,str) and quote in text and value in numeric_mentions(quote,words=True) and unit(raw['unit'])==allowed[key]['unit']:
                facts.append({'subject':key,'value':str(value),'unit':unit(raw['unit']),'quote':quote})
        except (KeyError,TypeError,ValueError):continue
    return {'facts':facts,'confirmation_required':True,'message':'Confirm or edit these stated facts before analysis.'}

def evaluate(rules,facts,applicability_confirmed=False,conflicted=None):
    by_subject={};conditions=[];conflicted=set(conflicted or [])
    for fact in facts:
        key=subject(fact['subject'])
        by_subject.setdefault(key,[]).append(fact)
    for rule in rules:
        candidates=by_subject.get(rule['subject'],[]);fact=candidates[0] if len(candidates)==1 else None
        status='insufficient evidence';reason='Provide one confirmed value in the required unit.'
        if fact and unit(fact.get('unit',''))==rule['unit']:
            if rule['subject'] in conflicted:reason='Possible conflicting source rules require clarification; no winner is chosen.'
            elif not applicability_confirmed:reason='Confirm that the source applies to your programme, cohort and situation.'
            elif rule['exceptions']:reason='An exception needs separate evidence; no exception is assumed.'
            else:
                status='satisfied' if OPERATORS[rule['operator']](number(fact['value']),number(rule['value'])) else 'not satisfied'
                reason=f"{number(fact['value'])} {rule['operator']} {rule['value']} is {'true' if status=='satisfied' else 'false'}."
        conditions.append({'rule':rule,'your_value':str(fact['value']) if fact else None,'status':status,'reason':reason})
    statuses={c['status'] for c in conditions}
    verdict='insufficient evidence'
    if conditions and 'insufficient evidence' not in statuses:verdict='ineligible' if 'not satisfied' in statuses else 'eligible'
    return {'verdict':verdict,'conditions':conditions,'missing_facts':list(dict.fromkeys(c['rule']['subject'] for c in conditions if c['your_value'] is None)),
            'scope':'Only these extracted conditions; not an official institutional eligibility decision.','abstained':not bool(conditions)}

async def analyse(question,facts,confirmed,applicability_confirmed=False):
    if not confirmed:raise ValueError('Confirm or edit your facts before analysis')
    for fact in facts:number(fact['value'])
    from src.retrieve import retrieve
    found=await retrieve(question,mode='raw',production=True)
    ids={c.chunk_id for c in found.chunks}
    rules=[r for r in list_rules() if r['chunk_id'] in ids]
    computed=evaluate(rules,facts,applicability_confirmed,conflicted={c['subject'] for c in conflicts()})
    computed.update(trust_notice=__import__('src.personal',fromlist=['TRUST_NOTICE']).TRUST_NOTICE,question=question,explanations=[])
    if not rules:return computed
    try:
        response=await get_llm_client().chat(messages=[{'role':'system','content':ELIGIBILITY_EXPLANATION_PROMPT},{'role':'user','content':json.dumps(public_model_data(computed))}],max_tokens=900,temperature=0)
        allowed={c['rule']['rule_id']:c for c in computed['conditions']}
        for item in parse_json(response.text).get('explanations',[]):
            row=allowed.get(item.get('rule_id'));text=item.get('text')
            if row and isinstance(text,str) and not re.search(r'\beligible|\bineligible|\bpermission|\bpermitted|\ballowed',text,re.I):
                permitted=numeric_mentions(json.dumps(row))
                if all(n in permitted for n in numeric_mentions(text)):
                    computed['explanations'].append({'text':text,'rule_id':item['rule_id'],'chunk_id':row['rule']['chunk_id'],'page':row['rule']['page'],'document':row['rule']['document']})
    except Exception:computed['explanation_warning']='AI explanation unavailable; deterministic comparisons are shown.'
    # Recheck live rule ownership/hash after the model call.
    live={r['rule_id'] for r in list_rules()}
    if any(r['rule_id'] not in live for r in rules):raise ValueError('Sources changed during analysis; review facts and retry')
    return computed


def conflicts_from_rules(rules):
    groups={};result=[]
    for rule in rules:groups.setdefault(rule['subject'],[]).append(rule)
    for key,rows in groups.items():
        for index,left in enumerate(rows):
            for right in rows[index+1:]:
                if left['document_id']==right['document_id'] or number(left['value'])==number(right['value']):continue
                result.append({'subject':key,'status':'possible conflict','evidence':[left,right],'winner':None,
                               'reason':'Different source values for the same subject. They may apply to different programmes, cohorts, units or situations. Dates alone do not establish authority. Seek applicability and issuing-authority evidence; no winner is selected.'})
    return result


def conflicts():return conflicts_from_rules(list_rules())


def public_model_data(value):
    if isinstance(value,dict):return {k:public_model_data(v) for k,v in value.items() if k not in {'workspace_id','institution_id','source_path'}}
    if isinstance(value,list):return [public_model_data(v) for v in value]
    return value


def version_catalog():
    result=[]
    for entry in get_registry().values():
        if entry['extraction_status']=='removed':continue
        seen=set()
        for version in [entry]+list(reversed(entry.get('history') or [])):
            if version.get('version_id') and version.get('source_path') and version['version_id'] not in seen:
                seen.add(version['version_id']);result.append({'document_id':entry['doc_id'],'document':version['doc_title'],'version_id':version['version_id'],
                    'current':version['version_id']==entry['version_id'],'effective_date':version.get('effective_date')})
    return result


def diff_rules(old,new):
    def grouped(rows):
        values={}
        for rule in rows:values.setdefault((rule['subject'],rule['unit'],rule.get('applies_to')),[]).append(rule)
        return values
    left,right=grouped(old),grouped(new);rows=[]
    for key in sorted(set(left)|set(right),key=str):
        a,b=left.get(key,[]),right.get(key,[])
        if not a:kind='addition'
        elif not b:kind='removal'
        else:
            def signature(values):return sorted(json.dumps({k:v.get(k) for k in ('operator','value','exceptions','deadline','penalty','effective_date')},sort_keys=True) for v in values)
            if signature(a)==signature(b):continue
            kind='modification'
        rows.append({'kind':kind,'subject':key[0],'old':a,'new':b})
    return rows


def compare_versions(old_document_id,old_version_id,new_document_id,new_version_id):
    old=document_entry(old_document_id,old_version_id);new=document_entry(new_document_id,new_version_id)
    cache=_cache()
    if not extraction_complete(cache.get(_key(old))) or not extraction_complete(cache.get(_key(new))):
        return {'status':'blocked','message':'Extract validated rules for both selected versions before comparison.','changes':[]}
    return {'status':'completed','changes':diff_rules(rules_for(old),rules_for(new)),
            'notice':'Source-backed rule-table differences only. No official applicability, authority or winner is inferred.'}
