---
title: "SQLite Session Storage"
status: done
---

# Specification: SQLite Session Storage

## Overview

`pi-storage-sqlite-node` implements a `node:sqlite` backend for agent sessions.
A `SqliteSessionRepository` implements the agent session-repository contract, backed by a single lazy shared connection.
Schema migrations set up the canonical tables plus materialized projections (session summaries, entries, sequences, branch tips), and an independent search backend provides FTS queries over the same database.

## Architecture

```
+-------------------------------+
|  SqliteSessionRepository      |
|  (implements session repo)    |
+--------------+----------------+
               | node:sqlite (lazy single connection)
               v
+--------------+----------------+
|        SQLite database        |
| migrations 001_initial,       |
| 002_branch_tips               |
| storage/: sessions, entries,  |
|  sequences, materialized,     |
|  branch-cache                 |
+-------------------------------+
               ^
+--------------+----------------+
|  createSqliteSessionSearch    |
|  (FTS search, query-only)     |
+-------------------------------+
```

`sqlite/repo.ts` is the repository; `sqlite/migrations.ts` + `sqlite/migrations/*.sql` the schema; `sqlite/storage/` the table/storage modules; `sqlite/search-backend.ts` the FTS search; `sqlite/types.ts` the shared types.

## Data Models

### Session table (excerpt, from `001_initial.sql`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text/uuid | PK | Session identifier |
| cwd | text | not null | Working directory |
| created_at | int | not null | Creation timestamp |
| ... | | | Full session schema from migration |

### Branch tips (from `002_branch_tips.sql`)

Tracks the tip of each session branch to support fast branch navigation and summaries.

## API Contracts

### `new SqliteSessionRepository(options)`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| options | object | yes | Path/database + session schema options |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| repository | SqliteSessionRepository | Async-disposable repository |

### `createSqliteSessionSearch(options)`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| options | object | yes | Database + search options |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| search | object | `.search({ text })` returning matching entries |

## Sequences

### Open + migrate

```
new SqliteSessionRepository → open database → run pending migrations
→ materialize views → ready
```

### Search

```
createSqliteSessionSearch → query-only projection over same database
→ search({ text }) → hits
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Driver | `node:sqlite` | No native dependency, Node >= 22.19.0 |
| Connection | single lazy shared connection | Simplicity; repository owns lifecycle |
| Migrations | versioned `.sql` files | Deterministic schema evolution |
| Projections | materialized views + branch tips | Fast reads without touching raw logs |
| Search | separate query-only backend | No write coupling between repo and search |

## Risks and Unknowns

1. `node:sqlite` is a recent Node API; version floor must be honored.
2. FTS behavior and query semantics are experimental.

## Out of Scope

- The remote-session protocol/client/server (separate features).
- The JSONL session manager in the coding agent.
