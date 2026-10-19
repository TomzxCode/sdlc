---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

TC-1, TC-2, TC-3, and TC-7 all still exist and remain accurate: `crates/jcode-base/src/compaction_tests.rs` (38 tests), the `crates/jcode-message-types` unit tests, `tests/context_window_matrix.rs` (6 tests), and the cache-relevant hash tests.

Two entries describe behavior that no single test matches:

| ID | Documented expectation | Reality | Correction |
|---|---|---|---|
| TC-4 | "Turn loop compacts and continues correctly" over `crates/jcode-app-core/src/agent_tests.rs` | No test asserts that. The compaction tests there are `run_turn_streaming_mpsc_emits_native_compaction_for_client_cache_reset` (`:819`), `messages_for_provider_replays_persisted_native_compaction_in_auto_mode` (`:1046`), `oversized_openai_native_compaction_is_persisted_as_text_fallback` (`:1087`), and `messages_for_provider_applies_manual_compaction_in_native_auto_mode` (`:1149`). | Reword to describe the native-compaction behaviors the file actually covers. |
| TC-5 | "Session at context limit → continues via compaction rather than failing" | No dedicated test exists. The recovery code is at `crates/jcode-app-core/src/agent/compaction.rs:130-230`; the closest coverage is `test_guard_at_95_triggers_hard_compact` in `crates/jcode-base/src/compaction_tests.rs:491`. | State that the behavior has no direct test and name the nearest coverage. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-base/src/session_tests/cases.rs` (session round-trip with `StoredCompactionState`)
- `crates/jcode-tui/src/tui/app/tests.rs:753` and `:837` (compaction invalidates the KV-cache baseline)
- `crates/jcode-tui/src/tui/app/conversation_state.rs:844` (`compaction_message_is_one_line_with_method_and_usage`, the before-and-after usage message)
- `crates/jcode-tui/src/tui/app/tests/cache_prompt_accounting.rs:120` (compaction event handling)
- `crates/jcode-tui/src/tui/app/tests/remote_events_reload_02/part_02.rs:293` and `:335` (remote compaction completion and compaction mode change)
- `crates/jcode-tui/src/tui/app/tests/remote_events_reload_04.rs:2564` (`test_setting_context_limit_also_syncs_the_compaction_budget`)
- `crates/jcode-app-core/src/protocol_tests/core_events.rs:17,168,301` (compaction state over the wire)
- `crates/jcode-app-core/src/agent/idle_hibernation.rs:148` (`idle_hibernation_refuses_queued_alerts_busy_compaction_and_live_tools`)

## Quality

The existing entries remain accurate apart from TC-4 and TC-5.

## Correctness

No issues found.

## Maintainability

No issues found.
