# Workspace UI upgrade

16 November 2026

## Delivered

- Refined shared light/dark design tokens, typography, spacing, cards, form controls, tables, source passages and empty states across all 13 views.
- Sidebar line icons and active states; page context header; responsive desktop and mobile navigation.
- Working quick-page search with Cmd/Ctrl+K, arrow-key navigation, Enter and Escape; page results route through existing navigation handlers so required data loading still occurs.
- Overview shortcuts into documents, analysis and rules.
- Floating Help Centre chatbox and header access. Handles app topics including uploads, source inspection, retrieval modes, errors, rules/facts, workspace privacy, document comparison and evaluation. Topic buttons, typed questions, contextual links, close/Escape and focus restoration work. Text is inserted safely and help history is held only in page memory.
- Help explicitly identifies itself as a local product guide. It does not simulate AI-generated university-policy answers or send help messages to providers. No fake support staff, ticket submission or online-service claim.
- Copy-guidance action with success/error notification and back-to-top control.
- Modest page/panel transitions and button interaction feedback, with reduced-motion preferences respected.
- Corrected misleading frontend copy: Fusion combines Raw and HyDE rankings, not keyword search; no unsupported “optimal accuracy” claim. Retrieval behavior is unchanged.

## Scope

Application edits are frontend-only: `web/index.html` and `web/ui.js`. No backend module, provider setting, retrieval prompt, threshold, API contract, source file, cache or index was changed. Previous frontend files are preserved under `backups/ui-upgrade/`.

Styles are embedded in the existing served HTML and behavior extends the existing served ui.js, avoiding backend route additions or new frontend dependencies. Existing element IDs and feature handlers remain. The visual system uses the existing green identity and theme tokens.

## Verification

```sh
python -m pytest tests/ -q
# 408 passed, 6 existing dependency warnings; 11.66s
node --check web/ui.js
node tests/personal_frontend.test.cjs
node tests/sidebar_frontend.test.cjs
node tests/frontend.test.cjs
node tests/whatif_frontend.test.cjs
NODE_PATH=/private/tmp/dell-browser/node_modules node tests/ui_upgrade.browser.cjs
```

All four existing JS suites pass, including 19 dashboard checks. Browser checks cover all 13 views at 1440px/390px, light/dark, no horizontal overflow, Help topics and escaped input, Escape/focus restoration, quick search/no-results/keyboard navigation, theme switching and reduced motion. No browser errors or mutation requests occurred. Browser API data is explicitly stubbed for read-only visual verification; this is not a live provider or populated-workspace end-to-end test. No LLM calls were made.

New test: `tests/ui_upgrade.browser.cjs`. Twenty screenshots under `docs/screenshots/ui-upgrade/` show Overview, analysis, document empty state, retrieval comparison and Help in each viewport/theme combination. Visual review found and corrected a visible mobile form label narrowing the help input and an animation-timing screenshot issue.

## Limits

Help is a local topic guide with limited keyword matching, not a policy-answering chatbot or human support service. For policy questions it directs users to the existing grounded question flow. No new login, notifications backend, analytics service or support infrastructure was added. Empty-data screenshot fixtures verify layout and navigation; existing populated result rendering remains covered by the JS/Python suites, not a fresh real-model visual run. Copying requires browser clipboard permission and shows a useful fallback message if unavailable.

Reload the application page (hard refresh if needed) to load the new HTML/JavaScript. Python source/provider logic did not change.

## Modified and added files

- Modified: web/index.html, web/ui.js.
- Added: tests/ui_upgrade.browser.cjs, docs/UI_WORKSPACE_UPGRADE.md, docs/screenshots/ui-upgrade/*.png, backups/ui-upgrade/index.html and ui.js.
- Updated documentation: PROJECT_LOG.md, UI_NOTES.md, codex_primpt.md.
