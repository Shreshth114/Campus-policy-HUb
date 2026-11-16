# Actual terminal output

```text
[reindex] Reading manifest and hashing source files...
[reindex] Scan complete in 0.00s: 1 added, 0 modified, 0 deleted, 0 unchanged.
[reindex] [1/1] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: preparing source
  Parsing: BTech_(Rules_&_Regulations)2013_21nov2023.pdf (doc_id=p-6ddc186c4533aefad995932a:96a1b7d0-6bcf-465e-aa48-8d42cf066587, approved=False)
    Extraction: 22 pages, 57818 chars; 0 short/empty pages; parsers=pymupdf; 0.12s
    Chunking: 114 chunks (approved=False); 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding 114 chunks...
[embeddings] Loading BAAI/bge-small-en-v1.5...
[embeddings] Model loaded in 0.22s; inference batch size=8.
[embeddings] Starting 114 chunks in batches of 8; no parallel model workers.
[embeddings] 8/114 chunks; 1.87s elapsed; 4.28 chunks/s
[embeddings] 16/114 chunks; 4.08s elapsed; 3.92 chunks/s
[embeddings] 24/114 chunks; 5.98s elapsed; 4.02 chunks/s
[embeddings] 32/114 chunks; 6.99s elapsed; 4.58 chunks/s
[embeddings] 40/114 chunks; 9.27s elapsed; 4.32 chunks/s
[embeddings] 48/114 chunks; 10.74s elapsed; 4.47 chunks/s
[embeddings] 56/114 chunks; 12.14s elapsed; 4.61 chunks/s
[embeddings] 64/114 chunks; 12.53s elapsed; 5.11 chunks/s
[embeddings] 72/114 chunks; 13.70s elapsed; 5.26 chunks/s
[embeddings] 80/114 chunks; 15.37s elapsed; 5.20 chunks/s
[embeddings] 88/114 chunks; 15.98s elapsed; 5.51 chunks/s
[embeddings] 96/114 chunks; 16.59s elapsed; 5.79 chunks/s
[embeddings] 104/114 chunks; 17.00s elapsed; 6.12 chunks/s
[embeddings] 112/114 chunks; 17.43s elapsed; 6.42 chunks/s
[embeddings] 114/114 chunks; 17.69s elapsed; 6.44 chunks/s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding finished in 18.32s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: committing index update...
[store] Upserting chunks 1-100/114...
[store] Upserted 100/114 chunks; batch took 0.07s
[store] Upserting chunks 101-114/114...
[store] Upserted 114/114 chunks; batch took 0.02s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: complete; 114 chunks; 18.81s total. Manifest saved.
[reindex] Synchronizing source-approval flags and saving manifest...
START ps1-02 raw
DONE ps1-02 raw: answered; None; 4 blocks
START ps1-02 hyde
DONE ps1-02 hyde: answered; None; 5 blocks
START ps1-02 fusion
  [retrieve] HyDE generation failed: ValueError
DONE ps1-02 fusion: answered; None; 4 blocks
START ps1-14 raw
DONE ps1-14 raw: answered; None; 5 blocks
START ps1-14 hyde
DONE ps1-14 hyde: answered; None; 5 blocks
START ps1-14 fusion
DONE ps1-14 fusion: abstained; quote_verification_failed; 5 blocks
START ps1-21 raw
DONE ps1-21 raw: answered; None; 4 blocks
START ps1-21 hyde
  [retrieve] HyDE generation failed: ValueError
DONE ps1-21 hyde: answered; None; 4 blocks
START ps1-21 fusion
  [retrieve] HyDE generation failed: ValueError
DONE ps1-21 fusion: answered; None; 4 blocks

```
