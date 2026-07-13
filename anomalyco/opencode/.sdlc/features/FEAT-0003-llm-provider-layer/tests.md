---
title: "LLM Provider Layer"
status: done
---

# Test Plan: LLM Provider Layer

## Scope

Model catalog resolution, provider protocol adaptation, model request options, generation controls, and models.dev data-driven provider support.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Catalog resolves model from provider ID | Provider + model name | Model config returned |
| TC-2 | Model request options partitioned correctly | Provider options | Options split into semantic/control/wire |
| TC-3 | Provider adapter selection | Provider type | Correct protocol adapter used |
| TC-4 | models.dev metadata parsed | models.dev JSON | Provider/model entries created |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Provider call completes successfully | Valid provider config | Response received |
| TC-6 | Provider call with streaming | Streaming enabled | Chunks received in order |
| TC-7 | Provider error handling | Invalid API key | ProviderError returned, session continues |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Unknown model requested | CatalogError with suggestion |
| TC-9 | Provider timeout | Timeout returned gracefully |
| TC-10 | Rate limited provider | Backoff or error propagated |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-4 |
| FR-02 | TC-2 |
| FR-03 | TC-3 |
| FR-04 | TC-5 |
| NFR-01 | TC-9, TC-10 |

## Test Files

- `packages/core/test/model.test.ts`
- `packages/core/test/models.test.ts`
- `packages/core/test/provider-xai-responses.test.ts`
- `packages/core/test/catalog.test.ts`
