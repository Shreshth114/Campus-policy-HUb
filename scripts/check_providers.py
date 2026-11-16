#!/usr/bin/env python3
"""Check configuration; use --live for one tiny, explicit request per configured adapter."""
import argparse
import asyncio
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.llm import GroqProvider, GeminiProvider, provider_error_details


async def check(live=False):
    results={}
    for adapter in (GroqProvider,GeminiProvider):
        provider=adapter()
        row={'configured':provider.is_configured(),'live_verified':False}
        if row['configured'] and getattr(provider, 'model', None):
            row['model'] = provider.model
        if live and row['configured']:
            try:
                # Reasoning models may exhaust 32 tokens before emitting content.
                result=await provider.chat([{'role':'user','content':'Reply with OK.'}],max_tokens=256,temperature=0)
                row.update(live_verified=bool(result.text.strip()),latency_ms=result.latency_ms)
            except Exception as exc:
                row.update(provider_error_details(exc, [getattr(provider, 'api_key', '')]))
        results[provider.name]=row
    print(json.dumps(results,indent=2))
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--live',action='store_true')
    asyncio.run(check(parser.parse_args().live))
