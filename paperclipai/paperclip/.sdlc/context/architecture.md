# Architecture

## System Overview

Paperclip is a single-process Node.js control plane that orchestrates externally-running AI agents.
The server hosts the REST API, serves the React UI in dev middleware mode, runs a lightweight in-process scheduler/worker, and talks to PostgreSQL (embedded PGlite in dev).
Agents never run inside Paperclip; they phone home over the API using bearer keys, and adapters translate heartbeats into whatever runtime each agent lives in.

```mermaid
block-beta
  columns 5
  claude["Claude Code adapter"]:1
  codex["Codex adapter"]:1
  cliagents["CLI agents\nCursor / Gemini / pi / opencode / Kimi"]:1
  httpbots["HTTP / webhook bots"]:1
  claw["OpenClaw gateway"]:1
  plugins["External adapter plugins (loaded via ~/.paperclip/adapter-plugins.json)"]:5
  server["PAPERCLIP SERVER\nExpress REST API (/api) + React UI (Vite, dev middleware)\nAuth: board sessions + agent API keys + run JWTs\nIn-process scheduler/worker (heartbeat triggers, stuck-run detection, budgets)"]:5
  db["PostgreSQL (embedded PGlite in dev)\nDrizzle ORM — companies, agents, issues, runs, costs..."]:5
  claude --> server
  codex --> server
  cliagents --> server
  httpbots --> server
  claw --> server
  plugins --> server
  server --> db
```

## Entity Relationship Diagram

The full detailed database schema (types, constraints, indexes) lives in `.sdlc/context/schema.dbml`.
The diagram below shows the core domain entities and their relationships only.

```mermaid
erDiagram
  companies {
    uuid id
    string name
    string status
    int budget_monthly_cents
    int spent_monthly_cents
  }
  agents {
    uuid id
    uuid company_id
    string name
    string status
    uuid reports_to
    string adapter_type
    int budget_monthly_cents
    int spent_monthly_cents
  }
  goals {
    uuid id
    uuid company_id
    string title
    string level
    string status
    uuid parent_id
    uuid owner_agent_id
  }
  projects {
    uuid id
    uuid company_id
    uuid goal_id
    string name
    string status
    uuid lead_agent_id
  }
  issues {
    uuid id
    uuid company_id
    uuid project_id
    uuid goal_id
    uuid parent_id
    string status
    uuid assignee_agent_id
    uuid checkout_run_id
    uuid execution_run_id
    int request_depth
  }
  heartbeat_runs {
    uuid id
    uuid company_id
    uuid agent_id
    string status
    string invocation_source
  }
  heartbeat_run_events {
    uuid id
    uuid run_id
    int seq
    string kind
  }
  cost_events {
    uuid id
    uuid company_id
    uuid agent_id
    uuid issue_id
    uuid heartbeat_run_id
    string provider
    string model
    int cost_cents
  }
  budget_policies {
    uuid id
    uuid company_id
    string scope_type
    uuid scope_id
    int amount
    boolean hard_stop_enabled
  }
  pipelines {
    uuid id
    uuid company_id
    uuid project_id
    string key
    string name
  }
  pipeline_stages {
    uuid id
    uuid pipeline_id
    string key
    string kind
    int position
  }
  pipeline_cases {
    uuid id
    uuid company_id
    uuid pipeline_id
    uuid stage_id
    string case_key
    uuid parent_case_id
  }
  cases {
    uuid id
    uuid company_id
    uuid project_id
    string identifier
    string case_type
    string status
    uuid parent_case_id
  }
  approvals {
    uuid id
    uuid company_id
    string type
    string status
    uuid requested_by_agent_id
  }
  company_secrets {
    uuid id
    uuid company_id
    string key
    string provider
    string status
    int latest_version
  }
  agent_api_keys {
    uuid id
    uuid company_id
    uuid agent_id
    string key_hash
  }
  activity_log {
    uuid id
    uuid company_id
    string actor_type
    string action
    string entity_type
    string entity_id
    uuid run_id
  }
  companies ||--o{ agents : "employs"
  agents ||--o{ agents : "reports_to (strict tree)"
  companies ||--o{ goals : "defines"
  goals ||--o{ goals : "parent/child"
  agents ||--o{ goals : "owns"
  companies ||--o{ projects : "has"
  goals ||--o{ projects : "groups"
  agents ||--o{ projects : "leads"
  companies ||--o{ issues : "tracks"
  projects ||--o{ issues : "contains"
  goals ||--o{ issues : "advances"
  issues ||--o{ issues : "parent/child"
  agents ||--o{ issues : "assigned (single assignee)"
  agents ||--o{ heartbeat_runs : "executes"
  heartbeat_runs ||--o{ heartbeat_run_events : "logs"
  issues ||--o{ heartbeat_runs : "checked out by"
  agents ||--o{ cost_events : "incurs"
  issues ||--o{ cost_events : "attributes"
  heartbeat_runs ||--o{ cost_events : "reports"
  companies ||--o{ budget_policies : "enforces"
  companies ||--o{ pipelines : "owns"
  projects ||--o{ pipelines : "scopes"
  pipelines ||--o{ pipeline_stages : "has"
  pipelines ||--o{ pipeline_cases : "tracks"
  pipeline_stages ||--o{ pipeline_cases : "holds"
  pipeline_cases ||--o{ pipeline_cases : "parent/child"
  companies ||--o{ cases : "owns"
  cases ||--o{ cases : "parent/child"
  companies ||--o{ approvals : "gates"
  agents ||--o{ approvals : "requests"
  companies ||--o{ company_secrets : "vaults"
  agents ||--o{ agent_api_keys : "authenticates"
  companies ||--o{ agent_api_keys : "scopes"
  companies ||--o{ activity_log : "audits"
  heartbeat_runs ||--o{ activity_log : "attributes"
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| `server/` | Express REST API, auth, orchestration services, in-process scheduler | Node.js, TypeScript, Express |
| `ui/` | Board operator interface (dashboard, org chart, tasks, approvals, costs) | React, Vite, TypeScript |
| `packages/db/` | Drizzle schema, migrations, DB clients (Postgres + embedded PGlite) | Drizzle ORM, PostgreSQL, PGlite |
| `packages/shared/` | Shared API types, constants, validators, API path constants | TypeScript |
| `packages/adapters/` | Adapter package implementations (claude-local, codex-local, cursor-local, cursor-cloud, gemini-local, grok-local, kimi-local, opencode-local, pi-local, hermes, hermes-gateway, openclaw-gateway; shared ACPX engine lives in `packages/adapter-utils/`) | TypeScript |
| `packages/adapter-utils/` | Shared adapter utilities | TypeScript |
| `packages/plugins/` | Plugin system: SDK, create-paperclip-plugin, sandbox providers, example plugins | TypeScript |
| `packages/mcp-server/` | MCP server package | TypeScript |
| `packages/skills-catalog/`, `packages/teams-catalog/` | Skills and teams catalogs | TypeScript |
| `skills/` | Paperclip runtime/operational skills (not part of the app catalog) | Markdown, scripts |
| `server/src/realtime/` | WebSocket real-time events (live dashboards, terminal sessions) | TypeScript, WebSocket |
| `server/src/services/tool-access.ts`, `tool-gateway.ts` | Third-party tool/connection integration (OAuth, MCP/SSE gateways, access policies, runtime slots) | TypeScript |
| `server/src/secrets/` | Secrets provider implementations (local-encrypted, AWS, GCP, Vault) and provider registry | TypeScript |
| `server/src/auth/` | Auth middleware (bearer token, session, board/agent resolution) | TypeScript |
| `server/src/services/pipelines.ts` | Pipeline management (stages, cases, automation, transitions, events) | TypeScript |
| `server/src/services/company-transfer-runs.ts`, `company-import-transfers.ts`, `cloud-instance.ts`, `paperclip-cloud-connector.ts` | Cross-instance company transfer/sync and Paperclip Cloud connector | TypeScript |
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

- Hosting: single-process Node.js control plane backed by PostgreSQL, with embedded PGlite as the dev default when `DATABASE_URL` is unset.
- Deployment topology: `local_trusted` (implicit board on loopback) or `authenticated` (session-based) modes with `private`/`public` exposure policy; file/object storage defaults to local disk with S3-compatible storage optional.
- Detailed technology stack, development tooling, CI/CD pipelines, environments, deployment procedures, and rollback live in `infrastructure.md`.
- Monitoring stack, alerting, and dashboards live in `observability.md`.

## Architecture Decisions

Key V1 product decisions are documented in `doc/SPEC-implementation.md` §3 (tenancy, board model, org graph shape, visibility, communication, task ownership, recovery, adapter strategy, budget period/enforcement, deployment modes).
Formal architecture/implementation decision records created during the pipeline live under `.sdlc/knowledge/decisions/`.
Notable decisions: single-tenant deployment with multi-company data model; strict tree org graph (`reports_to` nullable root); tasks+comments only (no separate chat); atomic single-assignee checkout; soft alerts + hard-limit auto-pause on monthly UTC budget window.
