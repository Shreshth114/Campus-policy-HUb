# General answer grounding — 16 November 2026

> Correction, subsequent refinement audit: the later late-SEMESTER-fee question was not supported by the supplied PDF. Its abstention must not be counted as a demonstrated retrieval failure. The genuine earlier SUMMER-registration case retrieved B17.2 and B17.5 at rank 1 and lost B17.5 during old context selection. See evaluation/ps1/refinements/FAILURE_TRACE.md. Historical run records and labels remain unchanged.

## Outcome

Implemented a general, conservative evidence-selection and answer-validation flow. There are no NIT Goa names, attendance thresholds, prepared student answers or document-specific clause IDs in the application logic. The supplied B.Tech PDF is development evidence, not a template of answers for other institutions.

**This is a reliability improvement, not a completed accuracy evaluation.** The real development checks answered medical condonation and reinstatement with complete cited provisions after the fixes. The compound late-fee question still fails retrieval and safely abstains. We have not established HyDE superiority or universal PDF correctness.

## Answer path

1. Existing Raw, HyDE or Fusion retrieval and the existing cosine confidence gate run unchanged. HyDE remains a search key and is excluded from the answer and review inputs.
2. Already-retrieved, adjacent cross-page continuations can be connected only when document/version/workspace/institution/section match, chunk indexes and pages are consecutive, and an unfinished clause is followed by lowercase continuation text. Both source IDs and pages are retained. This is a limited read-time operation, not re-indexing.
3. Extract complete numbered provisions or unnumbered paragraphs. Keep a retrieved block's complete units together when they fit, including units without exact question keywords. If a block cannot fit, select whole units around its strongest lexical anchor. Do not cut units mid-rule or deduplicate their legitimate repeated sentences. No whole provision can exceed the total evidence budget.
4. The existing total source-text budget remains `ANSWER_CHUNKS_LIMIT * CHUNK_MAX_TOKENS * 4` (currently 4,200 characters); there are still at most three source excerpts. There is additional provision-label markup. The existing capped generation budget is unchanged.
5. Give each complete provision an explicit ID within its source excerpt, e.g. `C1/P4`. The model returns JSON selecting source and provision IDs. The application uses exactly those selected source units; it does not infer a source for a missing citation or expand a partial quote by guessing intent. Each rendered quotation receives its own adjacent `[Cn]` citation.
6. Validate exact unit selection, citation labels, source ownership/version, per-quotation matches, factual/numeric support and material qualifications. The literal-quote contract is also supported, but must equal a complete provided unit. Existing free-text response bodies are not accepted as the new generation contract. Nested quotation syntax that the existing verifier cannot represent safely is withheld.
7. A second call through the same configured client checks actual-question relevance, coverage of every requested part, source support and preservation of qualifications. Its strict JSON verdict must approve all four checks with no reasons. Malformed, negative or truncated reviews do not pass. This model review is fallible and is never permitted to override deterministic checks.
8. Render only validated exact source provisions. The production generation path no longer calls the broad `complete_source_conditions()` supplementation helper. That helper remains for compatibility with its existing regression tests; it is not an answer-generation repair mechanism.
9. Cache successful answers with a versioned proof binding the question, rendered answer, exact ordered excerpts, source versions/pages/IDs, institution/workspace and generation/review system prompts. Contract/template changes must bump the protocol version. Cache hits repeat deterministic validation and require the matching reviewed proof plus the existing live-source fingerprint. Legacy entries safely miss without clearing production cache files. The proof is a local consistency record, not a cryptographic signature against a hostile local administrator.

A medical question about a live personal approval is no longer automatically misclassified as an ambiguous class/exam absence merely because it mentions medical leave. General policy still cannot establish a live approval.

## Live development observations

All calls used the existing Groq model, `openai/gpt-oss-120b`. Gemini fallback was disabled only inside each isolated diagnostic process. Provider configuration was not edited. These are revealed development questions, not an untouched holdout or an accuracy benchmark.

| Stage | Attendance | Late fee + deadline | Return after temporary discontinuation |
| --- | --- | --- | --- |
| Initial full-quote contract | Rejected partial B11.4 quotation; no missing conditions appended | Model abstained | Provider unavailable; local Groq token-budget rejection reported as 429 |
| Explicit provision IDs | Answered: full B11.4, verified quote and positive coverage review | Abstained: wrong retrieved provisions | Abstained: trimming dropped B8.2 despite retrieval finding it |
| Complete-block context fix | Not repeated after this final generic selection change; regression tests retain full B11.4 | Not repeated; retrieval algorithm unchanged | Answered: explicitly selected B8.1 and B8.2, two verified quotations and positive review |

The Attendance success selected `{"provision":"P4","source":"C1"}`. The rendered B11.4 contains **80% excluding medical leave**, **75% overall including illness**, AAC discretion, recommendations, the last-instructional-day deadline, two-semester limit and the IMO-endorsed medical certificate/seven-day deadline. Its normalized text matches the original PDF provision on page 10. Nothing was appended from an unselected rule.

The return-to-study success selected `C2/P1` and `C2/P2`. B8.2 states that the faculty adviser, consulting the Head of Department, decides creditable courses to register and communicates the decision to AAC. The model did not substitute first-semester enrollment rules.

The late-fee retrieval returned summer-term fees and other course-registration material; it did not supply the required late-semester-payment provisions. This is a remaining recall failure, not evidence that the policy is absent from the PDF. An exact generic answer cannot be produced safely from those excerpts.

Seven development pipeline attempts were recorded across three stages: eight successful model calls and one failed request. Earlier failures remain in their reports; they were not overwritten. Only Raw was exercised live in this round. All three retrieval modes pass isolated integration tests with the same answer flow. No new live Raw/HyDE/Fusion superiority comparison was performed.

Full raw selections, review outputs, final answers, quotation results, stage timings and tokens:

- [Initial contract diagnostic](evaluation/ps1/runs/structured-grounding-development-2026-11-16/REPORT.md)
- [Explicit-selection diagnostic](evaluation/ps1/runs/structured-grounding-selection-2026-11-16/REPORT.md)
- [Final context-fix diagnostic](evaluation/ps1/runs/structured-grounding-context-2026-11-16/REPORT.md)

## Tests

Baseline: `python -m pytest tests/ -q` — **422 passed**, six dependency warnings, 13.56s.

Tests were added first: the initial new suite reproduced five failures (three cases already passed). Two further synthetic regressions reproduced zero-keyword context loss and exclusion of a complete rule ending in a parenthetical amendment note before their fixes.

Final commands:

```sh
python -m pytest tests/ -q
python -m pytest tests/test_structured_grounding.py tests/test_answer_grounding_regressions.py tests/test_quotation_attribution.py tests/test_frozen_review_metrics.py -q
node tests/personal_frontend.test.cjs
node tests/sidebar_frontend.test.cjs
node tests/frontend.test.cjs
node tests/whatif_frontend.test.cjs
```

Full final Python result: **451 passed**, six existing dependency warnings, 12.74s. All four frontend suites passed, including 19 dashboard checks. No UI code changed or new visual QA was required. Targeted grounding result: **67 passed**, six dependency warnings, 3.60s.

Coverage includes full B11.4 and its AAC discretion, absent qualifications, invented/swapped thresholds, fabricated penalties, uncited claims, cache revalidation and binding, source/workspace isolation, exact source/provision IDs, unsupported and malformed reviews, multiple requested rules, same-line individually cited quotations, cut-off quotes, legitimate repetition, cross-page continuation metadata and HyDE exclusion. Synthetic library, fee and withdrawal rules exercise different numbers and wording; they are never ingested as university policies.

Existing positive model doubles now return the structured contract and an explicit review verdict. Original paraphrase support/rejection assertions remain separately tested. Legacy cache entries now miss because they lack the new review proof; HTTP integration tests verify that genuinely reviewed answers still hit cache, and that replacement/revocation invalidate them.

## Diagnostics and evaluation compatibility

Optional local diagnostics remain off by default. With `ANSWER_DIAGNOSTICS_ENABLED=true` and a safe local `ANSWER_DIAGNOSTICS_DIR`, records include exact generation messages, ordered source excerpts/mappings, raw rejected selection, individual failures and coverage-review messages/raw verdict. Existing secret redaction and private file permissions remain. Avoid shared diagnostic directories: source passages and questions are sensitive even after credential redaction. Provider exceptions during review may prevent the normal local answer record; the isolated diagnostic runner retains those captured calls/errors separately.

The diagnostic runner now captures the generation and coverage review separately, freezes the review prompt and records the literal proposed answer before review. Metrics distinguish raw JSON output from the selected source text and the final application decision. Historical free-text records still work. Mechanical exact-span coverage is not semantic accuracy. Comparing historical free-form generation with this controlled extractive workflow requires acknowledging the changed generation task.

## Files changed or added

Application:

- `src/answer.py` — whole-provision/block context budget, structured selection, fail-closed coverage review, no automatic supplementation.
- `src/grounding.py` — new source-unit contract, exact rendering, review schema and scope-bound cache proof.
- `src/evidence.py` — independently attributed same-line quote units; provision-scoped qualification checks for quotation-only answers; conservative retrieved page-continuation joining.
- `src/prompts.py` — selection/review instructions and labelled complete source units/page mappings; other task prompts unchanged.
- `src/query_intent.py` — distinguish live-status medical questions from absence ambiguity.
- `src/pipeline.py` — shared review-aware cache path, correct sent-excerpt quotation order and separate review token/latency reporting.
- `src/cache.py` — persist/return optional grounding proof; preserve existing source fingerprints and scope checks.
- `src/answer_diagnostics.py` — include optional coverage-review details with existing redaction.

Tests:

- Added `tests/test_structured_grounding.py`, `tests/grounding_helpers.py`.
- Updated `tests/test_guardrails.py`, `tests/test_answer_grounding_regressions.py`, `tests/test_end_to_end.py`, `tests/test_personal.py`, `tests/test_security_edges.py`, `tests/test_frozen_review_metrics.py`.

Evaluation/docs:

- `evaluation/ps1/run_diagnostic.py`, `evaluation/ps1/review_metrics.py`.
- Added `evaluation/ps1/structured-grounding-development/questions.json`, `README.md`, `INTEGRITY.md` and the three run directories linked above, with machine-readable records and Markdown reports.
- This report; appended `PROMPTS.md`, `DECISIONS.md`, `INTERVIEW_NOTES.md`, `PROJECT_LOG.md`.
- Preserved pre-change copies of `answer.py`, `pipeline.py`, `prompts.py`, `trace.py`, `cache.py`, `query_intent.py` under `backups/structured-grounding/`. The active `src/trace.py` was not changed.

No frontend, provider configuration, retrieval/ranking algorithm, threshold, institutional document or production index was changed.

## Integrity and remaining work

All **237 currently protected production files** under `data/`, `.chroma/` and `.chroma-institutions/` remain byte-identical, including their path/count sets. The original PDF and frozen ten-question labels match their existing SHA-256 manifest. No source was approved, rejected or relabelled. The historical 244-file count was already different before this round. See [integrity record](evaluation/ps1/structured-grounding-development/INTEGRITY.md).

The diagnostics generated embeddings only in disposable indexes, which were removed on exit. Stored personal chunks and production embeddings remain unchanged. The running application server was not restarted or queried against production data for this work.

Unfinished:

1. Fix and measure multi-part retrieval recall, beginning with the logged late-fee/deadline failure. Preserve retrieval-mode attribution and Raw fallback accounting.
2. Obtain human-reviewed, newly held-out questions across multiple real documents/institutions. These revealed cases cannot be reused as untouched evaluation. Human labels remain unverified.
3. Run a frozen Raw/HyDE/Fusion comparison, scoring source selection, final correctness, safe/false abstention, citations, latency and both generation/review tokens independently.
4. Measure review false approvals/rejections. One extra review call adds latency/cost; a favorable model verdict is not a proof of entailment.
5. Broaden layout coverage only with evidence and regressions. The present conservative boundary rules do not solve arbitrary tables, scanned PDFs, nested quotations, oversized provisions or all page continuations. Those can still abstain. Cross-references to unretrieved rules can remain incomplete. No universal PDF-correctness guarantee is justified.

## Exact development commands used

Run from the project root. Output directories must be new; do not overwrite earlier records.

```sh
python evaluation/ps1/run_diagnostic.py --questions-file evaluation/ps1/structured-grounding-development/questions.json --modes raw --pdf 'LOCAL_POLICY_PDFS/BTech_(Rules_&_Regulations)2013_21nov2023.pdf' --output evaluation/ps1/runs/structured-grounding-development-2026-11-16 --pause 5
python evaluation/ps1/run_diagnostic.py --questions-file evaluation/ps1/structured-grounding-development/questions.json --modes raw --pdf 'LOCAL_POLICY_PDFS/BTech_(Rules_&_Regulations)2013_21nov2023.pdf' --output evaluation/ps1/runs/structured-grounding-selection-2026-11-16 --pause 30
python evaluation/ps1/run_diagnostic.py --questions-file evaluation/ps1/structured-grounding-development/questions.json --ids dev-reinstatement --modes raw --pdf 'LOCAL_POLICY_PDFS/BTech_(Rules_&_Regulations)2013_21nov2023.pdf' --output evaluation/ps1/runs/structured-grounding-context-2026-11-16 --pause 5
```

Each stage has its own frozen code/prompt hashes. The Attendance live success precedes the final block-retention fix; the final tests check Attendance against that updated selector. The final live rerun intentionally targeted only the newly fixed reinstatement case rather than consuming more calls on already observed cases.
