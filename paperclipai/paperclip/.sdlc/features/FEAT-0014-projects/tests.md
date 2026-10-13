---
title: "Projects"
status: done
session_link: "reverse-engineered during sync 2026-10-13"
---

# Test Plan: Projects

## Scope

Covers project CRUD, status lifecycle, goal linkage, workspaces, runtime services, env config, memberships, and budget summaries.
Out of scope: cross-company sharing and project-level ACLs beyond company scoping (per specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Project list metrics | Company project query | Correct counts and aggregates (`server/src/__tests__/project-list-metrics.test.ts`) |
| TC-2 | Project repositories persistence | Workspace repo config | Repo URL and refs stored (`server/src/__tests__/project-repositories-persistence.test.ts`) |
| TC-3 | Project icon persistence | Icon update | Icon stored and returned (`server/src/__tests__/project-icon-persistence.test.ts`) |
| TC-4 | Project shortname resolution | Shortname lookup | Correct project resolved (`server/src/__tests__/project-shortname-resolution.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Project env routes | Project with env config | Env overlay resolved per company scope (`server/src/__tests__/project-routes-env.test.ts`) |
| TC-6 | Project workspace routes | Project workspace | CRUD succeeds (`server/src/__tests__/project-workspace-managed-sandbox-routes.test.ts`) |
| TC-7 | Archived projects listing | Archived project | Listed under archived filter (`server/src/__tests__/projects-list-archived-routes.test.ts`) |
| TC-8 | Heartbeat project env | Agent heartbeat in project | Project env injected (`server/src/__tests__/heartbeat-project-env.test.ts`) |
| TC-9 | Heartbeat referenced projects | Issue with project_id | Project context resolved (`server/src/__tests__/heartbeat-referenced-projects.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-10 | Create project with workspace | POST project, POST workspace with repo URL and CWD, assign issue | Agent executes in workspace context |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Invalid status transition | 400 INVALID_INPUT returned |
| TC-12 | Cross-company project access | 403/404 rejection |

## Test Infrastructure

- Vitest suites under `server/src/__tests__/`.
- Seeded companies, projects, workspaces, and runtime service configs.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-4, TC-7 |
| FR-02 | TC-7, TC-11 |
| FR-03 | TC-5 |
| FR-04 | TC-2, TC-6, TC-10 |
| FR-05 | TC-6, TC-10 |
| FR-06 | TC-1 |
| FR-07 | TC-6 |
| FR-08 | TC-5, TC-8 |
| FR-09 | TC-1 |
| NFR-01 | TC-5, TC-6 |
| NFR-02 | TC-5, TC-12 |
