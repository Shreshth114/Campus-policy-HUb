"""Adapter request contracts and retry/failover using fake transports, never live keys."""
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import httpx
import pytest
from google.genai import errors
from src import llm
from src.llm import GeminiProvider, GroqProvider, LLMClient, LLMResponse


def response(text="Fixture output"):
    return LLMResponse(text, "fixture", "test-model", 1.2, 3, 4)


def provider(name, side_effect=None, configured=True):
    return SimpleNamespace(name=name, is_configured=lambda: configured,
                           chat=AsyncMock(side_effect=side_effect, return_value=response()))


@pytest.mark.asyncio
async def test_groq_payload_and_usage(monkeypatch):
    seen = []
    def handler(request):
        import json
        seen.append(json.loads(request.content))
        assert request.headers["Authorization"] == "Bearer test-only"
        return httpx.Response(200, json={"choices":[{"message":{"content":"Fixture answer"}}],
                                         "usage":{"prompt_tokens":8,"completion_tokens":5}})
    real_client = httpx.AsyncClient
    monkeypatch.setattr(llm.httpx, "AsyncClient", lambda **kw: real_client(
        transport=httpx.MockTransport(handler), **kw))
    p = GroqProvider()
    p.api_key, p.model = "test-only", "fixture-model"
    result = await p.chat([{"role":"user","content":"Fixture request"}], max_tokens=25, temperature=0.1)
    assert seen[0]["model"] == "fixture-model"
    assert seen[0]["max_tokens"] == 25
    assert result.text == "Fixture answer"
    assert (result.input_tokens, result.output_tokens) == (8,5)


@pytest.mark.asyncio
async def test_gemini_role_mapping_system_tokens_and_timeout(monkeypatch):
    fake = MagicMock()
    fake.models.generate_content.return_value = SimpleNamespace(
        text="Fixture Gemini answer", usage_metadata=SimpleNamespace(prompt_token_count=7,candidates_token_count=4))
    constructor = MagicMock(return_value=fake)
    monkeypatch.setattr(llm.genai,"Client",constructor)
    p = GeminiProvider()
    p.api_key, p.model = "test-only", "fixture-model"
    result = await p.chat([{"role":"system","content":"Fixture rules"},
                           {"role":"user","content":"First"},
                           {"role":"assistant","content":"Prior reply"}], max_tokens=35)
    assert constructor.call_args.kwargs["http_options"].timeout == 30000
    call = fake.models.generate_content.call_args.kwargs
    assert call["model"] == "models/fixture-model"
    assert [c["role"] for c in call["contents"]] == ["user","model"]
    assert call["config"].system_instruction == "Fixture rules"
    assert call["config"].max_output_tokens == 35
    assert result.output_tokens == 4
    assert result.provider == "gemini"


@pytest.mark.asyncio
@pytest.mark.parametrize("status,retries", [(429,3),(500,3),(504,3),(401,1),(403,1)])
async def test_http_failover_is_bounded(monkeypatch,status,retries):
    error = httpx.HTTPStatusError("fixture",request=httpx.Request("POST","https://example.invalid"),
                                  response=httpx.Response(status))
    client = LLMClient()
    client.primary, client.fallback = provider("primary",error), provider("fallback")
    sleep = AsyncMock()
    monkeypatch.setattr(llm.asyncio,"sleep",sleep)
    # Neutralise pacing so only backoff sleeps are counted
    monkeypatch.setattr(llm,"pace_provider",AsyncMock())
    result = await client.chat([{"role":"user","content":"fixture"}])
    assert result.text == "Fixture output"
    assert client.primary.chat.await_count == retries
    assert sleep.await_count == retries-1
    client.fallback.chat.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("status,count",[(429,3),(503,3),(400,1)])
async def test_gemini_errors_retry_only_transient(monkeypatch,status,count):
    client = LLMClient()
    client.primary = provider("gemini", errors.APIError(status,{"error":{"message":"test-only"}}))
    client.fallback = provider("fallback")
    monkeypatch.setattr(llm.asyncio,"sleep",AsyncMock())
    await client.chat([])
    assert client.primary.chat.await_count == count


@pytest.mark.asyncio
async def test_timeout_retries_then_fails_without_leaking_secrets(monkeypatch):
    client = LLMClient()
    client.primary = provider("primary",httpx.ReadTimeout("secret-key-must-not-escape"))
    client.fallback = provider("fallback",ValueError("secret-key-must-not-escape"))
    monkeypatch.setattr(llm.asyncio,"sleep",AsyncMock())
    with pytest.raises(RuntimeError,match="All configured LLM providers failed") as caught:
        await client.chat([])
    assert "secret-key" not in str(caught.value)
    assert client.primary.chat.await_count == 3
    assert client.fallback.chat.await_count == 1


@pytest.mark.asyncio
async def test_no_configured_provider():
    client = LLMClient()
    client.primary = provider("primary",configured=False)
    client.fallback = provider("fallback",configured=False)
    with pytest.raises(RuntimeError,match="No LLM provider configured"):
        await client.chat([])


@pytest.mark.asyncio
async def test_gemini_empty_content_rejected(monkeypatch):
    p = GeminiProvider()
    fake = MagicMock()
    fake.models.generate_content.return_value = SimpleNamespace(text="",usage_metadata=None)
    monkeypatch.setattr(p,"_get_client",lambda:fake)
    with pytest.raises(ValueError,match="empty"):
        await p.chat([])


def test_model_listing_filters_current_sdk_actions(monkeypatch):
    from scripts import list_models
    fake = MagicMock()
    fake.models.list.return_value = [SimpleNamespace(name="models/chat",supported_actions=["generateContent"]),
                                    SimpleNamespace(name="models/embed",supported_actions=["embedContent"])]
    monkeypatch.setitem(list_models.PROVIDERS,"gemini",{"api_key":"test-only"})
    monkeypatch.setattr(list_models.genai,"Client",lambda **kw:fake)
    assert list_models.list_gemini_models() == ["chat"]


@pytest.mark.parametrize('status',[400,401,404,429,503])
def test_http_diagnostics_include_status_and_redact_credentials(status):
    import json
    from src.llm import provider_error_details
    key='gsk_fake_diagnostic_test_key'
    body={'error':{'message':f'Fixture API error with {key}', 'code':'model_not_found'},
          'request':{'headers':{'Authorization':'Bearer fixture-auth-value'},'api_key':key},
          'other':'Bearer fixture-bearer-value'}
    request=httpx.Request('POST','https://example.invalid',headers={'Authorization':f'Bearer {key}'})
    response=httpx.Response(status,json=body,request=request)
    error=httpx.HTTPStatusError('Do not serialize this exception or request',request=request,response=response)
    details=provider_error_details(error,[key])
    output=json.dumps(details)
    assert details['status_code']==status
    assert details['error']=='HTTPStatusError'
    assert 'model_not_found' in details['response_body']
    assert key not in output and 'fixture-auth-value' not in output
    assert 'fixture-bearer-value' not in output and 'Bearer' not in output
    assert 'https://example.invalid' not in output


def test_plain_text_error_redacted_before_truncation():
    from src.llm import provider_error_details
    key='fixture-secret-that-straddles-the-output-limit'
    request=httpx.Request('POST','https://example.invalid')
    response=httpx.Response(502,text='x'*1990+key,request=request)
    exc=httpx.HTTPStatusError('ignored',request=request,response=response)
    result=provider_error_details(exc,[key])
    assert len(result['response_body'])<=2000
    assert 'fixture-secret' not in result['response_body']


def test_non_http_diagnostics_never_serialize_exception_text():
    from src.llm import provider_error_details
    result=provider_error_details(httpx.ConnectError('fixture secret must not escape'))
    assert result=={'error':'ConnectError'}


@pytest.mark.asyncio
async def test_unified_client_logs_sanitized_http_error(monkeypatch,capsys):
    request=httpx.Request('POST','https://example.invalid')
    response=httpx.Response(404,json={'error':{'code':'model_not_found','message':'fixture-secret'}},request=request)
    error=httpx.HTTPStatusError('private request data',request=request,response=response)
    client=LLMClient()
    client.primary=provider('primary',error)
    client.primary.api_key='fixture-secret'
    client.fallback=provider('fallback')
    await client.chat([])
    output=capsys.readouterr().out
    assert '404' in output and 'model_not_found' in output
    assert 'fixture-secret' not in output and 'private request data' not in output
