---
title: "Routines & Schedules"
status: draft
---

# Specification: Routines & Schedules

## Overview

Routines are recurring definitions stored with their triggers, env, and revision history. A trigger fires a routine run that materializes an issue (with routine-scoped env overlay) and wakes the assigned agent. Routines are first-class company-scoped entities.

## Architecture

```
Trigger (cron/webhook/API) → routine run → create issue (routine env overlay) → wake assigned agent
                                  │
                                  └─► routine_runs + activity_log
routine_revisions (snapshotted env) ← routine_triggers ← routines (company-scoped)
```

## Data Models

### routines / routine_revisions / routine_triggers / routine_runs

| Field | Type | Constraints | Description |
|---|---|---|---|
| routines.id / company_id | uuid | FK, not null | Scoping |
| routines.env | jsonb | - | Secret-aware env binding |
| routine_triggers | - | - | cron / webhook / API trigger config |
| routine_revisions | - | - | Snapshotted routine state |
| routine_runs | - | - | Per-execution tracking |

## API Contracts

### /api/routines (CRUD + triggers)

Routine management and trigger configuration. Route handler: `server/src/routes/routines.ts`, service: `server/src/services/routines.ts`.

## Sequences

### Routine execution

```
trigger fires → routine run → issue created (routine env overlay after project env, before runtime keys) → wake agent → routine_runs + activity_log
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Env overlay order | routine env after project env, before runtime-owned keys | Predictable precedence; routine-owned secrets resolve without agent bindings |

## Risks and Unknowns

1. Overlapping executions and catch-up behavior need precise documented semantics.

## Out of Scope

- External calendar/scheduling integrations beyond cron/webhook/API.
