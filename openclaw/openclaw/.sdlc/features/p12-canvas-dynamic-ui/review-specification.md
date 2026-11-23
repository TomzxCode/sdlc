---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-10-19

### The plugin architecture diagram is missing five of the plugin's entry points and modules

- Status: BLOCKING
- Evidence:
  - The diagram's Plugin subgraph names `src/tool.ts`, `src/widget-presenter.ts`, `src/board-widget.ts`, `src/a2ui-jsonl.ts`, and `src/host/a2ui.ts`.
  - `extensions/canvas/index.ts` is the runtime entry; `extensions/canvas/setup-api.ts` is the config-migration entry; `extensions/canvas/doctor-contract-api.ts` is the doctor entry; `extensions/canvas/cli-metadata.ts` is the CLI-metadata entry; `extensions/canvas/runtime-api.ts` is the public re-export surface.
  - Additional modules exist: `extensions/canvas/src/node-eligibility.ts` (the shared macOS plus `canvas.present` eligibility rule), `extensions/canvas/src/tool-schema.ts` (the tool parameter schema), `extensions/canvas/src/config.ts` (the config parse and host gate), `extensions/canvas/src/config-migration.ts` (the retired-host migration), `extensions/canvas/src/cli.ts` (the `nodes canvas` commands), `extensions/canvas/src/host/a2ui-route.ts` (the HTTP handler), `extensions/canvas/src/host/a2ui-shared.ts` (the path constants), `extensions/canvas/src/host/file-resolver.ts` (the traversal-safe file resolver), and `extensions/canvas/src/host/a2ui-app/` (the renderer source: `bootstrap.jsx`, `bootstrap-v0.9.jsx`, `host.jsx`, `theme.js`, `host-styles.js`, `rolldown.config.mjs`).
  - `extensions/canvas/src/host/a2ui.ts:1-13` is now a thin re-export of `a2ui-route.ts` plus the path constants, not the route implementation.
- Artifact currently says: the Architecture diagram shows one plugin block with five modules, and the Overview says the plugin "owns the agent-driven visual surface: a lazily loaded `canvas` agent tool, a `node_panel` widget presenter behind core `show_widget`, versioned A2UI renderer bundles served from Gateway routes, and an A2UI board-widget content kind for session dashboards."
- What the code actually does: the plugin is a multi-entry extension with a lazy runtime module, a separate setup entry for the config migration, a separate doctor contract entry, a separate CLI metadata entry, a public runtime API re-export, and a bundled skill. The renderer itself is a JSX app under `src/host/a2ui-app/` that a rolldown build compiles into the two bundles. A reader following the diagram would look for route logic in `src/host/a2ui.ts` and find only re-exports.
- Needed change: redraw the plugin subgraph with the real entry points and modules, including the renderer app source and the build step.

### The hosted widget document is a core-owned record, not a plugin route

- Status: BLOCKING
- Evidence:
  - `src/canvas/documents.ts:13-30` defines the `CanvasDocumentKind` union (`html_bundle`, `url_embed`, `document`, `image`, `video_asset`), the `surface` union (`assistant_message`, `tool_card`, `sidebar`), `retentionScope`, and the `cspSandbox: "scripts"` option.
  - `src/canvas/documents.ts:200` sets the entry URL to `${CANVAS_DOCUMENTS_PATH}/${encodeURIComponent(id)}/index.html`, and `src/canvas/constants.ts:5-6` sets `CANVAS_HOST_PATH = "/__openclaw__/canvas"` and `CANVAS_DOCUMENTS_PATH = "/__openclaw__/canvas/documents"`.
  - `src/canvas/serve.runtime.ts:43-60` handles the request, and `src/canvas/serve.runtime.ts:26-41` resolves a per-document CSP sandbox from the document's `manifest.json`.
  - `src/gateway/server-http-request.ts:565-569` routes the request to the core canvas serve module after the node-capability auth check.
  - `src/canvas/constants.ts:26-33` strips stale plugin-owned canvas capability surfaces and prepends the core-owned one, so the core surface is authoritative.
  - The artifact's API Contracts table says: "GET (prefix) | `/__openclaw__/canvas/*` | Serve hosted widget documents from core storage (core-owned route, Canvas-gated)".
- Artifact currently says: hosted widget documents are served from core storage under `/__openclaw__/canvas/*`, with no data model for the document itself.
- What the code actually does: the document is a structured core record with a kind, a surface, a retention scope, a per-document CSP sandbox decision, and a manifest file; the entry path is `/__openclaw__/canvas/documents/<id>/index.html`; and the core owns the canvas node capability that authorizes the route. The artifact's routing-only view hides the whole document contract.
- Needed change: add a hosted widget document data model, correct the path, and record the core-owned capability surface and per-document CSP sandbox.

### The A2UI renderer source is a Solid app compiled by rolldown, not a prebuilt-only artifact

- Status: BLOCKING
- Evidence:
  - `extensions/canvas/src/host/a2ui-app/` contains `bootstrap.jsx`, `bootstrap-v0.9.jsx`, `host.jsx`, `host-styles.js`, `theme.js`, and `rolldown.config.mjs`.
  - `scripts/bundle-a2ui.mts:29-31` sets the default output to `extensions/canvas/src/host/a2ui/a2ui.bundle.js` and the v0.9 output to `extensions/canvas/src/host/a2ui/a2ui-v0.9.bundle.js`.
  - `scripts/bundle-a2ui.mts:140-148` runs the local rolldown CLI against `extensions/canvas/src/host/a2ui-app/rolldown.config.mjs`, falling back to `pnpm exec rolldown`.
  - `scripts/bundle-a2ui.mts:74-107` requires `@solidjs/compiler`, `@solidjs/web`, `solid-js`, `signal-utils/map`, `@a2ui/web_core/v0_9`, and `@a2ui/lit/ui` to be resolvable, and fails with "A2UI package missing and no complete prebuilt bundle found" when neither the packages nor a complete prebuilt pair exist.
  - `extensions/canvas/package.json` declares the asset script with outputs `src/host/a2ui/a2ui.bundle.js` and `src/host/a2ui/a2ui-v0.9.bundle.js`, and `extensions/canvas/scripts/copy-a2ui.mjs` copies them into the packaged plugin.
  - The artifact's Technical Decisions table says: "Dashboard renderer stack | `solid-js` 2.0.0-rc.14 with `@a2ui/lit` 0.12.0 and `@a2ui/web_core` 0.12.0" and "Renderer delivery | Prebuilt bundles via `scripts/bundle-a2ui.mjs`, served from the Gateway asset route, never copied per widget".
- Artifact currently says: the renderer is delivered as prebuilt bundles, with no mention of the renderer source or the build pipeline.
- What the code actually does: the renderer is a Solid 2 JSX app in the repository that a rolldown build compiles into two prebuilt bundles, which the asset pipeline then copies into the packaged plugin. The "never copied per widget" claim still holds (the copy is per plugin package, not per widget), but the artifact omits the source-of-truth app and the two-stage build-and-copy pipeline entirely. The pinned A2UI versions are also stale.
- Needed change: describe the renderer app, the rolldown build, the two-bundle output, the package-level copy step, and correct the dependency versions.

### The A2UI composition now injects a capability-scoped script URL

- Status: ADVISORY
- Evidence:
  - `extensions/canvas/src/board-widget.ts:22-30` builds the boot script with `{ messages, actionTier: promptGranted ? "prompt" : "state" }`.
  - `extensions/canvas/src/board-widget.ts:32-37` writes the resource script: when the resource URL differs from the path it emits a plain `<script src="...">`, and when it matches it emits an inline script that matches `^/__openclaw__/cap/[^/]+` on `location.pathname` and appends the scoped path as a new script source.
  - `extensions/canvas/src/board-widget.ts:41-53` composes the document as boot script, style, `<openclaw-a2ui-host>`, and the resource script.
  - The artifact's sequence diagram says only: "D->>H: GET versioned renderer bundle" and "D->>D: render via openclaw-a2ui-host".
- Artifact currently says: the document embeds the boot messages, the host element, and the matching versioned bundle URL.
- What the code actually does: the composition also carries an `actionTier` that depends on whether the caller holds prompt authority, and it resolves the bundle through the scoped capability prefix when the resource URL is a bare path. Both affect the rendered document and the security posture.
- Needed change: record the action tier and the capability-scoped script resolution in the composition data model and the sequence.

### The board widget content kind contract is stricter than the artifact implies

- Status: ADVISORY
- Evidence:
  - `src/plugins/board-widget-content-kinds.ts:12` reserves the kinds `html`, `mcp-app`, and `plugin`.
  - `src/plugins/board-widget-content-kinds.ts:13-14` constrains the kind to `^[a-z][a-z0-9-]{0,31}$` and the resource surface to `^[a-z][a-z0-9._-]{0,63}$`.
  - `src/plugins/board-widget-content-kinds.ts:47-58` requires 1 to 8 unique gateway-local absolute resource paths, each at most 256 characters and not equal to the sandbox host path.
  - `extensions/canvas/src/board-widget.ts:36-49` declares the two bundle paths and the `readPublicResource` resolver that returns `undefined` for any other path.
- Artifact currently says: the board kind "exposes only its two registered renderer bundles as public static resources", which matches, but the artifact's data model does not record that the kind id, surface, and path list are validated by the plugin registrar.
- What the code actually does: the content kind is a validated plugin contract with reserved ids, pattern constraints, and a bounded path list. A reader implementing another content kind would not know the constraints.
- Needed change: record the content-kind registration constraints.

### The "FEAT-p8 hosting surface" reference is now a split between two surfaces

- Status: ADVISORY
- Evidence:
  - The artifact's Out of Scope says: "The Control UI chat, dashboard shell, iframe lease, and sandbox policy (FEAT-p8)".
  - `ui/src/app/gateway-canvas-surface.ts:8-42` owns the canvas surface lease, and `ui/src/app/canvas-surface-lease.runtime.ts` is the lazy lease module.
  - `ui/src/components/canvas-widget-view.tsx` renders the hosted document in the canvas widget view using `WidgetSandboxHost` from `ui/src/lib/widget-sandbox-host.ts`.
  - `ui/src/components/board/board-widget-cell.solid.tsx` renders the A2UI board widget through a different path, resolving plugin widget kinds via `ui/src/lib/board/widgets/index.ts`.
  - `src/gateway/board-sandbox.ts` provides `buildBoardWidgetSandboxPath` and `buildBoardWidgetContentSecurityPolicy`, a separate sandbox from the canvas widget sandbox.
  - `.sdlc/features/p19-boards-projects-and-session-cards/requirements.md:12-15` describes boards, dashboards, and session cards as its own feature.
- Artifact currently says: the Control UI surfaces are all FEAT-p8's, and the A2UI board widget renders on "session dashboards".
- What the code actually does: the A2UI board widget renders through the boards subsystem with its own sandbox, which FEAT-p19 now describes, while the hosted canvas document renders through the canvas widget view and its own lease and sandbox. Two different surfaces with two different sandboxes and two different owners.
- Needed change: name the two surfaces separately and point the board-widget surface at FEAT-p19 rather than FEAT-p8.

### The plugin boundary constraint is still true but the plugin now owns a skill

- Status: ADVISORY
- Evidence:
  - The artifact's Constraints say: "The plugin boundary holds: Canvas imports only `openclaw/plugin-sdk/*` and its own local barrels, never core internals."
  - `extensions/canvas/src/board-widget.ts:1` imports `OpenClawPluginApi` from `openclaw/plugin-sdk/plugin-entry`; `extensions/canvas/src/tool.ts:1-12` imports from `openclaw/plugin-sdk/agent-harness-runtime`, `openclaw/plugin-sdk/channel-actions`, `openclaw/plugin-sdk/number-runtime`, `openclaw/plugin-sdk/param-readers`, and `openclaw/plugin-sdk/plugin-entry`; `extensions/canvas/src/host/a2ui-route.ts:1-3` imports from `openclaw/plugin-sdk/file-access-runtime`, `openclaw/plugin-sdk/media-mime`, and `openclaw/plugin-sdk/string-coerce-runtime`. The constraint still holds.
  - `extensions/canvas/skills/canvas/SKILL.md` is new: it tells the agent that `show_widget` with `presentation.target: "node_panel"` is the normal path, that the `canvas` tool is limited to direct panel control, that hosted documents use the capability-scoped `/__openclaw__/canvas/documents/...` route, and that A2UI content renders on session boards.
- Artifact currently says: the plugin owns the agent-driven visual surface, with no mention of a skill.
- What the code actually does: the plugin ships an agent-facing skill that shapes how the model is expected to use the Canvas and `show_widget` paths, including the exact route prefix and the disable switch. The import boundary is unchanged.
- Needed change: note the skill and that it is the agent-facing contract for the Canvas surface.

## Sync drift: 2026-11-16

### The A2UI approach, data models, routes, and sequences are obsolete

- Status: BLOCKING
- Evidence:
  - A2UI was retired. See `src/commands/doctor-a2ui-widgets.ts:76-207`, `docs/gateway/doctor/config-migrations.md:62-64`, and the `REMOVED_A2UI_ERROR` constant in `src/canvas/widget-tool.ts:43`.
  - No `@a2ui/*` dependency remains, `extensions/canvas/src/a2ui-jsonl.ts` and `extensions/canvas/src/board-widget.ts` are gone, the `src/host/a2ui-app/` renderer source is gone, and no `/__openclaw__/a2ui/` route exists.
  - The `registerBoardWidgetContentKind` Plugin SDK API was removed per `docs/gateway/doctor/config-migrations.md:62`.
- Artifact currently says: the Overview promises versioned A2UI renderer bundles and an A2UI board-widget content kind, the Data Models define v0.9 and v0.8 A2UI messages, the API Contracts list the `/__openclaw__/a2ui/*` route, the Sequences include an A2UI dashboard widget flow and an A2UI interaction return flow, and the Technical Decisions define the A2UI dialect, renderer stack, and renderer delivery.
- What the code actually does: Canvas hosts HTML documents in core storage and presents them inline, on a node panel, or pinned to a dashboard. There is no A2UI dialect, renderer, content kind, or route.
- Needed change: delete the A2UI data models, route row, sequences, and technical decisions, and rewrite the Overview around the HTML document flow.

### The architecture diagram does not match the current module layout

- Status: BLOCKING
- Evidence:
  - The diagram's Plugin subgraph names `src/board-widget.ts`, `src/a2ui-jsonl.ts`, and `src/host/a2ui.ts`, none of which exist.
  - Core `src/canvas/` now owns `documents.ts`, `serve.runtime.ts`, `constants.ts`, `config.ts`, `widget-tool.ts`, `wrap.ts`, and the `widget-script-*.ts` family.
  - `extensions/canvas/` keeps `index.ts`, `cli-metadata.ts`, `doctor-contract-api.ts`, `setup-api.ts`, `runtime-api.ts`, and `src/` modules for tool, CLI, config, config migration, and node eligibility.
- Artifact currently says: a single plugin block with five modules plus a Gateway route block that includes the A2UI asset route.
- What the code actually does: Canvas is split between a core document host and a multi-entry plugin, with no A2UI route.
- Needed change: redraw the diagram with the current core and plugin modules and remove the A2UI route node.

### The API contract table is stale

- Status: BLOCKING
- Evidence:
  - `src/canvas/constants.ts:4-6` sets the document path to `/__openclaw__/canvas/documents`, and `src/canvas/documents.ts:193` builds entry URLs as `/__openclaw__/canvas/documents/<id>/index.html`.
  - `src/canvas/serve.runtime.ts:43-101` serves those documents for GET and HEAD only, returns 405 for other methods, and adds a per-document CSP sandbox and no-referrer header.
  - No `CANVAS_DISABLED` string exists in `src/` or `extensions/`.
  - `extensions/canvas/src/tool-schema.ts:9-21` still matches the canvas tool parameter table, and the CLI rows still match `extensions/canvas/src/cli.ts`.
- Artifact currently says: the route table lists `/__openclaw__/a2ui/*` and a generic `/__openclaw__/canvas/*`, and the error code table lists `CANVAS_DISABLED`.
- What the code actually does: only the core document subtree is served, with a stricter path and a different method and header contract, and the `CANVAS_DISABLED` code is gone from the codebase.
- Needed change: correct the path, document GET and HEAD plus the 405 behavior, and remove `CANVAS_DISABLED`.

### Risks and unknowns include retired risks

- Status: ADVISORY
- Evidence: risk 1 depends on two A2UI dialects, and risk 4 depends on renderer root resolution across source, dist, and packaged layouts. Both subsystems were removed.
- Artifact currently says: risks 1 and 4 are open.
- What the code actually does: neither risk can occur. Risks 2 and 3 about capability URL expiry and agent-authored HTML exposure still apply.
- Needed change: remove risks 1 and 4 and recheck risks 2 and 3 against current code.

### Previously recorded drift remains open

- Status: BLOCKING
- Evidence:
  - The core document data model, the dual host gate, the board surface split, and the Canvas skill are unchanged from the 2026-10-19 findings.
  - The 2026-10-19 advisory about board content-kind registration constraints is now moot because the `registerBoardWidgetContentKind` API was removed.
- Artifact currently says: those 2026-10-19 entries remain open in this review file.
- What the code actually does: the drift persists except where A2UI removal superseded it.
- Needed change: apply the still-relevant 2026-10-19 needed changes.

## Sync drift: 2026-11-23

Fresh analysis against the current code confirms the 2026-11-16 drift is still open and unchanged.

### A2UI data models, routes, sequences, and technical decisions still have no implementation

- Status: BLOCKING
- Evidence:
  - A2UI was retired. See `docs/gateway/doctor/config-migrations.md:62-72`, `src/commands/doctor-a2ui-widgets.ts:76-207`, and `src/canvas/widget-tool.ts:43`.
  - `extensions/canvas/package.json:10-12` declares only `typebox`, so no `@a2ui/*` dependency exists.
  - No `extensions/canvas/src/a2ui-jsonl.ts`, `extensions/canvas/src/board-widget.ts`, `src/host/a2ui-app/`, or `/__openclaw__/a2ui/` route exists.
- Artifact currently says: the Overview promises A2UI renderer bundles and a board content kind, the Data Models define v0.9 and v0.8 A2UI messages, the API Contracts list `/__openclaw__/a2ui/*`, the Sequences contain two A2UI flows, and the Technical Decisions define the A2UI dialect, renderer stack, and renderer delivery.
- What the code actually does: Canvas hosts HTML documents in core storage and presents them inline, on a node panel, or pinned to a dashboard.
- Needed change: delete the A2UI data models, route row, sequences, and technical decisions, and rewrite the Overview around the HTML document flow.

### The architecture diagram still names modules that do not exist

- Status: BLOCKING
- Evidence:
  - The diagram's Plugin subgraph names `src/board-widget.ts`, `src/a2ui-jsonl.ts`, and `src/host/a2ui.ts`, none of which exist.
  - `extensions/canvas/src/` contains `cli.ts`, `config.ts`, `config-migration.ts`, `node-eligibility.ts`, `tool-schema.ts`, `tool.ts`, and `widget-presenter.ts`.
  - Core `src/canvas/` owns `documents.ts`, `serve.runtime.ts`, `constants.ts`, `config.ts`, `widget-tool.ts`, `wrap.ts`, and the `widget-script-*.ts` family.
- Artifact currently says: one plugin block with five modules plus a Gateway block with an A2UI asset route.
- What the code actually does: Canvas is split between a core document host and a multi-entry plugin, with no A2UI route.
- Needed change: redraw the diagram with the current core and plugin modules and remove the A2UI route node.

### The API contract table still describes the wrong route and method contract

- Status: BLOCKING
- Evidence:
  - `src/canvas/constants.ts:4-6` sets the document path to `/__openclaw__/canvas/documents`.
  - `src/canvas/documents.ts:193` builds entry URLs as `/__openclaw__/canvas/documents/<id>/index.html`.
  - `src/canvas/serve.runtime.ts:43-101` serves documents for GET and HEAD only, returns 405 for other methods, and adds a per-document CSP sandbox and no-referrer header.
  - No `CANVAS_DISABLED` string exists in `src/` or `extensions/`.
- Artifact currently says: the route table lists `/__openclaw__/a2ui/*` and a generic `/__openclaw__/canvas/*`, and the error code table lists `CANVAS_DISABLED`.
- What the code actually does: only the core document subtree is served, with a stricter path and a different method and header contract, and the `CANVAS_DISABLED` code is gone from the codebase.
- Needed change: correct the path, document GET and HEAD plus the 405 behavior, and remove `CANVAS_DISABLED`.

### Risks 1 and 4 still depend on retired subsystems

- Status: ADVISORY
- Evidence: risk 1 depends on two A2UI dialects and risk 4 depends on renderer root resolution across source, dist, and packaged layouts. Both subsystems were removed.
- Artifact currently says: risks 1 and 4 are open.
- What the code actually does: neither risk can occur.
- Needed change: remove risks 1 and 4 and recheck risks 2 and 3.

### The hosted widget document model is still missing from the specification

- Status: ADVISORY
- Evidence:
  - `src/canvas/documents.ts:13-39` defines the document kind union, the surface union, `retentionScope`, and `cspSandbox: "scripts"`.
  - `src/canvas/constants.ts:8-33` owns the core Canvas node capability surface and strips stale plugin-owned duplicates.
- Artifact currently says: hosted documents are described only as a route with no data model.
- What the code actually does: documents are structured core records with a kind, surface, retention scope, and per-document CSP sandbox.
- Needed change: add a hosted widget document data model and record the core-owned capability surface.
