# Archived fee/deadline failure trace

Offline inspection only. No new provider call, document indexing or label edits.

## Correction: two different questions

The later dev-compound question asks for a late SEMESTER-payment fee after classes start. No supporting provision was identified in the extracted original 22-page PDF. Its B17.5 is a SUMMER-course registration fee and must not be substituted. The archived development metadata expect=answer was an unverified assumption, not a gold label. Leave that archive intact; do not score it as a retrieval miss. Human confirmation remains pending.

The genuine earlier fresh-06 question asks whether passing summer subjects waives registration deadlines/fees. B17.2 and B17.5 are relevant to that question. These are revealed development cases, never untouched evaluation.

## Archived raw

Actual path: Raw; no fallback.

Will passing every summer subject let me ignore the summer registration deadline and fee?

| Provision | Candidate rank | In merged block | Sent to model | Complete in final text | Retained by current selector replay | Loss stage |
| --- | --- | --- | --- | --- | --- | --- |
| B17.2 | [1] | True | True | False | True | after_context_or_none |
| B17.5 | [1] | True | False | False | True | context_selection |

Archived decision: answered. Replay checks context inclusion only; it does not rerun generation or establish answer correctness.

Source record: `evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/fresh-06-raw.json`.

## Archived hyde

Actual path: Raw fallback (`hyde_failed=true`); not a genuine HyDE quality observation.

Will passing every summer subject let me ignore the summer registration deadline and fee?

| Provision | Candidate rank | In merged block | Sent to model | Complete in final text | Retained by current selector replay | Loss stage |
| --- | --- | --- | --- | --- | --- | --- |
| B17.2 | [1] | True | True | False | True | after_context_or_none |
| B17.5 | [1] | True | False | False | True | context_selection |

Archived decision: abstained. Replay checks context inclusion only; it does not rerun generation or establish answer correctness.

Source record: `evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/fresh-06-hyde.json`.

## Archived fusion

Actual path: Fusion with no reported HyDE fallback.

Will passing every summer subject let me ignore the summer registration deadline and fee?

| Provision | Candidate rank | In merged block | Sent to model | Complete in final text | Retained by current selector replay | Loss stage |
| --- | --- | --- | --- | --- | --- | --- |
| B17.2 | [1] | True | True | False | True | after_context_or_none |
| B17.5 | [1] | True | False | False | True | context_selection |

Archived decision: abstained. Replay checks context inclusion only; it does not rerun generation or establish answer correctness.

Source record: `evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/fresh-06-fusion.json`.

## Conclusion

Both target provisions were in the FIRST candidate in all three archived modes. The old selector retained B17.2 and dropped B17.5. The current complete-block selector retains both on replay, including the fee-change qualification. No ranking/top-k/model change is justified by this trace. Future genuine candidate-recall failures should be investigated separately with per-requirement probes; any expansion must be an explicit mode variant rather than silently redefining Raw.

## Supporting provisions

PDF page 12: 

B17.2. Summer term courses will be announced by the AAC after the publication of results of the even semester, if a minimum of 20% of the total registered regular students fail in a course. A summer term course may be offered by a department on the recommendation of the CC/DCC and with the approval of the AAC. A student will have to register within the time stipulated in the announcement by paying the prescribed fees.

PDF page 12: 

B17.5. A student will have to register within the time stipulated in the announcement by paying the prescribed fees of ₹ 5000/- per course. The amount will change periodically as per Senate approval. (Amended in 23rd Senate meeting)


Saved candidates are the returned pre-merge top-k list, not an unseen internal ANN candidate pool. No new vector query or provider call was made.
