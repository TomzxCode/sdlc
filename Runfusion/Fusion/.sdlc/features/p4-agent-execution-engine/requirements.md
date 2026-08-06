---
title: "Agent Execution Engine"
status: done
---

# Requirements: Agent Execution Engine

## Overview

The execution engine is the multi-agent runtime: the scheduler and triage pull eligible tasks into execution, the executor claims and drives permission-bounded agent sessions, durable agents run on heartbeats and auto-recover from error states, and permission policies and sandboxes constrain what agents can do.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Manages agents, presets, permissions, and watches runs |
| Agent | Executes tasks under a bounded permission policy |
| Enterprise/security | Enforces permission policy and command sandboxing |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall triage eligible tasks and schedule them into execution respecting capacity and dependencies |
| FR-2 | Must | The executor shall create and drive permission-bounded agent sessions for claimed tasks |
| FR-3 | Must | Durable agents shall run on heartbeats and auto-recover from recoverable error states up to a bounded budget |
| FR-4 | Must | The system shall enforce agent permission policies and presets |
| FR-5 | Must | The system shall isolate executor commands via pluggable sandbox backends |
| FR-6 | Should | The system shall expose agent management (list, detail, new, permission editing) in the dashboard |
| FR-7 | Should | The system shall record run-audit events for task lifetime and agent actions with ids/counts/outcomes-only metadata |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Heartbeats and self-healing shall not move user-paused or operator-actionable-parked agents backward |
| NFR-2 | Must | Security | Sandbox boundaries must be applied before executing user-provided commands |
| NFR-3 | Must | Maintainability | Executor must not use `execSync` for user-configured commands |

## Constraints

- `task.status === "needs-review"` / `needs-replan` are graph signals, not legacy; their writers must remain
- Task-review and executor mechanics live in the engine; the dashboard only reads via the domain API
- Modal review of execution is owned by workflow nodes; not reintroduce a second authority

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** eligible tasks
    - **When** triage/scheduler run
    - **Then** tasks are claimed and scheduled within capacity, respecting dependencies
- [ ] **FR-2**
    - **Given** a claimed task
    - **When** the executor runs
    - **Then** a permission-bounded agent session is created and driven to completion
- [ ] **FR-3**
    - **Given** a durable agent in a recoverable error state
    - **When** the heartbeat timer or self-healing sweep runs
    - **Then** it clears the error and retries up to the shared budget, or parks on exhaustion
- [ ] **FR-4**
    - **Given** a restricted action
    - **When** the agent attempts it
    - **Then** permission policy blocks or prompts per the policy
- [ ] **FR-5**
    - **Given** a user-configured command
    - **When** executed
    - **Then** it runs under the configured sandbox backend
- [ ] **NFR-2**
    - **Given** a sandboxed command
    - **When** execution begins
    - **Then** the sandbox boundary is enforced

## Conflicts

None identified yet.

## Open Questions

1. The precise capacity/claim accounting across solver lanes is under `.docs/agents.md` and settings reference.