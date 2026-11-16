# Dell PS1 evaluation — first review package

Prepared 16 November 2026. This package starts the evaluation; it contains no measured retrieval scores and no human-verified labels.

- `REVIEW.md`: 30 questions, exact PDF quotations and proposed target IDs for human review.
- `questions.draft.json`: corresponding structured draft, with every label unverified.
- `manifest.json`: source hash, question-set hash, actual provider/model identifiers, embedding model, top-k and HyDE prompt hash. No credentials or workspace capabilities.
- `check_draft.py`: offline consistency check. Run `python evaluation/ps1/check_draft.py` from the project root.

## Review status

12 proposed development cases and 18 proposed holdout cases; the deterministic split was assigned before scoring. No prompt tuning or new retrieval observations were performed in this round. Assistant-authored questions are not independent human questions, and the same PDF appears in both subsets: this tests held-out questions, not generalization to unseen institutions or documents.

22 answerable questions have an entire source quotation contained in a reconstructed target chunk. Three multi-condition cases (`ps1-22`, `ps1-24`, `ps1-25`) match fragments across multiple chunks. Their proposed targets require review for completeness. Quotes were extracted from physical PDF pages, never generated as policy text. The source file hash matches the personal registry and reconstruction produced the registry's 114 chunks. No live Chroma collection was opened; reconstruction is not verification that every target ID currently exists in the database.

The five out-of-scope labels are proposals about unavailable personal/live operational information. Their absence must be reviewed, not inferred solely from lack of a quotation.

For each entry in REVIEW.md, record accept/edit/reject and any corrected page, source span, target ID or expected behavior. Preserve every material condition in expected answers. No script in this package promotes drafts to verified labels or writes to the production workspace.

## Next execution checkpoint

After human review: freeze the accepted labels/configuration, check current target IDs in a disposable copy of the index, then run Raw versus current HyDE with identical top-k and cache policy. Use isolated outputs; keep provider failures and fallbacks separate. Score complete evidence coverage for multi-condition questions, not merely retrieval of one relevant chunk. Run answer generation separately and retain proposed answers for human factual review. Retrieve-only scores cannot establish answer reliability.

Use the existing benchmark functions after labels and scope are validated. Do not invoke its live-workspace CLI merely to bypass the review checkpoint; it persists results and HyDE cache and may invoke providers. A disposable runner must redirect all storage first. Historical ablation results are not results for this new question set.

## Reliability baseline

The targeted regression suite checks answer grounding, benchmark arithmetic, workspace isolation and removal of scripted paths with isolated fixtures and mocks. It does not measure live model accuracy. Outstanding issues documented in `docs/PROTOTYPE_REALITY_CHECK.md`—strict paraphrase rejection, operator parsing and incomplete extraction checkpoints—still need repair before a final answer-quality claim. They were not silently changed while constructing this dataset.
