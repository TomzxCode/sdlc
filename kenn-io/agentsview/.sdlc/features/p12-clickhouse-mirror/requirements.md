---
title: "ClickHouse Mirror"
status: done
---

# Requirements: ClickHouse Mirror

## Overview

The ClickHouse mirror pushes session data from the local SQLite archive to a remote ClickHouse instance, enabling team-wide dashboards and read-only queries at analytics scale.
It parallels the PostgreSQL sync and DuckDB mirror features with incremental push, named targets, project filtering, watch mode, OS service management, and read-only serving of the web UI from ClickHouse.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Engineering manager | Team-wide visibility into agent usage at scale |
| Team member | Access session data from ClickHouse-connected analytics tools |
| Operator | Configure multiple ClickHouse targets (work, archive) and run unattended push |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall push session data from SQLite to ClickHouse incrementally |
| FR-2 | Must | The system shall support project filtering (include/exclude projects) |
| FR-3 | Must | The system shall use fingerprint-based change detection for incremental pushes |
| FR-4 | Must | The system shall support named ClickHouse targets (multiple destinations) |
| FR-5 | Must | The system shall serve the web UI read-only from ClickHouse |
| FR-6 | Should | The system shall provide a watch mode that auto-pushes on session changes |
| FR-7 | Should | The system shall support OS service management (systemd/launchd) for auto-push |
| FR-8 | Should | The system shall sync pricing, usage, curation, and activity-report data to ClickHouse |
| FR-9 | Should | The system shall report per-target push status (watermarks, pending counts) |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Consistency | Push must be idempotent; re-running produces the same state |
| NFR-2 | Must | Security | Plain-text ClickHouse URLs are refused unless explicitly allowed |

## Constraints

- Push is one-way; ClickHouse content is never read back into SQLite.
- The mirror schema uses `ReplacingMergeTree` tables versioned per push.

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** local SQLite has session data
    - **When** `agentsview clickhouse push` is run
    - **Then** session data is replicated to ClickHouse
- [ ] **FR-2**
    - **Given** a target configured with project filters
    - **When** `agentsview clickhouse push` is run
    - **Then** only in-scope projects are pushed
- [ ] **FR-3**
    - **Given** a previous successful push
    - **When** `agentsview clickhouse push` is run with no local changes
    - **Then** unchanged sessions are skipped via fingerprint comparison
- [ ] **FR-4**
    - **Given** multiple named ClickHouse targets are configured
    - **When** `agentsview clickhouse push <name>` is run
    - **Then** only the named target receives data
- [ ] **FR-5**
    - **Given** ClickHouse holds mirrored data
    - **When** `agentsview clickhouse serve` is started
    - **Then** the web UI serves read-only from ClickHouse
- [ ] **FR-6**
    - **Given** the watch loop is running
    - **When** new sessions are synced locally
    - **Then** they are automatically pushed to ClickHouse
- [ ] **FR-7**
    - **Given** the OS service is installed
    - **When** the machine boots
    - **Then** ClickHouse watch push runs without manual intervention
- [ ] **FR-8**
    - **Given** local pricing and usage data exist
    - **When** `agentsview clickhouse push` is run
    - **Then** pricing, usage, curation, and activity-report tables are updated
- [ ] **FR-9**
    - **Given** a configured ClickHouse target
    - **When** `agentsview clickhouse status` is run
    - **Then** sync watermarks and pending work are reported
- [ ] **NFR-1**
    - **Given** a completed push
    - **When** the same push is run again
    - **Then** the mirror state is unchanged and no duplicates appear
- [ ] **NFR-2**
    - **Given** a `http://` ClickHouse URL without an explicit insecure allowance
    - **When** a push or status check is attempted
    - **Then** the command fails with a transport-security error

## Conflicts

None identified yet.

## Open Questions

1. Should the ClickHouse reader support recall entries and semantic search, which it currently reports as unavailable?
