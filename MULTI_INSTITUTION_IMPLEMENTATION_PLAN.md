# Approved implementation phases and delivered boundaries

This records the staged architecture approved in the master build instruction; it does not request another approval.

1. Registry/context/workspaces: generated immutable UUIDs, independent publication and activation, explicit request context.
2. Sources/index/retrieval: immutable versions, scoped chunk IDs/metadata, tenant predicates before ranking, pending defaults, bounded batches and rollback.
3. Answers/cache/citations: separate persistent files and live ownership/fingerprint checks at generation/cache boundaries.
4. Administration: local token, uploads, extraction/chunk/original inspection, review/history, scoped indexing/removal/publication.
5. Student frontend: landing/selector/chat/explainability/compare/benchmark/admin views, safe rendering and stale-response guards.
6. Evaluation: scoped labels/results and temporary two-institution isolation/regression tests. No invented measurements.
7. Migration: inventory/backup, immutable mapping, representative model compatibility check, reused vectors, count/hash/status validation, legacy retention.
8. Documentation: setup, API, architecture, migration and honest verification limitations.

MVP keeps JSON, FastAPI, vanilla JavaScript, FastEmbed and Chroma. Future production features: individual operator roles/SSO, TLS deployment, audit-grade event storage, crash-proof jobs and OCR. Browser visual verification requires connected BrowserOS neo tools.
