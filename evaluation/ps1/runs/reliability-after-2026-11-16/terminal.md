# Actual terminal output

```text
[reindex] Reading manifest and hashing source files...
[reindex] Scan complete in 0.00s: 1 added, 0 modified, 0 deleted, 0 unchanged.
[reindex] [1/1] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: preparing source
  Parsing: BTech_(Rules_&_Regulations)2013_21nov2023.pdf (doc_id=p-dad105fab2ff326169e7f3b1:6584f18e-01cb-4da6-aea7-8949bdf126a7, approved=False)
    Extraction: 22 pages, 57818 chars; 0 short/empty pages; parsers=pymupdf; 0.13s
    Chunking: 114 chunks (approved=False); 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding 114 chunks...
[embeddings] Loading BAAI/bge-small-en-v1.5...
[embeddings] Model loaded in 0.20s; inference batch size=8.
[embeddings] Starting 114 chunks in batches of 8; no parallel model workers.
[embeddings] 8/114 chunks; 1.73s elapsed; 4.63 chunks/s
[embeddings] 16/114 chunks; 3.34s elapsed; 4.78 chunks/s
[embeddings] 24/114 chunks; 4.53s elapsed; 5.30 chunks/s
[embeddings] 32/114 chunks; 5.24s elapsed; 6.11 chunks/s
[embeddings] 40/114 chunks; 7.52s elapsed; 5.32 chunks/s
[embeddings] 48/114 chunks; 8.83s elapsed; 5.43 chunks/s
[embeddings] 56/114 chunks; 11.44s elapsed; 4.89 chunks/s
[embeddings] 64/114 chunks; 11.89s elapsed; 5.38 chunks/s
[embeddings] 72/114 chunks; 13.12s elapsed; 5.49 chunks/s
[embeddings] 80/114 chunks; 14.11s elapsed; 5.67 chunks/s
[embeddings] 88/114 chunks; 14.44s elapsed; 6.09 chunks/s
[embeddings] 96/114 chunks; 14.74s elapsed; 6.51 chunks/s
[embeddings] 104/114 chunks; 15.08s elapsed; 6.90 chunks/s
[embeddings] 112/114 chunks; 15.40s elapsed; 7.27 chunks/s
[embeddings] 114/114 chunks; 15.63s elapsed; 7.29 chunks/s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: embedding finished in 16.23s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: committing index update...
[store] Upserting chunks 1-100/114...
[store] Upserted 100/114 chunks; batch took 0.07s
[store] Upserting chunks 101-114/114...
[store] Upserted 114/114 chunks; batch took 0.01s
[reindex] BTech_(Rules_&_Regulations)2013_21nov2023.pdf: complete; 114 chunks; 16.68s total. Manifest saved.
[reindex] Synchronizing source-approval flags and saving manifest...
START ps1-02 raw
DONE ps1-02 raw: abstained; unsupported_cited_claim; 4 blocks
START ps1-02 hyde
  [retrieve] HyDE generation failed: ValueError
DONE ps1-02 hyde: abstained; unsupported_cited_claim; 4 blocks
START ps1-02 fusion
DONE ps1-02 fusion: abstained; unsupported_cited_claim; 5 blocks
START ps1-14 raw
DONE ps1-14 raw: abstained; no_policy_found; 5 blocks
START ps1-14 hyde
  [llm] groq failed, trying fallback...
  [retrieve] HyDE generation failed: ProviderUnavailableError
  [llm] groq failed, trying fallback...
DONE ps1-14 hyde: provider_unavailable; None; 5 blocks
START ps1-14 fusion
  [llm] groq failed, trying fallback...
  [retrieve] HyDE generation failed: ProviderUnavailableError
  [llm] groq failed, trying fallback...
DONE ps1-14 fusion: provider_unavailable; None; 5 blocks
START ps1-21 raw
  [llm] groq failed, trying fallback...
DONE ps1-21 raw: provider_unavailable; None; 4 blocks
START ps1-21 hyde
  [llm] groq failed, trying fallback...
  [retrieve] HyDE generation failed: ProviderUnavailableError
  [llm] groq failed, trying fallback...
DONE ps1-21 hyde: provider_unavailable; None; 4 blocks
START ps1-21 fusion
  [llm] groq failed, trying fallback...
  [retrieve] HyDE generation failed: ProviderUnavailableError
  [llm] groq failed, trying fallback...
DONE ps1-21 fusion: provider_unavailable; None; 4 blocks

```
