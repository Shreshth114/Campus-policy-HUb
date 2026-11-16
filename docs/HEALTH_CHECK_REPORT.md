# Pipeline Health Check Report

- **Date & Time:** 2026-11-14 06:12:15 UTC
- **Workspace ID:** `klgwmSSSROT35DL71N2W7YcAkaUDUBFyn-CDArlJZkU`
- **Host:** localhost / in-process verification

## Summary of Checks

| # | Check Description | Status | Details |
|---|---|---|---|
| 0 | Gemini Provider Fallback | **PASS** | Gemini fallback: configured (model: gemini-3.5-flash-lite) |
| 1 | Document & Chunk Inventory | **PASS** | 1 doc(s), 6 page(s), 13 chunk(s): code_conduct_MSRIT (13 chunks, 6 pages) |
| 2 | Chunk Word Boundaries | **PASS** | 5 sample chunks inspected; all start/end on intact word & punctuation boundaries |
| 3 | Embedding Model & Dimensions | **PASS** | Model: BAAI/bge-small-en-v1.5, Vector Dimension: 384, Unit-normalized: 1.0000 |
| 4 | ChromaDB Record Consistency | **PASS** | ChromaDB has exactly 13 records, matching registry chunk count (13) |
| 5 | Multi-Mode Retrieval (3 Queries) | **PASS** | Raw, HyDE, and Fusion top-3 successfully computed for 3 sample queries with separate cosine & RRF scores |
| 6 | HyDE Structural Isolation | **PASS** | Generated HyDE text is verified absent from answer prompt; used strictly as vector search key |
| 7 | Target Question Answer & Verification | **PASS** | Answer: 'Five minutes before the close of the examination.  ' | Gate: PASS | Citations: ['5fc72ea4e40adbacf1c07f102d9ddd38ca054daf2eaede1e03a89af77b7b886c'] | Quotes verified: 1 | Unsupported: 0 |
| 8 | Out-of-Scope Safe Abstention | **PASS** | System safely abstained on 'What is the melting point of tungsten?' with reason: no_policy_found; no hallucinated permissions |
| 9 | Cross-Workspace Isolation | **PASS** | Tenant filtering strictly verified: Workspace B cannot retrieve Workspace A chunks; zero cross-leakage |
| 10 | Cache Hit/Miss Behaviour | **PASS** | Cache lookup verified: cached answer correctly retrieved and source fingerprints validated |

---

## Detailed Verification Details

### Sample Chunks (Word-Safe Boundary Check)

- **Chunk 0 (Page 1 - CODE OF CONDUCT HANDBOOK):**
  - *Start:* `FOR`
  - *End:* `FOR`
  - *Clean boundary:* True
- **Chunk 3 (Page 2 - PREAMBLE):**
  - *Start:* `This Handbook specifies the standard pro`
  - *End:* `nce to fellow students or other classes.`
  - *Clean boundary:* True
- **Chunk 6 (Page 3 - RAGGING IS A CRIMINAL OFFENCE):**
  - *Start:* `(1) shall, on conviction, be punished wi`
  - *End:* `iable to be rusticated from the college.`
  - *Clean boundary:* True
- **Chunk 9 (Page 4 - Examination Rules):**
  - *Start:* `Student must not carry notes, blank pape`
  - *End:* `-books are collected by the invigilator.`
  - *Clean boundary:* True
- **Chunk 12 (Page 6 - Page 6):**
  - *Start:* `Code of Conduct for Supporting Staff Com`
  - *End:* `d outside parking area of the institute.`
  - *Clean boundary:* True

### Three-Way Retrieval Comparison Details

#### Query: *"A warning bell will be given how many minutes before the examination"*

| Mode | Top 1 (Score / Page / Section) | Top 2 | Top 3 |
|---|---|---|---|
| **Raw** | cos=0.776 (p.4 Examination Rules) | cos=0.695 (p.4 Examination Rules) | cos=0.640 (p.5 Page 5) |
| **HyDE** | cos=0.786 (p.4 Examination Rules) | cos=0.779 (p.4 Examination Rules) | cos=0.717 (p.5 Page 5) |
| **Fusion** | cos=0.786, rrf=0.033 (p.4 Examination Rules) | cos=0.779, rrf=0.032 (p.4 Examination Rules) | cos=0.717, rrf=0.032 (p.5 Page 5) |

> **Generated HyDE Passage:**
> A preparatory signal shall be administered by the chief invigilator fifteen (15) minutes prior to the officially designated commencement time of any formal university examination. Candidates shall be permitted to enter the examination hall and occupy their assigned seating during this interval, subject to the inspection of institutional identification cards and authorized materials. No candidate shall be permitted to open the examination booklet or record any response prior to the definitive beginning bell, which shall sound exactly at the scheduled hour. Late arrivals shall be subject to the standard institutional tardiness policy as outlined in Section 14.2 of these regulations.

#### Query: *"What items are prohibited during the examination?"*

| Mode | Top 1 (Score / Page / Section) | Top 2 | Top 3 |
|---|---|---|---|
| **Raw** | cos=0.755 (p.4 Examination Rules) | cos=0.737 (p.4 Examination Rules) | cos=0.629 (p.2 PREAMBLE) |
| **HyDE** | cos=0.791 (p.4 Examination Rules) | cos=0.764 (p.4 Examination Rules) | cos=0.725 (p.2 PREAMBLE) |
| **Fusion** | cos=0.791, rrf=0.033 (p.4 Examination Rules) | cos=0.764, rrf=0.032 (p.4 Examination Rules) | cos=0.725, rrf=0.032 (p.2 PREAMBLE) |

> **Generated HyDE Passage:**
> A student shall be prohibited from possessing, displaying, or utilizing any material, device, or implement within the examination venue that may constitute a source of unauthorised assistance, a means of communication, or a potential source of distraction, including but not limited to electronic communication devices (e.g., mobile phones, smart watches, tablets, laptops), written notes, textbooks, reference manuals, calculators not expressly authorised for the specific assessment, and any form of concealed recording or transmission equipment. The presence of such items shall be subject to immediate confiscation by invigilators, and the student shall be required to submit a written explanation to the Examination Committee; any breach shall be adjud

#### Query: *"What is the attendance requirement to take exams?"*

| Mode | Top 1 (Score / Page / Section) | Top 2 | Top 3 |
|---|---|---|---|
| **Raw** | cos=0.818 (p.4 Examination Rules) | cos=0.734 (p.4 Examination Rules) | cos=0.675 (p.5 Page 5) |
| **HyDE** | cos=0.813 (p.4 Examination Rules) | cos=0.722 (p.4 Examination Rules) | cos=0.698 (p.2 PREAMBLE) |
| **Fusion** | cos=0.818, rrf=0.033 (p.4 Examination Rules) | cos=0.734, rrf=0.032 (p.4 Examination Rules) | cos=0.698, rrf=0.031 (p.2 PREAMBLE) |

> **Generated HyDE Passage:**
> A student shall be eligible to sit for any scheduled examination only upon satisfying the prescribed attendance quota for the corresponding instructional component. The minimum attendance requirement shall be set at seventy‑five percent (75 %) of the total contact hours allocated to the course, as recorded in the official attendance register maintained by the Course Instructor. Attendance records shall be verified by the Registrar’s Office prior to the issuance of examination permits. Exceptions to the attendance threshold may be granted solely on the basis of documented medical or compassionate grounds, subject to the prior written permission of the Head of the Department and the concurrence of the Academic Appeals Committee

### Target Query Grounded Answer

**Question:** *"A warning bell will be given how many minutes before the examination"*

**Answer Generated:**
> Five minutes before the close of the examination.  
“A warning bell will be given five minutes before the close of the examination” [C1]

- **Confidence Gate:** PASS (Threshold=0.35)
- **Cited Chunk IDs:** `['5fc72ea4e40adbacf1c07f102d9ddd38ca054daf2eaede1e03a89af77b7b886c']`
- **Quotes Verified:** `[{'quote': 'A warning bell will be given five minutes before the close of the examination', 'labels': ['C1']}]`
- **Unsupported Claims:** `[]`
- **Passage Deduplication:** 3 chunks merged into 2 evidence blocks

### Out-of-Scope Query Safe Abstention

**Question:** *"What is the melting point of tungsten?"*
- **Result:** `I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.`
- **Abstain Reason:** `no_policy_found`
