---
title: "Team Catalog"
status: done
session_link: "reverse-engineered during sync (no session)"
---

# Test Plan: Team Catalog

## Scope

Catalog listing, template installation, shipped-catalog integrity, and the React catalog page are covered by existing server, package, and UI tests.
Out of scope: community marketplace flows, which the spec defers.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Catalog service lists templates and installs into company | Template id and target company | Agents created; created count and errors reported (server/src/__tests__/teams-catalog-service.test.ts, 24 cases) |
| TC-2 | Catalog routes enforce access and report install results | List/install requests | 200 with templates/results; 403/404 otherwise (server/src/__tests__/teams-catalog-routes.test.ts, 8 cases) |
| TC-3 | Install without overrides respects governance settings | Template with governance constraints | Correct agent creation under policy (server/src/__tests__/teams-catalog-install-no-overrides.test.ts, 4 cases) |
| TC-4 | Catalog builder produces valid manifest | Catalog source files | Valid generated catalog.json (packages/teams-catalog/src/catalog-builder.test.ts, 3 cases) |
| TC-5 | Shipped catalog integrity holds | Bundled templates | All templates validate (packages/teams-catalog/src/shipped-catalog.test.ts, 8 cases) |
| TC-6 | Catalog page renders templates and install flow | Mocked catalog payload | Browse/preview/install works (ui/src/pages/TeamCatalog.test.tsx, 8 cases) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Installed agents carry roles, reporting structure, adapter configs, skills | Template with full agent definitions | Agents created with correct org tree and configs |

## End-to-End Tests

None automated for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Partial install failure | Per-agent errors reported; rollback semantics per service behavior |
| TC-9 | Skill reference missing in target company | Error surfaced in install errors array |

## Test Infrastructure

- Existing vitest suites in server/src/__tests__, packages/teams-catalog/src, and ui/src/pages.
- No dedicated DB tables; templates load from packages/teams-catalog/catalog and generated/catalog.json.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-2, TC-5, TC-6 |
| FR-02 | TC-5, TC-7 |
| FR-03 | TC-1, TC-3, TC-7 |
| FR-04 | TC-2, TC-6 (search/filter via list endpoint and page) |
| FR-05 | TC-1, TC-8 |
| NFR-01 | Gap: install latency not explicitly asserted |
