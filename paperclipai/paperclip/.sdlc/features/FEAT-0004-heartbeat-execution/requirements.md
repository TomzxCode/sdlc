---
title: "Heartbeat Execution & Adapters"
status: draft
---

# Requirements: Heartbeat Execution & Adapters

## Overview

Agents do not run inside Paperclip; they are invoked via heartbeats that call an adapter. The scheduler wakes agents on their heartbeat schedule or on event triggers, the execution service resolves workspace/secrets/skills and invokes the adapter, and runs are tracked with status, context snapshots, events, and audit trails. Adapters cover process spawning, HTTP/webhook, local CLI sessions, the OpenClaw gateway, and external plugins.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | See run status, logs, costs; cancel runs; detect stuck/orphaned runs |
| Agent | Receive heartbeats, execute, report status and cost events |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall invoke agents on per-agent schedules (`enabled`, `intervalSec` >= 30, `maxConcurrentRuns` clamped 1..50). |
| FR-02 | Must | The scheduler shall skip invocation when the agent is paused/terminated, a run is active, or the hard budget limit is hit. |
| FR-03 | Must | The system shall track heartbeat runs with status `queued \| running \| succeeded \| failed \| cancelled \| timed_out` and invocation source `scheduler \| manual \| callback`. |
| FR-04 | Must | The process adapter shall spawn a child process, stream stdout/stderr to run logs, set status on exit/timeout, and cancel via SIGTERM then SIGKILL after a grace period. |
| FR-05 | Must | The HTTP adapter shall invoke via outbound request (2xx accepted, non-2xx failed) with optional async callback completion. |
| FR-06 | Should | The system shall support context delivery modes `thin` (IDs/pointers) and `fat` (assignments, goal summary, budget snapshot, recent comments). |
| FR-07 | Should | The system shall support built-in local CLI adapters (claude, codex, gemini, opencode, pi, cursor), the OpenClaw gateway, and external adapter plugins. |
| FR-08 | Should | The system shall detect and recover orphaned/stuck runs automatically. |
| FR-09 | May | The system shall support an optional cheap-model profile lane restricted to status-only recovery coordination. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Heartbeat invoke acknowledgement < 2 s for the process adapter. |
| NFR-02 | Should | Observability | Runs must produce structured logs, cost events, session state, and audit trails. |

## Constraints

- Separate queue infrastructure is not required for V1; a lightweight in-process scheduler/worker handles heartbeat triggers, stuck-run detection, and budget checks.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-02**
    - **Given** an agent at its hard budget limit
    - **When** its schedule fires
    - **Then** no new run is invoked and the skip is recorded
- [ ] **FR-04**
    - **Given** a running process-adapter run
    - **When** it is cancelled
    - **Then** SIGTERM is sent and SIGKILL follows after the grace period
- [ ] **NFR-01**
    - **Given** a process-adapter heartbeat
    - **When** invoked
    - **Then** acknowledgement returns within 2 s

## Conflicts

None identified yet.

## Open Questions

1. What are the exact stuck-run detection thresholds and orphan-recovery heuristics?
