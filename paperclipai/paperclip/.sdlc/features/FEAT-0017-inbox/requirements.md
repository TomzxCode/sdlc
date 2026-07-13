---
title: "Inbox"
status: done
---

# Requirements: Inbox

## Overview

The inbox is a user-centric aggregated view of work items that need attention. It surfaces issues assigned to the user, recent activity, blocked items, unread items, and join request queues. Users can dismiss items from the inbox without affecting the underlying entities.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | See all work items requiring attention; filter by mine/recent/unread/blocked/all; manage join requests |
| Agent | Has an implicit inbox via its assigned issues |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The inbox shall display issues assigned to the current user, grouped by status. |
| FR-02 | Must | The inbox shall show unread issues and track read state per issue per user. |
| FR-03 | Must | The inbox shall surface blocked issues. |
| FR-04 | Must | The inbox shall surface pending join requests for the company. |
| FR-05 | Should | The inbox shall support dismissal of inbox items (local to the user, does not affect underlying issues). |
| FR-06 | Should | The inbox shall support filtering by view: mine, recent, unread, blocked, all. |
| FR-07 | Should | The inbox shall support archival of issues from the inbox view. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Inbox queries must load within p95 < 500 ms. |
| NFR-02 | Should | Usability | Inbox views should update when the underlying issue state changes. |

## Constraints

- Inbox is per-user and per-company; users in different companies see different inboxes.
- Dismissal and read state are per-user settings, not entity properties.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a user with assigned issues in various states
    - **When** the inbox loads with view=mine
    - **Then** only issues assigned to that user are shown
- [ ] **FR-02**
    - **Given** a user who has not read certain issues
    - **When** the inbox loads
    - **Then** unread issues are visually distinguished
- [ ] **NFR-01**
    - **Given** a user with 500+ issues in their scope
    - **When** the inbox is requested
    - **Then** response time is under 500 ms at p95

## Conflicts

None identified yet.

## Open Questions

1. Should the inbox include activity log entries, or is it purely issue-focused?
