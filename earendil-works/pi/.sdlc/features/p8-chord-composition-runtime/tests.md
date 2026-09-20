---
title: "Chord Composition Runtime"
status: done
session_link: "backfilled-from-shipped-code"
---

# Test Plan: Chord Composition Runtime

## Scope

The suite exercises facets, singleton and keyed services, replicated state, delta tracking, the remote-service wire boundary, facet bundling and loading, context, and strict-JSON validation.
The suite covers ten test files under packages/chord/test with roughly one hundred eighty individual cases.
Out of scope is any real transport, Pi host integration, and performance benchmarking beyond the delta traversal bench.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Delta tracker records intent, root ops, and whole-value replacement | Mutations through the tracked proxy | Correct operation batches with a complete base batch on first flush |
| TC-2 | Immutable apply preserves prior revisions while converging replicas | Operation batches against a base value | New revision equals the producer value and old revisions are unchanged |
| TC-3 | Unsafe array indices, malformed ops, and boundary escapes are rejected | Hostile or out-of-range operations | Descriptive apply-time errors with no state corruption |
| TC-4 | Path codec interns paths and property tests round-trip random ops | Random tracked mutations | Decoded batches match the producer value on every seed |
| TC-5 | Delta payloads are deeply detached from producer mutations | Shared and subsequently edited producer objects | Published snapshots stay independent of later producer edits |
| TC-6 | Tracker proxies survive garbage-collection pressure | Mutations interleaved with GC jobs | No lost operations and no retained-worker failures |
| TC-7 | Singleton provide, consume, replacement, and disposal behave stably | Facet graphs with singleton providers | Stable facades, buffered-update replay, and facade cleanup on disposal |
| TC-8 | Replicated state hydrates, buffers racing updates, and survives rebinds | Publish, rebind, and hydration races | Cold replicas hydrate and buffered updates arrive exactly once |
| TC-16 | Context layers values and propagates cancellation | Nested contexts with typed keys | Child isolation, parent inheritance, and prompt cancellation |
| TC-17 | Strict-JSON validation accepts JSON and rejects the rest | JSON and non-JSON candidate values | True for strict JSON and false otherwise with no normalization |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Facet host validates graphs and orders activation and disposal | Facets with chained dependencies | Providers activate before consumers and dispose in reverse order |
| TC-10 | Keyed services route through the host and stay local when marked local | Keyed providers with local and remote contracts | Remote keyed calls route through the provider while local ones never leave the process |
| TC-11 | Loaders combine in order and dispose generations in reverse | Multiple facet loaders with resources | Load-order facets and reverse-order disposal with cleanup on partial failure |
| TC-12 | Wire grammar encodes control calls and isolates per-state codecs | Service catalogue, subscribe, and unsubscribe calls | Valid calls encode and malformed snapshots or updates are rejected |
| TC-13 | Remote endpoints publish provider subscriptions and clean them up | A provider endpoint with active subscriptions | Updates publish while subscribed and resources release on close |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-14 | Package boundary keeps Chord free of Pi dependencies | Run the boundary test over the Chord tree | No import reaches another Pi workspace package or outside file |
| TC-15 | Facet bundles build, load, reload, and reject corrupt entries | Bundle a plugin package then load its entries | Fresh reloadable generations load and corrupt entries fail fast |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9E | Missing dependencies, cycles, duplicate providers, async setup | Host rejects the graph before binding any service |
| TC-11E | Replacement activation or post-cutover cleanup fails | Old generation stays active or the host terminates deterministically |
| TC-15E | Invalid entry configuration or corrupt bundle bytes | Build or load fails without touching the previous output generation |

## Test Infrastructure

- Vitest runs the suite from packages/chord with a loopback service transport helper.
- A dedicated retention worker exercises tracker proxies under garbage-collection pressure.
- Content-addressed bundle fixtures are built with esbuild and loaded through the Node VM loader.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-9, TC-11 |
| FR-2 | TC-9, TC-9E |
| FR-3 | TC-7 |
| FR-4 | TC-10 |
| FR-5 | TC-9 |
| FR-6 | TC-7, TC-8 |
| FR-7 | TC-12, TC-13 |
| FR-8 | TC-1, TC-2, TC-3, TC-4, TC-5, TC-6 |
| FR-9 | TC-11, TC-11E |
| FR-10 | TC-15, TC-15E |
| FR-11 | TC-16 |
| NFR-1 | TC-14 |
| NFR-2 | TC-12, TC-17 |
| NFR-3 | TC-8 |
| NFR-4 | TC-4, TC-8 |
