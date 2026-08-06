---
title: "Command Center & Operational Monitoring"
status: done
---

# Specification: Command Center & Operational Monitoring

## Overview

The Command Center (`packages/dashboard/app/components/command-center/`) surfaces fleet health; usage/cost route registrars track per-task usage; signal connectors accept HMAC-signed payloads; and monitor/diagnostics routes report system health. Real-time status flows over the shared `/api/events` SSE bus.

## Architecture

```
Dashboard CommandCenter (components/command-center + monitor routes)
      │  register-command-center-routes, register-usage-routes,
      │  register-signal-routes, monitor-routes, register-diagnostics-routes
      ▼
Signal connectors (HMAC verify) ──► board/command surface
      │  /api/events (SSE)
      ▼
@fusion/core task store (usage/cost accounting)
```

## Data Models

### Usage / Cost

| Field | Type | Constraints | Description |
|---|---|---|---|
| taskId | int | PK/FK | Task the usage pertains to |
| tokens | json | — | Input/output token totals per model |
| costMs | int | — | Computed cost in ms-equivalent |

### API Contracts

### POST /api/signals/<type>

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| type | enum | yes | sentry / datadog / pagerduty / webhook |
| payload | object | yes | Signal payload |
| signature | string | yes | HMAC signature |

**Response**

| Status | Code | Description |
|---|---|---|
| 202 | ACCEPTED | Signal accepted |
| 401 | UNAUTHORIZED | HMAC verification failed |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| HMAC signing | `docs/signals-connectors.md` | Authenticates payload origin |
| Realtime over SSE | shared `/api/events` | Single event stream for status |
| Cost in core | task store accounting | Read-only outside writer |

## Risks and Unknowns

1. Cost accounting basis (token vs. billing) is unresolved; tracked in requirements.

## Out of Scope

- Executor internals (FEAT-p4) and merge mechanics (FEAT-p5)