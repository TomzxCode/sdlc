# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Company | First-order business entity; all business records are company-scoped. One deployment can run many companies with full data isolation. |
| Board | The human operator(s) with full control across all companies in a deployment. In `local_trusted` mode this is implicit; in authenticated mode it is session-based. |
| Board API key | Optional key for board-level access (separate from agent API keys). |
| Agent | An AI employee registered in the org tree with a role, title, reporting line, budget, and adapter configuration. |
| CEO agent | Top-level management agent that proposes strategy (requires board approval before executing delegated work). |
| Org chart / org tree | Strict reporting tree via `reports_to` (nullable root); no multi-manager reporting, no cycles. |
| Goal | A node in the company → team → agent → task alignment hierarchy; at least one root company-level goal per company. |
| Project | A company-scoped grouping that may link to a goal and carry lead agent, target date, and secret-aware env. |
| Issue | The core task entity. Carries company/project/goal/parent links, single assignee, atomic checkout locks, comments, documents, work products, and attachments. |
| Task | Used interchangeably with "issue" in agent/operator contexts (the task system is the issues table). |
| Heartbeat | A scheduled or triggered wakeup that invokes an agent's adapter to do work. |
| Heartbeat run | A tracked execution record (`heartbeat_runs`) with status, context snapshot, and events. |
| Adapter | Translates a heartbeat into a concrete runtime invocation (process, HTTP, CLI session, gateway, or external plugin). |
| Checkout | The atomic operation that claims an issue for execution; sets `assignee_agent_id`, `status=in_progress`, and execution locks. Returns `409` on concurrent claims. |
| Execution lock | Fields (`checkout_run_id`, `execution_run_id`, `execution_locked_at`) that prevent double-work on an issue. |
| Work mode | How an issue is executed: `standard` (autonomous), `ask` (answer-only), or `planning` (plan-only). |
| Work product | A typed deliverable attached to an issue (e.g. artifact with an attachment, or a workspace-file reference). |
| Document | Editable text-first artifact (markdown) with append-only revisions, linked to issues by workflow key (`plan`, `design`, `notes`). |
| Approval | A governance request (`hire_agent`, `approve_ceo_strategy`, budget override, `request_board_approval`) the board approves/rejects. |
| Execution policy | A review/approval stage policy governing how an issue is executed. |
| Routine | A recurring task definition with cron/webhook/API triggers; each execution creates a tracked issue and wakes the assigned agent. |
| Workspace | Either a project workspace or an isolated execution workspace (git worktree) where an agent runs. |
| Task watchdog | A scoped execution capacity for one watched issue subtree that restores live task paths; not board authority and not active-run output monitoring. |
| Plugin | Instance-wide out-of-process extension with capability-gated host services, jobs, tools, and UI contributions. |
| Company portability | Export/import of entire organizations (agents, skills, projects, routines, issues) with secret scrubbing and collision handling. |

## Technical Terms

| Term | Definition |
|---|---|
| Control plane | The Paperclip server + UI that orchestrates agents (as opposed to the execution services/adapters that run them). |
| PGlite | Embedded PostgreSQL used as the dev default when `DATABASE_URL` is unset. |
| Drizzle | The TypeScript ORM used for schema, migrations, and DB clients. |
| Adapter plugin | An external adapter loaded dynamically via `~/.paperclip/adapter-plugins.json` (no hardcoded core imports). |
| Context mode | `thin` (send IDs/pointers; agent fetches via API) vs `fat` (include assignments, goal summary, budget snapshot, recent comments). |
| Cheap model profile | Optional low-cost model lane (`modelProfiles.cheap`) usable only for status-only recovery coordination, never deliverable work. |
| Request depth | Counter incremented as work is delegated down the org tree. |
| Activity log | Immutable audit trail for every mutating action (actor_type, action, entity, details). |
| Budget hard stop | At 100% of monthly UTC budget, the agent is paused and new invocations/checkout are blocked. |
| Greptile | Automated code-review service used in CI; PRs must reach 5/5 with no open P2+ comments. |
| Low-trust preset | A containment control for hostile automated work (not general project/issue privacy). |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| SDLC | Software Development Lifecycle (the `.sdlc/` artifact pipeline) |
| MCP | Model Context Protocol (served by `packages/mcp-server`) |
| OTEL | OpenTelemetry (opt-in tracing instrumentation) |
| SLI / SLO | Service Level Indicator / Service Level Objective |
| SSE | Server-Sent Events (deferred realtime transport) |
| ACL | Access Control List (Pro/Enterprise work-object privacy, deferred for V1) |
| RICE | Reach, Impact, Confidence, Effort (issue prioritization scoring) |
| JWT | JSON Web Token (short-lived run tokens) |
| PGlite | Embedded PostgreSQL (see Technical Terms) |
| CSP | Content Security Policy |
