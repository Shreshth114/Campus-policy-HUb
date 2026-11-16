# Legacy migration validation

Institution: Ramaiah Institute of Technology (`msrit`). Generated immutable ID: `192afc66-bae5-4f82-bdb9-6e2cbe4daafb`.

The application now uses the parallel institution collection/store. The workspace is active but **unpublished**. All ten real sources remain **pending**; no source authenticity, date or benchmark label was automatically verified.

| Check | Result |
|---|---:|
| Original PDFs copied with matching SHA-256 | 10 |
| Registry entries retained pending | 10 |
| Successfully indexed real documents | 7 |
| Real chunks/texts/vectors reused | 517 |
| Visible pending extraction failures | 3 |
| Decoy chunks, marked synthetic/evaluation-only | 4 |
| Legacy files matched against protected inventory | 22 |
| Production-eligible sources/chunks | 0 |

Backup: `data/migrations/baseline/legacy/`. SHA-256 inventory: `data/migrations/baseline/inventory.json`. Persisted document/chunk identity mapping: `data/migrations/baseline/mapping.json`. Exact exported input arrays: `data/migrations/baseline/legacy_vectors.npz`. The legacy `.chroma`, raw PDFs, registry, manifest, caches and benchmark dataset remain untouched. Per-institution caches started empty. The copied benchmark records retain unverified labels.

Embedding provenance: the recorded ingestion configuration and runtime diagnostic identify `BAAI/bge-small-en-v1.5` with 384 dimensions. Before copying, one excerpt from each of the eight indexed documents (seven real plus decoy) was recomputed using that same locally cached model. Minimum old/recomputed cosine agreement was 0.999999859234. Full-corpus vectors were **not** regenerated.

Every original vector was supplied unchanged to the new Chroma collection. Chroma normalizes float32 cosine vectors on insertion: readback differed by at most 2.98023223877e-08 per component, with measured minimum old/new cosine 0.9999999999999993. All 521 texts matched exactly. Validation permits only 1e-7 absolute storage rounding; the exact exported arrays and backup remain recoverable. The initial exact-bit comparison correctly paused validation; rerunning the staged migration reused its persisted identities without duplicates.

New vector store: `.chroma-institutions`, collection `institution_policy_chunks_v2`. Decoy vector exports also reside under the workspace's `evaluation/`; they are excluded from production by both registry approval and synthetic/decoy filters. The original decoy file/store is retained in the legacy backup and original location.

Failed sources: Common Brochure (outlined/vector text), Hostel (outlined/vector text), UG Fee Structure (image-only scan). See SOURCE_REVIEW.md for evidence and suitability recommendations. No OCR or invented chunks were added.

Recovery/rerun: stop the server and all CLI writers first. `HF_HUB_OFFLINE=1 python -m src.migrate_legacy --execute` validates the protected legacy inventory, then returns without resetting any source/cache once migration is validated. Before validation, deterministic IDs and staged upserts permit retry. Unexpected hashes, counts, statuses or ambiguous mappings abort migration.

Rollback: stop all writers, retain the new workspace/store separately, and restore the pre-migration application files from your normal application backup before pointing that version at the retained legacy data. Do not point the old unscoped application at the new collection, and do not delete either dataset. The legacy data backup is recoverable independently of application code. There is no automatic rollback command or distributed transaction.

No real-world retrieval accuracy is claimed. Source approval and benchmark gold-label review remain human tasks.
