# Step 1: fix answer evidence selection

## Confirmed change

The exact retrieved block from the failed paced ps1-14 Raw execution now supplies complete B11.4 to the answer prompt instead of only `B11. Attendance`. Verified against the entire original B11.4 text after whitespace normalization, including thresholds, recommendations, AAC deadline/discretion, concession limit and medical endorsement/deadline.

`src/answer.py:trim_chunk_span` now removes heading-only candidates from numbered-provision selection, requiring substantive rule wording before query scoring. `src/query_intent.py:provision_terms` supplies generic event vocabulary for that scoring: missed classes adds attendance/absence/shortage; missed exams adds examination vocabulary; illness adds medical/illness terms. These are search/selection cues, not generated policy facts or institution-specific thresholds. Original source text is selected verbatim and remains within the existing per-excerpt budget. Oversized/missing selections still abstain. Source IDs, pages, ordered labels and the original answer question remain unchanged.

## Regression-first verification

New file: `tests/test_provision_selection.py`.

Five tests failed before implementation; all pass afterward:

- Informal illness question selects full B11.4.
- Actual recorded retrieved block produces a prompt containing complete B11.4 and C1/page 10 metadata.
- Heading-only evidence is not accepted as a rule.
- Missing an exam selects the examination provision rather than a section heading or deadline-only clause.
- Different generic section numbering works without institution-specific answers.

Commands:

```sh
python -m pytest tests/test_provision_selection.py -q
# Before: 5 failed
python -m pytest tests/test_provision_selection.py tests/test_answer_grounding_regressions.py tests/test_guardrails.py -q
# After: 47 passed
python -m pytest tests/ -q
# After: 401 passed, 6 dependency warnings, 11.96 seconds
```

SHA-256 snapshots confirm all 244 files under production data and index directories are identical. No provider calls, embeddings, indexing or live database operations were performed. Previous application files are preserved under backups/provision-selection/.

## Scope and remaining limitations

This completes the first step of the agreed sequence: context selection. It does not establish that the model will produce a complete correct answer once it sees the rule. The previous grounding/qualification checks are retained. No accepted-answer count or accuracy result was invented.

Candidate selection still relies on English rule wording and lexical overlap. Some terse rules lacking the recognized substantive wording may be withheld; arbitrary cross-page continuations and multi-provision questions remain outside this small fix. The existing evidence budget and source completeness requirements remain in effect.

Next: improve failure diagnostics, then complete generation and validator false-rejection handling, followed by the controlled live diagnostic rerun. Avoid tuning HyDE until sufficient source evidence reliably reaches generation.

## Files changed

- src/answer.py
- src/query_intent.py
- tests/test_provision_selection.py (new)
- docs/PROVISION_SELECTION_FIX.md (new)
- PROJECT_LOG.md
- DECISIONS.md
