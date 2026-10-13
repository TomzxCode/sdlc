---
title: "Workspaces & Runtime"
status: done
session_link: "reverse-engineered during 2026-10-13 sync; no live session"
---

# Test Plan: Workspaces & Runtime

## Scope

Covers project and execution workspaces, per-issue workspace resolution, workspace operations (commands, diffs, uploads, git publishing), runtime services lifecycle, environments with secret-aware bindings and leases, and command authz.
Out of scope: cloud sandbox marketplaces beyond supported providers.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Execution workspaces service (`server/src/__tests__/execution-workspaces-service.test.ts`) | Issue with workspace preference/settings | Isolated worktree resolved or created on origin/master base |
| TC-2 | Execution workspace policy (`server/src/__tests__/execution-workspace-policy.test.ts`) | Policy inputs | Expected allow/deny decisions |
| TC-3 | Managed environments (`server/src/services/managed-environments.test.ts`) | Managed config env | Environments applied per config |
| TC-4 | Workspace runtime exposure (`server/src/services/workspace-runtime-exposure.test.ts`) | Runtime exposure inputs | Correct port derivation and exposure behavior |
| TC-5 | Workspace runtime read model (`server/src/services/workspace-runtime-read-model.test.ts`) | Runtime state | Correct read-model projection |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Execution workspaces routes (`server/src/__tests__/execution-workspaces-routes.test.ts`) | Authenticated company context | Workspace management endpoints behave per contract |
| TC-7 | Workspace runtime services (`server/src/__tests__/workspace-runtime.test.ts`) | Workspace with runtime service | Dev server/preview lifecycle transitions succeed |
| TC-8 | Environment service and runtime (`server/src/__tests__/environment-service.test.ts`, `server/src/__tests__/environment-runtime.test.ts`) | Environment with bindings | Env binds to execution target via leases |
| TC-9 | Workspace command authz (`server/src/__tests__/workspace-command-authz.test.ts`, `server/src/__tests__/issue-workspace-command-authz.test.ts`) | Agent command on a workspace | Unauthorized commands rejected with 403 |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-10 | Agent checkout flow (`server/src/__tests__/execution-workspace-reopen.test.ts`) | Agent checks out issue with preference | Execution workspace resolved, agent runs, diffs/uploads succeed |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Large uploads and git publishing | Succeed without truncation |
| TC-12 | Command outside workspace/agent scope | 403 UNAUTHORIZED |

## Test Infrastructure

- Vitest suite under `server/src/__tests__/` and `server/src/services/`.
- Git worktree fixtures and sandbox lease doubles.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-6, TC-10 |
| FR-02 | TC-9, TC-11 |
| FR-03 | TC-1, TC-10 |
| FR-04 | TC-4, TC-5, TC-7 |
| FR-05 | TC-3, TC-8 |
| FR-06 | TC-1 |
| NFR-01 | TC-9, TC-12 |
| NFR-02 | TC-11 |
