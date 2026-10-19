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
| TC-2 | `crates/jcode-session-types/src/session_search_tests.rs` | The file does not exist. The tests are an inline module at `crates/jcode-session-types/src/lib.rs:983-984` with 7 test functions. | Point TC-2 at the inline module and at `crates/jcode-app-core/src/tool/session_search_tests.rs`. |
| TC-1 | `crates/jcode-base/src/session_tests/` | Accurate, but the prewarm tests are missing from the entry. | Extend TC-1 to include `crates/jcode-base/src/session/prewarm.rs` (inline tests: `resume_uses_prewarmed_copy_once`, `a_write_after_prewarm_invalidates_the_copy`, `several_sessions_are_all_prewarmed_by_the_worker_pool`). |
| TC-3 | `crates/jcode-base/src/import_tests.rs` | Accurate, but the adversarial import suite is not listed. | Add `crates/jcode-import-core/tests/claude_adversarial.rs` to TC-3. |
| TC-5 | "Session at context limit → continues via compaction rather than failing" | No dedicated test exists. The recovery code is at `crates/jcode-app-core/src/agent/compaction.rs:130-230`; the closest coverage is `test_guard_at_95_triggers_hard_compact` in `crates/jcode-base/src/compaction_tests.rs:491`. | State that the behavior has no direct test and name the nearest coverage. |
| TC-6 | "Compaction then resume → compacted state reflected on resume" | Covered indirectly by `test_persisted_state_round_trip_preserves_compacted_view` and `crates/jcode-base/src/session_tests/cases.rs`. The `session_tests` file is not listed. | Add `crates/jcode-base/src/session_tests/cases.rs` to TC-6. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-base/src/session/prewarm.rs` (inline `mod tests`; covers the new fast-resume path)
- `crates/jcode-app-core/src/tool/session_search_tests.rs` (the `session_search` tool)
- `crates/jcode-app-core/src/replay/tests.rs` (replay timeline, `StoredReplayEventKind`)
- `crates/jcode-app-core/src/restart_snapshot_tests.rs` (reboot snapshot)
- `src/cli/commands/restart_tests.rs` (the `jcode restart save/restore/clear` CLI)
- `crates/jcode-import-core/tests/claude_adversarial.rs` (adversarial external-tool transcripts)
- `crates/jcode-tui/src/tui/session_picker/loading_tests.rs` (1564 lines: session discovery, disk cache, external sessions)
- `crates/jcode-tui/src/tui/session_picker_tests.rs` (71 tests, including `standalone_resume_renders_before_list_load_finishes`)
- `crates/jcode-tui/src/tui/session_picker_tests/live_presence.rs`
- `crates/jcode-base/src/session/maintenance.rs` (inline tests, `.bak` pruning)
- `crates/jcode-app-core/src/session_active_pids.rs` and `crates/jcode-storage/src/active_pids.rs` (active-session tracking)
- `crates/jcode-app-core/src/catchup.rs` (catch-up "seen" state for interrupted sessions)
- `crates/jcode-protocol/src/protocol_tests/misc_events.rs:410-498` (history-base round-trips and `test_resume_session_defaults_sync_flags`)

## Quality

The Test Infrastructure section claims "Session fixtures under `tests/fixtures/`".
`tests/fixtures/` holds provider fixtures only.
Reword to: "Session fixtures are synthesized per test (temporary `JCODE_HOME` session stores); `tests/fixtures/` holds provider fixtures only. Multi-client end-to-end harness: `tests/e2e/test_support/`."

## Correctness

No issues found.

## Maintainability

No issues found.
