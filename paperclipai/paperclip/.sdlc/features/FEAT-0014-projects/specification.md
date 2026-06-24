---
title: "Projects"
status: draft
---

# Specification: Projects

## Overview

Projects are first-class company-scoped entities with status lifecycle, goal linkage, env configuration, workspaces, runtime services, and budget summaries.
The projects service (`server/src/services/projects.ts`, 1215 lines) handles CRUD, workspace management, runtime service orchestration, goal linking, and plugin-managed project resolution.
Project workspaces provide named working directories with repo integration; project execution workspace policy governs how execution worktrees are created for issues within the project.

## Architecture

```
Board/Agent ──► /api/projects (CRUD + workspaces + runtime)
                    │
                    ▼
               projects (company_id, goal_id, status, lead_agent_id, env)
                    │
                    ├── project_goals (goal links)
                    ├── project_memberships (user/agent join state)
                    ├── project_workspaces (named working directories)
                    │       └── workspace_runtime_services (dev servers, preview URLs)
                    ├── issues.project_id (issue-to-project link)
                    └── activity_log (project mutations)
```

## Data Models

### projects

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Project identifier |
| company_id | uuid | FK companies, not null | Scoping |
| goal_id | uuid | FK goals, null | Strategic alignment |
| name | text | not null | Project name |
| description | text | null | Optional description |
| status | text | not null, default `backlog` | `backlog | active | paused | completed | archived` |
| lead_agent_id | uuid | FK agents, null | Responsible agent |
| target_date | date | null | Target completion date |
| color | text | null | UI color |
| icon | text | null | UI icon |
| env | jsonb | null | AgentEnvConfig (secret-aware env) |
| execution_workspace_policy | jsonb | null | Policy for execution worktree creation |
| archived_at / paused_at | timestamptz | null | Status timestamps |
| created_at / updated_at | timestamptz | not null | Timestamps |

### project_workspaces

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | Workspace identifier |
| project_id | uuid | FK projects, not null | Parent project |
| name | text | not null | Human name |
| source_type | text | null | `git`, `local`, etc. |
| cwd | text | null | Working directory |
| repo_url / repo_ref / default_ref | text | null | Git source config |
| runtime_config | jsonb | null | WorkspaceRuntimeConfig |
| is_primary | boolean | default false | Primary workspace flag |
| visibility | text | default `company` | Visibility scope |

## API Contracts

### GET /companies/:companyId/projects, POST /companies/:companyId/projects, GET /projects/:projectId, PATCH /projects/:projectId

Standard project CRUD. Create/update accept goal_id, status, lead_agent_id, target_date, color, icon, env.

### Project workspace endpoints

`POST /projects/:projectId/workspaces`, `GET/PATCH /projects/:projectId/workspaces/:workspaceId` for workspace management.

### Project runtime service control

Runtime service desired state management and control via workspace runtime endpoints.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Validation error |
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Project not found |

## Sequences

### Create project with workspace

```
Board → POST /projects (name, goal_id, lead_agent_id) → project row
Board → POST /projects/:id/workspaces (name, repo_url, cwd) → workspace row
Agent → issue within project → resolve execution workspace per policy → agent runs in workspace context
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Project env | JSONB with secret ref syntax | Consistent with other env config patterns in Paperclip |
| Workspace model | Named project workspaces + execution worktree policy | Separates shared project state from isolated agent execution |
| Goal linking | Direct goal_id FK on projects | Simple traceability without a join table |
| Runtime services | Desired-state model (start/stop to match config) | Declarative lifecycle management |

## Risks and Unknowns

1. Env overlay precedence (project env → routine env → runtime keys) needs clear documentation.
2. Project workspace isolation and concurrency semantics when multiple agents work in the same project.
3. Plugin-managed project features may expand the project data model significantly.

## Out of Scope

- Cross-company project sharing or federation.
- Project-level access control lists beyond company scoping (deferred to Pro/Enterprise).
