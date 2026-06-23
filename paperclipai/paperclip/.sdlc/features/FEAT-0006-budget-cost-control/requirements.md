---
title: "Budget & Cost Control"
status: draft
---

# Requirements: Budget & Cost Control

## Overview

Paperclip tracks token and cost usage and enforces budgets to prevent runaway spend. Cost events are ingested per agent/issue/project/goal/provider/model, rolled up across dimensions, and checked against monthly UTC budgets. At the hard limit (100%) the agent is auto-paused and new invocations/checkout are blocked; a soft alert fires at 80%. The board can override by raising budgets or explicitly resuming.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Set company/agent budgets; monitor spend; override hard stops |
| Agent | Report cost events for its own runs |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall ingest cost events (agent, issue, provider, model, input/output tokens, cost cents, occurred_at) with ownership checks. |
| FR-02 | Must | The system shall validate non-negative token counts and `costCents >= 0`. |
| FR-03 | Must | The system shall support company and agent monthly budgets and optional project budgets. |
| FR-04 | Must | At the hard limit (100%), the system shall set agent status to `paused`, block new checkout/invocation, and emit a high-priority activity event. |
| FR-05 | Must | The system shall roll up spend by company, agent, project, goal, and issue (read-time aggregation acceptable for V1). |
| FR-06 | Should | The system shall surface a soft alert at the 80% threshold. |
| FR-07 | Should | The board shall be able to override a hard stop by raising the budget or explicitly resuming the agent. |
| FR-08 | Should | The system shall expose a dashboard payload with month-to-date spend and budget utilization. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Correctness | Rollups are aggregations of cost events and are never manually edited. |
| NFR-02 | Should | Performance | Cost summary queries should stay within latency targets; materialized rollups deferred. |

## Constraints

- Budget period is a monthly UTC calendar window.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-04**
    - **Given** an agent that reaches 100% of its monthly budget
    - **When** spend crosses the limit
    - **Then** the agent is paused, new invocations are blocked, and a high-priority activity event is emitted
- [ ] **FR-04 (cont.)**
    - **Given** a budget-paused agent
    - **When** a checkout is attempted
    - **Then** it is rejected
- [ ] **NFR-01**
    - **Given** the cost rollup queries
    - **When** inspected
    - **Then** they are pure aggregations of `cost_events` with no manual overrides

## Conflicts

None identified yet.

## Open Questions

1. Should materialized rollups be added if read latency exceeds targets at scale?
