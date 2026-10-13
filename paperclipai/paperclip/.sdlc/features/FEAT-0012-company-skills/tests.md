---
title: "Company Skills"
status: done
session_link: "reverse-engineered during sync 2026-10-13"
---

# Test Plan: Company Skills

## Scope

Covers skills catalog browsing, company installation with version pinning, agent/team assignment, runtime resolution at heartbeat, custom skills, and teams catalog.
Out of scope: public marketplace and skill dependency resolution (per specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Skills catalog service | Catalog query | Skills listed with name, description, version (`server/src/__tests__/skills-catalog-service.test.ts`) |
| TC-2 | Company skills catalog service | Company-scoped catalog query | Correct per-company view (`server/src/__tests__/company-skills-catalog-service.test.ts`) |
| TC-3 | Company skills service | Install/update/remove skill | company_skills rows managed (`server/src/__tests__/company-skills-service.test.ts`) |
| TC-4 | Skill policy service | Policy evaluation input | Allow/deny per policy (`server/src/__tests__/company-skill-policy-service.test.ts`) |
| TC-5 | Runtime skill cache | Heartbeat skill resolution | Only assigned skills injected (`server/src/__tests__/runtime-skill-cache.test.ts`) |
| TC-6 | Skill repository package | Package build input | Valid skill bundle (`server/src/__tests__/skill-repository-package.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Company skills routes | Installed skill | CRUD via API succeeds (`server/src/__tests__/company-skills-routes.test.ts`) |
| TC-8 | Skill import authz routes | Import request | Permission-gated import (`server/src/__tests__/company-skills-import-authz-routes.test.ts`) |
| TC-9 | Heartbeat runtime skills | Assigned skills on agent | Skills present in heartbeat context (`server/src/__tests__/heartbeat-runtime-skills.test.ts`) |
| TC-10 | Teams catalog service | Team template query | Templates with bundled skills returned (`server/src/__tests__/teams-catalog-service.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-11 | Install and assign skill | Browse catalog, install with pinned version, assign to agent, run heartbeat | Agent executes with skill capabilities |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-12 | Invalid skill reference or version | 400 INVALID_INPUT returned |
| TC-13 | Unknown catalog skill | 404 NOT_FOUND returned |

## Test Infrastructure

- Vitest suites under `server/src/__tests__/` and `server/src/services/`.
- Seeded catalog entries, company_skills rows, and agent assignments.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2 |
| FR-02 | TC-3, TC-7 |
| FR-03 | TC-9, TC-11 |
| FR-04 | TC-1 |
| FR-05 | TC-8 |
| FR-06 | TC-3 |
| FR-07 | TC-10 |
| FR-08 | TC-5, TC-9 |
