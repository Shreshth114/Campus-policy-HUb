# Production-integrity observation

Checked at 2026-11-16T11:58:33.421758+00:00.

- Starting files: 237; current files: 243.
- Original files unchanged: 235.
- Original files changed: 2; new files: 6; removed files: 0.
- Therefore the full starting production snapshot is NOT byte-identical. Do not claim otherwise.

Changed original files:

- `.chroma-institutions/chroma.sqlite3`
- `data/personal_workspaces.json`

New files are under one personal synthetic-demo workspace. Capability-bearing paths are deliberately not recorded. Basenames: `test_queries.jsonl`, `answer_cache.json`, `hyde_cache.json`, `index_activity.json`, `manifest.json`, `source_registry.json`.

The new workspace metadata was created at approximately 11:45:46 UTC. The running server session recorded POST /personal/demo responses of 409 and 200. This is consistent with concurrent live demo use, but caller identity is not established. The automated Python fixtures use temporary scoped storage; the four JavaScript suites mock fetch; the single direct Groq smoke script does not call the application or Chroma. No cleanup, rollback or shared-database access was performed to hide these differences.

Original PDF and frozen ten-case label hashes still match the existing manifest. All other original protected file hashes match. Institutional vector-record identity cannot be confirmed from a changed shared database file without a suitable prior record snapshot; none was opened or rewritten to investigate.

Keep this integrity observation separate from application test success. A future frozen run needs a quiet or isolated environment and before/after record/file snapshots.
