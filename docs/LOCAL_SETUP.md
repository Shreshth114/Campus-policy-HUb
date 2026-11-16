# Student-first local setup

Open localhost:8000 after `python -m src.server`. Personal upload, Rule Book, Ask & Analyse, conflicts and document changes need no administrator account or published institution. See PERSONAL_PLATFORM.md and PERSONAL_DEMO.md. The following institutional instructions remain available for the secondary verified-knowledge workflow.

# Local operation

From the project directory:

```bash
cd /Users/shreshthagrawal/Documents/DELL_DEMO/ps1-policy-assistant
python -m pip install -r requirements.txt
python -m src.server
```

Open http://127.0.0.1:8000. Use one server process/worker. Stop it before running a CLI indexer or migration. Do not reset any Chroma directory.

Configuration lives in `.env`. Groq alone works with `LLM_PRIMARY=groq`, a valid `GROQ_API_KEY` and an available `GROQ_MODEL`; leave Gemini credentials blank if unused. List available models using `python scripts/list_models.py`; validate with `python scripts/check_providers.py --live`. Provider smoke checks make API calls. No provider key is displayed by the UI or health route.

`ADMIN_API_TOKEN` must be a long random secret. A token has been generated in the local `.env` if it was absent; inspect that file privately and enter its value into Administrator → Unlock administration. It stays in page memory, and a refresh removes it. Never paste it into URLs or static JS. To generate your own locally: `python -c 'import secrets; print(secrets.token_urlsafe(32))'`, then save it privately in `.env` and restart the server.

Administrator workflow:

1. Unlock administration, create an institution by name (ID and slug are generated), and select it in the dedicated administrator selector. No automatic default institution is selected.
2. Upload one to five PDFs. For replacement, provide the existing document ID; old bytes/history remain preserved. All new content starts pending.
3. Use Upload & index PDFs: drag PDFs into the upload area or Browse files, then submit. Byte progress is shown for upload, followed by extraction/chunk/embedding stages. Only the uploaded document versions are indexed automatically; extraction failures remain visible. Reindex workspace or Reindex this document is available for explicit retries. Do not launch a concurrent CLI indexer.
4. Inspect each source: original PDF, full extracted pages, chunks with page/section, content hash and review history. Check authenticity, issuer, applicability, dates, tables and missing pages against the actual source.
5. Record verified source URL, issuing authority, reviewer identity and known applicability. Leave unknown dates blank. Approve the exact current version only after verification, or keep pending/reject. Synthetic/decoy content is not production evidence.
6. Publish the workspace only after eligible evidence exists. Publication does not approve any pending document. Students see only published active institutions.
7. On Overview, choose a published college and click Enter student workspace. Selection is preserved. Ask a question, compare raw/HyDE, inspect citations/trace, or view actual benchmark results. Administration uses a separate selector and can be locked explicitly. If no approved policies are available, a clear message replaces chat.

The migrated demonstration workspace is intentionally **unpublished**, with ten **pending** documents. It will not appear to students until reviewed evidence is approved and the workspace is explicitly published. No policy authenticity or effective date was inferred during migration.

CLI commands (replace UUID with the selected institution's ID from the administrator list):

```bash
python -u -m src.reindex --institution-id UUID
python bench/run_benchmark.py --institution-id UUID --no-cache
python scripts/manage_sources.py --institution-id UUID list
python scripts/demo_freshness.py
python -m pytest tests/ -v
```

Benchmarks require `data/workspaces/UUID/bench/test_queries.jsonl` with the same `institution_id` on every record, actual approved gold chunk IDs and manually verified labels. Pending labels generate a blocked report, without invented zero accuracy. Review benchmark labels manually; ingestion/migration does not verify them. Freshness uses only temporary synthetic fixtures and deterministic test vectors.

The three legacy extraction failures need text-based originals or a separately reviewed future OCR workflow. No OCR is implemented. Browser visual QA remains unverified when BrowserOS neo MCP is unavailable; DOM/API tests are not a substitute for visual verification.
