# Personal NIT Goa chunking fix — offline comparison

The user explicitly chose **Leave the live index untouched** after confirmation that personal and institutional vectors share a database. No re-indexing or embeddings were run. Live count remains **77**; offline candidate count is **114** (previous algorithm: **77**).

The downloaded PDF SHA-256 matches its personal registry version. The old Attendance output matches the previous read-only live chunk snapshot exactly. This comparison uses the original PDF and in-memory chunking; it does not initialize Chroma or ingest test fixtures.

## Exact implementation changes

Only `src/chunking.py` application code changed. Personal splitting now records source-body identity and character offsets internally. Continuation/tiny-segment merges re-slice the original body rather than concatenate overlapped text. This removes only generated overlap and preserves intentional repeated sentences. Merges cannot cross a source page or section. Standalone numbered heading lines are paired with recognized following titles; heading numbers remain in the section metadata and chunk text header. Numeric as well as letter-prefixed headings are recognized. Existing institutional `chunk_text`, embedding/provider configuration and retrieval are unchanged.

A single chunk has one page field. Page-spanning rules are therefore retained in adjacent chunks with their actual page numbers rather than silently merged under the first page. The larger candidate count also retains short sections previously merged into preceding sections; count reduction is not a target.

## Full Attendance comparison

Before: chunk 23/77, stored index 22, page 10, 2568 characters. After (offline): chunk 39/114, index 38, page 10, 2400 characters.

### Before — exact old chunk text

```text
Btech (Rules & Regulations)2013 21Nov2023 > Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
B12.
```

### After — exact candidate chunk text

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

### Following section — exact candidate chunk text

```text
Btech (Rules & Regulations)2013 21Nov2023 > B12. Assessment Procedure
B12.1. The CC/DCC will decide from time to time the system of tests and examinations in each subject in consultation with AAC and inform the same to the Senate.
```

## Semantic and boundary verification

The entire new B11 body, from B11.1 through the last B11.5 sentence, equals the source page word-for-word after whitespace normalization. B11.4 is separately compared in full: 80% outside medical leave, 75% overall, faculty/HoD recommendations, AAC discretion, the two-semester limit, IMO endorsement and the seven-day/last-instructional-day deadline are all present. Both B11.5 numbered activity-approval items and its seven-instructional-day deadline remain. No legitimate Attendance policy text was lost.

The repeated passage appears once in the source and once in the new chunk. Deliberately repeated sentences in regression fixtures remain repeated. B12 is absent from Attendance and retained as `B12. Assessment Procedure`; its body starts with B12.1 and exactly matches the source until B13. The heading B11 formerly trailed Discipline; it now belongs to Attendance. The B13 page 10/11 continuation test confirms both halves and correct page provenance.

## Tests

- `python -m pytest tests/test_personal_chunk_boundaries.py tests/test_chunking_ingest.py tests/test_evidence_quality.py -q` — 28 passed.
- `python -m pytest tests/ -q` — **329 passed**, six existing dependency deprecation warnings.

Added `tests/test_personal_chunk_boundaries.py` (14 parameterized cases), plus verbatim page-10 text and provenance README under `tests/fixtures/chunking/`. Tests never ingest this fixture into production. Seven cases specifically cover overlap amounts, legitimate repetitions, unknown offsets and forbidden cross-boundary merges; remaining cases cover exact page 10 through both entrypoints, heading forms, rule-vs-heading detection and page continuation.

## Deployment status and embeddings

The fix is ready for a future explicitly authorized document-scoped re-index. Existing live chunks still contain the old defects until then. Changed chunk text would require new embeddings; unchanged text could reuse matching embeddings, but the current re-index implementation embeds all candidate chunks for the selected document. No embedding-reuse feature was added. No live embedding or provider call was made for this task.

## Integrity verification

SHA-256 snapshots of all 239 files under `data/`, `.chroma/` and `.chroma-institutions/` matched exactly before and after isolated tests/offline comparison, including the shared SQLite database and vector segment files. No files were added or removed in those locations. Other personal workspaces and protected institutional data remained byte-identical.
