# AI-assisted raw versus final answer assessment

Reviewer: Codex, inspecting actual saved outputs against frozen AI-assisted source rubrics. Human verification: **pending**. These are qualitative AI assessments, not human-reviewed benchmark labels or verified accuracy scores. Source quotations and all final answers are available in RESULTS.md. No model/prompt tuning was performed against this run.

| Case | Mode | Raw model assessment | Final application outcome |
|---|---|---|---|
| fresh-01 | fusion | answerable_abstention | abstained / no_policy_found |
| fresh-01 | hyde | answerable_abstention | abstained / no_policy_found |
| fresh-01 | raw | answerable_abstention | abstained / no_policy_found |
| fresh-02 | fusion | partial_and_misquoted | abstained / quote_verification_failed |
| fresh-02 | hyde | answerable_abstention | abstained / no_policy_found |
| fresh-02 | raw | partial_and_misquoted | abstained / quote_verification_failed |
| fresh-03 | fusion | wrong_scope | answered / accepted |
| fresh-03 | hyde | answerable_abstention | abstained / no_policy_found |
| fresh-03 | raw | wrong_scope | abstained / quote_verification_failed |
| fresh-04 | fusion | supported_core_misquoted | abstained / quote_verification_failed |
| fresh-04 | hyde | supported_core_misquoted | abstained / quote_verification_failed |
| fresh-04 | raw | supported_core_partial_rubric | answered / accepted |
| fresh-05 | fusion | correct_core_and_qualification | abstained / unsupported_cited_claim |
| fresh-05 | hyde | correct_core_and_qualification | answered / accepted |
| fresh-05 | raw | correct_core_and_qualification | abstained / unsupported_cited_claim |
| fresh-06 | fusion | answerable_abstention | abstained / no_policy_found |
| fresh-06 | hyde | answerable_abstention | abstained / no_policy_found |
| fresh-06 | raw | partial_missing_fee_qualification | answered / accepted |
| fresh-07 | fusion | partial_unfinished_quote | answered / accepted |
| fresh-07 | hyde | correct_core | answered / accepted |
| fresh-07 | raw | correct_core | answered / accepted |
| fresh-08 | fusion | correct_formula | answered / accepted |
| fresh-08 | hyde | correct_formula | answered / accepted |
| fresh-08 | raw | correct_formula | answered / accepted |
| fresh-09 | fusion | not_generated | clarification_required / accepted |
| fresh-09 | hyde | not_generated | clarification_required / accepted |
| fresh-09 | raw | not_generated | clarification_required / accepted |
| fresh-10 | fusion | appropriate_abstention | abstained / no_policy_found |
| fresh-10 | hyde | appropriate_abstention | abstained / no_policy_found |
| fresh-10 | raw | appropriate_abstention | abstained / no_policy_found |

## fresh-01

Raw: No model supplied the requested process/documentation evidence.

Final: All three abstain on an answerable question under the frozen rubric.

## fresh-02

Raw: Raw/Fusion state SGPA/CGPA exclusion but omit overall-credit inclusion and alter quoted wording; HyDE abstains.

Final: All withheld; source-grounded fact is partly present in raw text, so rejection is not equivalent to a retrieval miss.

## fresh-03

Raw: Raw/Fusion describe general semester registration, not the return-from-discontinuation procedure. HyDE abstains.

Final: Fusion is accepted despite failing the intended B8.2 rubric; source support alone does not establish relevance. The wording “semester break” also warrants human ambiguity review.

## fresh-04

Raw: All convey the at-least-one-failed condition. Raw is an exact supported quote; HyDE/Fusion add “The” inside their quotation. Raw does not include every frozen span.

Final: Raw accepted with additional conditions; HyDE/Fusion withheld for quotation fidelity. Cross-page mapping remains incomplete, so do not rank-score this case.

## fresh-05

Raw: All correctly include device prohibition and Senate-approved exception.

Final: HyDE accepted with extraneous charts/tables source addition. Raw/Fusion false-abstain despite faithful cited quotes: claim-unit processing remains brittle for same-line quote sequences.

## fresh-06

Raw: Raw gives deadline/payment obligation but omits the fee value and change qualification. HyDE/Fusion abstain.

Final: Raw accepted despite incomplete multi-provision evidence coverage; source completion cannot add a provision that was not selected.

## fresh-07

Raw: Raw/HyDE give correct W/F CGPA equivalence. Fusion includes that fact but stops its quoted sentence at “may be considered for”.

Final: Raw/HyDE accepted with extra grading conditions. Fusion accepted an unfinished substring despite finish_reason=stop. Mapping incomplete; content completeness needs a separate check.

## fresh-08

Raw: All provide the exact conversion formula.

Final: All accepted, but automatic source completion adds irrelevant GPA-definition material. More text is not necessarily a better answer.

## fresh-09

Raw: No answer model call: event-understanding gate intervened.

Final: All ask whether classes or an exam were missed. This avoids a fabricated approval but fails the intended explicit live-record capability limitation.

## fresh-10

Raw: All return NO_POLICY_FOUND for unavailable live room allocation.

Final: All safely abstain; helpful routing to the official timetable is still limited.