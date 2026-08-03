---
title: "SQLite Session Storage"
status: done
---

# Requirements: SQLite Session Storage

## Overview

`@earendil-works/pi-storage-sqlite-node` provides a `node:sqlite` storage backend for `pi-agent-core` sessions.
It ships the `SqliteDatabase` adapter, a `SqliteSessionRepository`, schema migrations (including branch-tips tracking), materialized session projections, and an optional full-text search backend.
Sessions can be created, opened, and queried with text search against a single canonical SQLite database.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agent users | Fast, queryable session persistence with search |
| `pi-agent-core` integrators | A drop-in SQLite backend behind the existing session repository interface |
| Search consumers | Optional FTS search over session content |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `SqliteDatabase` adapter over `node:sqlite`. |
| FR-02 | Must | The system shall provide a `SqliteSessionRepository` implementing the agent session repository interface. |
| FR-03 | Must | The system shall create and open sessions with a cwd, and persist session data durably. |
| FR-04 | Must | The system shall run schema migrations on open (including `001_initial` and `002_branch_tips`). |
| FR-05 | Should | The system shall maintain materialized views for session summaries, entries, and sequences. |
| FR-06 | Should | The system shall provide an optional FTS search backend (`createSqliteSessionSearch`) for text queries. |
| FR-07 | Should | The system shall share one lazy database connection across repository and search. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Correctness | Migrations shall be idempotent and version-tracked. |
| NFR-02 | Must | Reliability | The repository shall lazily own one shared connection; errors surface cleanly. |
| NFR-03 | Should | Performance | Search shall be a query-only projection over the canonical database. |
| NFR-04 | Should | Portability | Node `>=22.19.0` with built-in `node:sqlite`; no native build step. |

## Constraints

- Requires Node's built-in `node:sqlite` (Node >= 22.19.0).
- Tested through `packages/agent/test/harness/`; the package itself carries no test files.

## Acceptance Criteria

- [ ] **FR-02**
    - **Given** an open `SqliteSessionRepository`
    - **When** `repository.create({ cwd })` is called
    - **Then** a new session is created and persisted.
- [ ] **FR-04**
    - **Given** a fresh database file
    - **When** the repository is opened
    - **Then** migrations `001_initial` and `002_branch_tips` are applied.
- [ ] **FR-06**
    - **Given** a session with content
    - **When** `search.search({ text: "needle" })` runs
    - **Then** matching session entries are returned.
- [ ] **NFR-01**
    - **Given** an already-migrated database
    - **When** the repository is opened again
    - **Then** no migration is re-applied and no error is thrown.

## Conflicts

None identified yet.

## Open Questions

1. Should the SQLite backend become the default session store, or remain an opt-in alternative to JSONL?
