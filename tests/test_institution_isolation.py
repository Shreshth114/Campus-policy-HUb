"""Two temporary institutions; fixtures emulate review states, never university claims."""
import asyncio
import importlib
import json
from dataclasses import asdict
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pymupdf
import pytest
from fastapi.testclient import TestClient
from src import institutions as tenants, documents, authority, store, cache, server, hyde
from src.ingest import ingest_file
from src.retrieve import retrieve
from src.answer import confidence_gate, check_citations
from src.llm import LLMResponse


def pdf(marker):
    doc=pymupdf.open();page=doc.new_page();page.insert_text((50,50),'SYNTHETIC ISOLATION FIXTURE '+marker+' '+('marker text. '*20));return doc.tobytes()

@pytest.fixture
def pair(monkeypatch):
    a=tenants.current();b=tenants.resolve(tenants.create_institution('Synthetic College B','college-b')['institution_id'])
    results=[]
    for ctx,marker in [(a,'ALPHA'),(b,'BETA')]:
        with tenants.scope(ctx):
            entry=documents.upload('handbook.pdf',pdf(marker))
            chunks=ingest_file(__import__('pathlib').Path(entry['source_path']))
            store.upsert_chunks([c.chunk_id for c in chunks],[c.text for c in chunks],[[1.,0.] for c in chunks],[c.to_metadata() for c in chunks])
            documents.set_index_status(entry['doc_id'],'indexed',len(chunks))
            documents.review(entry['doc_id'],entry['version_id'],'approved',{'reviewer':'fixture operator','source_url':'https://example.invalid/synthetic','issuing_authority':'synthetic review emulation'})
            results.append((entry,chunks))
    monkeypatch.setattr('src.retrieve.embed_single',lambda text:[1.,0.])
    monkeypatch.setattr('src.retrieve.generate_hyde',AsyncMock(return_value=('Hypothetical search aid only.',SimpleNamespace(provider='fixture'))))
    return a,b,results

def test_same_filename_different_identity(pair):
    a,b,rows=pair
    assert rows[0][0]['doc_id']!=rows[1][0]['doc_id']
    assert set(c.chunk_id for c in rows[0][1]).isdisjoint(c.chunk_id for c in rows[1][1])
    assert all(r[0]['original_filename']=='handbook.pdf' for r in rows)

@pytest.mark.asyncio
@pytest.mark.parametrize('mode',['raw','hyde','fusion'])
async def test_same_question_all_modes(pair,mode):
    a,b,_=pair
    for ctx,marker in [(a,'ALPHA'),(b,'BETA')]:
        with tenants.scope(ctx):
            result=await retrieve('Where is the marker?',mode)
            assert result.chunks and all(c.institution_id==ctx.institution_id and marker in c.text for c in result.chunks)

@pytest.mark.parametrize('production',[True,False])
def test_foreign_high_similarity_and_filter_escape(pair,production):
    a,b,rows=pair
    with tenants.scope(a):
        assert store.query([1.,0.],where={'institution_id':b.institution_id},production=production)==[]
        assert {c.institution_id for c in store.query([1.,0.],top_k=100,production=production)}=={a.institution_id}

@pytest.mark.asyncio
async def test_fallback_scope(pair,monkeypatch):
    a,b,_=pair
    monkeypatch.setattr('src.retrieve.generate_hyde',AsyncMock(side_effect=RuntimeError('offline')))
    with tenants.scope(b):
        result=await retrieve('Where is the marker?','hyde');assert result.hyde_failed
        assert result.chunks and all(c.institution_id==b.institution_id for c in result.chunks)

def test_foreign_citations_rejected_before_generation(pair):
    a,b,rows=pair
    with tenants.scope(a):
        foreign=store.RetrievedChunk('foreign','foreign','foreign','Foreign','1',1,0,.99,institution_id=b.institution_id,approved=True)
        assert confidence_gate([foreign])==(False,'foreign_evidence')
        assert check_citations('text [C1]',[foreign])==(False,[])
        assert not store.valid_cached_citations([rows[1][1][0].chunk_id])

@pytest.mark.parametrize('status',['pending','rejected'])
def test_review_independence(pair,status):
    a,b,rows=pair
    with tenants.scope(a):
        documents.review(rows[0][0]['doc_id'],rows[0][0]['version_id'],status,{'reviewer':'test'})
        assert store.query([1.,0.])==[]
    with tenants.scope(b): assert store.query([1.,0.])

def test_answer_cache_and_clear_are_isolated(pair):
    a,b,rows=pair
    for ctx,row in zip((a,b),rows):
        with tenants.scope(ctx):cache.cache_store('identical question',ctx.institution_id,[row[1][0].chunk_id],[row[0]['doc_id']])
    with tenants.scope(a):
        assert cache.cache_lookup('identical question')['answer']==a.institution_id
        cache.clear_cache()
    with tenants.scope(b): assert cache.cache_lookup('identical question')['answer']==b.institution_id

@pytest.mark.asyncio
async def test_hyde_cache_isolated(pair,monkeypatch):
    a,b,_=pair
    chat=AsyncMock(return_value=LLMResponse('Synthetic hypothetical search passage only.','test','test',1))
    monkeypatch.setattr(hyde,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    for ctx in (a,b,a):
        with tenants.scope(ctx):await hyde.generate_hyde('same query')
    assert chat.await_count==2

def test_replacement_pending_history_and_other_tenant_unchanged(pair):
    a,b,rows=pair
    with tenants.scope(b):before=json.dumps(authority.get_registry(),sort_keys=True)
    with tenants.scope(a):
        new=documents.upload('handbook.pdf',pdf('REPLACED'),rows[0][0]['doc_id'])
        assert new['authority_status']=='pending' and new['history']
        assert __import__('pathlib').Path(rows[0][0]['source_path']).is_file()
        assert store.query([1.,0.])==[]
    with tenants.scope(b):assert json.dumps(authority.get_registry(),sort_keys=True)==before and store.query([1.,0.])

def test_reindex_and_remove_are_scoped(pair,monkeypatch):
    a,b,rows=pair;indexer=importlib.import_module('src.reindex')
    monkeypatch.setattr(indexer,'embed_texts',lambda texts:[[1.,0.] for _ in texts])
    with tenants.scope(b):before=store.get_collection_count()
    with tenants.scope(a):
        assert indexer.reindex()['status']=='ok'
        documents.remove(rows[0][0]['doc_id'])
        assert not store.query([1.,0.])
    with tenants.scope(b):assert store.get_collection_count()==before and store.query([1.,0.])

@pytest.mark.parametrize('field',['is_decoy','is_synthetic'])
def test_poisoned_chunks_excluded(pair,field):
    a,b,rows=pair
    with tenants.scope(a):
        meta=rows[0][1][0].to_metadata();meta.update({field:True,'approved':True})
        store.upsert_chunks(['poison'],['Poison'],[[1.,0.]],[meta])
        assert 'poison' not in {c.chunk_id for c in store.query([1.,0.],top_k=100)}

def test_no_context_fails_closed():
    with tenants.scope(None):
        with pytest.raises(ValueError):store.query([1.,0.],production=False)
        with pytest.raises(ValueError):cache.cache_lookup('query')

@pytest.mark.parametrize('body',[{'question':'q'},{'institution_id':'unknown','question':'q'}])
def test_api_requires_valid_institution(body):
    server._rate_windows.clear()
    with TestClient(server.app) as client:assert client.post('/ask',json=body).status_code==422

def test_admin_authentication_and_foreign_ownership(pair):
    a,b,rows=pair;server._rate_windows.clear()
    path=f'/admin/institutions/{a.institution_id}/sources/{rows[1][0]["doc_id"]}'
    with TestClient(server.app) as client:
        assert client.delete(path).status_code==401
        assert client.delete(path,headers={'Authorization':'Bearer isolated-test-admin'}).status_code==404
        assert client.get(path,headers={'Authorization':'Bearer isolated-test-admin'}).status_code==404
        assert client.get('/admin/institutions').status_code==401

def test_upload_review_api_and_publication(monkeypatch):
    ctx=tenants.current();server._rate_windows.clear()
    headers={'Authorization':'Bearer isolated-test-admin'}
    with TestClient(server.app,headers=headers) as client:
        base=f'/admin/institutions/{ctx.institution_id}'
        response=client.post(base+'/documents',files=[('files',('new.pdf',pdf('UPLOAD'),'application/pdf'))])
        assert response.status_code==200
        source=response.json()['documents'][0]['source'];assert source['authority_status']=='pending'
        assert client.get(base+'/sources/'+source['doc_id']).json()['pages']
        assert client.get(base+'/sources/'+source['doc_id']+'/original').content.startswith(b'%PDF-')
        assert client.patch(base,json={'published':True}).status_code==409
        assert client.post(base+'/sources/'+source['doc_id']+'/approve',json={'version_id':source['version_id'],'reviewer':'fixture'}).status_code==409

@pytest.mark.asyncio
async def test_benchmark_labels_scoped_and_unverified(pair):
    from bench.run_benchmark import load_queries,run_benchmark
    a,b,_=pair
    with tenants.scope(a):
        query={'id':'q','query':'same','institution_id':a.institution_id,'labels_verified':False,'gold_chunk_ids':[]}
        a.path('queries').write_text(json.dumps(query)+'\n')
        result=await run_benchmark();assert not result['metadata']['labels_verified'] and not result['retrieval_metrics']
        query['institution_id']=b.institution_id;a.path('queries').write_text(json.dumps(query))
        with pytest.raises(ValueError,match='Foreign'):load_queries()
    with tenants.scope(b):assert load_queries()==[]

def test_interrupted_staged_migration_is_idempotent(pair,monkeypatch):
    from src.migrate_legacy import stage_records
    a,b,rows=pair
    with tenants.scope(a):
        entries=authority.get_registry()
        for e in entries.values():e['authority_status']='pending';e['approved_at']=None
        records=store.get_collection().get(where={'institution_id':a.institution_id},include=['documents','metadatas','embeddings'])
    target=tenants.resolve(tenants.create_institution('Migration fixture','migration-fixture')['institution_id'])
    mapping={'documents':{did:target.institution_id+':'+str(__import__('uuid').uuid4()) for did in entries}}
    original=store.upsert_chunks
    def interrupted(ids,texts,vectors,metadatas):
        original(ids[:1],texts[:1],vectors[:1],metadatas[:1]);raise KeyboardInterrupt()
    monkeypatch.setattr(store,'upsert_chunks',interrupted)
    with pytest.raises(KeyboardInterrupt):stage_records(target,entries,records,mapping)
    monkeypatch.setattr(store,'upsert_chunks',original)
    first=stage_records(target,entries,records,mapping)
    second=stage_records(target,entries,records,mapping)
    assert first==second
    with tenants.scope(target):
        assert store.get_collection_count()==len(records['ids'])
        assert all(e['authority_status']=='pending' for e in authority.get_registry().values())
    with tenants.scope(a):assert store.get_collection_count()==len(records['ids'])


def test_api_conflicting_scope_cannot_select_another_tenant(pair):
    a,b,_=pair;server._rate_windows.clear()
    with TestClient(server.app) as client:
        assert client.post('/ask?institution_id='+a.institution_id,json={'institution_id':b.institution_id,'question':'marker'}).status_code==422


def test_global_reset_is_disabled(pair):
    a,b,_=pair
    with tenants.scope(a):
        with pytest.raises(ValueError):store.reset_collection()
    with tenants.scope(b):assert store.query([1.,0.])


def test_replacement_during_embedding_does_not_mark_new_version_indexed(pair,monkeypatch):
    a,b,rows=pair;indexer=importlib.import_module('src.reindex')
    def replacing_embed(texts):
        documents.upload('handbook.pdf',pdf('NEW VERSION DURING EMBEDDING'),rows[0][0]['doc_id'])
        return [[1.,0.] for _ in texts]
    monkeypatch.setattr(indexer,'embed_texts',replacing_embed)
    with tenants.scope(a):
        report=indexer.reindex()
        assert report['status']=='partial_failure'
        entry=authority.get_registry()[rows[0][0]['doc_id']]
        assert entry['authority_status']=='pending' and entry['extraction_status']=='pending'
        assert store.query([1.,0.])==[]
    with tenants.scope(b):assert store.query([1.,0.])
