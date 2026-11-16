---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-10-19

### The plan asserts no end-to-end tests exist, but the A2UI board widget now has one

- Status: BLOCKING
- Evidence:
  - The artifact's End-to-End Tests section says: "No dedicated end-to-end tests exist for this feature. Panel behavior is proven through node.invoke integration coverage and the macOS app surface."
  - `ui/src/e2e/board-a2ui.e2e.test.ts` exists and is a dedicated end-to-end suite for the A2UI surface. It defines `const suite = createBoardE2eSuite("Control UI dashboard A2UI", ...)` at line 78 and drives the renderer through a real browser.
  - Lines 17-23 of that file pin the two renderer bundles (`a2ui.bundle.js` for v0.8 and `a2ui-v0.9.bundle.js` for v0.9) read from `extensions/canvas/src/host/a2ui`, and lines 80-88 rebuild them with `scripts/bundle-a2ui.mts` when `OPENCLAW_A2UI_BUNDLE_DIR` is not set.
  - Line 115 covers "sends each v0.8 action once after the host reconnects", and lines 167-200 render both dialects under the dark and light themes plus a v0.9 rejected-action and reset case.
- Artifact currently says: "No dedicated end-to-end tests exist for this feature."
- What the code actually does: there is a dedicated browser-level end-to-end suite for the A2UI renderer inside a board widget cell, covering both protocol dialects, both themes, action emission across a host reconnect, and the rejected-action reset path. A reader of the plan would conclude the A2UI rendering path is only covered by unit tests.
- Needed change: replace the End-to-End Tests section with the board A2UI e2e suite and the behaviors it covers.

### The build-script test rows point at the wrong files and the wrong behaviors

- Status: BLOCKING
- Evidence:
  - The artifact's TC-37, TC-38, and TC-39 describe bundle-script behaviors: "Bundle script requires both prebuilt dialects when A2UI build dependencies are absent", "Bundle script sorts hash inputs without locale-dependent collation", and "Bundle script bounds tracked-input discovery and treats a timeout as a fallback".
  - TC-45 and TC-46 describe "Runner executes native pnpm from npm_execpath directly" and "Runner falls back to bare pnpm when native npm_execpath is not executable".
  - The bundle script is now `scripts/bundle-a2ui.mts` and no longer performs its own hash sorting or tracked-input discovery. Hashing lives in `scripts/lib/build-artifact-cache.mts:86-107` (`hashInputFiles`), which sorts env entries with `left.localeCompare(right)` at line 96 and files with a plain `files.toSorted()` at line 79, and the file inventory comes from `listCacheFiles` at line 74.
  - The bundle script's own input list is a static set (`scripts/bundle-a2ui.mts:104-113`: `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `patches`, `extensions/canvas/package.json`, `extensions/canvas/src/host/a2ui-app`, `scripts/bundle-a2ui.mts`, `scripts/pnpm-runner.mts`, `scripts/windows-cmd-helpers.mjs`, `scripts/lib/build-artifact-cache.mts`).
  - The bundle script's missing-dependency behavior is at `scripts/bundle-a2ui.mts:96-107`, which fails with "A2UI package missing and no complete prebuilt bundle found at: ...".
  - The pnpm runner is now `scripts/pnpm-runner.mts`, whose `resolvePnpmRunner` (lines 141-205) resolves a node-runnable `npm_execpath` through the node interpreter, falls back to a bare `pnpm` on PATH, then to `corepack pnpm`, and finally to the literal command `pnpm`.
  - The surviving suites are `test/scripts/bundled-plugin-assets.test.ts` (which includes `it("reuses both Canvas dialects across candidates and invalidates changed inputs", ...)` at line 49 and asserts on the "keeping prebuilt bundle" message at line 131) and `test/scripts/pnpm-runner.test.ts` (which covers the Windows `pnpm.cmd` wrapper, the ambient `ComSpec` handling, the Corepack fallback, and the shared spawn spec).
- Artifact currently says: the build-script rows are attributed to the Canvas build and the runner without naming the shared modules that now own the behavior, and the artifact's Test Infrastructure section says "Prebuilt A2UI bundles stubbed or resolved from the source asset tree" and "Vitest suites colocated with sources (`extensions/canvas/**/*.test.ts`)" with no mention of `test/scripts/`.
- What the code actually does: the bundle build and the pnpm runner are shared repository infrastructure exercised by suites under `test/scripts/`, not by suites colocated under `extensions/canvas/`. The hash-sorting and tracked-input-discovery behaviors the plan attributes to the bundle script now live in `scripts/lib/build-artifact-cache.mts`.
- Needed change: repoint TC-37 through TC-39 and TC-45 through TC-46 at `test/scripts/bundled-plugin-assets.test.ts`, `test/scripts/build-all.test.ts`, and `test/scripts/pnpm-runner.test.ts`, and move the hash-sorting and input-discovery behavior to the shared cache module the plan currently assigns to the bundle script.

### The doctor contract suite is not listed

- Status: ADVISORY
- Evidence:
  - `extensions/canvas/doctor-contract-api.test.ts` exists with two describe blocks: "Canvas doctor config repair" (line 28) and "Canvas doctor state migration" (line 91).
  - Its cases are: "flags and removes retired file-host settings" (line 29), "ignores the default core document root" (line 92), "moves custom-root documents into the stable core layout" (line 102), "leaves a conflicting legacy document in place" (line 140), and "cleans partial copies and retries the migration" (line 164).
  - These map to the artifact's TC-26 through TC-30, but the artifact does not name the file, and the doctor contract is now a separate plugin entry (`extensions/canvas/doctor-contract-api.ts`) registered through the manifest's `"doctorContract": { "configRepair": true, "stateMigrations": [{ "id": "canvas-custom-root-documents-to-core" }] }` in `extensions/canvas/openclaw.plugin.json`.
- Artifact currently says: the plan lists "Doctor flags and removes retired file-host settings", "Doctor ignores the default core document root", "Doctor moves custom-root documents into the stable core layout", "Doctor leaves a conflicting legacy document in place", and "Doctor cleans partial copies and retries the migration", but does not say which file implements them or that the migration is a manifest-declared plugin contract.
- What the code actually does: the doctor behavior is a plugin-declared contract with a stable migration id, implemented in its own plugin entry. A reader would not know the migration has a durable id or where the behavior lives.
- Needed change: name `extensions/canvas/doctor-contract-api.test.ts` and the `canvas-custom-root-documents-to-core` migration id.

### FR-10 has no plugin-owned coverage even though a new rendering surface exists

- Status: BLOCKING
- Evidence:
  - The artifact's coverage matrix says: "FR-10 | Covered under FEAT-p8 hosting surface, no plugin-owned cases".
  - The A2UI board widget is now rendered by `ui/src/components/board/board-widget-cell.solid.tsx`, a Solid 2 custom element that resolves plugin widget kinds through `ui/src/lib/board/widgets/index.ts` and `getPluginWidgetKindContribution`.
  - The board sandbox is a separate surface from the canvas widget sandbox: `src/gateway/board-sandbox.ts` provides `buildBoardWidgetSandboxPath` and `buildBoardWidgetContentSecurityPolicy`, and `ui/src/e2e/board-a2ui.e2e.test.ts:193` builds the renderer URL as `${rendererOrigin}/__openclaw__/cap/canvas-proof/__openclaw__/a2ui/${bundleFiles[version]}`.
  - `extensions/canvas/src/board-widget.ts:32-37` handles the case where the resource URL equals the bare path by resolving the scoped capability prefix at runtime from `location.pathname`.
- Artifact currently says: FR-10 has no plugin-owned cases and is delegated to FEAT-p8.
- What the code actually does: the plugin owns a board-widget content kind whose rendering path, capability-scoped URL resolution, and sandbox are distinct from the FEAT-p8 canvas widget hosting surface. The plugin's own composition logic (the `resourceScript` branch in `extensions/canvas/src/board-widget.ts:32-37`) is not covered by any plugin test, and the coverage matrix claims no plugin-owned cases exist.
- Needed change: add plugin-owned cases for the board-widget composition and capability-scoped resolution, and correct the FR-10 matrix row.

### The Control UI canvas widget view file was renamed to `.tsx` and now has a companion loader

- Status: ADVISORY
- Evidence:
  - The artifact's code scope and the FEAT-p12 code index both name `ui/src/components/canvas-widget-view.ts`.
  - The file today is `ui/src/components/canvas-widget-view.tsx`, a Solid 2 component, with `ui/src/components/canvas-widget-view-loader.ts` holding the loader contract and `ui/src/components/canvas-widget-view-loader.ts` exporting `createCanvasWidgetViewLoader`, `isCanvasWidgetLoadRetryEvent`, and `CanvasWidgetViewBinding`.
  - `ui/src/pages/chat/components/canvas-widget-mount.tsx` and `ui/src/lib/chat/canvas-widget-frame-generation.ts` and `ui/src/lib/chat/canvas-frame-presentation.ts` are the surrounding chat-side surfaces, and `ui/src/app/canvas-surface-lease.runtime.ts` plus `ui/src/app/gateway-canvas-surface.ts` own the surface lease.
- Artifact currently says: nothing about the Control UI rendering path beyond FR-10 and the out-of-scope note, and the referenced path `ui/src/components/canvas-widget-view.ts` no longer exists.
- What the code actually does: the Control UI canvas rendering path is a Solid 2 component plus a separate loader module plus a chat-side mount plus a frame-generation helper plus a surface lease, split across four directories. A reader following the old `.ts` path would not find the file.
- Needed change: update the referenced path to `.tsx` and note the loader, mount, and lease modules if the Control UI surface is to remain in scope.

## Sync drift: 2026-11-16

### A2UI test cases and suites no longer exist

- Status: BLOCKING
- Evidence:
  - No `ui/src/e2e/board-a2ui.e2e.test.ts` exists.
  - No `scripts/bundle-a2ui.mts`, `scripts/copy-a2ui.mjs`, or `extensions/canvas/scripts/copy-a2ui.mjs` exists.
  - `extensions/canvas/src/a2ui-jsonl.ts`, `extensions/canvas/src/board-widget.ts`, and the `src/host/a2ui-app/` renderer source are gone.
  - `test/scripts/bundled-plugin-assets.test.ts` still exercises generic bundled-plugin asset discovery and mentions the Canvas plugin, but it no longer tests A2UI dialect bundles.
- Artifact currently says: TC-6 covers the v0.9 validator, TC-11 and TC-12 cover board kind resources, TC-24 covers lazy A2UI asset loading, and TC-37 through TC-44 cover the A2UI bundle and copy scripts. The End-to-End Tests section was already flagged on 2026-10-19 for a board A2UI suite.
- What the code actually does: none of that A2UI-specific coverage can run because the code was retired.
- Needed change: delete TC-6, TC-11, TC-12, TC-24, and TC-37 through TC-44 from this plan, or replace them with tests of the HTML document host and `show_widget` validation.

### The end-to-end statement needs a new scope note

- Status: ADVISORY
- Evidence:
  - `ui/src/e2e/chat-canvas-detail-width.e2e.test.ts` exists, along with `ui/src/e2e/canvas-sandbox.test-support.ts`.
  - Those files sit under `ui/src/e2e/`, outside the `p12-canvas-dynamic-ui` code index.
- Artifact currently says: no dedicated end-to-end tests exist for this feature.
- What the code actually does: the A2UI e2e suite cited in the 2026-10-19 review was deleted, so the statement is true again for A2UI, but Canvas widget e2e coverage exists under the Control UI.
- Needed change: keep the statement for plugin-owned coverage and name the Control UI canvas e2e suites as out of scope or add them.

### New test suites are undocumented and the infrastructure section is stale

- Status: BLOCKING
- Evidence:
  - Core suites exist at `src/canvas/documents.test.ts`, `src/canvas/constants.test.ts`, `src/canvas/widget-script-syntax.test.ts`, `src/canvas/widget-tool.test.ts`, `src/canvas/widget-tool.presenter.test.ts`, `src/canvas/widget-tool.prompt.test.ts`, and `src/canvas/wrap.test.ts`.
  - Plugin suites exist at `extensions/canvas/index.test.ts`, `extensions/canvas/doctor-contract-api.test.ts`, `extensions/canvas/src/widget-presenter.test.ts`, and the existing CLI, config, config-migration, and tool suites.
  - `src/commands/doctor-a2ui-widgets.test.ts` covers the new A2UI retirement repair.
  - Control UI suites exist at `ui/src/app/canvas-surface-lease.test.ts` and `ui/src/components/canvas-widget-view.test.ts`.
  - The Test Infrastructure section says suites are colocated under `extensions/canvas/**/*.test.ts` and that prebuilt A2UI bundles are stubbed or resolved from the source asset tree.
- Artifact currently says: the plan lists 46 test cases under a single colocated Vitest convention with A2UI bundle stubs.
- What the code actually does: coverage is spread across core, plugin, Doctor, and Control UI suites, and no A2UI bundles are built or stubbed.
- Needed change: list the current suites, update the infrastructure section, and add the A2UI retirement repair coverage.

### The coverage matrix is stale

- Status: BLOCKING
- Evidence:
  - FR-5 and FR-6 no longer exist as implemented requirements.
  - The A2UI portions of the FR-7, FR-10, and NFR-3 rows have no code.
  - The FR-9 row still maps to `extensions/canvas/doctor-contract-api.test.ts`, which remains correct.
- Artifact currently says: the matrix assigns cases to FR-5, FR-6, A2UI-bearing rows, and the build-script row.
- What the code actually does: the matrix no longer reflects the requirement set or the suite layout.
- Needed change: rebuild the matrix against the revised requirements and current suites.

### Previously recorded drift remains open

- Status: ADVISORY
- Evidence:
  - `extensions/canvas/doctor-contract-api.test.ts` and the `canvas-custom-root-documents-to-core` migration id are unchanged.
  - The `ui/src/components/canvas-widget-view.ts` path is still missing because the file is `canvas-widget-view.tsx`.
  - The 2026-10-19 advice to repoint build-script rows at shared `test/scripts/` suites is now partly moot because the A2UI bundle scripts were deleted.
- Artifact currently says: those 2026-10-19 entries remain open in this review file.
- What the code actually does: the file rename and doctor contract observations still hold, while the A2UI build rows are obsolete.
- Needed change: apply the still-relevant 2026-10-19 changes together with this drift.
