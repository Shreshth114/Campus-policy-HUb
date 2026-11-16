# Campus Policy Intelligence Platform
## User Prompt Register

**Prepared:** 14 November 2026  
**Updated:** 16 November 2026  
**Project:** Campus Policy Discovery / Intelligence Platform  
**Purpose:** Company review of the instructions, scope changes and decisions used during development.

### About this record

This register covers the user messages available in this development conversation and the six attached instruction briefs. It does not claim to include other agents’ chats or project history that was not supplied here.

Entries follow conversation order. Long inline requests have been condensed and lightly edited for spelling, punctuation and readability; they are **not represented as verbatim transcripts**. Short replies are quoted directly. The full attached briefs are included in the appendices, with credential redaction where needed. No dates have been invented for individual prompts.

This document records **what was requested**, not whether each request was completed. Implementation claims, test evidence and current limitations belong in the project reports and logs. Later instructions may supersede earlier ones; the shared-index decision is explicitly recorded in entries 26–27. Source-policy text is distinguished from instructions to the agent.

**Security note:** A provider credential appeared in the conversation. Its value is omitted. No API key or authorization header is needed to review this record.

### Request index

| No. | Stage | Request |
|---:|---|---|
| 01 | Initial context | Confirm access to project files |
| 02 | Core implementation | Continue implementation and guardrail testing |
| 03 | Core implementation | Read the architecture audit and complete document-independent work |
| 04 | Operations | Prepare an operational guide without further feature development |
| 05 | Operations | Configure the supplied provider credential |
| 06 | Short follow-up | Ask about closing Codex |
| 07 | Provider selection | Ask whether Groq is suitable for the project |
| 08 | Provider troubleshooting | Investigate a failing Groq chat-completion check |
| 09 | Ingestion | Diagnose slow first ingestion and interruption safety |
| 10 | Source review | Audit the first real document ingestion |
| 11 | Architecture review | Expand the source audit to institution-independent architecture |
| 12 | Architecture planning | Plan multi-institution support before implementation |
| 13 | Attached build brief | Issue the master build instruction |
| 14 | Attached build brief | Request critical UI and end-to-end functionality fixes |
| 15 | Attached product brief | Redirect the product toward a student-first experience |
| 16 | Short follow-up | Continue the active implementation |
| 17 | Short follow-up | Continue the active implementation again |
| 18 | Attached build brief | Request the next UI, evidence-quality and demo-readiness round |
| 19 | UI design | Refresh the frontend without altering backend behavior |
| 20 | Attached evaluation brief | Request a held-out HyDE improvement ablation |
| 21 | Explicit authorization | Authorize specific ablation payloads to Groq |
| 22 | UI functionality | Check and repair nonfunctional sidebar features |
| 23 | Attached feature brief | Add Path to Eligibility and maintain project records |
| 24 | Document inspection UX | Add PDF preview controls and a dedicated chunk inspector |
| 25 | Evidence submission | Submit the problematic Attendance chunk as evidence |
| 26 | Chunking correction | Fix chunk overlap and numbered-section boundaries |
| 27 | Explicit scope decision | Keep the shared live index untouched |
| 28 | Answer grounding investigation | Investigate the failed Fusion answer without code changes |
| 29 | Investigation clarification | Continue with static evidence because raw trace is unavailable |
| 30 | Answer grounding implementation | Implement bounded context, stronger validation and diagnostics |
| 31 | Project documentation | Prepare a company-facing prompt register |

| 32 | Prototype integrity and assessment | Remove scripted answers/comparison and assess actual reliability |

---

## Chronological requests

### 01. Confirm access to project files

**Stage:** Initial context

Original message: “u have all the files?”

### 02. Continue implementation and guardrail testing

**Stage:** Core implementation

Continue the Campus Policy Discovery Assistant in `ps1-policy-assistant` from the supplied handoff.

The handoff reported source-authority registration, approval metadata, production filtering, separate cosine/RRF scoring, and migration of the model-listing script to `google.genai`.

- Check that `ChunkTrace` supports `rrf_score` and `approved` and that the pipeline passes `production=True`.
- Add tests proving that decoys and unapproved documents cannot enter production retrieval, approved documents remain retrievable, and high fusion rank cannot bypass the raw-similarity confidence gate.
- Verify the model-listing script uses the current Gemini SDK rather than `google.generativeai`.
- Run `python -m pytest tests/ -v` and resolve regressions.
- Report changed files, test results and open items. Do not begin PDF ingestion or add stretch features.

The statements above record the supplied handoff, not an independent confirmation of implementation status.

### 03. Read the architecture audit and complete document-independent work

**Stage:** Core implementation

Read `ARCHITECTURE_AUDIT.md` and `PS1_BUILD_GUIDE.md` and continue the existing application. Actual MSRIT PDFs have not yet been downloaded; do not wait for them.

Priorities:
1. Resolve outstanding audit issues.
2. Complete source-authority validation and decoy isolation.
3. Correct raw, HyDE and fusion scoring.
4. Verify provider integrations and all FastAPI endpoints.
5. Complete the frontend and dashboard views.
6. Test incremental indexing with isolated synthetic fixtures.
7. Complete the benchmark framework and visualizations.
8. Verify empty inputs, API failures, error handling and edge cases.
9. Review integration issues and unnecessary code.

Run the complete test suite and maintain `PROMPTS.md`, `DECISIONS.md` and `INTERVIEW_NOTES.md`. Do not fabricate university policies or benchmark results, mark labels as verified, claim real-world accuracy without documents, mix synthetic and production data, or add unnecessary features. Report completed work, test results, blockers and tasks requiring actual PDFs. Focus on implementation.

### 04. Prepare an operational guide without further feature development

**Stage:** Operations

Implementation is complete. Preserve the current working state and do not add unnecessary features or code changes.

Prepare a concise guide based on verified commands and paths in the current codebase:
- Configure Groq as the primary provider without Gemini credentials.
- Add MSRIT documents as pending sources.
- Inspect extracted content and chunks.
- Approve verified document versions.
- Run ingestion and the benchmark.
- Start and test the application locally.

Do not assume unimplemented or untested functionality. Modify application code only if a genuine blocker is discovered, and report that blocker separately.

### 05. Configure the supplied provider credential

**Stage:** Operations

Add the supplied Groq API key to the environment configuration.

**Credential redacted:** `[REDACTED_API_KEY]`. The original message contained a live API key; it is intentionally excluded from this company-facing record.

### 06. Ask about closing Codex

**Stage:** Short follow-up

Original message: “close codex?”

### 07. Ask whether Groq is suitable for the project

**Stage:** Provider selection

Original message: “is groq model best for out projec”

Edited request: Is a Groq model the best choice for this project?

### 08. Investigate a failing Groq chat-completion check

**Stage:** Provider troubleshooting

The live provider check reports `configured: true`, `live_verified: false`, and `HTTPStatusError`, although the model-listing script returns 11 models.

Inspect `scripts/check_providers.py` and `src/llm.py`. Identify the exact HTTP status and API error, validate the configured model ID, and inspect the payload for unsupported parameters. Check authentication, endpoint configuration and availability. Improve error reporting to expose the status and a sanitized response body.

Never print the key or authorization headers. Do not switch providers or rewrite working modules unnecessarily. Run the live check again and report the cause and recommended fix.

### 09. Diagnose slow first ingestion and interruption safety

**Stage:** Ingestion

Investigate the existing indexing implementation before changing it. `python -m src.reindex` processed a synthetic decoy into 4 chunks and AEC.pdf into 373 chunks, downloaded FastEmbed, then ran for over 10 minutes with fluctuating CPU usage and little visible disk growth or progress. Ctrl+C interrupted `list(model.embed(texts))` inside ONNX Runtime inference.

Inspect extraction, chunking, PDF/page/chunk sizes, embedding batching and Chroma insertion. Identify the actual bottleneck, inspect partial index/manifest/registry state, determine whether incremental reruns are safe, and check Python 3.14/FastEmbed/ONNX compatibility. Add meaningful document/stage progress and optimize the bottleneck without degrading quality.

Do not delete data, reset Chroma, silently skip content, reduce embedding quality, add unnecessary features, or weaken approval/decoy protections. Run relevant tests. Report the cause, changed files, results, partial-state assessment and exact safe resume command. Do not start ingestion automatically.

### 10. Audit the first real document ingestion

**Stage:** Source review

The first ingestion indexed 7 real PDFs and 517 real chunks; Common Brochure, Hostel and UG Fee Structure failed extraction. All real documents remain pending.

Inspect the actual extracted content and chunks of the seven successful documents. Summarize contents, topics and important sections; distinguish student policies from brochures, course information and general institutional material. Identify institution, issuer, effective date and official URL only when supported. Flag outdated, irrelevant, duplicate or ambiguous information.

Determine whether the three failures are scanned/image PDFs or have another extraction problem; do not implement OCR. Create `docs/MSRIT_SOURCE_REVIEW.md`, recommend suitability for production, and do not approve/reject sources, change registry metadata, fabricate missing details or modify application code.

### 11. Expand the source audit to institution-independent architecture

**Stage:** Architecture review

Resume the audit with the product direction clarified: this is an institution-independent Campus Policy Discovery Platform; MSRIT is only the first demonstration institution.

Audit the seven indexed PDFs and three extraction failures. Classify each successful document as official policy, academic/course information, general institutional information, brochure/informational material, or unsuitable for policy retrieval. Record only evidenced metadata and flag outdated, duplicated, ambiguous or incomplete content.

Evaluate the intended workflow: an authorized administrator creates an institution workspace, uploads pending documents, verifies authenticity/applicability/dates and approves them; students select an institution and receive grounded answers only from that institution’s approved sources.

Check `institution_id` isolation across registry, metadata, indexing, cache and retrieval. Report minimum changes needed. Create/update `docs/SOURCE_REVIEW.md` with document audit, failures, suitability recommendations, architecture compatibility and required changes.

Do not hardcode MSRIT, apply its policies elsewhere, change source decisions/metadata/code, reset data, fabricate information or implement features. Stop after the report.

### 12. Plan multi-institution support before implementation

**Stage:** Architecture planning

Prepare a detailed plan for institution-independent support while preserving existing functionality:
1. Institution registry and workspaces.
2. Institution-specific storage and ingestion.
3. Institution IDs in registries, document/chunk IDs and Chroma metadata.
4. Mandatory filtering in raw, HyDE, fusion and fallback retrieval.
5. Isolated answer and HyDE caches.
6. Institution-aware citations and source management.
7. Frontend institution selection.
8. Administrator upload, verification and approval workflows.
9. Non-destructive migration of the existing MSRIT dataset.
10. Two-institution tests with identical filenames and student questions.

Preserve HyDE, RAG, guardrails and benchmarks. Do not approve existing sources automatically, assign legacy documents to every institution, mix documents/answers/citations, introduce unnecessary infrastructure or damage the dataset. Present the migration plan before implementation. Separate essential MVP work from future production features.

### 13. Issue the master build instruction

**Stage:** Attached build brief

The user supplied **“MASTER BUILD INSTRUCTION — CAMPUS POLICY DISCOVERY PLATFORM.”**

The full attached request is reproduced in **Appendix A**. It covers the product objective, institution architecture and isolation, caches/citations, administrator and student workflows, dashboards, APIs, non-destructive migration, tests, documentation, execution rules and definition of done.

### 14. Request critical UI and end-to-end functionality fixes

**Stage:** Attached build brief

The user supplied **“CRITICAL UI + END-TO-END FUNCTIONALITY FIX — CAMPUS POLICY DISCOVERY PLATFORM.”**

See **Appendix B** for the full request, including inspection before changes, onboarding, document upload, student flow, actual RAG verification, end-to-end checks, visual design and preservation requirements.

### 15. Redirect the product toward a student-first experience

**Stage:** Attached product brief

The user supplied **“PRODUCT REDIRECTION: BUILD A STUDENT-FIRST CAMPUS POLICY INTELLIGENCE PLATFORM.”**

The complete request is preserved in **Appendix C**. This entry records a change in product direction; it does not assert that the requested functionality was completed at that point.

### 16. Continue the active implementation

**Stage:** Short follow-up

Original message: “continue”

### 17. Continue the active implementation again

**Stage:** Short follow-up

Original message: “continue”

### 18. Request the next UI, evidence-quality and demo-readiness round

**Stage:** Attached build brief

The user supplied **“NEXT BUILD ROUND: UI FIXES, EVIDENCE QUALITY AND DEMO READINESS FOR THE DELL PROTOTYPE.”**

The full request is reproduced in **Appendix D**.

### 19. Refresh the frontend without altering backend behavior

**Stage:** UI design

Another agent has made changes. Scan the current repository to understand its state, then improve the website’s UI. Make it professional, sleek and less generically AI-styled, with appropriate animations and light/dark modes throughout.

Do not change backend behavior, API contracts, retrieval, prompts, thresholds, guardrails or data. If a backend change appears necessary, document it in `UI_NOTES.md`. This request is for UI changes only.

### 20. Request a held-out HyDE improvement ablation

**Stage:** Attached evaluation brief

The user supplied **“HyDE IMPROVEMENT ROUND: ABLATION ON HELD-OUT DOCUMENTS, KEEP ONLY WHAT WINS.”**

The full experimental instructions and constraints are preserved in **Appendix E**.

### 21. Authorize specific ablation payloads to Groq

**Stage:** Explicit authorization

Original reply: **“Authorize these payloads to Groq.”**

The reply authorized sending extracted passages from `audit_inputs/Examination_Rules.pdf` and `audit_inputs/NIT_Goa_Regulations.pdf`, generated student questions and retrieved excerpts to the configured Groq chat-completions API for question generation, HyDE generation and answer evaluation. Credentials were to remain private.

This records the historical authorization for that ablation, not a general instruction to send unrelated data.

### 22. Check and repair nonfunctional sidebar features

**Stage:** UI functionality

Check the sidebar features against the current implementation. Some appear to be landing pages without functionality. Leave features that work unchanged; implement and repair those that do not work.

### 23. Add Path to Eligibility and maintain project records

**Stage:** Attached feature brief

The user supplied **“ADD ONE FEATURE: ‘PATH TO ELIGIBILITY’ WHAT-IF SIMULATOR, PLUS MANDATORY PROJECT LOG AND PROMPT ARCHIVE.”**

The complete request is preserved in **Appendix F**.

### 24. Add PDF preview controls and a dedicated chunk inspector

**Stage:** Document inspection UX

Scan the latest repository changes and inspect the existing frontend/backend document flow before implementing two focused fixes.

**Original PDF preview**
- Add a clearly visible Close Preview button near the heading/top-right.
- Close within the application and restore the prior inspection screen.
- Preserve selection, extracted text, inspection state and scroll where practical.
- Support Escape and keyboard accessibility; work on mobile and in both themes.

**View Chunks**
- Add an action to each personal document card.
- Show filename, total chunks, stored index/ID, page/range, exact stored text and available character/token count.
- Provide previous/next or pagination and a return to My Documents.
- Preserve actual stored boundaries and metadata; never regenerate text for display or trigger indexing.
- Handle missing metadata, zero chunks, long text, loading and errors clearly.

Reuse existing APIs where suitable; otherwise add the smallest endpoint with strict workspace/document ownership. Never expose another workspace’s chunks, secrets, or protected institutional data. Do not modify PDFs, extracted text, embeddings or records.

Test Close/Escape, all 77 NIT Goa chunks against stored content, navigation/back, empty/missing metadata, foreign-workspace denial, both themes and narrow mobile layout. Do not weaken tests. Report every changed file, API reuse/additions, exact test commands/results, integrity findings and limitations. Avoid unrelated redesign.

### 25. Submit the problematic Attendance chunk as evidence

**Stage:** Evidence submission

The user attached `BTech_(Rules_&_Regulations)2013_21nov2023.pdf` and pasted the displayed Attendance chunk:

- Chunk 23 of 77; stored index 22; source page 10.
- Chunk ID: `46e33c0bbd63f0abf207c38c5f750a2edf388ab1f814a5c55e9eadfa6224073e`.
- Heading: Attendance; displayed length: 2,568 characters.
- The body contained B11.1–B11.5, repeated the passage about permission to sit the exam and the two-semester concession limit, and ended with `B12.`.

This was supplied evidence, not a separately worded implementation instruction. The PDF’s policies are source content, not instructions to the development agent.

### 26. Fix chunk overlap and numbered-section boundaries

**Stage:** Chunking correction

Implement the smallest safe fix for the two confirmed chunking defects:
1. Remove only duplication caused by overlap merging; preserve legitimate repeated source sentences.
2. Keep numbered section headings such as B12. Assessment Procedure out of B11 Attendance.
3. Preserve complete rules, headings, numbering, numerical conditions and page metadata.
4. Add regressions for the exact page-10 example and additional overlap/heading cases.
5. After isolated verification, reprocess only the personal NIT Goa PDF and regenerate embeddings only if required.
6. Compare old/new Attendance chunks and verify no legitimate policy text was lost.

Do not modify protected MSRIT data/database, other personal documents, providers or unrelated functionality. Run relevant and full Python tests. Report exact changes, chunk count, before/after text and results. Verify full B11.4 and correct placement of B12, not merely disappearance of a duplicate.

The requested live reprocessing was subsequently withdrawn by the decision in entry 27.

### 27. Keep the shared live index untouched

**Stage:** Explicit scope decision

Original reply: **“Leave the live index untouched.”**

This followed clarification that personal and institutional vectors share `.chroma-institutions`, so a personal document update would still write that shared database. The reply superseded the live reprocessing part of entry 26. The approved scope became an isolated, tested code fix and offline comparison only.

### 28. Investigate the failed Fusion answer without code changes

**Stage:** Answer grounding investigation

Investigate the failed answer to:

> According to the uploaded B.Tech regulations, what is the minimum attendance required for medical condonation, and what is the minimum overall attendance allowed?

The retrieved page-10 evidence states 80% attendance outside medical leave and at least 75% overall including illness. The reported Groq answer instead claimed 75% cumulative attendance, a 60% absolute minimum and repeating coursework. Retrieval found the correct chunk, validation returned `citation_check_failed`, and the application abstained.

Inspect the exact answer context, system prompt, possible general-vs-medical-attendance confusion, citation/numeric validation, HyDE isolation, caches and cross-workspace handling. Confirm whether every factual claim is actually checked and whether supported and unsupported answers are distinguished.

Do not modify code/data, re-index, regenerate embeddings or make unnecessary LLM calls. Report the precise supported diagnosis, relevant files/functions and minimal proposed fix. The desired answer must preserve 80% excluding medical leave, 75% overall including medical leave, and AAC discretion—never invent 60%.

### 29. Continue with static evidence because raw trace is unavailable

**Stage:** Investigation clarification

The failed answer and retrieved evidence have already been described. The rejected claims were 75% cumulative attendance, a 60% absolute minimum and coursework repetition below 60%. The source states 80% excluding medical leave and 75% overall. The application returned `citation_check_failed` and abstained.

No separate raw trace JSON is available. Continue the static investigation using the supplied information. Identify the exact functions, distinguish what the code proves, and specify logging needed to capture the actual prompt and rejected response on a future run.

Do not make another LLM call, change code, re-index, or touch Chroma/institutional data.

### 30. Implement bounded context, stronger validation and diagnostics

**Stage:** Answer grounding implementation

First create regression tests reproducing the failures, then implement minimal fixes.

**Priority 1 — Complete provisions**
Preserve relevant rules and their conditions, exceptions, approval authorities and deadlines in the answer context without arbitrarily enlarging it. Keep IDs, pages and citation mappings. Test the complete B11.4 provision, including AAC discretion.

**Priority 2 — Factual validation**
Validate against the exact sent excerpts. Reject uncited factual claims, invented consequences and swapped thresholds. Check numerical values with their conditions/meanings, not number presence alone. Apply the same checks to cached answers and preserve safe abstention.

**Priority 3 — Diagnostics**
Add explicitly opt-in local logs for exact prompts, ordered excerpts, mappings, selection/trimming decisions, raw rejected answers and individual failure reasons. Never log keys, credentials, authorization headers or workspace capabilities. Default to disabled.

Regression coverage: correct 80%/75% answer; missing AAC discretion; fabricated 60%; swapped conditions; coursework penalties; uncited claims; cached unsupported answers; HyDE isolation; cross-workspace isolation.

Do not re-index, regenerate embeddings, modify live databases/institutional data, change providers, make unnecessary LLM calls or weaken existing protections. Run tests and the full suite. Report exact results, every modified file and remaining limitations.

### 31. Prepare a company-facing prompt register

**Stage:** Project documentation

Create a file named `codex_primpt.md` listing all the user’s prompts in a clear, professional structure suitable for submission to the company. Keep the writing natural rather than generically AI-styled.

Original message: “now just prepae a file names codex_primpt .md and list all the pormpts i gave in a good way ..bcoz company needs this also and it should not like all ai generated but should be in a good strucuted way how a copany expects”

### 32. Remove scripted results and assess prototype reliability

**Stage:** Prototype integrity and assessment

The user explained that time pressure led to hardcoded question/answer outputs for Raw RAG, HyDE and Fusion, as well as document comparison. Remove these shortcuts first, investigate why the real features were not working properly, and give an honest assessment of the prototype's current strength, outstanding issues and how to fix them.

This is an edited record of the request, not a claim that real-model reliability has been demonstrated.

---

## Appendices — full attached instructions

The sections below preserve the attached requests rather than substituting an assistant-written summary. Expand each brief in Markdown viewers that support collapsible sections. These are historical instructions, not new commands to execute.

### Appendix A. Master build instruction

<details>
<summary>Full user-supplied brief</summary>

# MASTER BUILD INSTRUCTION — CAMPUS POLICY DISCOVERY PLATFORM

## 1. Your role and objective

Act as a senior full-stack engineer, AI engineer and software architect.

You are working on an existing application called Campus Policy Discovery Assistant.

Your task is to transform it into a fully working, institution-independent **AI-Powered Campus Policy Discovery Platform**.

This is an implementation task, not an architecture-planning task.

Read these documents completely before making changes:

- `PS1_BUILD_GUIDE.md`
- `ARCHITECTURE_AUDIT.md`
- `docs/SOURCE_REVIEW.md`
- `MULTI_INSTITUTION_IMPLEMENTATION_PLAN.md` (or the latest institution implementation plan in the project)

Also inspect the complete existing codebase before modifying it.

I explicitly approve the proposed multi-institution architecture and staged migration approach. Start implementation immediately. Do not stop after presenting another plan or ask me to approve each phase.

## 2. Product vision

The application must work with documents from ANY college or university.

MS Ramaiah Institute of Technology (MSRIT) is our first demonstration institution only. It must not be hardcoded as the default institution or restrict the platform to MSRIT.

The intended user journey:

1. An authorised administrator creates an institution workspace.
2. The administrator uploads that institution's regulations, handbooks, examination policies, academic calendars and other documents.
3. Documents are extracted and indexed.
4. Every document remains pending until its authenticity, source and applicability are reviewed.
5. Approved documents enter that institution's isolated knowledge base.
6. Students select their institution.
7. Students ask questions in natural, informal language.
8. The AI uses HyDE + RAG to retrieve the relevant institutional policies.
9. Answers contain supporting passages, citations, applicable conditions and source documents.
10. When evidence is insufficient, the assistant abstains instead of inventing permissions.

The product must be designed around trust, institutional isolation and explainable answers.

## 3. Existing functionality — preserve it

Do not discard or casually rewrite working modules.

The existing application already contains:

- FastAPI backend.
- Vanilla JavaScript frontend.
- FastEmbed using BAAI/bge-small-en-v1.5.
- ChromaDB.
- Groq LLM integration using GPT-OSS 120B.
- Optional Gemini provider adapter.
- HyDE generation.
- Raw, HyDE and fusion retrieval.
- Reciprocal Rank Fusion.
- Grounded answer generation.
- Citation validation.
- Abstention.
- Source-authority registry.
- Hash-bound document approvals.
- Decoy and synthetic-data isolation.
- Incremental indexing.
- Cache validation and invalidation.
- Benchmark runner and dashboard.
- Source inspection and management.
- Automated regression tests.

Preserve all working behaviour unless an actual technical incompatibility requires a change.

Do not replace the existing technology stack with LangChain, LlamaIndex, Kafka, Redis, Pinecone or other unnecessary infrastructure.

## 4. Implement the institution architecture

### 4.1 Institution registry

Create an institution registry with:

- Server-generated immutable `institution_id`.
- Institution display name.
- Unique slug.
- Active/disabled status.
- Publication status.
- Creation timestamp.

Use a structure similar to:

```text
data/
├── institutions.json
└── workspaces/
    └── <institution_id>/
        ├── raw/
        ├── processed/
        │   ├── source_registry.json
        │   ├── manifest.json
        │   ├── answer_cache.json
        │   └── hyde_cache.json
        └── bench/
            ├── test_queries.jsonl
            └── results/
```

Create an explicit institution context that resolves all workspace paths.

Never change global directory variables per request.

### 4.2 Initial MSRIT workspace

Create one demonstration workspace:

Display name: Ramaiah Institute of Technology

Slug: `msrit`

Its institution ID must be generated by the system.

Assign the existing MSRIT document collection to this workspace through the explicit migration process.

Important distinctions:

- Workspace ownership does not mean source authenticity has been verified.
- Keep all existing source approval statuses pending.
- Do not publish the institution automatically.
- Do not approve documents based on their filenames or branding.
- Do not treat any MSRIT policy as applicable to another institution.

The product logic must remain fully institution-independent.

### 4.3 Institution-specific document storage

Each uploaded document must belong to a validated institution.

Implement:

- Unique document IDs.
- Version IDs tied to SHA-256 hashes.
- Original filename preservation.
- Safe file storage.
- Upload-size and file-type validation.
- Atomic file writes.
- Pending status by default.
- Extraction and indexing status.
- Source provenance.
- Issuing authority.
- Applicability information.
- Effective date, including an explicit unknown state.
- Reviewer identity and review notes.

Replacing a document must preserve its previous version and review history.

A replacement must become pending and must not silently retain the old version's publication status.

Retain the current bounded embedding batches and rollback behaviour.

## 5. Enforce institution isolation everywhere

This is the highest-priority architectural requirement.

Add `institution_id` to:

- Source registry records.
- Document identities.
- Chunk identities.
- ChromaDB metadata.
- Indexing and manifest records.
- Retrieval results.
- Citation provenance.
- Answer-cache keys.
- HyDE-cache keys.
- Benchmark datasets.
- API requests.
- Dashboard state.

Use the identity scheme:

```text
institution_id
+ document_id
+ version_id
+ section
+ chunk_index
```

### Mandatory retrieval filtering

Every production retrieval path must require an institution context:

- Raw retrieval.
- HyDE retrieval.
- Fusion retrieval.
- Fallback retrieval.
- Confidence checking.
- Citation validation.
- Cache lookup.

The production candidate set must satisfy ALL of these:

1. Matches selected institution.
2. Document is approved.
3. Version is current.
4. File hash matches approved registry entry.
5. Document is not a decoy.
6. Document is not synthetic.

Apply these restrictions before ranking.

Additional user-supplied filters must never weaken the institution restriction.

Never silently fall back to a global knowledge base.

Missing or invalid institution selection must return a validation error.

An institution with no approved policy evidence must return a safe abstention.

Internal evaluation may use test fixtures, but it must never bypass institution isolation.

Student-facing API requests must not be able to enable evaluation mode.

## 6. Institution-specific caches and citations

Separate answer and HyDE caches by institution.

A question asked by a student from College A must never reuse an answer or HyDE cache entry from College B.

Before serving a cached answer:

- Verify institution ownership.
- Verify current document version.
- Verify current source approval.
- Verify source and chunk fingerprints.
- Verify every citation belongs to the selected institution.

Cache clearing and document updates must affect only the relevant institution.

Preserve `[C1]`, `[C2]` citation formatting, but include full document and institution provenance internally.

Validate citation ownership before and after answer generation and on cache hits.

## 7. Build the complete administrator workflow

Create a working administrator interface.

Required workflow:

```text
Create institution
      ↓
Upload document
      ↓
Register pending source
      ↓
Extract text
      ↓
Chunk and embed
      ↓
Inspect original document and extracted chunks
      ↓
Review source authority and applicability
      ↓
Approve / Keep Pending / Reject
      ↓
Publish eligible knowledge base
```

The administrator must be able to:

- Create institutions.
- View existing workspaces.
- Upload multiple PDFs.
- See upload and indexing progress.
- View extraction failures.
- Inspect full extracted text.
- Inspect document chunks with page and section references.
- View source hashes.
- Record source URL and issuing authority.
- Record programme, cohort and effective-date applicability.
- Approve or reject a specific document version.
- Reindex or remove a document within the selected institution.
- View institution-specific indexing statistics.

All administrative mutation endpoints must require server-side authentication and institution-scoped authorisation.

For the local MVP, a simple authenticated administrator using a server-side `ADMIN_API_TOKEN` is sufficient.

Never expose administrative credentials in static JavaScript, URLs or logs.

Students must not receive administrative privileges.

Do not build an elaborate enterprise authentication system.

## 8. Build the complete student experience

Create a polished, professional application.

The frontend should have the following views.

### A. Landing page

- Product name: Campus Policy Discovery.
- Short explanation of what it does.
- Institution selector.
- Clear student/admin entry points.
- Clean, professional visual design.

### B. Student chat

After choosing an institution:

- Chat interface.
- Example question suggestions.
- Natural-language question input.
- Loading indicators.
- Clear source citations.
- Expandable policy excerpts.
- Document and page references.
- Conditional permission explanations.
- Safe abstention messages.
- Clear indication of which institution is being queried.

Do not show MSRIT-specific text as a universal product feature.

### C. Explainability / retrieval panel

Show:

- Original question.
- HyDE-generated hypothetical search passage.
- Raw query retrieval.
- HyDE retrieval.
- Fusion ranking.
- Retrieved policy excerpts.
- Source verification status.
- Cosine similarity.
- Separate RRF ranking score.
- Confidence/abstention decision.
- Provider used.
- Stage-wise latency.

Explicitly label HyDE text as a search aid, not authoritative policy.

Never pass hypothetical HyDE content into the final answer-generation prompt.

### D. Compare view

Show raw-query retrieval against HyDE retrieval side by side.

Highlight relevant verified policy passages when the query has a verified benchmark label.

### E. Benchmark dashboard

Display actual benchmark results only.

Include:

- Recall@1.
- Recall@3.
- Recall@5.
- MRR.
- Abstention accuracy.
- Answer/citation grounding checks.
- Retrieval latency.
- HyDE latency overhead.

If labels are unverified or the corpus is unavailable, display an honest blocked state.

Never display invented zero scores as measured performance.

### F. Institution administrator dashboard

Show:

- Institution details.
- Number of uploaded documents.
- Pending documents.
- Approved documents.
- Rejected documents.
- Extraction failures.
- Indexed chunk count.
- Recent indexing activity.
- Document review interface.

### UX requirements

- Responsive desktop and mobile layout.
- Consistent visual language.
- Good typography and spacing.
- No broken navigation.
- Working empty states and error messages.
- Safe DOM rendering; never inject untrusted document text as HTML.
- No decorative controls that do nothing.

## 9. Backend API changes

Implement institution-aware versions of existing endpoints.

At minimum:

Public/student:
- `GET /institutions`
- `POST /ask`
- `POST /compare`
- Institution-scoped source/citation retrieval.
- `GET /health`

Administrator:
- `POST /admin/institutions`
- `GET /admin/institutions`
- `POST /admin/institutions/{institution_id}/documents`
- `GET /admin/institutions/{institution_id}/sources`
- `GET /admin/institutions/{institution_id}/sources/{document_id}`
- `POST /admin/institutions/{institution_id}/sources/{document_id}/approve`
- `POST /admin/institutions/{institution_id}/sources/{document_id}/reject`
- `POST /admin/institutions/{institution_id}/reindex`
- Institution-scoped benchmark endpoints.

Use the existing coding conventions and request validation style.

Do not leave any student-facing or administrative route capable of accessing another institution's records.

Document the new API contracts.

## 10. Non-destructive migration of existing MSRIT data

This is a critical data-preservation task.

Before migration:

1. Stop indexing and application writers.
2. Inventory the current source registry, manifests, cache, PDFs, ChromaDB collection and vector counts.
3. Record SHA-256 hashes.
4. Create a recoverable backup.
5. Generate a migration mapping.

Expected audited baseline:

- 10 MSRIT PDFs.
- 7 successfully indexed real documents.
- 517 real-document chunks.
- 3 documents with extraction failures.
- 4 synthetic evaluation-decoy chunks.
- All real sources pending approval.

Recount the actual state before acting. These are expected figures, not hardcoded assumptions.

### Migration rules

- Create the MSRIT workspace explicitly.
- Copy original PDFs into its workspace.
- Preserve all ten source records as pending.
- Preserve the three extraction failures as pending/failed; do not fabricate chunks.
- Preserve the 517 existing vectors and text.
- Reuse existing vectors only if embedding-model provenance and vector compatibility are established.
- If provenance cannot be established, pause the vector migration decision rather than silently re-embedding or relabelling.
- Preserve four decoy vectors separately as evaluation fixtures, never as production evidence.
- Start new institution-specific caches empty.
- Preserve old benchmark labels as unverified.
- Keep the legacy data and ChromaDB state untouched.

Use a parallel staged collection and workspace.

Perform:

1. Inventory.
2. Backup.
3. Workspace creation.
4. Staged copying.
5. Vector migration.
6. Count/hash/status comparison.
7. Isolation tests.
8. Cutover to the new scoped storage.
9. Retain original legacy state for rollback.

Never delete or reset the old ChromaDB collection as part of migration.

If a count, hash, ownership mapping or approval status differs unexpectedly, abort cutover and report the discrepancy.

The three PDFs with zero text extraction must remain visible failures. Do not implement OCR in this task.

## 11. Automated testing — mandatory

Preserve the existing regression suite.

Add two-institution isolation tests using synthetic temporary fixtures only.

Test:

1. Same filename uploaded to two institutions creates different identities.
2. Same query returns only the selected institution's policy.
3. Foreign high-similarity chunks never enter candidate retrieval.
4. Raw retrieval enforces institution scope.
5. HyDE retrieval enforces institution scope.
6. Fusion retrieval enforces institution scope.
7. HyDE failure fallback remains institution-scoped.
8. Cache for institution A cannot be used by institution B.
9. Foreign citations are rejected.
10. Pending/rejected sources remain unavailable to students.
11. Approval in A does not grant approval in B.
12. Reindexing A does not alter B.
13. Replacing a document in A does not alter B.
14. Clearing A's cache does not affect B.
15. Unknown or missing institution returns an error.
16. Additional client filters cannot bypass tenant scope.
17. Administrative mutations cannot target foreign-owned documents.
18. Switching institution in the UI clears old sources and traces.
19. Late responses from the previous institution cannot appear in the new institution view.
20. Interrupted migration can be safely rerun without duplicate records or data loss.
21. Decoys and synthetic fixtures remain excluded from production.
22. Benchmark labels stay institution-scoped and unverified until manually confirmed.

Also retain tests for:

- HyDE structural isolation.
- Prompt injection.
- Citation checks.
- Confidence gate.
- Fusion scoring.
- Cache fingerprints.
- Incremental indexing.
- Rollback.
- Provider retries and timeouts.
- API validation.
- Dashboard functionality.

Run the full suite after implementation.

## 12. Documentation

Update:

- `README.md`
- `DECISIONS.md`
- `PROMPTS.md`
- `INTERVIEW_NOTES.md`
- `docs/SOURCE_REVIEW.md`
- New architecture documentation.
- API documentation.
- Migration report.
- Local setup guide.

Document:

- How to create institutions.
- How administrators upload and approve documents.
- How students select their college.
- How institution isolation works.
- How to run the application.
- How to run tests and benchmarks.
- Which features are implemented and which remain future work.

Do not fabricate benchmarks, policy sources, test outcomes or completed functionality.

## 13. Implementation execution rules

Implement in these phases:

Phase 1 — Institution registry, context and workspace storage.

Phase 2 — Institution-aware sources, IDs, metadata, indexing and retrieval.

Phase 3 — Cache, citation and answer isolation.

Phase 4 — Administrator API and document-management interface.

Phase 5 — Student frontend, institution selector and chat experience.

Phase 6 — Benchmark scoping and full regression suite.

Phase 7 — Non-destructive MSRIT migration and validation.

Phase 8 — Documentation and final polish.

Proceed autonomously through these phases. Do not stop after writing another plan.

At each phase:
- Implement the functionality.
- Run relevant tests.
- Fix failures.
- Preserve working functionality.
- Continue to the next phase.

Do not ask me to approve every small decision. Make sensible engineering decisions and record them in `DECISIONS.md`.

If a genuine destructive, security-sensitive or data-ownership ambiguity occurs, stop that specific operation, preserve existing data and report the blocker. Continue with independent implementation work.

Do not start a second parallel indexing process.

Do not add optional infrastructure or features outside this scope.

## 14. Definition of done

The work is complete only when:

- A new institution can be created.
- An authorised administrator can upload its documents.
- Documents begin in pending status.
- Source inspection and approval work.
- Multiple institutions can coexist.
- Every retrieval path enforces institution isolation.
- Different institutions cannot share cached answers or citations.
- A student can select an institution and use the assistant.
- HyDE, raw and fusion retrieval remain functional.
- Answers are grounded in approved institutional documents.
- Unsupported questions safely abstain.
- Admin operations are institution-scoped.
- Benchmark results are scoped and honest.
- The existing MSRIT dataset is migrated without data loss or automatic approval.
- Two-institution isolation tests pass.
- Existing regression tests pass.
- The application starts and works through the browser.
- Documentation accurately describes the implemented system.

At completion provide:

1. Final architecture summary.
2. Modified and newly created files.
3. Implemented features.
4. Migration results and data-preservation checks.
5. Full test results.
6. Exact run commands.
7. Remaining limitations or blockers.

START IMPLEMENTATION NOW. Do not return another plan instead of building the application.

</details>

### Appendix B. Critical UI and end-to-end functionality fix

<details>
<summary>Full user-supplied brief</summary>

# CRITICAL UI + END-TO-END FUNCTIONALITY FIX — CAMPUS POLICY DISCOVERY PLATFORM

You have already implemented the multi-institution backend. However, the current browser interface is confusing and does not expose the product's core workflow clearly.

The current application shows:
- One institution workspace in the service status, but an empty student institution selector.
- An empty student workspace.
- An administrator panel that initially only shows an authentication field.
- No obvious document-upload workflow.
- No clear evidence to the user that RAG, HyDE, retrieval, citations and answer generation are functioning.

I need you to fix this in the actual application, not just explain what should be changed.

## 1. Inspect before modifying

Inspect the existing implementation, especially:
- `web/index.html`
- `web/app.js`
- `src/server.py`
- `src/institutions.py`
- `src/documents.py`
- `src/ingest.py`
- `src/retrieve.py`
- `src/hyde.py`
- `src/pipeline.py`
- `src/answer.py`
- `src/store.py`
- `src/authority.py`
- `src/cache.py`

Read the implementation report, setup guide and API documentation.

Identify exactly why:
1. The institution selector is empty despite one existing workspace.
2. The existing MSRIT workspace is not accessible through the administrator workflow.
3. Upload and document-review controls are not visible.
4. The student workspace appears empty.

Do not guess. Trace the actual API responses and frontend rendering conditions.

## 2. Build a proper institution onboarding workflow

The application must support any college or university.

The administrator should be able to:

1. Unlock administration using the existing secure administrator token.
2. See all institution workspaces, including unpublished ones.
3. Create a new institution by entering its name.
4. Select an existing institution.
5. View its publication status, document count, approved count, pending count and failed extraction count.

The existing MSRIT demonstration workspace must be accessible to the administrator even though it is unpublished.

Do not create duplicate MSRIT workspaces.

Do not make MSRIT the hardcoded default institution.

## 3. Make document upload obvious and functional

Once an administrator selects a workspace, show a clearly visible document-management section.

It must include:

- Drag-and-drop PDF upload.
- Browse files button.
- Multiple PDF upload support.
- Upload progress.
- Extraction and indexing status.
- Reindex button where appropriate.
- List of uploaded documents.
- Pending, approved, rejected and extraction-failed status.
- Document details and original-file preview.
- Extracted text and chunks with page references.
- Document hash and version information.
- Issuing authority, official URL and effective-date review fields.

The workflow must be:

Upload → Extract → Chunk → Embed → Store → Review → Approve → Publish.

All newly uploaded documents must remain pending until a human explicitly reviews and approves them.

Never auto-approve documents.

Preserve document version history and existing migration data.

## 4. Make the student workflow clear

The student landing page should have a clear sequence:

**Step 1:** Select your college/university.

**Step 2:** Enter the student workspace.

**Step 3:** Ask a question about institutional policies.

**Step 4:** Receive an evidence-backed answer with citations.

The student should see:
- Selected institution name.
- Question input.
- Example policy questions.
- Retrieval mode selector (Raw, HyDE, Fusion, if supported).
- Answer area.
- Citations with source names and page references.
- Retrieved evidence/excerpts.
- Retrieval confidence or abstention explanation, where supported.
- Trace/explainability information.

If no approved documents exist, show a clear message:

"No verified institutional policies are currently available for this institution. Please contact your institution administrator."

Do not show an empty chat interface that gives the impression that the application is broken.

Unpublished institutions must remain hidden from students.

## 5. Verify the actual RAG pipeline

Do not merely claim that RAG works because the code contains retrieval functions.

Trace and verify the actual execution path:

Student question
→ Institution validation
→ Query processing
→ HyDE generation (when selected)
→ Local query embedding
→ Institution-filtered ChromaDB retrieval
→ Approved/current source filtering
→ Confidence threshold
→ Context construction from real retrieved chunks
→ Groq answer generation
→ Citation validation
→ Final answer and trace.

Verify that:
- HyDE text is used only as a retrieval search key.
- The final answer model receives the original question and retrieved real document evidence.
- Generated HyDE text is never treated as authoritative evidence.
- Retrieval cannot return documents from another institution.
- Pending, rejected, decoy and synthetic sources never enter student-facing production retrieval.
- Unsupported questions result in abstention.
- Citations resolve to actual source chunks and correct pages.
- Cache hits revalidate source eligibility.

Preserve existing Raw, HyDE and Fusion behavior.

## 6. Add a real end-to-end verification procedure

Run the application and test the workflows through actual API requests and browser interactions where possible.

Test:
1. Administrator authentication.
2. Institution creation.
3. Existing MSRIT workspace visibility in administration.
4. PDF upload.
5. Extraction and indexing.
6. Pending source inspection.
7. Explicit approval.
8. Institution publication.
9. Student institution selection.
10. Student question submission.
11. Retrieval of actual approved document chunks.
12. Answer generation through Groq.
13. Citation correctness.
14. Unsupported-question abstention.
15. Institution isolation.

Use existing documents and synthetic fixtures only where appropriate. Never fabricate a successful real-policy answer.

If source approval is required, do not approve existing MSRIT documents on my behalf. Keep them pending and demonstrate the workflow using clearly identified synthetic test fixtures in isolated test workspaces.

## 7. Improve the visual design

Keep the existing dark theme, but make the application look like a polished enterprise product.

Use:
- Clear section hierarchy.
- Proper spacing and alignment.
- Consistent cards and buttons.
- Visible workflow steps.
- Useful empty states.
- Clear loading and error states.
- Responsive layouts.
- Distinct student and administrator experiences.

The landing page should immediately explain what the platform does.

Do not overcrowd the page with technical disclaimers.

## 8. Preserve existing functionality and data

Critical restrictions:
- Do not reset ChromaDB.
- Do not delete existing documents.
- Do not change existing source approval states.
- Do not modify the Groq API key.
- Do not expose the administrator token.
- Do not weaken institution isolation.
- Do not remove existing HyDE, Fusion, caching, citation validation or benchmark functionality.
- Do not hardcode MSRIT into the architecture.
- Do not fabricate benchmark accuracy.
- Do not replace real retrieval with hardcoded responses.

Run the complete existing test suite after your changes and add regression tests for any bugs discovered.

## 9. Final deliverables

When finished, provide:

1. Root cause of the empty institution selector.
2. Root cause of the inaccessible upload workflow.
3. Files changed and why.
4. Actual working administrator workflow.
5. Actual working student workflow.
6. Evidence that the RAG pipeline executes end-to-end.
7. Test results.
8. Remaining limitations.

Most importantly, I want to open localhost:8000 and immediately understand how to create/select an institution, upload its documents, review them and use the policy assistant.

Do not stop after writing another plan. Implement, test and verify the fixes in the existing project.

</details>

### Appendix C. Student-first product redirection

<details>
<summary>Full user-supplied brief</summary>

# PRODUCT REDIRECTION: BUILD A STUDENT-FIRST CAMPUS POLICY INTELLIGENCE PLATFORM

You have already implemented a multi-institution Campus Policy Discovery application with FastAPI, ChromaDB, FastEmbed, Groq, HyDE, RAG, Fusion retrieval, citations, caching, institution isolation and an administrator document-management workflow.

I want to rethink the product experience. This is a product-direction change, not just a UI redesign. The current application is too administrator-centric: a student cannot use it until an institution is created, approved and published. The primary product must be useful to an individual student immediately.

Your job: inspect the existing architecture, then implement the best version of this idea while preserving valuable existing functionality. Do not just write a plan. Implement, test and verify.

Everything runs on localhost:8000. No deployment, Docker or hosting work.

====================================================================
0. HOW TO WORK
====================================================================
- Inspect the current code first. Identify what can be reused, what must change. Do not unnecessarily rewrite working components.
- Build in these phases, in order:
  Phase 1: personal workspace + upload + RAG with citations and abstention
  Phase 2: rule extraction + student-specific eligibility analysis
  Phase 3: policy conflict detection
  Phase 4: frontend redesign around the student workflow
  Phase 5: policy version comparison
- After each phase: run the full test suite, start the app on localhost, and confirm the app still loads and all earlier phases still work.
- Continue automatically to the next phase if tests pass. STOP and report only if a phase still fails after 2 fix attempts, or if a change would touch protected data (Section 8).
- If time runs short, drop phases in this order: Phase 5, then Phase 3. Never drop Phases 1, 2 or 4.
- Do not claim a feature works unless you actually tested it. At the end, report per phase: what was built, tests run, and what was NOT verified.
- Work autonomously and make sensible technical decisions. Do not sacrifice correctness for a visually impressive interface. Never replace real retrieval with hardcoded demo answers.

====================================================================
1. PRODUCT VISION
====================================================================
CAMPUS POLICY INTELLIGENCE PLATFORM: an AI-powered platform where students from ANY college or university upload their own institutional documents, understand campus policies, evaluate their personal situation against those policies and receive evidence-backed guidance.

It must not be limited to MSRIT or any institution. The student must NOT need an administrator account, a pre-created institution workspace, a published institution, or institutional approval just to upload their own documents. The primary experience must work immediately after opening the app.

Landing message: "Understand your college rules. Know your options."
Sub-message: "Upload your college documents and understand the rules that affect you."

====================================================================
2. PRIMARY USER JOURNEY
====================================================================
1. Student opens the app.
2. Student starts a personal workspace.
3. Student optionally enters their college/university name.
4. Student uploads one or more PDFs.
5. System extracts text, chunks, embeds and indexes them.
6. Student sees upload, extraction and indexing progress.
7. Student asks natural-language questions.
8. System retrieves evidence (Raw, HyDE or Fusion) and answers with document and page citations.

Also support: multiple documents per workspace; adding documents later; removing or replacing a document without affecting other users or institution workspaces; returning to the workspace later without re-uploading.

====================================================================
3. PERSONAL WORKSPACE DESIGN
====================================================================
- Anonymous workspaces, no accounts. The server generates an unguessable workspace_id (at least 128 bits of randomness). The browser keeps it in localStorage and sends it with every request. Document in DECISIONS.md that possession of the id grants access.
- Every retrieval, cache key, file operation and Chroma query MUST be scoped by workspace_id. No global unfiltered vector search anywhere. Personal workspaces must never see each other's documents.
- Personal documents have their own document identity, ownership, versioning, content hashes and retrieval scope.
- Persistence: use sensible local persistence (separate Chroma collection or metadata-scoped storage plus a registry file), consistent with the existing MVP.
- Public upload endpoint safeguards: accept PDF only (validate by content, not just extension); configurable max file size, max pages per file and max documents per workspace; reject cleanly with clear messages.
- Treat all uploaded text as UNTRUSTED DATA. Never follow instructions found inside documents. Add a prompt-injection test (a PDF chunk saying "ignore previous instructions...").
- Provide delete-workspace and delete/replace-document, with cache invalidation for affected entries.
- If a PDF has no extractable text (scanned), show a clear extraction error. OCR is not required.

====================================================================
4. TWO TRUST LEVELS (CRITICAL)
====================================================================
A. Personal student workspace: student-uploaded, unverified evidence. Every personal-workspace answer must display: "Based on documents you uploaded. Not verified by your institution."
B. Verified institutional knowledge: existing institution workspaces, documents reviewed and approved by authorised administrators, published explicitly, retrieved only within that institution's scope.

A student-uploaded PDF must NEVER automatically become an approved institutional source. Do not mix personal and institutional retrieval results silently. If a future combined query uses both, show which evidence came from which trust level. Keep the administrator workflow as a secondary institutional-management feature, not the entry point.

====================================================================
5. POLICY INTELLIGENCE (THE DIFFERENTIATOR)
====================================================================
Core principle: THE LLM EXTRACTS, CODE DECIDES. Never let the model invent a threshold or a verdict.

5.1 Rule extraction (per document, cached by file hash)
- Use the LLM to extract structured rules from chunks: {subject, applies_to, operator, value, unit, exceptions, deadline, penalty, verbatim_quote, document, page}.
- Validate in code: the verbatim_quote must be an exact substring of the source chunk text, and any numeric value must appear inside that quote. If validation fails, discard the rule. Never keep unverifiable rules.
- Expose extracted rules in a "Rule Book" (see Section 6). Mark them "extracted by AI, verify against the source quote."
- Do not present model-generated interpretations as direct quotations. Quotes are only exact source text.

5.2 Student-specific eligibility analysis
Example: "I have 78% attendance, 42 internal marks and one backlog. What restrictions apply to me?"
Pipeline:
1. Retrieve relevant chunks and extracted rules (attendance, examination, progression, etc.).
2. Parse the student's stated facts into structured fields and SHOW them for confirmation or editing.
3. Match facts to extracted rules.
4. Compare numerically in plain deterministic code (NO LLM) and produce per-condition status: satisfied / not satisfied / insufficient evidence.
5. Ask for missing facts where needed.
6. Only then use the LLM to write a step-by-step explanation from those computed results, citing every important conclusion.
7. Overall verdict: eligible / ineligible / insufficient evidence. Abstain when no matching rule exists.
Do not invent formulas. Do not assume all colleges share rules; derive everything from the student's uploaded documents.

5.3 Policy conflict detection
- Compare extracted rules ACROSS documents grouped by subject (not whole-document pairwise LLM comparison).
- Report a "possible conflict" only when the subject matches and the values differ.
- Show both quotes, document names, page numbers, dates and issuing authority if available, and whether they may apply to different programs, batches or situations.
- Explain why the conflict cannot safely be resolved without additional evidence. NEVER assume the newest-looking document is authoritative. Never pick a winner.

5.4 Policy version comparison (lowest priority)
- When a new circular or regulation is uploaded, diff its extracted rule table against an earlier document/version: additions, removals, modifications, changed requirements and dates, potentially affected rules. Cite old and new passages. Do not claim a change is official or applicable unless the source supports it.

5.5 Explainable evidence
For every important conclusion expose: document name, page number, retrieved passage, the rule or condition used, the reasoning connecting evidence to the conclusion, missing evidence and uncertainty.

====================================================================
6. FRONTEND REDESIGN
====================================================================
- Navigation: Home, My Documents, Rule Book, Ask & Analyse, Policy Conflicts, Document Changes. Secondary: Advanced (Compare Retrieval, Benchmark) and Institution Admin.
- Home: prominent landing message, upload button, drag-and-drop PDF area, supported-file info, example questions, processing status, workspace/document count.
- My Documents: per document show name, extraction status, page count, chunk count, indexing status, extraction errors, remove/replace.
- Ask & Analyse: natural-language questions; retrieval mode selector (Raw / HyDE / Fusion) tucked into an advanced toggle; student-facts panel for eligibility analysis.
- IT MUST NOT LOOK LIKE A BASIC CHATBOT. Render answers as structured result cards, not chat bubbles:
  - verdict badge (eligible / ineligible / insufficient evidence / abstained)
  - conditions table: rule | your value | required | status | source + page
  - evidence quote block with document and page
  - trust badge ("Based on documents you uploaded. Not verified by your institution.")
  - expandable trace: HyDE-generated text (labelled "search key only, not shown to the answer model"), retrieved chunks with scores, cache hit/miss, stage timings
- Rule Book page: all extracted rules in the workspace, filterable by document and subject, each with quote, page, and flagged conflicts.
- Compare Retrieval (raw vs HyDE side by side) and Benchmark remain working under Advanced. They are part of the evaluation criteria, so they must not break.
- Clear empty states, error states and loading states. Plain HTML/CSS/vanilla JS is fine. Clean and readable beats flashy.

====================================================================
7. PRESERVE AND REUSE
====================================================================
FastAPI backend, FastEmbed embeddings, ChromaDB, Groq integration, HyDE, Raw retrieval, Reciprocal Rank Fusion, confidence gating, citation validation, answer and HyDE caching, institution isolation, source versioning, incremental ingestion and rollback, existing guardrails and abstention.
Core guardrail that must keep holding: HyDE text is a search key only and never appears in the answer model's prompt. Personal-workspace scope must be mandatory in raw, HyDE, fusion, fallback and cache paths.

====================================================================
8. PROTECTED DATA (DO NOT VIOLATE)
====================================================================
The existing MSRIT workspace has 10 source records, 517 real chunks, 4 isolated decoy chunks, 3 extraction failures, and all 10 real documents pending approval. Preserve it exactly:
- Do not approve the existing sources or publish MSRIT.
- Do not delete or reset ChromaDB, registries or manifests; do not delete existing documents.
- Do not read, print, log or modify the existing administrator token or Groq API key.
- Keep the three extraction failures visible.
- Do not weaken institution isolation.
- Do not mix personal documents with institutional sources.
- Do not fabricate benchmark labels, results, accuracy figures or policy facts.

====================================================================
9. REAL DATA, FIXTURES AND BENCHMARK
====================================================================
- The demo and benchmark must work inside a PERSONAL workspace so I can upload real MSRIT PDFs there for demonstration without approving the institution workspace.
- I will supply and verify benchmark labels by hand. Do not generate labels or numbers. Benchmark script must read my labelled file and report Recall@1/3/5, MRR and abstain accuracy for raw vs HyDE vs fusion, with HyDE outputs cached so reruns are cheap.
- For testing conflicts and version comparison, create clearly labelled SYNTHETIC fixtures (filenames and visible text marked "SYNTHETIC TEST FIXTURE"). Never present synthetic policies as real college rules, in the UI or the demo.

====================================================================
10. END-TO-END VERIFICATION (actually run these)
====================================================================
1. Open the app without admin authentication; start a personal workspace.
2. Upload a PDF; real extraction, embeddings, Chroma storage.
3. Ask a question; run Raw, HyDE and Fusion retrieval.
4. Generate an answer with Groq; validate citations and page numbers.
5. Unsupported question -> abstention.
6. Upload multiple documents and retrieve across them.
7. Verify workspace isolation (workspace A cannot see, cite, cache-hit or mutate workspace B's data; personal cannot touch institution data).
8. Replace/remove a document and verify cache invalidation.
9. Prompt-injection document does not change behavior.
10. Eligibility analysis on a synthetic fixture: facts parsed, conditions computed in code, verdict correct, missing facts requested, no-rule case abstains.
11. Rule-extraction validation: a fabricated quote or number is rejected.
12. Conflict detection on deliberately conflicting synthetic fixtures; no winner is picked.
13. Version comparison on synthetic old/new fixtures (if Phase 5 is reached).
14. Upload limits and non-PDF rejection.
15. Full regression suite passes, including previous institution-workspace tests, Compare Retrieval and Benchmark.
Also exercise the UI flows through the running app on localhost where possible, and state clearly anything not visually verified.

====================================================================
11. DOCUMENTATION AND PROMPT LOG (MANDATORY)
====================================================================
- Update the Mermaid architecture diagram, DECISIONS.md and README (setup and run steps).
- Append every in-app prompt and each revision (HyDE, rule extraction, eligibility explanation, answer) to PROMPTS.md with its purpose and what changed. This is a required submission deliverable.
- Record chosen thresholds, assumptions and anything not verified in DECISIONS.md.

====================================================================
12. FINAL REPORT
====================================================================
At completion provide: architecture changes; features implemented per phase; files changed; actual test results; live RAG verification results; known limitations; exact steps to demonstrate the app on localhost (a short click-by-click demo script ending with the Rule Book, an eligibility analysis, a conflict and an abstention).

When I open localhost:8000, I should see a product that immediately makes sense: "Upload your college documents. Ask questions. Understand the rules. Find out what applies to you." The differentiator must be policy intelligence, not another PDF chatbot.

</details>

### Appendix D. UI, evidence quality and demo readiness

<details>
<summary>Full user-supplied brief</summary>

# NEXT BUILD ROUND: UI FIXES, EVIDENCE QUALITY AND DEMO READINESS FOR THE DELL PROTOTYPE

The student-first Campus Policy Intelligence Platform from the previous round is working (personal workspaces, scoped RAG, Rule Book, eligibility analysis, conflicts, version comparison; 257 tests passed). I reviewed it in a browser and found UI and evidence-quality problems. This round makes it a polished, defensible prototype for a Dell interview round. Run on localhost:8000. No deployment, Docker or hosting work.

Inspect the current code first. Do not rewrite working components. Fix, polish, then add the demo-readiness features below.

====================================================================
0. HOW TO WORK
====================================================================
- Phases A to F, in order. After each phase run the full test suite, restart the app on localhost and confirm every earlier phase still works.
- Continue automatically if tests pass. STOP and report only if a phase fails after 2 fix attempts or a change would touch protected data.
- If time runs short, drop in this order: Phase E (MCP), then Phase D (label tooling). Never drop A, B, C or F.
- FEATURE FREEZE after Phase F. Do not add anything beyond this prompt.
- Do not claim a fix works unless you tested it. If you can install Playwright/Chromium locally, use it to capture screenshots of every tab at 1440px and 390px widths and inspect them; if you cannot, say visual QA was NOT performed.
- Report per phase: what changed, tests run, what was NOT verified.

====================================================================
PROTECTED DATA (unchanged from before)
====================================================================
Do not approve or publish the MSRIT institution sources; do not delete or reset Chroma, registries or manifests; do not read, print, log or modify the admin token or Groq key; keep the 3 extraction failures visible; keep institution isolation and personal/institution separation; do not fabricate labels, benchmark numbers or policy facts. Re-verify the SHA-256 hashes of all 37 protected files at the end. Any chunking or normalisation changes apply ONLY to newly ingested or explicitly re-indexed PERSONAL documents, never to institution data.

====================================================================
PHASE A: UI BUGS AND CSS (must do)
====================================================================
A1. Navigation bar redesign
- Single compact sticky top bar (about 56 to 64px tall), consistent control heights, no tall bordered boxes.
- Left: product name "Campus Policy Intelligence". Centre or left: Home, My Documents, Rule Book, Ask & Analyse, Policy Conflicts, Document Changes. Active tab shown by an underline or subtle pill, not a tall box.
- "Advanced" is a dropdown/popover menu (Compare Retrieval, Benchmark, Evidence, Label Queries, Session Metrics), closed by default, closes on outside click and Escape, keyboard accessible.
- The scope selector ("My uploads" vs institution) moves out of the Advanced menu into a small workspace chip/switcher on the right, e.g. "Personal workspace · 3 documents".
- "Institution Admin" is a quiet text link on the far right, clearly secondary.
- On narrow screens (under about 900px) the tabs collapse into a menu button or a horizontally scrollable row. No overlap, no clipped text.
- Content must never be hidden under the sticky bar (check scroll-padding and anchors).
A2. Visual system
- Define CSS variables for colour, spacing scale, radius, font sizes. Keep the existing dark theme but fix contrast (WCAG AA for body text), line lengths (max-width about 900 to 1000px for reading content), consistent card padding, clear type hierarchy (page title, section title, label, body, caption).
- Consistent buttons: one primary style, one secondary, one quiet; visible focus rings; disabled states; loading spinners on long actions.
- Clear empty, loading and error states on every page.
A3. Render answers properly
- The answer currently shows literal markdown ("**Answer:**"). Render model output with a small SAFE renderer: HTML-escape everything first, then support only bold, italics, line breaks, simple bullet lists, and citation markers [C1] turned into clickable links to the evidence cards. NEVER insert model output or document text with innerHTML unescaped (uploaded documents and model output are untrusted). Add tests for HTML/script injection in answers and evidence.
A4. Trust footer
- The footer says "Answers cite reviewed source passages." That is wrong for personal workspaces. Make it scope-aware: personal workspace -> "Answers are based on documents you uploaded. They have not been verified by your institution."; institution workspace -> keep the reviewed-sources wording. Any other static text claiming verification must be scope-aware too.

====================================================================
PHASE B: EVIDENCE QUALITY (must do)
====================================================================
B1. Chunking and text cleaning (personal documents only)
- Chunks must never start or end mid-word (e.g. "ta storage device" from "data storage device"). Split on sentence or whitespace boundaries.
- Clean PDF extraction artefacts before embedding and display: standalone bullet characters on their own line, broken line wraps, repeated whitespace, hyphenated line breaks.
- Improve section titles: detect headings (numbered clauses, ALL-CAPS or short title-case lines followed by body text). If no heading is detected use "Page N" instead of "General".
- Provide a "Re-index this document" action for personal documents so existing personal uploads can pick up the improvements. Do not touch institution data.
B2. De-duplicate overlapping evidence
- If two retrieved chunks overlap textually or are adjacent chunks of the same document, merge them into one evidence block for both the answer context and the display, with one citation label. The user must not see the same sentence cited as C1 and C2.
B3. Quote verification (important guardrail)
- Any text the answer puts in quotation marks and attributes to a citation must be verified in code as an exact substring (after whitespace, case and quote-character normalisation) of that cited chunk. Handle "..." by verifying each segment separately.
- If a quote fails verification: remove it from the displayed answer (or regenerate once with a stricter prompt), and show a small "quote could not be verified" note. Never display an unverified string as a policy quotation.
- Verified quotes get a small "verified quote" marker. Add tests (fabricated quote, altered number, quote attributed to the wrong chunk).
- Also fix prompt wording that produces filler like "(Repeated in)". Answers should be short: a direct answer first, then the exact policy wording with citation.
B4. Evidence cards
- Show the full relevant sentence(s), not text cut mid-sentence with "...". Highlight the sentence that matched. Keep a "Full cited passage" expander. Show document name, page and section.
- If a cited chunk does not contain the claim attributed to it, that is a citation failure: abstain or drop that citation. Add a test.

====================================================================
PHASE C: DEMO READINESS (must do)
====================================================================
C1. "How it works" page (works fully offline: no CDN scripts, no external fonts or images; inline SVG)
- A clear architecture diagram: upload -> extract -> chunk -> embed -> Chroma (workspace-scoped) ; question -> cache check -> HyDE (search key only) -> retrieval -> confidence gate -> grounded answer (question + real chunks only) -> quote and citation verification -> answer or abstain. Add the rule extraction / deterministic comparison branch and the trust-level separation.
- A short plain-language caption per stage and the key design choices with trade-offs (local embeddings vs API, Chroma, extra LLM call latency vs retrieval gain, "model extracts, code decides").
- Make it readable at a glance when screen-recorded.
C2. Live pipeline trace on Ask & Analyse
- Under each answer, an expandable "How this answer was produced" panel: cache hit/miss, HyDE passage (labelled "search key only, never shown to the answer model"), retrieved chunks with scores for the chosen mode, confidence-gate decision, provider used, per-stage timings and total latency, verification results (citations verified, quotes verified).
C3. Compare Retrieval
- Make Raw vs HyDE vs Fusion side by side (top 3 each, scores, source+page) easy to find from the Advanced menu and polished enough to record. Highlight chunks that appear in one method but not the other. This is an explicit evaluation criterion: it must be reliable and clear.
C4. Freshness and cache visibility
- After upload, replace or re-index, show "Indexed in X s" per document (measured). Show cache hit/miss and cache-hit latency in the trace. Replacing a document must visibly invalidate cached answers that cited it; show a small note when that happens.
C5. Session Metrics (small card under Advanced)
- Requests this session, cache hit rate, p50 and p95 latency, provider used, abstain rate. Computed from real requests only. No placeholder numbers.
C6. Demo workspace
- A "Load synthetic demo workspace" button that creates a personal workspace from the existing SYNTHETIC fixtures (eligibility fixture, conflicting fixtures). All its documents and results must be visibly labelled SYNTHETIC TEST FIXTURE. This makes recording reliable. It must never be mistaken for real policy.
C7. Robustness
- Friendly handling for: provider rate limit or timeout (retry, fail over, then show a clear message), scanned PDF with no text, oversize file, non-PDF, lost workspace id (explain recovery limits), empty question. No raw stack traces in the UI.

====================================================================
PHASE D: BENCHMARK ASSIST (human labels only)
====================================================================
- Goal: save my time labelling. Do NOT generate gold labels or any accuracy number.
- Add bench/candidate_queries tooling that, for a chosen personal workspace, proposes 20 to 30 CANDIDATE casual student-style queries, each tied to a source chunk/page as a suggested target, written to bench/candidates.jsonl with "labels_verified": false.
- Add a "Label Queries" page under Advanced: shows one candidate at a time with the suggested source passage and page, and buttons: Correct / Wrong chunk (let me pick the right one) / Should abstain (out of scope) / Skip / Edit query text. Only human clicks create labels. Write confirmed labels to the benchmark label file in the format the existing benchmark already expects, with "labels_verified": true only for human-confirmed rows.
- Make sure the Benchmark page and bench/run_benchmark.py consume that file, run Raw vs HyDE vs Fusion, and report Recall@1/3/5, MRR and abstain accuracy, with a results table and the failure cases listed. Cache HyDE outputs so reruns are cheap and avoid provider rate limits. It must stay blocked without verified labels, as it is now.

====================================================================
PHASE E: MCP TOOL (stretch, drop if short on time)
====================================================================
- The evaluation criteria name MCP. Add a minimal local MCP server (stdio only, no network exposure) exposing a search_policies tool that runs the existing scoped retrieval for ONE personal workspace and returns chunks with source and page. Check the current official MCP Python SDK documentation before coding; do not guess the API.
- It must require a workspace id, must not expose institution data, admin features, keys or tokens, and must treat tool inputs as untrusted. Add a test. Document how to run it in the README and show it on the How it works page as an optional integration. If you cannot verify it works, say so rather than claiming it.

====================================================================
PHASE F: DOCUMENTATION AND DEMO SCRIPT (must do)
====================================================================
- Update README (setup and run in 5 commands or fewer), ARCHITECTURE.md and architecture.mmd, DECISIONS.md (thresholds, assumptions, trade-offs, what is NOT verified), INTERVIEW_NOTES.md.
- PROMPTS.md: append every in-app prompt version changed this round (answer prompt, quote-strict regeneration prompt, candidate-query prompt) with purpose and what changed.
- Write DEMO_SCRIPT.md: a click-by-click 4 to 5 minute video script with timestamps matched to the actual UI: problem (casual question vs handbook jargon) -> upload real document -> cited answer with verified quote -> Compare Retrieval (Raw vs HyDE) -> benchmark table (only if verified labels exist; otherwise say so) -> eligibility on the labelled SYNTHETIC fixture -> conflict (SYNTHETIC) -> abstention -> How it works diagram and design trade-offs -> limitations. Say "synthetic" wherever fixtures are used.
- Update INTERVIEW_NOTES.md with likely questions and short answers tied to this implementation: why HyDE, how HyDE text is kept out of the answer, why "model extracts, code decides", how quote verification works, what happens when a document changes, how workspace isolation works, what the limitations are.

====================================================================
FINAL REPORT
====================================================================
Provide: changes per phase, files changed, actual test results (including new tests), which screenshots were captured and inspected (if any), what was NOT verified, protected-file hash verification result, and exact steps to run and demo on localhost.

</details>

### Appendix E. Held-out HyDE improvement ablation

<details>
<summary>Full user-supplied brief</summary>

# HyDE IMPROVEMENT ROUND: ABLATION ON HELD-OUT DOCUMENTS, KEEP ONLY WHAT WINS

Project: ps1-policy-assistant (FastAPI, ChromaDB, FastEmbed bge-small-en-v1.5, Groq, HyDE, Raw/HyDE/Fusion retrieval, personal workspaces). Run on localhost. No deployment, Docker or hosting work.

BACKGROUND (from the earlier independent audit; re-measure, do not assume): HyDE alone scored lower than Raw (Recall@1 about 0.46 vs 0.625, MRR about 0.62 vs 0.74) on 24 machine-labelled answerable queries. HyDE helped casual or hypothetical student phrasing but hurt direct factual and numeric questions, apparently because the generated passage invented specific parameters or drifted off-topic. Fusion (RRF of Raw and HyDE) was best overall (Recall@5 about 1.0, MRR about 0.80). GOAL: make the HyDE side of retrieval measurably better and decide, with evidence, which retrieval strategy should be the default. A result of "no variant beats the current default" is a valid outcome.

====================================================================
0. HARD RULES
====================================================================
- Run all test traffic in a DISPOSABLE instance (temporary data directory, different port, same approach as scripts/verify_personal_e2e.py). Never test inside the main workspace or the institution workspace.
- PROTECTED DATA: do not approve or publish institution sources; do not delete or reset Chroma, registries or manifests; do not read, print, log or modify the admin token or any API key; keep the 3 extraction failures visible; keep institution isolation. Verify the protected-file SHA-256 hashes before and after (existing method) and report match or mismatch. Real MSRIT PDFs may only be used as READ-ONLY COPIES inside the disposable instance.
- GUARDRAILS ARE NON-NEGOTIABLE: the HyDE passage (or any hypothetical text or averaged vector derived from it) must NEVER reach the answer model's prompt; workspace scoping and isolation; citation validation; verbatim quote verification; abstention on no evidence; prompt-injection resistance; deterministic eligibility comparison; personal/institution trust separation. Any change that increases confident wrong answers on near-miss or out-of-scope questions is rejected, however much it improves retrieval. Do not lower the confidence threshold to raise answer yield.
- Do not hardcode anything derived from specific test documents or questions (no document-specific keywords, no question lists, no per-document rules). Every change must be general.
- Do not edit existing tests to make them pass. Add tests for new code.
- Provider failures (HTTP 429, timeouts, 5xx) are NOT retrieval results and NOT abstentions. Pace requests, honour Retry-After, back off, persist progress, re-run affected items later, and count failures separately. Cache every LLM-generated HyDE output keyed by (variant, prompt hash, query) in improve_hyde/cache/ so reruns are cheap and deterministic.
- Backwards compatibility: existing API contracts, modes (raw, hyde, fusion) and the UI keep working. New variants are added as additional selectable modes behind configuration. UI work is limited to listing new mode names in the existing mode selectors if trivial; no redesign.
- Before editing any file copy it to improve_hyde/backups/iter_N/ so changes can be reverted. Do not use git.
- Create improve_hyde/PROGRESS.md and update it after every step so an interrupted session can resume (read it first if it exists).
- Time-box about 90 minutes. If short on time, drop in this order: BM25 hybrid (V8), vocabulary-aware HyDE (V5), then multi-HyDE (V4). Never drop V1 to V3, V6, V7, the hold-out evaluation or the report.

====================================================================
1. SETUP
====================================================================
1. Run the full Python test suite and the JS DOM tests; record baseline counts.
2. Document pool: every usable text-based PDF in audit_inputs/ plus other non-protected PDFs found in the project (list page counts and file hashes; record extraction failures). If fewer than 4 usable PDFs exist, say so and use what exists. Also include any improve/ or audit/ outputs that already hold a verified test set only as additional reference, not as training data for your changes.
3. Split by DOCUMENT into TUNE and HOLD-OUT with a seeded random generator (record seed and assignment). If the pool has 4 or more documents hold out about one third, at least one. HOLD-OUT documents must not be inspected for failure analysis, prompt design or threshold choice; they are used only for the final comparison.
4. Test set per document, generated by you: 20 to 30 answerable questions written the way casual students ask (not reusing the document's own wording), tagged by type: direct factual, numeric/threshold, casual or hypothetical paraphrase, multi-condition. Plus at least 4 near-miss unanswerable (sound like a real policy topic the document does not cover) and 3 clearly out-of-scope per run. For every answerable question record the gold page and a GOLD QUOTE copied verbatim from the document; verify by code that the quote is an exact substring (after whitespace and quote-character normalisation) of the extracted text of that page, then identify the gold chunk(s). Discard any question that fails. State that labels are machine-generated and machine-verified for existence, not human-reviewed. If a human-verified label file exists in the project (labels_verified true), also evaluate on it and report it separately.
5. Record the baseline verbatim: current HyDE prompt, current HyDE parameters, fusion method and constants, default mode, confidence-gate logic and thresholds. Inspect how the confidence gate computes its score; keep that logic's meaning unchanged (see 3.7).

====================================================================
2. VARIANTS TO IMPLEMENT AND COMPARE
====================================================================
Implement each as a configurable retrieval mode with a clear name. Embeddings stay local (FastEmbed bge-small-en-v1.5); vectors are L2-normalised before averaging and again after.

V0  raw: embed the student query only (baseline).
V1  hyde_v1: the CURRENT HyDE (baseline for comparison).
V2  hyde_v2_prompt: new HyDE prompt. Same single call, but instruct the model: write in formal handbook vocabulary; use generic wording instead of specific figures (for example "a prescribed minimum percentage", "the stipulated period"); never state a specific number, date, name or fee unless it appears in the student's question; 60 to 110 words; no headings or disclaimers.
V3  hyde_plus_query_avg: average the embedding of the query with the embedding of the V2 passage (the original HyDE paper's formulation averages the query embedding with the hypothetical-document embeddings, giving the query the weight of one hypothesis). Also test weights (for example query 1:1, 1:2, 2:1).
V4  multi_hyde: ONE LLM call that returns 3 short passages from different angles (for example eligibility conditions, procedure and documents required, exceptions and penalties), each following the V2 rules; embed each, average them with the query embedding (also test without the query). Do not make 3 separate calls; token budget matters on the free tier. Parse robustly; if parsing fails fall back to V2 and count it.
V5  vocab_hyde: V2 plus a compact list of the workspace's document titles and section headings (capped, for example 40 items) passed to the HyDE prompt so it uses the corpus's own vocabulary. This is a generic mechanism, not hardcoded terms. The headings go only to the HyDE generator, never to the answer model.
V6  routed: if the raw top-1 similarity is at or above a cutoff tau use raw only (saves the LLM call); otherwise use the best HyDE-based variant. Choose tau by sweeping on TUNE documents only; report the sweep. A fixed tau, not per-document.
V7  fusion variants: RRF of raw and each HyDE variant with different constants (for example k = 10, 30, 60) and weights (raw weighted 1.0 vs 1.5 or 2.0 against HyDE). Include the current Fusion as the baseline.
V8  hybrid_bm25 (only if rank_bm25 installs and works offline): BM25 over chunk text fused with dense retrieval and with the best HyDE variant. If it cannot be installed, mark NOT TESTED.

For every variant record per query: top-5 chunk ids and scores, gold-chunk rank, HyDE text(s) used, LLM calls and approximate tokens, added latency, parse or fallback events.

====================================================================
3. PROCEDURE
====================================================================
3.1 Inspect HyDE outputs by hand (TUNE documents only): read at least 20 generated passages from V1 and V2. Classify each as on-topic / off-topic / contains invented specific figures. Report counts. This explains the baseline failures and checks whether V2 reduces them.
3.2 Run the ablation on the TUNE documents: all variants, all questions. Compute Recall@1/3/5 and MRR overall AND split by question type; per-question wins and losses versus V0 and versus the current Fusion. Save raw results to improve_hyde/results/tune/.
3.3 Select at most 2 or 3 candidate configurations from the TUNE results (for example the best HyDE-style variant, the best fusion, the best routed combination). Freeze them. Do not iterate further on TUNE after seeing HOLD-OUT results.
3.4 Evaluate the frozen candidates, plus V0, V1 and the current default, on the HOLD-OUT documents with questions generated fresh. Save raw results to improve_hyde/results/holdout/. Because samples are small, treat differences of one question as noise; report counts alongside rates and say which differences are meaningful.
3.5 Acceptance rule for changing the default retrieval mode. Adopt a candidate as the new default ONLY IF, on HOLD-OUT: (a) MRR and Recall@3 improve over the current default; (b) no question type gets clearly worse (state your tolerance and why); (c) near-miss, out-of-scope and prompt-injection abstention does not get worse and no new confident wrong answers appear in an end-to-end run; (d) average added latency and LLM tokens per query are reported and acceptable (state the budget you applied; the free-tier Groq limit is roughly 8,000 tokens per minute on some models, so prefer variants that do not multiply LLM calls); (e) the full test suite and JS tests pass and every guardrail in Section 0 passes. If no candidate satisfies all of this, keep the current default, and still keep any variant that is a harmless, selectable option.
3.6 End-to-end check for the adopted default: run the full pipeline (retrieval, answer, citation and quote verification, abstention) on the HOLD-OUT questions including near-miss, out-of-scope and injection questions. Provider failures are counted separately. Confirm HyDE text isolation with instrumented prompt checks on at least 10 questions (the HyDE passage, the averaged-vector source text and the heading list must not appear in the answer prompt).
3.7 Confidence gate: averaging embeddings or routing changes score scales. Inspect how the gate score is computed. Keep the gate's meaning unchanged (for example gate on the similarity of the best retrieved chunk to the original student query, computed the same way as before) so abstention behaviour is comparable, and verify with the near-miss and out-of-scope questions. Do not retune the threshold to raise answer yield; if a variant cannot be used without moving the threshold, report that and reject it.
3.8 Tests: add unit tests for each new variant (vector averaging and normalisation, multi-passage parsing and fallback, routing cutoff logic, cache keys), for the isolation guarantee (HyDE-derived text never in the answer prompt), and for backwards compatibility of the old modes.
3.9 Update README/DECISIONS notes briefly: the default mode and why, the new modes, and the measured trade-offs. Append every new or changed in-app prompt (V2, V4, V5) verbatim to PROMPTS.md with its purpose.

====================================================================
4. FINAL REPORT (improve_hyde/HYDE_REPORT.md plus a short summary in chat)
====================================================================
1. Setup: seed, document pool, TUNE/HOLD-OUT assignment, question counts per type, how labels were produced and verified (machine-generated, machine-verified for existence, not human-reviewed).
2. HyDE output inspection: counts of on-topic, off-topic and invented-figure passages for V1 vs V2.
3. TUNE ablation table: every variant, Recall@1/3/5, MRR overall and per question type, LLM calls and tokens per query, added latency.
4. HOLD-OUT table for the frozen candidates versus V0, V1 and the current default, with raw counts and a statement of which differences are meaningful.
5. Decision: which default was adopted (or kept) and the acceptance-rule checks (a) to (e) with evidence; every rejected variant with why.
6. End-to-end results on HOLD-OUT: answers, true abstentions by reason code, confident wrong answers, provider failures (separate), latency.
7. Guardrail checklist: each item in Section 0 PASS / FAIL / NOT TESTED with evidence; HyDE isolation check results.
8. Test counts before and after; protected-file hash result; institution workspace unchanged.
9. What is NOT verified (for example anything needing human-verified labels, small-sample effects, single LLM provider, no OCR).
10. How to reproduce (commands, seed, location of raw results and cache) and how to revert using improve_hyde/backups/.
Be blunt. Do not claim an improvement unless the HOLD-OUT numbers show it.

</details>

### Appendix F. Path to Eligibility, project log and prompt archive

<details>
<summary>Full user-supplied brief</summary>

# ADD ONE FEATURE: "PATH TO ELIGIBILITY" WHAT-IF SIMULATOR, PLUS MANDATORY PROJECT LOG AND PROMPT ARCHIVE

Project: ps1-policy-assistant (Campus Policy Intelligence: FastAPI, ChromaDB, FastEmbed, Groq, HyDE/Raw/Fusion retrieval, anonymous personal workspaces, Rule Book of quote-validated numeric rules, deterministic eligibility analysis, conflicts, version comparison). Run on localhost. No deployment, Docker or hosting work. Do not use git. Time-box about 60 to 90 minutes.

====================================================================
PART 0. DO THIS FIRST: LOGGING AND PROMPT ARCHIVE (applies to the whole session)
====================================================================
A. PROJECT_LOG.md (project root). Append-only, chronological. If it exists, read it first and append; if not, create it. After EVERY step or phase append an entry in this format:
  ## <YYYY-MM-DD HH:MM> | <short title>
  - What was done:
  - Files created or changed:
  - Tests run and counts (Python and JS):
  - Decisions and trade-offs:
  - Problems found / not verified:
  - Next step:
Keep it truthful: separate "verified" from "not verified". If you backfill history from existing reports in the repo (audit/, improve/, improve_hyde/, docs/, README, DECISIONS, PROMPTS.md), put it in a clearly marked section "Backfilled history (from existing documents, not re-verified)" and do not invent anything that is not in those files.

B. PROMPTS_USED.md plus a prompts/user/ folder. This archives the prompts the USER gave to the coding agent (separate from PROMPTS.md, which holds the app's in-app LLM prompts; do not merge or overwrite PROMPTS.md).
  1. Before doing any other work, save THIS ENTIRE PROMPT verbatim, character for character, to prompts/user/<NN>_<YYYY-MM-DD>_whatif-simulator-and-logging.md (NN = next free two-digit number).
  2. Append an index line to PROMPTS_USED.md: number, date, title, filename, one-line purpose, and the outcome (completed / partial / blocked, filled in at the end).
  3. If the user sends further prompts later in this session, save each verbatim the same way BEFORE starting work on it.
  4. Search the repo for any earlier user-provided prompt or instruction files (for example uploaded .md prompt files, files named like build guide, redirection, continuation, audit, improve, ablation, ui). List each in PROMPTS_USED.md with its path under "Found in repo (copied verbatim or referenced)". Copy them verbatim into prompts/user/ only if they are clearly prompts the user gave; do not guess or reconstruct prompts from memory. State plainly in the file that earlier prompts which are not in the repo must be pasted in by the user.
  5. Never store secrets. If a prompt contains anything that looks like an API key, token or password, replace it with [REDACTED] and note that you did.
  6. Append-only: never delete or rewrite earlier entries.

====================================================================
PART 1. RULES FOR THE FEATURE WORK
====================================================================
- Do not change existing guardrails or behaviour: HyDE text never reaches the answer prompt; workspace scoping and isolation; citation and quote verification; abstention; prompt-injection resistance; personal/institution trust separation; deterministic (non-LLM) eligibility comparison. Do not change retrieval, prompts, thresholds or API contracts. Add new code and endpoints only.
- PROTECTED DATA: do not approve or publish institution sources; do not delete or reset Chroma, registries or manifests; do not read, print, log or modify the admin token or any API key; keep the 3 extraction failures visible; keep institution isolation. Verify protected-file SHA-256 hashes before and after (existing method) and report the result.
- The simulator must make ZERO LLM or provider calls at runtime. The Groq daily quota is nearly exhausted: do not call Groq or any provider while building or testing. Use synthetic fixtures and cached or fixture rules only. Add a test that fails if the what-if endpoint triggers any provider call.
- Never fabricate: no invented thresholds, formulas or policy facts. The simulator only does arithmetic on thresholds that come from existing validated rules (the verbatim quote and number already verified by code). Nothing is hardcoded to a specific document, college, subject name or question.
- Before editing any existing file, copy it to backups/whatif/ so it can be reverted.
- Run the full Python suite and the JS DOM tests before starting (record baseline counts) and after the feature; restart the app on localhost and confirm it loads. If something breaks and you cannot fix it in two attempts, revert that change and log it.
- Use the existing design tokens and styles; support the light and dark themes if they exist; fully offline (no CDN, external fonts or images); keep safe rendering (escape all text, never insert unescaped via innerHTML); keep SYNTHETIC TEST FIXTURE labels visible on fixture data.
- Preserve existing element IDs and test hooks.

====================================================================
PART 2. THE FEATURE: PATH TO ELIGIBILITY (WHAT-IF SIMULATOR)
====================================================================
PURPOSE: After a student's eligibility analysis, let them change their numbers and instantly see which rules would be satisfied, and what change would be needed to satisfy each rule that currently is not. This moves the product from "answers questions" to "shows what the student can do", using only the student's own documents.

BEHAVIOUR
1. Entry point: a "What if I change this?" panel on the eligibility result in Ask & Analyse, shown only after a confirmed analysis exists (same confirmation gates as today: facts confirmed, rule applicability confirmed). Unconfirmed or missing facts remain "insufficient evidence"; the simulator never fills them in.
2. Scenario inputs: one editable field per confirmed numeric fact (value and unit, prefilled), with a "Reset to my real facts" button. Use number inputs and, where a sensible range exists (for example 0 to 100 for percentages), a slider as well. Hypothetical values are a SCENARIO: never saved as the student's confirmed facts, never cached as an answer, never persisted. Show a permanent banner while a scenario differs from the real facts: "Scenario only. These are not your real values."
3. Live results: for every rule used in the analysis show: rule text (the verbatim quote with document and page), required value and operator, scenario value, status (satisfied / not satisfied / insufficient evidence), and the gap. Recompute when inputs change, debounced, by calling a NEW backend endpoint that reuses the SAME deterministic evaluator as the real analysis (single source of truth, Decimal arithmetic, same operator handling). The client must not reimplement the comparison logic.
4. Path to eligibility, per rule that is not satisfied:
   a) Direct gap: the amount the value must change to meet the threshold, respecting the operator (for strict ">" say it must exceed the threshold; for "==" say it must equal the threshold and give no gap).
   b) For percentage rules, an optional "compute from counts" mode: the student may enter done (numerator), total so far (denominator) and optionally remaining (future items). Then compute with Decimal and show:
      - the minimum number of additional consecutive items that must be fully completed to reach the threshold: x = ceil( (t * total - done) / (1 - t) ) where t = threshold/100, and state when t >= 1 means it cannot be reached by additional items alone;
      - if remaining is provided: whether the threshold is still reachable (done + remaining over total + remaining), and the maximum number of the remaining items that can be missed while still meeting it.
      Label this clearly as ARITHMETIC ON THE STATED THRESHOLD ONLY. It does not model the institution's own counting rules, cut-off dates, condonation, exceptions or rounding practices unless those appear in the rule text. Use generic wording ("items", "classes or units as counted by your institution"); do not hardcode attendance terminology, though the label may reuse the rule's own subject text.
   c) Exceptions and caveats: if the validated rule has an exceptions or applicability field, show it as a verbatim quote with page and the line "These may change what applies to you. Check with your institution." Never present a route to eligibility that the document does not support, and never suggest an exception applies to the student.
5. Overall verdict under the scenario: eligible / ineligible / insufficient evidence computed by the same logic as today (all required conditions satisfied, any not satisfied, any unknown). Never claim eligibility if any condition is unknown. Say that the verdict covers only the rules found in the uploaded documents.
6. Conflicts: if two rules for the same subject conflict across documents, show both with quotes and do NOT produce a combined verdict or a path; say it cannot be resolved without more evidence (consistent with the existing conflict logic).
7. Ordering: list unmet rules by smallest required change first (units differ, so compare only within the same unit and otherwise keep document order).
8. Trust: personal-workspace results keep the existing line "Based on documents you uploaded. Not verified by your institution." Rules shown as "extracted by AI, verify against the source quote."

BACKEND
- New endpoint (workspace-scoped like the other personal endpoints, capability id required, rate-limited like others): POST /api/personal/<workspace>/whatif with {facts: [...scenario values...], counts?: {...}}. Reuse existing evaluator functions; add only thin new functions for the gap and count arithmetic in the intelligence module (or a new small module). Validate inputs strictly: numeric ranges, Decimal parsing, maximum magnitudes, reject NaN and infinity, unit mismatches handled explicitly (do not convert between units unless the code already supports it; otherwise return insufficient evidence for that rule).
- Response is JSON only (no free text from a model). Return per-rule structured results so the UI renders them without interpretation.
- Must never touch another workspace's rules and must work only with rules already extracted and validated for this workspace.

FRONTEND
- Compact, readable table plus the scenario controls; statuses shown as text plus a small neutral marker (not colour alone). Keyboard accessible, labelled inputs, aria-live region announcing the updated verdict. Clear empty state ("Run an analysis with confirmed facts first"), error state and a "no numeric rules found" state. No horizontal overflow at 390px width.
- Add it to the existing "How it works" page as one line describing the deterministic what-if (no new diagram required).

TESTS (add; do not edit existing tests to make them pass)
- Arithmetic: boundary equality for >= and > (value exactly at threshold), threshold 75 with done 60 of total 90, threshold 100 (unreachable by additional items), remaining items cases (reachable, exactly reachable, unreachable), zero total, negative or huge values rejected, Decimal rounding (ceil) correctness against an independent brute-force loop on at least 200 random cases.
- Operator handling for >=, >, <=, <, ==.
- Unit mismatch gives insufficient evidence, never a guessed conversion.
- Missing or unconfirmed fact stays insufficient evidence; verdict never "eligible" with an unknown condition.
- Conflicting rules produce no winner and no path.
- Zero provider calls (instrument the provider layer and assert it is never invoked).
- Workspace isolation: workspace B cannot use workspace A's rules or capability.
- Scenario values are never persisted or cached (check registries, caches and files before and after).
- Safe rendering: rule text or quotes containing HTML or script are escaped in the UI.
- JS DOM tests for the panel: prefilled values, reset, banner shown only when the scenario differs, aria-live updates.
Also run an end-to-end check in a disposable instance using the SYNTHETIC fixtures (and cached or fixture rules, no provider calls): confirm the numbers on screen match a hand calculation, and say clearly if browser-level visual QA was not performed. If Playwright/Chromium is available capture screenshots at 1440px and 390px in light and dark and inspect them.

DOCS (keep short)
- DECISIONS.md: what the simulator does and does not model, why it makes no LLM calls, the arithmetic and its stated limits, and what is NOT verified.
- One short "interview notes" paragraph in the existing interview notes file if present.
- Do not rewrite other documentation.

====================================================================
FINAL REPORT (short, also appended to PROJECT_LOG.md)
====================================================================
What was built, files changed, test counts before and after, the hash check result, whether any provider call occurred (it must be zero), what was verified end to end versus not, known limitations, and exactly how to demo the simulator on localhost with the synthetic fixture in under one minute. Then update PROMPTS_USED.md with this prompt's outcome and stop. Do not add any other feature.

</details>

## Additional request — Whole-website UI upgrade (16 November 2026)

**User request, lightly edited:** Improve the whole website's UI. Add a help button/chatbox and useful standard website interactions, animations, and a professional, sleek visual design. Upgrade the basic interface to a more advanced experience.

Implementation record: docs/UI_WORKSPACE_UPGRADE.md. This entry records the prompt; it does not replace the raw historical requests or represent a new company requirement.

## Additional request — Review, freeze and execute fresh evaluation

User requested proceeding with all six evaluation steps: review/label ten questions against the PDF; record exact provisions, alternatives, qualifications and abstentions; freeze labels; improve runner metrics/reproducibility; run Raw/HyDE/Fusion; assess raw and final answers separately. AI review was explicitly disclosed rather than represented as human approval. Actual implementation, 30-attempt results and remaining review limitations: docs/FROZEN_TEN_EVALUATION_EXECUTION.md.
