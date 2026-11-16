#!/usr/bin/env python3
"""
list_models.py — List models available from configured LLM providers.

Usage:
    python scripts/list_models.py              # list all providers
    python scripts/list_models.py groq         # list only Groq models
    python scripts/list_models.py gemini       # list only Gemini models
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import httpx
from google import genai
from src.config import PROVIDERS


def list_groq_models() -> list[str]:
    """List models available on Groq via OpenAI-compatible /models endpoint."""
    api_key = PROVIDERS["groq"]["api_key"]
    base_url = PROVIDERS["groq"]["base_url"]
    if not api_key:
        print("  ⚠  GROQ_API_KEY not set in .env")
        return []
    try:
        resp = httpx.get(
            f"{base_url}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        resp.raise_for_status()
        models = sorted(m["id"] for m in resp.json().get("data", []))
        return models
    except Exception as e:
        err_msg = str(e)
        if api_key:
            err_msg = err_msg.replace(api_key, "[REDACTED]")
        print(f"  ✗  Groq error: {err_msg}")
        return []


def list_gemini_models() -> list[str]:
    """List models available via the google-genai SDK."""
    api_key = PROVIDERS["gemini"]["api_key"]
    if not api_key:
        print("  ⚠  GEMINI_API_KEY not set in .env")
        return []
    try:
        client = genai.Client(api_key=api_key)
        models = []
        for m in client.models.list():
            if not m.name:
                continue
            # Filter to models that support generateContent
            actions = getattr(m, "supported_actions", None)
            if actions is None:
                actions = getattr(m, "supported_generation_methods", None)
            if actions is None or "generateContent" in actions:
                models.append(m.name.replace("models/", ""))
        return sorted(models)
    except Exception as e:
        err_msg = str(e)
        if api_key:
            err_msg = err_msg.replace(api_key, "[REDACTED]")
        print(f"  ✗  Gemini error: {err_msg}")
        return []


def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if target in ("all", "groq"):
        print("\n── Groq Models ──")
        models = list_groq_models()
        if models:
            for m in models:
                print(f"  {m}")
            print(f"\n  Total: {len(models)} models")
        else:
            print("  No models found (check API key)")

    if target in ("all", "gemini"):
        print("\n── Gemini Models ──")
        models = list_gemini_models()
        if models:
            for m in models:
                print(f"  {m}")
            print(f"\n  Total: {len(models)} models")
        else:
            print("  No models found (check API key)")

    print()


if __name__ == "__main__":
    main()

