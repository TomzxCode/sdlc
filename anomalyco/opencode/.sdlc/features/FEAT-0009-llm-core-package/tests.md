---
title: "LLM Core Package"
status: done
---

# Test Plan: LLM Core Package

## Scope

Effect Schema-first LLM core: route/protocol/endpoint/auth architecture, provider adapters, tool dispatch, and recorded provider interaction tests.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Route construction | Route config | Route valid |
| TC-2 | Auth header generation | Auth config | Correct header |
| TC-3 | Endpoint URL resolution | Endpoint config | URL correct |
| TC-4 | Schema validation | Message data | Schema passes |
| TC-5 | Tool schema projection | Tool schema | Projected correctly |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Protocol adapter execution | Provider + message | Response received |
| TC-7 | Recorded provider test | Recorded HTTP fixture | Deterministic response |
| TC-8 | Tool runtime dispatch | Tool call | Tool executed |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | Provider authentication failure | AuthError returned |
| TC-10 | Response parsing error | ParseError with context |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-3 |
| FR-02 | TC-2, TC-4 |
| FR-03 | TC-6 |
| FR-04 | TC-5 |
| NFR-01 | TC-7 |

## Test Files

- `packages/llm/test/route.test.ts`
- `packages/llm/test/endpoint.test.ts`
- `packages/llm/test/auth.test.ts`
- `packages/llm/test/executor.test.ts`
- `packages/llm/test/schema.test.ts`
- `packages/llm/test/llm.test.ts`
- `packages/llm/test/response.test.ts`
- `packages/llm/test/prepare.test.ts`
- `packages/llm/test/adapter.test.ts`
- `packages/llm/test/generate-object.test.ts`
- `packages/llm/test/tool-runtime.test.ts`
- `packages/llm/test/tool-stream.test.ts`
- `packages/llm/test/tool-schema-projection.test.ts`
- `packages/llm/test/provider-error.test.ts`
- `packages/llm/test/cache-policy.test.ts`
- `packages/llm/test/exports.test.ts`
- `packages/llm/test/provider/` (various provider test files)
- `packages/llm/test/recorded-*.ts` (recorded cassette tests)
