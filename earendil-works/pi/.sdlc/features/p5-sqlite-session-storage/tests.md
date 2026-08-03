---
title: "SQLite Session Storage"
status: done
---

# Test Plan: SQLite Session Storage

## Scope

Tests cover migrations, the SQLite session repository, branch-cache behavior, search queries, and backend equivalence against the agent session contract.
Tests live in `packages/agent/test/harness/` because the package itself carries no test files.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Migrations apply idempotently and in order | Fresh database, then reopen | `001_initial` + `002_branch_tips` applied once |
| TC-2 | Repository create/open persists sessions | `create({ cwd })` | Session persisted and reopenable |
| TC-3 | Branch-cache materialization tracks branch tips | Branching operations | Tips maintained correctly |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | SQLite backend matches the session-backend contract | Harness driving the repo | Same observable behavior as the contract |
| TC-5 | Branch queries over SQLite return correct branch data | Sessions with branches | Correct branch results |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Reopen an already-migrated database | No re-migration, no error |
| TC-7 | Search over sessions with no FTS content | Empty result set, no crash |

## Test Infrastructure

- Ran with Vitest from `packages/agent/test/harness/`:
  - `sqlite-migrations.test.ts`, `sqlite-branch-cache.test.ts`, `sqlite-node.test.ts`, `branch-query.test.ts`, `session-backends.test.ts`.
- Requires Node `>=22.19.0` for `node:sqlite`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-4 |
| FR-02 | TC-2, TC-4 |
| FR-03 | TC-2 |
| FR-04 | TC-1, TC-6 |
| FR-05 | TC-3 |
| FR-06 | TC-7 |
| NFR-01 | TC-1, TC-6 |
