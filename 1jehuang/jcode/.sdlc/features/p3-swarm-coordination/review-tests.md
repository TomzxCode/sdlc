---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

TC-1 through TC-7 all still exist and remain accurate: `crates/jcode-app-core/src/server/swarm_persistence_tests.rs`, `client_comm_tests.rs` and `comm_control_tests.rs`, `comm_plan_tests.rs`, `comm_session_tests.rs`, the inline `crates/jcode-plan` tests, `scripts/test_swarm.py`, `scripts/test_swarm_debug.py`, and `scripts/benchmark_swarm.py`.

Two entries describe behavior that no longer matches the code:

| ID | Documented expectation | Reality | Correction |
|---|---|---|---|
| TC-8 | "Malformed member completion report → Rejected or flagged per tldr/marker rules" | No test asserts rejection, because nothing is rejected. The behavior is normalize-and-derive. The closest coverage is the inline `validate_swarm_tldr_*` tests in `crates/jcode-swarm-core/src/lib.rs` and `append_swarm_completion_report_instructions_is_idempotent` at `crates/jcode-app-core/src/server/swarm.rs:1993`. | Reword the expected behavior to "the report is normalized, a tldr is derived when missing, and delivery is never blocked". |
| TC-9 | "Plan exceeds item limit → Plan bounded at MAX_PLAN_ITEMS without corruption" | No test asserts the limit. Enforcement lives at `crates/jcode-app-core/src/server/comm_plan.rs:407` and `debug_swarm_write.rs:402`. | Either point at the enforcement sites and state that no dedicated test exists, or drop the case. |
| TC-10 | "Reload mid-task → Swarm state restored; task not lost" | No dedicated test. The nearest coverage is `crates/jcode-app-core/src/server/swarm_persistence_tests.rs` and `crates/jcode-app-core/src/server/reload_tests.rs`. It is also contradicted in part by `IDLE_WORKER_NOT_RESTORED_NOTE`. | Reword to match the durable-snapshot behavior, including that idle headless workers are not resumed. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-app-core/src/tool/communicate_tests.rs` and `crates/jcode-app-core/src/tool/communicate_tests/{assignment,credential_failures,end_to_end,input_format}.rs` (the `run_plan` driver, the swarm tool schema, and the removed-action assertions)
- `crates/jcode-app-core/src/server/swarm_watchdog_tests.rs`
- `crates/jcode-app-core/src/server/swarm_cascade_tests.rs`
- `crates/jcode-app-core/src/server/swarm_mutation_state_tests.rs`
- `crates/jcode-app-core/src/server/comm_control_tests/` (all 20 files; the TC-2 entry cites only the index file)
- `crates/jcode-app-core/src/protocol_tests/comm_requests.rs` and `comm_responses.rs`
- `crates/jcode-app-core/src/agent/swarm_reminder_tests.rs`
- `crates/jcode-tui/src/tui/info_widget_tests/swarm_plan_todos.rs`
- `crates/jcode-tui-render/src/swarm_gallery_tests.rs`

## Quality

The existing entries remain accurate apart from the three above.

## Correctness

No issues found.

## Maintainability

No issues found.
