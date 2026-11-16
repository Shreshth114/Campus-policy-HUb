# RAG reliability engineering — 16 November 2026

## Confirmed diagnosis

- Citation parsing accepted ASCII labels only. Groq's `【C1】` therefore caused citation_check_failed before semantic checks. Canonicalization now handles only the recognized positive-number C-label form; unknown/out-of-range citations still fail. Raw response bytes are retained in diagnostic records.
- The Groq adapter discarded finish_reason and reasoning token counts. It now preserves them. Responses marked length are withheld as incomplete_generation. The observed GPT-OSS family now uses low reasoning effort with unchanged output-token limits; other model payloads are unchanged. Previously visible fragments at exactly 350 output tokens suggested budget exhaustion, but the old adapter did not retain sufficient metadata to prove it.
- No lightweight event-understanding step distinguished missing lectures from missing an exam. A generic event-cue module now annotates retrieval questions while preserving the original answer question. Illness questions without a stated event request clarification. Explicitly mixed events are not silently reduced to one event.
- The HyDE prompt asked for authoritative-sounding regulations and did not prohibit invented thresholds/offices. It now requests formal search vocabulary without policy assertions, with a conservative output check that rejects introduced numbers and selected normative/authority language. Rejected passages use the existing visibly traced Raw fallback, never become sources and are never cached as accepted HyDE keys.
- Concurrency control alone did not enforce a token-per-minute budget. A process-local conservative rolling reservation now accounts for prompt bytes and requested completion tokens, including retry attempts, using the observed 8,000 TPM default (`GROQ_TPM_BUDGET` override). Waits remain bounded by the existing wait budget. Provider errors retain sanitized status/retry/detail fields. Credentials, endpoints, provider ordering and fallback configuration are unchanged.

## Scope and tests

Git status/branch checks returned “not a git repository”. Relevant starting application files were copied under backups/reliability-2026-11-16 before edits; production files were hashed. No live Chroma client was initialized against production storage.

Baseline full suite: **387 passed**, six dependency warnings. Initial six focused regression cases: **3 failed / 3 passed**. Final full suite after code changes: **396 passed**, six dependency warnings. The personal frontend suite also passes. Existing network tests use fake transports to verify request contracts; actual engineering reruns use only real Groq calls and actual disposable Chroma retrieval. No fake success state or canned policy response was introduced.

New tests in tests/test_reliability_round.py cover canonical/unknown citations, event and clarification detection, rejected HyDE inventions, token-limited answers, oversized local budget rejection, and actual adapter metadata parsing through an isolated HTTP transport. Existing tests cover unsupported claims, missing conditions, 429 retries, empty responses, workspace isolation and cached answers.

## Modified files

Application: src/answer.py, src/prompts.py, src/hyde.py, src/pipeline.py, src/retrieve.py, src/llm.py; new src/query_intent.py; web/personal.js clarification label.

Evaluation: evaluation/ps1/run_diagnostic.py now supports pacing between attempts and canonicalizes citations before offline claim-failure display. Existing real prompts/raw answers remain retained. New tests: tests/test_reliability_round.py.

Documentation: this file, PROJECT_LOG.md, PROMPTS.md, DECISIONS.md, INTERVIEW_NOTES.md. New run reports are linked below. The complete user instruction is archived as evaluation/ps1/RELIABILITY_REQUEST.md.

## Limitations and deferred work

These changes do not establish reliable answer generation. The first after-change run showed the model still returning a threshold-only answer despite full B11.4 being present; safe grounding validation withheld it. No checks were relaxed to make it pass.

Token estimates are conservative approximations, process-local and not a cross-process quota coordinator. Repeated calls can be rejected locally rather than waiting beyond the request budget; the diagnostic runner therefore adds a 61-second inter-attempt pause. No provider cap is claimed to be universally 8,000 TPM.

HyDE checks are lexical and intentionally conservative; they do not prove fact-free generation. Worded numbers/novel authorities can evade finite patterns. Rejection/fallback rates must be measured. Event cues cover explicit events, not arbitrary language understanding. Ambiguity and informal paraphrase remain limited.

Global duplicate HyDE generation coalescing in concurrent comparison requests is deferred: its cancellation/cache/isolation semantics require dedicated testing. This run uses each mode serially with caches disabled. Structured condition extraction, broad semantic entailment, automatic complete-provision answer repair and retrying poor answers are also deferred; none is safely solved by accepting missing qualifications or silently replacing a model answer with prepared text.

## Actual reruns

- First after-change run: evaluation/ps1/runs/reliability-after-2026-11-16/REPORT.md. All nine attempts recorded, but several encountered the new local quota guard. These are availability outcomes, not retrieval-quality scores.
- Paced rerun: evaluation/ps1/runs/reliability-paced-2026-11-16/REPORT.md. Same PDF, 114 chunks, embedding model, top-k and output token settings. Intent annotation/HyDE prompt/reasoning effort are the disclosed experimental changes. Fallback disabled in runner, no normal provider config edit. Answer and HyDE caching disabled. Existing inspected diagnostic cases are not untouched holdout.

Final outcomes and integrity are appended after the paced run finishes. No accuracy or generalization claim is made from this three-question sample.

## Metadata interpretation

The adapter records total completion tokens and provider-reported reasoning tokens. It does not invent a visible-token count by subtracting them: the raw provider usage remains the source of truth. Empty Groq responses now use a typed ValueError subclass carrying finish/reasoning metadata, and the unified client preserves its sanitized classification. In the paced rerun, the process was already started before this last empty-response diagnostic refinement; its normal nonempty responses still include finish/reasoning metadata, while an empty response may have the earlier wrapper detail. Tests for the latest adapter passed afterward.

## Final measured result

Paced rerun: nine real Groq-only attempts, **0 accepted / 9 abstained**. Four unsupported-claim/qualification failures, two model NO_POLICY_FOUND responses, one quotation failure, two finish_reason=length failures. No provider_unavailable results in the paced run. These results do not establish answer reliability; the requested complete medical-condonation answer remains unsolved. The final Fusion full-condition response finished normally but still failed grounding.

Detailed table and metadata: [paced findings](../evaluation/ps1/runs/reliability-paced-2026-11-16/FINDINGS.md); every actual prompt/output/chunk/score: [full report](../evaluation/ps1/runs/reliability-paced-2026-11-16/REPORT.md); [terminal output](../evaluation/ps1/runs/reliability-paced-2026-11-16/terminal.md). Original and first-after-change records remain separate for comparison.

Final suite: `python -m pytest tests/ -q` — **396 passed**, six dependency warnings, 12.43s. Additional targeted final run: 55 passed; personal frontend suite passes. SHA-256 checks confirm all **244** original production data/index files byte-identical, including SQLite and vector segment files. No institutional approval/publication or production re-index occurred. All real provider responses in this round were Groq; fallback was disabled only in the diagnostic client.

The next engineering step needs an explicitly measured complete-answer strategy and output-budget experiment using observed finish/reasoning metadata; simply accepting the threshold-only output or deleting qualification checks is not acceptable. It should be tested on fresh development questions, retaining these cases as diagnostics.
