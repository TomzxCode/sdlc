# Architecture

## System Overview

Paperclip is a single-process Node.js control plane that orchestrates externally-running AI agents. The server hosts the REST API, serves the React UI in dev middleware mode, runs a lightweight in-process scheduler/worker, and talks to PostgreSQL (embedded PGlite in dev). Agents never run inside Paperclip; they phone home over the API using bearer keys, and adapters translate heartbeats into whatever runtime each agent lives in.

```
                      ┌──────────────── PAPERCLIP SERVER ────────────────┐
                      │  Express REST API (/api)   React UI (Vite, dev)    │
                      │  Auth (board sessions + agent API keys + run JWTs) │
                      │  Lightweight in-process scheduler/worker           │
                      │  (heartbeat triggers, stuck-run detection, budgets)│
                      └───────────────┬───────────────────────────────────┘
                                      │ Drizzle ORM
                          ┌───────────┴────────────┐
                          │ PostgreSQL             │  embedded PGlite in dev
                          │ (companies, agents,    │  (data/pglite)
                          │  issues, runs, costs…)  │
                          └────────────────────────┘
                                      ▲ bearer API keys / run JWTs
   ┌──────────┐  ┌──────────┐  ┌──────┴───────┐  ┌────────────┐  ┌────────────┐
   │ Claude   │  │  Codex   │  │  CLI agents │  │  HTTP/web  │  │ OpenClaw   │
   │  Code    │  │ adapter  │  │ Cursor/Gem/ │  │  webhook   │  │ gateway    │
   │ adapter  │  │          │  │ pi/opencode │  │  bots      │  │            │
   └──────────┘  └──────────┘  └─────────────┘  └────────────┘  └────────────┘
        process / local CLI adapters        http adapter       gateway adapter
   ── external adapter plugins loaded via ~/.paperclip/adapter-plugins.json ──
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| `server/` | Express REST API, auth, orchestration services, in-process scheduler | Node.js, TypeScript, Express |
| `ui/` | Board operator interface (dashboard, org chart, tasks, approvals, costs) | React, Vite, TypeScript |
| `packages/db/` | Drizzle schema, migrations, DB clients (Postgres + embedded PGlite) | Drizzle ORM, PostgreSQL, PGlite |
| `packages/shared/` | Shared API types, constants, validators, API path constants | TypeScript |
| `packages/adapters/` | Adapter package implementations (claude-local, codex-local, cursor-local, gemini-local, opencode-local, pi-local, openclaw-gateway, cursor-cloud, grok-local, acpx-local) | TypeScript |
| `packages/adapter-utils/` | Shared adapter utilities | TypeScript |
| `packages/plugins/` | Plugin system: SDK, create-paperclip-plugin, sandbox providers, example plugins | TypeScript |
| `packages/mcp-server/` | MCP server package | TypeScript |
| `packages/skills-catalog/`, `packages/teams-catalog/` | Skills and teams catalogs | TypeScript |
| `server/src/realtime/` | WebSocket real-time events (live dashboards, terminal sessions) | TypeScript, WebSocket |
| `server/src/services/tool-access.ts`, `tool-gateway.ts` | Third-party tool/connection integration (OAuth, MCP/SSE gateways, access policies, runtime slots) | TypeScript |
| `server/src/secrets/` | Secrets provider implementations (local-encrypted, AWS, GCP, Vault) and provider registry | TypeScript |
| `server/src/auth/` | Auth middleware (bearer token, session, board/agent resolution) | TypeScript |
| `server/src/services/pipelines.ts` | Pipeline management (stages, cases, automation, transitions, events) | TypeScript |
| `server/src/services/cloud-upstreams.ts` | Cross-instance company sync via OAuth (experimental) | TypeScript |
| `cli/` | `paperclipai` CLI (onboard, configure, plugin install) | TypeScript (tsx) |
| `doc/` | Operational and product docs (SPEC, GOAL, PRODUCT, DATABASE, DEVELOPING) | Markdown |

## Data Flow

1. A board operator creates a company, defines goals, and hires/configures agents (org tree via `reports_to`).
2. Agents authenticate with bearer API keys (hashed at rest) scoped to one company.
3. The in-process scheduler wakes agents on their heartbeat schedule (or on event triggers / @-mentions); it skips invocation when an agent is paused/terminated, a run is active, or the hard budget limit is hit.
4. The heartbeat execution service resolves workspace, injects secrets, loads skills, and invokes the agent's adapter (process spawn, HTTP call, CLI session, gateway, or external plugin).
5. Adapters stream stdout/stderr to run logs and report status; runs produce structured logs, cost events, session state, and audit trails.
6. Agents receive tasks via atomic checkout (single SQL update with `WHERE` guards), execute, write comments/documents/work products, report cost events, and delegate down the org tree (incrementing `request_depth`).
7. Cost events aggregate into per-company/agent/project/goal rollups; budget enforcement auto-pauses agents at the hard limit.
8. Every mutating action is written to `activity_log` for auditability; governance approvals gate hires and CEO strategy.

## Infrastructure

- **Runtime:** Node.js 20+, pnpm 9.15+ workspace monorepo (`pnpm-workspace.yaml` covers `packages/*`, `packages/adapters/*`, `packages/plugins/*`, `server`, `ui`, `cli`).
- **Database:** PostgreSQL in production; embedded PGlite at `~/.paperclip/instances/default/db` when `DATABASE_URL` is unset (dev default). Drizzle migrations are source of truth and auto-applied on dev startup.
- **File/object storage:** local disk default (`~/.paperclip/instances/default/data/storage`); S3-compatible object storage optional.
- **Deployment modes:** `local_trusted` (implicit board, loopback) or `authenticated` (session-based) with `private`/`public` exposure policy (see `doc/DEPLOYMENT-MODES.md`).
- **CI/CD:** GitHub Actions; `pnpm test` (Vitest) is the cheap default; `pnpm test:e2e` and `pnpm test:release-smoke` are opt-in Playwright suites.
- **Observability:** opt-in OpenTelemetry auto-instrumentation (traces) when `OTEL_EXPORTER_OTLP_ENDPOINT` is set (`@opentelemetry/*` are optional peer deps); structured JSON logs in production with per-request IDs.
- **Secrets:** Pluggable provider vault (default: local encrypted file); AWS Secrets Manager, GCP, and Vault optional; every secret access audited via `secret_access_events` table.
- **Releasing:** `scripts/release.sh` (canary/stable), npm package publishing via `scripts/build-npm.sh`, GitHub releases via `scripts/create-github-release.sh`.

## Architecture Decisions

Key V1 product decisions are documented in `doc/SPEC-implementation.md` §3 (tenancy, board model, org graph shape, visibility, communication, task ownership, recovery, adapter strategy, budget period/enforcement, deployment modes).
Formal architecture/implementation decision records created during the pipeline live under `.sdlc/knowledge/decisions/`.
Notable decisions: single-tenant deployment with multi-company data model; strict tree org graph (`reports_to` nullable root); tasks+comments only (no separate chat); atomic single-assignee checkout; soft alerts + hard-limit auto-pause on monthly UTC budget window.
