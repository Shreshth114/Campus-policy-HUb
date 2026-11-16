import json
"""Search-key cache correctness and fallback behavior with fake providers."""
from unittest.mock import AsyncMock
import pytest
from src import hyde
from src.llm import LLMResponse
from src.retrieve import retrieve
from types import SimpleNamespace


@pytest.mark.asyncio
async def test_cache_keys_include_prompt_and_no_cache_bypasses(monkeypatch):
    fake=AsyncMock(return_value=LLMResponse('Synthetic fixture search key, never a policy.','test','fixture',10,4,5))
    monkeypatch.setattr(hyde,'get_llm_client',lambda:SimpleNamespace(chat=fake))
    a=await hyde.generate_hyde('fixture question')
    b=await hyde.generate_hyde('fixture question')
    assert a[0]==b[0] and fake.await_count==1
    assert b[1].latency_ms==0
    monkeypatch.setattr(hyde,'HYDE_SYSTEM_PROMPT',hyde.HYDE_SYSTEM_PROMPT+' revision')
    await hyde.generate_hyde('fixture question')
    assert fake.await_count==2
    token=hyde.cache_enabled.set(False)
    try: await hyde.generate_hyde('fixture question')
    finally: hyde.cache_enabled.reset(token)
    assert fake.await_count==3


@pytest.mark.asyncio
@pytest.mark.parametrize('text',['','short','    '])
async def test_empty_hyde_not_cached(monkeypatch,text):
    fake=AsyncMock(return_value=LLMResponse(text,'test','fixture',1))
    monkeypatch.setattr(hyde,'get_llm_client',lambda:SimpleNamespace(chat=fake))
    with pytest.raises(ValueError): await hyde.generate_hyde('fixture')
    assert json.loads(hyde.HYDE_CACHE_PATH.read_text()) == {}


@pytest.mark.asyncio
async def test_empty_corpus_never_loads_embeddings(monkeypatch):
    def fail(*args): raise AssertionError('No model downloads allowed')
    monkeypatch.setattr('src.retrieve.embed_single',fail)
    for mode in ('raw','hyde','fusion'):
        assert (await retrieve('fixture',mode=mode)).chunks==[]
