# Interrupted first ingestion: diagnosis and safe resume

## Observed bottleneck

The interruption occurred inside ONNX inference, before AEC's database commit. The original wrapper called `list(model.embed(texts))` with no batch setting. Installed FastEmbed defaults to **256 texts per inference batch**. All vectors for a document are prepared before its old/new index replacement, so little or no Chroma/manifest growth during embedding is expected. Silent generator consumption hid this stage.

AEC is 10,647,401 bytes and 72 pages. Read-only measurements found extraction took **0.398 seconds** and chunking **0.009 seconds**, yielding **373 chunks**. Its chunk body size was not reduced. Full embedding text averaged 275 characters and peaked at 1,457 characters including source headers; token counts ranged from 9 to 410, with median 36. The original first inference batch padded 256 inputs to its longest sequence of 410 tokens. That is substantial padded compute/working memory, especially on this machine's **8 GB RAM**, which was using approximately **5.14 GB swap** during diagnosis.

**Most likely cause:** a large, padded CPU inference batch under system memory pressure. The trace definitively identifies the stage, but the exact ten-minute slowdown was not replayed. No full 256-chunk stress test or full-document embedding/indexing was run during diagnosis. CPU percentages alone do not distinguish useful inference from paging/contention.

## Bounded runtime diagnostics

Only the first 32 extracted AEC chunks were embedded for diagnosis, using the existing cached model; no vectors were inserted into the production index. Each probe had a bounded subprocess timeout. No model download, model substitution, token-limit change, chunk truncation, new quantization or parallel model workers were introduced.

| Batch size | ONNX thread setting | Inference time, 32 chunks | Peak process RSS |
|---|---|---|---|
| 8 | 2 | 2.767 s | 443.5 MiB |
| 16 | 2 | 3.659 s | 541.8 MiB |
| 32 | 2 | 5.566 s | 468.0 MiB |
| 32 | Existing runtime default | 5.203 s | 511.8 MiB |
| 8 | Existing runtime default | 2.463 s | 394.9 MiB |

These are individual local probes, not a controlled corpus benchmark or a prediction of total ingestion time. An additional run through the updated wrapper took 4.417 seconds for the same 32 chunks, demonstrating normal timing variability. All outputs were finite, normalized 384-dimensional vectors. Batch-8 versus batch-32 cosine agreement was at least **0.99999978**, with a maximum absolute component difference of approximately 0.000216. Small numerical batch differences are not a claim about real retrieval accuracy.

Default batching is now **8**, configurable through `EMBED_BATCH_SIZE`. The ONNX thread setting and execution-provider selection remain unchanged: there was no evidence that a thread-setting change was necessary. The same tokenizer, cached weights, normalization, source text and chunk order are retained. The original small embedding arrays themselves were not the major memory concern; inference activations and padded sequences are.

## Python/runtime compatibility

Observed runtime: Python **3.14.9**, native **arm64**, FastEmbed **0.9.1**, ONNX Runtime **1.32.0**, tokenizers **0.23.3**, NumPy **2.5.4**, Chroma **1.5.9**. The installed ONNX wheel is explicitly tagged `cp314-cp314-macosx_14_0_arm64`; tokenizers uses an arm64 stable-ABI wheel. CPUExecutionProvider loaded the cached model successfully, and actual inference completed with valid outputs.

There is no observed Python ABI incompatibility or failed model load. This does not establish performance across every batch size or Python version; no environment downgrade/reinstall was performed. FastEmbed's installed implementation and [ONNX Runtime's threading documentation](https://onnxruntime.ai/docs/performance/tune-performance/threading.html) were inspected; batching was changed rather than guessing at unsupported-runtime or thread faults.

## Persisted state after the user's interruption

Read-only SQLite inspection and file-hash comparison found:

- One Chroma collection, **4 stored vectors**, all `decoy__performance_gig_leave`.
- All four are `is_decoy=true` and `approved=false`.
- Four corresponding queued vector records, each 1,536 bytes / 384 float32 values; no embedding missing its metadata.
- SQLite `quick_check` returned `ok`.
- Manifest contains only the decoy; its recorded content hash matches the source.
- Registry contains AEC as **pending**, with its source hash; it has **no stored vectors** and no manifest checkpoint.
- Other real PDFs have not yet been registered/indexed by that interrupted run.

This is a completed decoy plus unfinished AEC preparation, not a partially inserted AEC document. A pending registry entry is expected because registration precedes embedding. No repair/reset is needed for this observed state. The index, registry, manifest, cache and raw files were fingerprinted; all **20 protected existing files** remained unchanged during investigation and tests.

The resume command reuses the decoy checkpoint, retries AEC's entire embedding preparation, then proceeds to remaining sources. Completed embedding batches of an uncommitted document are not persisted or checkpointed. Partial embedding-batch recovery has not been added.

## Extraction-only inspection of the 10 PDFs

This inspection used `extract_pages` and `chunk_text` directly, without source registration, approval, embedding all documents, or index writes.

| PDF | Pages | Chunks | Extraction time |
|---|---:|---:|---:|
| AEC.pdf | 72 | 373 | 0.398 s |
| Common+Brochure+2026-v5-web.pdf | 12 | 0 | 6.067 s |
| Exam section PPT.pptx.pdf | 27 | 51 | 0.043 s |
| Hostel.pdf | 2 | 0 | 9.372 s |
| MALPRACTICE+MANUAL.pdf | 20 | 49 | 0.059 s |
| RAGGING+IS+A+CRIME.pdf | 1 | 1 | 0.013 s |
| Support _ Proctorial System _ Ramaiah Institute of Technology, Bengaluru.pdf | 4 | 12 | 0.028 s |
| UGCOURSE-1STYEARB.E&B.ARCHFEESSTRUCTURE2026-2027.pdf | 1 | 0 | 0.010 s |
| code_conduct_MSRIT.pdf | 6 | 15 | 0.021 s |
| contineo.pdf | 1 | 16 | 0.079 s |

**Three files return no text even after parser fallback:** brochure, hostel and fee structure. Their exact underlying cause (for example, image-only/scanned pages) was not visually verified. They require usable text-based source versions or a separate reviewed OCR workflow. No OCR feature was added. A resume will explicitly report these failures and keep them out of successful manifest checkpoints. Do not interpret a `partial_failure` report as all ten PDFs successfully indexed.

No document has been approved on the basis of this performance inspection; source provenance, applicability and content still require human review.

## Changes and tests

Application/configuration files changed:

- `src/embeddings.py`: explicit bounded batches, streaming vector conversion, visible completed counts/rate, and count validation.
- `src/config.py`, `.env.example`: positive `EMBED_BATCH_SIZE`, default 8. The actual `.env` was not changed.
- `src/ingest.py`: extraction/page/character/parser diagnostics and extraction/chunking durations, without changing extraction/chunking logic.
- `src/store.py`: timing/progress around existing 100-vector upsert batches.
- `src/reindex.py`: scan/document/stage progress, per-document timings, explicit failed stages, and rollback/re-raise for Ctrl+C during delete/upsert.
- `tests/test_embeddings.py`: new batching/order/count/failure/progress tests.
- `tests/test_index_integration.py`: interruption/retry/rollback and reporting regressions using isolated fixtures.

Documentation updated: this report, `DECISIONS.md`, `PROMPTS.md`, `INTERVIEW_NOTES.md` and the resume note in `docs/OPERATIONS.md`.

`python -m pytest tests/ -q -p no:cacheprovider`: **197 passed**, six existing dependency deprecation warnings. A focused indexing/guardrail/parser test run also passed. Tests used temporary databases/registries and did not mutate the production documents or state. Source-approval and decoy/synthetic-isolation regression tests passed.

Rollback now covers a normal Ctrl+C during deletion/insertion as well as preparation. This does not provide crash-proof cross-process transactions or protection from repeated forced termination/SIGKILL. Stop the server and any other index writers before CLI indexing, as already required by the local single-process architecture.

## Exact safe resume command — not executed by the agent

```bash
cd /Users/shreshthagrawal/Documents/DELL_DEMO/ps1-policy-assistant
EMBED_BATCH_SIZE=8 python -u -m src.reindex
```

This one-command environment override guarantees the bounded batch size without editing `.env`. Keep the existing Chroma directory, manifest and registry. Do not use `--reset`. Expect per-stage progress and an explicit report for the three documents whose text cannot currently be extracted. Review/approve successfully indexed real document versions only after content/provenance verification; indexing itself does not approve them.
