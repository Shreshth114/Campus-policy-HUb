# Unseen-document evaluation design

Nothing in this document is a completed test or a human-approved label. The NIT Goa PDF, historical MSRIT material, repeated diagnostic questions and current 12-case packet are development material.

Target a manageable initial cohort of six previously unexposed official PDFs from at least three institutions, with 30 human-reviewed questions (five per PDF). This is a proposed sample size, not evidence of statistical power or accuracy. Use two single-provision, two multi-provision and one absent/ambiguous/live-record case per document where those categories are supported. Do not force a question type unsupported by a source.

| Layout/source condition | Evaluation requirement | Expected handling |
| --- | --- | --- |
| Ordinary numbered regulations | Amount/condition/authority wording and paraphrases | Complete exact evidence or safe abstention |
| Multi-page provision | Continuation and all qualifications, both page mappings | Check extraction and context separately; incomplete continuation must not grant permission |
| Tables | Row/column association, units, headers and footnotes | Correct cell meaning, not just a matching number; unsupported layout must abstain |
| Scanned/image-only PDF | Detect extraction availability and prevent invented evidence | Current system has no OCR; expected extraction failure/abstention, not retrieval success |
| Amendment/version pair | Effective date, scope, changed rule and superseded text | Human source applicability decisions; no automatic institutional approval |
| Multiple provisions/documents | Conditions, process, deadlines and fees in different locations | Per-requirement source coverage, correct institution and source citations |

Balance institutions across layouts so one institution does not stand for all difficult documents. Include identical question wording across institutions with different provisions, identical filenames, numerical distractors, plausible exceptions and unavailable live personal status. Use isolated institution/workspace copies; never expose one institution's evidence to another. Authenticity, URL, authority and dates must be recorded only when evidenced.

Human source review and labels must precede model runs. Annotators may inspect sources; implementers must not tune code/prompts after seeing held-out outputs. Exact document/question hashes can identify some reuse; humans must attest absence of paraphrase/near-duplicate leakage. If a failure is used to improve code, retire that case/document from untouched evaluation and retain it as a development regression.

Report extraction success on all documents. Report retrieval quality only where extraction and target mapping are available, while retaining extraction failures in end-to-end service/abstention reporting. Tables/scans are not silently excluded to inflate retrieval scores. A zero-extraction scanned PDF cannot demonstrate successful retrieval.
