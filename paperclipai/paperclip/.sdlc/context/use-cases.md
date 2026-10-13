# Use cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Run a company of AI agents with task ownership and cost control | Board operator | Paperclip provides the org chart, ticketing, budgets, governance, and agent coordination behind one dashboard (`README.md:37`). |
| UC-2 | Operate multiple isolated organizations from one deployment | Board operator | A single deployment hosts many companies with company-scoped data and access checks (`README.md:138`). |
| UC-3 | Execute assigned tasks and report results | Agent employees | Agents wake via heartbeats for assigned work, run it through their adapter, and produce logs, usage records, and session state (`README.md:277`). |
| UC-4 | Delegate work down the org tree under approval gates | CEO agent | The CEO agent proposes strategy and delegates down the hierarchy, with board approval required before executing (`.sdlc/context/project-overview.md:15`). |
| UC-5 | Keep agent spend within budgets with automatic pauses | Board operator | Scoped budget policies with warning thresholds and hard stops pause work when limits are reached (`README.md:296`). |
| UC-6 | Gate risky work behind human approval | Board operator | Approval workflows, review stages, and connection action approvals govern hires, strategy, task completion, and tool calls (`README.md:289`). |
| UC-7 | Automate recurring work on schedules and triggers | Board operator | Routines with cron, webhook, and API triggers create tracked, owned issues without manual kick-offs (`README.md:301`). |
| UC-8 | Give agents governed access to third-party apps and tools | Board operator | Connections, the MCP tool gateway, and per-agent access policies expose external services as Allowed, Ask first, or Off (`README.md:162`). |
| UC-9 | Self-host the control plane locally without an account | Self-hoster | The open-source quickstart runs a local instance with an embedded database and no Paperclip account required (`README.md:348`). |
| UC-10 | Extend the platform without forking it | Contributors | The instance-wide plugin system adds workers, tools, job schedules, and UI contributions through a published SDK (`README.md:309`). |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|

(none identified — add with a linked signal)

## Out of scope

- Cloud-grade plugin marketplace/distribution beyond local/self-hosted plugin runtime.
- Revenue/expense accounting beyond model/token costs.
- Knowledge base subsystem.
- Public template marketplace (ClipHub).
- Multi-board governance or role-based human permission granularity.
- Full automatic self-healing orchestration beyond bounded run recovery (auto-reassign/retry planners).
- Project/issue-level privacy ACLs and scoped assignment-only object visibility (deferred to Pro/Enterprise).
- Realtime transport optimization (SSE/WebSockets).
