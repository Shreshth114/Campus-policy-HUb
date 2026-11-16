# Structured grounding development diagnostic

Run: `structured-grounding-selection-2026-11-16`. Development observations only; no accuracy labels or benchmark score.

Groq only; fallback disabled locally. Original PDF copied into disposable storage; temporary 114-chunk index removed on exit. Production indexes were not opened by this runner.

## dev-attendance

According to the uploaded B.Tech regulations, what is the minimum attendance required for medical condonation, and what is the minimum overall attendance allowed?

Decision: **answered**. Reason: `none`. Elapsed request: 3.042s.

Raw generation:

```json
{"status":"answer","claims":[{"provision":"P4","source":"C1"}]}
```

Selection failures:

```json
[]
```

Coverage review:

```json
{
  "relevant": true,
  "complete": true,
  "qualifications_preserved": true,
  "supported": true,
  "reasons": []
}
```

Final application answer:

"B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C1]

Quotation attribution:

```json
{
  "verified": [
    {
      "quote": "B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.",
      "labels": [
        "C1"
      ]
    }
  ],
  "failed": []
}
```

Usage:

```json
{
  "answer_review": {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "latency_ms": 1320.6288814544678,
    "input_tokens": 1444,
    "output_tokens": 203,
    "finish_reason": "stop",
    "reasoning_tokens": 158
  },
  "answer": {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "latency_ms": 1429.034948348999,
    "input_tokens": 1457,
    "output_tokens": 158,
    "finish_reason": "stop",
    "reasoning_tokens": 129,
    "tokens_estimated_before": 2406,
    "tokens_estimated_after": 1657
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-selection-2026-11-16/dev-attendance-raw.json)

## dev-compound

If I pay my semester fees after classes start, how much is the late fee, and by when must I pay?

Decision: **abstained**. Reason: `no_policy_found`. Elapsed request: 28.490s.

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
    "latency_ms": 1253.4070014953613,
    "input_tokens": 1050,
    "output_tokens": 34,
    "finish_reason": "stop",
    "reasoning_tokens": 16,
    "tokens_estimated_before": 1380,
    "tokens_estimated_after": 1157
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-selection-2026-11-16/dev-compound-raw.json)

## dev-reinstatement

I temporarily discontinued my B.Tech studies for a semester. What is the procedure to return and register again?

Decision: **abstained**. Reason: `no_policy_found`. Elapsed request: 1.981s.

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
    "latency_ms": 1785.8750820159912,
    "input_tokens": 1190,
    "output_tokens": 51,
    "finish_reason": "stop",
    "reasoning_tokens": 33,
    "tokens_estimated_before": 1882,
    "tokens_estimated_after": 1348
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-selection-2026-11-16/dev-reinstatement-raw.json)

## Integrity

```json
{
  "files_checked": 237,
  "byte_identical": true
}
```

The frozen settings record contains exact source-code, model, prompt and input-PDF hashes. No label verification or approval was performed.
