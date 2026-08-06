---
title: "Context Compaction"
status: done
---

# Test Plan: Context Compaction

## Scope

Covers compaction policy, state, KV-cache hash correctness, and context-window resolution invariants. Out of scope: live provider behavior (covered by the context-window matrix suite where applicable).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Compaction policy and state | `crates/jcode-base/src/compaction_tests.rs` | Compaction triggers and records state correctly |
| TC-2 | Message cache-relevant hashing | `crates/jcode-message-types` unit tests | Hashes stable for unchanged prefixes, change on compaction |
| TC-3 | Context-window resolution invariants | `tests/context_window_matrix.rs` | Limits resolved per provider invariants |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Agent-loop compaction | `crates/jcode-app-core/src/agent_tests.rs` | Turn loop compacts and continues correctly |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-5 | Session at context limit | Continues via compaction rather than failing |
| TC-6 | Compaction then resume | Compacted state reflected on resume |
| TC-7 | Cache-relevant prefix change | Detected; KV-cache correctness preserved |

## Test Infrastructure

- Context-window matrix suite (`tests/context_window_matrix.rs`).
- Message-model unit fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-4 |
| FR-4 | TC-1, TC-6 |
| FR-5 | TC-2, TC-7 |
| FR-7 | TC-3 |
| NFR-1 | TC-6 |
| NFR-3 | TC-5 |
