---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-2 | `crates/jcode-app-core/src/ambient_runner.rs` tests | That file is now a 3-line re-export with no tests. The runner tests are `crates/jcode-app-core/src/ambient/runner_tests.rs` (7 tests) and `crates/jcode-app-core/src/ambient/runner_live_delivery_tests.rs`. | Correct the path. |
| TC-3 | `crates/jcode-app-core/src/ambient_scheduler.rs` tests | That file is now a 3-line re-export with no tests. The scheduler tests are inline in `crates/jcode-app-core/src/ambient/scheduler.rs` (inline `mod tests` at line 283, 10 tests), plus `tests/e2e/ambient.rs::test_adaptive_scheduler_intervals` and `_backoff` and `_pause`. | Correct the path. |
| TC-5 | "Ambient task requires permission → Action gated by safety system, no bypass" | Supported, but by files that are not listed: `tests/e2e/ambient.rs::test_ambient_request_permission_tool` and `crates/jcode-app-core/src/tool/ambient/tests.rs::test_request_permission_rejects_non_ambient_session`. | Name the covering files. |
| TC-6 | "Server reload during ambient cycle → Ambient state recovered; cycle resumes" | No such test exists. `tests/e2e/ambient.rs::test_ambient_state_lifecycle` exercises the in-memory `record_cycle`, not a server reload. | State that the behavior has no test, or reword to the in-memory lifecycle the test actually covers. |
| TC-7 | "Risky command in ambient task → Passed through command-risk gate before execution" | No ambient-specific test exists. The gate is shared with interactive bash (`crates/jcode-app-core/src/tool/bash_destructive_gate.rs`). | State that the behavior has no ambient-specific test, or point at the shared gate tests. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-app-core/src/ambient/runner_tests.rs`
- `crates/jcode-app-core/src/ambient/runner_live_delivery_tests.rs`
- `crates/jcode-app-core/src/ambient/scheduler.rs` (inline `mod tests`)
- `crates/jcode-app-core/src/tool/ambient/tests.rs` (23 tests: schedule-target parsing, permission input shape, `register_unregister_ambient_session`)
- `crates/jcode-tui/src/tui/info_widget_tests.rs` (the ambient widget render)
- `crates/jcode-tui/src/tui/ui_tests/swarm_buffer.rs` (`AmbientWidgetData`)
- `crates/jcode-tui/src/tui/app/tests/ssh_remote.rs` (`gather_ambient_info`)
- `crates/jcode-app-core/src/server/startup_tests.rs` (ambient server startup)

The `ambient:*` debug commands in `crates/jcode-app-core/src/server/debug_ambient.rs` have no test module at all and are entirely untested.

## Quality

The existing entries (TC-1 `crates/jcode-app-core/src/ambient_tests.rs` and TC-4 `tests/e2e/ambient.rs`) still exist and remain accurate.

## Correctness

No issues found.

## Maintainability

No issues found.
