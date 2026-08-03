---
title: "Session Server"
status: done
---

# Test Plan: Session Server

## Scope

Tests cover server startup and listeners, protocol handling, live-session management, snapshot publication, Unix-socket connectivity, and a conformance suite exercising the server as a client would.
Legacy supervisor behavior is not covered here (separate feature, `p1-orchestrator`).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | LiveSessionManager creates and tracks sessions | Create/open requests | Sessions tracked; snapshots updated |
| TC-2 | Snapshot publication reflects authoritative state | State change on a live session | Subscribers receive new snapshot |
| TC-3 | Protocol routing handles client requests | Request envelopes | Correct responses routed |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Server starts and accepts Unix-socket connections | `createUnixServer` on a temp path | Connections accepted |
| TC-5 | End-to-end session create over Unix socket | Running server + client | Session created and snapshots flow |
| TC-6 | Conformance suite drives server as a client | `testing` harness | Behavior matches the protocol contract |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-7 | Connection with missing/invalid token | Rejected before session operations |
| TC-8 | Client disconnect mid-session | Live session cleaned up; server remains up |
| TC-9 | Concurrent client connections | Sessions isolated per client lease |

## Test Infrastructure

- `test/fixtures` provides shared setup.
- `testing/` entrypoint provides in-memory server/client harness.
- Ran with Vitest (`packages/server/test/`).

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-4, TC-5 |
| FR-02 | TC-7 |
| FR-03 | TC-4 |
| FR-04 | TC-1 |
| FR-05 | TC-2 |
| FR-06 | TC-3, TC-5 |
| FR-08 | TC-6 |
| NFR-02 | TC-8, TC-9 |
