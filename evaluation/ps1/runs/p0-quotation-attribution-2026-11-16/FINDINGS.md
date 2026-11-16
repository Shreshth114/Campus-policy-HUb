# P0 Step 1 — per-quotation attribution fix

Scope: only the recorded PS1-14 Fusion development failure. No held-out labels or questions were modified or executed.

## Exact diagnosis

The original response contains five source-matching quotations but only one citation after quotation 5. Original validator look-ahead and prior-label fallback could also accidentally attribute quotations in other layouts. The fix requires same-line adjacency to each closing quotation; optional punctuation/whitespace is accepted, but no intervening prose, other quotation, newline or inherited preceding label.

Failures now carry distinct reasons: `missing_quote_citation`, `invalid_quote_citation`, `quote_mismatch`. Existing aggregate `citation_check_failed` / `quote_verification_failed` outcomes remain; no claim, number or qualification checks were relaxed. `_answer_units()` was inspected and left unchanged: strict independent quote attribution rejects retroactive attribution even where claim units share a line. No citation guessing or repair is introduced.

## Implementation

- `src/prompts.py`: answer-generation instructions require one valid same-line citation immediately after every individual quotation, including repeated references to the same source. HyDE and other unrelated prompts unchanged.
- `src/evidence.py:verify_quotes`: replace forward scanning/prior-label inheritance with anchored adjacent attribution; classify missing labels, invalid/unknown labels and text mismatch separately.
- `src/answer.py:validate_answer`: preserve these individual reasons instead of overriding failures with generic quote_mismatch.
- `tests/test_quotation_attribution.py` and `tests/fixtures/quotation_attribution/ps1_14_fusion.json`, `README.md`: exact raw failed response/messages, plus positive and negative cases.
- `evaluation/ps1/run_diagnostic.py`: mode selection permits only Fusion rerun; retains per-quotation verified/failed diagnostics for raw output. Retrieval and normal provider configuration unchanged.

## Tests

New regressions before change: **9 failed, 1 passed**. After change, targeted quotation/grounding suites: **66 passed**. Full `python -m pytest tests/ -q`: **418 passed**, six dependency warnings, 16.94 seconds. No tests weakened.

Coverage includes the original five-quote response (four missing attributions), individually cited exact quotations, same-paragraph trailing-citation rejection, preceding/separate-line/delayed attribution rejection, unknown/zero/malformed labels and changed threshold quotation rejection.

## Real diagnostic command

```sh
HF_HUB_OFFLINE=1 python -u evaluation/ps1/run_diagnostic.py --ids ps1-14 --modes fusion --pdf 'LOCAL_POLICY_PDFS/BTech_(Rules_&_Regulations)2013_21nov2023.pdf' --output evaluation/ps1/runs/p0-quotation-attribution-2026-11-16
```

The requested Groq-only run used actual disposable Chroma retrieval, 114 chunks, the existing embedding model/settings and disabled answer/HyDE caches. No Gemini calls.

## Raw model output

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%" [C1].  
"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester" [C1].  
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam" [C1].  
"A student will be eligible for this concession at most in two semesters during the entire degree programme" [C1].  
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier" [C1].
```

## Individual quotation results

| Quote | Adjacent label | Exact-source verification |
|---|---|---|
| 1 | C1 | passed |
| 2 | C1 | passed |
| 3 | C1 | passed |
| 4 | C1 | passed |
| 5 | C1 | passed |

Failed quotations: **0**. Final application decision: **answered**. Final validation failures: **none**. Additional source-condition completion: **not used**. HyDE fallback: **false**. No raw answer citation repair was needed.

Provider/model: Groq / `openai/gpt-oss-120b`; finish_reason `stop`; input tokens **949**, completion tokens **296**, provider-reported reasoning tokens **88**, answer-call latency **1,973 ms**. This is one successful development observation, not a reliability rate or held-out accuracy result.

## Production integrity discrepancy

The historical baseline had 244 files. The starting snapshot for this task has **237**, with **7 personal-workspace files already absent** and **2 surviving file hashes already different** versus the old snapshot. No cause is inferred. All 237 starting files, including current database/vector files and institutional sources, remained byte-identical; no files were added or removed in production paths during this task. Therefore the exact “all historical 244 remain byte-identical” statement cannot truthfully be made. Historical differences were present before edits and the diagnostic. No approval, publication, production indexing or document modification was performed.

## Limits

The generation contract is enforced by rejection, not a guarantee that the model always follows it. In future, missing/incorrectly positioned citations still abstain. A citation before a quote or on a separate line is deliberately rejected. Source wording must still match under existing normalization; semantic paraphrases in quotation marks remain invalid. This single successful run does not generalize beyond the tested development case. The historical production-manifest discrepancy remains an explicit limitation.

## Artifacts

[Full execution report](REPORT.md) · [Raw JSON](ps1-14-fusion.json) · [Actual terminal output](terminal.md) · [Current integrity check](integrity.json)