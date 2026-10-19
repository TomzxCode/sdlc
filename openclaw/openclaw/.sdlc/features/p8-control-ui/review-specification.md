---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Control UI specification

## Sync drift: 2026-10-19

### The overview still describes a Lit web component application (blocking)

- Evidence: `grep -rl "from ['\"]lit" ui/src` returns 0 files, `grep -rl "solid-js" ui/src --include="*.ts" --include="*.tsx"` returns 1316 files, `ui/package.json:36-37,53`, `ui/AGENTS.md:7`, `.sdlc/context/conventions.md:43`
- Artifact says: "The Control UI is a Lit-based web component application served by the gateway's HTTP server. It communicates with the gateway via REST API and WebSocket for real-time updates. Components use legacy decorators for Lit reactive properties." (specification.md:10)
- Code: the Control UI is a Solid 2 application with native DOM primitives. The repository guide forbids Lit and Web Awesome, and the project context already records the Control UI as Solid 2.
- Blocking: every downstream sentence in the artifact (the technical decision row, the decorator risk, the out-of-scope list) inherits this error.

### The Lit technical decision is contradicted by the code (blocking)

- Evidence: `ui/package.json:36-37,53` (`solid-js` `2.0.0-rc.14`, `@solidjs/web` `2.0.0-rc.14`), `ui/package.json:36` (`@solidjs/signals` `2.0.0-rc.14`), `ui/vitest.config.ts` (`controlUiSolidPlugin`), `ui/src/app/app-root.tsx`, `ui/src/components/solid/`
- Artifact says: "| Web framework | Lit (web components) | Native browser API, no build-time framework, legacy decorators for compatibility |" (specification.md:55)
- Code: the framework is Solid 2 with a compiled JSX transform (`@solidjs/vite-plugin`), a signal-based reactive layer (`@solidjs/signals`), and a dedicated `ui/src/components/solid/` component family. There is no `lit` package in `ui/package.json`.
- Blocking: the recorded decision is the opposite of the shipped design and would cause a contributor to add a forbidden dependency.

### The chat flow sequence uses an endpoint that does not exist (blocking)

- Evidence: `specification.md:42-49`, `ui/src/pages/chat/chat-command-executor.ts:593`, `ui/src/pages/chat/chat-commands.ts:157`, `src/gateway/server-methods.ts:281`, `src/gateway/server-methods/chat-send-setup.ts:18`, `packages/gateway-client/src/client.watchdog.test.ts:199`, `src/gateway/remote-control-ui-http-routing.ts:105` (only `/api/chat/media/outgoing/` is an HTTP route)
- Artifact says: "Browser → Gateway: POST /api/chat" (specification.md:45).
- Code: there is no `POST /api/chat` route. The Control UI sends a `chat.send` request over the Gateway Protocol WebSocket, and the Gateway dispatches it in `src/gateway/server-methods.ts` and `src/gateway/server-methods/chat-send-setup.ts`. The only `/api/chat` HTTP routes serve outgoing media artifacts.
- Blocking: the chat contract is the central sequence of the feature and names a transport that was replaced.

### The `ControlUIConfig` data model does not match the configuration schema (blocking)

- Evidence: `src/config/zod-schema.gateway.ts:194-272`, `src/config/schema.gateway-labels.ts:12-31`
- Artifact says: the `ControlUIConfig` table lists `title` (nullable), `theme` (nullable, light or dark), `allowedOrigins` (nullable) (specification.md:32-36).
- Code: `gateway.controlUi` is a strict object with `enabled`, `basePath`, `experimental` (`customPlugins`, `claws`, `chatBubbles`, `composerPredictions`), `root`, `environment` (`label`, `color`), `communityInvite`, `newSessionModelDefaults`, `github` (`host`, `token`), `sessionObserver`, `embedSandbox`, `allowExternalEmbedUrls`, `automaticallyFetchFavicons`, `allowedOrigins`, and `dangerouslyAllowHostHeaderOriginFallback`. There is no `title` field and no `theme` field.
- Blocking: two of the three documented fields do not exist, and thirteen real fields are absent.

### The architecture diagram omits the embedded subsystems (blocking)

- Evidence: `specification.md:14-26`, `ui/src/pages/terminal/terminal-page.tsx`, `ui/src/components/desktop/desktop-client.ts`, `ui/src/pages/chat/components/file-editor-view.ts`, `ui/src/plugins/control-ui-host.ts`
- Artifact says: the diagram shows only "Browser (SPA) / REST API (config, sessions, status) / WebSocket (streaming chat, real-time updates) / Gateway Server" with three gateway files (specification.md:14-26).
- Code: the Control UI also hosts a terminal, a noVNC desktop surface, a CodeMirror editor, and plugin-provided views, and the gateway side now has a dedicated `src/gateway/server-methods/` method family rather than a single `server-methods.ts` file.
- Blocking: the diagram is the reader's map of the feature and it leaves out every embedded surface.

### The "Plugin-provided UI components" out-of-scope entry is contradicted (blocking)

- Evidence: `specification.md:74`, `ui/src/plugins/control-ui-view.solid.tsx`, `ui/src/plugins/control-ui-contributions.solid.tsx`, `ui/src/plugins/control-ui-manager.solid.tsx`, `src/plugins/registry-control-ui.ts:76-83`, `src/plugins/host-hooks.ts:99`, `src/config/zod-schema.gateway.ts:206-221`
- Artifact says: "## Out of Scope" lists "- Plugin-provided UI components" (specification.md:74).
- Code: plugin Control UI surfaces are a first-class, shipped capability with seven surface kinds, a registry, a manager, a settings view, and a configuration flag.
- Blocking: the artifact excludes a capability the code implements and the runtime advertises.

### The decorator risk is resolved (advisory)

- Evidence: `specification.md:62`
- Artifact says: "1. Legacy decorators are tied to TypeScript `experimentalDecorators`; future migration needed" (specification.md:62).
- Code: the migration is complete. The UI compiles Solid JSX through `@solidjs/vite-plugin` and no decorator configuration remains in the UI build.
- Advisory: a resolved risk should be removed, but leaving it does not mislead about current behavior.

### The CSP risk is understated (advisory)

- Evidence: `src/gateway/control-ui-csp.ts:1-60`, `src/gateway/control-ui-csp.test.ts`, `src/gateway/remote-control-ui-http-routing.ts:105`
- Artifact says: "2. CSP hardening may break inline script patterns used by some plugins" (specification.md:63).
- Code: the CSP owner computes SHA-256 hashes for inline scripts (`computeInlineScriptHashes`) and separately maintains frame-ancestor policy for hosted Control UI embeds, so the risk is partly mitigated and the embed surface is larger than the artifact implies.
- Advisory.

### The styling decision omits the CSS ownership rules (advisory)

- Evidence: `specification.md:56`, `ui/AGENTS.md:57-65`
- Artifact says: "| Styling | CSS (no framework) | Minimal dependencies, full control |" (specification.md:56).
- Code: styling is plain CSS, but with strict ownership rules: token colors from `ui/src/styles/base.css`, a fixed breakpoint ladder, no `@layer`, and a `:has()` selector restriction enforced by stylelint.
- Advisory: the decision is still true, but the constraints it now operates under are worth recording.
