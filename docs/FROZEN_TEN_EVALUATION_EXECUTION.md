# Ten-question evaluation execution — 16 November 2026

## Status and review provenance

Completed the requested source review, label/rubric freeze, runner improvements, 30 real attempts and separate raw/final assessments. The review is explicitly **AI-assisted**, not human verification. No production `labels_verified` flag was set. This is an exploratory frozen-set evaluation, not a completed human-approved benchmark. Human approval and final semantic grading remain outstanding.

The ten original questions are unchanged. Before execution, exact supporting provisions, required qualifications, prohibited inferences and acceptable abstentions were frozen in `evaluation/ps1/frozen-ai-review/labels.json`, with its SHA-256 and source-PDF hash in manifest.json. Full source review: `evaluation/ps1/frozen-ai-review/REVIEW.md`. Physical PDF pages were inspected, including the cross-page re-examination rule and conversion formula. No policy facts were generated as source text.

Alternative chunk IDs were mapped before queries in the disposable index. Multiple chunks containing a source sentence are alternatives; separate required sentences are distinct requirements. Two cases (fresh-04, fresh-07) contain sentences spanning chunk boundaries with no whole-sentence target mapping. Their reciprocal ranks are unscored; partial evidence coverage remains visible. This limitation was identified before those cases ran and no labels were edited to improve results.

## Reproducible execution

```sh
HF_HUB_OFFLINE=1 python -u evaluation/ps1/run_diagnostic.py \
  --questions-file evaluation/ps1/frozen-ai-review/labels.json \
  --balanced --pause 25 \
  --pdf 'LOCAL_POLICY_PDFS/BTech_(Rules_&_Regulations)2013_21nov2023.pdf' \
  --output evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16
```

The same actual PDF and one disposable 114-chunk index served every mode. No live production collection was queried or updated. Groq-only, fallback disabled in the local client. Application source, prompts and labels were unchanged throughout the run; hashes were rechecked afterward. All source files matching the starting application hashes are archived under the run's code_snapshot/ without .env or credentials.

Mode order rotates by question; one repetition per case/mode; answer and HyDE caches disabled. The 25-second deliberate pause is excluded from request latency. Setup/indexing is separately recorded. Exact prompts, code hashes, dependency versions, configuration, model and source hash are in frozen_settings.json and metadata.json. Corpus, mappings, individual cases, successful-call usage and errors are retained. Failed HTTP/retry token usage may not be reported by the provider; it remains unknown, not zero.

## Actual service results

| Mode | Attempts | Accepted | Abstained | Clarification | Raw fallback | Source-completed | Median request seconds | Reported successful-call input+output tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Raw | 10 | 4 | 5 | 1 | 0 | 4 | 0.96 | 9,581 |
| HyDE | 10 | 3 | 6 | 1 | 4 | 3 | 4.68 | 12,044 |
| Fusion | 10 | 3 | 6 | 1 | 4 | 2 | 5.15 | 12,089 |

Provider-unavailable application outcomes: **0**. Accepted application answers: **10/30**, not semantic accuracy. Nine of ten accepted answers received appended exact source qualifications. Raw-model and final-output quality therefore cannot be conflated. All finish/reasoning metadata, quotations and source-completion warnings remain in actual records.

The two out-of-scope cases behave differently: fresh-10 safely abstains in all modes; fresh-09 asks an irrelevant missed-class/exam clarification in all modes rather than explaining that personal live approval records are unavailable. No personal approval was fabricated, but the intended capability response was not delivered.

## Fair retrieval comparison

Per-mode genuine, fully mapped subsets differ in size, so their separate aggregates must not be used directly to declare a winner. Only **3 identical mapped answerable cases** have genuine HyDE results and corresponding Raw results: fresh-02, fresh-03 and fresh-05. First-relevant reciprocal-rank comparisons give **0 HyDE wins, 2 ties, 1 loss**. These are AI-reviewed relevance observations on a tiny sample, not verified benchmark superiority or statistical evidence.

Eight HyDE/Fusion service attempts fell back to Raw and remain visible. Unmapped requirements are not silently counted as clean ranking failures or dropped from the report. Evidence-group recall, first-relevant MRR, pre-merge ranks, post-selection excerpts and all individual scores are recorded. Cosine differences across query embeddings are not interpreted as relevance improvements.

## Separate raw and final quality assessment

Mechanical scoring in metrics.json reports required exact-span inclusion separately for raw model text and final application text. It explicitly leaves semantic accuracy null. It may undercount correct paraphrases and must not be called answer accuracy.

`AI_ANSWER_ASSESSMENT.md` and .json provide a separate, qualitative AI inspection of every raw/final result against the frozen rubric. Human grades remain pending. Important findings:

- fresh-01: every mode abstains despite an answerable documentation/approval question.
- fresh-02: Raw/Fusion contain a correct partial fact but omit overall-credit treatment and alter the quotation; the final answers are withheld.
- fresh-03: Fusion accepts a source-backed general-registration answer that misses the intended return-from-discontinuation rule. The question's “semester break” wording also needs human ambiguity review.
- fresh-04: Raw answers the key failed-student condition and appends source conditions. HyDE/Fusion are withheld after adding text inside a quote. Cross-page evidence mapping is incomplete.
- fresh-05: all raw responses include the device prohibition and Senate exception. Raw/Fusion are nevertheless rejected by brittle same-line quotation/claim-unit processing; HyDE is accepted with extraneous source material.
- fresh-06: Raw is accepted while missing the fee value and change qualification from a second provision; final source completion cannot supply evidence that was not selected.
- fresh-07: Raw/HyDE convey the W/F calculation equivalence. Fusion accepts a quotation ending mid-clause despite finish_reason=stop. Broader completeness is not ensured by token-limit detection.
- fresh-08: all give the correct formula, but final source completion appends distracting GPA-definition passages.
- fresh-09: clarification gate misclassifies the live personal-approval question.
- fresh-10: appropriate safe abstention, with limited practical routing help.

These outputs expose weaknesses that the repeated attendance diagnostic did not. No application fixes or prompt tuning were made against them during execution. Future changes should use these cases as development evidence; they are now revealed and cannot be reused as an untouched final test.

## Metric/runner changes

- `evaluation/ps1/run_diagnostic.py`: accepts an explicit question file, rotates mode order, captures retrieval before merging, archives frozen settings and real corpus, resolves evidence alternatives before querying, and retains raw/final data. Existing three-case invocation remains supported.
- `evaluation/ps1/review_metrics.py` (new): group/alternative-aware retrieval metrics, mapping-completeness flags, paired genuine Raw/HyDE comparison, separate raw/final exact-span coverage, quote/citation observations, source-completion rate, stage/request latency, observed p95 and successful-call usage. Human semantic and abstention grades stay pending.
- `bench/run_benchmark.py`: clarification requests and unknown decisions no longer enter the successful-answer/citation denominator. Existing report fields remain, with a clarification count added.
- `tests/test_frozen_review_metrics.py` (new): alternative groups versus independent requirements, missing mappings, no fabricated correctness from word matching, clarification not counted as an answer.

No src/ or frontend application module, retrieval algorithm, provider configuration, production label or policy PDF was modified in this round.

## Verification

```sh
python -m pytest tests/test_frozen_review_metrics.py tests/test_benchmark.py -q
# 23 passed
python -m pytest tests/ -q
# 422 passed, 6 existing dependency warnings, 10.94s
```

Production integrity: all **237 files present at run start** remained byte-identical; see integrity.json. The earlier 244-file history was already discrepant before this round; do not claim that absent historical files were verified. No institutional approval/publication, credential edit or live re-index occurred.

Frozen application source hashes and label hash were checked again after execution. The original fresh-review sheet and production benchmark labels remain unchanged. No human-reviewed label or score was manufactured.

## Remaining gate and next work

Human review is still needed to confirm relevance/expected-answer labels and grade the outputs. The two incomplete evidence mappings and fresh-03 wording must be adjudicated before an official benchmark. Fixes should next target event/capability understanding, multi-provision/cross-page context selection, same-line quotation claim parsing and question-relevant qualification completion. The accepted mid-clause substring requires an explicit completeness test.

No current result supports a HyDE-superiority claim. The correct final submission story is a reproducible prototype with real measured failures, explicit safeguards and clearly bounded evidence—not a completed reliability proof.

## Artifacts

- [Frozen source review](../evaluation/ps1/frozen-ai-review/REVIEW.md)
- [Execution/scoring protocol](../evaluation/ps1/frozen-ai-review/PROTOCOL.md)
- [Actual results and every raw/final answer](../evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/RESULTS.md)
- [Separate qualitative AI answer assessment](../evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/AI_ANSWER_ASSESSMENT.md)
- [Actual terminal output](../evaluation/ps1/runs/frozen-ten-ai-reviewed-2026-11-16/terminal.md)

Other added artifacts are labels/manifest JSON and Markdown companions under evaluation/ps1/frozen-ai-review/, raw per-attempt records, settings/corpus/mapping/metric JSON and matching code snapshots under the run directory. These are reproducibility records, not additional application features.
