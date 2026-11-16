# Personal document inspection — implementation and verification

Implemented 2026-11-14. Focus: close the original PDF preview and inspect actual stored personal chunks.

## Changes

- `web/personal.js`: high-contrast Close Preview beside the heading; Escape handling while the document view is active; focus and window-scroll restoration; revoke preview blob URLs; ignore stale preview/inspection responses. Keep extracted-page and indexed-chunk disclosures intact. Each document card now offers View Chunks, with a dedicated screen, filename, count, stored ID/index/page/section, exact stored text, character count, previous/next/jump navigation and Back to My Documents. Loading, empty, missing-metadata and error states included. Workspace changes clear the inspection state.
- `web/index.html`: scoped responsive inspection styles, wrapping identifiers and scrollable whitespace-preserving chunk text. Existing theme tokens reused.
- `src/personal_api.py`: new GET `/personal/documents/{document_id}/chunks`. Existing detail/original endpoints remain unchanged. The detail endpoint re-extracts pages, so the new endpoint avoids that dependency. Existing capability middleware establishes the personal scope; registry membership, nonremoved source, workspace, document ID and current version constrain retrieval. Only display metadata is returned; no embeddings, filesystem paths or capabilities are exposed. No extraction, re-indexing or vector writes.
- `tests/test_personal.py`: two integration tests cover exact stored values, unchanged fixture embeddings, cross-workspace/missing capability/missing document denial, no extraction or embedding calls, empty documents and missing optional metadata.
- `tests/document_inspection.browser.cjs`: read-only browser checks against the requested personal document, plus explicitly mocked empty/error/metadata cases. External/institutional requests and all non-GET requests are blocked. Target capability and baseline response are read from private temporary files; never committed. `INSPECTION_TARGETS` and `INSPECTION_CHUNKS` can override those file locations.
- Eight verification screenshots: `docs/screenshots/document-inspection/`.

## Commands and results

Run from the project directory:

```sh
python -m pytest tests/ -q
node --check web/personal.js
node tests/frontend.test.cjs
node tests/personal_frontend.test.cjs
node tests/sidebar_frontend.test.cjs
node tests/whatif_frontend.test.cjs
NODE_PATH=/private/tmp/dell-browser/node_modules node tests/document_inspection.browser.cjs
```

Results: **315 Python tests passed**, six existing dependency deprecation warnings. All four existing JavaScript suites passed (including 19 dashboard checks); JavaScript syntax passed. Browser assertions passed with no page errors at 1440px and 390px, light and dark themes. Close restores focus and preserves expanded extracted pages; Escape closes; all 77 choices were visited; previous/next bounds and return navigation passed. Empty, missing metadata, escaped source text and unavailable-service cases passed. Cross-workspace denial is tested using isolated API fixtures, never a production foreign workspace.

The personal `BTech_(Rules_&_Regulations)2013_21nov2023.pdf` has **77** current stored chunks. All 77 IDs, texts, indices and pages from the new endpoint match the existing detail endpoint's stored records. Browser-rendered text and page metadata were compared for every chunk. No chunks were reconstructed or merged.

## Data integrity and limitations

No production write, indexing, approval or deletion request was made. Original PDFs, extracted files, manifests, registries and vector segment files retained their file sizes and nanosecond modification times. The isolated integration test additionally compared embeddings before/after inspection and found them identical.

Integrity monitoring used filesystem metadata only for institutional files, without opening their contents. Of 239 tracked production data/index files, 238 retained identical size/mtime. The shared `.chroma-institutions/chroma.sqlite3` retained its size but its timestamp changed during live verification. Personal and institutional records share that existing database; normal client initialization uses `get_or_create_collection`. The timestamp change was not conclusively attributed, and **whole-database byte identity / a before-and-after hash of live embeddings is not claimed**. No institutional records were requested or intentionally changed; no chunk/embedding mutation was executed. Protected source and registry file metadata remained unchanged.

Escape is handled by the app when the parent page receives the key. A browser-native PDF viewer can consume keyboard events while focus is inside its iframe; the visible Close Preview button remains the reliable control. Headless Chromium verified PDF loading and container controls, but did not paint native PDF pages in screenshots. Native PDF rendering itself was not changed.
