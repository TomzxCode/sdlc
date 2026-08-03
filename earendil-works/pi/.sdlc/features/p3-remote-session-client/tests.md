---
title: "Remote Session Client"
status: done
---

# Test Plan: Remote Session Client

## Scope

Tests cover connection lifecycle, session acquisition and ownership enforcement, request/response correlation, state transitions, and disposal semantics.
Transport-level integration uses a Unix-socket transport (`unix.ts`); core client logic is transport-neutral.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Connection establishes via `ByteTransportFactory` and authenticates | Valid factory + token | Client reaches connected/ready state |
| TC-2 | Ownership enforcement: exclusive then shared acquisition | Session with exclusive lease held | Shared acquisition throws `PiSessionOwnershipError` |
| TC-3 | Ownership enforcement: exclusive while a lease exists | Session with any lease held | Exclusive acquisition throws `PiSessionOwnershipError` |
| TC-4 | Request correlation delivers each response to its caller | Concurrent in-flight requests | Each caller receives its own response |
| TC-5 | State machine transitions on connect/close/error | Sequence of transport events | Correct state transitions |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Unix-socket transport end-to-end session create | Running server on a Unix socket | `createSession({ cwd })` returns an exclusive lease |
| TC-7 | Session subscribe/event delivery over the socket | Active session | Subscribers receive snapshots/events |
| TC-8 | Disposal releases leases and cleans up | Leases held | Disposal closes connection and releases resources |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | Transport factory returns a stale/closed transport | Fresh transport is created per attempt |
| TC-10 | Disconnection without explicit reconnect | Client surfaces failure; no auto-reconnect |
| TC-11 | Duplicate release of a lease | Release is idempotent, no double-free |

## Test Infrastructure

- `packages/client/test/support.ts` provides shared transport/test harness helpers.
- `test/unix.test.ts` exercises the concrete Unix-socket transport.
- Ran with Vitest.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-6 |
| FR-02 | TC-6 |
| FR-04 | TC-2, TC-3 |
| FR-05 | TC-2, TC-3 |
| FR-06 | TC-4 |
| FR-07 | TC-7 |
| NFR-02 | TC-9 |
| NFR-04 | TC-10 |
