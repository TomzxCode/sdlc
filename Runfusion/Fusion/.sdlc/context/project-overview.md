# Project Overview

## Purpose

Fusion is a software factory: a model- and surface-agnostic multi-agent orchestrator that converts a rough idea into planned, built, reviewed, and merged code.
It is an AI-orchestrated task board where each task runs through a workflow graph, and AI agents plan, implement, review, and ship the work in isolated git worktrees, with configurable human approval gates and auto-merge controls.
Board columns are defined by the workflow, not hard-coded in the engine.
The default workflow (`builtin:coding`) declares six columns: triage, todo, in-progress, in-review, done, and archived.
It is neutral by design across models, workflows, and surfaces: the same board is driven from an Electron desktop app, a browser web dashboard, a Capacitor mobile app, and the `fn` CLI with its terminal UI, and it runs across many machines (nodes) in a fleet.
Two npm packages are published: `@runfusion/fusion` (the `fn` CLI plus a `pi` extension) and the `runfusion.ai` alias package.
The `@fusion/*` packages are private and ship bundled inside the published CLI.
Current workspace version: `0.78.0-beta.7` (root `package.json`, package name `fusion-workspace`).

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Solo developer | Primary user | Drives many coding-agent sessions across machines and surfaces without losing track, and ships code through Fusion |
| Operator / power user | Board and workflow owner | Defines selectable workflows, agent presets, approval gates, and monitors in-flight work |
| Plugin / extension author | Third-party developer | Extends the dashboard and engine through the plugin SDK and `pi` extensions |
| Open-source community | Adopter and contributor | Runs Fusion on their own hardware under the MIT license, with no vendor lock-in |
| Maintainer / contributor | Internal team | Keeps the multi-package monorepo consistent, tested, and releasable |

The repository names no individual stakeholders, so this table lists stakeholder roles only.

## Scope

**In scope:**
- Multi-agent task orchestration: task board, lifecycle management, planning, execution, review, merge, and PR automation
- Selectable and visually authored workflows, including workflow-defined columns and traits, built-in workflow graphs, and per-task workflow selection
- Multi-node and multi-surface coverage (Electron desktop, Capacitor mobile, web dashboard, CLI/TUI), plus project, node, and mesh management
- Model and provider-agnostic execution with credential, MCP server, and settings configuration, including user-defined custom providers
- Missions, goals, research runs, task evaluations, and agent companies as product layers that drive task work
- Plugin ecosystem with first-party runtime plugins (Claude, Droid, Grok, Cursor, Antigravity, OMP, ACP, Hermes, OpenClaw, Paperclip, agent browser) and first-party `pi` extensions (Claude CLI, Droid CLI, llama.cpp)
- Encrypted secrets store, usage and cost tracking, and external signal connectors (webhook, GitHub, GitLab, Sentry, Datadog, PagerDuty)
- Command Center operational monitoring for the agent fleet
- Scheduled automations and routines triggered by cron, webhooks, or manual runs, in global or project scope

**Out of scope:**
- Becoming bound to any single model, vendor, or interface (neutrality is a hard constraint)
- Publishing the private `@fusion/*` packages separately (they ship bundled with the CLI)
- Pluggable multi-user identity and role system (planned in `ROADMAP.md`, not yet shipped)
- Full event-driven re-architecture and the dashboard websocket migration (planned in `ROADMAP.md`, not yet shipped)

## Key Constraints

- Two npm packages are published: `@runfusion/fusion` and the `runfusion.ai` alias. Every `@fusion/*` package is private and bundled into the CLI
- Cross-`@fusion/*` imports must be statically analyzable (no dynamic `import("@fusion/engine")`); `@fusion/core` uses DI (`setCreateFnAgent`) instead to avoid circularity
- `task.status === "needs-replan"` is a durable graph replan signal, not unmigrated legacy; its writer must not be "cleaned up"
- Runtime storage is PostgreSQL by default; legacy SQLite files are one-time migration inputs only
- The merge gate is intentionally thin (Lint, Typecheck, Build, Gate); everything else runs non-blocking in `full-suite.yml`
- Port 4040 is reserved; never kill processes on it or start test servers on it
- No unbounded recursive scans rooted at the OS temp directory
- Releasing is an operator-only human action, never run inside a Fusion task
- Flaky tests are quarantined on sight (never appeased with widened timeouts or retries)
- Dashboard API routes register through domain registrars; `createApiRoutes` is orchestrator-only and registrar mount order is a tested contract
- New engine and core run-audit emitters must use the bounded `emitBoundedRunAudit` seam so telemetry can never delay a lifecycle transition
- Node.js 22.19.0 or later is required to run Fusion
