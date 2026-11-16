from src.institutions import current,workspace_path
"""Approved-source state emulation in temporary storage; no MSRIT claims or live LLM."""
import importlib
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient
from src import authority,server,store
from src.llm import LLMResponse
from tests.grounding_helpers import fixture_reply


@pytest.mark.parametrize('mode',['raw','hyde','fusion'])
def test_http_index_retrieve_answer_cache_and_revoke(monkeypatch,mode):
    indexer=importlib.import_module('src.reindex')
    target=indexer.DATA_RAW_DIR/'review_emulation.txt'
    target.write_text('ISOLATED TEST FIXTURE ALPHA. This is not a university policy and asserts no student permissions. '*20)
    monkeypatch.setattr(indexer,'embed_texts',lambda texts:[[1.,0.] for _ in texts])
    assert indexer.reindex()['status']=='ok'
    assert store.query([1.,0.])==[]
    did=next(iter(authority.get_registry()))
    assert authority.approve_source(did)
    store.sync_authority_metadata()
    monkeypatch.setattr('src.retrieve.embed_single',lambda text:[1.,0.])
    observed=[]
    async def fake_chat(messages,**kwargs):
        if 'retrieval key' in messages[0]['content']:
            return LLMResponse('UNIQUE SYNTHETIC HYDE KEY for an isolated storage fixture.','fixture','fixture-model',2,3,4)
        text='\n'.join(m['content'] for m in messages)
        if messages[0]['content'].startswith('Review a proposed evidence selection'):
            import json
            text=json.loads(messages[1]['content'])['evidence']
        observed.append(text)
        assert 'UNIQUE SYNTHETIC HYDE KEY' not in text
        assert 'ISOLATED TEST FIXTURE ALPHA' in text
        import re,html
        from src.grounding import provisions
        excerpt=html.unescape(re.search(r'<provision id="P1">(.*?)</provision>',text,re.S)[1])
        return fixture_reply(messages,provisions(excerpt)[0])
    mock=AsyncMock(side_effect=fake_chat)
    monkeypatch.setattr('src.answer.get_llm_client',lambda:SimpleNamespace(chat=mock))
    monkeypatch.setattr('src.hyde.get_llm_client',lambda:SimpleNamespace(chat=mock))
    server._rate_windows.clear()
    with TestClient(server.app,headers={'Authorization':'Bearer isolated-test-admin'}) as client:
        first=client.post('/ask',json={'institution_id':current().institution_id,'question':'Where is the fixture marker?','mode':mode})
        assert first.status_code==200
        trace=first.json()
        assert trace['decision']=='answered' and not trace['cache_hit']
        assert trace['retrieved'][0]['approved'] is True
        assert trace['retrieved'][0]['extraction_method']=='text'
        assert trace['llm_usage']['answer']['model']=='fixture-model'
        assert observed
        calls=mock.await_count
        second=client.post('/ask',json={'institution_id':current().institution_id,'question':'Where is the fixture marker?','mode':mode}).json()
        assert second['cache_hit'] and second['retrieved'] and mock.await_count==calls
        assert authority.reject_source(did)
        third=client.post('/ask',json={'institution_id':current().institution_id,'question':'Where is the fixture marker?','mode':mode}).json()
        assert third['decision']=='abstained' and not third['cache_hit']
        assert mock.await_count==calls
