---
title: "Inbox"
status: done
session_link: "reverse-engineered during sync (no session)"
---

# Test Plan: Inbox

## Scope

Inbox dismissal API, attention aggregation, and React inbox views are covered by existing server and UI tests.
Out of scope: p95 latency benchmarking (NFR-01) and push-style live updates, which the spec defers.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Inbox dismissal CRUD is company-scoped per user | Dismissal create/list/delete calls | Correct scoping and persistence (server/src/__tests__/inbox-dismissals.test.ts, 3 cases) |
| TC-2 | Attention service aggregates items needing attention | Seeded issues/activity | Correct attention items (server/src/__tests__/attention-service.test.ts, 27 cases) |
| TC-3 | Inbox page renders views and dismissal flows | Mocked inbox payloads | Views render; filters and dismissals work (ui/src/pages/Inbox.test.tsx, 27 cases) |
| TC-4 | WhatNeedsMe view surfaces actionable items | Mocked payload | Items listed correctly (ui/src/pages/WhatNeedsMe.test.tsx, 3 cases) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Dismissal and read-state tables join correctly with issue queries | Seeded inbox_dismissals, issue_read_states, issue_inbox_archives | Dismissed/archived items filtered; unread distinguished |

## End-to-End Tests

None automated for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Dismissal of nonexistent issue | 404 NOT_FOUND |
| TC-7 | Cross-company inbox access | 403 UNAUTHORIZED |

## Test Infrastructure

- Existing vitest suites in server/src/__tests__ and ui/src/pages.
- Schema tables inbox_dismissals, issue_read_states, issue_inbox_archives exist in packages/db/src/schema.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-2, TC-3 |
| FR-02 | TC-3, TC-5 |
| FR-03 | TC-2, TC-4 |
| FR-04 | TC-2 (join request queue surfaced via attention/inbox paths) |
| FR-05 | TC-1, TC-3 |
| FR-06 | TC-3 |
| FR-07 | TC-1, TC-5 |
| NFR-01 | Gap: no automated p95 perf test |
| NFR-02 | Gap: live-update behavior not asserted |
