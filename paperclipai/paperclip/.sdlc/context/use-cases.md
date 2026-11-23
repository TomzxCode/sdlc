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
| UC-11 | Create an organization and its first agent through guided onboarding | Board operator | The UI onboarding wizard creates a company and seeds its first agent (`ui/src/App.tsx`, `README.md:348`). |
| UC-12 | Clear work that waits on a person's decision | Board operator | The attention feed, decision queues, decision history, and experimental fast responses collect items that need input and let a person resolve them (`ui/src/pages/WhatNeedsMe.tsx`, `server/src/routes/attention.ts`). |
| UC-13 | Track durable cases and handoffs across tasks | Board operator | Cases group related tasks, documents, and attachments and keep a handoff trail for work that spans runs (`ui/src/pages/Cases.tsx`, `server/src/routes/cases.ts`). |
| UC-14 | Manage areas of responsibility and agent status reports | Board operator | Responsibilities group projects, tasks, and routines by owner, and agents write status reports that the owner can request (`ui/src/pages/Responsibilities.tsx`, `server/src/routes/responsibility-status-reports.ts`). |
| UC-15 | Publish a shared status board refreshed by agents | Board operator | Status cards show agent-written summaries on a company board with refresh and interest controls (`ui/src/pages/StatusCards`, `server/src/routes/status-cards.ts`). |
| UC-16 | Talk directly with an agent in the UI | Board operator | Agent Chat opens a conversation with an agent and can hand the work off to an assigned task (`ui/src/pages/AgentChat.tsx`, `README.md:337`). |
| UC-17 | Reuse and maintain shared skills from connected repositories | Board operator | Skill sources import skills from authorized GitHub repositories, preview packages, and refresh selected skills into the company catalog (`ui/src/pages/SkillSources.tsx`, `server/src/routes/company-skills.ts`). |
| UC-18 | Configure and safeguard a self-hosted instance | Self-hoster | Instance settings manage access, adapters, plugins, environments, experimental features, and database backup retention, while an admin endpoint reports server metrics (`ui/src/pages/InstanceGeneralSettings.tsx`, `server/src/routes/instance-server-metrics.ts`). |

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
