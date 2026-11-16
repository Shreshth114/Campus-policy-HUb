# Actual after-change outcomes

| Case | Mode | Decision/reason | HyDE fallback | Finish / reasoning / output tokens |
|---|---|---|---|---|
| ps1-02 | fusion | abstained: unsupported_cited_claim | True | stop / 41 / 88 |
| ps1-02 | hyde | abstained: unsupported_cited_claim | False | stop / 35 / 140 |
| ps1-02 | raw | abstained: unsupported_cited_claim | False | stop / 35 / 143 |
| ps1-14 | fusion | abstained: no_policy_found | False | stop / 45 / 57 |
| ps1-14 | hyde | abstained: quote_verification_failed | False | stop / 28 / 117 |
| ps1-14 | raw | abstained: no_policy_found | False | stop / 49 / 61 |
| ps1-21 | fusion | abstained: unsupported_cited_claim | True | stop / 116 / 220 |
| ps1-21 | hyde | abstained: incomplete_generation | True | length / 116 / 350 |
| ps1-21 | raw | abstained: incomplete_generation | False | length / 163 / 350 |

**0/9 accepted answers.** No claim of improved accuracy or complete reliability. All nine real attempts completed without provider_unavailable after pacing. Compare the original run: six citation syntax failures and three provider failures. Current failures are four unsupported-claim/qualification abstentions, two NO_POLICY_FOUND responses, one quotation failure, and two token-limited generations.

The low-reasoning setting reduced reasoning consumption for the direct question but did not make the output complete. The full-condition question still exhausted 350 completion tokens. Unknown finish details from the original baseline cannot be reconstructed. Both prompt variation and intent cues changed retrieval, so this is a diagnostic comparison, not a controlled isolated-effect ablation.

See [full outputs](REPORT.md), which retain actual source text, prompts, provider outputs and usage. Credentials and workspace capabilities are excluded.