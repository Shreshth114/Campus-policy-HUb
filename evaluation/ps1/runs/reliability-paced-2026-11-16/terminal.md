# Actual terminal output

```text
[reindex] Reading manifest and hashing source files...
[reindex] Scan complete in 0.00s: 1 added, 0 modified, 0 deleted, 0 unchanged.
[reindex] [1/1] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: preparing source
  Parsing: BTech_(Rules_&_Regulations)2013_21nov2023.pdf (doc_id=p-fc4400b86c45ec104c0a932e:991d80fa-4b47-4787-9542-f1d045a25c2e, approved=False)
    Extraction: 22 pages, 57818 chars; 0 short/empty pages; parsers=pymupdf; 0.13s
    Chunking: 114 chunks (approved=False); 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding 114 chunks...
[embeddings] Loading BAAI/bge-small-en-v1.5...
[embeddings] Model loaded in 0.21s; inference batch size=8.
[embeddings] Starting 114 chunks in batches of 8; no parallel model workers.
[embeddings] 8/114 chunks; 1.74s elapsed; 4.59 chunks/s
[embeddings] 16/114 chunks; 3.37s elapsed; 4.75 chunks/s
[embeddings] 24/114 chunks; 4.47s elapsed; 5.37 chunks/s
[embeddings] 32/114 chunks; 5.04s elapsed; 6.34 chunks/s
[embeddings] 40/114 chunks; 6.56s elapsed; 6.10 chunks/s
[embeddings] 48/114 chunks; 7.42s elapsed; 6.47 chunks/s
[embeddings] 56/114 chunks; 8.14s elapsed; 6.88 chunks/s
[embeddings] 64/114 chunks; 8.38s elapsed; 7.64 chunks/s
[embeddings] 72/114 chunks; 9.11s elapsed; 7.91 chunks/s
[embeddings] 80/114 chunks; 10.10s elapsed; 7.92 chunks/s
[embeddings] 88/114 chunks; 10.41s elapsed; 8.45 chunks/s
[embeddings] 96/114 chunks; 10.77s elapsed; 8.91 chunks/s
[embeddings] 104/114 chunks; 11.02s elapsed; 9.44 chunks/s
[embeddings] 112/114 chunks; 11.29s elapsed; 9.92 chunks/s
[embeddings] 114/114 chunks; 11.49s elapsed; 9.92 chunks/s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding finished in 12.06s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: committing index update...
[store] Upserting chunks 1-100/114...
[store] Upserted 100/114 chunks; batch took 0.07s
[store] Upserting chunks 101-114/114...
[store] Upserted 114/114 chunks; batch took 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: complete; 114 chunks; 12.53s total. Manifest saved.
[reindex] Synchronizing source-approval flags and saving manifest...
START ps1-02 raw
DONE ps1-02 raw: abstained; unsupported_cited_claim; 4 blocks
START ps1-02 hyde
DONE ps1-02 hyde: abstained; unsupported_cited_claim; 5 blocks
START ps1-02 fusion
  [retrieve] HyDE generation failed: ValueError
DONE ps1-02 fusion: abstained; unsupported_cited_claim; 4 blocks
START ps1-14 raw
DONE ps1-14 raw: abstained; no_policy_found; 5 blocks
START ps1-14 hyde
DONE ps1-14 hyde: abstained; quote_verification_failed; 5 blocks
START ps1-14 fusion
DONE ps1-14 fusion: abstained; no_policy_found; 5 blocks
START ps1-21 raw
DONE ps1-21 raw: abstained; incomplete_generation; 4 blocks
START ps1-21 hyde
  [retrieve] HyDE generation failed: ValueError
DONE ps1-21 hyde: abstained; incomplete_generation; 4 blocks
START ps1-21 fusion
  [retrieve] HyDE generation failed: ValueError
DONE ps1-21 fusion: abstained; unsupported_cited_claim; 4 blocks

```
