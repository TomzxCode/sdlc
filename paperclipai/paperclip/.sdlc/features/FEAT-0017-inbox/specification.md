---
title: "Inbox"
status: draft
---

# Specification: Inbox

## Overview

The inbox service aggregates issues relevant to the current user. It queries the issues table filtered by assignee and company, applies read-state and dismissal tracking, and supports archival. Join request queue is surfaced separately. Dismissal and read state are stored in per-user tables (`inbox_dismissals`, `issue_read_states`, `issue_inbox_archives`).

## Architecture

```
User → GET /api/inbox?view=mine|recent|unread|blocked|all
           │
           ▼
      inbox service:
        ├─ issues query (filtered by view)
        ├─ read state join (issue_read_states)
        ├─ dismissal filter (inbox_dismissals)
        ├─ join request queue (join_requests)
        └─ archival (issue_inbox_archives)
           │
           ▼
      Inbox.tsx (tabs: mine, recent, unread, blocked, all)
```

## Data Models

### issue_read_states

| Field | Type | Constraints | Description |
|---|---|---|---|
| user_id | uuid | PK, not null | User who read |
| issue_id | uuid | PK, not null | Issue read |
| read_at | timestamptz | not null | When first read |
| last_seen_comment_at | timestamptz | null | Last read comment timestamp |

### inbox_dismissals

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| user_id | uuid | FK, not null | User who dismissed |
| issue_id | uuid | FK, not null | Dismissed issue |
| dismissed_at | timestamptz | not null | When dismissed |

### issue_inbox_archives

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| user_id | uuid | FK, not null | User who archived |
| issue_id | uuid | FK, not null | Archived issue |
| archived_at | timestamptz | not null | When archived |

## API Contracts

### GET /inbox

Returns inbox items.

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| view | string | no, default mine | `mine | recent | unread | blocked | all` |
| companyId | uuid | yes | Company scope |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| items | array | Inbox item objects |
| joinRequests | array | Pending join requests (board only) |

### POST /inbox/dismiss

Dismiss an inbox item.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Issue not found |

## Sequences

### Inbox load

```
User navigates to inbox → GET /inbox?companyId=X&view=mine → query issues WHERE assignee=userId → filter out dismissed & archived → join read state → return items
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Read state | Separate table per user-issue pair | Simple, no field on issues table |
| Dismissal | Soft delete (table) | Reversible; no data loss |

## Risks and Unknowns

1. Read state tracking for users with hundreds of issues may require batch operations.

## Out of Scope

- Real-time inbox updates via push notifications (deferred)
- Inbox for agents (agents use heartbeat-based task discovery)
