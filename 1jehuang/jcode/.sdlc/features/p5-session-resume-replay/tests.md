---
title: "Session Persistence, Resume and Replay"
status: done
---

# Test Plan: Session Persistence, Resume and Replay

## Scope

Covers session persistence, journaling, resume, import, replay, and reload recovery. Out of scope: live provider round-trips.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Session store behavior | `crates/jcode-base/src/session_tests/` | Sessions persist, load, and resume correctly |
| TC-2 | Session search scoring | `crates/jcode-session-types/src/session_search_tests.rs` | Search results ranked correctly |
| TC-3 | External session import | `crates/jcode-base/src/import_tests.rs` | Imported sessions parse and convert correctly |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | End-to-end session flow | `tests/e2e/session_flow.rs` | Create, stream, persist, resume works end to end |
| TC-5 | Reload multi-client recovery | `tests/e2e/reload_multiclient.rs` | Clients reconnect and sessions survive reload |
| TC-6 | Reload recovery audit | `scripts/test_reload.py`, `scripts/reload_recovery_audit.py` | Crashed/reloaded sessions recover cleanly |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-7 | Corrupted or partial journal | Journal repaired or rejected without corrupting the snapshot |
| TC-8 | Very large session files | Load and search stay responsive |
| TC-9 | Crash mid-write | Session marked crashed and recoverable on next start |

## Test Infrastructure

- Session fixtures under `tests/fixtures/`.
- Multi-client e2e harness (`tests/e2e/test_support/`).
- Python reload-recovery audit scripts.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-4 |
| FR-3 | TC-5, TC-9 |
| FR-4 | TC-3 |
| FR-8 | TC-6, TC-9 |
| FR-9 | TC-2 |
| NFR-1 | TC-7 |
