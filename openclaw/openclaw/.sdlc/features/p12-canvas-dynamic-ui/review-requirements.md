---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-10-19

### The A2UI dependency versions named in the artifact are stale

- Status: BLOCKING
- Evidence:
  - `extensions/canvas/package.json:12-13` declares `"@a2ui/lit": "0.13.0"` and `"@a2ui/web_core": "0.13.0"`.
  - `pnpm-lock.yaml:3193` and `pnpm-lock.yaml:3201` pin `@a2ui/lit@0.13.0` and `@a2ui/web_core@0.13.0`.
  - `extensions/canvas/src/a2ui-jsonl.ts:1` imports `A2uiMessageSchema as A2uiV09MessageSchema` from `@a2ui/web_core/v0_9`.
  - The artifact's Technical Decisions table states: "Dashboard renderer stack | `solid-js` 2.0.0-rc.14 with `@a2ui/lit` 0.12.0 and `@a2ui/web_core` 0.12.0 per `extensions/canvas/package.json`".
- Artifact currently says: "`@a2ui/lit` 0.12.0 and `@a2ui/web_core` 0.12.0 per `extensions/canvas/package.json`".
- What the code actually does: both A2UI packages are at 0.13.0, and the v0.9 message schema is imported from the `v0_9` subpath. A reader reproducing the renderer stack from the artifact would pin the wrong upstream versions and could hit a schema or renderer API difference.
- Needed change: update the pinned versions to 0.13.0.

### The plugin now ships three additional entry surfaces the artifact does not mention

- Status: BLOCKING
- Evidence:
  - `extensions/canvas/setup-api.ts` is a separate plugin entry that registers `migrateCanvasHostConfig` through `api.registerConfigMigration`.
  - `extensions/canvas/doctor-contract-api.ts` is a separate plugin entry implementing the doctor config repair and the `canvas-custom-root-documents-to-core` state migration.
  - `extensions/canvas/cli-metadata.ts` is a separate plugin entry registering the `nodes canvas` CLI descriptors.
  - `extensions/canvas/runtime-api.ts` re-exports the config parse helpers, `A2UI_PATH`, `CANVAS_HOST_PATH`, `handleA2uiHttpRequest`, and `registerNodesCanvasCommands`.
  - `extensions/canvas/openclaw.plugin.json` declares `"doctorContract": { "configRepair": true, "stateMigrations": [{ "id": "canvas-custom-root-documents-to-core" }] }` and `"contracts": { "tools": ["canvas"] }`.
  - `extensions/canvas/skills/canvas/SKILL.md` ships a Canvas skill that documents the panel control path and the capability-scoped `/__openclaw__/canvas/documents/...` route.
  - The artifact's Architecture diagram lists only `src/tool.ts`, `src/widget-presenter.ts`, `src/board-widget.ts`, `src/a2ui-jsonl.ts`, and `src/host/a2ui.ts` as the plugin's modules.
- Artifact currently says: the Overview describes "a lazily loaded `canvas` agent tool, a `node_panel` widget presenter behind core `show_widget`, versioned A2UI renderer bundles served from Gateway routes, and an A2UI board-widget content kind for session dashboards", and the architecture diagram shows a single plugin entry with five modules.
- What the code actually does: the plugin ships five entry points (runtime, setup, doctor contract, CLI metadata, and the skill), and a doctor state migration registered in the plugin manifest. The doctor contract, the setup migration entry, and the skill are all user- or operator-visible surfaces that the artifact does not describe, and the doctor migration is now a first-class plugin-declared contract rather than a one-off helper.
- Needed change: describe the multi-entry plugin structure, the doctor contract and its state migration id, the skill, and the CLI metadata entry.

### The hosted-widget-document route moved to core storage with a new document model

- Status: BLOCKING
- Evidence:
  - `src/canvas/` is a new top-level core directory (18 files) that owns the hosted widget document store: `src/canvas/documents.ts`, `src/canvas/serve.runtime.ts`, `src/canvas/constants.ts`, `src/canvas/config.ts`, `src/canvas/widget-tool.ts`, `src/canvas/wrap.ts`, and `src/canvas/widget-script-syntax.ts`.
  - `src/canvas/constants.ts:5` sets `const CANVAS_HOST_PATH = "/__openclaw__/canvas"` and line 6 sets `const CANVAS_DOCUMENTS_PATH = `${CANVAS_HOST_PATH}/documents``.
  - `src/canvas/documents.ts:13-30` defines the `CanvasDocumentKind` union as `html_bundle | url_embed | document | image | video_asset` and the surface union as `assistant_message | tool_card | sidebar`, plus `retentionScope` and a `cspSandbox: "scripts"` option.
  - `src/canvas/documents.ts:200` builds the entry URL as `${CANVAS_DOCUMENTS_PATH}/${encodeURIComponent(id)}/index.html`.
  - `src/gateway/server-http-request.ts:565-569` serves the document route from core when `isCoreCanvasHostEnabled(configSnapshot)` and the path is a canvas document path, using `getCanvasServeModule().handleCanvasDocumentHttpRequest`.
  - `src/canvas/config.ts:7-18` implements the core-side host gate, reading `plugins.entries.canvas.config.host.enabled` and the `OPENCLAW_SKIP_CANVAS_HOST` escape hatch, with the comment "Canvas owned these shipped operator switches before hosting moved into core."
  - `src/canvas/constants.ts:26-33` removes stale plugin-owned canvas capability surfaces and prepends the core-owned one.
  - The artifact's Out of Scope says: "HTML `show_widget` document composition, script validation, and bridge protocol (core `show_widget`)", and its API Contracts table says: "GET (prefix) | `/__openclaw__/canvas/*` | Serve hosted widget documents from core storage (core-owned route, Canvas-gated)".
- Artifact currently says: the artifact already knows the document route is core-owned and Canvas-gated, but it names the path as `/__openclaw__/canvas/*` and never mentions the document kind, surface, retention, or sandbox attributes that the document model now carries.
- What the code actually does: hosted widget documents are core-owned records with a kind, a surface, an optional retention scope, and a CSP-sandbox flag, served at `/__openclaw__/canvas/documents/<id>/index.html` from a core route, and the core canvas capability surface replaces the plugin's. The document model is a materially richer contract than the artifact's routing-only description.
- Needed change: describe the document model (kind, surface, retention scope, CSP sandbox), the `/__openclaw__/canvas/documents/` path, and the core-owned capability surface.

### FR-10 is now delivered by a board widget cell rather than the canvas widget view

- Status: BLOCKING
- Evidence:
  - `ui/src/components/canvas-widget-view.ts` no longer exists; the file is now `ui/src/components/canvas-widget-view.tsx` (Solid 2), with `ui/src/components/canvas-widget-view-loader.ts` as a companion loader.
  - `ui/src/components/board/board-widget-cell.solid.tsx` is a Solid 2 custom-element renderer that resolves plugin widget kinds through `ui/src/lib/board/widgets/index.ts` and `getPluginWidgetKindContribution`.
  - `ui/src/e2e/board-a2ui.e2e.test.ts:1-25` exercises the A2UI renderer inside a board cell, loading `a2ui.bundle.js` and `a2ui-v0.9.bundle.js` from `extensions/canvas/src/host/a2ui` and asserting both protocol dialects render under the dark and light themes.
  - `extensions/canvas/src/board-widget.ts:33-35` registers the content kind through `OpenClawPluginApi["registerBoardWidgetContentKind"]`.
  - `src/plugins/board-widget-content-kinds.ts:31-58` validates plugin-declared board widget content kinds.
  - The artifact's FR-10 says: "The system shall render Canvas and A2UI content in the Control UI through scoped capability URLs with sandboxed iframes, reusing the FEAT-p8 hosting surface", and the coverage matrix says "FR-10 | Covered under FEAT-p8 hosting surface, no plugin-owned cases".
- Artifact currently says: FR-10 is entirely delegated to FEAT-p8, with no plugin-owned test cases.
- What the code actually does: the A2UI content kind is registered as a **board** widget content kind and rendered by the board widget cell in Solid 2, which is a different rendering surface from the canvas widget view that renders hosted widget documents. The board widget cell and its capability-scoped sandbox frame are a separate surface from the FEAT-p8 canvas hosting path, and they now own the A2UI rendering path.
- Needed change: state that A2UI renders as a board widget cell in the Solid 2 Control UI, separate from the hosted-document canvas widget view, and add plugin-owned coverage for the board-widget path.

### The A2UI v0.8 dialect is now schema-validated, not just action-key checked

- Status: ADVISORY
- Evidence:
  - `extensions/canvas/src/a2ui-jsonl.ts:56-70` runs every v0.9 message through `A2uiV09MessageSchema.safeParse(record)` and reports `result.error.issues[0]?.message` on failure, while v0.8 messages are only checked for their action key.
  - `extensions/canvas/src/a2ui-jsonl.ts:38-47` rejects an explicit `version: "v0.8"` with "A2UI v0.8 messages must not include a version field" and rejects any other explicit version as unsupported.
  - The artifact's data model table lists only the four v0.9 action keys and the four v0.8 action keys, with no mention of a per-message schema check.
- Artifact currently says: "A2UI message (v0.9, via `@a2ui/web_core`)" with the constraint "Exactly one action key per message" for each dialect.
- What the code actually does: v0.9 messages must additionally satisfy the upstream `@a2ui/web_core` v0_9 message schema, and the version field itself has asymmetric rules (v0.9 must carry `version: "v0.9"`; v0.8 must not carry a version field at all). The requirement text ("one dialect per file (v0.8 unversioned or v0.9 versioned)") is still accurate, but the data model does not record the schema validation.
- Needed change: record the v0.9 schema validation and the version-field asymmetry in the data model.

### FR-8's host-enablement gate is now enforced in two places

- Status: ADVISORY
- Evidence:
  - `extensions/canvas/src/config.ts:33-40` implements the plugin-side gate `isCanvasHostEnabled`, reading `plugins.entries.canvas.config.host.enabled` and the `OPENCLAW_SKIP_CANVAS_HOST` escape hatch.
  - `src/canvas/config.ts:7-18` implements a second, core-side gate `isCoreCanvasHostEnabled` reading the same config key and the same env var, with the comment "Canvas owned these shipped operator switches before hosting moved into core."
  - `src/gateway/server-core-runtime.ts:432-435` and `src/gateway/server-plugin-reload.ts:368-371` both use the core gate to publish the canvas node capability surface.
  - `src/gateway/server-http-request.ts:567` uses the core gate to serve the hosted document route.
  - `extensions/canvas/index.ts:29-41` uses the plugin gate to register the board widget kind, the A2UI route, and the widget presenter.
- Artifact currently says: "FR-8 | Must | The system shall gate all Canvas hosting behind `plugins.entries.canvas.config.host.enabled` (default on) with an `OPENCLAW_SKIP_CANVAS_HOST` escape hatch".
- What the code actually does: the same switch is now read by both the plugin and core, and the two gates cover different surfaces (the plugin gate covers the A2UI route, presenter, and board kind; the core gate covers the hosted document route and the canvas capability surface). A reader would assume one gate covers one surface.
- Needed change: state that the switch and escape hatch are read by both the plugin entry and the core canvas module, and name which surfaces each covers.

### The A2UI bundle build entry moved from `.mjs` to `.mts`

- Status: ADVISORY
- Evidence:
  - `package.json:1768` defines `"canvas:a2ui:bundle": "node --import ./scripts/tsx.mjs scripts/bundle-a2ui.mts"`.
  - `scripts/bundle-a2ui.mts` is the build script; there is no `scripts/bundle-a2ui.mjs`.
  - `extensions/canvas/package.json` declares the asset script as `"build": "node --import ../../scripts/tsx.mjs ../../scripts/bundle-a2ui.mts"` with outputs `src/host/a2ui/a2ui.bundle.js` and `src/host/a2ui/a2ui-v0.9.bundle.js`.
  - The artifact's Technical Decisions table says: "Renderer delivery | Prebuilt bundles via `scripts/bundle-a2ui.mjs`".
- Artifact currently says: "Prebuilt bundles via `scripts/bundle-a2ui.mjs`".
- What the code actually does: the script is `scripts/bundle-a2ui.mts`, and the build is also declared as a plugin asset script in `extensions/canvas/package.json` so the standard asset pipeline can invoke it.
- Needed change: correct the script path and note the plugin asset-script declaration.

## Sync drift: 2026-11-16

### A2UI requirements are obsolete because A2UI was retired

- Status: BLOCKING
- Evidence:
  - `src/canvas/widget-tool.ts:43` defines `REMOVED_A2UI_ERROR = 'A2UI widgets were removed; use kind "html"'`, and lines 328 to 339 reject `kind: "a2ui"` during argument preparation and execution.
  - `src/commands/doctor-a2ui-widgets.ts:76-207` backs up agent databases, deletes stored A2UI widgets, and converts other registered-renderer widgets to inert HTML previews.
  - `docs/gateway/doctor/config-migrations.md:62-64` states that A2UI widgets and the `registerBoardWidgetContentKind` Plugin SDK API have been removed.
  - `docs/web/dashboards.md:418-427` carries the same retirement notice.
  - No `@a2ui/*` dependency remains in any `package.json`, and `extensions/canvas/package.json` declares only `typebox` as a runtime dependency.
  - There is no `extensions/canvas/src/a2ui-jsonl.ts`, no `extensions/canvas/src/board-widget.ts`, no `extensions/canvas/src/host/` directory, and no `/__openclaw__/a2ui/` route.
- Artifact currently says: FR-5 requires A2UI JSONL validation, FR-6 requires composing an A2UI board widget document with boot messages and a versioned renderer bundle, FR-7 names the `/__openclaw__/a2ui/` asset route, FR-10 includes rendering A2UI content in the Control UI, NFR-3 names lazy A2UI renderer loading, the Overview describes A2UI JSONL dashboard widgets, the Constraints include an A2UI dashboard rule, and open question 1 asks whether the macOS panel should accept A2UI commands.
- What the code actually does: `show_widget` accepts only `kind: "html"` and rejects A2UI, hosted Canvas documents are HTML records, and A2UI is a retired feature with a Doctor repair path.
- Needed change: remove FR-5 and FR-6, narrow FR-7 and FR-10 to HTML Canvas documents, remove the A2UI clause from NFR-3, rewrite the Overview and Constraints, and retire open question 1.

### Open question 2 about retention now has an answer in code

- Status: ADVISORY
- Evidence:
  - `src/canvas/documents.ts:11` sets `WIDGET_MAX_PER_SCOPE = 32`.
  - `src/canvas/documents.ts:98-140` prunes the oldest documents in a retention scope when the count exceeds 32.
  - `src/canvas/widget-tool.ts:170-175` derives the retention scope from the session id or the agent id.
  - `docs/tools/show-widget.md:475` documents the 32 widget limit.
- Artifact currently says: open question 2 asks whether a retention or quota policy exists for hosted widget documents.
- What the code actually does: core Canvas allows 32 documents per session scope, or per agent scope when no session exists, and removes the oldest on overflow.
- Needed change: resolve open question 2 into a requirement or remove it.

### Implemented Canvas behavior is missing from the requirements

- Status: ADVISORY
- Evidence:
  - `src/canvas/widget-script-syntax.ts` and `src/canvas/widget-script-validation.ts` parse and validate inline JavaScript with line and column diagnostics, with large scripts validated in a worker.
  - `src/canvas/widget-tool.ts:242-254` and `src/canvas/widget-tool.ts:471-521` support native dashboard `report` objects with `pin: true`.
  - `src/canvas/widget-tool.ts:106-123` and `src/canvas/widget-tool.ts:197-203` support current-channel and channel presenters in addition to `node_panel`.
  - `src/canvas/documents.ts:13-39` carries document kind, surface, retention scope, and CSP sandbox fields.
- Artifact currently says: the functional requirements cover the canvas tool, node eligibility, CLI, node panel presenter, A2UI, hosting routes, config, doctor migration, and Control UI rendering only.
- What the code actually does: user-visible `show_widget` behavior, including reports, channel presenters, script syntax validation, and retention, has no requirement in the artifact.
- Needed change: add requirements for these behaviors or explicitly scope them out with a pointer to `docs/tools/show-widget.md`.

### Previously recorded drift remains open

- Status: BLOCKING
- Evidence:
  - The core document record and capability surface in `src/canvas/documents.ts` and `src/canvas/constants.ts` are unchanged from the 2026-10-19 findings.
  - The multi-entry plugin structure in `extensions/canvas/index.ts`, `setup-api.ts`, `doctor-contract-api.ts`, `cli-metadata.ts`, and `runtime-api.ts` is unchanged.
  - Both host gates in `extensions/canvas/src/config.ts:32-37` and `src/canvas/config.ts:7-15` are unchanged.
- Artifact currently says: the 2026-10-19 entries for these items are still marked BLOCKING and the artifacts have not been edited.
- What the code actually does: the drift persists, and the earlier advisory about `scripts/bundle-a2ui.mts` is now moot because that script was deleted with A2UI.
- Needed change: apply the 2026-10-19 needed changes, then recheck against the current code.
