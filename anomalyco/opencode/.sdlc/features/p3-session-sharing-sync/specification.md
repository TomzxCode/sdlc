---
title: "Session Sharing & Sync"
status: done
---

# Specification: Session Sharing & Sync

## Overview

Sharing is implemented by the `SessionShare` service (`packages/opencode/src/share/session.ts`) and the `ShareNext` service (`packages/opencode/src/share/share-next.ts`). `ShareNext` owns the HTTP integration with the share host, queues and debounces sync payloads, and persists share metadata in the `SessionShareTable`. File state is tracked by the `Snapshot` service (`packages/opencode/src/snapshot/index.ts`), which maintains a shadow git repository per project/worktree to produce file diffs. Cross-device replay is enabled by the `SyncEvent` event-sourcing abstraction (`packages/opencode/src/sync/`), which records mutation events with a sequence id and republishes them as `Bus` events for backwards compatibility.

## Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │                Session runtime               │
                       │  mutations → SyncEvent.run(...)  ──►  Bus   │
                       └──────────────────┬───────────────────────────┘
                                          │ session/message/part/diff events
                                          ▼
                       ┌──────────────────────────────────────────────┐
                       │                ShareNext                     │
                       │  per-session queue  ── debounce 1s ── flush  │
                       │  request() selects host (legacy vs console)  │
                       │  SessionShareTable (id, url, secret)         │
                       └───────┬──────────────────────────────────────┘
                               │ HTTPS (Effect HttpClient)
                               ▼
                    share host  (/api/share | /api/shares)
                       │
                       │    ┌───────────────────────────────────────┐
                       │    │  Snapshot (shadow git repo)           │
                       │    │  track → patch → diff → restore →     │
                       │    │  revert; seeds object db from source  │
                       └────┴───────────────────────────────────────┘
```

## Data Models

### SessionShareTable (`packages/core/src/share/sql.ts`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| session_id | text | PK | The shared session |
| id | text | not null | Share host id (e.g. `shr_abc`) |
| secret | text | not null | Secret for authenticating sync/remove calls |
| url | text | not null | Public share URL |

### SyncEvent

| Field | Type | Description |
|---|---|---|
| id | uuid | Unique event id |
| seq | number | Monotonically increasing sequence for total ordering |
| type | text | Event type (e.g. `session.created`) |
| aggregateID | text | Session id the event belongs to |
| data | json | Typed event payload |
| version | number | Event schema version |

### Share payload (`Data` union)

The synced payload is a union of `session`, `message`, `part`, `session_diff`, and `model` items, each carrying its SDK-typed data.

## API Contracts

### POST /api/share (legacy) or /api/shares (console)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| sessionID | string | yes | Session to share |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| id | string | Share id |
| url | string | Public share URL |
| secret | string | Sync/remove secret |

### POST /api/share/:id/sync

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| secret | string | yes | Share secret |
| data | array | yes | Debounced batch of Data items |

### DELETE /api/share/:id

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| secret | string | yes | Share secret |

### GET /api/share/:id/data

Returns full shared session data (used by `opencode import`).

## Sequences

### Share creation

```
User /share → SessionShare.share(sessionID)
   ├─ if config share=disabled → error
   ├─ ShareNext.create(sessionID) → POST host → {id,url,secret}
   ├─ persist SessionShareTable row
   ├─ session.setShare({url})
   └─ fork full() sync: session info + messages + parts + diffs + models
```

### Incremental sync (debounced)

```
MessageV2.Event.PartUpdated / Session.Event.Diff
   └─ ShareNext.sync(sessionID, [item]) → upsert queue keyed by item
   └─ schedule flush after 1s → POST :id/sync with queued items
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Host selection | Legacy `/api/share` vs console `/api/shares` | Single writer model; enterprise/org auth via bearer token |
| Debounce | 1s delayed flush per session | Bounds request count under event bursts |
| Queue coalescing | Map keyed by item key | Latest data wins for a given message/part/diff |
| Snapshot storage | Shadow git repo with alternates seeding | Reuses source object hashes; large-repo performance |
| Event sourcing | `SyncEvent` with seq, republished to `Bus` | Total ordering with one writer; backwards compatible |
| Auth | `x-org-id` + `Authorization: Bearer` headers | Enterprise console routing |

## Risks and Unknowns

1. Sync events rely on a single writer; multi-device concurrent writes are not supported.
2. The `convertEvent` runtime reshape (e.g. `session.updated`) is a temporary backwards-compatibility hook.
3. Snapshot cleanup runs hourly with a 7-day prune; very large worktrees may still be slow to snapshot.

## Out of Scope

- Multi-writer distributed consistency.
- Rate limiting or abuse protection for the share host.
- A web viewer UI for shared links (hosted on the share host, not in this codebase).
