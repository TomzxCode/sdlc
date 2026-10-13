# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Turn a rough idea into merged production code | Solo developer | The developer describes the desired outcome in plain language and Fusion plans, builds, reviews, and ships it through the task lifecycle in an isolated git worktree behind a human approval gate. |
| UC-2 | Drive many coding-agent sessions across machines without losing track | Solo developer | The developer runs tasks across laptop, server, and cloud nodes and follows every session from one board with a single task store and lifecycle. |
| UC-3 | Control the same board from any surface | Solo developer | The developer monitors and steers identical board state from the dashboard, desktop app, mobile shell, or terminal CLI/TUI. |
| UC-4 | Ship code with a chosen level of automation and oversight | Operator / power user | The operator selects and authors workflow graphs, agent presets, and approval gates so routine work merges automatically while risky work waits for human review. |
| UC-5 | Organize related work toward a larger outcome | Operator / power user | The operator groups tasks under missions, goals, and research runs, and uses evals to check agent output quality before scaling up. |
| UC-6 | Operate the agent fleet with confidence | Operator / power user | The operator watches fleet health, usage and cost, and external signals in Command Center monitoring, including diagnostics and recovery for stalled work. |
| UC-7 | Extend the factory with custom capabilities | Plugin / extension author | The author adds dashboard UI, engine behavior, and agent runtimes through the plugin SDK and first-party `pi` extensions. |
| UC-8 | Keep the monorepo consistent, tested, and releasable | Maintainer / contributor | The maintainer evolves the bundled private packages behind the single published CLI package under a thin merge gate with non-blocking full-suite signal. |

## Wanted

_No wanted goals recorded yet: every actor goal above is served by the current build, and future gaps should be added here with their issue, feature, or roadmap signal._

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|

## Out of scope

- Becoming bound to any single model, vendor, or interface (neutrality is a hard constraint).
- Splitting the private `@fusion/*` packages into separate published packages (they ship bundled with the CLI).
- Pluggable multi-user identity and role system (roadmap, not yet shipped).
- A full event-sourced re-architecture and dashboard websocket migration (roadmap, not yet shipped).
