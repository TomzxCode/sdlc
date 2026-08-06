# Project Overview

## Purpose

Fusion is a software factory: a model- and surface-agnostic multi-agent orchestrator that converts a rough idea into planned, built, reviewed, and merged code. It is an AI-orchestrated task board that drives tasks through a workflow graph (planning → todo → in-progress → in-review → done), with AI agents that plan, implement, review, and ship work in isolated git worktrees behind a human approval gate. It is neutral by design across models, workflows, and surfaces: the same board is controllable from a desktop dashboard, a web UI, a mobile shell, and a terminal CLI, and it runs across many machines (nodes) in a fleet. Only the `@runfusion/fusion` package is published; it is the CLI plus a `pi` extension. The `@fusion/core`, `@fusion/dashboard`, and `@fusion/engine` packages are private and bundled into it.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Solo developers | Primary user | Drives many coding-agent sessions across machines and surfaces without losing track; ships code through Fusion |
| Operator / power user | Board and workflow owner | Defines selectable workflows, agent presets, approval gates, and monitors in-flight work |
| Plugin / extension author | Third-party developer | Extends the dashboard and engine through the plugin SDK and `pi` extensions |
| Maintainer / contributor | Internal team | Keeps the multi-package monorepo consistent, tested, and releasable |

## Scope

**In scope:**
- Multi-agent task orchestration: task board, lifecycle management, planning, execution, review, merge, and PR automation
- Selectable and visually authored workflows (graph of planning/code/review/gate/merge nodes)
- Multi-node and multi-surface coverage (dashboard, desktop, mobile, CLI/TUI), project/node/mesh management
- Model/provider-agnostic execution with credential, MCP, and settings configuration
- Missions, goals, research runs, and evals as product-hierarchy layers that drive task work
- Plugin ecosystem and first-party pi extensions (Claude CLI, Droid CLI, Llama.cpp)
- Encrypted secrets store, usage/cost tracking, and external signal connectors
- Command Center operational monitoring for the agent fleet

**Out of scope:**
- Becoming bound to any single model, vendor, or interface (neutrality is a hard constraint)
- Migration of the private `@fusion/*` packages into separate published packages (they ship bundled with the CLI)
- Pluggable multi-user identity and role system (roadmap, not yet shipped)
- A full event-sourced re-architecture and dashboard websocket migration (roadmap, not yet shipped)

## Key Constraints

- Only `@runfusion/fusion` is published; `@fusion/core`, `@fusion/dashboard`, and `@fusion/engine` are bundled private packages
- Cross-`@fusion/*` imports must be statically analyzable (no dynamic `import("@fusion/engine")`); `@fusion/core` uses DI (`setCreateFnAgent`) instead to avoid circularity
- `task.status === "needs-replan"` is a durable graph replan signal, not unmigrated legacy; its writer must not be "cleaned up"
- The merge gate is intentionally thin (Lint, Typecheck, Build, Gate); everything else runs non-blocking in `full-suite.yml`
- Port 4040 is reserved; never kill processes on it or start test servers on it
- No unbounded recursive scans rooted at the OS temp directory
- Releasing is an operator-only human action, never run inside a Fusion task
- Flaky tests are quarantined on sight (never appeased with widened timeouts or retries)