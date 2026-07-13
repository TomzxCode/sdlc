---
title: "HTTP API Server"
status: done
---

# Test Plan: HTTP API Server

## Scope

HTTP API route groups, server lifecycle, request routing, response formatting, client contract compliance.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Health endpoint returns OK | GET /health | 200 OK |
| TC-2 | Session CRUD routes | POST session | Session created |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-3 | Contract identity test | Server running | Client matches server routes |
| TC-4 | Message routes return { info, parts } | Message request | Correct projection |
| TC-5 | Project-scoped routing | Project context | Routes scoped |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Request to non-existent session | 404 with error body |
| TC-7 | Invalid request body | 400 validation error |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-5 |
| FR-03 | TC-2 |
| FR-04 | TC-4 |

## Test Files

- `packages/protocol/test/session-cursor.test.ts`
- `packages/client/test/contract-identity.test.ts`
- `packages/client/test/effect.test.ts`
- `packages/client/test/promise.test.ts`
- `packages/client/test/import-boundaries.test.ts`
- `packages/opencode/test/server/`
