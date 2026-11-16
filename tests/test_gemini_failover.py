"""
Tests for Gemini failover provider, secure key handling, and immediate quota failover.
All tests here use mocks to avoid burning quota.
"""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import pytest

from src import llm
from src.llm import (
    LLMClient,
    LLMResponse,
    ProviderUnavailableError,
    provider_error_details,
    is_daily_quota_error,
)
from src.config import PROVIDERS, LLM_PRIMARY, LLM_FALLBACK


def test_provider_order_is_groq_then_gemini():
    """Verify configured provider order: Groq is primary, Gemini is fallback."""
    assert LLM_PRIMARY == "groq"
    assert LLM_FALLBACK == "gemini"
    client = LLMClient()
    assert client.primary.name == "groq"
    assert client.fallback.name == "gemini"


@pytest.mark.asyncio
async def test_failover_on_429(monkeypatch):
    """When primary provider returns 429 and exhausts retries, it routes to Gemini fallback."""
    req = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    resp_429 = httpx.Response(429, headers={"Retry-After": "1.0"}, request=req)
    err = httpx.HTTPStatusError("Rate limited", request=req, response=resp_429)

    monkeypatch.setattr(llm.asyncio, "sleep", AsyncMock())

    primary_chat = AsyncMock(side_effect=err)
    fallback_chat = AsyncMock(
        return_value=LLMResponse("Answer from Gemini", "gemini", "gemini-3.5-flash-lite", 120.0, 10, 5)
    )

    client = LLMClient()
    client.primary = SimpleNamespace(name="groq", is_configured=lambda: True, chat=primary_chat, api_key="test-key")
    client.fallback = SimpleNamespace(name="gemini", is_configured=lambda: True, chat=fallback_chat, api_key="test-gemini")

    res = await client.chat([{"role": "user", "content": "What is the policy?"}])
    assert res.text == "Answer from Gemini"
    assert res.provider == "gemini"
    assert res.failovers == 1
    assert primary_chat.await_count == 3
    fallback_chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_failover_on_daily_quota_immediate(monkeypatch):
    """Daily quota exhaustion (TPD/quota) must fail over immediately without waiting."""
    req = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    body = {"error": {"message": "Rate limit reached for model: limit 500000 tokens per day (TPD). Please try again tomorrow.", "type": "tokens"}}
    resp_quota = httpx.Response(429, json=body, request=req)
    err = httpx.HTTPStatusError("Quota reached", request=req, response=resp_quota)

    assert is_daily_quota_error(err)

    sleep_calls = []
    async def mock_sleep(s):
        sleep_calls.append(s)

    monkeypatch.setattr(llm.asyncio, "sleep", mock_sleep)
    # Neutralise pacing so only backoff sleeps are counted;
    # daily-quota failover must produce zero backoff sleeps
    monkeypatch.setattr(llm, "pace_provider", AsyncMock())

    primary_chat = AsyncMock(side_effect=err)
    fallback_chat = AsyncMock(
        return_value=LLMResponse("Answer from Gemini fallback", "gemini", "gemini-3.5-flash-lite", 90.0, 8, 4)
    )

    client = LLMClient()
    client.primary = SimpleNamespace(name="groq", is_configured=lambda: True, chat=primary_chat, api_key="test-key")
    client.fallback = SimpleNamespace(name="gemini", is_configured=lambda: True, chat=fallback_chat, api_key="test-gemini")

    res = await client.chat([{"role": "user", "content": "What are attendance rules?"}])
    assert res.text == "Answer from Gemini fallback"
    assert res.provider == "gemini"
    assert res.failovers == 1
    # MUST fail over on attempt 1 without waiting for retry backoff
    assert primary_chat.await_count == 1
    # Zero backoff sleep occurs on daily quota exhaustion
    assert len(sleep_calls) == 0
    fallback_chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_both_providers_down_raises_provider_unavailable(monkeypatch):
    """When both Groq and Gemini fail, raise ProviderUnavailableError (not policy abstention)."""
    req = httpx.Request("POST", "https://api.example.com")
    err = httpx.HTTPStatusError("Rate limited", request=req, response=httpx.Response(429, request=req))

    monkeypatch.setattr(llm.asyncio, "sleep", AsyncMock())

    primary_chat = AsyncMock(side_effect=err)
    fallback_chat = AsyncMock(side_effect=err)

    client = LLMClient()
    client.primary = SimpleNamespace(name="groq", is_configured=lambda: True, chat=primary_chat, api_key="test-key")
    client.fallback = SimpleNamespace(name="gemini", is_configured=lambda: True, chat=fallback_chat, api_key="test-gemini")

    with pytest.raises(ProviderUnavailableError) as exc_info:
        await client.chat([{"role": "user", "content": "Hello"}])

    assert "The AI provider is rate-limited" in str(exc_info.value)
    assert exc_info.value.status_code == 429
    assert exc_info.value.retry_after is not None


def test_key_redaction_in_diagnostics():
    """Ensure Gemini and Groq API keys are redacted in all diagnostics and logs."""
    fake_gemini_key = "AQ.TestFakeSecretKeyThatMustNeverLeak123456"
    fake_groq_key = "gsk_testGroqKeyThatMustNeverBePrintedInLogs123"

    req = httpx.Request("POST", f"https://generativelanguage.googleapis.com/v1beta/models?key={fake_gemini_key}")
    resp = httpx.Response(400, json={
        "error": {
            "message": f"API key {fake_gemini_key} is invalid",
            "details": f"Bearer {fake_groq_key}",
        }
    }, request=req)
    err = httpx.HTTPStatusError("Invalid key", request=req, response=resp)

    details = provider_error_details(err, secrets=[fake_gemini_key, fake_groq_key])
    out = str(details)
    assert fake_gemini_key not in out
    assert fake_groq_key not in out
    assert "[REDACTED]" in out


@pytest.mark.asyncio
async def test_health_check_never_prints_key(capsys):
    """Verify health_check reporting does not leak configured API keys."""
    from scripts.health_check import run_health_check
    from pathlib import Path

    output_path = Path("/tmp/test_health_report.md")
    # Run health check without live ping to check static report
    report = await run_health_check(workspace_id="test-workspace", output_path=output_path, live_ping=False)
    captured = capsys.readouterr()

    real_gemini_key = PROVIDERS.get("gemini", {}).get("api_key", "")
    real_groq_key = PROVIDERS.get("groq", {}).get("api_key", "")

    if real_gemini_key:
        assert real_gemini_key not in captured.out
        assert real_gemini_key not in captured.err
        if output_path.exists():
            assert real_gemini_key not in output_path.read_text()

    if real_groq_key:
        assert real_groq_key not in captured.out
        assert real_groq_key not in captured.err
        if output_path.exists():
            assert real_groq_key not in output_path.read_text()

    if output_path.exists():
        output_path.unlink()
