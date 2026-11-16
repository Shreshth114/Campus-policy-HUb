"""Tests for LLM reliability: 429 handling, Retry-After, exponential backoff,
concurrency limit, failover, and provider_unavailable decision.
"""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import pytest
from src import llm, pipeline
from src.llm import LLMClient, LLMResponse, ProviderUnavailableError, extract_retry_after, get_llm_semaphore
from src.retrieve import RetrievalResult
from src.store import RetrievedChunk


def make_chunk(chunk_id="c1", text="Students must maintain 75% attendance to take examinations.", doc_id="d1"):
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=text,
        doc_id=doc_id,
        doc_title="Attendance Policy",
        section="Section 3",
        page=2,
        chunk_index=0,
        similarity=0.92,
        workspace_id="test-ws",
        approved=True,
    )


@pytest.mark.asyncio
async def test_extract_retry_after_header_and_body():
    # Test HTTP header Retry-After
    req = httpx.Request("POST", "https://api.example.com")
    resp_header = httpx.Response(429, headers={"Retry-After": "18.5"}, request=req)
    err_header = httpx.HTTPStatusError("rate limited", request=req, response=resp_header)
    assert extract_retry_after(err_header) == 18.5

    # Test body JSON error message "Please try again in 14.2s."
    resp_body = httpx.Response(
        429,
        json={"error": {"message": "Rate limit exceeded. Please try again in 14.2s."}},
        request=req,
    )
    err_body = httpx.HTTPStatusError("rate limited", request=req, response=resp_body)
    assert extract_retry_after(err_body) == 14.2


@pytest.mark.asyncio
async def test_429_with_retry_after_honoured(monkeypatch):
    req = httpx.Request("POST", "https://api.example.com")
    resp = httpx.Response(429, headers={"Retry-After": "2.5"}, request=req)
    err = httpx.HTTPStatusError("rate limited", request=req, response=resp)

    sleep_calls = []

    async def mock_sleep(s):
        sleep_calls.append(s)

    monkeypatch.setattr(llm.asyncio, "sleep", mock_sleep)
    # Neutralise pacing so only backoff sleeps are counted
    monkeypatch.setattr(llm, "pace_provider", AsyncMock())

    mock_chat = AsyncMock(side_effect=[
        err,
        LLMResponse("Success after retry", "groq", "test-model", 100.0, 10, 5),
    ])

    client = LLMClient()
    client.primary = SimpleNamespace(
        name="groq",
        is_configured=lambda: True,
        chat=mock_chat,
    )
    client.fallback = SimpleNamespace(
        name="gemini",
        is_configured=lambda: False,
        chat=AsyncMock(),
    )

    res = await client.chat([{"role": "user", "content": "hello"}])
    assert res.text == "Success after retry"
    assert len(sleep_calls) == 1
    # Should sleep at least the 2.5s indicated in Retry-After
    assert sleep_calls[0] >= 2.5


@pytest.mark.asyncio
async def test_429_without_retry_after_uses_exponential_backoff(monkeypatch):
    req = httpx.Request("POST", "https://api.example.com")
    resp = httpx.Response(429, request=req)
    err = httpx.HTTPStatusError("rate limited", request=req, response=resp)

    sleep_calls = []

    async def mock_sleep(s):
        sleep_calls.append(s)

    monkeypatch.setattr(llm.asyncio, "sleep", mock_sleep)
    # Neutralise pacing so only backoff sleeps are counted
    monkeypatch.setattr(llm, "pace_provider", AsyncMock())

    mock_chat = AsyncMock(side_effect=[
        err,
        err,
        LLMResponse("Success after two retries", "groq", "test-model", 100.0, 10, 5),
    ])

    client = LLMClient()
    client.primary = SimpleNamespace(
        name="groq",
        is_configured=lambda: True,
        chat=mock_chat,
    )
    client.fallback = SimpleNamespace(
        name="gemini",
        is_configured=lambda: False,
        chat=AsyncMock(),
    )

    res = await client.chat([{"role": "user", "content": "hello"}])
    assert res.text == "Success after two retries"
    assert len(sleep_calls) == 2
    # Second wait should be strictly larger than first (exponential growth)
    assert sleep_calls[1] > sleep_calls[0]


@pytest.mark.asyncio
async def test_failover_to_fallback_when_primary_exhausted(monkeypatch):
    req = httpx.Request("POST", "https://api.example.com")
    resp = httpx.Response(429, request=req)
    err = httpx.HTTPStatusError("rate limited", request=req, response=resp)

    monkeypatch.setattr(llm.asyncio, "sleep", AsyncMock())

    primary_chat = AsyncMock(side_effect=err)
    fallback_chat = AsyncMock(return_value=LLMResponse("Fallback response", "gemini", "gemini-model", 150.0, 8, 4))

    client = LLMClient()
    client.primary = SimpleNamespace(name="groq", is_configured=lambda: True, chat=primary_chat)
    client.fallback = SimpleNamespace(name="gemini", is_configured=lambda: True, chat=fallback_chat)

    res = await client.chat([{"role": "user", "content": "hello"}])
    assert res.text == "Fallback response"
    assert res.provider == "gemini"
    assert primary_chat.await_count == 3
    fallback_chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_provider_outage_yields_provider_unavailable_in_pipeline(monkeypatch):
    # Simulated provider outage in pipeline.ask()
    monkeypatch.setattr(pipeline, "retrieve", AsyncMock(return_value=RetrievalResult(chunks=[make_chunk()])))
    monkeypatch.setattr(pipeline, "valid_cached_citations", lambda c: True)

    exc = ProviderUnavailableError(
        "The AI provider is rate-limited. Retrying in 22 seconds",
        provider="groq",
        status_code=429,
        retry_after=22.0,
    )
    monkeypatch.setattr(pipeline, "generate_answer", AsyncMock(side_effect=exc))

    trace = await pipeline.ask("What is the attendance requirement?", use_cache=False)
    # Must NEVER be reported as policy abstention
    assert trace.decision == "provider_unavailable"
    assert trace.abstain_reason is None
    assert trace.retry_after_s == 22.0
    assert "rate-limited" in trace.error
    assert "Retrying in 22 seconds" in trace.answer


@pytest.mark.asyncio
async def test_concurrency_semaphore_limits_parallelism():
    sem = get_llm_semaphore()
    initial_value = sem._value

    active_tasks = 0
    max_active_observed = 0

    async def simulated_call():
        nonlocal active_tasks, max_active_observed
        async with sem:
            active_tasks += 1
            max_active_observed = max(max_active_observed, active_tasks)
            await asyncio.sleep(0.05)
            active_tasks -= 1

    tasks = [asyncio.create_task(simulated_call()) for _ in range(8)]
    await asyncio.gather(*tasks)

    # Concurrency should never exceed initial semaphore value
    assert max_active_observed <= initial_value
