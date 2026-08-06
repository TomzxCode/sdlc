---
title: "Multi-Node Operator Surfaces & Shells"
status: done
---

# Test Plan: Multi-Node Operator Surfaces & Shells

## Scope

Covers project/node management, mesh coordination over shared PostgreSQL, shell onboarding and the shell bridge, and the CLI serve/daemon/dashboard/project/node/mesh surfaces.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Mesh task replication | task mutation | Replicated across nodes |
| TC-2 | Node route CRUD | node payload | Nodes created/updated |
| TC-3 | Project CRUD | project payload | Projects managed |
| TC-4 | Shell onboarding backcompat | legacy profile | Backcompat onboarding applied |
| TC-5 | ShellContext bridge | host type | Normalized shell host |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Scheduler node-unreachable audit | unreachable node | Claims audited, work preserved |
| TC-7 | Scheduler fanout escalation lanes | overloaded lane | Escalation applied |
| TC-8 | Shell onboarding E2E | fresh device | Onboard via profile |
| TC-9 | Node/project API integration | live server | Routes serve data |
| TC-10 | CLI serve/daemon/dashboard | CLI installed | Processes supervised |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Autolaunch bypass | Bypass respected |
| TC-12 | Node unreachable | Degrades gracefully |

## Test Infrastructure

- Vitest across core/engine/dashboard/CLI; Electron/Capacitor shell E2E where applicable

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2, TC-3, TC-9 |
| FR-2 | TC-1, TC-6 |
| FR-3 | TC-4, TC-5, TC-8 |
| FR-4 | TC-10 |
| NFR-1 | TC-6, TC-7 |

## Key Test Files

- `packages/core/src/__tests__/mesh-task-replication.test.ts`, project tests
- `packages/engine/src/__tests__/scheduler-node-unreachable-audit.test.ts`, `scheduler-fanout-escalation-lanes.test.ts`
- `packages/dashboard/src/routes/__tests__/register-node-routes.test.ts`, `api-node.test.ts`, `api-projects.test.ts`
- `packages/cli/src/commands/__tests__/node.test.ts`, `project.test.ts`, `serve.test.ts`, `daemon.test.ts`, `dashboard-supervise.test.ts`, `onboard-*.test.ts`
- `packages/dashboard/app/__tests__/App.shell-onboarding.test.tsx`, `ShellContext.test.tsx`