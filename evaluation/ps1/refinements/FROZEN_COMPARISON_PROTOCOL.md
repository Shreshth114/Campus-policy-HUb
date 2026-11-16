# Freeze and fair Raw/HyDE/Fusion comparison

## Freeze gate

Do not freeze the current calibration packet as held-out evaluation. `FREEZE_STATUS.md` lists its blockers. Human source adjudication, multiple new institutions/PDFs and exposure attestation are missing.

After development fixes and regression checks pass, prepare a new specification and genuinely adjudicated annotations. Freeze:

- Source-PDF hashes, extraction outcomes, public document/institution identifiers and applicability/version decisions.
- Questions, supporting provisions, alternative relevant chunks, required qualifications, acceptable abstention/clarification and human provenance.
- Code, prompts, Python/package versions, embedding model, configured Groq model, top-k, cosine threshold, chunk/evidence/output budgets, caches, retry/rate-limit policy and fallback policy.
- Exact query/mode order, pause/warm-up policy, repetition count and scoring definitions. Provider responses may remain nondeterministic; report that limitation.

The freeze helper hashes current source and evaluation-tool code, documents, labels, cases and settings, and refuses pending human labels, exact known document/question reuse, model/settings drift and overwrites. It cannot authenticate humans or detect all paraphrase leakage. It never approves institutional sources. Store outputs under evaluation directories, not production storage.

```sh
python -m evaluation.ps1.refinements.freeze_manifest \
  --spec evaluation/ps1/NEW_HELDOUT_SPEC.json \
  --output evaluation/ps1/NEW_FROZEN_MANIFEST.json

python -m evaluation.ps1.refinements.freeze_manifest \
  --spec evaluation/ps1/NEW_HELDOUT_SPEC.json \
  --verify evaluation/ps1/NEW_FROZEN_MANIFEST.json
```

These are future input filenames, not existing approved evaluation files. The helper and drift/overwrite guards are tested on synthetic temporary inputs. The current `freeze_spec.NOT_READY.json` is a deliberately blocked example, not permission to edit exposure/human flags until they are true.

The diagnostic runner's settings capture is useful but is not a replacement for this gate. A final benchmark execution wrapper must invoke preflight verification immediately before execution and preserve the frozen cases/mode schedule. Wiring that reviewed dataset into execution is pending the new human-reviewed inputs; no held-out run has started.

## Comparison procedure

1. Build disposable, institution-scoped indexes from identical frozen source copies. Record the corpus/metadata hash and map complete required provisions to alternatives before asking questions. Do not touch production indexes or approve/publish sources.
2. Use the same questions, evidence budget, confidence gate, selection/review prompts/model and validators in Raw, HyDE and Fusion. Preserve the current meaning of Raw: dispatch applies the shared event cue transformation in `src/query_intent.search_question`. Record the exact embedding input/HyDE text and actual retrieval provenance.
3. Disable answer and HyDE caches for the primary cold comparison. Use declared balanced mode order. Separate model warm-up/index creation from request latency. Evaluate warm caches and concurrency separately, with scope/source-version validation unchanged.
4. Record requested mode and actual execution path. A HyDE failure followed by Raw is a service fallback, not a genuine HyDE observation. Fusion with a failed HyDE arm is a degraded Raw-only lane; do not count Raw twice in RRF. Preserve failed calls and retry costs.
5. Score retrieval before merge, after merge, after provision selection and in the final prompt. Use per-requirement evidence recall/complete-question coverage and relevance rank metrics; show unmapped targets instead of dropping them. Use cosine for the confidence gate and RRF only for ranking.
6. Score raw source selection separately from final application answer. Raw model output is now structured IDs; assess its selected literal provisions, not JSON token overlap with an answer. Keep deterministic rejection, review rejection, clarification, true/false abstention and provider/extraction errors separate. An accepted answer is not automatically correct.
7. Have humans grade final answers, scope, every number/meaning, qualifications and citations independently. Evaluate the second call's false approvals/rejections against those human decisions. Report final source completion separately; automatic condition supplementation remains disabled.
8. Report per-mode all-attempt service outcomes and a genuine-success paired subset on identical questions. Do not silently discard fallback/provider/error cases from the service denominator. Report subset size, exclusions, per-document results and uncertainty. Fallbacks cannot be used as evidence for or against HyDE quality.
9. Measure total request and stage wall latency, generation/review provider latency, successful and failed-call usage availability, input/output/reasoning tokens and cold/warm state. Report observed medians and tails with sample size. No currency estimate without declared prices. Do not double-count reasoning tokens.
10. Preserve all raw traces and rejected outputs. Hash-check production files before/after. Publish findings with limitations, not an assumed HyDE advantage. A small mixed result does not establish superiority; predeclare comparisons and uncertainty analysis before outputs are opened.

## Pass criteria before claiming completion

- Full Python and frontend regressions pass; no institution/workspace/citation leakage; protected production snapshot unchanged.
- Source applicability reviewed; all required evidence mappings resolved or explicitly marked unscorable.
- Every held-out question has genuine final human adjudication; scanned/layout failures have a separate declared outcome.
- Manifest verification passes before execution, and code/prompts/labels remain unchanged during the run.
- All planned attempts are accounted for, including errors/fallbacks; raw selections and final answers scored separately.
- Review false approvals/rejections, abstention errors, latency and token costs reported with denominators and uncertainty.

If any gate fails, report the evaluation as incomplete. Do not change thresholds, source labels or expected answers to improve the score mid-run.
