# UI control polish — 16 November 2026

Replaced the two browser-native controls identified in the screenshots.

## Deletion confirmation

A theme-aware HTML dialog replaces native window.confirm for personal workspace and document deletion. It has a clear title, permanent-removal description, deletion icon, Cancel button and explicitly named destructive action. Cancel is focused first; Escape cancels; focus returns to the trigger. Native dialog behavior traps modal focus. Concurrent confirmation requests are rejected safely. Workspace/epoch checks ensure a confirmation cannot delete an item after the workspace has changed while the dialog is open. Existing deletion APIs and execution remain unchanged.

## Retrieval method

Raw, HyDE and Fusion are presented as three labelled radio cards, with concise descriptions and clear selected/focus states. Cards stack on mobile. The existing hidden personal-mode select remains the compatibility value read by the request handler; radio changes synchronize it and external select change events synchronize the cards. Mode values and the default remain unchanged. No backend, scoring or provider edits.

## Files

- web/index.html: mode cards and scoped dialog/card styles.
- web/ui.js: Promise-based confirmation component and mode-control synchronization.
- web/personal.js: await confirmation and validate workspace identity before existing deletion action.
- tests/ui_upgrade.browser.cjs: expanded browser coverage.
- docs/UI_CONTROL_POLISH.md, PROJECT_LOG.md: documentation.

## Verification

`python -m pytest tests/ -q`: **408 passed**, six existing dependency warnings, 15.05 seconds. JavaScript syntax checks passed.

`NODE_PATH=/private/tmp/dell-browser/node_modules node tests/ui_upgrade.browser.cjs`: passed. Covers both mode selection and keyboard interaction, underlying personal-mode values, real workspace-delete trigger with synthetic workspace state, Cancel/Escape and focus restoration, and generic acceptance result without a deletion callback. Existing 13-view desktop/mobile light/dark checks also pass. No DELETE/mutation requests occurred and no real workspace/data was removed. Screenshots: docs/screenshots/ui-upgrade/mode-picker-* and delete-dialog-*.

The browser test uses read-only mocked API responses and synthetic state. It verifies frontend behavior; the live deletion API was deliberately not exercised. Reload the page to use the updated controls.
