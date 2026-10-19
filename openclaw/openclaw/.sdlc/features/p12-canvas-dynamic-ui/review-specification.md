---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
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
