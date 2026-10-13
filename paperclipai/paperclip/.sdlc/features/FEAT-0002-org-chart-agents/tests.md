---
title: "Org Chart & Agents"
status: done
session_link: "—"
---

# Test Plan: Org Chart & Agents

## Scope

Agent lifecycle (hire, pause/resume/terminate), strict-tree org graph, hashed API keys, hire approval flow, and adapter validation are covered by module and route tests.
Out of scope: multi-board governance / human RBAC granularity.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Agent lifecycle state machine | Hire/pause/resume/terminate transitions | Correct statuses, `terminated` irreversible (`server/src/modules/agent-lifecycle/__tests__/lifecycle.test.ts`) |
| TC-2 | Lifecycle policy sweep | Policy inputs | Enforcement decisions (`server/src/modules/agent-lifecycle/__tests__/policy-sweep.test.ts`) |
| TC-3 | Lifecycle diagnostics | Diagnostic inputs | Correct diagnostic output (`server/src/modules/agent-lifecycle/__tests__/diagnostics.test.ts`) |
| TC-4 | Agent invokability rules | Agent state | Invokable/not-invokable verdicts (`server/src/__tests__/agent-invokability.test.ts`) |
| TC-5 | Agent identity (key hashing) | New API key request | Only hash persisted, plaintext once (`server/src/__tests__/agent-identity.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Hire idempotency routes | Duplicate hire requests | Single agent created (`server/src/__tests__/agent-hire-idempotency-routes.test.ts`) |
| TC-7 | Hire auth inheritance | Hiring agent context | Correct inherited auth (`server/src/__tests__/agent-hire-auth-inheritance-routes.test.ts`) |
| TC-8 | Adapter validation routes | Adapter type/config payloads | Valid configs accepted, invalid rejected (`server/src/__tests__/agent-adapter-validation-routes.test.ts`) |
| TC-9 | Pending-approval agent config | `pending_approval` agent | Config gating holds (`server/src/__tests__/agents-pending-approval-config.test.ts`) |
| TC-10 | Cross-tenant authz | Agent key, foreign company agent | Rejected (`server/src/__tests__/agent-cross-tenant-authz-routes.test.ts`) |
| TC-11 | Agent secret bindings | Agent + secret bindings | Bindings resolve per service (`server/src/__tests__/agents-service-secret-bindings.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-12 | Hire via approval flow | Agent requests hire, board approves | Agent row + optional key created, activity logged |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Cycle-creating `reports_to` | Rejected `422`/`409`, tree stays acyclic |
| TC-14 | Resume a `terminated` agent | Rejected per transition rules |

## Test Infrastructure

- Vitest suite; agent-lifecycle module tests plus route-level tests.
- `doc/AGENT-LIFECYCLE.md` documents lifecycle semantics.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-6, TC-7 |
| FR-02 | TC-1, TC-13 |
| FR-03 | TC-1, TC-2 |
| FR-04 | TC-14 |
| FR-05 | TC-5 |
| FR-06 | TC-1 |
| FR-07 | TC-9, TC-12 |
| FR-08 | TC-8 |
| FR-09 | TC-4 |
| NFR-01 | TC-5 |
| NFR-02 | Activity-log assertions in lifecycle/route tests |
