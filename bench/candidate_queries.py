"""Unverified candidate proposals and explicit human-labelled benchmark records."""
import argparse,asyncio,json,time,uuid
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.institutions import current,scope
from src.personal import resolve
from src.store import get_collection,production_filter,valid_cached_citations
from src.persistence import write_json,INDEX_LOCK
from src.llm import get_llm_client
from src.intelligence import parse_json
from src.prompts import CANDIDATE_QUERY_PROMPT


def candidate_path():return current().bench/'candidates.jsonl'

def current_chunks():
    where=production_filter()
    if not where:return {}
    rows=get_collection().get(where=where,include=['documents','metadatas'])
    return {cid:{'chunk_id':cid,'text':text,**{k:v for k,v in meta.items() if k!='source_path'}} for cid,text,meta in zip(rows['ids'],rows['documents'],rows['metadatas'])}


def candidates():
    path=candidate_path();rows=[json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    owned=current_chunks();result=[]
    for row in rows:
        if row.get('workspace_id')!=current().workspace_id:continue
        chunk=owned.get(row['suggested_chunk_id']);stale=not chunk or row['version_id']!=chunk['version_id']
        result.append({**row,'labels_verified':False,'suggested_source':chunk if not stale else None,'stale':stale})
    return result


async def generate():
    if not current().personal:raise ValueError('Personal workspace required')
    owned=current_chunks()
    if not owned:raise ValueError('Upload and index personal evidence first')
    rows=list(owned.values());sample=[rows[i*len(rows)//min(25,len(rows))] for i in range(min(25,len(rows)))]
    response=await get_llm_client().chat(messages=[{'role':'system','content':CANDIDATE_QUERY_PROMPT},{'role':'user','content':json.dumps([{'chunk_id':r['chunk_id'],'text':r['text']} for r in sample])}],max_tokens=2400,temperature=.4)
    parsed=parse_json(response.text)
    proposals=parsed.get('candidates',[]) if isinstance(parsed,dict) else parsed if isinstance(parsed,list) else []
    allowed={r['chunk_id'] for r in sample};result=[];seen=set()
    for p in proposals:
        text=p.get('query','').strip();cid=p.get('suggested_chunk_id')
        if not text or len(text)>500 or cid not in allowed or text.casefold() in seen:continue
        seen.add(text.casefold());source=owned[cid]
        result.append({'id':'candidate-'+uuid.uuid4().hex[:16],'workspace_id':current().workspace_id,'query':text,'suggested_chunk_id':cid,
                       'version_id':source['version_id'],'document':source['doc_title'],'page':source['page'],'labels_verified':False})
    if not 20<=len(result)<=30:raise ValueError('Provider did not return 20–30 valid distinct candidates; no labels or partial candidate file were written')
    if not all(valid_cached_citations([r['suggested_chunk_id']]) for r in result):raise ValueError('Sources changed during candidate generation; retry')
    path=candidate_path();path.parent.mkdir(parents=True,exist_ok=True)
    # Atomic JSONL replace; never touch the human label file here.
    temp=path.with_suffix('.jsonl.tmp');temp.write_text(''.join(json.dumps(r)+'\n' for r in result));temp.replace(path)
    return {'candidates':len(result),'labels_verified':False}


def confirm(candidate_id,action,query=None,gold_chunk_ids=None,human_confirmed=False):
    if action=='skip':return {'status':'skipped','labels_verified':False}
    if not human_confirmed:raise ValueError('Explicit human confirmation is required')
    row=next((r for r in candidates() if r['id']==candidate_id),None)
    if not row:raise ValueError('Candidate not found in this workspace')
    text=(query if query is not None else row['query']).strip()
    if not text or len(text)>500:raise ValueError('Question must contain 1–500 characters')
    if action=='correct':gold=[row['suggested_chunk_id']]
    elif action=='wrong':gold=gold_chunk_ids or []
    elif action=='abstain':gold=[]
    else:raise ValueError('Choose Correct, Wrong chunk, Should abstain or Skip')
    with INDEX_LOCK:
        if action!='abstain' and (not gold or not valid_cached_citations(gold)):raise ValueError('Select current eligible chunks from this workspace')
        if action=='correct' and row['stale']:raise ValueError('Suggested source changed; choose a current chunk instead')
        label={'id':row['id'],'workspace_id':current().workspace_id,'query':text,'gold_chunk_ids':gold,'labels_verified':True,
               'label_origin':'human_confirmation','verified_at':time.time()}
        if action=='abstain':label['expect']='abstain'
        path=current().path('queries');existing=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        existing=[r for r in existing if r.get('id')!=candidate_id];existing.append(label)
        temp=path.with_suffix('.jsonl.tmp');temp.write_text(''.join(json.dumps(r)+'\n' for r in existing));temp.replace(path)
    return {'status':'human_confirmed','labels_verified':True,'id':candidate_id}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workspace-id',required=True);args=parser.parse_args()
    with scope(resolve(args.workspace_id)):print(json.dumps(asyncio.run(generate())))
