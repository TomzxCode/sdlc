---
title: "Company Management & Multi-Tenancy"
status: done
session_link: "—"
---

# Test Plan: Company Management & Multi-Tenancy

## Scope

Company lifecycle CRUD, per-company isolation boundaries, branding, and export/import portability are covered by route and service tests.
Out of scope: cloud-grade multi-tenant infra (explicitly out of scope in specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Company service CRUD and status transitions | Create/update/archive payloads | Company rows with correct status, prefix, counter (`server/src/__tests__/companies-service.test.ts`) |
| TC-2 | Quota windows per company | Company quota config | Correct quota enforcement (`server/src/__tests__/company-quota-windows.test.ts`) |
| TC-3 | Company artifacts service | Artifact payloads | Artifacts scoped to company (`server/src/__tests__/company-artifacts-service.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Cross-company authz rejection | Two companies, agent key scoped to A | B-scoped reads/writes rejected (`server/src/__tests__/companies-route-cross-company-authz.test.ts`) |
| TC-5 | Company route path guard | Board vs agent actors | Correct actor gating (`server/src/__tests__/companies-route-path-guard.test.ts`) |
| TC-6 | Company branding routes | Board operator, branding payload | Brand fields persisted (`server/src/__tests__/company-branding-route.test.ts`) |
| TC-7 | Portability export/import round-trip | Exported company package | Agents, skills, projects, routines, issues recreated with secrets scrubbed (`server/src/__tests__/company-portability.test.ts`) |
| TC-8 | Portability route preview/apply | Portable package upload | Preview and apply endpoints behave (`server/src/__tests__/company-portability-routes.test.ts`) |
| TC-9 | Import batching and transfers | Large company package | Batched import and transfer runs (`server/src/__tests__/company-portability-import-batching.test.ts`, `server/src/__tests__/company-import-transfer-routes.test.ts`, `server/src/__tests__/company-transfer-runs.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-10 | Import cloud floor guard | Import into fresh deployment | Import succeeds within floor limits (`server/src/__tests__/company-import-cloud-floor.test.ts`) |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Agent key for company A calls company B endpoint | Denied before any B data is exposed (NFR-01) |
| TC-12 | Pause reason tracking | Pause with reason sets `status=paused`, `paused_at`, reason |

## Test Infrastructure

- Vitest suite (`pnpm test`); PGlite-backed dev DB.
- Fixtures for multi-company isolation in cross-company authz tests.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-4 |
| FR-03 | TC-1 |
| FR-04 | TC-12 |
| FR-05 | TC-6 |
| FR-06 | TC-7, TC-8, TC-9, TC-10 |
| FR-07 | TC-2 (related: quota/size policy surface) |
| NFR-01 | TC-4, TC-11 |
| NFR-02 | Activity-log assertions in service/route tests |
