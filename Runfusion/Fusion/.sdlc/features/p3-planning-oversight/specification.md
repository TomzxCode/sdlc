---
title: "Planning Mode & Planner Oversight"
status: done
---

# Specification: Planning Mode & Planner Oversight

## Overview

Planning is owned by a workflow-graph Plan Review node, fed by a Planning Mode chat and a specification editor. An overseer controller in `@fusion/core` (state, events, interventions, recovery) plus engine planner lanes produce plan artifacts and record events; the dashboard surfaces Planning Mode, the Intervention Timeline, and oversight controls.

## Architecture

```
Dashboard (PlanningModeModal, TaskPlannerChatTab, SpecEditor,
           PlannerInterventionTimeline, plannerOverseerBadge)
      │
      ▼
Dashboard API (register-planning-chat, register-planning-subtask-routes,
               tasks-overseer-controls, tasks-planner-overseer-state)
      │
      ▼
@fusion/core/planner (plan-approval, planner-confirmation,
                      planner-intervention, planner-overseer-state,
                      planner-overseer-events, planner-recovery, overseer-advice,
                      planning-plan-md)
      │
      ▼
@fusion/engine (planner-lane-resolution, planning-handoff-recovery,
                plan-review-continuation, plan-review-feedback-history,
                plan-artifact-writeback, overseer/)
```

## Data Models

### Planner Oversight State

| Field | Type | Constraints | Description |
|---|---|---|---|
| oversightLevel | enum | not null | off / observe / steer / autonomous |
| perTaskOverride | enum | — | Per-task override of the global level |
| confirmation | object | — | Pending human confirmation for merge/PR/destructive actions |
| interventions | array | — | Timeline of overseer interventions |

## API Contracts

### GET /api/tasks/:id/overseer-state

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| oversightLevel | enum | Effective oversight level |
| interventions | array | Intervention timeline entries |

## Sequences

### Plan and review

```
Planning Mode → planner produces plan → Plan Review node (workflow graph)
   → verdict approved / changes-requested
   → on failure: plan-replan → requestPreMergeOptionalStepFix → executor replan
```

### Oversight action

```
overseer tick → evaluateOverseerHumanControl (guard) → withhold/steer/confirm
   → if user-paused/auto-merge-off → emit task:oversight-withheld-human-control (deduped)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Oversight levels | off/observe/steer/autonomous | Escalating automation with a human gate at the top |
| Guard-first | `evaluateOverseerHumanControl` runs before classification | Prevents actions on paused/auto-merge-off tasks |
| Graph-owned Plan Review | workflow node | No duplicate review authority |
| Intervention Timeline | persisted interventions + events | Operator observability of overseer behavior |

## Risks and Unknowns

1. Confirmation state must survive engine restarts (handoff recovery), tracked by engine tests.

## Out of Scope

- Plan execution (FEAT-p4) and merge mechanics (FEAT-p5)