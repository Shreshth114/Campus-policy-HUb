# Four evaluation-readiness refinements — 16 November 2026

## Status

Implemented explicit question-to-selected-evidence coverage and prepared the human-review/scoring and freeze tooling. Investigated the real archived failure before changing retrieval. **Human adjudication, an independent document cohort and a frozen benchmark execution remain unfinished.** The new coverage review also produced a problematic development response; it has not been declared accurate.

## 1. Trace before retrieval changes

Two different questions had been conflated:

- The later `dev-compound` question asks for a late semester-payment penalty. No supporting provision was identified in the original PDF's extracted text. B17.5 concerns summer-course registration, so it cannot supply that answer. The previous report incorrectly called this a demonstrated retrieval miss. Its archived `expect=answer` metadata was unverified; no archived labels or traces were changed.
- The genuine summer-registration question (`fresh-06`) required B17.2 and B17.5. Both were in rank 1 of the returned pre-merge candidate list in Raw, HyDE-labelled and Fusion runs. The old context selector removed B17.5. The current complete-block selector retains both on offline replay, including the fee-change qualification. No ranking/top-k change is justified by that trace.

The HyDE-labelled archived case was a Raw fallback; Fusion reported no HyDE fallback. These are different execution paths, not three independent equivalent mode observations. Returned top-k records do not reveal the internal ANN candidate pool.

Added exact-source summer-rule and trace-stage regressions. Ranking algorithms, cosine thresholds, providers and production indexes were not changed by this work. See [stage-by-stage trace](evaluation/ps1/refinements/FAILURE_TRACE.md).

## 2. Explicit coverage mechanism

`src/question_coverage.py` creates literal question-span requirements. Q0 always retains the full question; bounded conjunction/semicolon spans expose additional parts. It contains no institution names, policy rules, thresholds or prepared answers. This is a heuristic: it may over-split conditions or miss implicit requests. The reviewer must still assess every request and preserve whole-question scope; human annotations explicitly assess decomposition mistakes.

The existing second model call must now return one ledger row per requirement, with `covered`, `unsupported` or `ambiguous` status, a reason and selected source/provision references. Code rejects missing/duplicate/unknown requirement IDs, unknown or unselected evidence references, and any unsupported/ambiguous coverage. Four positive overall flags cannot override an incomplete ledger. The ledger enforces completeness of the required reporting structure, not semantic truth.

Both generation and review see the literal requirements; there is no extra decomposition model call. No source-text budget or confidence threshold was increased. The review output cap remains 400 tokens and truncated/malformed results fail closed. Trace fields expose `question_requirements` and `evidence_coverage`; opt-in diagnostics already retain the exact review payload/raw response. The cache protocol was advanced to v3 coverage and binds the user template as well as both system prompts. Old proofs safely miss; production cache files were not cleared. Quote, claim, numeric, qualification, ownership, source-version and per-quotation attribution protections remain.

### Live development limitation

One direct Groq-only second-call smoke test used preselected B17.2/B17.5 evidence from the already revealed case. It did not run retrieval, generation, indexing or a held-out benchmark. The model treated the student's request for an exemption as an asserted answer claim and rejected the mandatory-rule selection. It returned only Q0, omitting Q1/Q2. The selection would be withheld. Its semantic correctness requires independent human adjudication; a likely false rejection is not a human-labelled result.

Saved the exact response as a rejected development fixture. No extra call was made to obtain a favorable verdict, and no safeguard was relaxed. Provider latency: 1563.50 ms; wall time: 1564.27 ms; 911 input / 291 output tokens, including 92 reasoning tokens within output. One observation does not establish general latency or cost. [Exact live record](evaluation/ps1/refinements/LIVE_REVIEW_SMOKE.md), [cost observations and limits](evaluation/ps1/refinements/REVIEW_COSTS.md).

## 3. Human-review evaluation

Prepared 12 AI-assisted calibration candidates with real source passages, exact selections and blank human annotations. They exercise faithful selections, missing provisions/conditions, wrong situations, unavailable live records and nonliteral candidate quotes. They use one revealed PDF and cannot establish unseen-document generalisation. Intentionally altered candidate answers are test inputs, never policy evidence or indexed sources. No candidate was marked human-reviewed or verified.

The protocol requires original-PDF checks, human atomic requirements, relevance, completeness, support, qualification preservation, citation correctness, appropriate answer/withhold/clarify outcomes and final adjudication. Prefer independent blinded reviewers. Human flags are declarations; the tool does not authenticate people.

The offline scorer reports false approvals and false rejections with distinct denominators, per-dimension agreement, raw Boolean approvals versus ledger-enforced decisions, pending counts and review token/latency observations. Provider errors are separated from semantic false rejections. Unreviewed or inconsistent labels are unscored. Evaluate production-gate-passing selections separately from malformed stress cases. Reasoning tokens are not added to output tokens again. No currency price is assumed.

- [Review packet](evaluation/ps1/refinements/review-packet/REVIEW.md)
- [Human-review/scoring protocol](evaluation/ps1/refinements/REVIEW_PROTOCOL.md)
- [Pending score status](evaluation/ps1/refinements/review-packet/PENDING_SCORE.md)

## 4. Freeze after development and independent review

Prepared a new-document matrix covering multiple institutions, multi-page rules, tables, scans, amendments and multi-provision questions. Scans currently require extraction abstention because OCR is not implemented; do not count that as successful retrieval. Proposed first cohort: six PDFs from at least three institutions and 30 genuinely reviewed questions. These are targets, not collected sources, completed labels or benchmark scores.

The freeze helper refuses missing human source adjudication, insufficient institution coverage, known exposed document hashes (including archived development metadata), declared reused questions, hash mismatches, duplicate contents, incorrect cache/fallback policy and overwrites. It hashes code/tools, inputs, model/settings and package versions. Verification detects code inventory/content, input, model and runtime drift. It refuses output in production storage. Exact hashes cannot prove semantic novelty; human exposure attestation remains required.

The current calibration specification intentionally fails readiness. No new held-out manifest or benchmark was created. Final execution must wire preflight verification into its runner and use the future reviewed dataset. The existing diagnostic runner remains a development tool; it does not alone enforce this final gate.

The comparison protocol specifies identical settings and questions, balanced mode order, cold caches, stage-by-stage evidence coverage, raw selections versus final answers, real mode results versus Raw fallbacks, separate extraction/provider failures, human correctness/citation/abstention grading, and generation/review latency and token costs. No HyDE superiority claim is supported yet.

- [Unseen-document matrix](evaluation/ps1/refinements/UNSEEN_DOCUMENT_MATRIX.md)
- [Freeze/comparison protocol](evaluation/ps1/refinements/FROZEN_COMPARISON_PROTOCOL.md)
- [Current blockers](evaluation/ps1/refinements/FREEZE_STATUS.md)

## Verification and integrity

`python -m pytest tests/ -q`: **476 passed**, six existing dependency warnings, 11.96s. All four frontend suites passed, including 19 dashboard checks:

```sh
node tests/personal_frontend.test.cjs
node tests/sidebar_frontend.test.cjs
node tests/frontend.test.cjs
node tests/whatif_frontend.test.cjs
```

The new coverage tests were first run before implementation and failed collection because the module did not exist. Subsequent tests cover missing evidence, incomplete ledgers despite positive flags, actual summer provisions, selected-source mappings, trace-stage attribution, legacy proofs, service-error denominators, pending human labels, freeze/drift/overwrite guards and the exact live missing-row response. Malformed cached contracts and null human dimension fields also fail safely. Existing positive doubles were updated for the stricter review contract; original grounding assertions were retained. [Full final output](evaluation/ps1/refinements/TEST_RESULTS.md).

**The live production snapshot is not identical.** It started at 237 files and ended at 243: 235 original files match, `data/personal_workspaces.json` and `.chroma-institutions/chroma.sqlite3` changed, and six synthetic-demo workspace files were added. The running server logged a successful demo-creation request, consistent with concurrent live use; caller identity is unconfirmed. No rollback, deletion or shared-database inspection was performed. Do not claim institutional vector records are byte-identical. The original PDF and frozen ten-case labels still match their prior manifests. See [integrity evidence and limits](evaluation/ps1/refinements/INTEGRITY.md).

The task's tests use isolated temporary storage; JavaScript suites mock network calls. The one direct review smoke called Groq only and never used the live app/index. This round performed no ingestion or embedding generation and did not change provider configuration, registry approvals or institutional publication state. No server restart was requested or performed.

## Exact changed files

Application: added `src/question_coverage.py`; updated `src/answer.py`, `src/grounding.py`, `src/prompts.py`, `src/pipeline.py`, `src/trace.py`.

Tests: added `tests/test_question_coverage.py`, `tests/test_review_evaluation.py`, `tests/test_evaluation_freeze.py`, `tests/fixtures/coverage/nit_goa_summer_actual.txt`, `tests/fixtures/coverage/summer_review_missing_rows.json`; updated `tests/grounding_helpers.py`, `tests/test_structured_grounding.py`, `tests/test_answer_grounding_regressions.py`.

Evaluation: added `evaluation/ps1/refinements/trace_failure.py`, `review_evaluation.py`, `freeze_manifest.py`, `freeze_spec.NOT_READY.json`, the Markdown reports/protocols linked above, and `review-packet/{cases.json,annotations.template.json,predictions.empty.json,REVIEW.md,PENDING_SCORE.md}`. These are development/review artifacts, not approved labels.

Documentation: this report; a corrective note in `docs/GENERAL_ANSWER_GROUNDING.md`; appended `PROMPTS.md`, `DECISIONS.md`, `INTERVIEW_NOTES.md`, `PROJECT_LOG.md`. Pre-change copies of seven application/test files are under `backups/coverage-refinements/`.

## Next execution order

1. Obtain independent human decisions for the calibration packet, especially the mandatory-rule versus requested-exemption distinction. Measure requirement decomposition and reviewer errors before further semantic prompt tuning.
2. Resolve any adjudicated failures using general synthetic regressions; preserve every revealed case as development data.
3. Collect independent PDFs and human labels, validate extraction/mappings and freeze the complete specification in a quiet/isolated environment.
4. Wire preflight into final execution, run the balanced Raw/HyDE/Fusion comparison, then grade and report raw selections, final answers, abstentions, fallbacks and costs separately.

The website is not yet demonstrated reliable across arbitrary PDFs. Strict rejection and passing regression tests are useful protections, not a completed accuracy evaluation.
