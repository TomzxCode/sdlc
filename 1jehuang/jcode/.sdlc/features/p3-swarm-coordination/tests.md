---
title: "Swarm Multi-Agent Coordination"
status: done
---

# Test Plan: Swarm Multi-Agent Coordination

## Scope

Covers swarm persistence, comm channels, plan graph handling, and member report validation. Out of scope: live multi-agent behavior against paid providers (covered by scripted e2e suites).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Swarm state persistence | `crates/jcode-app-core/src/server/swarm_persistence_tests.rs` | Swarm survives reload/restart |
| TC-2 | Comm channel behavior | `crates/jcode-app-core/src/server/client_comm_tests.rs`, `comm_control_tests.rs` | Messages delivered to the right members |
| TC-3 | Comm plan graph handling | `crates/jcode-app-core/src/server/comm_plan_tests.rs` | Plan updates propagate |
| TC-4 | Comm session handling | `crates/jcode-app-core/src/server/comm_session_tests.rs` | Session-level comm works |
| TC-5 | Plan DAG invariants | `crates/jcode-plan` tests | Plan stays bounded and versioned |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Swarm e2e scenarios | `scripts/test_swarm.py`, `scripts/test_swarm_debug.py` | Coordinator + workers complete a delegated task |
| TC-7 | Swarm performance benchmark | `scripts/benchmark_swarm.py` | Throughput/latency within expectations |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Malformed member completion report | Rejected or flagged per tldr/marker rules |
| TC-9 | Plan exceeds item limit | Plan bounded at MAX_PLAN_ITEMS without corruption |
| TC-10 | Reload mid-task | Swarm state restored; task not lost |

## Test Infrastructure

- Script-based swarm suites (`test_swarm.py`, `test_swarm_debug.py`, `benchmark_swarm.py`).
- Durable-state fixtures for reload tests.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-2 | TC-3, TC-5, TC-9 |
| FR-4 | TC-2, TC-4 |
| FR-6 | TC-1, TC-10 |
| FR-7 | TC-8 |
| NFR-1 | TC-1, TC-10 |
