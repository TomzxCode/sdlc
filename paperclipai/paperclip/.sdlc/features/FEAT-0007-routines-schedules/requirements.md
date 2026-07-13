---
title: "Routines & Schedules"
status: done
---

# Requirements: Routines & Schedules

## Overview

Routines are recurring task definitions that fire on cron, webhook, or API triggers. Each routine execution creates a tracked issue and wakes the assigned agent, so regular work (customer support, reports, social) happens without manual kick-offs. Routines carry concurrency and catch-up policies, secret-aware env overlays, and revision history.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Configure recurring jobs, triggers, and concurrency policy |
| Agent | Wake on routine execution and work the generated issue |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support routines with cron, webhook, and API triggers. |
| FR-02 | Must | Each routine execution shall create a tracked issue and wake the assigned agent. |
| FR-03 | Must | The system shall support concurrency and catch-up policies per routine. |
| FR-04 | Should | The system shall support routine revisions and snapshotted routine env (secret-aware binding format). |
| FR-05 | Should | The routine env overlay shall apply after project env and before Paperclip runtime-owned keys, resolving secret refs against the routine binding target. |
| FR-06 | Should | The system shall track routine runs. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Should | Reliability | Missed routine executions follow the configured catch-up policy. |
| NFR-02 | Should | Auditability | Routine executions are visible as issues and runs. |

## Constraints

- Routine-owned secrets do not require direct bindings on the executing agent (resolved against the routine binding target).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-02**
    - **Given** a cron-triggered routine
    - **When** the schedule fires
    - **Then** a tracked issue is created and the assigned agent is woken

## Conflicts

None identified yet.

## Open Questions

1. What are the exact concurrency and catch-up semantics when executions overlap?
