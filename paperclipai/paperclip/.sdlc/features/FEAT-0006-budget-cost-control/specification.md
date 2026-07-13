---
title: "Budget & Cost Control"
status: done
---

# Specification: Budget & Cost Control

## Overview

Cost events are the atomic input; all spend figures are aggregations. Budgets are monthly UTC windows scoped to company and agent (project optional). Enforcement runs in the heartbeat scheduler/checkout path: at the hard limit the agent is paused and invocations are blocked. A soft threshold warns at 80%.

## Architecture

```
Agent → POST /cost-events → cost_events (validated) → rollups (read-time aggregation)
Scheduler/checkout → budget check → hard limit? → pause agent + block + activity
Board → PATCH /budgets, resume → override
```

## Data Models

### cost_events

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| agent_id | uuid | FK, not null | Spending agent |
| issue_id / project_id / goal_id | uuid | FK, null | Attribution |
| provider / model | text | not null | Cost source |
| input_tokens / output_tokens | int | not null, default 0 | Usage |
| cost_cents | int | not null | Cost |
| occurred_at | timestamptz | not null | When it happened |

Supporting tables: `budget_policies`, `budget_incidents`, `finance_events`.

## API Contracts

### POST /companies/:companyId/cost-events

Ingest a cost event with ownership checks and validation.

### GET /companies/:companyId/costs/summary | /by-agent | /by-project

Read-time aggregate rollups.

### PATCH /companies/:companyId/budgets | PATCH /agents/:agentId/budgets

Set company/agent budgets.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Negative tokens or cost |
| 403 | UNAUTHORIZED | Agent reporting cost for another company's entity |

## Sequences

### Hard-stop auto-pause

```
cost event ingest → spend crosses 100% → agent.status=paused → block checkout/invocation → high-priority activity
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Rollups | Read-time aggregation | Simplicity for V1; materialize later only if needed |
| Enforcement point | Scheduler + checkout path | Catches both scheduled and manual work |

## Risks and Unknowns

1. Concurrent cost ingestion near the threshold must not double-spend or miss the pause.

## Out of Scope

- Revenue/expense accounting beyond model/token costs.
