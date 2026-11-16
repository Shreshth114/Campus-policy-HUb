"""Evidence-only answer contract. No institutional facts, retrieval or storage writes."""
import hashlib
import json
import re
from src.evidence import normalize
from src.institutions import current

PROTOCOL = 'complete-provisions-v3-coverage'
# A numbered provision, not a decimal value or a bare cross-reference in prose.
BOUNDARY = re.compile(r'(?<!\w)(?:[A-Z]\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)*)\.\s+')


def provisions(text):
    """Keep literal, contiguous units. Never deduplicate legitimate repetition.

    Numbered provisions are atomic; their sublists stay attached. For prose,
    blank-line paragraphs are the only boundaries. A cut-off unit is withheld.
    """
    body = text.split('\n',1)[-1] if ' > ' in text.split('\n',1)[0] else text
    matches=list(BOUNDARY.finditer(body))
    if matches:
        parts=[body[m.start():matches[i+1].start() if i+1<len(matches) else len(body)].strip()
               for i,m in enumerate(matches)]
        prefix=body[:matches[0].start()].strip()
        if prefix and complete(prefix):parts.insert(0,prefix)
    else:
        parts=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
    return [p for p in parts if complete(p)]


def complete(text):
    # Conservative terminal-boundary check, not semantic completeness. A
    # balanced trailing parenthetical after a finished sentence stays literal.
    text=text.strip()
    terminal = bool(re.search(r'[.!?;][\)\]"”\x27]*$',text))
    parenthetical = bool(re.search(r'[.!?;]\s*\([^()]*\)$',text))
    return (terminal or parenthetical) and bool(re.search(r'[a-z]{2,}',text))


def parse_object(text):
    try:
        data=json.loads(text)
    except (ValueError,TypeError):
        return None
    return data if isinstance(data,dict) else None


def render_contract(data,chunks):
    """Accept only complete exact units. Do not guess or repair model citations."""
    if not isinstance(data,dict) or set(data)!={'status','claims'} or data['status'] not in ('answer','insufficient'):
        return None,[{'reason':'invalid_answer_contract'}]
    claims=data['claims']
    if data['status']=='insufficient':
        return None,[{'reason':'model_abstained'}]
    if not isinstance(claims,list) or not 1<=len(claims)<=12:
        return None,[{'reason':'invalid_answer_contract'}]
    rendered=[];failures=[]
    for claim in claims:
        if not isinstance(claim,dict) or set(claim) not in ({'quote','source'},{'provision','source'}) or not all(isinstance(v,str) for v in claim.values()):
            failures.append({'reason':'invalid_claim_contract'});continue
        label=claim['source'];quote=claim.get('quote','').strip()
        if not re.fullmatch(r'C[1-9]\d*',label) or int(label[1:])>len(chunks):
            failures.append({'reason':'invalid_quote_citation','label':label});continue
        c=chunks[int(label[1:])-1]
        units=provisions(c.text)
        if 'provision' in claim:
            unit_id=claim['provision']
            if not re.fullmatch(r'P[1-9]\d*',unit_id) or int(unit_id[1:])>len(units):
                failures.append({'reason':'invalid_provision_id','label':label});continue
            quote=units[int(unit_id[1:])-1]
        if normalize(quote) not in {normalize(unit) for unit in units}:
            failures.append({'reason':'incomplete_or_nonliteral_provision','label':label,'quote':quote});continue
        # Use literal model wording, normalized whitespace only. Nested quotation
        # syntax is ambiguous for the existing per-quotation validator: fail closed.
        if any(mark in quote for mark in ('"','“','”','\n')):
            quote=' '.join(quote.split())
        if any(mark in quote for mark in ('"','“','”')):
            failures.append({'reason':'ambiguous_nested_quotation','label':label});continue
        rendered.append('"'+quote+'" ['+label+']')
    return ('\n\n'.join(dict.fromkeys(rendered)) if not failures else None),failures


def review_messages(question,chunks,contract):
    from src.prompts import ANSWER_REVIEW_PROMPT,format_chunks_for_prompt
    from src.question_coverage import question_requirements
    excerpts=format_chunks_for_prompt([vars(c) for c in chunks],provision_labels=True)
    return [{'role':'system','content':ANSWER_REVIEW_PROMPT},
            {'role':'user','content':json.dumps({'question':question,'proposed_selection':contract,
                                               'evidence':excerpts,
                                               'requirements':question_requirements(question)},ensure_ascii=False)}]


def review_passes(review,requirements=None,selected=None):
    fields={'relevant','complete','qualifications_preserved','supported','reasons','coverage'}
    if not (isinstance(review,dict) and set(review)==fields
            and all(review.get(k) is True for k in fields-{'reasons','coverage'})
            and isinstance(review['reasons'],list) and not review['reasons']):
        return False
    from src.question_coverage import coverage_failures
    if requirements is None:
        # Compatibility for schema-only callers; production always supplies
        # independently computed requirements and selected source references.
        if not isinstance(review['coverage'],list) or not review['coverage']:return False
        requirements=[{'id':row.get('requirement_id')} for row in review['coverage'] if isinstance(row,dict)]
        selected=set(ref for row in review['coverage'] if isinstance(row,dict)
                     for ref in row.get('evidence',[]) if isinstance(ref,str))
    return not coverage_failures(review['coverage'],requirements,selected or set())


def _binding(question,answer,chunks):
    from src.prompts import ANSWER_SYSTEM_PROMPT,ANSWER_USER_TEMPLATE,ANSWER_REVIEW_PROMPT
    payload={'prompt_sha256':hashlib.sha256((ANSWER_SYSTEM_PROMPT+ANSWER_USER_TEMPLATE+ANSWER_REVIEW_PROMPT).encode()).hexdigest(),'protocol':PROTOCOL,'question':question,'answer':answer,
             'institution':current().institution_id,'workspace':current().workspace_id,
             'evidence':[{'id':c.chunk_id,'doc':c.doc_id,'version':c.version_id,'text':c.text,
                          'institution':c.institution_id,'workspace':c.workspace_id,
                          'page':c.page,'pages':c.pages or [c.page],'source_ids':c.source_chunk_ids or [c.chunk_id]} for c in chunks]}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def make_proof(question,answer,chunks,contract,review):
    return {'protocol':PROTOCOL,'binding':_binding(question,answer,chunks),'contract':contract,'review':review}


def proof_matches(proof,question,answer,chunks):
    from src.question_coverage import question_requirements,selected_references
    if not isinstance(proof,dict) or proof.get('protocol')!=PROTOCOL or not review_passes(
            proof.get('review'),question_requirements(question),selected_references(proof.get('contract'),chunks)):
        return False
    rendered,failures=render_contract(proof.get('contract'),chunks)
    return not failures and rendered==answer and proof.get('binding')==_binding(question,answer,chunks)
