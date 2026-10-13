---
title: "Activity Audit Log"
status: done
session_link: "reverse-engineered during sync 2026-10-13"
---

# Test Plan: Activity Audit Log

## Scope

Covers append-only activity writes on mutation, paginated filtered queries, actor/entity/action filters, and audit UI surfaces.
Out of scope: tamper-evident hashing chains and real-time event streaming (per specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Activity service log | Mutation event | activity_log row with actor, action, entity, details (`server/src/__tests__/activity-service.test.ts`) |
| TC-2 | Responsible-user attribution | Mutation with responsible user | Correct actor recorded (`server/src/__tests__/activity-log-responsible-user.test.ts`) |
| TC-3 | Credential access activity | Credential mutation | Audit entry with origin context (`server/src/__tests__/activity-credential-access.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Activity routes pagination | Company with 100+ entries | Paginated newest-first results (`server/src/__tests__/activity-routes.test.ts`) |
| TC-5 | Activity filters | Entries across actors/entities/actions | Correct filtered subsets (`server/src/__tests__/activity-routes.test.ts`) |
| TC-6 | Issue activity events routes | Issue mutations | Per-issue event stream returned (`server/src/__tests__/issue-activity-events-routes.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-7 | Mutation audit trail | Create agent, update issue status, approve request | Each mutation has a matching activity_log row |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | UPDATE or DELETE on entry | Operation rejected, table stays append-only |
| TC-9 | Cross-company activity query | 403 rejection, no leakage |

## Test Infrastructure

- Vitest suites under `server/src/__tests__/`.
- Companies seeded with high-volume activity entries for pagination checks.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2, TC-7 |
| FR-02 | TC-4 |
| FR-03 | TC-5 |
| FR-04 | TC-8 |
| FR-05 | TC-6 |
| FR-06 | TC-3 |
| NFR-02 | TC-8 |
