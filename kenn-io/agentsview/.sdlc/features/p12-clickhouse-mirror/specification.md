---
title: "ClickHouse Mirror"
status: done
---

# Specification: ClickHouse Mirror

## Overview

The ClickHouse integration has two modes: push sync and read-only serve.
Push sync (`internal/clickhouse/sync.go`, `push.go`) incrementally copies sessions from SQLite to ClickHouse using fingerprint comparison against the mirror.
Read-only serve (`internal/clickhouse/store.go`) implements `db.Store` for ClickHouse-backed queries, including sessions, messages, analytics, usage, search, secrets, and activity reports.
Named targets allow multiple ClickHouse destinations, and the `clickhouse-go/v2` driver provides the transport.

## Architecture

```
SQLite DB → Sync engine (fingerprint diff) → ClickHouse (ReplacingMergeTree)
                  ↓
           Watch loop (change events + periodic floor)
                  ↓
           OS service (systemd/launchd via clickhouse service)
                  ↓
           Read-only serve (db.Store over ClickHouse)
```

## Data Models

### ClickHouse target config

| Field | Type | Constraints | Description |
|---|---|---|---|
| url | string | required | ClickHouse DSN (native or HTTP protocol) |
| database | string | optional | Mirror database name |
| allow_insecure | bool | optional | Permit plain-text HTTP URLs |
| projects | list | optional | Inclusive project filter |
| exclude_projects | list | optional | Exclusive project filter |

### Push options

| Field | Type | Constraints | Description |
|---|---|---|---|
| full | bool | optional | Re-push every in-scope session and remove stale mirror rows |

### Push result

| Field | Type | Constraints | Description |
|---|---|---|---|
| sessions_pushed | int | not null | Sessions written in this push |
| messages_pushed | int | not null | Messages written in this push |
| skipped_unchanged | int | not null | Sessions skipped by fingerprint match |
| deleted_stale | int | not null | Stale mirror sessions removed |
| errors | int | not null | Sessions that failed to push |

### Mirror tables

| Table | Purpose |
|---|---|
| sessions | Mirrored session rows with fingerprints and archive identity |
| messages | Mirrored message rows per session |
| usage_events | Token and cost usage events |
| cursor_usage_events | Cursor usage API events |
| model_pricing | Pricing catalog snapshot |
| tool_calls | Tool call records for analytics |
| secret_findings | Secret scan findings |
| sync_metadata | Push cursors and schema version |
| source_archives | Contributing archive identities |

## API Contracts

### `agentsview clickhouse push [target]`

**Request**

| Flag | Type | Required | Description |
|---|---|---|---|
| --all | bool | no | Push every configured target sequentially |
| --full | bool | no | Force full local resync and push |
| --projects | string | no | Comma-separated inclusive project list |
| --exclude-projects | string | no | Comma-separated exclusive project list |
| --all-projects | bool | no | Ignore configured project filters |
| --watch | bool | no | Run continuously with debounce and interval floor |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| summary | text | Pushed/skipped/removed session and message counts |

### `agentsview clickhouse status [target]`

**Request**

| Flag | Type | Required | Description |
|---|---|---|---|
| --all | bool | no | Show status for every configured target |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| status | text | Sync watermarks and pending work per target |

### `agentsview clickhouse serve`

Serves the web UI read-only from ClickHouse.
Accepts `--base-path` and the shared serve flags.

### `agentsview clickhouse service`

Installs and manages the OS service (systemd/launchd) for unattended watch push.
Refuses to install when the URL is unset, comes from the environment, or uses unresolved variable expansion.

### POST /api/v1/push/clickhouse

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| target | string | no | Named target to push |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| result | object | Push result summary |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | URL not configured or project filters invalid |
| 400 | INSECURE_TRANSPORT | Plain-text URL without explicit allowance |

## Sequences

### Incremental push

```
CLI → resolve target → CheckTransportSecurity → fingerprint local candidates
→ compare against mirror fingerprints → write changed batches with retry
→ sync machine metadata → update sync_metadata cursor
```

### Watch push

```
File watcher event → debounce window → scoped push → progress report
→ periodic interval floor push even without events
```

### Read-only serve

```
HTTP request → ClickHouse Store (db.Store) → SQL over mirror tables → web UI
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Change detection | Mirror-side fingerprint comparison | Avoids a monotonic local column and handles scope changes |
| Table engine | ReplacingMergeTree with push version | Idempotent re-pushes collapse to the latest version |
| Read serve | Implements `db.Store` interface | Same API handlers work for SQLite, PG, DuckDB, and ClickHouse |
| Driver | clickhouse-go/v2 | Native protocol plus HTTP support in one maintained client |
| Transport guard | Refuse plain-text URLs by default | ClickHouse often holds full session content |

## Risks and Unknowns

1. Schema drift between SQLite and ClickHouse on version upgrade requires role privileges to create tables.
2. The ClickHouse reader does not implement recall queries or semantic search, so those surfaces stay unavailable in `clickhouse serve` mode.

## Out of Scope

- Bi-directional sync from ClickHouse back into SQLite.
- Quack-style remote protocol exposure (unlike the DuckDB mirror).
