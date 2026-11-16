# Operations

The former global data/raw and unscoped reindex commands are retired. The legacy directories are retained only for recovery and audit.

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for current commands, [API.md](API.md) for authenticated operations, and [MIGRATION_REPORT.md](MIGRATION_REPORT.md) for preserved data. Every indexing/benchmark command now requires `--institution-id UUID`. Never run a CLI writer beside the single-process server. Global resets are disabled.
