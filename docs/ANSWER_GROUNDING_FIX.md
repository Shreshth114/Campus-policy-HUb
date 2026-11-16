# Answer context, grounding and diagnostics fix — 2026-11-14

## Scope and implementation

No re-index, live embeddings, provider calls, provider changes or live database write operations were performed. All executable pipeline tests used the repository's temporary-storage fixtures and mocked providers/embeddings. No existing tests were weakened.

Application files modified:

- `src/answer.py`: selects a complete query-relevant numbered provision under the existing `CHUNK_MAX_TOKENS * 4` per-excerpt budget and existing `ANSWER_CHUNKS_LIMIT`. Unnumbered passages retain every distinct sentence, removing only exact repeated sentences if necessary to fit. If the selected evidence still exceeds the budget, abstains before calling the model. Preserves ordered labels, IDs and page metadata. Shared `validate_answer` checks citation references, quotes, claims and qualifications against precisely the selected excerpts; retains established rejection reasons and reports individual failures. Responses carry the exact selected excerpts for tracing/caching.
- `src/evidence.py`: conservative clause-level lexical validation. Every substantive response unit needs a citation; all substantive tokens and numerical values must be supported together by one cited source clause. Normalizes a small generic vocabulary such as “at least” / “or more”, percent notation and “outside” / “excluding”. Checks negation and rejects ambiguous multi-number paraphrases unless exact source wording supports them. Unknown consequences fail support checks. Associated approval/discretion/exception/deadline qualifications must also be represented. The older `unsupported_claims` helper delegates to the same validator.
- `src/pipeline.py`: cached answers use the same validator with recorded sent excerpts. Older entries without these excerpts safely miss; files are not proactively cleared. Existing workspace, citation and fingerprint checks remain. Cached citation mappings must agree with the validated labels. Optional diagnostics also cover cache revalidation.
- `src/trace.py`: adds optional `ChunkTrace.answer_excerpt`; full retrieved text remains available separately.
- `src/prompts.py`: requests complete associated qualifications, exact condition/value associations and source wording; prohibits uncited filler. No provider settings changed.
- `src/answer_diagnostics.py` (new): opt-in local diagnostics using an allowlisted payload. Records messages, ordered selected excerpts, document/chunk/source IDs, pages, selection/size information, raw rejected answers and validation failures. No request headers or workspace fields are logged. Known provider/admin secrets, workspace capabilities, recognizable key/capability patterns and labelled credentials are redacted. Files use mode 0600, newly created directories 0700; refuses destinations under production data/index directories or served web files. I/O failure does not alter the answer result.

Tests added: `tests/test_answer_grounding_regressions.py` (24 cases).

Documentation updated: this report, `PROMPTS.md`, `DECISIONS.md`, `INTERVIEW_NOTES.md`, `PROJECT_LOG.md`.

## Regression-first evidence

Before implementation, the first 11 regression cases produced **7 failures and 4 passes**. Failures reproduced incomplete B11.4, missing conditions, swapped thresholds, invented penalties, uncited statements, cached unsupported answers and validation using unsent context. The fake cache fixture includes all required trace fields, so it exercises a genuine cache candidate rather than an unrelated parsing failure.

Final command:

```sh
python -m pytest tests/ -q
```

**353 passed; 6 dependency deprecation warnings; 11.11 seconds.** Includes all 329 pre-existing cases and 24 new cases. Intermediate focused runs also passed, including 64 answer, guardrail, evidence, end-to-end and personal-workspace cases before the last three regression additions. No external API calls.

Coverage includes:

1. Full page-10 B11.4—including AAC discretion, application recommendations, the two-semester restriction and the medical-certificate deadline—survives context construction.
2. Correct 80% excluding medical leave / 75% overall answer with complete qualifications is accepted.
3. Omitting AAC discretion alone is rejected, as is omitting the qualifications collectively.
4. Fabricated 60%, swapped 80%/75%, invented coursework penalties and uncited statements are rejected.
5. Correctly quoted complete provisions pass; ambiguous multi-value paraphrases fail closed.
6. Fresh and cached unsupported answers are rejected; valid caches continue to work.
7. Values present in full retrieved text but absent from sent excerpts cannot support an answer.
8. HyDE is absent from answer messages; existing cross-workspace protections remain tested.
9. Oversized provisions cause abstention without a model call.
10. Diagnostics are disabled by default, redact test credentials/capabilities, retain exact nonsecret excerpts, restrict permissions and cannot write to production storage.

## Optional diagnostics

To enable deliberately on a local server startup (not executed during this task):

```sh
ANSWER_DIAGNOSTICS_ENABLED=true \
ANSWER_DIAGNOSTICS_DIR=/private/tmp/campus-answer-diagnostics \
python -m src.server
```

Both variables are required. Leave the enabled flag unset to disable. Logs contain user questions and policy excerpts, so treat the directory as private local debugging material and remove it when no longer needed. Secret-containing strings are redacted, rather than recorded literally. Logs do not expose a new API or browser download route.

## Limits

This is a conservative consistency validator, not a general semantic-entailment engine. It accepts exact evidence and limited, clause-supported paraphrases; valid novel paraphrases may abstain. Unrecognized contradictions are not mathematically ruled out. The selector can preserve only provisions available in retrieved evidence, and selects one relevant provision per active block; it does not retrieve missing continuations or synthesize missing conditions. Oversized selected provisions abstain rather than raising the context budget. Source sentence boundaries and numbered-rule recognition remain heuristic. No success rate or real-provider reliability claim is made without a live evaluation. The current live NIT Goa chunks were not updated by this work.
