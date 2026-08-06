---
title: "Selectable Workflows & Visual Workflow Editor"
status: done
---

# Specification: Selectable Workflows & Visual Workflow Editor

## Overview

Workflows are modeled as an intermediate representation (workflow IR) of nodes and transitions in `@fusion/core`, executed by a graph executor and node runners in `@fusion/engine`, and authored visually in the dashboard's workflow editor. Definition types, built-in workflows, transition policy, and settings resolution live in core; execution, review, planning, foreach/loop, and task-runtime services live in the engine.

## Architecture

```
Workflow editor (WorkflowNodeEditor, WorkflowSimpleCanvas, WorkflowFieldsPanel,
                 WorkflowSettingsPanel, WorkflowSelector)  [dashboard/app]
      │  author / validate / select
      ▼
Dashboard API (register-workflow-routes, board-workflows)
      │
      ▼
@fusion/core/workflows (workflow-ir, workflow-definition-types,
                        workflow-transitions, workflow-transition-policy,
                        workflow-settings-resolver, builtin-workflows, builtin-*)
      │
      ▼
@fusion/engine/workflows (workflow-graph-executor, workflow-node-runner,
                          workflow-node-handlers, workflow-review-service,
                          workflow-planning-service, workflow-graph-foreach,
                          workflow-graph-loop, workflow-task-runtime)
      │  per-node runners (code / gate / merge / exit-gate / review)
      ▼
Task store / worktree execution
```

## Data Models

### Workflow Definition

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Workflow identifier |
| kind | enum | not null | builtin / custom / v1 |
| nodes | array | not null | Graph nodes with node type, settings, and successors |
| settings | object | — | Workflow-level settings (oversight level, gates, merge strategy) |

## API Contracts

### POST /api/workflows/validate

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| definition | object | yes | Workflow IR to validate |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| valid | boolean | Whether the definition is valid |
| errors | array | Validation errors |

## Sequences

### Graph advance

```
graph-executor → node-runner(code) → runner executes in worktree
     → next node (review) → workflow-review-service → verdict
     → gate/merge node → transition policy → next or terminal
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Workflow IR in core | `workflow-ir.ts` | Single canonical representation shared by editor and engine |
| Graph executor in engine | `workflow-graph-executor.ts` | Executes transitions outside the domain layer |
| Single review authority | graph-owned review nodes | Prevents duplicate Plan Review race |
| Visual editor | dashboard components | Operator-authored custom workflows without file editing |

## Risks and Unknowns

1. Custom workflow reliability acceptance across restart durability and deferred journeys is a tracked map (`docs/custom-workflow-reliability-acceptance-map.md`).

## Out of Scope

- Non-graph legacy lifecycle execution (deleted; ratcheted by `legacy-tombstones.test.ts`)
- Merging mechanics themselves (FEAT-p5)