# Implementation report

The product now uses generated institution UUIDs, immutable workspace context, versioned source storage, mandatory tenant predicates, separate caches and live citation provenance. The existing FastAPI/vanilla-JS/FastEmbed/Chroma/Groq stack, HyDE structural isolation, raw cosine/RRF distinction and incremental rollback are retained.

Delivered: institution creation/publication; authenticated multi-PDF uploads; pending source versions/history; extraction/chunk/original inspection; metadata review, approval/rejection/keep-pending; scoped indexing/activity/removal; student institution selector/chat/explainability/full excerpts; compare; honest scoped benchmark dashboard/results. A local administrator token was added privately to `.env` if absent. No provider credentials were changed or exposed.

Migration: ten copied originals and pending records, seven indexed real documents/517 real chunks, three visible extraction failures and four excluded decoy vectors; all 22 inventoried legacy files remain unchanged. The demonstration institution remains unpublished. Details and rollback considerations are in MIGRATION_REPORT.md.

Tests: **223 passed**, six dependency warnings; 11 Node DOM checks; successful local server/read-only HTTP checks; Groq live smoke succeeded. Browser visual QA remains blocked by unavailable BrowserOS neo MCP. No real-world accuracy is claimed, no benchmark labels were verified and no OCR was implemented.

## Application files

New: `src/institutions.py`, `src/documents.py`, `src/migrate_legacy.py`.

Updated: `src/authority.py`, `src/chunking.py`, `src/ingest.py`, `src/store.py`, `src/reindex.py`, `src/cache.py`, `src/hyde.py`, `src/retrieve.py`, `src/answer.py`, `src/pipeline.py`, `src/trace.py`, `src/server.py`, `bench/run_benchmark.py`, `scripts/manage_sources.py`, `scripts/demo_freshness.py`, `web/index.html`, `web/app.js`, `requirements.txt`, `.env.example`; private local `.env` administrator-token entry only. Existing LLM adapter, embedding implementation and prompts remain unchanged.

## Tests and documentation

New `tests/test_institution_isolation.py`; updated isolated fixtures and relevant benchmark/cache/guardrail/ingestion/server/frontend/CLI regressions. New architecture/API/setup/migration/implementation documentation and implementation-phase record; updated README, DECISIONS, PROMPTS, INTERVIEW_NOTES, SOURCE_REVIEW, OPERATIONS and VERIFICATION.

## Run

```bash
cd /Users/shreshthagrawal/Documents/DELL_DEMO/ps1-policy-assistant
python -m pip install -r requirements.txt
python -m src.server
# Stop the server before CLI indexing:
python -u -m src.reindex --institution-id UUID
python bench/run_benchmark.py --institution-id UUID --no-cache
python -m pytest tests/ -v
```

Open http://127.0.0.1:8000. Use the administrator token from private `.env`, select a workspace, inspect/review documents, approve exact versions and explicitly publish before student use. Replace UUID with the selected institution ID. See LOCAL_SETUP.md for full instructions.
