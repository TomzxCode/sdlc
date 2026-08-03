---
title: "Kanban Multi-Agent Work Queue"
status: done
---

# Requirements: Kanban Multi-Agent Work Queue

## Overview

Kanban is a durable, SQLite-backed multi-agent work queue that lets multiple Hermes profiles and workers collaborate on shared tasks. It provides a CLI (`hermes kanban <verb>`), a dedicated worker/orchestrator toolset (`kanban_*` tools) with zero schema footprint when idle, and a long-lived dispatcher that reclaims stale claims, promotes ready tasks, atomically claims them, and spawns assigned profiles. The dispatcher runs inside the gateway by default with a standalone daemon option. Boards are the hard isolation boundary; tenants are a soft namespace within a board.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operators / multi-profile users | Coordinate multiple Hermes profiles on shared tasks with a persistent board they can inspect and drive from the CLI or dashboard |
| Orchestrator agents | Create and assign tasks via `kanban_create`, chain work through dependency links, and track progress |
| Worker agents | Claim, work, heartbeat, comment on, and complete tasks without seeing other boards |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a `hermes kanban` CLI with board, task, run, and board lifecycle verbs |
| FR-2 | Must | The system shall persist boards and tasks in a SQLite database keyed by board directory |
| FR-3 | Must | The system shall support board creation, listing, switching, renaming, archiving (recoverable), and hard deletion |
| FR-4 | Must | The system shall support task creation (including idempotent dedup keys), listing, showing with comments/events, editing, assigning, blocking, unblocking, completing, and archiving |
| FR-5 | Must | The system shall support dependency links (parent->child) and task links/unlinks |
| FR-6 | Must | The system shall support file attachments and attachment listing/removal |
| FR-7 | Must | The system shall support task comments with a durable event log |
| FR-8 | Must | The system shall expose a `kanban_*` toolset for worker/orchestrator agents (show, complete, block, heartbeat, comment, create, link, attach, attachments) |
| FR-9 | Must | The dispatcher shall reclaim stale claims, promote ready tasks, atomically claim tasks, and spawn assigned profiles |
| FR-10 | Must | The dispatcher shall run inside the gateway by default (`kanban.dispatch_in_gateway: true`) with a standalone `hermes kanban daemon` option |
| FR-11 | Must | Workers shall be isolated per board via a pinned `HERMES_KANBAN_BOARD` environment variable |
| FR-12 | Should | The system shall auto-block a task after a configurable consecutive failure limit to prevent spin loops |
| FR-13 | Should | The system shall support tenant namespaces within a board (workspace-path + memory-key isolation) |
| FR-14 | Should | The system shall provide a web dashboard plugin for visualizing boards and a systemd unit for standalone deployment |
| FR-15 | Should | The system shall support a swarm-style multi-agent pattern with dedicated worker, verifier, and synthesizer profiles |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Isolation | Worker agents must not see or modify boards other than the one pinned in their environment |
| NFR-2 | Must | Durability | Task state, comments, attachments, and run history shall survive process restarts (SQLite-backed) |
| NFR-3 | Must | Concurrency | Atomic claims shall prevent two workers from claiming the same task simultaneously |
| NFR-4 | Should | Availability | The dispatcher shall reclaim stale claims (default 60s tick) so abandoned work is not lost forever |

## Constraints

- Board is the hard boundary: workers are spawned with `HERMES_KANBAN_BOARD` pinned in their env
- Tenant is a soft namespace within a board
- After `kanban.failure_limit` consecutive non-success attempts (default 2), the dispatcher auto-blocks the task
- The `kanban` toolset is only enabled for dispatcher-spawned workers unless the profile explicitly enables it

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the Hermes CLI
    - **When** the user runs `hermes kanban --help`
    - **Then** board, task, run, and lifecycle verbs are listed
- [ ] **FR-4**
    - **Given** an empty board
    - **When** the user creates a task with a dedup key and creates it again with the same key
    - **Then** the second call returns the existing task id instead of duplicating
- [ ] **FR-9**
    - **Given** a ready task assigned to a profile and a running dispatcher
    - **When** the dispatch tick fires
    - **Then** the task is atomically claimed and the assigned profile is spawned
- [ ] **FR-11**
    - **Given** a worker spawned for board A
    - **When** the worker lists boards
    - **Then** only board A is visible
- [ ] **FR-12**
    - **Given** a task that fails more than the failure limit times
    - **When** the dispatcher processes it
    - **Then** the task is auto-blocked to prevent a spin loop

## Conflicts

None identified yet.

## Open Questions

1. Should the dispatcher support remote/standalone boards across machines, or is a single gateway host the supported topology?
2. Should tenant isolation extend to per-tenant attachment storage?
