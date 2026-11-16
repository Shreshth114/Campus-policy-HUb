# Actual terminal output

```text
[reindex] Reading manifest and hashing source files...
[reindex] Scan complete in 0.00s: 1 added, 0 modified, 0 deleted, 0 unchanged.
[reindex] [1/1] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: preparing source
  Parsing: BTech_(Rules_&_Regulations)2013_21nov2023.pdf (doc_id=p-663d932e05d3b994f434cb08:3612e346-1881-4293-9437-099aa585e1ce, approved=False)
    Extraction: 22 pages, 57818 chars; 0 short/empty pages; parsers=pymupdf; 0.13s
    Chunking: 114 chunks (approved=False); 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding 114 chunks...
[embeddings] Loading BAAI/bge-small-en-v1.5...
[embeddings] Model loaded in 0.33s; inference batch size=8.
[embeddings] Starting 114 chunks in batches of 8; no parallel model workers.
[embeddings] 8/114 chunks; 2.98s elapsed; 2.69 chunks/s
[embeddings] 16/114 chunks; 8.27s elapsed; 1.93 chunks/s
[embeddings] 24/114 chunks; 10.31s elapsed; 2.33 chunks/s
[embeddings] 32/114 chunks; 11.32s elapsed; 2.83 chunks/s
[embeddings] 40/114 chunks; 13.29s elapsed; 3.01 chunks/s
[embeddings] 48/114 chunks; 15.00s elapsed; 3.20 chunks/s
[embeddings] 56/114 chunks; 16.99s elapsed; 3.30 chunks/s
[embeddings] 64/114 chunks; 17.56s elapsed; 3.65 chunks/s
[embeddings] 72/114 chunks; 18.87s elapsed; 3.82 chunks/s
[embeddings] 80/114 chunks; 20.29s elapsed; 3.94 chunks/s
[embeddings] 88/114 chunks; 20.76s elapsed; 4.24 chunks/s
[embeddings] 96/114 chunks; 21.10s elapsed; 4.55 chunks/s
[embeddings] 104/114 chunks; 21.42s elapsed; 4.85 chunks/s
[embeddings] 112/114 chunks; 21.76s elapsed; 5.15 chunks/s
[embeddings] 114/114 chunks; 22.00s elapsed; 5.18 chunks/s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding finished in 22.78s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: committing index update...
[store] Upserting chunks 1-100/114...
[store] Upserted 100/114 chunks; batch took 0.08s
[store] Upserting chunks 101-114/114...
[store] Upserted 114/114 chunks; batch took 0.02s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: complete; 114 chunks; 23.21s total. Manifest saved.
[reindex] Synchronizing source-approval flags and saving manifest...
START fresh-01 raw
DONE fresh-01 raw: abstained; no_policy_found; 5 blocks
START fresh-01 hyde
  [retrieve] HyDE generation failed: ValueError
DONE fresh-01 hyde: abstained; no_policy_found; 5 blocks
START fresh-01 fusion
DONE fresh-01 fusion: abstained; no_policy_found; 5 blocks
START fresh-02 hyde
DONE fresh-02 hyde: abstained; no_policy_found; 4 blocks
START fresh-02 fusion
  [retrieve] HyDE generation failed: ValueError
DONE fresh-02 fusion: abstained; quote_verification_failed; 5 blocks
START fresh-02 raw
DONE fresh-02 raw: abstained; quote_verification_failed; 5 blocks
START fresh-03 fusion
DONE fresh-03 fusion: answered; None; 5 blocks
START fresh-03 raw
DONE fresh-03 raw: abstained; quote_verification_failed; 4 blocks
START fresh-03 hyde
DONE fresh-03 hyde: abstained; no_policy_found; 5 blocks
START fresh-04 raw
DONE fresh-04 raw: answered; None; 5 blocks
START fresh-04 hyde
DONE fresh-04 hyde: abstained; quote_verification_failed; 5 blocks
START fresh-04 fusion
DONE fresh-04 fusion: abstained; quote_verification_failed; 5 blocks
START fresh-05 hyde
DONE fresh-05 hyde: answered; None; 5 blocks
START fresh-05 fusion
  [llm] groq failed, trying fallback...
  [retrieve] HyDE generation failed: ProviderUnavailableError
DONE fresh-05 fusion: abstained; unsupported_cited_claim; 3 blocks
START fresh-05 raw
DONE fresh-05 raw: abstained; unsupported_cited_claim; 3 blocks
START fresh-06 fusion
DONE fresh-06 fusion: abstained; no_policy_found; 4 blocks
START fresh-06 raw
DONE fresh-06 raw: answered; None; 4 blocks
START fresh-06 hyde
  [retrieve] HyDE generation failed: ValueError
DONE fresh-06 hyde: abstained; no_policy_found; 4 blocks
START fresh-07 raw
DONE fresh-07 raw: answered; None; 3 blocks
START fresh-07 hyde
DONE fresh-07 hyde: answered; None; 3 blocks
START fresh-07 fusion
DONE fresh-07 fusion: answered; None; 4 blocks
START fresh-08 hyde
  [retrieve] HyDE generation failed: ValueError
DONE fresh-08 hyde: answered; None; 3 blocks
START fresh-08 fusion
  [retrieve] HyDE generation failed: ValueError
DONE fresh-08 fusion: answered; None; 3 blocks
START fresh-08 raw
DONE fresh-08 raw: answered; None; 3 blocks
START fresh-09 fusion
DONE fresh-09 fusion: clarification_required; None; 0 blocks
START fresh-09 raw
DONE fresh-09 raw: clarification_required; None; 0 blocks
START fresh-09 hyde
DONE fresh-09 hyde: clarification_required; None; 0 blocks
START fresh-10 raw
DONE fresh-10 raw: abstained; no_policy_found; 4 blocks
START fresh-10 hyde
  [retrieve] HyDE generation failed: ValueError
DONE fresh-10 hyde: abstained; no_policy_found; 4 blocks
START fresh-10 fusion
  [retrieve] HyDE generation failed: ValueError
DONE fresh-10 fusion: abstained; no_policy_found; 4 blocks

```
