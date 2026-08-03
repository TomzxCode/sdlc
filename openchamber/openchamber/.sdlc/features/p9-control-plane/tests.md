---
title: "Control Plane and Agent Tool"
status: done
---

# Test Plan: Control Plane and Agent Tool

## Scope

Tests cover the shared control service action allowlist and validation, the CLI HTTP adapter, the managed agent-tool adapter, and the CLI `control` command.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Service validates actions against the allowlist | In-scope and out-of-scope action names | In-scope executes; out-of-scope rejected |
| TC-2 | CLI-only actions are excluded from agent exposure | Allowlist scan | `schedule.status` marked `agentExposed: false` |
| TC-3 | Wait does not treat initial idle response as completion | Fresh dispatch, no activity | Wait continues / times out rather than completing |
| TC-4 | One failed directory lookup yields `unknown` only for it | Multi-directory status | Others return normally, failing one is `unknown` |
| TC-5 | Explicit scope takes precedence over the managed fallback | Explicit projectId + fallback present | Explicit scope used |
| TC-6 | Send/fork reuse last user-message model selection | Session with prior selection | Selection reused; defaults only when none |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | CLI adapter forwards one action over HTTP | Server running, authenticated | Action executed, status + partial details preserved |
| TC-8 | Agent-tool route wraps results in the native-tool envelope | Managed tool calls back | Versioned envelope returned |
| TC-9 | Request cancellation propagates | Long-running wait action | Cancellation reaches the service |
| TC-10 | CLI `control` command drives a session dispatch | `openchamber control` installed | Dispatch, wait, and status work end to end |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Timeout during wait | Reported as failure, never authoritative idle result |
| TC-12 | Invalid/conflicting input | Usage error naming the missing or conflicting input |
| TC-13 | Unauthenticated CLI request | Rejected by auth |
| TC-14 | `agentControlToolEnabled: false` | Tool not injected into the managed OpenCode environment |

## Test Infrastructure

- `packages/web/server/lib/openchamber-control/service.test.js`, `routes.test.js`
- `packages/web/server/lib/agent-tool/runtime.test.js`
- `packages/web/bin/lib/cli-control.test.js`
- Mocks for session and scheduled-task domain modules; ephemeral loopback credentials in tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-7, TC-8 |
| FR-3 | TC-10 |
| FR-4 | TC-3, TC-11 |
| FR-5 | TC-6, TC-10 |
| FR-6 | TC-4 |
| FR-7 | TC-1 |
| FR-8 | TC-5 |
| FR-9 | TC-2 |
| FR-10 | TC-13, TC-14 |
| FR-11 | TC-9 |
| FR-12 | TC-14 |
| NFR-1 | TC-13, TC-14 |
| NFR-2 | TC-3, TC-11 |
| NFR-3 | TC-4 |
| NFR-4 | TC-12 |
