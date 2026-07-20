---
title: "PostgreSQL Sync"
status: done
---

# Specification: PostgreSQL Sync

## Overview

The PostgreSQL integration has two modes: push sync and read-only serve. Push sync (`internal/postgres/push.go`) incrementally copies sessions from SQLite to PostgreSQL using a fingerprint-based diff. Read-only serve (`internal/postgres/store.go`) implements `db.Store` for PostgreSQL-backed queries. Named targets allow multiple PG destinations.

## Architecture

```
SQLite DB → Push Engine (fingerprint diff) → PostgreSQL
                  ↓
           Watch Daemon (fsnotify events)
                  ↓
           OS Service (systemd/launchd)
```

## Data Models

### Named PG Target Config

| Field | Type | Description |
|---|---|---|
| name | string | Target name (e.g. "work", "archive") |
| url | string | PostgreSQL DSN |
| machine_name | string | Identifier for this machine |
| exclude_projects | []string | Projects to skip |
| schema | string | PG schema name |

## API Contracts

### POST /api/v1/push/pg
**Request:** `{"target": "default"}`
**Response:** Push status

## Sequences

### Incremental Push
```
1. Query SQLite for sessions with fingerprint > last_push_fingerprint
2. Batch insert/update into PostgreSQL
3. Record max fingerprint for next push
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Change detection | Monotonic fingerprint column | O(1) incremental detection |
| Read serve | Implements `db.Store` interface | Same API handlers work for SQLite, PG, DuckDB |
| Conflict resolution | Machine-owner wins | Different machines may have different versions of same session |

## Risks and Unknowns

1. Schema drift between SQLite and PostgreSQL on version upgrade
