# Student-first implementation and verification — 2026-11-14

## Architecture changes

Added anonymous personal capability workspaces, separate registry/files/cache paths, mandatory workspace metadata filtering and explicit unverified-evidence trust. Institutional approval/publication remains a separate unchanged access path. Reused FastAPI, Chroma/FastEmbed, Groq, Raw/HyDE/Fusion, source hashing/versioning, rollback and citation/cache guards. The model extracts source-bound rules; Decimal code decides confirmed-fact comparisons. See ARCHITECTURE.md and architecture.mmd.

## Per-phase delivery and tests

| Phase | Built | Full suite at phase completion | Verification limits |
|---|---|---:|---|
| 1 | Personal creation/persistence, capability access, validated PDF upload, scoped indexing/RAG/citations/cache, replace/remove/delete, trust levels | 236 passed | API fixtures; live-model verification performed after integration |
| 2 | Cached quote/number/operator/unit-bound numeric rules, proposed facts for confirmation, deterministic statuses/verdicts and constrained explanation | 246 passed | Numeric subset; extraction completeness/authenticity is not established |
| 3 | Same-subject possible conflicts, both source quotes and no winner; affected analysis becomes insufficient evidence | 247 passed | Lexical extracted-subject grouping, not universal semantic conflict proof |
| 4 | Personal-first Home, My Documents, Rule Book, structured Ask & Analyse cards/facts, Conflicts, Changes and secondary Advanced/Admin | 248 passed | DOM checks and actual HTTP loading; visual browser QA unavailable |
| 5 | Retained owned-version extraction and quoted rule-table additions/removals/modifications, with historical evidence excluded from current retrieval | 250 passed | Extracted-table comparison; not official policy applicability or whole-document diff |

Additional integration/safety cases bring the final suite to **257 passed**, six existing dependency deprecation warnings, **9.76 seconds**, no skips. Each phase was followed by a localhost restart/loading check; an automatic approval usage-limit interruption delayed one restart, which was completed after continuation. No phase was abandoned. JavaScript syntax and unique HTML IDs were checked. Existing institution, provider, cache, guardrail, benchmark and frontend regressions remain passing.

## Live personal verification

`scripts/verify_personal_e2e.py --live --output <file>` runs a separate disposable localhost application with real PyMuPDF extraction, FastEmbed document/query embeddings, Chroma, and the configured Groq provider. It requires no administrator authentication. The test instance uses a higher request-rate ceiling for the bounded functional run; production rate limiting remains unchanged and tested. Provider configuration is used through normal app integration; keys/tokens were not inspected, printed or modified.

The final recorded live run returned **answered** for Raw, HyDE and Fusion, with no HyDE fallback; cited chunks resolved to page **1**. The original question and real retrieved evidence reached the answer prompt; six instrumented prompt checks confirmed HyDE passage isolation. An unsupported question returned `no_policy_found`. Cache reuse and replacement invalidation, cross-workspace citation/mutation rejection, multiple PDFs, explicit fact confirmation, an eligible synthetic comparison, missing facts, a possible conflict with no winner, adversarial instruction resistance, invalid PDF rejection and workspace deletion were observed. Personal Compare returned actual Raw/HyDE results. Benchmark execution correctly stayed blocked without manually verified labels. Details: PERSONAL_LIVE_VERIFICATION.json.

The live version-table comparison recorded **addition and removal** categories for the model's extracted keys. An earlier run recorded a modification; deterministic tests separately verify modifications with both quotes. These are reported as actual extracted-table observations, not fabricated proof of official policy changes. Model extraction can choose different field/applicability wording across versions, which can classify a changed requirement as an addition/removal.

All live evidence is clearly labelled **SYNTHETIC TEST FIXTURE**, not real university policy. No institutional approval was emulated or required for these personal tests. No benchmark accuracy or gold label was generated.

## Data preservation

All **37 protected files** (existing original/scoped documents, registries, manifests, caches and legacy Chroma) match their starting SHA-256 hashes. The protected demonstration remains one unpublished institution, ten pending real sources, seven indexed PDFs/517 real chunks, four isolated decoy chunks and three visible extraction failures. No reset, approval, publication or deletion of that dataset occurred. The administrator token and Groq API key were not read for inspection, displayed or changed. Actual provider execution loads its configuration normally.

Personal deletion purges only the selected personal source/version files and derived entries; deleting a personal workspace purges only its own path and vectors. This final file-purge behavior is covered by automated temporary API tests. Institutional removal retains its pre-existing history behavior.

## Files

New application modules: `src/personal.py`, `src/personal_api.py`, `src/intelligence.py`; new frontend `web/personal.js`.

Updated integration: `src/institutions.py`, `src/authority.py`, `src/documents.py`, `src/chunking.py`, `src/ingest.py`, `src/reindex.py`, `src/store.py`, `src/answer.py`, `src/cache.py`, `src/hyde.py`, `src/pipeline.py`, `src/trace.py`, `src/prompts.py`, `src/server.py`, `bench/run_benchmark.py`, `web/index.html`, `web/app.js`, `.env.example`. Existing embedding/provider implementations were reused.

New tests/helpers: `tests/test_personal.py`, `tests/test_intelligence.py`, `tests/personal_frontend.test.cjs`, synthetic PDF fixtures and their generator, and `scripts/verify_personal_e2e.py`. Updated frontend test invocation. Documentation: README, DECISIONS, PROMPTS (full runtime prompt strings), INTERVIEW_NOTES, architecture/Mermaid, personal API/setup/demo/report and verification artifacts.

## Demo and limitations

Run `python -m src.server` and open localhost:8000. Start a personal workspace, upload PDFs, inspect My Documents, ask for cited guidance, extract Rule Book rules, confirm/edit facts and applicability, then analyse. Upload the labelled conflicting fixture to show both passages with no winner; end with an unsupported-question abstention. See PERSONAL_DEMO.md for the complete click sequence and exact fixture paths. For actual policy evidence, use the student's own PDFs; personal uploads remain explicitly unverified.

Known limitations: BrowserOS neo MCP is unavailable, so no visual browser interaction/responsive QA is claimed. Rules cover explicit numeric comparisons only; no formulas or categorical eligibility engine is invented. Exact quote checks do not establish semantic completeness, source authenticity or applicability. Grouping is by extracted subject, and version wording may vary. Unknown facts, applicability, exceptions or conflicts remain insufficient evidence. OCR, enterprise accounts, distributed/crash-proof jobs and deployment are not implemented. Local JSON/Chroma requires one server writer process. Loss of the saved capability ID prevents convenient anonymous workspace recovery.
