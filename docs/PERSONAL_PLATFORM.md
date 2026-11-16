# Personal workspace operation and API

Start `python -m src.server` from the project directory and open localhost:8000. No deployment or additional infrastructure is required. Provider integration uses the existing runtime configuration; no administrator credential is needed for personal use.

The anonymous server-generated workspace ID is a bearer capability. localStorage key `campus-personal-workspace` stores it; requests send `X-Workspace-ID`. Do not share it with someone who should not access the workspace. No accounts or ID recovery service exist. The optional college name is a display label, not verified ownership or institutional affiliation. New documents remain unverified; their authority status is never promoted to an institution's approved source.

Personal data: `data/personal/<workspace_id>/raw`, `processed` (registry, manifest, caches, rules/activity), and `bench` (user labels/results). Existing institutional storage remains separate and unchanged. Only capability-owned document/version records are accessible. Replacing a document keeps original versions, revokes old retrieval eligibility and invalidates citing answers/rules. Remove deletes that personal document and its versions, scoped vectors and derived rule/answer entries; Delete workspace removes all that personal workspace's files and vectors. Institutional removal retains its existing original/history behavior.

Routes:

- `POST /personal/workspaces` `{college?: string}`: create anonymous workspace; no credential required.
- `GET /personal/workspace`: scope details, document/chunk counts, readiness and configured limits.
- `DELETE /personal/workspace`: delete the selected personal workspace.
- `GET /personal/documents`, `POST /personal/documents`: list or multipart upload (`files`, up to five per request; optional `document_id` replacement).
- `GET /personal/documents/{id}` and `/original`: extracted pages/chunks/version/history or PDF bytes.
- `POST /personal/documents/{id}/index`, `GET /personal/activity`: incremental indexing and stage progress.
- `DELETE /personal/documents/{id}`: remove only that owned source from current retrieval.
- `POST /personal/ask` `{question, mode}`: raw/hyde/fusion answer trace with trust notice, citations, scope and timings.
- `GET /personal/citations/{chunk_id}`: live eligible source excerpt and page.
- `POST /personal/compare`: same question contract; actual Raw/HyDE comparison.
- `POST /personal/cache/clear`: selected answer cache only.
- `POST /personal/rules/extract` `{document_id?, version_id?}`, `GET /personal/rules`, `GET /personal/rules/activity`: quote-validated numeric Rule Book, optional explicit historical extraction and progress. Historical rules are used only for comparison.
- `POST /personal/facts/parse` `{text}`: source-subject-bound proposed facts; confirmation always required.
- `POST /personal/analyse` `{question, facts:[{subject,value,unit}], confirmed, applicability_confirmed}`: deterministic conditions/verdict and constrained explanation. Values are decimal strings. Unconfirmed facts return 422.
- `GET /personal/conflicts`: same-subject, differing-value possible conflicts; no winner.
- `GET /personal/versions`, `POST /personal/changes` `{old_document_id, old_version_id, new_document_id, new_version_id}`: owned versions and validated rule-table differences. Missing extracted tables return a blocked state.
- `GET /personal/bench/status`, `/bench/results/latest.json|latest.md|latest.svg`, `POST /personal/bench/run`: scoped actual benchmark status/results. Supply labels manually; no scores are invented.

All except workspace creation require the workspace header. Unknown/missing capabilities return 404; personal headers confer no administrator access. Institutional/public routes retain their existing requirements. Upload validation checks content, encryption, bytes, page count and active-document count; invalid files return per-file errors. Extraction failure is visible and contributes no chunks.

Known limits: numeric comparisons only (>=, >, <=, <, ==, !=), no invented formulas, no guarantee of complete extraction, conservative applicability/exception handling, and exact subject grouping rather than a universal policy ontology. AI explanations and excerpts remain untrusted evidence to inspect. Rule/quote validation is not institutional authenticity verification. Browser visual QA is not claimed without browser connectivity.
