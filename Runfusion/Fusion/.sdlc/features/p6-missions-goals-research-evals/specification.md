---
title: "Missions, Goals, Research & Evals"
status: done
---

# Specification: Missions, Goals, Research & Evals

## Overview

Missions (mission → milestone → feature) are modeled in `@fusion/core` and driven by engine autopilot/execution loops with board sync. Goals add objectives/KRs with citation extraction. Research runs are orchestrated with providers and step runners. Evals score outcomes with persisted evidence. Dashboard views surface all four.

## Architecture

```
Dashboard (MissionManager, GoalsView, ResearchView, MissionInterviewModal)
      │  integrated routers (register-integrated-routers)
      ▼
@fusion/core (mission-store, goal-store, research-store)
      │
      ▼
@fusion/engine (mission-autopilot, mission-execution-loop, mission-feature-sync,
                mission-verification, mission-symbol-admission,
                goal-*, research-orchestrator/step-runner/dispatcher, eval-*)
```

## Data Models

### Mission / Milestone / Feature

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Mission id |
| milestone | object | — | Milestones with their features |
| feature | object | — | Feature synced to board task |
| progress | int | — | Completion-derived progress |

## API Contracts

### GET /api/missions/:id

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| mission | object | Mission with milestones/features |

## Sequences

### Mission autopilot

```
mission → autopilot → features synced to board → execution loop → verification
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Hierarchy in core store | `mission-store.ts` | Single domain model |
| Autopilot in engine | `mission-autopilot.ts` | Drives execution outside domain |
| Research orchestrator | engine providers | Cited-search/synthesis + experiment sessions |
| Run-audit hygiene | ids/counts/outcomes only | Never persist prose or research prompt text |

## Risks and Unknowns

1. `evaluations` and `insights` integrated routers are not fully mapped to a canonical feature surface at sync time.

## Out of Scope

- Board rendering (FEAT-p1) and execution engine (FEAT-p4) internals