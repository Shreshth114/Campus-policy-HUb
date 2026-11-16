# Groq-only baseline: actual observed failures

Executed 16 November 2026 against `openai/gpt-oss-120b` through the existing unified client. User authorized Groq only. The disposable runner replaced its local fallback object with a disabled provider; application configuration was not changed. The client's generic “trying fallback” log does not indicate a Gemini request: no fallback was configured in this runner.

## Execution scope

Three diagnostic questions × three modes = nine completed application attempts. Disposable real-PDF index: 22 pages, 114 chunks, existing embedding model/settings. Answer and HyDE caches disabled. This is a small, deliberately selected attendance diagnostic, not a representative accuracy benchmark. Labels remain unverified. All 244 production files matched their pre-run SHA-256 snapshots.

| Question | Mode | Top page | Top cosine | Application result | Wall seconds |
|---|---|---:|---:|---|---:|
| Medical condonation thresholds (ps1-02) | Raw | 10 | 0.783 | citation_check_failed | 1.41 |
| ps1-02 | HyDE | 10 | 0.809 | citation_check_failed | 2.62 |
| ps1-02 | Fusion | 10 | 0.793 | citation_check_failed | 4.81 |
| Sick, missed classes, still write finals? (ps1-14) | Raw | 11 | 0.666 | citation_check_failed | 1.39 |
| ps1-14 | HyDE | 10 | 0.798 | citation_check_failed | 2.51 |
| ps1-14 | Fusion | 11 | 0.703 | citation_check_failed | 2.32 |
| Thresholds, process and medical deadline (ps1-21) | Raw | 10 | 0.680 | provider_unavailable | 1.41 |
| ps1-21 | HyDE | 10 | 0.815 | provider_unavailable | 7.88 |
| ps1-21 | Fusion | 10 | 0.680 | provider_unavailable; HyDE fallback | 9.85 |

Cosine numbers across different query embeddings are not directly comparable relevance scores. Fusion retains best-path cosine and uses RRF separately. The full report includes every retrieved block and its RRF value. Do not interpret a larger cosine as proven improvement.

## Actual generated answers

For ps1-02, Raw returned:

> At least 80 % attendance in the non-medical period, and the overall attendance—including the medical-leave period—must not drop below 75 %【C1】.

This display normalizes Unicode spacing; exact bytes and the accompanying source quotation are in `ps1-02-raw.json`. All three modes used `【C1】` instead of the required `[C1]`. The citation parser rejects that form. The threshold pair is supported, but the answer also omits material qualifications including AAC discretion. Fixing citation syntax alone would not make the answer fully qualified.

For ps1-14, the actual Raw output was:

> Yes—you may request a make-up exam

HyDE returned “Yes, you can request a make-up exam by applying to the”, and Fusion stopped at “Yes—you can request a make-up exam by applying to the Head of Department (or first”. All three lacked citations and were visibly incomplete. Each response used exactly the configured **350 output tokens**, despite only 34/54/82 visible characters. This strongly suggests the reasoning model's output budget was consumed before a complete visible answer, but the provider adapter does not retain finish_reason or reasoning-token details, so token exhaustion is not conclusively diagnosed from those fields alone. Do not raise limits blindly before capturing that metadata.

For ps1-21, no usable answer content was obtained. The existing unified client reports ProviderUnavailableError; its generic error serialization hides some nested reasons. Terminal output records at least one Groq 429 TPM error: limit 8,000, used 7,404, requested 1,048, retry suggested after 3.39 seconds. Other “groq failed” lines cannot be attributed definitively to rate limiting versus empty content from the saved wrapper error alone.

## Retrieval differences worth inspecting

The informal scenario (ps1-14) is an actual observed difference: Raw ranked page 11 (make-up examinations) first, while HyDE ranked page 10 (medical attendance condonation) first; Fusion ranked page 11 first. The question says missed classes rather than missed an examination, so page 10 appears more relevant on manual inspection. This is a candidate HyDE win, pending human target review—not a measured benchmark result. The direct threshold question retrieved page 10 first in all modes, a likely tie at that coarse level.

Actual HyDE passages invented policy details: for example 75% cumulative attendance, a five-day certificate deadline, and, for ps1-21, a 55% lower limit. These were search keys only. Inspection of captured answer messages confirms the generated passages were not injected as authoritative excerpts. Nonetheless, invented details can distort search direction; prompt quality and retrieval outcomes need independent evaluation.

## Next changes to consider after reviewing records

1. Capture Groq finish_reason and reasoning/visible-token usage and preserve sanitized nested provider failures. This is needed to distinguish truncation, empty content and quota exhaustion.
2. Enforce the requested citation format or safely canonicalize only recognized equivalent labels before the existing checks. Keep exact-source and qualification validation active.
3. Investigate complete qualified answers within a deliberate reasoning/output budget. All answers in this pilot failed; retrieval improvements alone will not resolve this.
4. Examine the actual HyDE generations and introduce a tested instruction against invented numeric details, then compare using fixed reviewed targets. Do not tune on the proposed holdout cases used here.
5. Pace provider calls to remain within actual limits. Report provider failures separately from retrieval misses.

No application code or settings were modified in response to these failures. The only change for execution was to the diagnostic runner's local provider selection.

## Evaluation-design disclosure

ps1-02 and ps1-14 were originally tagged proposed holdout in the draft set and have now been inspected diagnostically. They must not be represented as untouched holdout examples in a future tuned evaluation. Reserve fresh final questions before tuning. No official label was promoted or edited.

## Artifacts

- `REPORT.md`: every question/mode, generated HyDE and answer text, application result, full retrieved text, exact sent excerpts, cosine/RRF scores, timings and usage.
- Nine `ps1-*.json` records: complete prompt message arrays, response metadata, claim-failure details and trace.
- `terminal.txt`: actual process output, with organization identifier redacted.
- `metadata.json`, `index_setup.json`, `integrity.json`: run settings, isolated indexing and production-integrity evidence.
