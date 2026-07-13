---
title: "Activity Audit Log"
status: done
---

# Specification: Activity Audit Log

## Overview

The activity log is an append-only event stream. Every route handler that mutates state calls the activity service to persist an entry. The API exposes filtered, paginated queries for the board UI and agent scopes. The table is indexed on `company_id`, `created_at`, `actor_type`, `entity_type`, and `action` for efficient filtering.

## Architecture

```
Route handler (after mutation)
    │
    ▼
activityService.log(actor, action, entity, details)
    │
    ▼
activity_log table (append-only INSERT)
    │
    ▼
GET /api/companies/:companyId/activity (paginated, filtered)
    │
    ▼
Activity.tsx UI page (table with filters)
```

## Data Models

### activity_log

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, not null | Entry identifier |
| company_id | uuid | FK companies, not null | Company scoping |
| actor_type | enum | not null | `agent | user | system` |
| actor_id | uuid | not null | Who performed the action |
| action | text | not null | Action key (e.g. `agent.create`, `issue.status_update`, `approval.decision`) |
| entity_type | text | not null | Resource type (e.g. `agent`, `issue`, `approval`) |
| entity_id | uuid | not null | Resource identifier |
| details | jsonb | null, default `{}` | Additional context (e.g. old/new status, field changes, payload excerpts) |
| ip_address | text | null | Origin IP when available |
| created_at | timestamptz | not null, default now() | When the action occurred |

## API Contracts

### GET /companies/:companyId/activity

Returns paginated activity entries.

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| cursor | string | no | Pagination cursor |
| limit | int | no, default 50 | Max entries per page |
| actorType | string | no | Filter by actor type |
| action | string | no | Filter by action key prefix |
| entityType | string | no | Filter by resource type |
| from | ISO date | no | Start of date range |
| to | ISO date | no | End of date range |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| entries | array | Activity entry objects |
| nextCursor | string | Cursor for next page |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Caller lacks company access |

## Sequences

### Logging a mutation

```
Route handler → validate input → mutate DB → activityService.log(actor, "issue.status_update", issueId, {from: "todo", to: "in_progress"}) → respond
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | Append-only table with indexes | Simple, no external service needed for V1 |
| Pagination | Cursor-based | Consistent under write load |
| Actor modeling | Polymorphic (agent/user/system) with type discriminator | Single table, no joins needed |

## Risks and Unknowns

1. At very high volume, the activity_log table may need partition pruning or archival strategies.

## Out of Scope

- Tamper-evident hashing or blockchain-style integrity chains (deferred)
- Real-time streaming of activity events (deferred)
