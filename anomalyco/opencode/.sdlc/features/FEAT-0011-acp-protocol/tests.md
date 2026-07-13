---
title: "Agent Client Protocol (ACP)"
status: done
---

# Test Plan: Agent Client Protocol (ACP)

## Scope

ACP agent lifecycle, tool dispatch, session management, permission model, and event streaming.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | ACP agent lifecycle | Create agent | Agent registered |
| TC-2 | ACP tool dispatch | Tool call request | Tool executed |
| TC-3 | ACP session management | Session CRUD | Session handled |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | ACP event streaming | Event subscription | Events received |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-2 |
| FR-03 | TC-3 |
| NFR-01 | TC-4 |

## Test Files

- `packages/opencode/test/acp/` (agent, event, session, tool tests)
