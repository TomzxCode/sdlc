---
title: "Command Center & Operational Monitoring"
status: done
---

# Requirements: Command Center & Operational Monitoring

## Overview

The Command Center is the operator "mission control" surface for the agent fleet: fleet health, usage and cost per task, system diagnostics, and external signal connectors (Sentry/Datadog/PagerDuty/generic webhooks) that flow into the board and command surfaces.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Monitors fleet health, usage/cost, and signals in one place |
| Cost/ops | Tracks token usage and per-task cost |
| External systems | Sends HMAC-signed signal events into Fusion |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a Command Center view with fleet and health surfaces |
| FR-2 | Must | The system shall track usage and cost per task (token usage, cost tabs, usage indicator) |
| FR-3 | Must | The system shall receive HMAC-signed external signal connectors (Sentry/Datadog/PagerDuty/webhooks) and map payloads |
| FR-4 | Must | The system shall expose diagnostics and monitor routes for system health |
| FR-5 | Should | The system shall stream realtime status via the shared `/api/events` SSE bus |
| FR-6 | Should | The system shall expose usage/signals/monitor data through dashboard API route registrars |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Signal connectors must verify HMAC signatures before accepting payloads |
| NFR-2 | Must | Performance | Monitoring/usage reads must not degrade dashboard interactive latency |
| NFR-3 | Should | Availability | Health surfaces must degrade gracefully when a node is unreachable |

## Constraints

- Port 4040 is reserved; monitoring tools must not bind it
- Usage/cost data is read-only outside the engine's accounting writer

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** an operator
    - **When** the Command Center is opened
    - **Then** fleet/health surfaces render from monitor data
- [ ] **FR-2**
    - **Given** executed tasks
    - **When** the usage view is opened
    - **Then** per-task cost and usage are shown
- [ ] **FR-3**
    - **Given** an HMAC-signed signal payload
    - **When** a signal connector receives it
    - **Then** it is verified and mapped into the board/command surface
- [ ] **NFR-1**
    - **Given** an unsigned signal payload
    - **When** a signal connector receives it
    - **Then** it is rejected

## Conflicts

None identified yet.

## Open Questions

1. Which usage metrics are authoritative for cost accounting (token counts vs. provider billing)?