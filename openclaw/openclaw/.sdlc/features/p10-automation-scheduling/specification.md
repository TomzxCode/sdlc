---
title: "Automation and Scheduling"
status: done
---

# Specification: Automation and Scheduling

## Architecture

Cron scheduling (`src/cron/`) provides timer-based job triggering with persistent state in SQLite. Webhooks (`extensions/webhooks/`) provide HTTP-triggered agent sessions. Flows (`src/flows/`) implement multi-step automation scripts typically used for doctor checks and setup.

```
Cron Service ───→ SQLite Store ───→ Isolated Agent Sessions
(src/cron/)         (cron jobs,         (per-job config:
                    schedules)           model, tools, sandbox)

Webhook Receiver ───→ Agent Session
(extensions/webhooks/)  (HTTP body as context)

Flow Engine ───→ Health Checks / Doctor / Setup
(src/flows/)
```

## Data Models

### CronJob

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Unique job identifier |
| schedule | string | not null | Cron expression |
| model | string | optional | Model override for job execution |
| tools | string[] | optional | Tool allowlist for job |
| enabled | boolean | not null | Whether the job is active |
| last_run | timestamp | nullable | Last execution timestamp |

### WebhookConfig

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Webhook identifier |
| path | string | not null, unique | URL path segment |
| agent_id | string | not null | Target agent for the session |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Job persistence | SQLite via Kysely | Consistent with project-wide storage convention |
| Isolated sessions | Per-job agent session with configurable model/tools | Prevents cron jobs from interfering with user sessions |
| Webhook plugin | Extension (extensions/webhooks/) | Follows plugin architecture for optional functionality |

## Risks and Unknowns

1. Cron precision may drift under heavy system load
2. Webhook endpoint security requires careful configuration

