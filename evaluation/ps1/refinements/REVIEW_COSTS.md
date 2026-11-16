# Coverage-review cost observations

Historical observations from the prior implementation, before the new per-requirement ledger. A single new-ledger smoke observation is recorded separately below. The ledger changes prompt/output length; its general latency/token overhead is not established by one observation. These two observations are not a latency benchmark.

| Prior development case | Provider review latency ms | Input tokens | Output tokens | Reasoning tokens (included in output) |
| --- | --- | --- | --- | --- |
| dev-attendance | 1320.63 | 1444 | 203 | 158 |
| dev-reinstatement | 1635.09 | 1249 | 207 | 173 |

Prior median successful review provider latency: 1477.86 ms. Total reported review input/output tokens: 2693/410.

One additional review call is made per deterministically valid fresh selection. Early gate failures/insufficient selections do not incur it; valid cache hits reuse the version-bound review proof. Provider retries, failures, waits and reported/missing usage must be logged separately. Provider latency is not full wall-clock overhead. Monetary cost requires an explicitly supplied current pricing schedule; none is assumed here.

For the next frozen evaluation record per call: prompt/version hash, model/provider, start/end wall time, provider latency, input/output/reasoning tokens, finish reason, retry/fallback status and usage completeness. Compare selection-only and selection+review timing without changing the deployed safety decision. Do not add reasoning tokens to output tokens again.

## New-ledger schema smoke observation

One direct Groq-only review call used a preselected pair of summer-registration provisions, without retrieval, indexing or generation. It is not human-graded or held-out. Model: `openai/gpt-oss-120b`; finish: `stop`; provider latency **1563.50 ms**; measured wall time **1564.27 ms**; **911 input / 291 output tokens**, with **92 reasoning tokens included in output**.

The model returned a negative verdict and only Q0, omitting Q1 and Q2. The full selection would be withheld. Its reasoning treated the student's requested exemption as an asserted answer claim. This is a human-adjudication candidate, not a manufactured false-rejection label. Exact messages/raw response/usage: `LIVE_REVIEW_SMOKE.md`. Do not compare these tokens directly with the earlier two calls: evidence and prompt lengths differ. No additional call was made to obtain a favorable result.
