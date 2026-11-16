# Structured grounding development diagnostic

Run: `structured-grounding-development-2026-11-16`. Development observations only; no accuracy labels or benchmark score.

Groq only; fallback disabled locally. Original PDF copied into disposable storage; temporary 114-chunk index removed on exit. Production indexes were not opened by this runner.

## dev-attendance

According to the uploaded B.Tech regulations, what is the minimum attendance required for medical condonation, and what is the minimum overall attendance allowed?

Decision: **abstained**. Reason: `invalid_answer_contract`. Elapsed request: 1.651s.

Raw generation:

```json
{"status":"answer","claims":[{"quote":"B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.","source":"C1"},{"quote":"B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.","source":"C1"}]}
```

Selection failures:

```json
[
  {
    "reason": "incomplete_or_nonliteral_provision",
    "label": "C1",
    "quote": "B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%."
  },
  {
    "reason": "incomplete_or_nonliteral_provision",
    "label": "C1",
    "quote": "B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%."
  }
]
```

Coverage review:

Not run: selection rejected, model abstained, or provider unavailable.

Final application answer:

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

Quotation attribution:

```json
{
  "verified": [],
  "failed": []
}
```

Usage:

```json
{
  "answer": {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "latency_ms": 1455.2459716796875,
    "input_tokens": 1336,
    "output_tokens": 249,
    "finish_reason": "stop",
    "reasoning_tokens": 109,
    "tokens_estimated_before": 2347,
    "tokens_estimated_after": 1544
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-development-2026-11-16/dev-attendance-raw.json)

## dev-compound

If I pay my semester fees after classes start, how much is the late fee, and by when must I pay?

Decision: **abstained**. Reason: `no_policy_found`. Elapsed request: 3.154s.

Raw generation:

```json
{"status":"insufficient","claims":[]}
```

Selection failures:

```json
[
  {
    "reason": "model_abstained"
  }
]
```

Coverage review:

Not run: selection rejected, model abstained, or provider unavailable.

Final application answer:

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

Quotation attribution:

```json
{
  "verified": [],
  "failed": []
}
```

Usage:

```json
{
  "answer": {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "latency_ms": 3074.939966201782,
    "input_tokens": 962,
    "output_tokens": 37,
    "finish_reason": "stop",
    "reasoning_tokens": 19,
    "tokens_estimated_before": 1321,
    "tokens_estimated_after": 1067
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-development-2026-11-16/dev-compound-raw.json)

## dev-reinstatement

I temporarily discontinued my B.Tech studies for a semester. What is the procedure to return and register again?

Decision: **provider_unavailable**. Reason: `none`. Elapsed request: 0.128s.

Raw generation:

```json
No successful generation; see provider error in machine record.
```

Selection failures:

```json
[]
```

Coverage review:

Not run: selection rejected, model abstained, or provider unavailable.

Final application answer:

The AI provider is rate-limited. Retrying in 45 seconds

Quotation attribution:

```json
{}
```

Usage:

```json
{}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-development-2026-11-16/dev-reinstatement-raw.json)

## Integrity

```json
{
  "files_checked": 237,
  "byte_identical": true
}
```

The frozen settings record contains exact source-code, model, prompt and input-PDF hashes. No label verification or approval was performed.
