---
title: "Session Hibernation"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Session Hibernation

## Scope

Covers the shared idle policy in the configuration layer, the daemon idle sweep and the agent cache release, the terminal client hibernation and wake, the client retained heap trim, and the remote history reload that the transcript mode triggers.

Out of scope: the exit-mode process re-exec and the waiter process in `src/cli/hibernate_wait.rs`, which have no automated test in this repository, and the measured resident memory of an ordinary session, which depends on the workload and the allocator.

The tests live in the modules they cover, as `#[cfg(test)] mod tests` blocks, not as separate test files.
Each row below names the file and the test function that exists in it.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | The idle due check in `crates/jcode-app-core/src/server/idle_hibernation.rs` (`idle_hibernation_due_respects_disable_idle_and_recent_activity`) | An idle state built at a start instant, a 30 second threshold, and variations of the threshold, the status idle age and the activity age | A zero threshold is never due, an unreached threshold is not due, a status that changed recently is not due, a recent activity age is not due, and the fully idle state is due |
| TC-2 | The idle re-arm in `crates/jcode-app-core/src/server/idle_hibernation.rs` (`idle_hibernation_rearms_for_turn_entirely_between_monitor_ticks`) | A released idle state, a 1 second threshold, a turn that finished 2 seconds after the start, and a sweep at 10 seconds | The state is not due while the status change is recent, it becomes due once the turn that started and finished between two sweeps is observed, and it is not due again while it stays released |
| TC-3 | The agent refusal guards in `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_refuses_queued_alerts_busy_compaction_and_live_tools`) | An agent with a queued pending alert, a queued soft interrupt, a held soft interrupt queue, a held compaction write lock, a tool marked in flight, and a registered active turn | Each guard makes `hibernate_idle_caches` return `None`, the provider cache keeps its two messages while the tool is in flight, and the release succeeds once the turn is dropped |
| TC-4 | The agent cache release in `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_releases_cache_and_rebuilds_exact_history_and_indexes`) | An agent with a large paired tool result, frozen tools, a captured instructions snapshot, a provider session handle and a rewind undo snapshot | The release reports more than one million provider cache bytes and two tool index entries, the provider cache count drops to zero, the tool id sets are emptied, the serialized session, the provider messages, the frozen tools, the captured instructions, the undo snapshot and the provider handle are unchanged, and the next turn rebuilds the indexes without adding synthetic duplicates |
| TC-5 | The no-write and lease behaviour in `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_does_not_write_session_and_refuses_migration_lease`) | A saved session file, an unsaved local message, and a migration lease written for the session | The release leaves the session file bytes and its modification time unchanged, a save under the lease succeeds without writing, the release is refused while the lease is present, and the local message and the provider cache survive |
| TC-6 | The client idle trigger in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_respects_timeout_typing_streaming_and_disabled_config`) | An expired idle timer, a zero idle period, a 1802 second idle period, a fresh user interaction, a fresh stream activity | A zero period never hibernates, a period that has not elapsed does not hibernate, a fresh user interaction does not hibernate, a fresh stream activity does not hibernate, and the elapsed period does hibernate |
| TC-7 | The eviction point work guard in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_rechecks_every_queued_and_active_work_guard`) | Sixteen busy states, each applied after the idle timer elapsed but before the paint | For every state no frame is frozen and the client stays awake |
| TC-8 | The retained client state in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_keeps_sources_draft_scroll_and_first_typed_character`) | A client with a local-only display message, a provider source message, a stored session message, a draft, a cursor, an attachment, a pasted content, a scroll offset and a paused scroll | The draft, the cursor, the scroll offset, the paused scroll, the session id, the source messages, the stored messages, the attachment and the pasted content survive the hibernation, and the first typed character is appended at the original cursor with the scroll offset unchanged and the notice cleared |
| TC-9 | The wake triggers in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_paste_resize_and_display_changes_wake_without_loss`) | A hibernated client that is then pasted into, resized, and given a new display message | Each of the three wakes the client, the pasted text lands in the input, and the new display message is kept |
| TC-10 | The frame bounds in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_rejects_unbounded_and_missing_screen_snapshots`) | A missing frame, a frame with a single oversized symbol, and an empty frame | No frame is frozen when the frame is missing, the oversized frame is refused by the freeze check, and the empty frame is refused |
| TC-11 | The memory metric in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`private_memory_metric_prefers_pss_anon`) | The process memory snapshot taken twice in a row, on a platform that reports the anonymous proportional set size | The measured private memory matches the reported anonymous proportional set size within 64 MiB |
| TC-12 | The transcript reload flag in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`transcript_drop_marks_history_reload_on_wake_only_when_dropped`) | A client that hibernated in the caches mode, and a client whose transcript was dropped | The caches mode does not request a history reload, the dropped transcript does, and the dropped flag is cleared |
| TC-13 | The notice formatting in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_rss_notice_reports_measurement_without_inventing_savings`) | A before and after pair 30 MiB apart in each direction, an equal pair, and a missing reading | The notice reports `-30.0 MiB`, reports `+30.0 MiB` for an increase, reports `unchanged` for a flat reading, and never breaks the line when a reading is missing |
| TC-14 | The wake event filter in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_ignores_heartbeat_but_wakes_before_remote_stream_event`) | A hibernated remote client that receives a pong, an acknowledgment and a text delta | The pong and the acknowledgment leave the client hibernated with a wake count of zero, and the text delta wakes the client, clears the notice and raises the wake count to one |
| TC-15 | The debug surface in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_debug_request_survives_recent_input_and_read_only_queries`) | A client with a recent user interaction that requests a debug hibernation and then reads the debug state three times | The state is `pending` before the paint, `hibernated` afterwards, the hibernation count is one, the wake count is zero, and reading the state does not wake the client |
| TC-16 | The retention check cadence in `crates/jcode-tui/src/tui/app/idle_heap_release.rs` (`retention_check_runs_immediately_then_obeys_interval`) | No previous check, a check at the current instant, and a check one interval old | The check is due when it never ran, not due again in the same instant, and due once one retention check interval has passed |
| TC-17 | The per-client budget in `crates/jcode-tui/src/tui/app/idle_heap_release.rs` (`client_retention_threshold_caps_default_but_honors_lower_and_disabled`) | A global threshold of 64 MiB, of 8 MiB, and a disabled threshold | The 64 MiB global threshold is capped to 16 MiB, the lower 8 MiB threshold is honored, and the disabled threshold stays disabled |
| TC-18 | The idle re-trim cadence in `crates/jcode-tui/src/tui/app/idle_heap_release.rs` (`idle_retrim_waits_for_first_trim_then_fires_on_cadence`) | No trim yet this idle period, a trim at the current instant, and a trim one re-trim interval old | The re-trim is not due before the first trim of the idle period, not due again in the same instant, and due once the re-trim interval has passed |
| TC-19 | The config defaults in `crates/jcode-config-types/src/session.rs` (`missing_setting_defaults_to_thirty_minutes`) | A session config deserialized from an empty object | The idle period is 1800 seconds and the mode is the caches mode |
| TC-20 | The config round trip in `crates/jcode-config-types/src/session.rs` (`zero_disables_hibernation_and_roundtrips`) | A session config with a zero idle period and the exit mode, serialized and deserialized | The serialized form contains `"exit"`, and the restored config keeps both the zero period and the exit mode |
| TC-21 | The mode aliases in `crates/jcode-config-types/src/session.rs` (`mode_parses_aliases`) | The strings `" Transcript "`, `"process"` and `"bogus"` | The first parses as the transcript mode, the second as the exit mode, and the third is refused |
| TC-22 | The environment override in `crates/jcode-base/src/config_tests.rs` (`hibernation_environment_override_accepts_seconds_and_zero_but_not_invalid_values`) | The values `60`, `" 0 "`, `-1` and `invalid` for `JCODE_HIBERNATION_IDLE_SECS` | The first two are applied, and the two invalid values leave the default of 1800 in place |
| TC-23 | The configuration file in `crates/jcode-base/src/config/default_file.rs` (`default_config_template_parses`, `session_hibernation_config_defaults_and_roundtrips`) | The shipped configuration template, an empty file, a file with a zero idle period, and a file with the exit mode | The shipped template parses and holds an idle period of 1800, an empty file inherits the default, a zero period round-trips through the file, and the exit mode parses from the file |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-24 | The daemon sweep in `crates/jcode-app-core/src/server/idle_hibernation.rs` (`idle_hibernation_monitor_skips_busy_and_running_then_releases_once`) | A real `Agent` behind a `tokio` mutex, a real swarm member whose status is changed, and a one second threshold | The sweep releases nothing while the agent lock is held and drops the session from the idle map, releases nothing while the member is running, releases once when the member is ready, does not release the same session twice, and clears the idle map when the threshold is zero |
| TC-25 | The next turn after a release in `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_next_turn_sends_original_tool_pairs_without_duplicates`) | A real `Agent` with a capturing provider, a paired tool result from before the release, and an isolated `JCODE_HOME` | The release succeeds, the next turn runs and returns the provider text, and the captured request holds exactly one tool use and one tool result for the pre-hibernation tool, with the original result text and no missing-output placeholder |
| TC-26 | The frozen frame and the render caches in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_frozen_frames_do_not_repopulate_prepared_caches`) | A real ratatui `TestBackend` terminal, a drawn frame, and a weakly held prepared chat frame | The prepared frame owners are all released at hibernation, the render caches stay empty across three redraws of the frozen frame, the screen shows the hibernation notice and the measured change, the frozen frame is not replaced by a later hibernation attempt, and the caches are rebuilt only after the client wakes |
| TC-27 | The hibernation status row in `crates/jcode-tui/src/tui/app/idle_hibernation.rs` (`idle_hibernation_notice_shows_measured_rss_on_one_status_row`) | A hibernated client rendered through a real ratatui `TestBackend` terminal of 70 by 10 cells | The rendered screen contains the hibernation word, the measured change of `-30.0 MiB` and the resume hint |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-28 | The measured resident memory of a release in `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_measured_rss_delta`) | Run the ignored test on an isolated process: build an agent with a 64 MiB tool result, warm the provider cache, snapshot the resident memory, release, purge the retained heap, snapshot again | The release reports the provider cache size, the two resident memory readings differ by the released amount, and the provider cache count is zero while the session still holds its two messages. The test is marked `#[ignore]` because the allocator and the other tests in the same process perturb the reading, so it is a manual measurement rather than an automated one |
| TC-29 | The remote history reload in `crates/jcode-tui/src/tui/app/tests/remote_events_reload_03/part_02.rs` (`test_delta_history_without_prefix_requests_full_history`) | Deliver a delta history event that carries no prefix to a client that had dropped its transcript | The client marks the history as needing a reload and does not treat the remote history as loaded |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-30 | The idle period is set to zero | Hibernation is disabled on both the daemon and the client, the daemon clears its idle map, and the debug hibernation command refuses with a disabled error |
| TC-31 | The environment override carries a negative or a non-numeric value | The override is ignored and the file value stays in place |
| TC-32 | A whole turn starts and finishes between two daemon sweeps | The idle window is re-armed from the moment the turn finished, so the session is not hibernated by the sweep that missed the turn |
| TC-33 | A session is running a turn, or a tool is in flight | The daemon declines the release, resets the idle window, and neither the turn nor the tool is cancelled |
| TC-34 | A queued alert or a queued soft interrupt is pending | The daemon declines the release, so a scheduled wake is never dropped by hibernation |
| TC-35 | A compaction is in flight | The daemon declines the release, so the compaction is not disturbed |
| TC-36 | A migration lease is held for the session | The daemon declines the release, and a save under the lease is a successful no-op that does not write the file |
| TC-37 | The session file was saved before the hibernation | The file bytes and the modification time are unchanged after the release |
| TC-38 | The frozen frame is missing, empty, oversized in cells, or oversized in symbol bytes | The release still happens, no frame is frozen, and the client does not retry the oversized frame on every idle tick |
| TC-39 | The memory reading is flat, or cannot be taken | The notice reports `unchanged` or a reading without a saving, and it never claims a positive saving |
| TC-40 | The memory reading increased after the release | The notice reports the increase with a `+` sign, and the change is not presented as a saving |
| TC-41 | The client receives a heartbeat, an acknowledgment or a read-only debug query while hibernated | The client stays hibernated, the wake count does not change, and the idle clock is not reset |
| TC-42 | The client receives an event that may change the conversation content | The client wakes, the notice is cleared, and the wake count increases by one |
| TC-43 | Work is queued between the idle timer and the paint | Nothing is evicted, the client stays awake, and the queued work is not cancelled |
| TC-44 | The client is repainted repeatedly while hibernated | The prepared frame caches stay released and are rebuilt only after the wake |
| TC-45 | The global retained heap threshold is disabled | The client never trims its retained heap, and the disabled state is preserved |
| TC-46 | The global retained heap threshold is lower than the per-client budget | The lower threshold is honored |
| TC-47 | The client stays idle for a long stretch with only heartbeats and remote snapshots | The retained heap is re-trimmed on the re-trim cadence, not only once per idle period |

## Test Infrastructure

- The daemon and agent tests take `crate::storage::lock_test_env()` and set `JCODE_HOME` to a temporary directory, so parallel tests do not share session state.
- The agent tests use a `TestProvider` that fails the test if the provider is called, so a hibernation path can never silently issue a request.
- The next turn test uses a `CaptureProvider` that records the message list it receives, so the request that follows a release can be inspected.
- The daemon sweep test builds a real `Agent`, a real `SwarmMember` and a real `SessionAgents` map, so the sweep exercises the same locks and the same status flags as production.
- The client tests use `crate::tui::app::tests::create_test_app()` and a ratatui `TestBackend` terminal, so the frame bounds, the frozen frame and the rendered status row are exercised through the real renderer.
- The render tests take `crate::tui::ui::render_state_test_lock()`, because the prepared frame caches are process-global.
- The idle timer is expired deterministically by moving `app_started`, `last_busy`, `last_user_interaction` and `last_stream_activity` into the past, so no test sleeps for the idle period.
- The manual RSS measurement test is marked `#[ignore]` and is meant to be run on an isolated process.
- Useful commands: `cargo test -p jcode-app-core idle_hibernation`, `cargo test -p jcode-tui idle_hibernation`, `cargo test -p jcode-tui idle_heap_release`, `cargo test -p jcode-config-types session`, `cargo test -p jcode-base hibernation`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-6, TC-19, TC-20 |
| FR-2 | TC-19, TC-20, TC-21, TC-23 |
| FR-3 | TC-3, TC-4, TC-24 |
| FR-4 | TC-3, TC-24, TC-33, TC-34, TC-35 |
| FR-5 | TC-1, TC-2, TC-24, TC-32 |
| FR-6 | TC-4, TC-5 |
| FR-7 | TC-24, TC-28 |
| FR-8 | TC-26, TC-44 |
| FR-9 | TC-8, TC-9, TC-41 |
| FR-10 | TC-10, TC-38 |
| FR-11 | TC-11, TC-13, TC-27, TC-39, TC-40 |
| FR-12 | TC-8, TC-9, TC-42 |
| FR-13 | TC-7, TC-43 |
| FR-14 | TC-14, TC-15, TC-41, TC-42 |
| FR-15 | TC-16, TC-17, TC-18, TC-45, TC-46, TC-47 |
| FR-16 | TC-19, TC-21, TC-23 |
| FR-17 | TC-12, TC-29 |
| FR-18 | TC-23 |
| FR-19 | TC-15, TC-30 |
| FR-20 | TC-22, TC-31 |
| NFR-1 | TC-11, TC-13, TC-39, TC-40 |
| NFR-2 | TC-4, TC-25 |
| NFR-3 | TC-5, TC-36, TC-37 |
| NFR-4 | TC-16, TC-24 |
| NFR-5 | TC-10, TC-17, TC-38 |
| NFR-6 | TC-3, TC-7, TC-24, TC-33 |
| NFR-7 | TC-8, TC-29 |
| NFR-8 | TC-26, TC-44 |
| NFR-9 | TC-19, TC-20, TC-23 |
| NFR-10 | TC-28 |
| NFR-11 | TC-24, TC-28 |

## Known gaps

- The exit mode has no automated test. `src/cli/hibernate_wait.rs` and the exit branch of `crates/jcode-tui/src/tui/app/idle_hibernation.rs` are not covered by any test, so the waiter command, the re-exec and the resume on the next key press are unverified. FR-18 and NFR-10 are mapped to the configuration test only.
- The daemon sweep interval of 10 seconds is a constant in the source. No test asserts the interval, and the sweep test drives `reclaim_idle_caches` directly instead of waiting for the timer.
- The daemon log line, the client log line and the memory history entries named `server_idle_hibernation_before` and `server_idle_hibernation_after` are not asserted by a test. The sweep test checks the release counts, not the log output.
- The provider cache byte count and the tool index entry count are reported by the release, but the daemon-side aggregation of those counts across the sessions of one sweep is not asserted.
- The real terminal path of the exit mode, where the daemon owns the session and the waiter resumes it, was validated manually and is described in `docs/SESSION_HIBERNATION.md`, not by a test.
- The `transcript` mode path that clears the remote side pane images and shrinks the display messages is not covered, only the reload flag is.
