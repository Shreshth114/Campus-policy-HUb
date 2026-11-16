# Structured grounding development diagnostic

Run: `structured-grounding-context-2026-11-16`. Development observations only; no accuracy labels or benchmark score.

Groq only; fallback disabled locally. Original PDF copied into disposable storage; temporary 114-chunk index removed on exit. Production indexes were not opened by this runner.

## dev-reinstatement

I temporarily discontinued my B.Tech studies for a semester. What is the procedure to return and register again?

Decision: **answered**. Reason: `none`. Elapsed request: 3.232s.

Raw generation:

```json
{"status":"answer","claims":[{"provision":"P1","source":"C2"},{"provision":"P2","source":"C2"}]}
```

Selection failures:

```json
[]
```

Coverage review:

```json
{"relevant":true,"complete":true,"qualifications_preserved":true,"supported":true,"reasons":[]}
```

Final application answer:

"B8.1. A student may be permitted by the AAC to discontinue temporarily from the programme for a semester or a longer period for reasons of medical problems or other valid reasons. Normally, a student will be permitted to discontinue from the programme only for a maximum duration of two semesters." [C2]

"B8.2. Once the student resumes back to his/her course work, post temporary discontinuity, the creditable courses to be registered will be decided by the faculty adviser in consultation with Head of the Dept. The same shall be communicated to AAC." [C2]

Quotation attribution:

```json
{
  "verified": [
    {
      "quote": "B8.1. A student may be permitted by the AAC to discontinue temporarily from the programme for a semester or a longer period for reasons of medical problems or other valid reasons. Normally, a student will be permitted to discontinue from the programme only for a maximum duration of two semesters.",
      "labels": [
        "C2"
      ]
    },
    {
      "quote": "B8.2. Once the student resumes back to his/her course work, post temporary discontinuity, the creditable courses to be registered will be decided by the faculty adviser in consultation with Head of the Dept. The same shall be communicated to AAC.",
      "labels": [
        "C2"
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
    "latency_ms": 1635.0913047790527,
    "input_tokens": 1249,
    "output_tokens": 207,
    "finish_reason": "stop",
    "reasoning_tokens": 173
  },
  "answer": {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "latency_ms": 1488.353967666626,
    "input_tokens": 1252,
    "output_tokens": 85,
    "finish_reason": "stop",
    "reasoning_tokens": 45,
    "tokens_estimated_before": 1882,
    "tokens_estimated_after": 1417
  }
}
```

[Exact sanitized messages, evidence and raw responses](evaluation/ps1/runs/structured-grounding-context-2026-11-16/dev-reinstatement-raw.json)

## Integrity

```json
{
  "files_checked": 237,
  "byte_identical": true
}
```

The frozen settings record contains exact source-code, model, prompt and input-PDF hashes. No label verification or approval was performed.
