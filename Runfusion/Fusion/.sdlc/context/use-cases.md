# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Turn a rough idea into merged production code | Solo developer | The developer describes the desired outcome in plain language or imports it from an issue tracker, and Fusion plans, builds, reviews, and ships it through the task lifecycle in an isolated git worktree, landing it as a squash merge or as a pull request for human review. |
| UC-2 | Drive many coding-agent sessions across machines without losing track | Solo developer | The developer runs tasks across laptops, servers, and cloud nodes and across several registered projects, and follows every session from one dashboard backed by one shared database and one task lifecycle. |
| UC-3 | Control the same board from any surface | Solo developer | The developer monitors and steers identical board state from the dashboard, desktop app, mobile shell, or terminal CLI/TUI, including over a tokenized remote link when away from the machine. |
| UC-4 | Ship code with a chosen level of automation and oversight | Operator / power user | The operator selects and authors workflow graphs, agent presets, and approval gates so routine work merges automatically while risky work waits for human review, and can add gates such as browser verification before the merge. |
| UC-5 | Organize related work toward a larger outcome | Operator / power user | The operator groups tasks under missions, goals, and research runs, and uses evals to check agent output quality before scaling up. |
| UC-6 | Operate the agent fleet with confidence | Operator / power user | The operator watches fleet health, token usage and cost, incident signals, and system health in Command Center, and uses diagnostics and self-healing to recover stalled work. |
| UC-7 | Extend the factory with custom capabilities | Plugin / extension author | The author adds dashboard UI, engine behavior, and agent runtimes through the plugin SDK and first-party `pi` extensions. |
| UC-8 | Keep the monorepo consistent, tested, and releasable | Maintainer / contributor | The maintainer evolves the bundled private packages behind the single published CLI package under a thin merge gate with non-blocking full-suite signal. |
| UC-9 | Understand and steer running work by talking to agents | Solo developer | The developer asks an agent why a task failed or redirects it mid-flight in direct chat, task chat, chat rooms, and agent mail, with attachments, question cards, and resumable streams. |
| UC-10 | Put a team of agents to work without supervising each one | Operator / power user | The operator imports a prebuilt agent company or staffs durable agents with roles and heartbeats, and lets those agents delegate work to each other through the mailbox and mission autopilot. |
| UC-11 | Turn production alerts into tracked work | Operator / power user | The operator points signed GitHub, GitLab, Sentry, Datadog, PagerDuty, or webhook signals at Fusion, and every actionable alert becomes a triage task and an incident record. |
| UC-12 | Have recurring work run without being asked | Operator / power user | The operator schedules shell command automations and agent routines on a cron or webhook trigger in a global or per-project scope, and reads their run history. |
| UC-13 | Give agents durable knowledge of the codebase | Operator / power user | The operator builds the deterministic knowledge graph, keeps the memory backend capturing session shots and transcripts, and lets agent reflections update prompts as the fleet learns the codebase. |

## Wanted

_Goals the product does not serve yet go here, each with the issue, feature, or roadmap item that asks for them._

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| UC-14 | Bring work items in from a Beads tracker | Solo developer | Fusion imports issues from GitHub, GitLab, Jira, and Linear, but no Beads import path exists, so work already tracked there cannot become Fusion tasks. | ROADMAP.md planned work, "Import from Beads" |

## Out of scope

- Becoming bound to any single model, vendor, or interface (neutrality is a hard constraint).
- Splitting the private `@fusion/*` packages into separate published packages (they ship bundled with the CLI).
- Pluggable multi-user identity and role system (roadmap, not yet shipped).
- A full event-sourced re-architecture and dashboard websocket migration (roadmap, not yet shipped).
