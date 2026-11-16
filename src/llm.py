"""
llm.py — Unified LLM client with Groq (OpenAI-format) and Gemini (Google SDK) providers.

Design decision D-001: Separate adapter per provider behind a unified interface.
Retry with exponential backoff on 429/5xx; failover to fallback provider.
"""

import time
import asyncio
import json
import random
import os
import re
from dataclasses import dataclass
from typing import Optional

import httpx
from google import genai
from google.genai import errors as genai_errors

from src.config import PROVIDERS, LLM_PRIMARY, LLM_FALLBACK, LLM_MAX_CONCURRENCY, LLM_TOTAL_WAIT_BUDGET


class ProviderUnavailableError(RuntimeError):
    """Raised when all configured LLM providers fail or are rate-limited.

    Never reported as a policy-level abstention.
    """
    def __init__(self, message: str, provider: str = "", status_code: Optional[int] = None,
                 retry_after: Optional[float] = None, details: str = ""):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code
        self.retry_after = retry_after
        self.details = details


class EmptyGenerationError(ValueError):
    def __init__(self, finish_reason=None, reasoning_tokens=None):
        super().__init__('Provider returned empty content')
        self.finish_reason=finish_reason
        self.reasoning_tokens=reasoning_tokens


def extract_retry_after(exc: Exception) -> Optional[float]:
    """Extract Retry-After value from HTTP headers or provider response text."""
    if isinstance(exc, httpx.HTTPStatusError):
        hdr = exc.response.headers.get("retry-after") or exc.response.headers.get("Retry-After")
        if hdr:
            try:
                return max(0.5, float(hdr))
            except (ValueError, TypeError):
                pass
        try:
            body = exc.response.text
            m1 = re.search(r"try again in (?:(\d+)m)?(\d+(?:\.\d+)?)s", body, re.IGNORECASE)
            if m1:
                mins = float(m1.group(1) or 0)
                secs = float(m1.group(2) or 0)
                return max(0.5, mins * 60 + secs)
            m = re.search(r"try again in (\d+(?:\.\d+)?)\s*(s|sec|seconds|ms)", body, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                if m.group(2).lower() == "ms":
                    val /= 1000.0
                return max(0.5, val)
        except Exception:
            pass
    elif isinstance(exc, genai_errors.APIError):
        try:
            body = str(exc)
            m1 = re.search(r"try again in (?:(\d+)m)?(\d+(?:\.\d+)?)s", body, re.IGNORECASE)
            if m1:
                mins = float(m1.group(1) or 0)
                secs = float(m1.group(2) or 0)
                return max(0.5, mins * 60 + secs)
            m = re.search(r"try again in (\d+(?:\.\d+)?)\s*(s|sec|seconds|ms)", body, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                if m.group(2).lower() == "ms":
                    val /= 1000.0
                return max(0.5, val)
        except Exception:
            pass
    return None


_PROVIDER_SEMAPHORES: dict[str, asyncio.Semaphore] = {}
_PROVIDER_LAST_CALL: dict[str, float] = {}


def get_provider_semaphore(provider_name: str) -> asyncio.Semaphore:
    if provider_name not in _PROVIDER_SEMAPHORES:
        _PROVIDER_SEMAPHORES[provider_name] = asyncio.Semaphore(LLM_MAX_CONCURRENCY)
    return _PROVIDER_SEMAPHORES[provider_name]


def get_llm_semaphore() -> asyncio.Semaphore:
    return get_provider_semaphore("global")


async def pace_provider(provider_name: str, min_interval_s: float = 0.1) -> None:
    now = time.monotonic()
    last = _PROVIDER_LAST_CALL.get(provider_name, 0.0)
    elapsed = now - last
    if elapsed < min_interval_s:
        await asyncio.sleep(min_interval_s - elapsed)
    _PROVIDER_LAST_CALL[provider_name] = time.monotonic()


_GROQ_RESERVATIONS = []
_GROQ_RESERVATION_LOCK = asyncio.Lock()

async def reserve_groq_tokens(messages, max_tokens):
    """Conservative process-local rolling budget; reserve retries as real requests."""
    budget = int(os.getenv('GROQ_TPM_BUDGET', '8000'))
    estimate = sum(len(m.get('content','').encode()) for m in messages)//3 + max_tokens + 100
    if estimate > budget:
        raise ProviderUnavailableError('Request exceeds local token budget', provider='groq', status_code=413)
    async with _GROQ_RESERVATION_LOCK:
        while True:
            now=time.monotonic()
            _GROQ_RESERVATIONS[:] = [(t,n) for t,n in _GROQ_RESERVATIONS if now-t<60]
            if sum(n for _,n in _GROQ_RESERVATIONS)+estimate <= budget:
                _GROQ_RESERVATIONS.append((now,estimate));return
            wait=60-(now-_GROQ_RESERVATIONS[0][0])
            if wait>LLM_TOTAL_WAIT_BUDGET:
                raise ProviderUnavailableError('Local token budget busy; retry later',provider='groq',status_code=429,retry_after=wait)
            await asyncio.sleep(max(.1,wait))


def is_daily_quota_error(exc: Exception) -> bool:
    """Detect daily quota or hard limit exhaustion that should fail over immediately."""
    text = ""
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            text = exc.response.text
        except Exception:
            pass
    elif isinstance(exc, genai_errors.APIError):
        text = str(exc)
    else:
        text = str(exc)

    lower = text.lower()
    return bool(
        "daily" in lower
        or "tpd" in lower
        or "tokens per day" in lower
        or "requests per day" in lower
        or "day limit" in lower
        or "limit: 0" in lower
    )


def provider_error_details(exc: Exception, secrets=()) -> dict:
    """HTTP diagnostics without request headers, URLs, or credential values."""
    details = {"error": type(exc).__name__}
    if isinstance(exc, EmptyGenerationError):
        details.update(finish_reason=exc.finish_reason,reasoning_tokens=exc.reasoning_tokens)
        return details
    if isinstance(exc, ProviderUnavailableError):
        details.update(provider=exc.provider, status_code=exc.status_code, retry_after_s=exc.retry_after, details=exc.details)
        return details
    if not isinstance(exc, httpx.HTTPStatusError):
        return details
    details["status_code"] = exc.response.status_code
    credentials = [cfg.get("api_key", "") for cfg in PROVIDERS.values()]
    credentials.extend(secrets)

    def redact_text(value):
        for secret in credentials:
            if secret:
                value = value.replace(secret, "[REDACTED]")
        value = re.sub(r"\bgsk_[A-Za-z0-9_-]+", "[REDACTED]", value)
        value = re.sub(r"\bAQ\.[A-Za-z0-9_-]+", "[REDACTED]", value)
        value = re.sub(r"\bAIza[A-Za-z0-9_-]+", "[REDACTED]", value)
        value = re.sub(r"(?i)\bbearer\s+[^\s\"'<>]+", "[REDACTED]", value)
        value = re.sub(r"(?im)^.*authorization\s*[:=].*$", "[REDACTED]", value)
        return value

    def redact(value):
        if isinstance(value, dict):
            return {key: "[REDACTED]" if key.lower().replace("-", "_") in {
                "authorization", "headers", "api_key", "apikey", "x_api_key",
                "token", "access_token", "refresh_token",
            } else redact(item) for key, item in value.items()}
        if isinstance(value, list):
            return [redact(item) for item in value]
        return redact_text(value) if isinstance(value, str) else value

    try:
        body = json.dumps(redact(exc.response.json()), ensure_ascii=False)
    except ValueError:
        body = redact_text(exc.response.text)
    except httpx.ResponseNotRead:
        body = "[Response body unavailable]"
    # Sanitize before truncation so a truncated secret cannot escape redaction.
    details["response_body"] = redact_text(body)[:2000]
    return details


@dataclass
class LLMResponse:
    """Response from an LLM call with metadata."""
    text: str
    provider: str
    model: str
    latency_ms: float
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cached: bool = False
    tokens_estimated_before: Optional[int] = None
    tokens_estimated_after: Optional[int] = None
    failovers: int = 0
    finish_reason: Optional[str] = None
    reasoning_tokens: Optional[int] = None


class GroqProvider:
    """OpenAI-compatible chat completions for Groq."""

    def __init__(self):
        cfg = PROVIDERS["groq"]
        self.api_key = cfg["api_key"]
        self.model = cfg["model"]
        self.base_url = cfg["base_url"]
        self.name = "groq"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.model)

    async def chat(self, messages: list[dict], max_tokens: int = 300,
                   temperature: float = 0.3) -> LLMResponse:
        t0 = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    **({'reasoning_effort':'low'} if self.model.startswith('openai/gpt-oss-') else {}),
                },
            )
            resp.raise_for_status()
            data = resp.json()

        latency = (time.time() - t0) * 1000
        usage = data.get("usage", {})
        choice = data['choices'][0]
        text = choice['message'].get('content')
        if not isinstance(text, str) or not text.strip():
            raise EmptyGenerationError(choice.get("finish_reason"),(usage.get("completion_tokens_details") or {}).get("reasoning_tokens"))
        return LLMResponse(
            text=text.strip(),
            provider=self.name,
            model=self.model,
            latency_ms=latency,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            finish_reason=choice.get('finish_reason'),
            reasoning_tokens=(usage.get('completion_tokens_details') or {}).get('reasoning_tokens'),
        )


class GeminiProvider:
    """Google Gemini via the google-genai SDK (decision D-001)."""

    def __init__(self):
        cfg = PROVIDERS["gemini"]
        self.api_key = cfg["api_key"]
        self.model = cfg["model"]
        self.name = "gemini"
        self._client: Optional[genai.Client] = None

    def is_configured(self) -> bool:
        return bool(self.api_key and self.model)

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(
                api_key=self.api_key,
                http_options=genai.types.HttpOptions(
                    timeout=30000, retry_options=genai.types.HttpRetryOptions(attempts=1)),
            )
        return self._client

    async def chat(self, messages: list[dict], max_tokens: int = 300,
                   temperature: float = 0.3) -> LLMResponse:
        """
        Convert OpenAI-format messages to Gemini format and call the API.

        Gemini uses 'user'/'model' roles (not 'assistant'), and the system
        message goes into a system_instruction parameter.
        """
        t0 = time.time()
        client = self._get_client()

        # Extract system message
        system_text = None
        gemini_contents = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                system_text = content
            elif role == "user":
                gemini_contents.append({"role": "user", "parts": [{"text": content}]})
            elif role == "assistant":
                gemini_contents.append({"role": "model", "parts": [{"text": content}]})

        config = genai.types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        if system_text:
            config.system_instruction = system_text

        # Use sync API in a thread to avoid blocking
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=self.model if self.model.startswith("models/") else f"models/{self.model}",
            contents=gemini_contents,
            config=config,
        )

        latency = (time.time() - t0) * 1000
        text = response.text or ""
        if not text.strip():
            raise ValueError("Provider returned empty content")

        input_tokens = None
        output_tokens = None
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            input_tokens = getattr(response.usage_metadata, "prompt_token_count", None)
            output_tokens = getattr(response.usage_metadata, "candidates_token_count", None)

        return LLMResponse(
            text=text.strip(),
            provider=self.name,
            model=self.model,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


# ── Unified client with retry and failover ────────────────────

_PROVIDERS_MAP = {
    "groq": GroqProvider,
    "gemini": GeminiProvider,
}

_MAX_RETRIES = 3
_BACKOFF_BASE = 1.5  # seconds


class LLMClient:
    """
    Unified LLM client. Tries primary provider with retry and Retry-After honouring,
    then falls back to secondary on repeated failure. Capped by concurrency semaphore.
    """

    def __init__(self):
        self.primary = _PROVIDERS_MAP[LLM_PRIMARY]()
        self.fallback = _PROVIDERS_MAP[LLM_FALLBACK]()

    async def chat(self, messages: list[dict], max_tokens: int = 300,
                   temperature: float = 0.3) -> LLMResponse:
        """
        Send a chat completion request. Retries on 429/5xx, then fails over.
        Enforces concurrency limit via semaphore and wait budget.

        Returns LLMResponse with the provider that succeeded.
        Raises ProviderUnavailableError if all providers fail.
        """
        providers = []
        if self.primary.is_configured():
            providers.append(self.primary)
        if self.fallback.is_configured():
            providers.append(self.fallback)

        if not providers:
            raise ProviderUnavailableError(
                "No LLM provider configured. Set API keys and models in .env",
                provider="none",
                status_code=503,
                retry_after=30.0,
            )

        last_details = {}
        last_status = None
        last_provider = providers[0].name
        last_retry_after = None
        failover_count = 0

        for p_idx, provider in enumerate(providers):
            last_provider = provider.name
            failover_count = p_idx
            elapsed_wait = 0.0

            async with get_provider_semaphore(provider.name):
                for attempt in range(_MAX_RETRIES):
                    try:
                        await pace_provider(provider.name)
                        if provider.name == 'groq':
                            await reserve_groq_tokens(messages, max_tokens)
                        resp = await provider.chat(messages, max_tokens, temperature)
                        resp.failovers = failover_count
                        return resp
                    except httpx.HTTPStatusError as e:
                        last_details = provider_error_details(e, [getattr(provider,'api_key','')])
                        print(f"  [llm] {provider.name}: {json.dumps(last_details)}")
                        status = e.response.status_code
                        last_status = status
                        retry_after = extract_retry_after(e)
                        if retry_after is not None:
                            last_retry_after = retry_after

                        if is_daily_quota_error(e):
                            print(f"  [llm] {provider.name} daily quota exhausted, failing over immediately...")
                            break

                        if status == 429 or status >= 500:
                            if retry_after is not None and retry_after > 0:
                                wait = retry_after + random.uniform(0.1, 0.4)
                            else:
                                wait = min(20.0, (_BACKOFF_BASE ** (attempt + 1)) + random.uniform(0.1, 0.4))

                            if elapsed_wait + wait > LLM_TOTAL_WAIT_BUDGET:
                                rem = LLM_TOTAL_WAIT_BUDGET - elapsed_wait
                                if rem > 1.0 and attempt < _MAX_RETRIES - 1:
                                    wait = rem
                                else:
                                    print(f"  [llm] {provider.name} wait budget ({LLM_TOTAL_WAIT_BUDGET}s) exhausted, trying fallback...")
                                    break

                            print(f"  [llm] {provider.name} {status}, retry in {wait:.1f}s (budget remaining: {max(0.0, LLM_TOTAL_WAIT_BUDGET - elapsed_wait - wait):.1f}s)...")
                            if attempt < _MAX_RETRIES - 1:
                                await asyncio.sleep(wait)
                                elapsed_wait += wait
                        else:
                            break  # Non-retryable HTTP error
                    except genai_errors.APIError as e:
                        err_msg = str(e)
                        for secret in [getattr(provider, 'api_key', '')]:
                            if secret:
                                err_msg = err_msg.replace(secret, '[REDACTED]')
                        err_msg = re.sub(r'\bAQ\.[A-Za-z0-9_-]+', '[REDACTED]', err_msg)
                        err_msg = re.sub(r'\bAIza[A-Za-z0-9_-]+', '[REDACTED]', err_msg)
                        print(f"  [llm] {provider.name} error: {err_msg[:200]}")
                        status = getattr(e, "code", 500)
                        last_status = status
                        retry_after = extract_retry_after(e)
                        if retry_after is not None:
                            last_retry_after = retry_after

                        if is_daily_quota_error(e):
                            print(f"  [llm] {provider.name} daily quota exhausted, failing over immediately...")
                            break

                        if status != 429 and (not status or status < 500):
                            break
                        wait = retry_after if (retry_after and retry_after > 0) else min(20.0, (_BACKOFF_BASE ** (attempt + 1)) + random.uniform(0.1, 0.4))
                        if elapsed_wait + wait > LLM_TOTAL_WAIT_BUDGET:
                            break
                        if attempt < _MAX_RETRIES - 1:
                            await asyncio.sleep(wait)
                            elapsed_wait += wait
                    except (httpx.TransportError, TimeoutError) as e:
                        last_status = 504
                        wait = min(15.0, (_BACKOFF_BASE ** (attempt + 1)) + random.uniform(0.1, 0.4))
                        if elapsed_wait + wait > LLM_TOTAL_WAIT_BUDGET:
                            break
                        if attempt < _MAX_RETRIES - 1:
                            await asyncio.sleep(wait)
                            elapsed_wait += wait
                        continue
                    except Exception as e:
                        last_details = provider_error_details(e, [getattr(provider,'api_key','')])
                        if isinstance(e,ProviderUnavailableError):
                            last_status=e.status_code
                            last_retry_after=e.retry_after
                        else:
                            last_status=502
                        break  # Invalid responses/configuration do not improve on retry.

            print(f"  [llm] {provider.name} failed, trying fallback...")

        rec_retry = int(last_retry_after or 15)
        raise ProviderUnavailableError(
            f"All configured LLM providers failed. The AI provider is rate-limited or temporarily unavailable. Retrying in {rec_retry} seconds.",
            provider=last_provider,
            status_code=last_status or 429,
            retry_after=float(rec_retry),
            details=json.dumps(last_details),
        )


# Module-level singleton
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client

