# HyDE ablation report — incomplete

The authorized live run reached a Groq daily-token limit. No held-out comparison was completed and no candidate qualifies for adoption. The current personal Fusion default is retained pending evidence, rather than on the strength of a completed comparison.

## Setup

Seed 20261114. The metadata pool in setup.json contains six non-protected PDFs. Four synthetic, near-duplicate or adversarial unit fixtures were excluded. Only two independent policy PDFs remain. Examination_Rules.pdf (14 pages) is TUNE; NIT_Goa_Regulations.pdf (22 pages) is HOLD-OUT. The initial metadata-only split was corrected before any content-based work. Hold-out content remains uninspected. No protected MSRIT PDF was copied or used.

Four paced generation batches proposed 28 TUNE questions. Exact normalized page-quote checks rejected nine. Six assistant-written questions with verified source quotes were added. Indexed-chunk validation rejected another two, leaving 23 eligible cases. Labels are machine-generated and machine-verified for existence, not human reviewed. Existing benchmark (25 rows) and audit (36 rows) label files contain zero labels_verified=true rows. Existing audit data was used only as a reference, not training data.

## Baseline and prepared variants

baseline.json preserves both current HyDE templates verbatim. runtime-settings.json records actual HYDE_MAX_TOKENS=200, threshold=0.35, TOP_K=5, bge-small-en-v1.5 and DEFAULT_RETRIEVAL_MODE=fusion. The observed provider/model is Groq openai/gpt-oss-120b. The current institutional request schema still defaults to hyde. Existing Fusion uses unweighted RRF k=60 and best-path cosine.

The research runner prepares V1, V2, normalized query/passage averages at 1:1, 1:2 and 2:1, and RRF k=10/30/60 with raw weights 1/1.5/2. V6 cutoff sweeps are offline replay scaffolding only. V4, V5 and V8 are NOT TESTED. These configurations have not been integrated as selectable production/API modes.

The current confidence gate uses maximum retrieved cosine, including best raw/HyDE path scores in Fusion. Experimental averaged-vector scores cannot safely be assumed equivalent. Original-query cosines are saved separately for completed experimental observations. No gate or threshold has been changed.

## Measured TUNE Raw results

Only cases with a verified page quote and at least one indexed gold chunk are included. Scores are provisional machine-labelled TUNE observations.

| Type | n | Recall@1 | Recall@3 | Recall@5 | MRR |
|---|---:|---:|---:|---:|---:|
| Overall | 23 | 0.783 | 0.913 | 0.913 | 0.841 |
| casual/hypothetical paraphrase | 7 | 0.857 | 1.000 | 1.000 | 0.905 |
| direct factual | 6 | 0.833 | 1.000 | 1.000 | 0.917 |
| multi-condition | 3 | 1.000 | 1.000 | 1.000 | 1.000 |
| numeric/threshold | 7 | 0.571 | 0.714 | 0.714 | 0.643 |

Raw retrieved gold at rank 1 for 18/23 and within ranks 3 and 5 for 21/23. Zero LLM calls are required by Raw retrieval itself. Timings are recorded per raw-query file. No Raw-versus-HyDE or default comparison can be inferred from this table.

## HyDE inspection and provider failures

Only one paired V1/V2 query completed. Manual inspection finds V1 on-topic but inventing a 25–35% range, while V2 is on-topic without specific figures. Word counts are {'hyde_v1': 68, 'hyde_v2_prompt': 36}; the V2 output fails its requested 60–110-word range. This is one observation, not the required 20-passage inspection or evidence of improvement. No completed per-type ablation or meaningful wins/losses analysis exists.

The saved outer failure log contains {413: 4, 429: 6}. Unified-client internal retries are additional and are not counted as separate log rows. A subsequent direct diagnostic of the affected V1 request succeeded after cooldown and was cached. The next V2 run received 429 and then an empty-content response after retry. Empty content is a provider failure, not a retrieval miss or an abstention. The one-token diagnostic also returned empty content and is excluded from evaluation statistics.

The sanitized 429 reports a daily token limit of 200000, usage 199646 and request size 369. Its Retry-After was 7 seconds for that individual call. Recovering enough capacity for one request does not establish capacity for the full experiment. The earlier 413 question-generation failure was addressed with smaller batches. Research retries now log sanitized response bodies and Retry-After and handle empty-content and transport failures separately.

## HOLD-OUT, acceptance and safety

No candidates are frozen and no HOLD-OUT question set or retrieval table exists. Acceptance conditions (a) MRR/Recall@3 improvement, (b) per-type non-regression, (c) safety, and (d) acceptable latency/tokens are NOT TESTED. The full regression suite covers only the existing-system portion of condition (e). No candidate is accepted or rejected on retrieval quality. All remain unvalidated research configurations.

e2e.py is prepared to exercise the existing Fusion pipeline in disposable storage with near-miss, out-of-scope and injection questions and instrument answer-prompt isolation. It has not run. No held-out answer, true-abstention, confident-wrong-answer or semantic-faithfulness claim is made. Candidate safety comparison, source-injection fixtures, ten successful instrumented prompts and further scaffolding work remain required. No benchmark labels were marked verified.

## Guardrails and tests

- PASS — all 219 protected-file SHA-256 hashes match before/after, preserving institution sources and extraction-failure state.
- PASS — no approval, publication, deletion or reset of protected storage; no application module or UI edit.
- PASS — disposable, separately ported HTTP indexing and Raw retrieval exercised; temporary instances exited.
- PASS — eight local tests cover vector normalization, weighting, invalid input, cache-key separation and uncached empty provider failures.
- NOT TESTED — experimental citation/quote safety, query-cosine gate equivalence, cross-workspace negative checks and hypothetical-text isolation over live end-to-end candidate calls.
- Existing isolation, quote validation, injection resistance, deterministic eligibility and trust-separation regression tests pass. This is not live experimental safety equivalence.

Baseline suite passed 275 tests plus both JS DOM suites. Final suite passed 283 tests with six dependency warnings; both existing JS DOM suites pass, including 19 dashboard checks. Logs are under results/. No existing test was edited.

## Resume and revert

Provider payload authorization is already granted for the two named PDFs, questions and excerpts. Read PROGRESS.md first. After sufficient provider quota recovers, run `python -u improve_hyde/experiment.py` from the project root with localhost/network permission. Successful generations are cached by variant, prompt hash, query and token budget in cache/. Results resume per question. `python improve_hyde/experiment.py --raw-only` reruns local Raw checks in disposable storage.

Complete V2 length validation, per-variant latency/cost accounting, routing sweeps, 20-pair inspection, gold uniqueness checks and ranking integration before freezing candidates. Then evaluate only frozen candidates and baselines on fresh HOLD-OUT questions. Merely creating frozen.json is insufficient. Complete the E2E candidate safety comparisons before considering production integration or a default change.

Backups/iter_N retain each pre-edit research revision. Existing README.md, DECISIONS.md and PROMPTS.md were backed up in backups/iter_12 before research-status additions. No application module needs restoration.

Human-reviewed relevance labels, small-sample robustness, a multi-document hold-out, complete semantic entailment, OCR and provider generalization remain unverified. The experiment is incomplete.
