# Source review: initial MSRIT dataset and institution-independent platform

Review date: **14 November 2026**. Scope: a read-only content, extraction and architecture audit. MSRIT/Ramaiah Institute of Technology is the initial demonstration institution, **not** a product-wide institution restriction. Information from this dataset must not be applied to another institution.

The recommendations below are review findings, **not approvals or rejections**. No application code, registry metadata, source status, PDF, index, manifest, cache or benchmark label was changed. No OCR, reindexing or live answer generation was performed.

## A. Current MSRIT document audit

### A1. Evidence and limitations

- Inspected all **517 indexed real-document chunks** across seven PDFs, their stored page/section/hash metadata, and the corresponding PDF text. The separate four evaluation-decoy chunks are not institutional evidence.
- Compared every stored chunk body with its normalized source page: **517/517 matched**, and all stored source hashes matched the present PDFs. This establishes text correspondence, **not completeness, correct table interpretation, authenticity or current applicability**.
- Read the policy/service material and surveyed the curriculum's course sections; visually inspected covers, table/diagram pages, image-only pages and all pages of the three extraction failures. Page references below are **physical PDF pages, starting at 1**; printed page numbers can differ.
- All **10 registry entries remain pending**. Their free-text `institution` values are empty; effective dates and source URLs have not been populated. None of the 517 real chunks contains `institution_id`; their stored `approved` flags are false.
- Institution/authority/date/URL observations below come only from the supplied documents, visible page content, embedded links and PDF properties. No original download URL or current official status has been independently verified online. A logo, PDF author field, print/export date or staff name does not itself certify authenticity.
- “Official institutional policy” below describes the document's apparent genre and institutional self-identification; it does not mean the platform has approved it. Missing effective dates remain **not stated**, rather than being inferred from PDF metadata.

### A2. Inventory and classification

| Indexed document | Pages | Chunks | Primary classification | Production recommendation |
|---|---:|---:|---|---|
| `code_conduct_MSRIT.pdf` | 6 | 15 | Official institutional policy; mixed student/faculty/staff handbook | Priority candidate after provenance/current-version and role-scope verification |
| `RAGGING+IS+A+CRIME.pdf` | 1 | 1 | Official institutional policy/anti-ragging notice | Candidate supplementary source after current-authority verification |
| `MALPRACTICE+MANUAL.pdf` | 20 | 49 | Official institutional policy/procedural manual | Strong subject relevance, but hold current whole-file approval until table/continuation risks are resolved |
| `Support _ Proctorial System _ Ramaiah Institute of Technology, Bengaluru.pdf` | 4 | 12 | General institutional information, including student-support procedures | Conditional support/navigation source; not a substitute for current academic regulations |
| `Exam section PPT.pptx.pdf` | 27 | 51 | Academic/course information presented as an orientation slide deck | Hold current indexed version: program/grade/progression context is fragmented |
| `AEC.pdf` | 72 | 373 | Academic/course information; mostly a curriculum/syllabus collection | Exclude the complete file from the general policy corpus; reconsider narrowly scoped AEC procedures separately |
| `contineo.pdf` | 1 | 16 | Irrelevant or unsuitable for policy retrieval: software architecture/capability diagram | Exclude from the student-policy corpus |
| **Total** | **131** | **517** | | |

### A3. Code of Conduct Handbook

Source: [original PDF](<data/raw/code_conduct_MSRIT.pdf>).

**Actual contents and important sections**

- **P1:** identifies the handbook as covering students, faculty and supporting staff at M. S. Ramaiah Institute of Technology, an autonomous institution affiliated to VTU, Belagavi.
- **P2, preamble/student conduct:** identity cards; attendance at lectures/laboratories; the document's stated 85% attendance requirement; absence without permission; tests/examinations; conduct and property; permission for associations, invited speakers and trips.
- **P3, anti-ragging:** prohibition, restrictions involving seniors/freshers, institutional anti-ragging committee, quoted legal provisions and Supreme Court-order material. A Principal stamp/signature is visible on this page.
- **P4, examination rules:** attendance, reporting inability to appear with supporting documents, reporting time/late-entry restrictions, invigilator instructions, communication/material/device restrictions and handing in answer books.
- **P5:** faculty responsibilities, including attendance/CIE entry, proctor meetings, evaluation and faculty leave arrangements. **P6:** supporting-staff conduct and parking rules.

**Supported identification:** institution explicitly named. The handbook is institution-issued in presentation; Principal endorsement is visible on p3, but no reliably identified individual signatory or adoption/effective date is stated. PDF creation metadata is **20 January 2020**, which is not an effective date. The cover prints `www.msrit.edu`; it does **not** give the original PDF URL. The legal reference URLs on p3 are references, not the source URL for this handbook.

**Review flags:** student, faculty and staff rules must not be interchanged. Faculty leave provisions are not student leave permissions. The older legal references/current version need confirmation; this review does not determine their present legal force. Attendance and exam topics overlap other documents, but this is not a byte-identical duplicate. The 15 chunks contain four bodies shorter than 80 characters, so citations should be checked for sufficient context. Candidate use should prioritise the student-facing sections and preserve role labels; no page-level approval feature is currently implemented.

### A4. Anti-ragging notice

Source: [original PDF](<data/raw/RAGGING+IS+A+CRIME.pdf>).

**Actual contents:** a one-page notice headed “Ragging is a crime,” defining ragging, describing possible institutional/police consequences, and directing affected students to approach a faculty member for complaint/redressal. It ends with **Principal, M. S. Ramaiah Institute of Technology**. Its one indexed chunk retains the notice's text together.

**Supported identification:** institution and issuing office are explicit in the footer. No named Principal, effective date or source URL is stated. PDF creation/modification metadata is **5 January 2017**, not a policy commencement date.

**Review flags:** older, undated notice; confirm it is still operative and obtain current reporting/escalation information. It is not a complete current anti-ragging procedure or a verified statement of current criminal law. It overlaps the handbook's anti-ragging section; prefer a single current primary policy rather than treating duplicate coverage as independent corroboration. Suitable as a supplementary, institution-scoped notice only after verification.

### A5. Malpractice Manual

Source: [original PDF](<data/raw/MALPRACTICE+MANUAL.pdf>).

**Actual contents and important sections**

- **P1–2:** RIT-branded cover and contents. Some early contents-page references are one page behind the physical PDF location; use physical page references.
- **P3–4:** acts of malpractice covering behaviour, identification marks, devices, communication/copying, inducement/pressure, unauthorised material, impersonation and destruction of evidence.
- **P5–6:** SEE reporting, seizure/documentation, statements, handling the paper concerned and subsequent papers, inquiry memo and results held pending recommendations.
- **P7:** corresponding CIE reporting procedure.
- **P8–10:** committees, inquiry, severity considerations and recommendations for SEE/CIE. The Principal appoints the SEE committee; its described membership includes the COE, Registrar (Academic) and relevant HODs.
- **P11–14:** a multi-page, two-column **nature-of-malpractice versus possible penalties** table, including repeat cases and SEE/CIE distinctions.
- **P15–18:** blank candidate, invigilator/squad-report and memo forms. **P19:** additional consequences/communications. **P20:** the Principal approves/modifies committee recommendations; COE/Principal office labels appear at the end.

**Supported identification:** institution established by the cover logo, MSRIT address and text references. COE, Principal and the malpractice committee have stated procedural roles; the document is not a named, dated signed adoption order. Effective date and original source URL are **not stated**. PDF creation/modification metadata is **11 March 2025**, not an effective date.

**Review flags:** the indexed text linearises merged cells and cross-page continuations. For example, p11's first chunk interleaves the first offence with a list of SEE options; later offences become separate chunks without that shared context. P13 starts with a continuation from the preceding page. **Do not derive an automatic one-offence/one-penalty mapping from these chunks**: the source itself assigns severity assessment and recommendations to the committee/Principal. Blank annexures are forms, not completed case facts. Some wording/cross-references are awkward; clarify from the issuing office rather than silently correcting them. This is valuable policy material, but the current whole-file representation should remain outside production until the sensitive table and continuation context are made reviewable and verified.

### A6. Proctorial System page printout

Source: [saved PDF](<data/raw/Support _ Proctorial System _ Ramaiah Institute of Technology, Bengaluru.pdf>).

**Actual contents and important sections**

- **P1–2:** purpose of mentoring/proctorial support, objectives, Chief Proctor contact information and faculty-proctor functions.
- **P3:** proctorial process history, students allocated to proctors, Student Information Records, meetings, progress reporting, attendance/CIE monitoring and Contineo e-sutra SIS access. It states attendance of 85% and internal marks of 40% in its progress-reporting discussion.
- **P4:** counselling-service description and the process for registering through the Proctor/HOD/Chief Proctor's office. A link is labelled “Proctor Students List”; its contents were not fetched.

**Supported identification:** Ramaiah Institute of Technology is in the title/footer. The page names **Dr Monica R Mundada** as Chief Proctor and describes the Chief Proctor/HOD/Principal structure; these are names/roles as printed, not independently verified current appointments. The visible page-source base is **`https://www.msrit.edu/support/proctorial-system.html`**; the footer's tracking query is truncated, so it has not been reconstructed. This is the one clear document-specific institutional page URL supported by the supplied files. Capture footer **13/11/26, 10:43 pm** and PDF export metadata identify capture, **not** publication/effective date.

**Review flags:** the saved four pages carry original print pagination **3–6 of 13**, so this is a partial website printout, not proof of a complete policy document. Staff names, appointments, service times and contacts may change. Its general CIE statement must not override program-specific rules elsewhere. Navigation and print footers are indexed; four chunks repeat the timestamp alone as their body. A linked student-assignment list would require separate relevance/privacy review before any later ingestion. Useful for support navigation after currentness verification; limited authority for academic eligibility or exceptions.

### A7. Examination orientation presentation

Source: [original PDF](<data/raw/Exam section PPT.pptx.pdf>).

**Actual contents and important sections**

- **P1–3:** freshers/parents presentation by **Dr G S Prakash, Controller of Examinations**, exam-section responsibilities and NEP/curriculum overview.
- **P4–8:** credits and minimum/maximum durations by program, exam workflow/calendar and CIE/SEE evaluation structure.
- **P9:** stated examination eligibility of 85% attendance and at least 20/50 CIE marks. **P10:** separate passing-standard tables for BE and for the other listed programs. **P11–14:** grade bands, transitional I/X grades, SGPA/CGPA and award-of-class information.
- **P15–18:** vertical progression, failed/re-registered subjects, supplementary/backlog arrangements and activity-point categories. **P19:** example admission/hall ticket; **p20–21:** website/results navigation. **P22–25:** award-of-degree criteria, honours/minor conditions and credits. **P26–27:** graduation photograph/closing material.

**Supported identification:** RIT branding and the stated COE presenter support institutional context. P1 prints **`10/4/2024`**; its day/month order is not established here. This is a presentation date, not an effective-date notification. No original presentation URL is supplied. `www.msrit.edu/Examination/Results` on p21 is a related results address, **not** this PDF's provenance URL.

**Critical representation flags**

- **P4:** degree-table rows are split; a previous row's maximum duration becomes part of the next chunk's heading, such as `8 / Diploma Students`.
- **P10:** the BE/other-program labels occur in a separate preamble chunk from the two passing tables; retrieving just the table can lose which thresholds apply.
- **P11:** grade points become headings attached to the next band, making a single chunk misleading.
- **P15:** diagram labels and qualifiers are fragmented. The stored page chunks do not retain the complete first-year-completion condition for progression to fourth year, and lose the “not more than” qualifier around the credit condition. A text match for each surviving chunk does not detect this missing meaning.
- **P14 versus p22:** the deck displays a class band starting at CGPA 4, but separately lists CGPA 5 for degree award. Do not infer one universal graduation threshold without knowing the relevant program/cohort and current regulation.
- **P19** contains identifiable student information/photo in an example ticket. Its image text was not indexed; it must not be turned into general policy evidence or indiscriminately OCR-indexed later. No student identifiers have been reproduced in this report.

This is a useful roadmap to academic-rule topics, **not a safe current production policy source in its present chunk form**. Obtain the authoritative current program/cohort regulations and retain their tables/conditions together before using these thresholds for student answers.

### A8. AEC curriculum

Source: [original PDF](<data/raw/AEC.pdf>).

**Actual identity:** **Curriculum for Ability Enhancement Courses**, printed **Academic Year 2022–2023**, **scheme from 2021–22** on the visible cover and text title page. It is not a general attendance/exam/leave handbook.

**Contents and important sections**

- **P1–7:** cover, historical ranking/institute introduction, vision/mission/quality statement, program outcomes and NEP/AEC rationale.
- **P8:** AEC credits, registration under proctor supervision, the III–V semester course-selection/non-overlap requirement and parent-department registration, plus AEC-specific assessment.
- **P9–10:** catalog of 22 AEC offerings. **P11–68:** syllabi, units, pedagogy, references, outcomes and assessment tables: scientific writing, environmental life-cycle assessment, UNIX shell programming, engineering geology, technical writing/LaTeX, electrical safety, engineering aptitude, agriculture technology, psychology, employability soft skills, environmental law, value engineering, green IT, IT capacity planning, rural development, Indian education systems, sensors, HR management, business analytics, contract law, project management and cyber law.
- **P69–70:** anthem and institute vision/mission/quality/contact material, not extracted as text. **P71–72:** an appended Public Speaking for Engineers syllabus, not listed among the 22 entries on p9–10; no separate amendment date was found.

**Supported identification:** Ramaiah Institute of Technology, autonomous/VTU-affiliated, is printed. Multiple teaching departments/course coordinators are identified, but a formal issuing committee/signatory and current adoption date are not established. AY/scheme labels are supported applicability information, **not an inferred ISO effective date**. The cover/back matter shows `www.msrit.edu`; an original PDF URL is not supplied. November 2026 PDF metadata reflects a Firefox/PDF.js print/export, not a 2026 curriculum edition.

**Review flags:** this older, cohort-specific curriculum accounts for **373/517 (72.1%)** of the real chunks and could dominate an otherwise small policy corpus. Course descriptions about law, ethics, psychology or safety are teaching content, not student permissions or institution-wide rules. Assessment tables and repeated outcomes/references yield many fragments: 207 chunk bodies are shorter than 80 characters. P8's summary does not explain test averaging, whereas tables such as p16 do; do not simply sum two 30-mark tests and another 20 as the stated CIE total. P68 labels continuous internal evaluation with `(SEE)`, an apparent source acronym inconsistency. Repeated assessment text and an undated appendix also need version/context review.

**Recommendation:** keep the whole file outside the general student-policy corpus. A later, separately reviewed AEC-registration/assessment extract could be useful for the correct scheme/cohort; full-course syllabus search belongs in a separately classified academic-information scope. This audit creates neither an extract nor a new approval mechanism.

### A9. Contineo diagram

Source: [original PDF](<data/raw/contineo.pdf>).

**Actual contents:** a one-page RIT-branded diagram of a software platform for academic autonomy/outcome-based education. It lists planning, admission/fees, attendance/CIE workflows, evaluation, reporting/analytics and parent/student services. It does not specify actual eligibility conditions, approval procedures, fee schedules or student rights.

**Supported identification:** the page visually carries the Ramaiah Institute of Technology logo and credits **`contineo.in`** as the software provider. This is not a policy-issuing authority or an institutional PDF source URL. The PDF title references `DKTEeduArchitecture_diagram_may_2016.cdr`, while creation metadata is **16 January 2017** and the diagram contains historical sample result periods. The reused internal title creates provenance/version ambiguity; it does not override the visible RIT branding or prove ownership by another institution. No effective date or original institutional source URL is established.

**Review flags/recommendation:** flattened diagram relationships and vertical typography produce 16 mostly short, disconnected chunks. Exclude this file from policy retrieval. A label such as “eligibility approvals” is a software feature, not proof of eligibility or permission. It might be retained outside the policy corpus as historical IT-system background after provenance review.

### A10. Cross-document quality and currency findings

- No two supplied PDFs have the same SHA-256 hash. There is **topical/boilerplate duplication**, not evidence of ten unique policy authorities: anti-ragging overlaps the handbook; attendance overlaps the handbook, exam deck and proctorial page; AEC repeats assessment structures and general institute material.
- Indexed text correspondence is good, but **semantic completeness is not**. Short chunk bodies below 80 characters (excluding the complete generated title/section header): AEC 207/373; exam deck 34/51; malpractice 10/49; anti-ragging 0/1; proctorial 4/12; conduct 4/15; Contineo 8/16. This is a diagnostic, not a relevance/accuracy score.
- Older file metadata does not prove a policy has expired. Conversely, a new print/export timestamp does not prove its contents are current. Cohort, program, role, hostel/residency category and effective version must be verified before answering.
- The proctorial page's generic 40% internal-marks language and the exam deck's different passing standards need program/cohort clarification. Shared 85% attendance statements are not evidence that the full corpus is current or covers every exception.
- The dataset is not a complete policy library: it does not establish a current general leave/condonation policy, automatic entertainment-related attendance exemption, or comprehensive accommodation/appeal policy. Absence here is not proof such policies do not exist.

## B. Extraction failures

All three PDFs open and render successfully, are unencrypted, and have **zero extracted characters in both PyMuPDF and pdfplumber**. They are not password failures or merely empty files. Inspection used page images and PDF structure; **no OCR was implemented or run**.

| File | Physical structure | Diagnosis | Visible content and scope |
|---|---|---|---|
| `Common+Brochure+2026-v5-web.pdf` (12 pages) | No embedded text fonts or character layer; raster artwork/photos plus about 4,040 vector drawing objects; Adobe Illustrator creator | Digitally designed, flattened/outlined text with images; **not simply a scanned-text PDF** | RIT promotional brochure: institute/profile/rankings, programs, international admissions, clubs, research/library, scholarships, placements, sport/culture, hostel/alumni and admissions contacts |
| `Hostel.pdf` (2 pages) | No text fonts/character layer; photos/artwork plus about 7,300 vector drawings; CorelDRAW creator | Designed/outlined hostel leaflet; visible text is represented as artwork rather than selectable text | Boys' hostel facilities **and genuine refund, residence, discipline and mess rules** |
| `UGCOURSE-1STYEARB.E&B.ARCHFEESSTRUCTURE2026-2027.pdf` (1 page) | No text fonts/character layer; 19 raster-image placements and no vector drawings; Konica Minolta scanner metadata; content displayed sideways | **Image-based scanned fee notice**, without a searchable text layer. Rotation is additional presentation work, not the reason text becomes extractable | First-year 2026–2027 B.E./B.Arch fee schedule by admission/residency category; foreign/NRI/PIO miscellaneous fees, payment modes and Registrar stamp |

### B1. Brochure evidence and recommendation

Source: [original PDF](<data/raw/Common+Brochure+2026-v5-web.pdf>).

Classification: **Brochure or informational material**. RIT name/logo and `www.msrit.edu` are visible; p12 lists the **Admission Section (Deputy Registrar)** as a contact, not a dated policy approver. Filename/title indicate a 2026 brochure and PDF creation metadata is **9 April 2026**; no policy effective date is established. P1 expressly uses 2025 rankings, and p5's NRI/FQ/PIO criteria explicitly refer to **VTU eligibility for 2025–26**. Do not present those as automatically applicable to 2026–27. P7 describes scholarships/application availability but is not a comprehensive current scholarship regulation.

Original official PDF URL is not supplied. Keep excluded from the core policy corpus even if text is later recovered; consider separately labelled institutional/admissions information after date-specific verification. Request a searchable original/export if needed rather than treating parser fallback as OCR.

### B2. Hostel evidence and recommendation

Source: [original PDF](<data/raw/Hostel.pdf>).

Classification: **Brochure/informational material with embedded official institutional-policy content**. It is explicitly for **RIT boys' hostels**, not all students or every campus residence. P1 contains hostel blocks, mess times, a time-dependent refund table and named wardens. P2 contains facilities; accommodation eligibility/deposits; room allocation/change rules; belongings/electrical equipment; cooking/food/behaviour restrictions; absence/notice/vacating rules; and mess rules/limited leave conditions. The refund table distinguishes admission before occupancy, departure within one month, within two months, and later departure; component-level wording matters, not merely a single “refund percentage.”

P2 places hostel management under **Gokula Education Foundation Trust, under the Principal's direction through the Warden and appointed officials**. These are governance roles actually stated in the leaflet. P1 names the Chief Warden and deputies; these are not verified current appointments. No operative date or original PDF URL is visible. Creator metadata is **24 May 2025**, and its title says “Book work (May 25)”; neither proves an effective date. The `hostel@msrit.edu` contact is an email address, not a source URL.

Unlike a purely promotional brochure, this is **worth recovering for the appropriate institution/residency scope**, especially refund and absence/mess rules. Keep excluded now because there are no indexed chunks, origin/currency are unverified, and its tables need faithful recovery and review. Seek a selectable-text original, or authorise a separate OCR/review task later; no recovery was undertaken here.

### B3. Fee-structure evidence and recommendation

Source: [original PDF](<data/raw/UGCOURSE-1STYEARB.E&B.ARCHFEESSTRUCTURE2026-2027.pdf>).

Classification: **Official institutional policy/administrative fee notice**, as presented by its institutional header and visible Registrar stamp/signature. The signatory's individual name is not reliably established. It expressly covers **first year, academic year 2026–2027**, with different CET/SNQ and COMED'K/management, program and Karnataka/non-Karnataka/SAARC categories; a separate foreign-national/PIO/NRI line concerns miscellaneous fees. The tables must not be collapsed into one universal tuition amount. It also lists payment modes and an exchange-rate condition.

The AY is directly supported; an exact commencement/issue date and original source URL are not stated legibly. Scanner metadata records **9 July 2026** but is not a policy effective date. Keep excluded from retrieval until searchable content/table structure, issuing-office provenance and applicability are verified. It is a useful future scoped fee source, not evidence for other institutions, other admission years or continuing-year students. No OCR or fee data entry was performed.

## C. Document suitability recommendations

**No source should enter production solely on this audit's classification.** All remain pending. Authenticate the official origin, confirm the applicable current version and inspect the actual indexed representation before any later approval. Existing approval operates at **whole-document level**, so “use only these pages” below is a curation recommendation, not an available page-level approval operation.

| Priority/disposition | Documents | Conditions before production consideration |
|---|---|---|
| First review candidates for student-policy evidence | Code of Conduct; anti-ragging notice | Confirm current approved institutional copies, role/cohort scope and source URLs; review old legal references and overlap |
| Strong policy relevance, but current representation needs resolution | Malpractice Manual | Verify authority/currentness; preserve multi-page penalty tables and committee discretion; omit blank-form noise from any future curated evidence |
| Conditional student-support source | Proctorial System | Verify current office/service details; distinguish support procedures from binding academic regulations; remove irrelevant print/navigation fragments in a future authorised curation step |
| Hold current full-file representation | Examination presentation | Obtain current authoritative regulations or reviewable table-preserving extracts; resolve program/date/progression/grade context and remove example personal data from any future evidence source |
| Exclude full file from general policy retrieval | AEC curriculum | Mostly older syllabus content; only separately verified, cohort-specific AEC procedures might later merit a narrow extract or academic-information scope |
| Exclude from policy retrieval | Contineo architecture diagram; Common Brochure | Capabilities/marketing are not student permissions. Separate informational search is a possible future product choice, not implemented here |
| Recover and review later; excluded now | Hostel leaflet; first-year fee notice | Both contain relevant, narrowly scoped rules, but no extractable/indexed text. Obtain usable originals or separately authorised OCR; verify dates, provenance, categories and table structure |

The evaluation decoy must remain excluded regardless of content similarity. These recommendations apply only to this initial institution's dataset. Another college's documents require their own authenticity, applicability and version review.

## D. Multi-institution architecture compatibility

### D1. Verdict

The core is **institution-neutral in wording and reusable for another college**, but it is currently a **single global corpus application, not an institution-isolated platform**. `SourceEntry.institution` is a descriptive string; it is not an institution identity, access check or query boundary. There is no implemented institution workspace/upload lifecycle or student institution selection.

Currently all sources are pending, so this corpus is fail-closed for production answers. However, approving documents from two institutions in the current shared deployment would make both eligible in the same retrieval pool. The answer grounding/citation guards do not determine which institution owns a chunk. Therefore the intended workflow is not safe merely by entering institution names in the existing registry.

### D2. Scope audit by layer

| Layer | Actual current implementation/evidence | `institution_id` isolation? | Minimum implication |
|---|---|---|---|
| Institution workspace and roles | No institution entity, membership/RBAC, workspace-create or document-upload endpoint; source CLI assumes a trusted local operator | **No** | Add institution records and authorised administrator scope; upload/review actions must be bound to that scope |
| Source registry (`src/authority.py`) | Global JSON keyed by `doc_id`; optional free-text `institution`; approval validates current file hash/synthetic status, not tenant membership, issuer provenance, date or applicability | **No** | Require a stable owner ID and scoped registry keys/lookups/mutations, with recorded review evidence |
| Raw files and indexing (`src/config.py`, `src/ingest.py`, `src/reindex.py`) | One `data/raw/`, decoy directory and manifest; flat scan. Document ID is normalised filename stem; delete/replace is by `doc_id` alone | **No** | Resolve storage/manifest and document operations under a trusted institution scope; namespace document/version IDs |
| Chunk identity/metadata (`src/chunking.py`) | Chunk hash uses `doc_id`, section and index. Metadata has no institution field. Confirmed missing from all 517 real chunks | **No** | Include institution ownership in IDs and persisted metadata so same-named documents cannot collide |
| Vector index (`src/store.py`) | One global persistent client/`policy_chunks` collection; filter requires approval, live registry/hash match and exclusion of decoys/synthetic material | **No** | Add a mandatory institution boundary before candidate selection; keep the existing approval/hash/decoy guards |
| Raw/HyDE/fusion retrieval (`src/retrieve.py`) | Every mode propagates `production`, but no mode/signature carries an institution ID | **No** | Require and propagate institution scope through raw, HyDE, fusion and fallback paths |
| Pipeline/citation eligibility (`src/pipeline.py`, `src/store.py`) | `ask(question, mode, use_cache)` and citation checks use globally approved chunks | **No** | Validate ownership on fresh answers and cached citations against the selected institution |
| Answer cache (`src/cache.py`) | Global JSON/list; key matching is normalised question. Fingerprints verify source/chunk content, not selected institution; invalidation is by global `doc_id` | **No** | Partition keys, lookups, stored traces/fingerprints and invalidation by institution |
| HyDE cache (`src/hyde.py`) | Key covers question, prompt/template, token limit and provider config; shared file, no institution scope | **No** | Scope search-key cache for privacy/context. HyDE remains a search key, not policy evidence |
| API/UI (`src/server.py`, `web/`) | Question schema accepts only `question` and `mode`; extra fields forbidden. No institution selector or admin identity checks. Sources, reindex, cache and benchmark routes are global | **No** | Carry explicit, validated institution context and scope both reads and administrator mutations |
| Traces/prompts (`src/trace.py`, `src/prompts.py`) | Prompts are generic; citation labels are local C1/C2, with no ownership identity in trace metadata | **No enforcement** | Attach institution/document-version provenance to traces; prompt wording cannot substitute for server-side filtering |
| Benchmark | One global candidate query file/results directory; labels reference global chunk IDs | **No** | Bind datasets/gold IDs/reports to an institution; do not reuse MSRIT labels or measured outcomes for another institution |

Code inspection was supplemented by read-only/in-memory checks: `/institution-a/policy.pdf` and `/institution-b/policy.pdf` produce the same current `doc_id`; identical document/section/index inputs produce the same current chunk ID; the request model has only `question`/`mode`, and adding `institution_id` raises validation error. No actual sources were registered for those examples.

### D3. Important distinctions

- Approval filtering is implemented; **institution filtering is not**. Live source fingerprints protect version correctness but do not fix cross-institution cache hits.
- The vector store's optional caller `where` is not an existing tenant feature: metadata lacks `institution_id`, and public retrieval paths do not supply institution scope. Future enforcement must not be caller-optional or bypassable with `production=False` in student-facing routes.
- `CHROMA_DIR` can point elsewhere, but changing that variable alone does **not** partition the global registry, raw files, manifest and answer/HyDE caches. Fully separate project deployments can isolate data operationally; that is not the intended in-app multi-institution workflow.
- Generic prompts, parser/chunker, local embeddings, cosine/RRF separation, abstention, citation checking and source-version validation are useful foundations. They do not need institution-specific hardcoding.
- `web/app.js` currently contains a benchmark warning mentioning “approved MSRIT documents.” It should eventually use neutral/selected-institution wording. This is a demonstration-text assumption, not an existing MSRIT enforcement mechanism; it was not edited during this audit.

## E. Minimum changes required for institution-independent support

**Design recommendations only; none were implemented.** No MSRIT-specific identifier, domain, policy threshold or default institution should be hardcoded.

1. **Define explicit institution ownership and access.** Add stable institution IDs and workspace records. Bind authorised administrator accounts/memberships to institution actions. Students must select a valid institution; access should follow its publication settings. Reject missing/unknown scope rather than silently falling back to a global corpus. Institution selection is not administrator authorisation.
2. **Scope storage and identity.** Use institution-owned upload/raw/processed/manifest locations and stable document/version IDs. Include institution identity in chunk IDs and metadata. A shared vector collection with a mandatory institution predicate is sufficient for a minimal version; a per-institution collection resolver is an alternative, not an additional requirement. The existing local stack can be retained initially.
3. **Make ingestion and source review institution-aware.** Pass trusted scope from upload through extraction, registry, chunking and index commits. Scope all approval/rejection/delete/reindex operations to the owning institution. Record issuing authority, provenance URL/evidence, applicability, effective/version context and reviewer identity/time against the exact file hash. Unknown dates must remain unknown with a review disposition, not be fabricated. Existing optional date/URL fields do not constitute this workflow today.
4. **Enforce scope at retrieval and final validation.** Require institution context in the API, `ask`, `retrieve` and store interfaces, including raw/HyDE/fusion fallback and comparison paths. Apply institution + approval/current-version + non-decoy/non-synthetic restrictions **before ranking**. Validate returned/cached citation ownership too; never rely on the LLM or institution words in the question for isolation.
5. **Partition every cache and output.** Include institution ID in answer-cache and HyDE-cache keys, content fingerprints/trace provenance, persistence and invalidation. Scope source listings, cache controls, index jobs, benchmark labels/results and citation/source-file access. Shared immutable model weights are fine; cached answers and source data are not a shared institution-neutral resource.
6. **Expose the intended workflow.** Add an institution selector and institution-scoped administrator workspace/upload/review controls backed by the server's access checks. Uploads enter pending state; they do not gain trust from filename/domain/logo recognition alone. Keep source review and whole-document/curated-extract applicability explicit; do not imply a page-level approval capability that does not exist.
7. **Plan a non-destructive migration.** Back up and inventory existing data first. An authorised reviewer must explicitly assign the current demo records to the correct institution workspace. Treat legacy records lacking ownership as unassigned/quarantined, not globally eligible or automatically assigned to every institution. Stage new IDs/metadata/index state and validate before switching; preserve originals and review statuses. Legacy unscoped cache entries must not be reused across institutions. No migration, reset or metadata assignment was performed here.
8. **Prove the boundary before hosting a shared platform.** Add two-institution tests with identical filenames, identical questions and different policies; assert no foreign chunks, cached answers, citations, source listings or administrative mutations cross scope. Cover approval changes, version updates/deletions, fallback, decoy isolation, missing scope and legacy data. Existing local-process locks are not distributed transactions; multiworker/distributed deployment needs separate coordination review, not an unrequested rewrite now.

**Minimum release gate:** a request selecting institution A must be unable to retrieve, cite, cache-hit or mutate institution B's documents through any supported path. This must hold independently of model behaviour, document wording and whether both institutions' sources are approved.

## Audit completion and preservation check

The only intended project deliverable for this task is this report. All existing source statuses remain pending, and no source metadata was populated from these findings. Final SHA-256 checks confirmed all 54 protected existing application, configuration, PDF, registry, manifest, cache, benchmark and index files were unchanged. All ten registry statuses remained pending. All ten report links target existing PDFs, and report sections A–E were validated. No ingestion or approval command was run. Temporary extracted-text copies and rendered page images were used only for read-only review, outside production storage. No application test suite was rerun because application code was not changed; the checks here are content correspondence, PDF structure/visual inspection, schema/signature inspection and state-preservation checks, not a claim of tested multi-institution support.


## Implementation update — 2026-11-14

The audit above describes the pre-migration snapshot and remains evidence of the original documents. Institution isolation is now implemented as documented in ARCHITECTURE.md and API.md; statements above about missing institution_id describe the audited legacy implementation, not the new scoped pipeline.

The explicitly migrated demonstration workspace has generated ID `192afc66-bae5-4f82-bdb9-6e2cbe4daafb` and is unpublished. All ten real sources remain pending; seven indexed documents/517 real chunks and three failed extractions are preserved. Four decoy vectors remain evaluation-only. No issuer, URL, applicability or effective date was fabricated. Suitability recommendations in this audit still require human review and were not converted into automatic approval or rejection. Legacy files remain unchanged; see MIGRATION_REPORT.md.
