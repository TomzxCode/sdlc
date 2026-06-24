---
title: "Goal Hierarchy"
status: draft
---

# Specification: Goal Hierarchy

## Overview

Goals are company-scoped tree nodes with level, status, and owner.
They form the alignment chain from company mission down to individual tasks.
The goals table uses `parent_id` for hierarchy and `level` for semantic tiering.
Projects and issues link to goals via `goal_id` foreign keys, enabling cost rollups and progress tracking by goal.

## Architecture

```
Board/Agent ──► /api/goals (CRUD)
                    │
                    ▼
               goals table (company_id, parent_id, level, status, owner_agent_id)
                    │
                    ├── issues.goal_id (task-to-goal link)
                    ├── projects.goal_id (project-to-goal link)
                    └── activity_log (goal mutations)
```

## Data Models

### goals

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Goal identifier |
| company_id | uuid | FK companies, not null | Scoping |
| title | text | not null | Goal name |
| description | text | null | Optional description |
| level | text | not null, default `task` | `company | team | task` |
| status | text | not null, default `planned` | `planned | active | completed | cancelled` |
| parent_id | uuid | FK goals, null | Parent goal (null = root) |
| owner_agent_id | uuid | FK agents, null | Responsible agent |
| created_at / updated_at | timestamptz | not null | Timestamps |

## API Contracts

### GET /companies/:companyId/goals

List goals for a company.

### POST /companies/:companyId/goals

Create a goal. Request body includes title, description, level, status, parentId, ownerAgentId.

### GET /goals/:goalId

Get a single goal by ID.

### PATCH /goals/:goalId

Update goal fields.

### DELETE /goals/:goalId

Delete a goal (soft delete optional, hard delete board-only).

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Validation error on goal fields |
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Goal not found |

## Sequences

### Create a goal hierarchy

```
Hirer → POST /companies/:id/goals (root level=company) → goals row
Hirer → POST /companies/:id/goals (parent=root, level=team) → child goal
Issue  → issue.goal_id = childGoal.id → traceable chain: issue → childGoal → rootGoal
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Hierarchy model | Adjacency list (`parent_id`) | Simple, well-understood for shallow trees |
| Level enum | `company | team | task` | Matches the org hierarchy semantic tiers |
| Linking method | Foreign keys (goal_id on issues/projects) | Direct traceability without join tables |

## Risks and Unknowns

1. Deep goal hierarchies may cause slow recursive queries; materialized paths or closure tables may be needed at scale.
2. The relationship between goal level and org tree (`reports_to`) level needs precise documentation.

## Out of Scope

- Goal-based budget allocation (V1 uses agent/company budgets only).
- Automatic goal progress calculation from subtask completion.
