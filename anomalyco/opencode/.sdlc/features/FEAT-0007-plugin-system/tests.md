---
title: "Plugin System"
status: done
---

# Test Plan: Plugin System

## Scope

Plugin SDK (`@opencode-ai/plugin`), hook registration, runtime registry, plugin lifecycle, provider and tool contributions.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Plugin SDK namespace hooks | Hook registration | Hook registered |
| TC-2 | Plugin readiness await | Plugin registration | Runtime resumes after ready |
| TC-3 | Provider integration via plugin | Plugin with provider | Provider available |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Plugin loading from config | Plugin configured in opencode.json | Plugin loaded, hooks active |
| TC-5 | Plugin tool contribution | Plugin registers tool | Tool available in registry |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Plugin fails to load | Plugin skipped, warning logged |
| TC-7 | Duplicate hook registration | Last registered wins |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-2, TC-4 |
| FR-03 | TC-3 |
| FR-05 | TC-5 |

## Test Files

- `packages/core/test/plugin.test.ts`
- `packages/core/test/plugin/`
