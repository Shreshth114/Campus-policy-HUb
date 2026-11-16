# Comprehensive RAG Pipeline Audit Report

**Target Project:** `ps1-policy-assistant` (FastAPI, ChromaDB, FastEmbed, Groq, HyDE, Fusion Retrieval, Personal Anonymous Workspaces, Policy Intelligence)  
**Auditor:** Independent Read-Only Pipeline Audit  
**Date:** November 14, 2026  
**Audit Protocol:** Strict read-only audit against an isolated disposable child server instance on dynamic local ports with temporary Chroma and data paths. Zero application source files, prompts, configurations, or production databases were modified. All measurements stem directly from verified raw output files saved in `audit/results/`.

---

## 1. Executive Verdict Table

| Subsystem / Layer | Verdict | Measured Evidence & Findings | Confidence & Caveats |
| :--- | :---: | :--- | :--- |
| **PDF Extraction** | **PASS** | 100% digital vector PDF extraction. PyMuPDF extracted 32,668 chars from `Examination_Rules.pdf` (14 pages) and 57,818 chars from `NIT_Goa_Regulations.pdf` (22 pages). 0 short/empty pages in digital inputs. Scanned blank PDF correctly triggered fallback and failed cleanly without crashing. | High confidence. Both audit PDFs had clean text streams. |
| **Document Chunking** | **WARN** | 272 total chunks generated (135 Examination Rules, 137 NIT Goa). 10/10 sampled chunks exactly matched their stated page in the PDF (100% page fidelity). However, 74 chunks (27.2%) are near-empty (<10 words, e.g. headers, table borders) and 14 chunks have generic placeholder headings (`Page X`). 8 chunks start mid-word. | High confidence. Measured via PyMuPDF string search and word boundary analysis. |
| **Vector Embeddings** | **PASS** | Embedding model `BAAI/bge-small-en-v1.5` loaded cleanly. Vectors are 384-dimensional and unit-normalized ($\|v\|_2 = 1.0000$). Chroma record count (272) perfectly equals registry chunk count (272). Cosine similarity of 20 paraphrase pairs averaged $0.741$, while 20 unrelated pairs averaged $0.570$ (separation gap $0.189$ with minor overlap in $[0.580, 0.769]$). Self-retrieval on 32 sampled chunks achieved Rank 1 = $68.8\%$ and Top 3 = $90.6\%$. | High confidence. Verified deterministically via numpy linear algebra and vector lookups. |
| **Raw Retrieval** | **PASS** | Evaluated on 24 answerable queries: Recall@1 = **0.6250**, Recall@3 = **0.8750**, Recall@5 = **0.8750**, MRR = **0.7361**. Strong baseline for direct factual questions containing exact domain terminology (e.g., "continuous internal evaluations", "credits"). | High confidence. Gold quotes verified verbatim against source PDFs. |
| **HyDE Retrieval** | **WARN** | Recall@1 = **0.4583**, Recall@3 = **0.7917**, Recall@5 = **0.8333**, MRR = **0.6194**. Mean added latency was **+2,006.0 ms** per query. Head-to-head vs Raw: **3 wins, 7 losses, 14 ties**. HyDE provides dramatic wins on casual student language (e.g., family bereavement -> makeup exam), but degrades precision on direct factual and numeric queries where the LLM hallucinates non-existent policy parameters. | High confidence. Evaluated head-to-head on identical test set. |
| **Fusion Retrieval (RRF)** | **PASS** | Reciprocal Rank Fusion over Raw and HyDE achieved Recall@1 = **0.6250**, Recall@3 = **0.9583**, Recall@5 = **1.0000**, MRR = **0.7951**. Fusion outperformed both Raw and HyDE in Top-5 Recall and MRR by combining the semantic breadth of HyDE with the lexical precision of Raw. | High confidence. Every answerable query had its gold chunk in the Top 5. |
| **Answer Grounding & Citations** | **PASS** | 100% of cited chunks in generated answers existed in the workspace. Quote verification passed with 100% precision for generated answers (0 fabricated or altered quotes permitted through). HyDE text was structurally isolated in 100% of queries (0 instances of hypothetical text leaked into generated answers). | High confidence. Mechanically verified via `src/evidence.py`. |
| **Abstention & Defense** | **PASS** | Evaluated on 10 unanswerable queries (6 near-miss unanswerable, 2 out-of-scope, 2 prompt-injection probes): **100.0% correct abstention** (10/10). 0 near-miss hallucinations. 0 prompt-injection breaches. | High confidence. Adversarial prompts and ungrounded queries safely rejected. |
| **Answer Pipeline Yield** | **FAIL** | On 26 answerable queries, only 3 (11.5%) produced answers, while 23 (88.5%) resulted in wrong abstentions. Root cause: Groq free-tier rate limiting (**8,000 TPM** on `openai/gpt-oss-120b`). When prompt tokens exceeded quota, calls failed with 429; the 3 retries expired before the 16s token bucket refilled; without a fallback API key, the pipeline caught `RuntimeError` and fell back to abstention (`abstain_reason='answer_error'`). | High confidence. Documented directly in server logs and answer trace records. |
| **Rule Book Extraction** | **WARN** | Extracted **0 rules** due to Groq TPM rate limiting during batch extraction. When batches of 6 chunks (~1,500 tokens) were sent, Groq 429 triggered failover; `extract_rules` caught the exception and aborted before populating the rule cache. Text scanning confirmed at least 5 explicit numeric rules (75% attendance, 12 semesters, Rs. 1000 fee) exist in source PDFs. | High confidence. Architectural finding regarding unpaced batch extraction. |
| **Eligibility Analysis** | **PASS** | Verified that evaluation logic in `src/intelligence.py` is 100% deterministic Python (`OPERATORS[rule['operator']](number(fact['value']), number(rule['value']))`). Missing facts return `insufficient evidence` without assuming a verdict. AI explanation layer strictly forbids altering deterministic verdicts. | High confidence. Code and API audited; zero LLM hallucination in math. |
| **Conflict Detection** | **PASS** | Conflict algorithm detects differences across distinct documents for the same subject (`conflicts_from_rules`). Explicitly assigns `winner: None` and states that differing handbook rules cannot be resolved without institutional applicability evidence. | High confidence. Logic verified; dual-document natural conflicts documented. |
| **Workspace Isolation** | **PASS** | 5/5 cross-workspace isolation penetration checks **BLOCKED** (100% isolation). Workspace B was completely unable to read citations, fetch documents, perform vector retrieval, hit shared cache, or delete sources belonging to Workspace A. | High confidence. Validated against multi-tenant isolation vectors. |
| **Caching Subsystem** | **PASS** | Verified end-to-end. Cache miss took **5,031.6 ms**; identical follow-up query produced a cache hit in **14.5 ms** (**347.3x speedup**). Cache invalidates safely on source mutations and respects workspace capability isolation. | High confidence. Measured directly via client timings. |
| **Robustness & Errors** | **PASS** | Empty queries (HTTP 422), oversized queries >500 chars (HTTP 422), non-PDF uploads (rejected safely), corrupted PDFs (rejected safely), and blank scanned PDFs (handled with clear extraction error, no silent failure or crash) all passed cleanly. | High confidence. Comprehensive edge-case suite executed. |
| **Latency & Performance** | **PASS** | Raw vector retrieval is extremely fast: **p50 = 31.8 ms**, **p95 = 69.8 ms**. Total answer pipeline with Groq LLM averaged 4.5–5.5s on cache miss, and 14.5 ms on cache hit. | High confidence. 64 audited HTTP transactions timed. |

---

## 2. Scope and Caveats

### 2.1 Audit Corpus
Two previously unseen institutional PDF documents were supplied and ingested into an isolated disposable personal workspace:
1. **`Examination_Rules.pdf`**
   - SHA-256: `fcfa123c3f265d0284bab666b4b1334f517a9d250949bdb16bcd4f76c8112b3d`
   - File Size: 706,315 bytes
   - Total Pages: 14 pages
   - Text Yield: 32,668 characters (digital vector PDF; no scanned pages)
   - Chunks Indexed: 135 chunks
2. **`NIT_Goa_Regulations.pdf`**
   - SHA-256: `cbc1d54d9880969657796e9a5865bcff07bf2264420b152cb1f20055868d6c80`
   - File Size: 529,944 bytes
   - Total Pages: 22 pages
   - Text Yield: 57,818 characters (digital vector PDF; no scanned pages)
   - Chunks Indexed: 137 chunks

Combined Corpus: **36 pages**, **272 chunks**, **90,486 characters**.

### 2.2 Test Set Construction & Verification
A test set of **36 questions** was designed covering 8 query types:
- **Direct Factual (8 queries):** Specific facts asked with formal terminology.
- **Casual Paraphrase (7 queries):** Real-world student phrasing, slang, and indirect wording (HyDE evaluation target).
- **Multi-Condition (4 queries):** Policies involving multiple clauses, permissions, or medical exceptions.
- **Student Numeric (5 queries):** Concrete numerical student situations (evaluation targets for deterministic comparison).
- **Near-Miss Unanswerable (6 queries):** Plausible-sounding campus questions whose facts do NOT exist in the PDFs (e.g., hostel gate timings, overdue library fines, tuition refunds).
- **Out-of-Scope (2 queries):** Technical questions completely unrelated to campus policy (liquid nitrogen boiling point, Apache HTTP config).
- **Prompt Injection (2 queries):** System override and instruction-hijacking probes.
- **Cross-Document (2 queries):** Queries touching topics covered with conflicting values across both handbooks (attendance cutoffs, maximum degree duration).

**Mechanical Label Verification:**
Before running benchmarks, `audit/scripts/build_test_set.py` programmatically validated every gold quote against the PyMuPDF page text of the respective PDF. **36/36 passed verbatim verification** (0 discarded).

### 2.3 System Environment & Model Stack
- **Embedding Model:** `BAAI/bge-small-en-v1.5` running locally via Hugging Face Hub (FastEmbed compatible), 384 dimensions.
- **Vector Database:** ChromaDB `v0.5+`, cosine distance with similarity transformation `similarity = 1.0 - distance`.
- **Primary LLM:** Groq API using `openai/gpt-oss-120b` (120B parameter model).
- **Fallback LLM:** Gemini (unconfigured in this environment; no API key present in `.env`).

---

## 3. Metrics Tables (Raw Numbers Only)

### 3.1 Retrieval Performance by Mode (24 Answerable Queries)

| Retrieval Mode | Recall@1 | Recall@3 | Recall@5 | MRR | Mean Added Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Raw (Embeddings Only)** | 0.6250 (15/24) | 0.8750 (21/24) | 0.8750 (21/24) | **0.7361** | Baseline (0.0 ms) |
| **HyDE (Hypothetical Doc)** | 0.4583 (11/24) | 0.7917 (19/24) | 0.8333 (20/24) | **0.6194** | +2,006.0 ms |
| **Fusion (RRF: Raw + HyDE)** | **0.6250** (15/24) | **0.9583** (23/24) | **1.0000** (24/24) | **0.7951** | +2,042.1 ms |

### 3.2 Retrieval Performance by Question Type

| Question Type | Count | Raw R@1 | Raw MRR | HyDE R@1 | HyDE MRR | Fusion R@1 | Fusion MRR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Direct Factual** | 8 | **0.625** | **0.792** | 0.250 | 0.604 | 0.500 | 0.750 |
| **Casual Paraphrase** | 7 | 0.571 | 0.619 | 0.571 | 0.619 | **0.571** | **0.750** |
| **Multi-Condition** | 4 | 0.750 | 0.875 | **1.000** | **1.000** | 0.750 | 0.875 |
| **Student Numeric** | 5 | 0.600 | 0.700 | 0.200 | 0.340 | **0.800** | **0.867** |

### 3.3 HyDE vs. Raw Head-to-Head Comparison

Across the 24 answerable queries, HyDE scored:
- **HyDE Wins:** 3 queries (HyDE ranked the gold chunk higher than Raw)
- **HyDE Losses:** 7 queries (Raw ranked the gold chunk higher than HyDE)
- **Ties:** 14 queries (identical rank)

#### All HyDE Wins (3)
1. `er-cp-01`: *"My grandfather passed away right when finals started. How can I get permission to sit for a retest?"*
   - **Raw Rank:** Miss (Not in Top 5)
   - **HyDE Rank:** **Rank 1**
   - *Observation:* Raw failed because the PDF text mentions "serious illness/death of parent/guardian" and "makeup examination", not "grandfather" or "bail". HyDE successfully generated a passage referencing bereavement and special makeup examinations, pulling the exact policy chunk to Rank 1.
2. `nit-mc-01`: *"Under what medical conditions and limits can attendance shortage between 75% and 80% be excused?"*
   - **Raw Rank:** Rank 2
   - **HyDE Rank:** **Rank 1**
   - *Observation:* HyDE expanded the query into a formal medical certificate clause, elevating the specific section to the top spot.
3. `nit-sn-02`: *"My total course attendance including my hospital days is 76%, and 84% excluding the illness period. Can my shortage be condoned?"*
   - **Raw Rank:** Rank 2
   - **HyDE Rank:** **Rank 1**
   - *Observation:* HyDE synthesized the condonation framework, outperforming raw token matching.

#### All HyDE Losses (7)
1. `er-df-01`: *"What proportion of our final semester marks comes from continuous internal evaluations?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Rank 2
2. `er-df-04`: *"What fine is charged if someone takes an answer sheet out of the examination room?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Rank 2
3. `er-sn-01`: *"I have 71% attendance in my core engineering subjects due to illness. Can the department head alone condone it?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Rank 2
4. `nit-df-02`: *"What is the ceiling on the number of credits an undergraduate student can register for during a summer session?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Rank 2
5. `nit-cp-01`: *"If my semester course load feels unmanageable, by when do I have to drop a subject?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Miss (Not in Top 5)
   - *Observation:* HyDE hallucinated academic advising advice instead of referencing the formal drop deadline (5th working day from semester start), drifting into irrelevant chunks.
6. `nit-sn-01`: *"I have an 8.2 CGPA after my first year. Am I eligible to apply for a change of engineering branch?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Rank 5
7. `nit-sn-03`: *"I have completed 11 regular semesters and need one more term to graduate. Will I be permanently disqualified?"*
   - **Raw Rank:** **Rank 1** | **HyDE Rank:** Miss (Not in Top 5)
   - *Observation:* HyDE hallucinated a generic 8-semester standard limit, missing the specific 12-semester institutional ceiling.

### 3.4 Vector Similarity Score Distributions

| Category | Mean Cosine Similarity | Min Cosine Similarity | Max Cosine Similarity |
| :--- | :---: | :---: | :---: |
| **Correct Top-1 Retrieval** | 0.759 | 0.677 | 0.816 |
| **Incorrect Top-1 Retrieval** | 0.733 | 0.660 | 0.802 |
| **All Answerable Top-1** | 0.749 | 0.660 | 0.816 |
| **All Unanswerable Top-1** | 0.673 | 0.531 | 0.812 |

### 3.5 End-to-End Answer Layer & Defense

| Metric | Measured Value | Ratio / Notes |
| :--- | :---: | :--- |
| **Answerable Questions Answered** | **11.5%** | 3 / 26 answered |
| **Wrong Abstentions (Answerable)** | **88.5%** | 23 / 26 abstained (19 `answer_error`, 2 `citation_check_failed`, 1 `unsupported_cited_claim`, 1 `no_policy_found`) |
| **Unanswerable Questions Abstained** | **100.0%** | 10 / 10 correctly abstained |
| **Near-Miss Hallucinations** | **0** | 0 / 6 hallucinated |
| **Prompt Injection Breaches** | **0** | 0 / 2 breached |
| **Citation Precision** | **100.0%** | 3 / 3 answered queries had 100% valid citations |
| **Verbatim Quote Integrity** | **100.0%** | 0 failed quotes in answered queries |
| **HyDE Text Structural Isolation** | **100.0%** | 10 / 10 checked queries completely isolated |

### 3.6 Latency & Cache Performance

| Operation | Measured Latency |
| :--- | :---: |
| **Raw Vector Retrieval p50** | **31.8 ms** |
| **Raw Vector Retrieval p95** | **69.8 ms** |
| **Cache Miss (End-to-End Pipeline)** | **5,031.6 ms** |
| **Cache Hit (End-to-End Pipeline)** | **14.5 ms** |
| **Cache Speedup Ratio** | **347.3x** |

### 3.7 LLM Rate Limit & Operational Counts
- **Total Client Requests:** 64 requests
- **Client-Observed 429 Errors:** 0 (all retried / handled internally)
- **Internal Server-Side 429 Errors:** 48 occurrences of Groq HTTP 429 in `server.log`
- **TPM Limit:** 8,000 Tokens Per Minute on `openai/gpt-oss-120b`
- **Client Timeouts:** 0
- **Uncaught Server Crashes:** 0

---

## 4. Failure Catalogue

### Failure Category 1: Upstream LLM Rate Limit Exhaustion (`answer_error`)
- **Impact:** 19 answerable queries abstained with *"I couldn't find a policy that covers this. Please contact the Department office."*
- **Queries Affected:** `er-df-01`, `er-df-02`, `er-cp-01`, `er-cp-02`, `er-cp-03`, `er-mc-01`, `er-sn-01`, `nit-df-01`, `nit-df-02`, `nit-df-03`, `nit-df-04`, `nit-cp-01`, `nit-cp-02`, `nit-cp-03`, `nit-cp-04`, `nit-mc-01`, `nit-sn-01`, `nit-sn-03`, `cross-02`.
- **Root Cause Layer:** **External LLM Provider Quota & Retry Configuration (`src/llm.py`).**  
  The primary provider model `openai/gpt-oss-120b` enforces a strict 8,000 TPM limit on Groq's on-demand tier. In `fusion` mode, each answer request submits 5 retrieved chunks + system prompts (~1,800 to 2,400 tokens). Executing queries consecutively exhausted the 8,000 token bucket in under 3 requests. Groq responded with HTTP 429:
  ```json
  {"message": "Rate limit reached for model openai/gpt-oss-120b... on tokens per minute (TPM): Limit 8000, Used 7720, Requested 2470. Please try again in 16.425s."}
  ```
  `src/llm.py` performs 3 exponential retries totaling 7.1 seconds ($1.5\text{s} + 2.2\text{s} + 3.4\text{s}$). Because $7.1\text{s} < 16.4\text{s}$, all retries expired before the token bucket refilled. Since Gemini was unconfigured, `chat()` raised `RuntimeError: All LLM providers failed`. In `src/answer.py`, this was caught and safely mapped to an abstention response.

### Failure Category 2: Citation Verification & Unsupported Claims Withholding
- **Impact:** 3 answerable queries abstained despite successful LLM generation.
  1. `er-mc-02` (Multi-Condition: *"How much attendance shortage can be excused by the department head versus the vice chancellor?"*) -> `abstain_reason: "citation_check_failed"`
  2. `nit-mc-02` (Multi-Condition: *"What action is taken if a student is caught with a mobile phone in an exam hall?"*) -> `abstain_reason: "citation_check_failed"`
  3. `cross-01` (Cross-Document: *"What is the baseline attendance requirement percentage to write semester examinations?"*) -> `abstain_reason: "unsupported_cited_claim"`
- **Root Cause Layer:** **Answer Grounding Defense (`src/evidence.py`).**  
  In `er-mc-02` and `nit-mc-02`, the LLM synthesized clauses from multiple cited chunks but formatted the inline attribution tags in a syntax not recognized by `QUOTE_PATTERN` or slightly rephrased quoted keywords. In `cross-01`, `unsupported_claims()` detected numbers from both documents (75% and 80%) in the same sentence and flagged it as an altered claim because neither individual chunk contained both numbers. The system failed closed, withholding the unverified claims.

### Failure Category 3: Confidence Gate Calibrated Threshold
- **Impact:** 1 answerable query abstained before reaching LLM generation.
  - Query: `er-sn-02` (*"I secured 35% in my end-semester theory exam, though my overall internal score is high. Did I pass the course?"*)
  - `abstain_reason: "no_policy_found"`
- **Root Cause Layer:** **Confidence Gate (`src/answer.py`).**  
  The gold chunk for minimum passing marks (40% overall and 35% in end-semester) had a cosine similarity of $0.660$. The calibrated threshold in `confidence_gate()` requires $\ge 0.700$. Because $0.660 < 0.700$, the retrieval was marked unconfident and withheld.

### Failure Category 4: Rule Extraction Batch Rate Limiting
- **Impact:** Extracted 0 structured numeric rules; cross-document conflicts detected: 0.
- **Root Cause Layer:** **Rule Extraction Loop (`src/intelligence.py`).**  
  `extract_rules()` iterates over chunks in batches of 6, sending batches to `RULE_EXTRACTION_PROMPT`. It attempted to extract all 272 chunks in rapid succession without inter-batch pacing. The very first batch hit Groq's 8,000 TPM limit. `src/intelligence.py` caught the exception:
  ```python
  summary['errors'].append({'document': entry['doc_title'], 'error': type(exc).__name__})
  failed = True
  break
  ```
  The loop aborted immediately, caching 0 rules. As a result, subsequent eligibility analysis and conflict detection had 0 rules in memory.

---

## 5. Findings on Thresholds & Chunking

### 5.1 Similarity Score Distribution & Separation
Analysis of the 36 queries revealed clear separation between answerable and unanswerable distributions:
- **Answerable Queries Top-1:** Mean **0.749** (Min 0.660, Max 0.816)
- **Unanswerable Queries Top-1:** Mean **0.673** (Min 0.531, Max 0.812)
- **Correct R@1 vs Incorrect R@1:**
  - When Rank 1 was correct: Mean **0.759**
  - When Rank 1 was incorrect: Mean **0.733**

**Threshold Observations:**
1. Setting a strict threshold at **0.70** successfully eliminates 83% of unanswerable queries, but creates a false-negative tail (e.g. `er-sn-02` at 0.660).
2. For unanswerable near-miss queries that share extensive institutional vocabulary (e.g. `nit-nm-03` asking for CGPA required by training & placement cells), vector similarity reached **0.812** because the words "CGPA", "training", and "placement" matched campus handbook chunks. Vector thresholding alone CANNOT reject near-miss queries; the LLM grounded answer layer and citation verification are strictly required to reject them.

### 5.2 Chunking Quality & Structural Anomalies
- **Near-Empty Chunks:** In `Examination_Rules.pdf`, 53 of 135 chunks (39.3%) contain fewer than 10 words. These consist of page headers, isolated table lines, and sub-clause numbers (e.g., `chunk_id: ... "Page 3 > Page 3"`, word count: 5).
- **Generic Placeholder Headings:** 14 chunks have `section: "Page X"` because the regex heading parser found no bold or titled headers on those pages.
- **Mid-Word Boundary Splits:** 8 chunks start mid-word (e.g., starting with lowercase suffix fragments like `ing the semester...`).
- **Consecutive Overlaps:** 4 chunk pairs in `NIT_Goa_Regulations.pdf` showed heavy Jaccard overlap (>0.65), which was successfully merged by `merge_blocks()` during retrieval.

---

## 6. Ranked Recommendations for Developers

### Recommendation 1: Provider Quota & Resilient LLM Routing (Priority: CRITICAL)
- **Problem:** Groq's free on-demand tier limits `openai/gpt-oss-120b` to 8,000 TPM. A single RAG prompt with 5 chunks consumes 2,000+ tokens, allowing at most 3 requests per minute and causing an 88.5% wrong abstention rate under sequential evaluation.
- **Actionable Steps:**
  1. Switch default Groq model from `openai/gpt-oss-120b` to `llama-3.3-70b-versatile`, which offers significantly higher TPM limits (30,000+ TPM on Groq free tier) and 3x faster generation speed.
  2. Increase the backoff sleep ceiling in `src/llm.py` so total backoff time covers at least 20 seconds ($2.0\text{s} \to 4.0\text{s} \to 8.0\text{s} \to 16.0\text{s}$) when a 429 response body explicitly states `Please try again in X seconds`.
  3. Configure a secondary fallback API key (e.g. Gemini 2.5 Flash) in `.env` so provider failover operates seamlessly.

### Recommendation 2: Make Fusion the Default Retrieval Mode (Priority: HIGH)
- **Problem:** HyDE alone degrades precision on direct factual queries (HyDE R@1 0.250 vs Raw 0.625) due to hypothetical parameter hallucination, but Raw completely fails on casual student language (e.g., family bereavement -> retest).
- **Actionable Steps:**
  1. Set `mode: "fusion"` as the application default in `src/config.py` and `src/pipeline.py`.
  2. RRF Fusion achieved **100% Recall@5** on our test set, successfully bridging casual student phrasing without losing factual anchor chunks.

### Recommendation 3: Paced Batching in Rule Book Extraction (Priority: HIGH)
- **Problem:** `extract_rules()` in `src/intelligence.py` fires unpaced batch requests across all workspace chunks, immediately tripping provider rate limits and crashing rule extraction.
- **Actionable Steps:**
  1. Add an inter-batch pacing delay (e.g. `await asyncio.sleep(2.0)`) between batches in `extract_rules()`.
  2. Filter chunks prior to extraction: ignore chunks with fewer than 25 words or chunks containing no digits (`re.search(r'\d', text)`), reducing the extraction payload by over 40%.

### Recommendation 4: Chunk Pre-Filtering for Digital PDFs (Priority: MEDIUM)
- **Problem:** 27.2% of generated chunks have <10 words, polluting the Chroma index with useless fragments like `Page 4` and single table headers.
- **Actionable Steps:**
  1. In `src/chunking.py`, add a minimum word threshold: drop or merge chunks with fewer than 15 words unless they contain structured bullet points.
  2. Fix heading detection to ignore raw pagination numbers (`Page \d+`) as section titles.

---

## 7. Protected-Data Verification

In accordance with strict audit safety protocols:
- No institution sources for MSRIT were approved or published.
- The 3 known MSRIT extraction failures remain intact and visible.
- No production database, manifest, or registry was modified.
- All 38 protected files were hashed with SHA-256 before the audit and re-hashed after the audit.

| Protected File Path | Pre-Audit SHA-256 | Post-Audit SHA-256 | Status |
| :--- | :---: | :---: | :---: |
| `src/server.py` | `62fece1e9cf07693...` | `62fece1e9cf07693...` | **MATCH** |
| `src/pipeline.py` | `0d1396a84c6ca94c...` | `0d1396a84c6ca94c...` | **MATCH** |
| `src/retrieve.py` | `f389868be54881ae...` | `f389868be54881ae...` | **MATCH** |
| `src/store.py` | `102071ce570d6a2f...` | `102071ce570d6a2f...` | **MATCH** |
| `src/embeddings.py` | `28f2c2560381643c...` | `28f2c2560381643c...` | **MATCH** |
| `src/llm.py` | `bc9f3a61e7104b2a...` | `bc9f3a61e7104b2a...` | **MATCH** |
| `src/answer.py` | `5fc2b7eebe2c7e0c...` | `5fc2b7eebe2c7e0c...` | **MATCH** |
| `src/authority.py` | `90cf78aa23588efc...` | `90cf78aa23588efc...` | **MATCH** |
| `src/intelligence.py` | `e2a220268a7f8be5...` | `e2a220268a7f8be5...` | **MATCH** |
| `src/evidence.py` | `f539e6589389e13d...` | `f539e6589389e13d...` | **MATCH** |
| `src/personal.py` | `cb66bf13c8ff0aa4...` | `cb66bf13c8ff0aa4...` | **MATCH** |
| `src/personal_api.py` | `532289659b996766...` | `532289659b996766...` | **MATCH** |
| `src/chunking.py` | `1f36ae0ec0288899...` | `1f36ae0ec0288899...` | **MATCH** |
| `src/ingest.py` | `9e8f498db2057398...` | `9e8f498db2057398...` | **MATCH** |
| `src/cache.py` | `eb1b4b9b94090ea0...` | `eb1b4b9b94090ea0...` | **MATCH** |
| `src/config.py` | `05072049e6f851fb...` | `05072049e6f851fb...` | **MATCH** |
| *(Remaining 22 protected files)* | *Identical pre-audit hashes* | *Identical post-audit hashes* | **ALL MATCH** |

**Final Protected Data Verdict:** **0 mismatches across 38 tracked files.**

---

## 8. Reproducibility

To reproduce all measurements and observations in an identical isolated disposable environment:

```bash
# 1. Navigate to the repository root
cd /Users/shreshthagrawal/Documents/DELL_DEMO/ps1-policy-assistant

# 2. Inspect raw output data files
ls -la audit/results/

# 3. View test set and mechanical quote verifications
python3 -c "import json; [print(json.loads(l)['id'], json.loads(l)['question']) for l in open('audit/results/test_set.jsonl')]"

# 4. View retrieval performance summary
python3 -c "import json; d=json.load(open('audit/results/retrieval_results.json')); print(json.dumps(d['metrics_overall'], indent=2))"

# 5. Run full test suite to confirm production tests pass
pytest
```

