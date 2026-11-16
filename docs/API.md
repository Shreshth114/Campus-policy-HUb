# API contract

Run one local worker. Open `/docs` for generated schemas. JSON models reject unknown fields. Questions are trimmed, control-character checked and limited to 500 characters. JSON mutation bodies are capped at 8 KB; upload bodies at five 30 MB PDFs plus multipart overhead. Mutation requests are rate limited to 30 per client/minute. No student option enables evaluation retrieval.

Public routes:

- `GET /institutions`: active, published institutions only.
- `POST /ask`: `{ "institution_id": "<uuid>", "question": "...", "mode": "raw|hyde|fusion" }`; returns a trace including institution, chunk/document/version provenance, answer, citations, cosine/RRF and timings.
- `POST /compare`: same contract; raw and HyDE retrieval side by side, verified highlights only for institution-owned labels.
- `GET /sources?institution_id=<uuid>`: eligible sources only.
- `GET /institutions/<uuid>/citations/<chunk_id>`: live eligible full excerpt and provenance, 404 for foreign/stale/unapproved citations.
- `GET /bench/status?institution_id=<uuid>` and `/bench/results/latest.json|latest.md|latest.svg?institution_id=<uuid>`: scoped actual status/results. Result symlinks outside the scoped results directory are rejected.
- `GET /health`: basic service/provider configuration booleans, never credentials. Add `?institution_id=<uuid>` for published corpus statistics.

Missing/unknown/unpublished public institution returns 422. No eligible evidence returns a normal abstention trace. Dependency failures are sanitized.

All `/admin/*` routes require `Authorization: Bearer <ADMIN_API_TOKEN>`. A missing or incorrect token returns 401. The MVP operator manages all institutions. Source IDs from another workspace return 404/409, never a foreign record.

- `GET /admin/institutions`: all workspaces.
- `POST /admin/institutions`: `{ "name": "Example University" }`; UUID and slug are generated, pending publication. Optional explicit `slug` remains supported. Duplicate display names are rejected with guidance to select the existing workspace.
- `PATCH /admin/institutions/<uuid>`: `{ "published": true, "status": "active" }`. Publishing requires live approved evidence; false unpublishes. Status may be `disabled`.
- `POST /admin/institutions/<uuid>/documents`: multipart `files` (1–5 PDFs), optional `document_id` to create replacement versions. Returns per-file pending records/errors. Run reindex separately.
- `GET /admin/institutions/<uuid>/sources`: records and scoped chunk count.
- `GET /admin/institutions/<uuid>/sources/<document_id>`: metadata, history, full extracted pages, indexed chunks.
- `GET /admin/institutions/<uuid>/sources/<document_id>/original`: authenticated original PDF download.
- `POST /admin/institutions/<uuid>/sources/<document_id>/approve|pending|reject`: JSON `version_id`, `reviewer`, optional `source_url`, `issuing_authority`, `programme`, `cohort`, `effective_date`, `notes`. Approval requires indexed real content, unchanged current hash, source URL and issuer. Unknown applicability/dates remain null. This records the operator's verification; it does not automatically establish authenticity.
- `DELETE /admin/institutions/<uuid>/sources/<document_id>`: remove vectors, reject record, retain original/version history.
- `POST /admin/institutions/<uuid>/reindex`: incremental workspace indexing; 409 while another API indexing operation runs.
- `PATCH /admin/institutions/<uuid>/sources/<document_id>/reindex-current`: index only that document.
- `GET /admin/institutions/<uuid>/activity`: current/recent indexing stage, file, counts, timings and errors.
- `POST /admin/institutions/<uuid>/cache/clear`: answer cache for selected institution only.
- `GET /admin/institutions/<uuid>/bench/status`, `POST /admin/institutions/<uuid>/bench/run`: honest scoped benchmark status/run.

Legacy `/reindex`, `/cache/clear`, `/cache/stats` aliases also require admin authentication and explicit institution selection. They cannot access the legacy global corpus.


## Personal student workflow

The primary student path is now anonymous personal workspaces. See PERSONAL_PLATFORM.md for the X-Workspace-ID capability API, upload limits, scoped RAG/rules/analysis/conflicts/version differences and personal benchmark endpoints. Institutional/public/admin contracts above remain secondary and unchanged.
