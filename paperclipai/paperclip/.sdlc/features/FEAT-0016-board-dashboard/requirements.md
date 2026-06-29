---
title: "Board Dashboard"
status: draft
---

# Requirements: Board Dashboard

## Overview

The board dashboard is the primary landing page for human operators. It provides an at-a-glance overview of company health: agent status counts, issue state counts, month-to-date spend and budget utilization, and pending approval counts. It is the first thing a board operator sees when logging in and should surface actionable information immediately.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | See company status at a glance; identify stalled agents, blocked issues, budget overruns, and pending approvals |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The dashboard shall display agent status counts (active, running, paused, error, terminated) for the selected company. |
| FR-02 | Must | The dashboard shall display issue state counts (open, in_progress, in_review, done, blocked, cancelled) for the selected company. |
| FR-03 | Must | The dashboard shall display month-to-date spend and budget utilization percentage for the selected company. |
| FR-04 | Must | The dashboard shall display pending approval counts. |
| FR-05 | Should | The dashboard shall display recent activity entries. |
| FR-06 | Should | The dashboard shall display agent and issue counts visible from the org tree. |
| FR-07 | Should | The dashboard shall update periodically or support refresh. |
| FR-08 | May | The dashboard shall support a full-screen wallboard/live view mode for display monitors. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Dashboard load must complete within p95 < 500 ms. |
| NFR-02 | Should | Availability | Dashboard should gracefully handle temporary unavailability of any data source (e.g. budget service down). |

## Constraints

- Dashboard is read-only; no mutations are performed from dashboard endpoints.
- Data is aggregated at read time; no materialized views required for V1.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a company with agents in various states
    - **When** the dashboard loads
    - **Then** counts for each agent status are displayed correctly
- [ ] **FR-03**
    - **Given** a company with recorded cost events
    - **When** the dashboard loads
    - **Then** month-to-date spend and budget utilization are shown
- [ ] **NFR-01**
    - **Given** a company with 1k+ tasks and 50+ agents
    - **When** the dashboard is requested
    - **Then** response time is under 500 ms at p95

## Conflicts

None identified yet.

## Open Questions

1. Should the dashboard include goal hierarchy progress or is that a separate view?
