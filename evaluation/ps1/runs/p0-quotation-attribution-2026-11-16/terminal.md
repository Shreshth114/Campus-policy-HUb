# Actual terminal output

```text
[reindex] Reading manifest and hashing source files...
[reindex] Scan complete in 0.00s: 1 added, 0 modified, 0 deleted, 0 unchanged.
[reindex] [1/1] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: preparing source
  Parsing: BTech_(Rules_&_Regulations)2013_21nov2023.pdf (doc_id=p-59ead16fdfcdf8426f127f4d:af824e4a-2d4a-4415-af7b-185e41afe841, approved=False)
    Extraction: 22 pages, 57818 chars; 0 short/empty pages; parsers=pymupdf; 0.13s
    Chunking: 114 chunks (approved=False); 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding 114 chunks...
[embeddings] Loading BAAI/bge-small-en-v1.5...
[embeddings] Model loaded in 0.29s; inference batch size=8.
[embeddings] Starting 114 chunks in batches of 8; no parallel model workers.
[embeddings] 8/114 chunks; 2.59s elapsed; 3.09 chunks/s
[embeddings] 16/114 chunks; 4.71s elapsed; 3.40 chunks/s
[embeddings] 24/114 chunks; 6.19s elapsed; 3.88 chunks/s
[embeddings] 32/114 chunks; 6.96s elapsed; 4.60 chunks/s
[embeddings] 40/114 chunks; 8.70s elapsed; 4.60 chunks/s
[embeddings] 48/114 chunks; 9.85s elapsed; 4.87 chunks/s
[embeddings] 56/114 chunks; 10.85s elapsed; 5.16 chunks/s
[embeddings] 64/114 chunks; 11.17s elapsed; 5.73 chunks/s
[embeddings] 72/114 chunks; 12.21s elapsed; 5.90 chunks/s
[embeddings] 80/114 chunks; 13.61s elapsed; 5.88 chunks/s
[embeddings] 88/114 chunks; 13.98s elapsed; 6.30 chunks/s
[embeddings] 96/114 chunks; 14.39s elapsed; 6.67 chunks/s
[embeddings] 104/114 chunks; 14.71s elapsed; 7.07 chunks/s
[embeddings] 112/114 chunks; 15.16s elapsed; 7.39 chunks/s
[embeddings] 114/114 chunks; 15.46s elapsed; 7.37 chunks/s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding finished in 16.22s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: committing index update...
[store] Upserting chunks 1-100/114...
[store] Upserted 100/114 chunks; batch took 0.08s
[store] Upserting chunks 101-114/114...
[store] Upserted 114/114 chunks; batch took 0.02s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: complete; 114 chunks; 16.75s total. Manifest saved.
[reindex] Synchronizing source-approval flags and saving manifest...
START ps1-14 fusion
DONE ps1-14 fusion: answered; None; 5 blocks

```
