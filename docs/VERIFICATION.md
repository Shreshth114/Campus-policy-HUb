# Verification — 2026-11-14

`python -m pytest tests/ -v`: **223 passed**, six dependency deprecation warnings, 7.76 seconds. This retains the 197 previous regression cases with explicit institution-aware fixtures, plus 26 new isolation/migration cases. No tests were skipped. Fixtures use temporary data and deterministic embedding/provider stubs; no synthetic fixture was installed as a real university source.

The suite covers raw/HyDE/fusion/fallback tenant filtering, conflicting/absent scope, foreign high-similarity exclusion, answer/HyDE cache isolation, live citation ownership/fingerprints, pending/rejected/synthetic/decoy isolation, independent approval/replacement/reindex/removal, foreign administrator IDs, upload/original/page/chunk inspection, publication eligibility, scoped unverified benchmark labels, staged migration interruption/rerun, indexing rollback and version replacement during embedding. Existing provider retry/timeout/sanitization, confidence, prompt isolation/injection, RRF/cosine, incremental-indexing and API edge regressions remain passing.

The Node DOM harness passes **11 dashboard checks**, including safe rendering, measured/null metric distinction, all dashboard tabs, request failure recovery, duplicate submission handling, citation navigation, clearing institution state and rejecting a late answer from the previous institution. `node --check web/app.js` passes. These are behavior checks, not visual browser QA.

A real uvicorn process started on `127.0.0.1:8000`. Read-only HTTP smoke checks: `/`, `/app.js`, `/health`, `/institutions` and authenticated `/admin/institutions` returned 200. The scoped admin source list returned ten records and 521 chunks. Public institution list returned zero because the only workspace is intentionally unpublished. Unauthenticated admin returned 401; missing or unpublished institution questions returned 422. No source was approved or published for this check.

Live provider smoke: Groq `openai/gpt-oss-120b` verified successfully (approximately 714 ms for that request). Gemini is unconfigured and optional. Credentials/authorization headers were not printed. This is provider connectivity validation, not policy-answer quality or retrieval accuracy.

Migration validation: 22 protected legacy files still match the pre-migration SHA-256 inventory; 10 sources remain pending, seven indexed real documents/517 real chunks and three failed extractions remain visible; four decoy chunks stay evaluation-only; no approved evidence is available; workspace remains unpublished. Exact texts and original vector export remain preserved. See MIGRATION_REPORT.md for measured float32 storage rounding and backups.

**Outstanding verification:** BrowserOS neo's MCP tools are unavailable in this session. The installed skill does not itself provide browser connectivity. Visual/responsive browser QA and a live approved-policy answer demonstration have not been verified. The latter requires human-reviewed source approvals; real-world retrieval benchmarks additionally require manually verified institution-owned gold labels. No benchmark accuracy is claimed. OCR, enterprise operator roles and distributed/crash-proof jobs are future work.


## UI/onboarding correction — 2026-11-14

Latest full suite: **227 passed**, six dependency warnings (8.40 s). The DOM harness now checks 19 behaviors. A disposable real HTTP application exercised synthetic PDF upload, real extraction/FastEmbed/Chroma, explicit fixture review/publication, Groq answers through Raw/HyDE/Fusion, page-1 citation resolution, prompt separation, unsupported-question abstention, cache revocation and foreign access rejection. No real university source was approved. All 37 protected production files remain unchanged. See UI_FUNCTIONALITY_FIX.md and UI_LIVE_E2E_RESULTS.json. BrowserOS neo is unavailable, so visual browser QA remains outstanding.


## Student-first platform final verification — 2026-11-14

Latest full suite: **257 passed**, six dependency warnings, 9.76 s, no skips. All five phases were implemented and checked with full suites and localhost loading. A disposable personal-workspace live run exercised real PDF extraction, FastEmbed, Chroma, Groq Raw/HyDE/Fusion answers, page citations, prompt isolation, fact confirmation, numeric analysis, possible conflict, version-table differences, cache invalidation, injection resistance and workspace isolation. No administrator authentication or institutional approval was used. Benchmark metrics stayed blocked without labels. All 37 protected files remain unchanged. Visual browser QA remains unavailable. See PERSONAL_IMPLEMENTATION_REPORT.md and PERSONAL_LIVE_VERIFICATION.json.
