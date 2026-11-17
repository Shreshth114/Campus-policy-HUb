# Document Changes loading fix — 17 November 2026

## Diagnosis

The comparison button first extracts quote-validated numeric rules from both selected versions. It does not run a quick whole-PDF textual diff. At inspection, the saved extraction activity showed 33 of 47 candidate chunks processed and 17 validated rules. The UI hid that progress behind an indefinite “Working…” message and allowed duplicate submissions. Its requests had no timeout.

Static investigation and regression tests also reproduced a backend completion bug: provider exhaustion could fall through as success, and even explicitly failed extraction caches were finalized with partial=false. Comparison checked cache presence rather than trustworthy completion, so it could compare incomplete results. The actual observed wait establishes lengthy extraction, not proof that a provider failure occurred in that particular request.

## Fix

- Reuse the existing workspace-scoped `/personal/rules/activity` endpoint to show the current document, processed candidate chunks and validated-rule progress.
- Disable comparison and selectors while working; suppress duplicate submissions. Preserve epoch checks so stale workspace results cannot continue into the next document/comparison.
- Bound extraction requests with a 120-second backend deadline and 135-second frontend timeout; the final comparison has a 30-second client timeout. Errors restore controls with an actionable retry message.
- Rely on the unified client's existing transport retries instead of a second extraction retry/sleep loop with arbitrary Retry-After waits.
- Persist completed chunk IDs after each successful batch. A retry processes only remaining batches for the same document/content/prompt/model cache key. Invalid/truncated model output does not complete a batch.
- Mark provider errors, cancellation/timeouts and incomplete work as partial. A busy extractor returns promptly instead of queuing another long request.
- Require a versioned, non-partial extraction completion marker before comparison. Older cached validated rules are retained, but must be rechecked once because their old completion flag cannot prove all batches ran.
- Distinguish a blocked/incomplete comparison from a completed comparison with no validated numeric-rule differences. No invented changes or whole-document coverage claims.

No new API endpoint, provider configuration, rule-extraction prompt, quote validator, retrieval algorithm or embedding setting was introduced. This fix performs no re-indexing, embedding regeneration or PDF editing. Existing normal rule-cache/activity writes remain scoped to the personal workspace.

## Verification

- `python -m pytest tests/ -q`: **481 passed**, six existing dependency warnings, 16.03 seconds.
- `node tests/document_changes_frontend.test.cjs`: passed. Covers progress, duplicate prevention, provider/partial errors, blocked results, completion, retry controls and request timeout. It is also part of the Python suite.
- Existing personal frontend checks passed. The full Python suite includes the established dashboard/what-if/frontend checks.
- Backend regressions cover provider exhaustion, partial comparison blocking, exact batch resumption, bounded timeout/checkpoint preservation, busy extraction and validated cache reuse. Tests use isolated synthetic fixtures and mocked providers; no live extraction/model request was triggered for verification.
- The earlier live extraction was no longer marked running before the local server was restarted. The updated server bound port 8000 successfully and returned HTTP 200.

BrowserOS tools were unavailable, so no live browser visual test was claimed. The supplied screenshot and saved progress were used for diagnosis; behavior was checked through DOM/API regression tests. Loading text uses existing theme styles and an aria-live status region.

## Remaining limitations

Large documents still require multiple AI calls. Provider limits can interrupt extraction; the UI now explains the state and retry resumes saved batches. A browser timeout does not guarantee instant cancellation of server work, so the message explicitly warns that a server request may still be finishing. The backend time budget bounds that work.

Comparison covers validated numeric rule tables, not every policy sentence or textual amendment. Model extraction can miss rules; an empty comparison is not proof that complete PDFs are identical. No additional live accuracy claim is made.

Changed files: `src/intelligence.py`, `web/personal.js`, `tests/test_intelligence.py`, `tests/test_frontend.py`, new `tests/document_changes_frontend.test.cjs`, this report and the project log.
