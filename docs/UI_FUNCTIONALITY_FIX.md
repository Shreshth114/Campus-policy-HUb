# UI and end-to-end functionality verification — 2026-11-14

## Actual root causes

Live localhost responses before the fix: `/health` reported one workspace, `/institutions` returned an empty list, and authenticated `/admin/institutions` returned Ramaiah Institute of Technology, active/unpublished. Its source list contained ten pending documents. The student filter was correct: unpublished institutions must remain hidden. The service count included private workspaces, but the UI failed to explain that distinction.

The administrator API was accessible and returned the existing workspace; the interface reused the student selector at the top of the page rather than providing one within administration. Upload controls were hidden by `admin-controls` until authentication, without a visible guided path from unlock to workspace selection/document management. Creating an institution unnecessarily required a slug.

The student-entry handler cleared the selected institution, reloaded the public list and reset scope before opening chat. Chat also appeared before a valid institution was chosen. `switchInstitution` cleared its content without restoring an actionable empty state. These rendering/navigation conditions gave the appearance of an unavailable product.

## Implemented fixes and files

- `web/index.html`: separate Overview/student/administrator experiences, visible onboarding steps, dedicated private workspace selector, named institution context, document upload/drop zone, progress, status metrics, PDF preview, full review interface and responsive dark-theme hierarchy.
- `web/app.js`: independent public/admin lists and selections; student entry retains selection; no-policy/empty/error states; name-only creation; drag-and-drop and actual XHR byte progress; scoped per-document extraction/indexing after upload; review remains pending until an explicit approval action; original PDF preview uses an authenticated request and a revocable blob URL, never a token in the URL. Late responses and source-inspection races are guarded. Review form validation names required fields.
- `src/institutions.py`, `src/server.py`: optional generated safe slugs and duplicate-name rejection, preserving immutable IDs and existing explicit-slug callers. The public publication filter and all retrieval/approval boundaries are unchanged.
- `scripts/verify_e2e.py`: opt-in live API/embedding/Groq procedure in a separate disposable app instance with synthetic review-state emulation; no production source/approval/cache/index writes.
- `tests/test_onboarding.py`, `tests/frontend.test.cjs`, `tests/test_frontend.py`: regressions for private workspace visibility, name-only creation, duplicate prevention, workflow separation, upload/index progress, pending defaults, student selection retention and no-evidence messages.
- Setup/API/verification documentation and DECISIONS/PROMPTS/INTERVIEW_NOTES updated.

## Administrator workflow

Open Administration → enter existing ADMIN_API_TOKEN privately from `.env` → select an existing workspace (unpublished ones are listed) or create by name → inspect counts/publication state → drop PDFs or Browse files → Upload & index PDFs → inspect original/text/chunks/hash/version → record issuer, official URL, reviewer and known applicability → explicitly approve the current version → publish reviewed knowledge base.

Publication requires eligible approved evidence. New documents remain pending, and replacements preserve history. An administrator may keep pending/reject, retry scoped indexing, unpublish, or clear only the selected workspace's answer cache. No source was approved on the user's behalf in the real demonstration workspace.

## Student workflow

Overview → choose published institution → Enter student workspace → see selected institution name → ask or choose an example → receive answer/citations and source-page evidence, or a grounded abstention → inspect confidence, separate RRF/cosine, HyDE search aid, provider and stage timings. Compare and benchmark views retain their existing retrieval/evaluation functions.

No published institutions: Overview explains administrator setup. Published institution with no eligible evidence: chat is replaced with “No verified institutional policies are currently available for this institution. Please contact your institution administrator.” Unpublished institutions remain hidden.

## Actual execution evidence

`python scripts/verify_e2e.py --live --output <report.json>` starts a separate localhost server with temporary data, a temporary administrator token and the existing configured Groq provider. Synthetic fixture PDFs emulate source review only in that disposable test instance; they are not authenticated university policies and never enter the real knowledge base. No production filter is disabled or replaced.

The final live run used the same question across Raw, HyDE and Fusion, clearing only the disposable answer cache between modes so each retrieval/generation path executed. All three returned `answered` through Groq `openai/gpt-oss-120b`; all citations resolved to the fixture's actual chunk and page 1; neither HyDE nor Fusion fell back in this final run. Local FastEmbed generated actual document/query embeddings and real Chroma retrieval ran with production predicates. See UI_LIVE_E2E_RESULTS.json for observed stage timings and token usage. These are functional observations, not retrieval-accuracy benchmarks.

Instrumented answer-prompt checks ran four times (three supported requests plus an unsupported request). Each contained the original question and retrieved document evidence, and excluded the generated HyDE passage. The unsupported question returned `no_policy_found`. A cache hit succeeded while eligible; moving the fixture back to pending prevented reuse and caused abstention. Foreign source inspection/approval was rejected. Public institution selection exposed only the explicitly published fixture workspace.

Earlier verification attempts also exercised a HyDE fallback and citation-check abstention. Those were recorded as guard behavior, not successful policy answers. LLM responses remain nondeterministic; passing the final check does not guarantee every future answer will satisfy citation requirements.

## Results and preservation

- Complete automated suite: **227 passed**, six existing dependency deprecation warnings, 8.40 seconds. No skips.
- Node DOM harness: **19 checks passed**; JavaScript syntax check passed.
- Live isolated HTTP/Groq/embedding verification: completed as above.
- All **37 protected existing files** matched their starting SHA-256 hashes: original/scoped documents, registries, manifests, caches and legacy Chroma. The real workspace remains the same single institution, unpublished, with ten pending sources. No duplicate MSRIT institution was created. Provider credentials and administrator token were not changed or exposed.

BrowserOS neo MCP tools are unavailable, so actual visual/browser interaction QA remains unverified. API and DOM checks are not visual QA. The three existing extraction failures, human authenticity/applicability review and unverified real benchmark labels remain unchanged. OCR and invented policy/accuracy claims are outside this work.
