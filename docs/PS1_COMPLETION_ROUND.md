# Reliability implementation order — completion round

## Implemented work

1. Evidence selection: completed previously; exact failed informal context now selects full B11.4 rather than a heading.
2. Diagnostics: Trace.validation_failures preserves individual uncited/unsupported/omitted-condition/quote errors; personal explainability renders the reasons. Existing aggregate abstention codes remain compatible.
3. Generation: prompt requests complete relevant source quotations, with no uncited summary. Output budget now follows the selected evidence length (roughly one token per two source characters plus 160 overhead), bounded at 1,200 and never below configured ANSWER_MAX_TOKENS. Context budget and model identity are unchanged. This controlled increase follows measured length finishes at 350 tokens; length-limited generations are still rejected. It is not a guarantee of complete output or a fixed answer fixture.
4. Validator: normalizes a narrowly tested equivalent deadline expression (“no later than” / “on or before”). Unsupported values, swapped conditions, missing qualifications and invented permissions still fail. Existing cache path uses the same validator. Broad free paraphrase acceptance remains deliberately restricted because lexical matching is not entailment.
5. Live diagnostics: actual nine-attempt Groq-only rerun is recorded under evaluation/ps1/runs/reliability-completed-2026-11-16. No mock answers used in that execution; normal fallback configuration unchanged, fallback disabled in runner only. Tests use isolated fake transports as before.
6. HyDE/Fusion efficiency: compare requests now share one in-flight HyDE generation via request-local ContextVar state keyed by the scoped query/configuration key. It is not a cross-user global answer cache. Cancellation cleanup drains pending tasks. Raw/Fusion searches remain independently executed; no unnecessary vector-database architecture change. The previous HyDE fact-invention checks remain conservative and explicit Raw fallbacks remain visible.
7. Final held-out evaluation: fresh proposed questions are in evaluation/ps1/FRESH_HOLDOUT_REVIEW.md. Diagnostic questions are excluded from untouched-holdout claims. Human relevance/answer-label decisions are outstanding; no labels were promoted and no official accuracy table was manufactured.

## Code and tests

Application files changed this round: src/answer.py, src/evidence.py, src/prompts.py, src/trace.py, src/pipeline.py, src/hyde.py, src/server.py, web/personal.js. No other application modules were modified this round.

New tests: tests/test_reliability_completion.py (seven cases, covering deadline equivalence, bounded complete-source output budget, individual validation reasons, invented threshold rejection and request-scoped generation sharing).

Initial four regressions: two failed/two passed. Final full suite: `python -m pytest tests/ -q` — **408 passed**, six dependency deprecation warnings, 14.70s. Personal frontend suite passes. No existing tests were weakened.

Documentation added: this report and fresh-holdout review sheet. PROJECT_LOG.md, PROMPTS.md and DECISIONS.md updated. Actual run artifacts include REPORT.md, FINDINGS.md and terminal.md with raw JSON retained alongside them.

## Boundaries

The code changes do not by themselves establish answer accuracy or HyDE superiority. Final baseline outcomes are recorded after execution below. All evaluation labels remain unverified. No production index or document was altered; hash integrity is checked independently. Provider cost/latency may increase with the source-size output allowance and is disclosed in the run metadata. The token reservation accounts for the higher request budget. Compare sharing saves duplicate HyDE generation within a compare request, not across independent diagnostic attempts with caching disabled.

## Source-condition completion safeguard

If, and only if, the model response contains solely verified source quotations and the only failures are omitted qualifications, `answer.complete_source_conditions` appends missing qualifying sentences verbatim with their existing citation labels. It then runs the complete validator again. Any free paraphrase, invented number, changed quote, bad citation, insufficient evidence or length finish prevents this completion path. A warning explicitly says that source conditions were appended, and the original model output remains in diagnostic records. This is a generic evidence-completeness operation, not a prepared answer or institution-specific threshold rule.

Unicode whitespace is normalized for quotation support matching; raw source/model text is preserved. The regression contains the actual curly-quote/narrow-space pattern. Empty non-substantive context candidates are omitted with labels re-numbered consistently; trace order follows sent evidence before unused retrieval blocks. Cache revalidation uses actual selected excerpts in that order.

Intermediate runs under complete-provisions, final-completion and completion-verified are marked interrupted, with their available observations preserved. They are debugging history, not the final nine-case result. The final run is under reliability-completed-2026-11-16. No claims of complete execution are made for interrupted directories.

## Explicit remaining evaluation limitation

The final held-out stage cannot be completed honestly from an acknowledgment alone. All draft/fresh labels remain pending human review; there is no verified accuracy claim. The supplied fresh questions are a review package, not scored labels. The nine repeated diagnostic cases are development evidence.

## Final actual execution result

**8 of 9 final application responses passed**, versus 0 of 9 in the earlier paced diagnostic. The informal Fusion response was withheld for quote_verification_failed. No provider_unavailable results in this final run. Three attempts used HyDE rejection/Raw fallback; these do not count as evidence of HyDE quality. All accepted attendance answers retain the source qualifications, either in the model-selected quotation or as explicitly disclosed verbatim source-condition additions. Raw LLM text is preserved separately, so final application acceptance must not be described as the model independently generating every condition.

Actual records: [findings](../evaluation/ps1/runs/reliability-completed-2026-11-16/FINDINGS.md), [full prompts/answers/evidence/scores](../evaluation/ps1/runs/reliability-completed-2026-11-16/REPORT.md), [terminal output](../evaluation/ps1/runs/reliability-completed-2026-11-16/terminal.md). Offline claim_failures in the JSON concern raw model text; trace.validation_failures and decision concern the final application validation after any allowed source completion.

No benchmark labels were approved. A verified held-out evaluation remains pending explicit accept/edit/reject decisions. Final complete automated suite: **408 passed**, six warnings, 14.70 seconds. All **244** starting production data/index SHA-256 hashes matched after all executions. No credentials, normal provider configuration, source approvals or production index changed.

Remaining limitations: English lexical intent/validation, missing multi-page retrieval evidence, occasional altered model quotes, source-completion conservatism and HyDE assertion fallbacks. These changes improve this diagnostic sample but do not establish production reliability. Final held-out scoring cannot be completed without actual reviewed labels.
