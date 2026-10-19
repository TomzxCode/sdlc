---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Control UI requirements

## Sync drift: 2026-10-19

### The Lit constraint is contradicted by the code (blocking)

- Evidence: `grep -rl "from ['\"]lit" ui/src` returns 0 files, `grep -rl "solid-js" ui/src --include="*.ts" --include="*.tsx"` returns 1316 files, `ui/package.json:36-37,53` lists `solid-js` `2.0.0-rc.14`, `@solidjs/web` `2.0.0-rc.14`, and `@solidjs/signals` `2.0.0-rc.14`, and no `lit` package, `ui/AGENTS.md:7`
- Artifact says: "Uses Lit web components (legacy decorators)" (requirements.md:45).
- Code: the Control UI is a Solid 2 application. It uses `solid-js`, `@solidjs/signals`, and `@solidjs/web` at `2.0.0-rc.14`, and it has no `lit` dependency. The repository guide states: "The Control UI and its plugin views use Solid 2 and native primitives; never add Lit or Web Awesome." (`ui/AGENTS.md:7`). The project context agrees: `ui/` is described as "Control UI (Solid 2 web components)" (`.sdlc/context/conventions.md:43`).
- Blocking: the constraint tells an implementer to use a framework the repository forbids.

### The feature scope omits four shipped subsystems (blocking)

- Evidence: `ui/src/pages/terminal/terminal-page.tsx`, `ui/src/components/terminal/`, `packages/terminal-core/`, `ui/package.json:26` (`@openclaw/libterminal`), `ui/package.json:43` (`ghostty-web`), `src/config/zod-schema.gateway.ts:286-299` (`gateway.terminal`), `ui/src/components/desktop/desktop-client.ts`, `ui/package.json:23` (`@novnc/novnc`), `ui/src/pages/chat/components/file-editor-view.ts`, `ui/package.json:12-16` (`@codemirror/*`), `ui/src/plugins/control-ui-contributions.solid.tsx`, `ui/src/plugins/control-ui-view.solid.tsx`
- Artifact says: "It provides a chat interface, session management, configuration access, system status monitoring, and plugin management." (requirements.md:10), with ten functional requirements that cover none of these.
- Code: the Control UI also ships an operator terminal page backed by `ghostty-web` and `@openclaw/libterminal` with a `gateway.terminal` configuration block, a remote desktop viewer backed by `@novnc/novnc`, a CodeMirror file and diff editor, and a plugin view and contribution surface that renders plugin-supplied UI.
- Blocking: a reader of this artifact would not know the Control UI now embeds a shell, a remote desktop, a code editor, and plugin-rendered views.

### Plugin-provided UI components are in scope, not out of scope (blocking)

- Evidence: `ui/src/plugins/control-ui-view.solid.tsx`, `ui/src/plugins/control-ui-contributions.solid.tsx`, `ui/src/plugins/control-ui-manager.solid.tsx`, `ui/src/plugins/control-ui-settings-view.solid.tsx`, `src/plugins/registry-control-ui.ts:76-83`, `src/plugins/host-hooks.ts:99`, `src/config/zod-schema.gateway.ts:206-221` (`gateway.controlUi.experimental.customPlugins`)
- Artifact says: "## Out of Scope" lists "- Plugin-provided UI components" (requirements.md:75) and the requirements only promise a "plugin management interface" (requirements.md:31).
- Code: plugins register Control UI surfaces across seven kinds (`session`, `tool`, `run`, `settings`, `tab`, `widget`, `link-reader`) and the Control UI renders them through Solid views and contributions. A configuration flag enables custom plugin UI.
- Blocking: the artifact declares a shipped capability out of scope.

### The configuration access requirement understates the shipped settings surface (advisory)

- Evidence: `ui/src/pages/config/config-page.tsx`, `ui/src/pages/config/curated-settings.tsx`, `ui/src/pages/config/view-raw.browser.test.tsx`, `src/config/zod-schema.gateway.ts:194-272`
- Artifact says: "FR-7 | Should | The Control UI shall support viewing and editing configuration" (requirements.md:29).
- Code: the Control UI has a curated settings editor, a raw JSON view, and a large set of routed settings pages under `ui/src/pages/config/`.
- Advisory: the requirement still holds, but it is now one of many settings surfaces.

### The dark mode requirement is still accurate but understates theming (advisory)

- Evidence: `ui/src/app/theme.test.ts`, `ui/src/app/custom-theme.test.ts`, `ui/src/app/bootstrap-theme.ts`, `ui/src/pages/config/custom-theme-import.ts`
- Artifact says: "FR-10 | May | The Control UI shall support dark mode" (requirements.md:32).
- Code: theming goes beyond a light and dark switch to custom theme import, a palette system rooted in `ui/src/styles/base.css`, and a branded theme model.
- Advisory.

### Open question 1 is answered in code (advisory)

- Evidence: `ui/src/app/app-host.tsx`, `ui/src/app/app-shell-gateway.ts`, `ui/src/lib/sessions/session-placement-startup.ts`, `src/gateway/server-methods/chat-send-*.ts`
- Artifact says: "1. Should the Control UI support multiple simultaneous chat sessions?" (requirements.md:62)
- Code: the Control UI supports multiple concurrent sessions through a session roster, a held-window reconciler, and a gateway-scoped session list, and the chat route is keyed by session.
- Advisory: the question should be closed.

### Open question 2 is partly answered (advisory)

- Evidence: `ui/src/e2e/`, `ui/vitest.config.ts:1-10` (Playwright browser project), `ui/src/pages/chat/`, `docs/help/testing/`
- Artifact says: "2. What is the target mobile browser support for the Control UI?" (requirements.md:63)
- Code: the Control UI has a Playwright browser test project and dedicated phone scenarios, including `ui/src/e2e/phone-stale-build-recovery.e2e.test.ts`, but there is no stated browser support matrix in the tree.
- Advisory: the question is partially answered by the presence of phone-specific test lanes.
