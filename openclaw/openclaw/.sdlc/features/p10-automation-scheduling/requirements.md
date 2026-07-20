---
title: "Automation and Scheduling"
status: done
---

# Requirements: Automation and Scheduling

## Overview

OpenClaw provides a cron-based job scheduling system, a webhook receiver for external triggers, a workflow/flow engine, and auto-reply capabilities. These allow the assistant to operate proactively, respond to external events, and run maintenance tasks on a schedule.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Schedule recurring agent tasks, receive automated responses, trigger workflows on external events |
| Maintainers | Reliable scheduling, failure handling, observability of automated jobs |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall support cron-based job scheduling with standard cron expressions |
| FR-2 | Must | The system shall persist scheduled jobs across gateway restarts |
| FR-3 | Must | The system shall support webhook receivers for external HTTP triggers |
| FR-4 | Must | The system shall provide a flow/workflow engine for multi-step automations |
| FR-5 | Should | The system shall support auto-reply rules for common message patterns |
| FR-6 | Must | Scheduled jobs shall execute as isolated agent sessions with configurable model and tools |
| FR-7 | Must | The system shall support failure notification and retry for failed scheduled jobs |
| FR-8 | Should | The system shall support heartbeat-style recurring jobs in addition to cron |
| FR-9 | Must | The system shall prevent duplicate timer scheduling for the same job |
| FR-10 | Should | The system shall expose job history and status for operator visibility |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Scheduled jobs must fire within 60 seconds of their scheduled time |
| NFR-2 | Must | Durability | Job definitions must survive gateway process restarts |

## Acceptance Criteria

- [ ] **FR-1**: A job scheduled with `0 9 * * *` runs at 9 AM daily
- [ ] **FR-3**: An HTTP POST to the webhook URL triggers an agent session
- [ ] **FR-6**: A cron job executes with the configured model and tool set, not the default session

## Open Questions

1. What is the maximum supported cron frequency (sub-minute intervals?)

