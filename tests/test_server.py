from src.institutions import current,workspace_path
"""Exercise every HTTP endpoint, validation and unavailable-dependency paths."""
import asyncio
from threading import Event
from unittest.mock import AsyncMock
import httpx
import pytest
from fastapi.testclient import TestClient
from src import server
from src.trace import Trace


@pytest.fixture
def client(monkeypatch,tmp_path):
    server._rate_windows.clear()
    monkeypatch.setattr(server,"BENCH_RESULTS_DIR",tmp_path / "results")
    with TestClient(server.app,headers={'Authorization':'Bearer isolated-test-admin'}) as client:
        yield client


@pytest.mark.parametrize("endpoint",["/ask","/compare"])
@pytest.mark.parametrize("body",[{},[],{"question":None},{"question":5},{"question":" "},
                                {"question":"valid","mode":"bad"},{"question":"\x00"},
                                {"question":"valid","unexpected":True}])
def test_question_validation(client,endpoint,body):
    assert client.post(endpoint,json=body).status_code == 422


def test_json_and_size_validation(client):
    assert client.post('/ask',content='{',headers={'Content-Type':'application/json'}).status_code == 422
    assert client.post('/ask',json={'institution_id':current().institution_id,'question':'x'*9000}).status_code == 413


def test_long_and_nonenglish_input(client,monkeypatch):
    fake = AsyncMock(return_value=Trace(question='fixture',mode='raw'))
    monkeypatch.setattr(server,'ask',fake)
    assert client.post('/ask',json={'institution_id':current().institution_id,'question':'x'*700,'mode':'raw'}).status_code == 200
    assert len(fake.call_args.kwargs['question']) == 500
    assert client.post('/ask',json={'institution_id':current().institution_id,'question':'ನಿಯಮಗಳು ಏನು?','mode':'raw'}).status_code == 200


def test_empty_corpus_end_to_end(client,monkeypatch):
    forbidden = AsyncMock(side_effect=AssertionError('Must not call LLM with empty corpus'))
    monkeypatch.setattr('src.retrieve.generate_hyde',forbidden)
    response = client.post('/ask',json={'institution_id':current().institution_id,'question':'Is there an approved policy?'})
    assert response.status_code == 200
    assert response.json()['decision'] == 'abstained'
    assert response.json()['abstain_reason'] == 'no_chunks_retrieved'
    forbidden.assert_not_called()
    compare = client.post('/compare',json={'institution_id':current().institution_id,'question':'policy?'})
    assert compare.status_code == 200
    assert compare.json()['raw']['chunks'] == []
    assert compare.json()['hyde']['chunks'] == []


def test_health_sources_cache_and_static_files(client):
    health = client.get('/health?institution_id='+current().institution_id).json()
    assert health['status'] == 'ok' and health['production_ready'] is False
    assert 'api_key' not in str(health)
    assert client.get('/sources?institution_id='+current().institution_id).json() == {'sources':[]}
    assert client.get('/cache/stats?institution_id='+current().institution_id).status_code == 200
    assert client.post('/cache/clear?institution_id='+current().institution_id).json() == {'cleared':0}
    page = client.get('/')
    assert page.status_code == 200 and 'Sources & index' in page.text
    assert client.get('/app.js').status_code == 200
    assert client.get('/bench/status?institution_id='+current().institution_id).json()['verified_labels'] == 0


def test_rate_limit(client,monkeypatch):
    monkeypatch.setattr(server,'RATE_LIMIT',2)
    for _ in range(2):
        assert client.post('/cache/clear?institution_id='+current().institution_id).status_code == 200
    assert client.post('/cache/clear?institution_id='+current().institution_id).status_code == 429
    assert client.get('/health?institution_id='+current().institution_id).status_code == 200


def test_storage_failure_is_safe(client,monkeypatch):
    def fail(): raise RuntimeError('secret-path')
    monkeypatch.setattr(server,'get_collection_count',fail)
    response=client.get('/health?institution_id='+current().institution_id)
    assert response.status_code == 503 and 'secret-path' not in response.text
    monkeypatch.setattr(server,'reindex',fail)
    assert client.post('/reindex?institution_id='+current().institution_id).status_code == 503


def test_reindex_empty_and_benchmark_files(client,tmp_path):
    assert client.post('/reindex?institution_id='+current().institution_id).json()['chunks_added'] == 0
    assert client.get('/bench/results/latest.json?institution_id='+current().institution_id).status_code == 404
    assert client.get('/bench/results/source_registry.json?institution_id='+current().institution_id).status_code == 404
    server.BENCH_RESULTS_DIR=workspace_path("results")
    (server.BENCH_RESULTS_DIR/'latest.json').write_text('{"metadata":{"status":"pending"}}')
    assert client.get('/bench/results/latest.json?institution_id='+current().institution_id).status_code == 200
    external=tmp_path/'private.json'
    external.write_text('{"secret":true}')
    (server.BENCH_RESULTS_DIR/'latest.json').unlink()
    (server.BENCH_RESULTS_DIR/'latest.json').symlink_to(external)
    assert client.get('/bench/results/latest.json?institution_id='+current().institution_id).status_code == 404


def test_compare_partial_failure(client,monkeypatch):
    from src.retrieve import RetrievalResult
    async def search(question,mode,production):
        if mode=='hyde': raise RuntimeError('secret')
        return RetrievalResult(mode='raw')
    monkeypatch.setattr(server,'retrieve',search)
    response=client.post('/compare',json={'institution_id':current().institution_id,'question':'fixture'})
    assert response.status_code==200
    assert response.json()['raw']['chunks']==[]
    assert response.json()['hyde']['error']=='Retrieval unavailable'
    assert 'secret' not in response.text


@pytest.mark.asyncio
async def test_concurrent_reindex_returns_conflict(monkeypatch):
    started, finish = Event(), Event()
    def work():
        started.set()
        assert finish.wait(5)
        return {'status':'ok'}
    monkeypatch.setattr(server,'reindex',work)
    server._rate_windows.clear()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://test',headers={'Authorization':'Bearer isolated-test-admin'}) as client:
        first=asyncio.create_task(client.post('/reindex?institution_id='+current().institution_id))
        try:
            assert await asyncio.to_thread(started.wait,3)
            second=await client.post('/reindex?institution_id='+current().institution_id)
            assert second.status_code==409
        finally:
            finish.set()
        assert (await first).status_code==200


def test_cache_errors_have_safe_http_responses(client,monkeypatch):
    def fail(): raise OSError('private-location')
    monkeypatch.setattr(server,'clear_cache',fail)
    monkeypatch.setattr(server,'get_cache_stats',fail)
    for method,path in [('post','/cache/clear?institution_id='+current().institution_id),('get','/cache/stats?institution_id='+current().institution_id)]:
        response=getattr(client,method)(path if '?' in path else path+'?institution_id='+current().institution_id)
        assert response.status_code==503 and 'private-location' not in response.text


def test_unexpected_pipeline_failure_is_safe(client,monkeypatch):
    monkeypatch.setattr(server,'ask',AsyncMock(side_effect=OSError('private-location')))
    response=client.post('/ask',json={'institution_id':current().institution_id,'question':'fixture'})
    assert response.status_code==503 and 'private-location' not in response.text
