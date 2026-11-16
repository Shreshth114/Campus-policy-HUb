import pytest
from src.answer import validate_answer
from tests.test_guardrails import make_chunk


def test_unicode_citation_canonicalization():
    c=make_chunk(text='Attendance must be 75 percent.')
    assert validate_answer('Attendance must be 75 percent 【C1】.',[c])[0] is None

@pytest.mark.parametrize('label',['【C0】','【C99】','【source】'])
def test_unknown_citations_rejected(label):
    assert validate_answer('Attendance must be 75 percent '+label,[make_chunk()])[0]


def test_events_and_ambiguity():
    from src.query_intent import understand
    assert understand('I was sick and missed classes. Can I write finals?')['event']=='missed_classes'
    assert understand('I was sick and missed my exam')['event']=='missed_exam'
    assert understand('I was sick. What can I do?')['clarification']


def test_hyde_fact_invention_rejected():
    from src.hyde import safe_search_key
    assert not safe_search_key('Attendance must be 55% and apply within five days.','I missed classes')
    assert not safe_search_key('Approval from the Head of Department is required.','I missed classes')
    assert safe_search_key('Attendance shortage due to illness and medical absence documentation.','I missed classes')


@pytest.mark.asyncio
async def test_incomplete_generation_with_valid_citation_is_withheld(monkeypatch):
    from types import SimpleNamespace
    from unittest.mock import AsyncMock
    from src import answer
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=SimpleNamespace(text='Attendance is 75 percent [C1].',finish_reason='length'))))
    assert (await answer.generate_answer('attendance?', [make_chunk()]))[1]=='incomplete_generation'


@pytest.mark.asyncio
async def test_local_token_budget_refuses_oversized_request(monkeypatch):
    from src import llm
    monkeypatch.setenv('GROQ_TPM_BUDGET','100')
    with pytest.raises(llm.ProviderUnavailableError) as exc:
        await llm.reserve_groq_tokens([{'content':'test'}],200)
    assert exc.value.status_code==413


@pytest.mark.asyncio
async def test_groq_finish_reason_and_reasoning_metadata(monkeypatch):
    import httpx
    from src import llm
    def handler(request):
        import json
        assert json.loads(request.content)['reasoning_effort']=='low'
        return httpx.Response(200,json={'choices':[{'finish_reason':'length','message':{'content':'Fragment'}}], 'usage':{'completion_tokens':350,'completion_tokens_details':{'reasoning_tokens':340}}})
    client=httpx.AsyncClient
    monkeypatch.setattr(llm.httpx,'AsyncClient',lambda **kw:client(transport=httpx.MockTransport(handler),**kw))
    provider=llm.GroqProvider();provider.model='openai/gpt-oss-test';provider.api_key='test-only'
    r=await provider.chat([{'role':'user','content':'test'}])
    assert r.finish_reason=='length' and r.reasoning_tokens==340
