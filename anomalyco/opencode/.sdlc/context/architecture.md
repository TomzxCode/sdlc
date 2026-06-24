# Architecture

## System Overview

OpenCode is a TypeScript monorepo (Bun workspaces) built around a durable session runtime.
A core server process owns sessions, the tool registry, provider adapters, and storage, while thin clients (TUI, web, desktop) connect to it.

```
                         ┌─────────────────────────────────────────────┐
   TUI (opentui/Solid)   │             OpenCode Core Server            │
   Web app (SolidJS)  ──▶│  ┌──────────────┐   ┌────────────────────┐  │
   Desktop (Electron)    │  │   Session     │   │  System Context     │  │
   VSCode extension      │  │   Runtime V2  │──▶│  Registry + Epochs  │  │
                        │  └──────┬───────┘   └────────────────────┘  │
   HTTP/SDK clients   ──▶│         │ provider turns                    │
                        │  ┌──────▼───────┐   ┌────────────────────┐  │
                        │  │ Agent + Tool  │   │  LLM Provider Layer │──▶ providers
                        │  │ Registry      │   │  (Catalog/adapters) │   (models.dev)
                        │  └──────┬───────┘   └────────────────────┘  │
                        │         │ durable history / tool output      │
                        │  ┌──────▼───────────────────────────────┐   │
                        │  │  Storage (SQLite via Effect/Drizzle)  │   │
                        │  └──────────────────────────────────────┘   │
                        └─────────────────────────────────────────────┘
                  plugins (hooks) · MCP servers · skills · snapshot/share/sync
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| `packages/opencode` | Core business logic and server: sessions, config, server, tools, providers, plugins | TypeScript, Bun, Effect |
| `packages/tui` + `packages/opencode/src/cli/cmd/tui` | Terminal UI | SolidJS, opentui |
| `packages/app` | Shared web UI components | SolidJS, Tailwind, Vite |
| `packages/desktop` | Native desktop app wrapping the web UI | Electron |
| `packages/server` | HTTP API surface / server package | Hono, Effect |
| `packages/llm` | Standalone Effect Schema-first LLM core: route/protocol/endpoint/auth architecture, provider adapters, tool dispatch | Effect |
| `packages/core` | Shared core: database, Effect services, system context, session runner, PTY, config, tools, agents, providers, plugins, permissions | TypeScript, Effect, Drizzle |
| `packages/plugin` | Source for `@opencode-ai/plugin` (plugin SDK) | TypeScript |
| `packages/sdk` (`packages/sdk/js`) | Generated TypeScript client SDK | TypeScript (generated) |
| `packages/cli` | Standalone CLI distribution package | TypeScript |
| `packages/ui` | Shared UI primitives | SolidJS |
| `packages/server` / `packages/function` / `packages/identity` | Cloud/enterprise services (console, auth, stats) | Hono, SST, OpenAuth |
| `packages/effect-sqlite-node`, `effect-drizzle-sqlite` | Effect-integrated SQLite storage adapters | Effect, Drizzle, Bun SQLite |
| `packages/http-recorder` | Deterministic record/replay of Effect HTTP traffic | Effect |
| `packages/slack` | Slack bot integration | TypeScript, @slack/bolt |
| `packages/enterprise` | Enterprise self-hosted web app (teams, projects) | SolidJS, Hono, SST |
| `packages/schema` | Shared Effect Schema definitions | Effect |
| `github/` | GitHub Actions composite action for running in CI | TypeScript |
| `sdks/vscode` | VSCode editor extension | TypeScript |

## Data Flow

1. A client (TUI/web/desktop/SDK) sends a prompt to the server for a project/session.
2. The Session runtime admits a durable `session_input` row, then schedules advisory execution.
3. The runner promotes eligible input into session history at a safe provider-turn boundary and renders the baseline system context for the current context epoch.
4. One `llm.stream(request)` call is made to the selected provider for the turn.
5. Tool calls returned by the model are executed through the Location-scoped tool registry; bounded tool output is persisted to history and oversized output spills to managed tool-output files.
6. Compaction starts a new context epoch with a fresh baseline when history grows too large.
7. Mid-conversation system messages are emitted durably when context sources change, admitted lazily at the next safe boundary.

## Infrastructure

- **CI/CD:** GitHub Actions (`.github/workflows`) with 26 workflows covering test, typecheck, lint, publish, containers, docs, triage, pr-standards, release, storybook, Nix builds, SDK regeneration, and more.
- **Lint/format:** oxlint (lint) and prettier; `bun typecheck` runs turbo typecheck across packages.
- **Cloud:** SST (`sst.config.ts`) defines stages for app, console, enterprise, lake, monitoring, stats, identity; infra lives under `infra/`.
- **Distribution:** npm (`opencode-ai`), Homebrew, Scoop, Chocolatey, pacman, AUR, mise, Nix, plus an `install` script and GitHub releases for desktop builds.
- **Build:** single-executable local builds via `packages/opencode/script/build.ts --single`.
- **Observability:** Effect telemetry/OpenTelemetry hooks; Sentry for error tracking (`@sentry/solid`, `@sentry/vite-plugin`); per-service monitoring defined in `infra/monitoring.ts`.

## Architecture Decisions

- The V2 session core keeps durable prompt admission separate from model execution; see `CONTEXT.md` and `specs/v2/` for the full algebra.
- One explicit `llm.stream` call per provider turn; history is reloaded before durable continuation.
- Provider support is data-driven through models.dev rather than per-provider code.
- Storage is SQLite accessed through Effect/Drizzle adapters (see `specs/storage/`).
- Formal ADRs live under `.sdlc/knowledge/decisions/`.
