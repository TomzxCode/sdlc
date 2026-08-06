---
title: "Harness API and SDKs"
status: done
---

# Test Plan: Harness API and SDKs

## Scope

Covers harness API framing, translation, Rust SDK behavior, TypeScript SDK behavior, and schema parity. Out of scope: live long-running sessions in CI (covered by scripted e2e suites).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Bridge framing | `crates/jcode-harness-api-server/src/framing_tests.rs` | Requests/events frame and unframe correctly |
| TC-2 | Bridge translation | `crates/jcode-harness-api-server/src/translate_tests.rs` | Internal protocol translates to API types |
| TC-3 | Background progress | `crates/jcode-harness-api-server/src/background_progress_tests.rs` | Progress events surface correctly |
| TC-4 | Rust SDK behavior | `crates/jcode-sdk/src/sdk_tests/` | SDK connects, drives sessions, streams events |
| TC-5 | Capability coverage | `crates/jcode-harness-api/src/capability_coverage.rs` tests | Capability negotiation works |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | TypeScript SDK client tests | `sdk/typescript/test/client.test.ts`, `structured.test.ts`, `launch.test.ts` | TS client drives sessions against the bridge |
| TC-7 | SDK schema parity | `sdk/typescript/test/schema-parity.test.ts` | Rust and TS SDK types agree |
| TC-8 | SDK e2e | `scripts/test_sdk_e2e.sh` | End-to-end launch + session flow works |
| TC-9 | SDK package test | `scripts/test_sdk_package.sh` | Published npm tarball imports and works |
| TC-10 | SDK parity in CI | `ci.yml` SDK parity job | Rust/TS parity gates pass |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Bridge not running | SDK reports a clear connection error |
| TC-12 | Version mismatch between client and server | Negotiation detects incompatible surfaces |
| TC-13 | Cancel mid-turn | Cancel honored, stream stops cleanly |

## Test Infrastructure

- Mock harness for TS tests (`sdk/typescript/test/mock-harness.ts`).
- Live TS test scripts (`live-*.mjs`) against a real bridge.
- `scripts/test_sdk_e2e.sh`, `scripts/test_sdk_package.sh`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-4 |
| FR-3 | TC-4 |
| FR-4 | TC-6 |
| FR-6 | TC-7, TC-10 |
| FR-7 | TC-13 |
| FR-8 | TC-5, TC-12 |
