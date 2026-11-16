# HyDE improvement progress

Status — payload authorization granted; live evaluation incomplete due Groq daily-token quota and empty-content responses. No disposable worker is running. No candidates frozen, no default change, no production/API-mode integration.

Completed

- Seed 20261114; TUNE Examination_Rules.pdf and unopened HOLD-OUT NIT_Goa_Regulations.pdf.
- 23 eligible TUNE questions after exact page-quote and indexed-gold checks. Labels remain unverified by humans.
- Local Raw baseline complete, 18/23 rank-1 hits, 21/23 rank-3 hits, MRR 0.841. See raw-summary.json.
- One V1/V2 pair and one additional V1 generation cached. Full variant comparison is unavailable.
- Groq reports daily-token limit 200000 with usage 199646. Initial 413 handled via batching; repeated 429 retries and empty content are separate failures.
- Final 283 Python tests passed; both JS DOM suites passed. All 219 protected hashes match.
- Research scaffold, caches, logs, backups and report persisted. README, DECISIONS and PROMPTS contain research-status notes only.

Next steps

1. Resume after provider quota recovers. No new authorization is needed for the already approved payloads.
2. Complete V2 length validation, gold uniqueness checks and latency/cost bookkeeping before claiming a complete ablation.
3. Finish TUNE V1/V2/averaging/RRF and routing sweeps, inspect at least 20 V1/V2 pairs, then freeze at most three configurations.
4. Generate fresh held-out questions. Complete held-out comparisons, negatives and prompt-isolation E2E checks. The prepared e2e.py has not run and does not yet compare experimental candidates.
5. Integrate only validated configurable modes with tests, preserve the threshold, and apply all acceptance rules before changing any default.

See HYDE_REPORT.md for exact limitations, counts, commands and revert locations.
