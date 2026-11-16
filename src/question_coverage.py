"""Explicit question spans and fail-closed evidence coverage, without policy facts.

This bounded heuristic makes conjunctions visible; it is not a semantic parser.
The full question remains mandatory so context, alternatives and implicit needs
must still be assessed by the reviewer and independently evaluated by humans.
"""
import re


def question_requirements(question):
    if not isinstance(question,str) or not question.strip():
        raise ValueError('Question is required')
    result=[{'id':'Q0','text':question,'start':0,'end':len(question),'kind':'whole_question'}]
    separators=list(re.finditer(r'\band\b|;',question,re.I))[:5]
    if not separators:return result
    spans=[];start=0
    for match in separators:
        spans.append((start,match.start()));start=match.end()
    spans.append((start,len(question)))
    trimmed=[]
    for a,b in spans:
        while a<b and question[a] in ' ,':a+=1
        while b>a and question[b-1] in ' ,':b-=1
        if a<b:trimmed.append((a,b))
    spans=trimmed
    if len(spans)<2:return result
    for i,(a,b) in enumerate(spans,1):
        result.append({'id':f'Q{i}','text':question[a:b],'start':a,'end':b,'kind':'conjoined_span'})
    return result


def selected_references(contract,chunks):
    """Return only valid complete units explicitly chosen by the generator."""
    from src.grounding import render_contract,provisions
    from src.evidence import normalize
    _,failures=render_contract(contract,chunks)
    if failures:return set()
    refs=set()
    for claim in contract['claims']:
        source=claim['source'];units=provisions(chunks[int(source[1:])-1].text)
        if 'provision' in claim:
            refs.add(source+'/'+claim['provision'])
        else:
            refs.update(source+f'/P{i}' for i,unit in enumerate(units,1) if normalize(unit)==normalize(claim['quote']))
    return refs


def coverage_failures(rows,requirements,selected):
    expected={r['id'] for r in requirements}
    if not isinstance(rows,list):return [{'reason':'missing_coverage_ledger'}]
    failures=[];seen=set()
    for row in rows:
        if (not isinstance(row,dict) or set(row)!={'requirement_id','status','evidence','reason'}
                or not isinstance(row.get('requirement_id'),str)
                or not isinstance(row.get('reason'),str)
                or row.get('status') not in ('covered','unsupported','ambiguous')
                or not isinstance(row.get('evidence'),list)
                or any(not isinstance(ref,str) for ref in row.get('evidence',[]))):
            failures.append({'reason':'invalid_coverage_row'});continue
        rid=row['requirement_id']
        if rid not in expected or rid in seen:
            failures.append({'reason':'unknown_or_duplicate_requirement','requirement_id':rid})
        seen.add(rid)
        refs=row['evidence']
        if row['status']=='covered':
            if not refs or len(refs)!=len(set(refs)) or not set(refs)<=selected:
                failures.append({'reason':'coverage_invalid_evidence','requirement_id':rid})
        else:
            failures.append({'reason':'coverage_'+row['status'],'requirement_id':rid,'details':row['reason']})
            if refs:failures.append({'reason':'uncovered_requirement_has_evidence','requirement_id':rid})
    for rid in sorted(expected-seen):
        failures.append({'reason':'coverage_requirement_missing','requirement_id':rid})
    return failures
