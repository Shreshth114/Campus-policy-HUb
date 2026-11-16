# ADD ONE FEATURE: "PATH TO ELIGIBILITY" WHAT-IF SIMULATOR, PLUS MANDATORY PROJECT LOG AND PROMPT ARCHIVE

Project: ps1-policy-assistant (Campus Policy Intelligence: FastAPI, ChromaDB, FastEmbed, Groq, HyDE/Raw/Fusion retrieval, anonymous personal workspaces, Rule Book of quote-validated numeric rules, deterministic eligibility analysis, conflicts, version comparison). Run on localhost. No deployment, Docker or hosting work. Do not use git. Time-box about 60 to 90 minutes.

====================================================================
PART 0. DO THIS FIRST: LOGGING AND PROMPT ARCHIVE (applies to the whole session)
====================================================================
A. PROJECT_LOG.md (project root). Append-only, chronological. If it exists, read it first and append; if not, create it. After EVERY step or phase append an entry in this format:
  ## <YYYY-MM-DD HH:MM> | <short title>
  - What was done:
  - Files created or changed:
  - Tests run and counts (Python and JS):
  - Decisions and trade-offs:
  - Problems found / not verified:
  - Next step:
Keep it truthful: separate "verified" from "not verified". If you backfill history from existing reports in the repo (audit/, improve/, improve_hyde/, docs/, README, DECISIONS, PROMPTS.md), put it in a clearly marked section "Backfilled history (from existing documents, not re-verified)" and do not invent anything that is not in those files.

B. PROMPTS_USED.md plus a prompts/user/ folder. This archives the prompts the USER gave to the coding agent (separate from PROMPTS.md, which holds the app's in-app LLM prompts; do not merge or overwrite PROMPTS.md).
  1. Before doing any other work, save THIS ENTIRE PROMPT verbatim, character for character, to prompts/user/<NN>_<YYYY-MM-DD>_whatif-simulator-and-logging.md (NN = next free two-digit number).
  2. Append an index line to PROMPTS_USED.md: number, date, title, filename, one-line purpose, and the outcome (completed / partial / blocked, filled in at the end).
  3. If the user sends further prompts later in this session, save each verbatim the same way BEFORE starting work on it.
  4. Search the repo for any earlier user-provided prompt or instruction files (for example uploaded .md prompt files, files named like build guide, redirection, continuation, audit, improve, ablation, ui). List each in PROMPTS_USED.md with its path under "Found in repo (copied verbatim or referenced)". Copy them verbatim into prompts/user/ only if they are clearly prompts the user gave; do not guess or reconstruct prompts from memory. State plainly in the file that earlier prompts which are not in the repo must be pasted in by the user.
  5. Never store secrets. If a prompt contains anything that looks like an API key, token or password, replace it with [REDACTED] and note that you did.
  6. Append-only: never delete or rewrite earlier entries.

====================================================================
PART 1. RULES FOR THE FEATURE WORK
====================================================================
- Do not change existing guardrails or behaviour: HyDE text never reaches the answer prompt; workspace scoping and isolation; citation and quote verification; abstention; prompt-injection resistance; personal/institution trust separation; deterministic (non-LLM) eligibility comparison. Do not change retrieval, prompts, thresholds or API contracts. Add new code and endpoints only.
- PROTECTED DATA: do not approve or publish institution sources; do not delete or reset Chroma, registries or manifests; do not read, print, log or modify the admin token or any API key; keep the 3 extraction failures visible; keep institution isolation. Verify protected-file SHA-256 hashes before and after (existing method) and report the result.
- The simulator must make ZERO LLM or provider calls at runtime. The Groq daily quota is nearly exhausted: do not call Groq or any provider while building or testing. Use synthetic fixtures and cached or fixture rules only. Add a test that fails if the what-if endpoint triggers any provider call.
- Never fabricate: no invented thresholds, formulas or policy facts. The simulator only does arithmetic on thresholds that come from existing validated rules (the verbatim quote and number already verified by code). Nothing is hardcoded to a specific document, college, subject name or question.
- Before editing any existing file, copy it to backups/whatif/ so it can be reverted.
- Run the full Python suite and the JS DOM tests before starting (record baseline counts) and after the feature; restart the app on localhost and confirm it loads. If something breaks and you cannot fix it in two attempts, revert that change and log it.
- Use the existing design tokens and styles; support the light and dark themes if they exist; fully offline (no CDN, external fonts or images); keep safe rendering (escape all text, never insert unescaped via innerHTML); keep SYNTHETIC TEST FIXTURE labels visible on fixture data.
- Preserve existing element IDs and test hooks.

====================================================================
PART 2. THE FEATURE: PATH TO ELIGIBILITY (WHAT-IF SIMULATOR)
====================================================================
PURPOSE: After a student's eligibility analysis, let them change their numbers and instantly see which rules would be satisfied, and what change would be needed to satisfy each rule that currently is not. This moves the product from "answers questions" to "shows what the student can do", using only the student's own documents.

BEHAVIOUR
1. Entry point: a "What if I change this?" panel on the eligibility result in Ask & Analyse, shown only after a confirmed analysis exists (same confirmation gates as today: facts confirmed, rule applicability confirmed). Unconfirmed or missing facts remain "insufficient evidence"; the simulator never fills them in.
2. Scenario inputs: one editable field per confirmed numeric fact (value and unit, prefilled), with a "Reset to my real facts" button. Use number inputs and, where a sensible range exists (for example 0 to 100 for percentages), a slider as well. Hypothetical values are a SCENARIO: never saved as the student's confirmed facts, never cached as an answer, never persisted. Show a permanent banner while a scenario differs from the real facts: "Scenario only. These are not your real values."
3. Live results: for every rule used in the analysis show: rule text (the verbatim quote with document and page), required value and operator, scenario value, status (satisfied / not satisfied / insufficient evidence), and the gap. Recompute when inputs change, debounced, by calling a NEW backend endpoint that reuses the SAME deterministic evaluator as the real analysis (single source of truth, Decimal arithmetic, same operator handling). The client must not reimplement the comparison logic.
4. Path to eligibility, per rule that is not satisfied:
   a) Direct gap: the amount the value must change to meet the threshold, respecting the operator (for strict ">" say it must exceed the threshold; for "==" say it must equal the threshold and give no gap).
   b) For percentage rules, an optional "compute from counts" mode: the student may enter done (numerator), total so far (denominator) and optionally remaining (future items). Then compute with Decimal and show:
      - the minimum number of additional consecutive items that must be fully completed to reach the threshold: x = ceil( (t * total - done) / (1 - t) ) where t = threshold/100, and state when t >= 1 means it cannot be reached by additional items alone;
      - if remaining is provided: whether the threshold is still reachable (done + remaining over total + remaining), and the maximum number of the remaining items that can be missed while still meeting it.
      Label this clearly as ARITHMETIC ON THE STATED THRESHOLD ONLY. It does not model the institution's own counting rules, cut-off dates, condonation, exceptions or rounding practices unless those appear in the rule text. Use generic wording ("items", "classes or units as counted by your institution"); do not hardcode attendance terminology, though the label may reuse the rule's own subject text.
   c) Exceptions and caveats: if the validated rule has an exceptions or applicability field, show it as a verbatim quote with page and the line "These may change what applies to you. Check with your institution." Never present a route to eligibility that the document does not support, and never suggest an exception applies to the student.
5. Overall verdict under the scenario: eligible / ineligible / insufficient evidence computed by the same logic as today (all required conditions satisfied, any not satisfied, any unknown). Never claim eligibility if any condition is unknown. Say that the verdict covers only the rules found in the uploaded documents.
6. Conflicts: if two rules for the same subject conflict across documents, show both with quotes and do NOT produce a combined verdict or a path; say it cannot be resolved without more evidence (consistent with the existing conflict logic).
7. Ordering: list unmet rules by smallest required change first (units differ, so compare only within the same unit and otherwise keep document order).
8. Trust: personal-workspace results keep the existing line "Based on documents you uploaded. Not verified by your institution." Rules shown as "extracted by AI, verify against the source quote."

BACKEND
- New endpoint (workspace-scoped like the other personal endpoints, capability id required, rate-limited like others): POST /api/personal/<workspace>/whatif with {facts: [...scenario values...], counts?: {...}}. Reuse existing evaluator functions; add only thin new functions for the gap and count arithmetic in the intelligence module (or a new small module). Validate inputs strictly: numeric ranges, Decimal parsing, maximum magnitudes, reject NaN and infinity, unit mismatches handled explicitly (do not convert between units unless the code already supports it; otherwise return insufficient evidence for that rule).
- Response is JSON only (no free text from a model). Return per-rule structured results so the UI renders them without interpretation.
- Must never touch another workspace's rules and must work only with rules already extracted and validated for this workspace.

FRONTEND
- Compact, readable table plus the scenario controls; statuses shown as text plus a small neutral marker (not colour alone). Keyboard accessible, labelled inputs, aria-live region announcing the updated verdict. Clear empty state ("Run an analysis with confirmed facts first"), error state and a "no numeric rules found" state. No horizontal overflow at 390px width.
- Add it to the existing "How it works" page as one line describing the deterministic what-if (no new diagram required).

TESTS (add; do not edit existing tests to make them pass)
- Arithmetic: boundary equality for >= and > (value exactly at threshold), threshold 75 with done 60 of total 90, threshold 100 (unreachable by additional items), remaining items cases (reachable, exactly reachable, unreachable), zero total, negative or huge values rejected, Decimal rounding (ceil) correctness against an independent brute-force loop on at least 200 random cases.
- Operator handling for >=, >, <=, <, ==.
- Unit mismatch gives insufficient evidence, never a guessed conversion.
- Missing or unconfirmed fact stays insufficient evidence; verdict never "eligible" with an unknown condition.
- Conflicting rules produce no winner and no path.
- Zero provider calls (instrument the provider layer and assert it is never invoked).
- Workspace isolation: workspace B cannot use workspace A's rules or capability.
- Scenario values are never persisted or cached (check registries, caches and files before and after).
- Safe rendering: rule text or quotes containing HTML or script are escaped in the UI.
- JS DOM tests for the panel: prefilled values, reset, banner shown only when the scenario differs, aria-live updates.
Also run an end-to-end check in a disposable instance using the SYNTHETIC fixtures (and cached or fixture rules, no provider calls): confirm the numbers on screen match a hand calculation, and say clearly if browser-level visual QA was not performed. If Playwright/Chromium is available capture screenshots at 1440px and 390px in light and dark and inspect them.

DOCS (keep short)
- DECISIONS.md: what the simulator does and does not model, why it makes no LLM calls, the arithmetic and its stated limits, and what is NOT verified.
- One short "interview notes" paragraph in the existing interview notes file if present.
- Do not rewrite other documentation.

====================================================================
FINAL REPORT (short, also appended to PROJECT_LOG.md)
====================================================================
What was built, files changed, test counts before and after, the hash check result, whether any provider call occurred (it must be zero), what was verified end to end versus not, known limitations, and exactly how to demo the simulator on localhost with the synthetic fixture in under one minute. Then update PROMPTS_USED.md with this prompt's outcome and stop. Do not add any other feature.