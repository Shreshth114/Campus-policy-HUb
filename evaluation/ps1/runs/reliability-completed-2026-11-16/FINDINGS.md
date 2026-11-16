# Final diagnostic outcomes

Actual Groq-only execution using a disposable 114-chunk index and the same three diagnostic questions. This is repeated development evidence, not a verified held-out accuracy benchmark. Caches disabled. Final application output may include clearly disclosed, verbatim source-condition additions; raw LLM output remains separately recorded.

| Case | Mode | Outcome | HyDE fallback | Finish | Output/reasoning tokens | Source conditions appended |
|---|---|---|---|---|---|---|
| ps1-02 | fusion | answered / passed | True | stop | 86/23 | True |
| ps1-02 | hyde | answered / passed | False | stop | 78/15 | True |
| ps1-02 | raw | answered / passed | False | stop | 86/23 | True |
| ps1-14 | fusion | abstained / quote_verification_failed | False | stop | 214/21 | False |
| ps1-14 | hyde | answered / passed | False | stop | 149/30 | True |
| ps1-14 | raw | answered / passed | False | stop | 130/11 | True |
| ps1-21 | fusion | answered / passed | True | stop | 271/93 | True |
| ps1-21 | hyde | answered / passed | True | stop | 223/18 | False |
| ps1-21 | raw | answered / passed | False | stop | 271/93 | True |

Accepted application responses: **8/9**, compared with 0/9 in the earlier paced diagnostic. This is not an accuracy estimate. The failed case(s) remain withheld.

Material changes: full-provision selection with event cues; bounded evidence-size output allowance; exact-quotation generation; strict whitespace/citation normalization; explicit missing-source-qualification completion only when the model generated valid quotations and no other substantive content. Grounding checks remain active after completion.

The repeated cases have been used for repair. Fresh final labels remain pending human decisions. No claim of statistical significance, unseen-document generalization or HyDE superiority is made.

Compare-mode in-flight HyDE sharing is tested separately; independent diagnostic attempts intentionally use separate uncached calls. HyDE fallback attempts cannot establish HyDE quality.

All prompts, raw outputs, final application answers, selected excerpts, rankings, cosine/RRF scores, validation reasons and usage are in [REPORT.md](REPORT.md) and the adjacent JSON records.