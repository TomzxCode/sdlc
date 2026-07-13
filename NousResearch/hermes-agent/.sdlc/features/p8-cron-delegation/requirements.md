---
title: "Cron Scheduling and Subagent Delegation"
status: done
---

# Requirements: Cron Scheduling and Subagent Delegation

## Overview

Hermes provides two systems for work that extends beyond a single conversation turn: a cron scheduler for recurring and one-shot jobs, and a subagent delegation system for spawning isolated child agents. The cron system supports multiple schedule formats, per-job skill/model overrides, chaining, and multi-platform delivery. Delegation supports both single-task and batch (parallel) execution with configurable concurrency.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Want scheduled reports, reminders, and automated workflows delivered to their messaging platform |
| Operators | Need parallel task execution to speed up complex operations |
| Developers | Want to integrate cron jobs into their workflows |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The cron system shall support duration-based schedules (30m, 2h, 1d) |
| FR-2 | Must | The cron system shall support cron expressions (0 9 * * *) |
| FR-3 | Must | The cron system shall support every-phrase schedules (every 2h, every monday 9am) |
| FR-4 | Must | The cron system shall support ISO timestamp one-shot jobs |
| FR-5 | Must | The cron system shall support per-job skill loading, model/provider overrides, and workdir |
| FR-6 | Must | The cron system shall support multi-platform delivery of results |
| FR-7 | Must | The delegation system shall support spawning subagents with isolated context and terminal |
| FR-8 | Must | The delegation system shall support both blocking (wait for summary) and background (fire and forget) modes |
| FR-9 | Must | The delegation system shall support concurrent batch execution |
| FR-10 | Should | The delegation system shall support role levels (leaf and orchestrator) |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Cron jobs shall have a 3-minute hard interrupt to prevent runaway sessions |
| NFR-2 | Must | Safety | File lock prevents duplicate cron ticks across processes |
| NFR-3 | Should | Performance | Delegation concurrency shall be capped (default 3) by max_concurrent_children |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a cron job with schedule "30m"
    - **When** 30 minutes pass
    - **Then** the job fires and executes its prompt
- [ ] **FR-7**
    - **Given** a user asks to delegate a task
    - **When** the agent calls delegate_task
    - **Then** a subagent is spawned with an isolated session and terminal
- [ ] **FR-9**
    - **Given** a batch of 5 tasks with max_concurrent_children=3
    - **When** the agent calls delegate_task with tasks=[5 items]
    - **Then** 3 tasks run concurrently, then the remaining 2

## Conflicts

None identified yet.

## Open Questions

1. Should cron jobs support retry policies or only the current one-shot + scheduled patterns?