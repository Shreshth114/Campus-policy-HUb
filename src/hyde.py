"""HyDE search keys: bounded cache keyed by question, prompt and provider config."""
from contextvars import ContextVar
from dataclasses import asdict, replace
import asyncio
import hashlib
import json
import time
from threading import RLock

from src.llm import get_llm_client, LLMResponse
from src.prompts import HYDE_SYSTEM_PROMPT, HYDE_USER_TEMPLATE
from src.config import HYDE_MAX_TOKENS, DATA_PROCESSED_DIR, PROVIDERS, LLM_PRIMARY, LLM_FALLBACK
from src.persistence import write_json
from src.institutions import current, workspace_path

HYDE_CACHE_PATH = DATA_PROCESSED_DIR / "hyde_cache.json"
cache_enabled = ContextVar("hyde_cache_enabled", default=True)
request_generations = ContextVar("hyde_request_generations", default=None)
_LOCK = RLock()


def safe_search_key(text, question):
    import re
    numbers=set(re.findall(r'\b\d+(?:\.\d+)?\b',text))
    if numbers-set(re.findall(r'\b\d+(?:\.\d+)?\b',question)): return False
    if re.search(r'\b(?:shall|must|required|eligible|permitted|approval|registrar|dean|head of|within|percent|first|second|third|five|seven|ten)\b',text,re.I):return False
    return True


def _cache_key(question):
    models = [(name, PROVIDERS[name].get("model"), PROVIDERS[name].get("base_url"))
              for name in (LLM_PRIMARY, LLM_FALLBACK) if name in PROVIDERS]
    value = [current().personal, current().scope_id, question, HYDE_SYSTEM_PROMPT, HYDE_USER_TEMPLATE, HYDE_MAX_TOKENS, models]
    return hashlib.sha256(json.dumps(value).encode()).hexdigest()


def _read():
    try:
        value = json.loads(workspace_path('hyde').read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _lookup(key):
    with _LOCK:
        entry = _read().get(key)
        if entry and time.time() - entry.get("timestamp", 0) < 3600:
            try:
                return replace(LLMResponse(**entry["response"]), latency_ms=0,
                               input_tokens=0, output_tokens=0, cached=True)
            except (TypeError, KeyError):
                pass


def _store(key, response):
    with _LOCK:
        cache = _read()
        cache[key] = {"timestamp": time.time(), "response": asdict(response)}
        keys = sorted(cache, key=lambda k: cache[k].get("timestamp", 0))[-128:]
        write_json(workspace_path('hyde'), {k: cache[k] for k in keys})


async def generate_hyde(question: str) -> tuple[str, LLMResponse]:
    # Only explicit compare requests share in-flight generations; never tenants.
    pending = request_generations.get()
    if pending is None:
        return await _generate_hyde(question)
    key = _cache_key(question)
    if key not in pending:
        pending[key] = asyncio.create_task(_generate_hyde(question))
    return await asyncio.shield(pending[key])


async def _generate_hyde(question: str) -> tuple[str, LLMResponse]:
    key = _cache_key(question)
    if cache_enabled.get():
        cached = await asyncio.to_thread(_lookup, key)
        if cached and safe_search_key(cached.text, question):
            return cached.text, cached
    messages = [
        {"role": "system", "content": HYDE_SYSTEM_PROMPT},
        {"role": "user", "content": HYDE_USER_TEMPLATE.format(question=question)},
    ]
    response = await get_llm_client().chat(messages=messages, max_tokens=HYDE_MAX_TOKENS, temperature=0.4)
    if not response.text or len(response.text.strip()) < 10 or sum(c.isalpha() for c in response.text) < 10 or len(response.text.split()) < 4:
        raise ValueError("HyDE returned empty or short text")
    if not safe_search_key(response.text, question):
        raise ValueError('HyDE generated ungrounded policy assertions')
    if cache_enabled.get():
        await asyncio.to_thread(_store, key, response)
    return response.text, response
