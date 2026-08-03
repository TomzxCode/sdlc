---
title: "Remote Session Protocol"
status: done
---

# Test Plan: Remote Session Protocol

## Scope

Tests cover CBOR encoding/decoding correctness, length-prefixed framing, incremental decoding across fragmentation boundaries, and the validated message API (`encodeClientMessage`/`encodeServerMessage`) plus the `hello` handshake.
Transport-level behavior is out of scope (covered by `pi-client`/`pi-server`).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | CBOR encode/decode round-trips representative values | Mixed JS values | Lossless round-trip |
| TC-2 | Encoded messages carry a four-byte BE length prefix then one definite-length CBOR item | A `hello` message | Length prefix matches CBOR payload length |
| TC-3 | Incremental decoder recovers messages across arbitrary fragmentation | Framed bytes split at many offsets | Original messages recovered exactly |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | `encodeClientMessage` validates and frames a valid client message | Valid message object | Complete framed `Uint8Array` returned |
| TC-5 | Decoder tolerates coalescing of multiple framed messages in one chunk | Multiple encoded messages concatenated | All messages emitted in order |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Fragment boundary inside the length prefix | Decoder waits for the full prefix before parsing |
| TC-7 | Fragment boundary inside the CBOR payload | Decoder buffers until the full payload arrives |
| TC-8 | Invalid message shape | `encodeClientMessage` rejects rather than emitting malformed bytes |

## Test Infrastructure

- Pure function tests; no network, sockets, or timers.
- Ran with Vitest (`packages/protocol/test/`).

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2 |
| FR-02 | TC-2, TC-5 |
| FR-03 | TC-4 |
| FR-04 | TC-3, TC-5, TC-6, TC-7 |
| FR-05 | TC-8 |
| FR-09 | TC-1 |
