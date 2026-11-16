# PS1: reliable answers and an honest Raw–HyDE comparison

16 November 2026

## Newest execution — ten-question exploratory run

See [FROZEN_TEN_EVALUATION_EXECUTION.md](FROZEN_TEN_EVALUATION_EXECUTION.md). Thirty real attempts completed using a frozen AI-assisted rubric (human verification pending): Raw 4/10, HyDE 3/10 and Fusion 3/10 application acceptances. These are not semantic accuracy rates. Two source mappings are incomplete; genuine same-case Raw/HyDE retrieval subset has n=3, with 0 HyDE wins/2 ties/1 loss. Nine accepted responses used source completion. Full suite 422 passed; all 237 current production files byte-identical. Human final adjudication remains outstanding. Earlier diagnostic summaries below are historical.

## Latest completion round

See [PS1_COMPLETION_ROUND.md](PS1_COMPLETION_ROUND.md): full suite 408 passed; final actual nine-attempt Groq-only diagnostic produced 8 accepted application responses and 1 quote-verification abstention. Some accepted outputs include explicitly disclosed verbatim source conditions, and three attempts used Raw fallback. This is diagnostic progress, not verified accuracy or HyDE superiority. Fresh final question/answer labels remain pending human review. Older results below are historical.

## Reliability engineering update

The subsequent fixes and paced rerun are documented in [RAG_RELIABILITY_ENGINEERING.md](RAG_RELIABILITY_ENGINEERING.md). Final suite: 396 passed. Paced real diagnostic: 0/9 accepted, with no provider-unavailable outcomes but remaining grounding/completeness failures. Citation syntax handling and failure metadata improved; reliable answer coverage has not been achieved. The older status below is historical.

## Latest status — 16 November 2026

The initial plan below is preserved for context. Evaluation has now started:

- 30 draft questions prepared under `evaluation/ps1/`; none human-verified.
- Actual Groq-only diagnostic completed: 3 questions across Raw, HyDE and Fusion, 9 attempts.
- Application outcomes: 6 citation-check abstentions, 3 provider-unavailable outcomes, 0 accepted answers in this diagnostic subset.
- Observed nonstandard citation syntax, incomplete visible answers at the output-token limit, hypothetical numeric inventions and a Groq 429 error.
- Informal attendance question ranked page 10 first under HyDE versus page 11 under Raw/Fusion; this is an inspected observation, not verified benchmark improvement.
- No fixes have been applied following these live findings. No accuracy winner is established.
- Last complete automated suite: 387 passed before the diagnostic scripts were added. Diagnostic scripts passed Python compilation; no claim of a new full-suite run is made.
- All 244 production data/index file hashes matched before/after the live diagnostic.
- Two inspected proposed holdout cases must be replaced before a final untouched evaluation.

Actual results: [Findings](../evaluation/ps1/runs/groq-only-2026-11-16/FINDINGS.md), [full execution report](../evaluation/ps1/runs/groq-only-2026-11-16/REPORT.md). Chronological record: [PROJECT_LOG.md](../PROJECT_LOG.md).

## Objective

Demonstrate Dell PS1's core chain: informal student question → policy retrieval → real source evidence → accurate answer or justified abstention. The experiment must show where HyDE wins, ties or loses. A different answer is not evidence of better retrieval, and a hypothetical HyDE policy is never an answer source.

## Completed in this round

The existing benchmark now retains each question's actual HyDE passage, provider usage, retrieved IDs, reciprocal rank and Recall@3. It calculates paired Raw–HyDE wins/ties/losses on the same questions, excluding retrieval errors, missing modes and HyDE fallback-to-Raw observations from the genuine HyDE-quality comparison. Exclusions remain visible. Aggregate mode metrics still describe service behavior including failures/fallbacks and are explicitly distinguished from paired quality results.

It no longer declares a unique best mode for tied results, incomplete retrieval runs or HyDE failures. A HyDE fallback causes a completed-with-errors status rather than an apparently clean experiment. These changes are metric/reporting fixes, not measured retrieval improvement.

Changed code: `bench/run_benchmark.py`; regression cases added to `tests/test_benchmark.py`. No retrieval prompts, providers, thresholds, index or documents changed.

## Current measurement prerequisite

The real personal-document workspace currently contains zero benchmark questions and zero labels flagged as verified. No accuracy numbers or claim of HyDE superiority can be produced from that state. This check read JSON metadata only and did not initialize the live vector database.

## Next work, in order

1. Resolve the diagnosed answer/extraction reliability defects, especially threshold/operator recognition, incomplete extraction checkpoints and unnecessary rejection of faithful paraphrases. Preserve safety protections and test accepted as well as rejected answers.
2. Draft 30 questions from the actual uploaded regulations: 10 direct factual, 10 informal scenarios, 5 multi-condition questions and 5 out-of-scope cases. Attach exact source provisions/pages and proposed current chunk targets. Mark every draft unverified until reviewed by the user; never treat model-generated labels as human verification.
3. Split the reviewed cases into a small development set and an untouched final evaluation set before tuning. Include general attendance versus medical condonation, approvals, deadlines and misleading near-matches. Do not pick only questions where HyDE is expected to win.
4. Freeze corpus version, chunk IDs, embedding model, top-k, HyDE prompt/model and relevance labels for each measured run. Start with Raw versus HyDE; include Fusion secondarily. Disable answer caching for comparisons, identify HyDE caching state, warm local embedding initialization separately and report cold/warm timings clearly.
5. Measure retrieval first: Recall@1/3/5, reciprocal rank/MRR, per-question ranks, wins/ties/losses, provider failures, latency and usage. Separate fallback availability from genuine HyDE quality. Repeat stochastic HyDE runs when quota permits; do not hide run-to-run variability.
6. Evaluate answering separately on the same questions: all requested facts supported, conditions retained, no invented permissions, correct citations, answerable-question false abstentions and out-of-scope abstentions. Passing citation-format checks alone is not semantic accuracy. Use human review for final correctness labels.
7. Present a representative win, a tie and a failure/abstention alongside the complete held-out results. If Raw is already better, report that and explain when HyDE's additional cost is not justified. Keep the demo selectable and live, never scripted.

## Completion criteria

- Actual source evidence supports every displayed answered claim, including threshold conditions and required approvals.
- No answer content is copied from the hypothetical passage.
- Reviewed labels and reproducible measurements exist; errors and excluded pairs are disclosed.
- HyDE's benefit, or lack of benefit, is based on the frozen evaluation set rather than the appearance of different wording.
- No claim of production readiness, universal hallucination prevention or statistical significance from a small sample.

## Test evidence

`python -m pytest tests/ -q` — 387 passed, six existing dependency warnings. Five new regression cases cover paired wins/ties/losses, missing/fallback exclusions, absent measurements, recorded HyDE observations, tied winners and failure status. All fixture results are synthetic test arithmetic, not university retrieval scores. No live LLM calls, embedding generation, re-indexing or production-result writes were performed.
