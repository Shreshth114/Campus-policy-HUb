# RAG Reliability Audit and Engineering Improvements

You already have the complete context of this project, including its name, architecture, technology stack, existing features, repository structure and implementation history.

Do not spend time rediscovering or rewriting the general project overview.

I have completed a real Groq-only diagnostic run on 16 November 2026. I am providing its complete report and execution traces. Your task is to use these results to identify the actual root causes in the existing codebase and improve the prototype.

This is now a real engineering improvement task. No hardcoded answers, scripted demos, mock LLM responses or artificial success states.

## 1. Observed diagnostic results

Three questions were tested across Raw, HyDE and Fusion: nine application attempts.

- PS1-02: all three modes retrieved the correct B11.4 attendance section first, but failed citation validation.
- PS1-14: Raw and Fusion ranked the make-up examination section first, while HyDE ranked the attendance section first. All three generated incomplete answers without valid citations.
- PS1-21: all three failed because Groq encountered provider rate limits. The correct attendance section was nevertheless retrieved first.

**Zero of nine attempts produced a usable answer.**

This is a diagnostic sample, not a representative benchmark. Do not claim that any retrieval mode is more accurate based on these results.

## 2. Investigate and fix these five issues

### A. Citation validation

The model generated citations as `【C1】`, but the validator expected `[C1]`.

Inspect:
- Citation-generation instructions.
- Citation parsing and normalisation.
- Claim-to-source matching.
- Exact quotation validation.
- The path that converts validation failures into abstentions.

Implement safe canonicalisation of recognised citation formats.

Do not weaken evidence verification. An answer must still cite an existing retrieved source, and every material claim must be supported.

Also address incomplete answers. Correct citation syntax alone must not make an incomplete or unqualified answer acceptable.

### B. Incomplete LLM responses

PS1-14 responses stopped after fragments such as:

- "Yes—you may request a make-up exam"
- "Yes, you can request a make-up exam by applying to the"

All three responses used the configured 350 output tokens.

Investigate:
- Groq response metadata.
- `finish_reason`.
- Visible completion tokens.
- Reasoning tokens, if exposed.
- Response parsing and extraction.
- Output-token configuration.
- Whether reasoning content is consuming the completion budget.

Do not blindly increase token limits.

Ensure incomplete generations are detected and never presented as complete answers.

Capture and log sanitised generation metadata so we can distinguish output truncation, empty content, provider failures and validation failures.

### C. Question intent and ambiguity

PS1-14 asks:

"I was sick and missed classes. Is there a way to still write my finals?"

The system confuses two different situations:

- Missing classes due to illness → B11 attendance condonation.
- Missing an examination due to illness → B15 make-up examination.

Investigate the current query-understanding and retrieval flow.

Improve intent recognition so the system understands the actual event described by the student.

If a question is genuinely ambiguous, ask a concise clarification question rather than confidently choosing the wrong regulation.

Avoid adding an unnecessarily expensive LLM call if a lightweight solution or existing pipeline component can handle the problem.

### D. HyDE hallucinations

Actual generated HyDE passages invented:

- 55% attendance thresholds.
- 75% cumulative attendance.
- Five-day medical certificate deadlines.
- 25% absence limits.
- Unverified offices and approval authorities.

Improve the HyDE prompt so it generates alternative formal policy wording without inventing policy facts.

Explicitly prohibit invented numbers, deadlines, clause references, eligibility criteria, approval authorities and exceptions.

Preserve numbers explicitly provided by the student as question context, but never transform them into invented policy rules.

HyDE output must remain retrieval-only. It must never be treated as authoritative evidence or passed off as an actual university regulation.

Evaluate generated HyDE passages separately from final answer quality.

### E. Groq rate limiting and provider reliability

The diagnostic encountered HTTP 429 TPM errors with an 8,000-token-per-minute limit.

Investigate:
- Token estimation and reservation.
- Request concurrency.
- Retry behaviour.
- Backoff and retry budgets.
- Whether retries make quota exhaustion worse.
- Fusion's additional HyDE generation calls.
- Provider error classification.
- Fallback behaviour.

Implement sensible token-aware pacing, bounded retries and useful error reporting.

Do not confuse provider unavailability with missing policy evidence.

The isolated diagnostic runner had Gemini fallback disabled. Do not change the normal application's provider configuration as part of this work.

## 3. Preserve the following behaviour

These are non-negotiable:

- Real LLM calls only.
- Real ChromaDB retrieval only.
- No hardcoded answers or question-specific response fixtures.
- No fabricated retrieval scores, citations or provider metadata.
- No weakening of grounding and safety checks.
- No silent conversion of provider errors into successful answers.
- No automatic publication or approval of institutional documents.
- No mixing of personal and institutional workspaces.
- No changes to credentials or secrets.
- No destructive database operations.

Do not change the embedding model, chunking strategy, database architecture or production index unless investigation demonstrates a specific issue and you explain the evidence first.

## 4. Implementation approach

Work in this order:

**Phase 1 — Inspect and diagnose**

Trace the exact code paths for all five failure categories. Identify the root causes and relevant files/functions.

**Phase 2 — Establish a baseline**

Run relevant existing tests before changes. Record the results.

Create focused regression tests for:
- Both citation formats.
- Invalid and unknown citation IDs.
- Unsupported claims.
- Missing material conditions.
- Incomplete generations.
- Provider 429 errors.
- Empty provider responses.
- HyDE-generated invented numbers.
- Ambiguous student questions.
- Provider fallback disabled in an isolated runner.

**Phase 3 — Implement fixes**

Make minimal, targeted changes to the existing architecture.

Keep concerns separated: retrieval, query understanding, generation, citation validation and provider reliability should not become one giant function.

**Phase 4 — Regression testing**

Run the relevant tests after implementation.

Compare results against the original baseline. Report test counts, failures and any regressions honestly.

**Phase 5 — Real diagnostic rerun**

Use the same three diagnostic questions and modes after the fixes.

Keep:
- The same PDF.
- The same embedding model and index settings.
- The same retrieval configuration unless the specific change requires otherwise.
- Caching disabled for comparability.
- Groq-only authorisation for this diagnostic.

Do not alter production or institutional data.

The earlier PS1-02 and PS1-14 questions are no longer untouched holdout examples. Do not use them to claim generalisation or tune an official holdout score. Reserve fresh questions for final evaluation.

## 5. Expected answer quality

For PS1-02, a successful answer must cover:

1. At least 80% attendance excluding medical leave.
2. At least 75% overall attendance including medical leave.
3. Recommendations from the Faculty Advisor, concerned faculty and HoD.
4. Submission to AAC by the last instructional day.
5. AAC's discretionary decision.
6. The medical certificate endorsed by IMO.
7. The seven-day/last-instructional-day deadline, whichever is earlier.
8. The maximum two-semester concession.

For PS1-14, the system should recognise that the student describes missed classes, not necessarily a missed examination. If the question remains ambiguous, clarify.

For PS1-21, all requested conditions must be covered. A response that mentions only the two percentages is incomplete.

All these details must be grounded in the actual retrieved source.

## 6. Protect production data

Before making changes:

- Check Git status and current branch.
- Identify uncommitted user changes.
- Do not overwrite or discard existing work.
- Do not modify production ChromaDB collections.
- Do not approve, publish, delete or reset institutional documents.
- Keep diagnostic indexes isolated.
- Preserve environment variables and credentials.
- Verify production-file integrity where practical.

Use the existing test infrastructure and isolated temporary resources.

## 7. Final deliverables

When finished, provide:

1. Root-cause analysis for each observed failure.
2. Exact files and functions modified.
3. Summary of each code change and why it was necessary.
4. New regression tests added.
5. Before/after test results.
6. Results of the nine diagnostic reruns.
7. Actual provider metadata and failure details.
8. Remaining known limitations.
9. Any changes that were deliberately deferred.

Clearly distinguish:
- Confirmed root causes.
- Likely contributing factors.
- Hypotheses that remain unverified.

Do not invent successful results if a provider call fails.

## 8. Execution rules

Do not stop after producing a theoretical audit. Implement the fixes once the repository inspection confirms the proposed changes are safe and appropriately scoped.

However, do not make broad architectural changes or destructive modifications just to make the tests pass.

If a proposed change could affect production data, institutional isolation, credentials or normal provider configuration, stop and explain the risk before proceeding.

Prioritise correctness, source-grounding, reliability and maintainability over adding new features.

**The objective is simple: make the existing prototype reliably retrieve the right policy, understand the student's actual situation, generate a complete evidence-backed answer and gracefully handle provider failures.**