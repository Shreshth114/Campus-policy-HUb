# Why the attendance attempts failed — exact trace inspection

## NO_POLICY_FOUND: retrieval and sent context were different

In the paced ps1-14 Raw and Fusion records, the answer prompt's C1 contains only `B11. Attendance`. B11.4 is present in the retrieved block, but not in the actual prompt. The earlier suggestion that the model refused despite receiving the complete B11.4 provision was incorrect for these attempts.

`answer.trim_chunk_span` treats B11. as a numbered provision boundary as well as B11.1 etc. It selects a candidate using exact query-word overlap. The informal original question shares few terms with the formal rule; tied candidates choose the first, which here is the section heading. The retrieval intent annotation does not reach this selector: pipeline passes the original question for answer construction. Thus retrieval gets page 10 while context construction discards its content. With irrelevant C2/C3 evidence also present, NO_POLICY_FOUND is a reasonable model response. This is a confirmed context-selection defect, not proof of model refusal with complete source evidence.

## Supported thresholds: a combined rejection reason hides distinct failures

For ps1-02 Raw, C1 does contain full B11.4. The generated opening sentence correctly names the percentages but has no citation attached; only the following quotation has [C1]. It also says “eligible for medical condonation”, stronger than the source's “considered”. The answer omits recommendations/submission, AAC discretion, the two-semester limit and endorsed-certificate/deadline conditions. `claim_failures` returns uncited_claim and omitted_qualification. The pipeline groups these under unsupported_cited_claim; that label does not mean 80/75 themselves are absent from the source.

For ps1-21 Fusion, citation canonicalization succeeds, but the paraphrase validator rejects the compound sentence. It uses clause-token containment and very limited vocabulary normalization, so it can reject faithful paraphrases. This is a validator false-negative risk. Independently, that answer still omits AAC discretion, IMO endorsement and the concession limit, so it would not satisfy the requested full-qualified answer contract even with better paraphrase handling.

The offline diagnostic display for ps1-21 Fusion initially applied claim_failures to the raw Unicode citation rather than the canonicalized answer, incorrectly displaying uncited_claim. Recomputed diagnostic failures now use canonicalized citations, while retaining the provider's raw output unchanged. Application result/reason was not altered. This corrects report instrumentation, not model behavior.

## Proposed next fixes (not implemented in this explanation)

- Distinguish section headings from substantive provisions; never select a heading-only excerpt as policy evidence.
- Use the understood event for provision selection as well as retrieval, preserving full clauses and qualifications.
- Report uncited statements, missing qualifications and unsupported conditions separately in the UI.
- Improve structured condition/value attribution and supported paraphrase handling, retaining rejection of invented rules and incomplete eligibility claims.

No LLM calls, indexing, embeddings or application-code changes were made for this explanation. Sources: actual prompts/raw outputs in evaluation/ps1/runs/reliability-paced-2026-11-16/ps1-02-raw.json, ps1-14-raw.json, ps1-14-fusion.json and ps1-21-fusion.json; src/answer.py and src/evidence.py.
