---
title: "Activity Audit Log"
status: done
---

# Requirements: Activity Audit Log

## Overview

Every mutating action in Paperclip must be auditable. The activity log provides an immutable event stream recording actor, action, entity, and details for every mutation across all entities. It is the single source of truth for who did what, when, and on which resource. This feature covers the activity log backend, API, UI, and the conventions that ensure every mutation path writes an entry.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | View complete audit trail for all companies; filter by actor, entity, action, date range |
| Agent | See activity relevant to its own scope (own actions, actions on its issues) |
| Auditor / compliance | Verify that all mutations are recorded immutably and are tamper-evident |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | Every mutating API request must write an `activity_log` entry recording actor type (agent/user/system), actor id, action, entity type, entity id, and JSONB details. |
| FR-02 | Must | The system shall expose a paginated GET endpoint returning activity log entries scoped to a company. |
| FR-03 | Must | The system shall support filtering activity log entries by actor, entity type, action type, and date range. |
| FR-04 | Must | Activity entries must include a timestamp (`created_at`) and must be append-only (no updates, no deletes). |
| FR-05 | Should | The system shall expose an activity summary/dashboard widget showing recent events. |
| FR-06 | Should | Activity entries should include the IP address or origin context when available. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Activity log queries must complete within p95 < 500 ms even with 100k+ entries per company. |
| NFR-02 | Must | Auditability | Entries must never be modified or deleted; the table is append-only. |
| NFR-03 | Should | Storage | Activity log retention and pruning strategy must be documented; old entries may be archived. |

## Constraints

- The activity_log table is append-only; no UPDATE or DELETE operations are permitted.
- Cross-company visibility must be enforced: board sees all, agents see only their own company.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a mutating API action (e.g., create agent, update issue status, approve request)
    - **When** the action completes
    - **Then** an `activity_log` row exists with correct actor, action, entity, and details
- [ ] **FR-02**
    - **Given** a company with 100+ activity entries
    - **When** the board requests GET /activity?companyId=X
    - **Then** entries are returned paginated, scoped to that company, newest first
- [ ] **FR-04**
    - **Given** an existing activity entry
    - **When** an UPDATE or DELETE is attempted
    - **Then** the operation is rejected (table-level RLS or app-level enforcement)
- [ ] **NFR-01**
    - **Given** a company with 100k activity entries
    - **When** a filtered query is executed
    - **Then** response time is under 500 ms at p95

## Conflicts

None identified yet.

## Open Questions

1. What is the archive/retention policy for old activity entries?
2. Should activity entries include IP addresses or request metadata for security auditing?
