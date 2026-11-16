# Frozen exploratory execution protocol

Review provenance: AI-assisted source inspection; human verification pending. All ten questions and exact source/rubric text were frozen in labels.json before execution. manifest.json records its SHA-256. Original FRESH_HOLDOUT_REVIEW.md and production labels are untouched.

## Execution

Actual PDF, current application prompts/thresholds/embedding model, one disposable 114-chunk personal index, Groq only with fallback disabled locally. Answer cache and HyDE cache disabled. One repetition per question/mode. Mode order rotates Raw/HyDE/Fusion, HyDE/Fusion/Raw, Fusion/Raw/HyDE. A 25-second inter-attempt pause is outside request latency. Embedding/index setup precedes all measured requests. No mid-run application/prompt tuning.

Runner: evaluation/ps1/run_diagnostic.py --questions-file evaluation/ps1/frozen-ai-review/labels.json --balanced --pause 25 --pdf <source PDF> --output <new run directory>.

frozen_settings.json records Python/packages, application source hashes, exact prompts, model/retrieval settings and label hash. corpus.json records actual isolated chunks; evidence_mapping.json was generated before query execution. Captured retrieval_before_merge preserves vector ranks and scores before answer-context merging. Each case records actual prompt messages, raw provider outputs, final trace/answer, token/finish metadata and errors. Successful request usage is known; failed-provider/retry token usage can be unknown and must never be counted as zero cost.

## Scores and denominators

Retrieve first relevant rank and complete evidence-group recall at k=1/3/5. Multiple chunks containing a required sentence are alternatives, not independently mandatory. A missing evidence mapping is a mapping defect: do not present that case as a clean ranking win/miss. Keep its outputs and partial coverage visible. fresh-04 and fresh-07 currently contain unmapped source sentences; their reciprocal-rank scores are null rather than silently zero.

Raw-model and final-application exact-span coverage are separate mechanical measurements. They deliberately underestimate faithful paraphrases and cannot prove semantic correctness. Report quote attribution/content checks separately from application acceptance and semantic grades. Raw generated NO_POLICY_FOUND, final safe abstention, clarification and provider/local-quota unavailability are distinct outcomes. Source-completion rates are reported, not attributed to independent model reasoning.

For mode quality: compare identical mapped answerable cases; report all service failures and Raw fallbacks. Genuine HyDE comparisons exclude explicitly flagged Raw fallbacks, with exclusions disclosed. Positive cosine differences across query embeddings are not relevance gains. No winner/superiority or human-verified accuracy is declared from this small exploratory run. Human raw/final grading remains pending, with fields in metrics.json.

## Final-review gate

A human reviewer must accept/edit/reject source relevance and judge every raw/final answer against the frozen rubric: factual meaning, required qualifications, no invented permission/consequence, exact citation support, appropriate abstention. No automation changes labels_verified. Once outputs are inspected, this set is revealed; further tuning requires a new final set. This run must not be relabelled as a completed human-approved held-out evaluation.
