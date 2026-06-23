---
title: "Workspaces & Runtime"
status: draft
---

# Specification: Workspaces & Runtime

## Overview

Workspaces split into project workspaces (shared project state) and execution workspaces (isolated git worktrees per run). Runtime services run dev servers/preview URLs; environments bind secret-aware env to execution targets via leases. Workspace operations expose commands, diffs, and uploads to agents under authorization.

## Architecture

```
Issue (execution_workspace_*) ──► execution_workspaces (git worktree)
                                          │
Project workspace ──────────► project_workspaces
Environments (secret-aware env) ──► environment_leases ──► execution target
Runtime services ──► workspace_runtime_services (dev servers, preview URLs)
Workspace operations ──► commands, diffs, uploads (authz-gated)
```

## Data Models

### execution_workspaces / project_workspaces / workspace_runtime_services / workspace_operations / environments / environment_leases

| Field | Type | Constraints | Description |
|---|---|---|---|
| execution_workspaces.id / company_id | uuid | FK, not null | Scoping |
| issues.execution_workspace_id/preference/settings | - | - | Per-issue workspace resolution |
| environments | - | - | Secret-aware env binding |
| environment_leases | - | - | Env-to-target leases |

## API Contracts

### /api/execution-workspaces, environment-selection, environments, workspace-command-authz, workspace-runtime-service-authz

Workspace/runtime management and authorization. Routes under `server/src/routes/`, services under `server/src/services/execution-workspaces.ts`, `environments.ts`, etc.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Command not authorized for this workspace/agent |

## Sequences

### Execution workspace checkout

```
checkout → resolve execution_workspace (preference/settings) → create/reuse worktree (base origin/master) → run agent → operations/diffs/uploads (authz)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Isolation | Git worktrees per execution | Reproducible, isolated agent working directories |

## Risks and Unknowns

1. Sandbox provider lease reuse (e.g. Daytona) and large-upload reliability need careful handling.

## Out of Scope

- Cloud sandbox marketplaces beyond supported providers.
