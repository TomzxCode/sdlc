---
title: "Model Picker"
status: done
---

# Test Plan: Model Picker

## Scope

Tests cover the model display naming logic used by the model picker, including humanization of model ids and fallback derivation when provider data is unavailable.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Prefers the model name over the model id | Model with both id and name | Display uses the model name |
| TC-2 | Falls back to a human-readable model id when name is missing | Model with id only | Human-readable model id shown |
| TC-3 | Falls back to a human-readable explicit model id when provider data is unavailable | Undefined provider, explicit model id | Human-readable model id shown |
| TC-4 | Uses the fallback label only when no model id is available | No provider, no model id, fallback label | Fallback label shown |
| TC-5 | Supports provider model records and truncation | Provider record with long model name | Name truncated to the max length |
| TC-6 | Humanizes provider-prefixed model ids using common model catalog patterns | `anthropic/claude-opus-4-7-fast`, `google/gemini-3.1-flash-lite-preview`, etc. | Correct humanized display strings |
| TC-7 | Humanizes alias and custom model ids without provider data | Alias or custom model id | Correct humanized display string |

## Test Files

- `packages/ui/src/lib/modelDisplay.test.ts`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 (models grouped by provider) | TC-6 |
| FR-05 (search/filter across all models) | TC-1, TC-2, TC-3, TC-6 |
| FR-08 (display model cost indicators and capability icons) | TC-1, TC-2, TC-5 |
| FR-09 (fallback derivation from provider data) | TC-3, TC-4, TC-7 |