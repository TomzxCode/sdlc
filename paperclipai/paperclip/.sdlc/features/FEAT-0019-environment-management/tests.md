---
title: "Environment Management"
status: done
session_link: "reverse-engineered during sync (no session)"
---

# Test Plan: Environment Management

## Scope

Environment CRUD, lease lifecycle, runtime overlay resolution, and the React environments page are covered by extensive existing tests.
Out of scope: custom-image provisioning flows and sandbox driver specifics, which belong to adjacent features.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Environment CRUD is company-scoped | Create/update/delete calls | Scoped persistence; 403/404 otherwise (server/src/__tests__/environment-routes.test.ts, 87 cases) |
| TC-2 | Runtime overlay resolves project, environment, routine, runtime keys in order | Layered env definitions with secret refs | Correct precedence; secrets resolved at runtime (server/src/__tests__/environment-runtime.test.ts, 84 cases) |
| TC-3 | Environments page renders and manages configs | Mocked environments payload | List/edit flows work (ui/src/pages/CompanyEnvironments.test.tsx, 32 cases) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Lease creation grants agent runtime access | Existing environment and agent | Lease row created; heartbeat injects resolved vars |
| TC-5 | Lease expiry and release handling | Expired or released lease | Access revoked; mid-execution semantics per service behavior |

## End-to-End Tests

None automated for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Secret ref syntax stored unresolved | Definition read returns `${{ secrets.key }}`, not plaintext (NFR-01) |
| TC-7 | Invalid environment config | 400 INVALID_INPUT |

## Test Infrastructure

- Existing vitest suites in server/src/__tests__ and ui/src/pages.
- Schema tables environments and environment_leases exist in packages/db/src/schema.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-3 |
| FR-02 | TC-2, TC-6 |
| FR-03 | TC-4, TC-5 |
| FR-04 | TC-4 (selection flow via environment-selection route) |
| FR-05 | TC-2 |
| NFR-01 | TC-2, TC-6 |
| NFR-02 | Gap: activity-log emission for lease creation not explicitly asserted |

Note: feature directory title mentions slots, but requirements/spec cover environments and leases only.
Summary-slot routes (server/src/routes/summary-slots.ts) are a separate concern and are not claimed here.
