# Vocabulary

This file defines domain-specific terms, acronyms, and abbreviations used across the project. Keeping definitions here avoids ambiguity in requirements, specs, and discussions. Add new terms as they are introduced.

## Domain Terms

| Term | Definition |
|---|---|
| Task board | The kanban surface of planning/todo/in-progress/in-review/done (or graph-driven variants) that tracks AI-orchestrated work items |
| Workflow graph | A DAG of nodes (plan/code/review/gate/merge) a task traverses; replaces the fixed legacy lifecycle columns |
| Workflow node | A unit in the workflow graph (e.g. plan, code, review, gate, merge, exit-gate) with its own runner |
| Task lifecycle | The domain state machine modeling a task's progression and its status values |
| Planner overseer | Automated oversight of planning work across `off` / `observe` / `steer` / `autonomous` levels with human-confirmation gates |
| Planning mode | A dedicated human-in-the-loop planning chat and Plan Review node for shaping a task before execution |
| Durable agent | A persistent agent that runs on a heartbeat and can be auto-recovered from error states |
| Mission / milestone / feature | The product-hierarchy layers (mission → milestone → feature) that drive task work |
| Auto-merge | Automated promotion of finished branches into the default branch (squash/rebase/PR paths) |
| Command Center | The operator "mission control" dashboard for the agent fleet, signals, and usage |
| Signals connector | HMAC-signed external ingest (Sentry/Datadog/PagerDuty/webhooks) into Fusion |
| Run audit | Append-only structured event log of engine/task lifecycle events (ids/counts-outcomes metadata only) |
| Smart pull | Strategy-aware pull logic during merge conflict handling |
| Self-healing | Engine sweeps that reconcile stranded, orphaned, or stale task/agent/worktree state |

## Technical Terms

| Term | Definition |
|---|---|
| Worktree | An isolated git working tree used for branch-scoped task work, keeping the primary checkout on main |
| File-scope | The set of files a task is allowed/expected to touch; enforced on squash merges |
| Workflow graph executor | Engine component that drives the workflow graph through its node runners |
| Node runner | Per-node implementation (code-runner, gate-runner, merge-runner, exit-gate-runner, review) |
| Merger | Engine component that lands branches via squash/rebase/PR with conflict resolution and guards |
| Smart pull / auto-prerebase | Strategies to reconcile divergent branches before merge |
| Task store / task-advisory lock | The domain persistence layer and per-task advisory locking used for lifecycle moves |
| Triple-proof liveness | The canonical proof that a task/session is contended before backward moves |
| Sandbox | Pluggable executor command isolation (bubblewrap, spawn-based) |
| pi extension | A first-party carrier that routes Fusion's agent commands into a specific coding-agent CLI |
| Mesh | Distributed coordination across multiple Fusion nodes sharing a PostgreSQL backend |
| Legislature: artifact | A produced SDLC artifact instance (requirements, specification, tests, etc.) under `.sdlc/` |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ACP | Agent Client Protocol |
| CLI | Command-line interface |
| FEAT | Feature identifier in SDLC artifacts (`FEAT-N`) |
| FN-XXXX | Fusion task/issue tracker identifier |
| FR / NFR | Functional / non-functional requirement |
| HMAC | Hash-based message authentication code |
| L10n / i18n | Localization / internationalization |
| MCP | Model Context Protocol |
| PR | Pull request |
| SDLC | Software development lifecycle |
| SLA / SLO / SLI | Service-level agreement / objective / indicator |
| TUI | Terminal user interface |
| UI | User interface |