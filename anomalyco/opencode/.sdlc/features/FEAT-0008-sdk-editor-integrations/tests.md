---
title: "SDK & Editor Integrations"
status: done
---

# Test Plan: SDK & Editor Integrations

## Scope

TypeScript SDK, VSCode extension, MCP server integration, client library, and SDK-next.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | SDK client methods match API | API call | Correct request sent |
| TC-2 | SDK-next composes client + core | Compound call | Both layers invoked |
| TC-3 | Client effect bindings | Effect API call | Effect executed |
| TC-4 | Client promise bindings | Promise API call | Promise resolved |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | SDK generated from server | Server running | SDK matches current routes |
| TC-6 | VSCode extension activation | Extension loaded | Commands registered |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-7 | Server unavailable | Error propagated to caller |
| TC-8 | API version mismatch | Compatibility error or graceful degradation |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-5 |
| FR-03 | TC-3, TC-4 |
| NFR-01 | TC-3, TC-4 |

## Test Files

- `packages/client/test/contract-identity.test.ts`
- `packages/client/test/effect.test.ts`
- `packages/client/test/promise.test.ts`
- `packages/client/test/import-boundaries.test.ts`
- `packages/sdk-next/test/`
