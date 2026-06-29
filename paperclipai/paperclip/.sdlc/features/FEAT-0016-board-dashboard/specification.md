---
title: "Board Dashboard"
status: draft
---

# Specification: Board Dashboard

## Overview

The dashboard aggregates data across multiple entity types into a single summary payload. The server endpoint performs several parallel aggregation queries and returns a structured response. The React UI renders cards/stats for each section. The full-screen live/wallboard variant uses the same endpoint with auto-refresh.

## Architecture

```
Board → GET /api/companies/:companyId/dashboard
           │
           ▼
      Parallel queries:
        ├─ agent status counts (agents table, GROUP BY status)
        ├─ issue state counts (issues table, GROUP BY status)
        ├─ cost summary (cost_events aggregation, current month)
        ├─ pending approvals count
        └─ recent activity (activity_log, last N entries)
           │
           ▼
      DashboardPayload → Dashboard.tsx / DashboardLive.tsx
```

## Data Models

No dedicated dashboard table. All data is aggregated at read time from existing entity tables: `agents`, `issues`, `cost_events`, `approvals`, `activity_log`.

## API Contracts

### GET /companies/:companyId/dashboard

Returns the dashboard summary.

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| companyId | uuid | path | Company to scope to |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| agentCounts | object | `{active, running, paused, error, terminated, idle, pending_approval}` |
| issueCounts | object | `{backlog, todo, in_progress, in_review, done, blocked, cancelled}` |
| spend | object | `{spentCents, budgetCents, utilizationPct}` |
| pendingApprovals | int | Count of pending approvals |
| recentActivity | array | Last 10 activity entries |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Company not found |

## Sequences

### Dashboard load

```
Board navigates to company → GET /dashboard → parallel DB aggregations → render cards
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Aggregation | Read-time parallel queries | Simple V1; no materialized view maintenance |
| UI | Server-rendered payload, React cards | Separation of concerns; payload can evolve independently |

## Risks and Unknowns

1. Dashboard load may degrade at large scale; materialized views or caching may be needed later.

## Out of Scope

- Real-time push updates (WebSocket/SSE) for live dashboard (deferred)
- Custom widget configuration per user
