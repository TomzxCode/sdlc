# Conventions

## Naming

- **Files:** kebab-case for source files (e.g., `use-session-store.ts`, `event-pipeline.ts`). React components use PascalCase filenames (e.g., `SettingsView.tsx`, `ChatMessage.tsx`).
- **Variables:** camelCase for local variables and function parameters.
- **Functions / Methods:** camelCase. React hooks use `use` prefix (e.g., `useEventStream`, `useActiveNowStore`). Factory functions use `create` prefix (e.g., `createTunnelProviderRegistry`, `createFsSearchRuntime`).
- **Classes:** PascalCase. Class usage is rare; functional components and factory patterns are preferred.
- **Constants:** UPPER_SNAKE_CASE for module-level constants (e.g., `DEFAULT_PORT`, `TUNNEL_MODE_QUICK`). camelCase for exported config objects.
- **Zustand stores:** Named `use<Domain>Store.ts` (e.g., `useGitStore.ts`, `useSessionFoldersStore.ts`).
- **Package scope:** `@openchamber/` for workspace packages.

## Directory Structure

```
packages/
  ui/             Shared React UI (components, hooks, stores, theme, sync)
    src/
      components/   React components organized by feature (chat/, terminal/, sections/, etc.)
      hooks/        Custom React hooks
      stores/       Zustand stores (split by domain)
      lib/          Shared utilities (theme, typography, opencode client)
      sync/         SSE event pipeline, bootstrap, reconnect logic
  web/            Web server + frontend + CLI
    src/            Frontend entry (main.tsx)
    server/         Express server (index.js is the main entry)
      lib/          Server-side modules (git, github, tunnels, terminal, tts, etc.)
    bin/            CLI entry (cli.js)
    dist/           Built frontend assets
  electron/       Electron desktop app (forward)
    main.mjs        Electron main process
    preload.mjs     Preload script with __TAURI__ IPC shim
  desktop/        Tauri desktop app (legacy, maintenance-only)
    src-tauri/      Rust source for Tauri shell
  vscode/         VS Code extension
    src/            Extension host (extension.ts)
    webview/        Webview frontend (main.tsx)
  docs/           Documentation website source
scripts/          Build, dev, and release scripts
docs/             Static docs (CUSTOM_THEMES.md, REVERSE_PROXY.md, etc.)
.github/workflows/  CI/CD pipelines
```

## Coding Standards

- Functional React components only; no class components
- TypeScript strict mode; avoid `any`, blind casts, and shape guessing
- Use existing theme colors/typography from `packages/ui/src/lib/theme/`; never add new ones without updating the theme system
- All UI colors must use theme tokens; no hardcoded values or Tailwind color classes
- All icons must use the shared Icon component from the SVG sprite system; never import from `@remixicon/react` directly
- Tailwind v4 for styling; typography via `packages/ui/src/lib/typography.ts`
- Prefer early returns and `if/else`/`switch` over nested ternaries
- Prefer dependency injection over hidden module coupling
- Keep orchestration entrypoints thin; move logic into focused modules
- Backend changes must keep web, desktop, and VS Code behavior consistent when they share contracts
- Toasts: use the wrapper from `@/components/ui`; do not import `sonner` directly in feature code
- No comments in code unless explicitly requested
- One sentence per line in markdown files

## Commit Messages

Conventional Commits format observed in practice:

- `feat(scope): description` for new features
- `fix(scope): description` for bug fixes
- `fix(ui): description` for UI-specific fixes
- `chore: description` for maintenance tasks
- `refactor: description` for code restructuring
- `release vX.Y.Z` for version bumps

Lowercase description after the type prefix. Parenthetical scope is common but not always present.

## Branching

- `main` is the development trunk
- Feature branches: `issue-NNNN-descriptive-slug` (e.g., `issue-1346-artful-falcon`)
- Fork-based contribution model: contributors fork and create branches like `fork/issue-NNNN-slug`
- Tags: `vX.Y.Z` for releases
- Kanban branch exists for multi-agent management work

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs
- Reference file paths with `file_path:line_number` format
- Keep diffs tight; avoid drive-by refactors
