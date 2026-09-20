---
title: "Telemetry Contracts"
status: done
session_link: "none"
---

# Test Plan: Telemetry Contracts

## Scope

This plan covers unit behavior in telemetry.test.ts and adapter conformance in conformance.test.ts.
Package-level behavior is verified with vitest from the telemetry package directory.
External backend exporters remain out of scope for this plan.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Schema definition preserves identity and infers exact attributes | Serializable definition with closed string sets | Same object reference with JSON round-trip and exact kind union |
| TC-2 | Combined vocabularies bind child starters and preserve parentage | Operation and request schemas with nested typed starter calls | Child span records parent identifier and result value passes through |
| TC-3 | Noop context admits callbacks synchronously with one frozen span | Named span with nested child callback | Synchronous admission with identical child span and frozen parent span |
| TC-4 | Noop and typed starters preserve rejection identity | Callbacks that throw synchronously or reject asynchronously | Promises rejected with the identical thrown or rejected value |
| TC-5 | Recording ignores unreadable payloads without throwing | Proxy payloads that throw on property reads | Business callback still runs exactly once without exceptions |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Conformance callback lifecycle preserves results and errors | Fresh in-memory context per case | Single synchronous admission with ok status and identical rejection values |
| TC-7 | Conformance status keeps last explicit write | Spans with explicit ok or error before return or throw | Final status matches the last explicit write without automatic overwrite |
| TC-8 | Conformance recording merges attributes and orders events | Start attributes plus repeated setAttributes and two events | Merged bag with last-defined wins and ordered event list |
| TC-9 | Conformance atomicity ignores failed recording calls | Attributes containing unreadable values | Prior attributes retained with no partial merge and no throw |
| TC-10 | Conformance settlement makes late calls inert | Captured span used after its callback returned | Late mutations ignored while late child span still executes normally |
| TC-11 | Conformance parentage tracks nested and concurrent children | Overlapping first and second child spans under one parent | Correct parent identifiers with ordered end sequences |
| TC-12 | Conformance passivity suppresses backend payload failures | Unreadable span options and recording payloads | Business callbacks execute once with empty or retained snapshots |
| TC-13 | Snapshot isolation detaches recorded state | Open span observed mid-callback plus later external mutation | Open snapshot unsettled without end sequence and later reads unaffected by mutation |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-14 | Package-level span flow exercises start through settlement | Start span then add event then set attributes then set status then resolve | Settled snapshot contains merged attributes and ordered events and final status |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-15 | Synchronous throw inside callback | Span settles as error and promise rejects with identical value |
| TC-16 | Asynchronous rejection inside callback | Span settles as error and rejection value is preserved |
| TC-17 | Explicit ok status before a throw | Explicit status survives without automatic overwrite |
| TC-18 | Child started from settled parent | Call degrades to noop semantics while still executing the callback |
| TC-19 | Undefined attribute values in merges | Undefined entries are ignored without removing prior values |

## Test Infrastructure

- Vitest runs the telemetry package suite from the package directory.
- In-memory contexts isolate each test without shared global state.
- Proxy-based unreadable payloads verify passive non-throwing behavior.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-4, TC-6 |
| FR-2 | TC-8, TC-9, TC-19 |
| FR-3 | TC-8, TC-13 |
| FR-4 | TC-7, TC-14, TC-17 |
| FR-5 | TC-4, TC-6, TC-15, TC-16 |
| FR-6 | TC-3, TC-4, TC-5 |
| FR-7 | TC-11, TC-12, TC-13, TC-18 |
| FR-8 | TC-1, TC-2 |
| FR-9 | TC-2, TC-11 |
| NFR-1 | TC-5, TC-9, TC-12 |
| NFR-2 | TC-2, TC-6 |
| NFR-3 | TC-3 |
| NFR-4 | TC-5, TC-8 |
