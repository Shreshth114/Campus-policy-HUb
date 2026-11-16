# Interview notes — current evidence

## What is implemented?
A local FastAPI assistant with raw, HyDE and fusion search, explicit source approval, grounded-answer prompts, citation checking, source-version-aware caching, incremental indexing, and chat/trace, comparison, benchmark and source-management dashboard views.

## Why HyDE?
It is a hypothesis for bridging casual questions and formal handbook wording. The generated passage is only an embedding search key; it never enters the answer prompt. It can drift to the wrong topic or miss a second topic. **We have not established that it improves MSRIT retrieval.**

## How are scores interpreted?
Chroma returns cosine distance, converted to clamped similarity using `1 - distance`. Fusion ranks by RRF while retaining a separate cosine score for confidence gating. A top-ranked low-similarity result still abstains. These scores are not calibrated probabilities.

## How are sources trusted?
A human must explicitly approve a source's current content hash. Edited, deleted or rejected files become ineligible. A registry record does not prove official institutional ownership; provenance and current applicability still require review. Decoys/synthetic fixtures are excluded independently of approval flags.

## What does a citation prove?
That its excerpt reference exists in the retrieved set. It does not prove semantic faithfulness. The UI says “Citation references checked” to make that distinction. XML escaping prevents structural delimiter breakout; live-model resistance to every injection is not claimed.

## Why local embeddings and Chroma?
They keep serving infrastructure local and avoid an embedding API dependency after model installation. CPU performance, corpus size and semantic accuracy must be measured on the target machine/data; no embedding latency is claimed here. The embedding model still needs a first download. Chroma supports metadata filters and selective document replacement.

## What happens on updates?
Only changed files are parsed and embedded. A failed preparation retains the previous index/manifest, and a failed commit restores the previous document. Approved old content is not served after its source file changes. Dependent caches are invalidated, and cache lookups also recheck exact source/chunk versions. Unchanged-file tests verify zero new embeddings.

## What does the freshness demo measure?
An edited synthetic marker becoming searchable in a temporary database using deterministic fixture vectors. It verifies indexing mechanics and isolation, not production semantic retrieval speed. It never modifies university PDFs. Read the actual printed measurement from the current run rather than memorizing a latency claim.

## How were thresholds chosen?
They have **not** been tuned. Confidence 0.35, top-k 5 and 12% chunk overlap are starting values. The benchmark has threshold-sweep machinery, but meaningful selection needs reviewed PDFs and verified labels. Semantic answer-cache lookup remains disabled in production.

## What integration evidence exists?
Automated tests exercise adapter request formats, transient/permanent errors, timeouts, failover, endpoints, indexing rollback, cache invalidation, source changes, score boundaries and end-to-end HTTP flows with mocked LLMs. The Node DOM harness tests dashboard behavior; it does not substitute for visual browser QA. Live Groq/Gemini calls have not been verified because keys/models are absent.

## What can be presented as results?
The actual automated test output and the isolated synthetic indexing smoke test. **No real-world retrieval accuracy or measured HyDE improvement is available.** All 25 candidate benchmark labels remain unverified. The benchmark dashboard displays its blocked status instead of fabricated scores.

## What is intentionally deferred?
Rerankers, BM25, multi-HyDE, OCR, a file watcher, MCP and an LLM faithfulness judge. These are unnecessary to complete the current local implementation and would require additional evaluation.

## What changes at scale?
Use coordinated storage/transactions and a server vector database, an ingestion queue, persistent distributed cache and authentication/rate controls. The current locks and limiter apply to one local process. Those alternatives are future architecture, not implemented features.

## Before a real demo

1. Supply actual MSRIT PDFs, inspect extraction/page references and review official origin/applicability.
2. Reindex, explicitly approve the correct current source versions, and inspect the source dashboard.
3. Configure actual provider models/keys and run `check_providers.py --live`.
4. Fill gold chunk IDs and manually verify every label, including out-of-scope expectations.
5. Run the real benchmark and threshold sweeps; report failures as well as successes.
6. Perform visual/browser QA. Use only resulting measured values in the presentation.

## Groq verification update

The adapter has now passed a real, small Groq chat request using a temporary `openai/gpt-oss-120b` override, without Gemini credentials. The saved model setting still needs replacing: it contains a template comment and returns `404 model_not_found`. The smoke test was increased from 32 to 256 tokens after HTTP 200/length-limited reasoning produced no answer at 32. This is adapter evidence, not an MSRIT benchmark or proof that current production generation budgets fit every question. Full automated suite after diagnostics changes: 187 passed.

## First real-ingestion performance investigation

AEC (72 pages / 373 chunks) extracted in 0.398 s and chunked in 0.009 s. The interruption was inside ONNX inference before Chroma insertion, not PDF parsing. The implicit FastEmbed batch of 256 padded texts was a likely memory/compute bottleneck on an 8 GB machine under swap pressure. Explicit batches of 8 now expose progress and bound inference memory while retaining the same model and text. Native Python 3.14 / arm64 runtime probes completed with finite normalized 384-dimensional vectors; no compatibility failure was observed.

Only the decoy had a saved checkpoint/vector set; AEC was pending and uncommitted. Resume is safe for that observed state, without resetting data. Three PDFs produced no text and must be handled as extraction blockers rather than quietly ignored. No sources were approved during diagnosis. The diagnostic probe is throughput/runtime evidence, not a university retrieval benchmark. Full test suite after the changes: 197 passed. Details: `docs/INGESTION_DIAGNOSTIC.md`.


## Multi-institution demonstration

Explain the boundary before showing the model: choose an institution; only its approved current documents can become candidates. Raw, HyDE, fusion and HyDE fallback share the same filter. Confidence uses cosine, while RRF affects ordering only. Answers and cached citations revalidate provenance. The administrator records human review of a specific content hash before publication.

The demonstration dataset was migrated without approving it: ten pending PDFs, seven indexed documents/517 real chunks, three visible extraction failures and four isolated decoy chunks. Show the migration report and synthetic two-institution tests, not invented accuracy. The benchmark remains blocked until actual approved evidence and manually checked labels exist. Single-process local administration is the MVP; enterprise authentication, OCR and distributed processing remain future work.


## UI and live execution evidence

Explain why an unpublished workspace appears only after administrator authentication. Demonstrate Overview → selected published institution → named student chat; Administration has its own workspace selector and Upload → Index → Review → Approve → Publish path. The real dataset still has no approved policy evidence. The disposable verification procedure exercised actual embeddings, Chroma, Groq and citation resolution in all three modes; it is synthetic review-state emulation, not real-world accuracy. The latest suite has 227 passing tests and 19 DOM checks. Visual browser verification still requires BrowserOS neo connectivity.


## Personal-first demonstration

Start without administrator authentication: upload own PDFs, then inspect actual source/page citations. Keep the two trust levels visible. Demonstrate the differentiator in Rule Book and confirmed-fact analysis: the model extracts, exact quote/number/operator/unit checks validate, and Decimal code decides. Show missing facts and a possible conflict rather than choosing a convenient policy winner. Version comparison is a quoted rule-table diff, not a declaration of official policy change. Synthetic fixtures remain explicitly fictional; the existing institutional dataset is unchanged and pending. See PERSONAL_DEMO.md for the click sequence.

Path to Eligibility separates a hypothetical scenario from confirmed facts. Its endpoint revalidates current owned rule IDs and reuses the same Decimal evaluator, then computes gaps and generic percentage-count paths without a model or storage writes. A 75% synthetic requirement with 60/90 completed needs 30 consecutive completed items, or allows five misses out of 50 remaining. Strict inequalities, conflicts, missing inputs and exceptions are handled conservatively. This demonstrates deterministic arithmetic and source traceability, while institutional counting practices and official eligibility still require verification.

2026-11-14: A real page-10 regression exposed generated overlap being concatenated into a duplicate and a split heading number leaking into the preceding section. Fixed through source-span provenance and heading recognition, with full-rule equality tests rather than checking only that the duplicate vanished. Offline candidate count increased because preserving page/section boundaries is more important than minimizing chunk count. The user chose to leave live data untouched; all 239 production data/index hashes matched.

2026-11-14: Correct retrieval did not imply grounded generation. Sentence-window trimming dropped AAC discretion, while old validation checked number presence rather than its condition. Regression-first repair now preserves complete bounded provisions and validates exact sent evidence for fresh and cached responses. Initial regressions: 7 failed/4 passed; final full suite: 353 passed. No live calls or re-indexing. Conservative paraphrase handling can increase abstention; it is not a universal semantic proof.

2026-11-16: Removed deadline-driven scripted answer and document-comparison paths. The important lesson is that retrieval success, answer grounding and provider availability are separate. Current deterministic checks are conservative enough to reject some correct paraphrases; rule extraction also mishandles completion after failure and misses certain comparison phrases. The project has substantial tested infrastructure, but full live-model reliability and held-out HyDE gains remain unproved. Present actual source-backed capabilities and limitations, not scripted output as measured retrieval.

2026-11-16 reliability round: Baseline 387 passes; nine new regressions bring full suite to 396. Correct percentages can still be an incomplete answer: citation normalization must not accept missing AAC discretion. Finish metadata is necessary to distinguish reasoning-budget exhaustion from a hallucination or retrieval miss. Conservative local pacing can itself cause unavailability within bounded wait budgets; the isolated evaluation must pace calls explicitly. No claim of reliable answer coverage follows from passing unit tests.

2026-11-16 completion round: Full-source quotation selection plus bounded output budgeting and narrowly guarded source-condition supplementation improved repeated diagnostic application acceptance from 0/9 to 8/9. Model-generated content and appended exact source conditions remain distinguishable; the system never repairs invented claims, bad quotes or truncation. One quote mismatch still abstains. Three Raw fallbacks prevent claiming HyDE wins. 408 automated passes are regression evidence; human-verified held-out accuracy remains outstanding.

2026-11-16: The fresh ten-question exploratory run is harder than the repaired attendance diagnostic. Thirty real attempts yield ten application acceptances, including wrong-scope/incomplete answers; nine accepted outputs were supplemented from sources. Eight HyDE/Fusion fallbacks leave only three mapped genuine Raw/HyDE pairs (0 wins, 2 ties, 1 loss). Real source citations do not guarantee relevance or complete answers. AI-assisted review remains explicitly separate from human-verified benchmark labels and final grading. Full raw/final records are retained.

## 2026-11-16 — How do answers generalize beyond one PDF?

The application contains no prepared NIT Goa answers. It selects complete labelled source units, checks literal evidence/citations/qualifications and renders each with its own citation. A separate model review checks the actual question and every requested part; it is not an infallible semantic validator. Tests vary policy numbering, topics, values, authorities and wording in isolated synthetic fixtures. Real Groq checks answered full medical condonation and reinstatement provisions after fixes; a late-fee question still missed the needed evidence and abstained. These are development observations, not benchmark accuracy. Human-reviewed independent multi-document evaluation and a fair Raw/HyDE/Fusion comparison remain necessary. Production data was unchanged. Full evidence: docs/GENERAL_ANSWER_GROUNDING.md.

## 2026-11-16 — What did tracing change?

The apparent late-fee retrieval failure conflated semester late payment with summer-course registration. The original summer question had both provisions at rank 1; context trimming removed one. This is why we trace source availability, ranking and context separately before altering retrieval.

Coverage now requires explicit per-question-span statuses and selected-source mappings. It still relies on a fallible reviewer: a new development call treated a request for exemption as an asserted claim and omitted two coverage rows, so it was withheld. Human adjudication and new-document evaluation remain pending. Twelve calibration candidates are prepared with zero human labels. Freeze/drift and scoring tools are tested, but no new held-out benchmark has run and no HyDE advantage is claimed. Final suite: 476 pass. Live integrity changed during concurrent demo use; report the actual differences instead of claiming all production files unchanged. See docs/RELIABILITY_REFINEMENTS.md.
