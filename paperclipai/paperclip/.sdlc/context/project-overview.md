# Project Overview

## Purpose

Paperclip is the open-source control plane for autonomous AI-agent companies.
It is a Node.js server plus React UI that orchestrates a team of AI agents to run a business: bring your own agents, assign goals, and track work and costs from one dashboard.
Where a single agent is an "employee," Paperclip is the "company" — it provides the org chart, ticketing, budgets, governance, goal alignment, and agent coordination that a workforce of agents needs to operate continuously and accountably.
The problem it solves: when the entire workforce is AI agents, a to-do list is not enough; you need a full control plane that manages atomic task ownership, persistent agent state, cost control, approval gates, and auditability.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Board operator (human) | Single human administrator per deployment | Full visibility and control: create companies, hire/fire agents, approve strategy, set budgets, intervene anywhere |
| CEO agent | Top-level management agent | Proposes strategy, delegates work down the org tree (requires board approval before executing) |
| Agent employees | Individual AI agents (Claude Code, Codex, Cursor, OpenClaw, HTTP bots, etc.) | Receive tasks via heartbeats, execute work, report costs, delegate to subordinates |
| Self-hosters / solo entrepreneurs | Operators running their own instance | Local-first, embedded-DB deployment; multi-company isolation; mobile-friendly management |
| Open-source contributors | External developers | Bug fixes, small targeted improvements; plugin-based feature extension |

## Scope

**In scope (V1):**

- Company lifecycle and multi-company data isolation (single-tenant deployment, multi-company data model)
- Goal hierarchy linked to company mission (company → team → agent → task)
- Agent lifecycle with strict-tree org structure and adapter configuration
- Task lifecycle with parent/child hierarchy, atomic checkout, comments, documents, work products, attachments
- Heartbeat invocation, status tracking, and cancellation via adapters (process, http, local CLI, OpenClaw gateway, external plugins)
- Board approvals for hires and CEO strategy; execution policies
- Cost event ingestion and rollups; monthly budget hard-stop auto-pause
- Routines and schedules (cron, webhook, API triggers)
- Workspaces and runtime (project workspaces, execution worktrees, runtime services)
- Local/self-hosted plugin runtime
- Company portability (export/import orgs with secret scrubbing)
- Auditable activity log for all mutating actions
- Board web UI (dashboard, org chart, tasks, agents, approvals, costs, activity)

**Out of scope (V1):**

- Cloud-grade plugin marketplace/distribution beyond local/self-hosted plugin runtime
- Revenue/expense accounting beyond model/token costs
- Knowledge base subsystem
- Public template marketplace (ClipHub)
- Multi-board governance or role-based human permission granularity
- Automatic self-healing orchestration (auto-reassign/retry planners)
- Project/issue-level privacy ACLs and scoped assignment-only object visibility (deferred to Pro/Enterprise)
- Realtime transport optimization (SSE/WebSockets)

## Key Constraints

- Single-assignee task model with atomic checkout required for `in_progress` transition (conflict-safe, returns `409` on concurrent claims)
- Every business record belongs to exactly one company; company boundaries enforced on every fetch/mutation
- Monthly UTC calendar budget window; hard limit at 100% auto-pauses the agent and blocks new invocations
- Node.js 20+, pnpm 9.15+; PostgreSQL via Drizzle (embedded PGlite when `DATABASE_URL` unset)
- Agent API keys hashed at rest; plaintext shown once at creation
- Every mutating request must write an auditable `activity_log` entry
- Reliability targets: API p95 < 250 ms for standard CRUD at 1k tasks/company; heartbeat invoke acknowledgement < 2 s for process adapter
