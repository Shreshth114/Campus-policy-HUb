# Human review and second-call evaluation protocol

## Review sequence

Use `review-packet/REVIEW.md` for the initial 12-case calibration. It contains actual source passages and proposed answers, including plausible wrong-situation selections and incomplete evidence. It is AI-assisted, already revealed material from one PDF. It is not a held-out benchmark and cannot establish cross-institution generalisation.

1. Review the original PDF and its applicability/version first. Confirm physical page numbers and exact provisions. Do not substitute a similar summer-course fee for a semester-payment penalty.
2. Independently write the question's atomic evidence requirements, retaining its scenario, actor, event, time and scope. Include amounts/units, deadlines, process, authorities, conditions and exceptions only when the question or applicable provision requires them. Distinguish alternatives and ambiguity from multiple mandatory requests.
3. Judge the proposed selection, not what a better answer could have said. An unselected excerpt cannot complete that selection. Inspect every selected quote/citation against the PDF and the actual excerpt supplied to the model.
4. Record four independent Boolean dimensions: relevance to the actual situation; completeness for all requested parts; source support for every claim/value/meaning; preservation of material qualifications/discretion/deadlines. Record citation correctness and required qualifications separately. A literal quote can still concern the wrong situation.
5. Set `selection_acceptable` and `appropriate_outcome`: answer, withhold, or clarify. Withholding an unsupported selection is not proof that no policy exists. Missing extraction, missing retrieval, ambiguous intent, absent policy, live personal records and provider errors have different causes.
6. Compare the generated question spans against the human atomic requirements. Record missed requirements, unnecessary splits and lost scope in notes. Q0 always contains the entire question; the splitter is a bounded heuristic, not a guarantee of semantic decomposition.
7. Keep each reviewer's copy separate. Prefer two independent reviewers blinded to model verdicts; resolve disagreements against the original source and record adjudication. Do not flip human flags merely because the model or coding agent agrees. The initial packet has zero human labels.

Copy `annotations.template.json` to a new file for each reviewer. Complete every field, including source-PDF checking, supporting provisions, required qualifications, atomic requirements and notes. Only genuine human decisions go in a final adjudicated annotation file. The software checks declarations and consistency; it cannot authenticate whether the named reviewer is human.

## Predictions and scoring

A prediction record contains `case_id`, the unmodified parsed model `review`, and `usage` (`latency_ms`, input/output/reasoning tokens). A failed request has an `error` field and is not scored as a semantic false rejection. Preserve raw responses/messages separately in opt-in local diagnostics or the isolated diagnostic runner. Unknown/duplicate IDs are rejected.

The scorer validates the per-requirement ledger against independently computed requirement IDs and the generator's selected source/provision IDs. It reports:

- False approval: approved unacceptable selections / human-unacceptable selections.
- False rejection: rejected acceptable selections / human-acceptable selections.
- Raw Boolean false approvals separately, exposing cases where four positive flags were overridden by invalid/missing coverage.
- Per-dimension agreement, denominators, unscored counts, service errors and usage completeness.
- Median observed review-provider latency and reported token totals, without adding reasoning tokens to output again.

Evaluate two strata separately: selections that pass deterministic production checks, and deliberately malformed/nonliteral selections used only for isolated reviewer stress testing. Do not combine these strata to make the second model appear safer. The packet includes both; split cases/annotations/predictions by the deterministic result before reporting stratum-specific scores. Inspect false approvals and rejections individually. The model review is fallible and does not replace quote or numeric validation.

Verified plumbing command (the committed templates intentionally return no semantic scores):

```sh
python -m evaluation.ps1.refinements.review_evaluation \
  --cases evaluation/ps1/refinements/review-packet/cases.json \
  --annotations evaluation/ps1/refinements/review-packet/annotations.template.json \
  --predictions evaluation/ps1/refinements/review-packet/predictions.empty.json \
  --output /private/tmp/coverage-review-pending-NEW.md
```

Use a new output filename; the scorer refuses overwrites. Final evaluation needs actual human adjudication and captured predictions. `PENDING_SCORE.md` is an empty-input readiness report, not benchmark performance.

## Cost and latency

`REVIEW_COSTS.md` contains two historical review-call observations. The new ledger's live overhead has not been measured. Future runs must record both provider latency and wall time around the review call (including waits/retries), and separate successful usage from unknown failed-attempt usage. Report selection generation and review usage separately and combined. Do not infer monetary cost without a declared pricing schedule. Keep deployment decisions unchanged when timing the additional review stage.
