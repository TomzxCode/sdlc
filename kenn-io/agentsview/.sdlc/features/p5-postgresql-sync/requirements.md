---
title: "PostgreSQL Sync"
status: done
---

# Requirements: PostgreSQL Sync

## Overview

The PostgreSQL sync feature pushes session data from the local SQLite archive to a shared PostgreSQL instance, enabling team-wide dashboards and read-only queries. It supports incremental push with fingerprint-based change detection, named targets for multiple PG instances, and read-only serving of the web UI from PostgreSQL.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Engineering manager | Team-wide visibility into agent usage |
| Team member | Access session data from PostgreSQL-connected tools |
| Operator | Configure multiple PG targets (work, archive) |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall push session data from SQLite to PostgreSQL incrementally |
| FR-2 | Must | The system shall support project filtering (include/exclude projects) |
| FR-3 | Must | The system shall use fingerprint-based change detection for incremental pushes |
| FR-4 | Must | The system shall support named PostgreSQL targets (multiple destinations) |
| FR-5 | Must | The system shall serve the web UI read-only from PostgreSQL |
| FR-6 | Must | The system shall support conflict detection based on owning machine |
| FR-7 | Should | The system shall provide a watch mode that auto-pushes on session changes |
| FR-8 | Should | The system shall support OS service management (systemd/launchd) for auto-push |
| FR-9 | Should | The system shall support pricing sync from SQLite to PostgreSQL |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Consistency | Push must be idempotent; re-running produces the same state |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** local SQLite has session data
    - **When** `agentsview pg push` is run
    - **Then** session data is replicated to PostgreSQL
- [ ] **FR-7**
    - **Given** the watch daemon is running
    - **When** new sessions are synced locally
    - **Then** they are automatically pushed to PostgreSQL

## Open Questions

None.
