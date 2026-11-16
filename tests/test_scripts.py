from tests import scoped_metadata, mark_indexed
"""Operational helpers remain safe and usable without real documents or keys."""
import json
from unittest.mock import AsyncMock
import pytest
from scripts.demo_freshness import measure_freshness
from scripts import check_providers,manage_sources
from src import authority,store,cache


def test_freshness_demo_never_touches_production():
    paths=[cache.CACHE_PATH,authority.REGISTRY_PATH]
    before={p:p.read_bytes() if p.exists() else None for p in paths}
    result=measure_freshness()
    assert result['scope']=='synthetic_storage_only' and result['marker_verified']
    assert not result['production_leakage'] and result['freshness_ms']>=0
    assert {p:p.read_bytes() if p.exists() else None for p in paths}==before


@pytest.mark.asyncio
async def test_provider_check_without_keys_never_calls_network(monkeypatch):
    class Unconfigured:
        name='fixture'
        chat=AsyncMock(side_effect=AssertionError('Must not call unconfigured provider'))
        def is_configured(self): return False
    monkeypatch.setattr(check_providers,'GroqProvider',Unconfigured)
    monkeypatch.setattr(check_providers,'GeminiProvider',Unconfigured)
    result=await check_providers.check(live=True)
    assert result['fixture']=={'configured':False,'live_verified':False}
    Unconfigured.chat.assert_not_called()


def test_source_cli_requires_existing_review_and_syncs(monkeypatch,tmp_path):
    path=tmp_path/'fixture.txt'
    path.write_text('SYNTHETIC CLI review-state fixture only. '*20)
    authority.register_source('fixture','Review fixture',source_path=str(path))
    mark_indexed('fixture')
    digest=authority.get_registry()['fixture']['file_hash']
    store.upsert_chunks(['fixture-c'],['Fixture marker'],[[1.,0.]],
                        scoped_metadata([{'doc_id':'fixture','file_hash':digest,'approved':False}]))
    monkeypatch.setattr('sys.argv',['manage_sources.py','--institution-id',__import__('src.institutions',fromlist=['current']).current().institution_id,'approve','fixture'])
    manage_sources.main()
    assert authority.is_approved('fixture') and store.valid_cached_citations(['fixture-c'])
    monkeypatch.setattr('sys.argv',['manage_sources.py','--institution-id',__import__('src.institutions',fromlist=['current']).current().institution_id,'reject','fixture'])
    manage_sources.main()
    assert not authority.is_approved('fixture') and not store.valid_cached_citations(['fixture-c'])
    monkeypatch.setattr('sys.argv',['manage_sources.py','--institution-id',__import__('src.institutions',fromlist=['current']).current().institution_id,'approve','unknown'])
    with pytest.raises(SystemExit) as exc: manage_sources.main()
    assert exc.value.code==1


@pytest.mark.asyncio
async def test_live_check_reports_http_status_and_safe_body(monkeypatch,capsys):
    import httpx
    request=httpx.Request('POST','https://example.invalid',headers={'Authorization':'Bearer fixture-secret'})
    response=httpx.Response(404,json={'error':{'code':'model_not_found','message':'model unavailable fixture-secret'}},request=request)
    error=httpx.HTTPStatusError('private request text',request=request,response=response)
    class Failing:
        name='groq'
        api_key='fixture-secret'
        chat=AsyncMock(side_effect=error)
        def is_configured(self): return True
    class Unconfigured:
        name='gemini'
        def is_configured(self): return False
    monkeypatch.setattr(check_providers,'GroqProvider',Failing)
    monkeypatch.setattr(check_providers,'GeminiProvider',Unconfigured)
    result=await check_providers.check(live=True)
    assert result['groq']['status_code']==404
    assert Failing.chat.call_args.kwargs['max_tokens']==256
    assert 'model_not_found' in result['groq']['response_body']
    output=capsys.readouterr().out
    assert 'fixture-secret' not in output and 'private request text' not in output


def test_example_env_model_ids_are_empty_not_comments():
    from pathlib import Path
    from dotenv import dotenv_values
    example=Path(__file__).resolve().parents[1] / '.env.example'
    values=dotenv_values(example)
    assert values['GROQ_MODEL']==''
    assert values['GEMINI_MODEL']==''
