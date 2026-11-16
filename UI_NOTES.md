# UI refresh

## Design

The interface now uses a desktop sidebar, a compact two-row phone header, a restrained green palette, an editorial home heading, and consistent forms, panels, evidence cards and status colours. Existing navigation controls retain their element IDs and handlers.

Light and dark themes cover all application views, including the inline architecture diagram, tables, citations, warnings and administration. Initial appearance follows the operating system. The toggle saves only `campus-ui-theme` in localStorage and synchronises across tabs. Theme switching also works when storage is unavailable. Font stacks use locally available Inter/Baskervville with system/Georgia fallbacks, avoiding external font dependencies.

View entry and menu transitions are short. Button feedback, keyboard focus, a skip-to-content link and reduced-motion support are included.

## Files changed

- `web/index.html` contains presentation styles, the initial theme selection, theme control, skip link and home heading.
- `web/ui.js` contains theme preference handling alongside the existing UI helpers.
- `UI_NOTES.md` records the scope and verification.

## Verification

- Full existing suite passed with 275 tests and six dependency deprecation warnings.
- Chromium checked all 13 main views at 1440 px and 390 px in both themes, producing 52 screenshots. Contact sheets were visually reviewed. These checks covered fresh-session, empty and locked states.
- No browser runtime errors or page-level horizontal overflow appeared in those checks.
- Additional responsive checks passed at 320, 768, 1150, 1151 and 1920 px on the How it works view.
- Actual mobile navigation, Advanced menu navigation, Escape dismissal, theme persistence, blocked-storage fallback and reduced-motion behaviour passed.
- Data-changing browser requests were blocked during these checks. Populated live answer generation, uploads and authenticated administrator mutations were outside this visual verification run.
- SHA-256 verification matched all 251 snapshotted backend, benchmark and data/index files after testing.

## Backend dependencies

No backend dependency was required for this redesign. Existing backend implementation, API handlers and request-building code were preserved. Theme colours apply to the application interface. Original PDF pages and previously exported artifacts retain their own document styling.

## Existing copy to review separately

The advanced retrieval selector describes Fusion as keyword plus semantic search, while its nearby explanation describes direct plus hypothetical retrieval. This refresh retained those existing labels. A separate terminology review should reconcile that description with the actual retrieval implementation.

## Sidebar functionality check

Verified all 13 views through their controls in a disposable localhost instance with synthetic PDFs and a deterministic provider stub. Browser actions exercised upload/index, source inspection, re-index, rule extraction, questions, fact parsing/confirmation, eligibility analysis, conflicts, version comparison, Raw/HyDE/Fusion comparison, benchmark blocking, evidence, candidate generation/skip, session metrics and the architecture view. Administration was verified at its locked entry screen in the browser; existing automated tests cover authenticated administration. The browser run reported zero runtime errors. This run verifies integration, not live provider quality or quota availability.

Confirmed repairs

- Personal document actions now report progress/errors in My Documents. Replacing a document there also shows its upload/index status in that view.
- Returning to personal advanced tools re-enables comparison after an institutional readiness check disabled it.
- Changing workspace clears documents, changes, evidence and candidate content. Late evidence/label responses and candidate actions are guarded by workspace generation.
- Version comparison selects different initial reference/comparison entries.
- Plain JSON arrays from candidate generation now parse correctly. This required small fixes in `src/intelligence.py` and `bench/candidate_queries.py`. Both object-wrapped and plain-array responses have regression coverage. Generated suggestions remain unverified, and the human label file stays empty during generation.

Working feature handlers were retained. Benchmarking still requires human-verified labels. Rule extraction, answers and candidate generation require an available provider in normal operation. Empty workspaces and a single available document version produce explanatory prerequisite messages.

Final full suite passed 287 tests with six dependency warnings. Added regressions cover candidate response formats, workspace clearing and stale evidence responses. All 219 protected data/index hashes matched after the run. The only persisted test inputs and provider stubs used for browser verification were under temporary storage.

## 2026-11-16 — Whole-workspace presentation refresh

Implemented shared visual refinement and local Help Centre in web/index.html and web/ui.js. Help/quick navigation preserve existing page handlers; no backend work required. No new LLM calls or fake policy answers. UI previously described Fusion as keyword+semantic and promised optimal accuracy; changed copy to actual Raw+HyDE rank combination. Full details and verification limits: docs/UI_WORKSPACE_UPGRADE.md.
