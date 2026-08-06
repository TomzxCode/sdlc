---
title: "Task Board & Task Lifecycle Management"
status: done
---

# Specification: Task Board & Task Lifecycle Management

## Overview

The task board is implemented by a domain task store in `@fusion/core` (task creation, mutation ops, lifecycle ops, moves, comments, artifacts, file-scope, branch-context, search, and an advisory-lock), exposed through dashboard API route registrars and CLI commands, and rendered by React components in the dashboard SPA.

## Architecture

```
board/list React components (Board, ListView, TaskDetail, NewTask, TaskCard, Column)
      │  fetch + mutate
      ▼
Dashboard API registrars (register-tasks, register-task-workflow-routes)
      │
      ▼
@fusion/core task-store (task-creation, mutation-ops, lifecycle-ops, moves,
                           comments-ops, task-artifacts-ops, file-scope,
                           branch-context, search, task-advisory-lock)
      │
      ▼
PostgreSQL (tasks + related rows, soft-delete tombstones)
```

## Data Models

### Task

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | int | PK, not null | Task identifier (padded in some flows, bare elsewhere per convention) |
| column | enum | not null | planning/todo/in-progress/in-review/done |
| status | enum | not null | Domain status; `needs-replan` is the durable graph replan signal |
| userPaused | bool | — | User-paused semantics for backward moves |
| prompt / spec doc | text | — | The task's specification/prompt |
| file-scope | json | — | Files the task is allowed to touch |
| branch-context | json | — | Assigned branch / shared-branch group |

## API Contracts

### POST /api/tasks

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| title | string | yes | Task title |
| column | enum | no | Initial column (default planning) |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| task | object | The created task |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Malformed task payload |
| 404 | TASK_NOT_FOUND | Referenced task/issue missing |

## Sequences

### Create and move

```
Operator → dashboard create-task → task-store(task-creation) → DB (advisory lock)
Operator → move-task(in-progress → todo) → lifecycle guard → park with user-paused
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Domain store in core | `@fusion/core` task-store | Single source of truth; dashboard/CLI never touch raw DB |
| Per-task advisory lock | `task-advisory-lock.ts` | Prevents conflicting concurrent lifecycle mutations |
| Board move | `moves.ts` | Supports per-task and board-level moves with guard rails |
| Soft-delete tombstone | keep tombstone | Preserves audit trail, prevents resurrect |

## Risks and Unknowns

1. Board-level move semantics across mixed workflow selections are not fully specified above.

## Out of Scope

- Workflow graph execution (see FEAT-p2); lifecycle here is the board surface and its guards
- Specific merge behavior (see FEAT-p5)