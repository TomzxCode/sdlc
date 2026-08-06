---
title: "Task Board & Task Lifecycle Management"
status: done
---

# Requirements: Task Board & Task Lifecycle Management

## Overview

The task board is Fusion's core Kanban surface. It lets operators create tasks (free text, import, GitHub), track them through a workflow-driven lifecycle (planning/todo/in-progress/in-review/done), attach prompt specs, comments, and artifacts, declare dependencies and subtasks, and move or delete them with guard rails. Every piece of work in Fusion, including missions and research, eventually resolves to tasks on this board.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Creates and tracks tasks, reads prompt specs, adds comments/artifacts, manages dependencies |
| Agent executor | Consumes task state (spec, file scope, branch context) when driving implementation |
| Dashboard/CLI users | Same board and lifecycle surfaced on every device |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let users create tasks via quick entry, a new-task modal, import, GitHub issues, and mission/research flows |
| FR-2 | Must | The system shall render tasks on a board (column-based) and a list view, with search and filtering |
| FR-3 | Must | The system shall persist a task's prompt/spec document, comments, artifacts, dependencies, subtasks, branch context, and file scope |
| FR-4 | Must | The system shall enforce lifecycle move rules and guards (column eligibility, dependencies, user pause semantics) |
| FR-5 | Must | The system shall let users move tasks between columns and move the board itself (board-level moves) |
| FR-6 | Must | The system shall support archiving and soft-delete with verification, keeping tombstones for audit |
| FR-7 | Should | The system shall expose task operations through the dashboard API, CLI, and workflow routes |
| FR-8 | Should | The system shall render board columns in a resolved order with degraded-mode flags for unsupported columns |
| FR-9 | Should | The system shall group tasks (GroupTask) and break work into subtasks with their own lifecycle |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Concurrency | Task lifecycle mutations shall use per-task advisory locks to prevent conflicting concurrent moves |
| NFR-2 | Must | Reliability | Soft-deleted tasks shall never be resurrected by lifecycle or self-healing sweeps |
| NFR-3 | Should | Usability | The board shall work on desktop and mobile breakpoints |
| NFR-4 | Should | Performance | Task search and list reads shall complete without full-table scans in normal use |

## Constraints

- Task store lives in `@fusion/core`; dashboard and CLI must not walk the raw DB directly
- Port 4040 is reserved and must not be used by tests or tooling
- Backward moves (e.g. in-review → todo) require liveness proof before mutation

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** an operator with the dashboard or CLI open
    - **When** they create a task via quick entry, the modal, import, or GitHub
    - **Then** the task appears on the board with a prompt spec and correct column
- [ ] **FR-2**
    - **Given** tasks exist in the store
    - **When** the board or list view is opened
    - **Then** tasks render in resolved column order with search/filtering available
- [ ] **FR-3**
    - **Given** a task with comments, artifacts, dependencies, and subtasks
    - **When** the task detail is opened
    - **Then** all attached data persists and renders correctly
- [ ] **FR-4**
    - **Given** a task in a non-target column
    - **When** an invalid move is attempted
    - **Then** the move is rejected with a guard/error and the task column is unchanged
- [ ] **FR-6**
    - **Given** a task to remove
    - **When** the operator archives/deletes it
    - **Then** it becomes tombstoned and is never resurrected by sweeps
- [ ] **NFR-1**
    - **Given** two concurrent lifecycle mutations on the same task
    - **When** both are submitted
    - **Then** exactly one wins and the loser is rejected, with no torn state

## Conflicts

None identified yet.

## Open Questions

1. How are board-level (multiple-task) moves reconciled with per-task workflow selection?
