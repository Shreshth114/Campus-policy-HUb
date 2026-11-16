"""Personal APIs require the opaque X-Workspace-ID capability, never admin access."""
import asyncio
from pathlib import Path
from fastapi import APIRouter,HTTPException,Request
from pydantic import BaseModel,ConfigDict,StrictStr
from src import personal,documents
from src.institutions import current
from src.authority import get_registry
from src.store import has_chunks,get_collection_count

router=APIRouter(prefix='/personal')
class WorkspaceRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    college:StrictStr=''
class PersonalQuestion(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question:StrictStr
    mode:str='fusion'

@router.post('/workspaces')
async def create_workspace(body:WorkspaceRequest):return personal.create(body.college)

@router.get('/workspace')
async def workspace():
    return {'workspace':personal.registry()[current().workspace_id],'documents':sum(e['extraction_status']!='removed' for e in get_registry().values()),
            'chunks':await asyncio.to_thread(get_collection_count),'ready':await asyncio.to_thread(has_chunks),
            'trust_notice':personal.TRUST_NOTICE,'limits':{'bytes':personal.MAX_BYTES,'pages':personal.MAX_PAGES,'documents':personal.MAX_DOCUMENTS}}

@router.delete('/workspace')
async def delete_workspace():return await asyncio.to_thread(personal.delete)

@router.get('/documents')
async def list_documents():return {'documents':[e for e in get_registry().values() if e['extraction_status']!='removed'],'trust_notice':personal.TRUST_NOTICE}

@router.post('/documents')
async def upload(request:Request):
    from src.server import upload_documents
    return await upload_documents('',request)

@router.get('/documents/{document_id}')
async def detail(document_id:str):
    from src.server import source_detail
    # The shared detail helper uses the active scope, never the route's arbitrary ID.
    return await source_detail('',document_id)

@router.get('/documents/{document_id}/chunks')
async def document_chunks(document_id: str):
    """Read exact current-version vectors' text; never extract or index a PDF."""
    from src.store import get_collection
    ctx = current()
    entry = get_registry().get(document_id) if ctx.personal else None
    if not entry or entry.get('extraction_status') == 'removed':
        raise HTTPException(404, 'Document not found in this workspace')
    rows = await asyncio.to_thread(
        get_collection().get,
        where={'$and': [ctx.filter, {'doc_id': document_id},
                        {'version_id': entry['version_id']}]},
        include=['documents', 'metadatas'])
    chunks = []
    for cid, text, metadata in zip(rows['ids'], rows['documents'], rows['metadatas']):
        meta = metadata or {}
        chunks.append({'chunk_id': cid, 'text': text,
                       **{key: meta.get(key) for key in
                          ('chunk_index', 'page', 'pages', 'section')},
                       'character_count': len(text) if text is not None else None})
    chunks.sort(key=lambda c: (c['chunk_index'] if isinstance(c['chunk_index'], (int, float))
                              else float('inf'), c['chunk_id']))
    return {'document_id': document_id, 'filename': entry['original_filename'],
            'version_id': entry['version_id'], 'total': len(chunks), 'chunks': chunks}

@router.get('/documents/{document_id}/original')
async def original(document_id:str):
    from src.server import source_original
    return await source_original('',document_id)

@router.delete('/documents/{document_id}')
async def remove(document_id:str):
    try:return await asyncio.to_thread(documents.remove,document_id)
    except ValueError:raise HTTPException(404,'Document not found in this workspace')

@router.post('/documents/{document_id}/index')
async def index(document_id:str):
    from src.server import reindex_document
    return await reindex_document('',document_id)

@router.get('/activity')
async def activity():
    from src.server import index_activity
    return await index_activity('')

@router.post('/ask')
async def ask(body:PersonalQuestion):
    from src.pipeline import ask
    try:return (await ask(body.question,body.mode)).to_dict()
    except ValueError as exc:raise HTTPException(422,str(exc))

@router.post('/compare')
async def compare(body:PersonalQuestion):
    from src.server import compare_endpoint,QuestionRequest
    try:return await compare_endpoint(QuestionRequest(question=body.question,mode=body.mode,institution_id=''))
    except ValueError as exc:raise HTTPException(422,str(exc))

@router.get('/citations/{chunk_id}')
async def citation(chunk_id:str):
    from src.server import citation_detail
    return await citation_detail('',chunk_id)

@router.post('/cache/clear')
async def cache_clear():
    from src.cache import clear_cache
    return {'cleared':await asyncio.to_thread(clear_cache)}

@router.get('/bench/status')
async def benchmark_status():
    from src.server import benchmark_status
    return await benchmark_status()

@router.get('/bench/results/{filename}')
async def benchmark_result(filename:str):
    from src.server import serve_bench_result
    return await serve_bench_result(filename)

@router.post('/bench/run')
async def benchmark_run():
    from bench.run_benchmark import run_benchmark
    return await run_benchmark()

class ExtractionRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    document_id:str|None=None
    version_id:str|None=None
class FactRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    text:StrictStr
class Fact(BaseModel):
    model_config=ConfigDict(extra='forbid')
    subject:StrictStr
    value:StrictStr
    unit:StrictStr=''
class AnalysisRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question:StrictStr
    facts:list[Fact]
    confirmed:bool=False
    applicability_confirmed:bool=False

@router.get('/rules')
async def rules():
    from src.intelligence import list_rules
    return {'rules':await asyncio.to_thread(list_rules),'notice':'Extracted by AI, verify against the source quote.'}

@router.post('/rules/extract')
async def extract(body:ExtractionRequest):
    from src.intelligence import extract_rules
    try:return await extract_rules(body.document_id,body.version_id)
    except ValueError as exc:raise HTTPException(422,str(exc))

@router.post('/facts/parse')
async def facts(body:FactRequest):
    from src.intelligence import parse_facts
    try:return await parse_facts(body.text[:2000])
    except Exception:raise HTTPException(503,'Fact extraction unavailable. Enter and confirm facts manually; no verdict was assumed.')

@router.post('/analyse')
async def analyse(body:AnalysisRequest):
    from src.intelligence import analyse
    try:return await analyse(body.question,[f.model_dump() for f in body.facts],body.confirmed,body.applicability_confirmed)
    except ValueError as exc:raise HTTPException(422,str(exc))


@router.get('/conflicts')
async def conflicts():
    from src.intelligence import conflicts
    return {'conflicts':await asyncio.to_thread(conflicts),'trust_notice':personal.TRUST_NOTICE}


class ChangeRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    old_document_id:StrictStr
    old_version_id:StrictStr
    new_document_id:StrictStr
    new_version_id:StrictStr

@router.get('/versions')
async def versions():
    from src.intelligence import version_catalog
    return {'versions':await asyncio.to_thread(version_catalog)}

@router.post('/changes')
async def changes(body:ChangeRequest):
    from src.intelligence import compare_versions
    try:return await asyncio.to_thread(compare_versions,**body.model_dump())
    except ValueError as exc:raise HTTPException(422,str(exc))

@router.get('/rules/activity')
async def rule_activity():
    import json
    path=current().processed/'rules_activity.json'
    return json.loads(path.read_text()) if path.exists() else {'status':'idle'}


@router.get('/evidence')
async def evidence(document_id:str|None=None,offset:int=0,limit:int=50):
    from src.store import production_filter,get_collection
    if offset<0 or not 1<=limit<=500:raise HTTPException(422,'Invalid evidence page')
    where=production_filter()
    if not where:return {'chunks':[]}
    if document_id:where={'$and':[where,{'doc_id':document_id}]}
    rows=await asyncio.to_thread(get_collection().get,where=where,offset=offset,limit=limit,include=['documents','metadatas'])
    return {'chunks':[{'chunk_id':cid,'text':text,**{k:v for k,v in meta.items() if k!='source_path'}} for cid,text,meta in zip(rows['ids'],rows['documents'],rows['metadatas'])]}

@router.post('/demo')
async def demo():
    from src.institutions import scope
    from src.config import PROJECT_ROOT
    from src.server import _reindex_lock
    from src.reindex import reindex
    if _reindex_lock.locked():raise HTTPException(409,'Indexing is already running; retry shortly')
    async with _reindex_lock:
        entry=personal.create('SYNTHETIC TEST FIXTURE — Demo',synthetic_demo=True)
        ctx=personal.resolve(entry['workspace_id']);sources=[]
        with scope(ctx):
            for suffix in ('A','B'):
                path=PROJECT_ROOT/'tests/fixtures/personal_demo'/f'SYNTHETIC TEST FIXTURE {suffix}.pdf'
                if not path.is_file():raise HTTPException(503,'Synthetic fixtures unavailable; run scripts/create_personal_fixtures.py')
                source=await asyncio.to_thread(documents.upload,path.name,path.read_bytes());sources.append(source)
            report=await asyncio.to_thread(reindex)
        return {'workspace':entry,'documents':sources,'index_report':report,'notice':'SYNTHETIC TEST FIXTURE — not real institutional policy.'}

class LabelRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    action:StrictStr
    query:StrictStr|None=None
    gold_chunk_ids:list[StrictStr]=[]
    human_confirmed:bool=False

@router.get('/bench/candidates')
async def label_candidates():
    from bench.candidate_queries import candidates
    return {'candidates':await asyncio.to_thread(candidates)}

@router.post('/bench/candidates/generate')
async def generate_candidates():
    from bench.candidate_queries import generate
    try:return await generate()
    except ValueError as exc:raise HTTPException(422,str(exc))
    except Exception:raise HTTPException(503,'Candidate generation unavailable; no labels were verified or written.')

@router.post('/bench/candidates/{candidate_id}/label')
async def label(candidate_id:str,body:LabelRequest):
    from bench.candidate_queries import confirm
    try:return await asyncio.to_thread(confirm,candidate_id,**body.model_dump())
    except ValueError as exc:raise HTTPException(422,str(exc))
