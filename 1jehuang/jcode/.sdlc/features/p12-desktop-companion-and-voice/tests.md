---
title: "Desktop Companion and Voice"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Desktop Companion and Voice

## Scope

Covers the companion socket protocol, the lid-close override and its crash recovery, the desktop-open helpers, the global push-to-talk hotkey listener, the microphone capture and streaming transcription path, and the configured dictation command.
Every test listed here is an existing test in the repository.
Out of scope: the live macOS and Windows power-plan changes, the live Nari service, the live notification daemon, and physical evdev devices, which are exercised manually rather than in an automated test.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Companion requests and responses round-trip as tagged JSON | `crates/jcode-base/src/companion_client.rs` -> `requests_round_trip_as_tagged_json` | The request serializes with an `op` tag and deserializes back to the same value. |
| TC-2 | Lid override engages and restores the original setting | `crates/jcode-companion/src/lid_override.rs` -> `engages_then_restores_original_setting` | The setting is blocked while engaged, the original value comes back, and the journal is removed. |
| TC-3 | Dropping the override restores the original setting | `crates/jcode-companion/src/lid_override.rs` -> `drop_restores_setting` | The original value is restored and the journal is removed when the owner goes out of scope. |
| TC-4 | A crashed owner is repaired by the next process | `crates/jcode-companion/src/lid_override.rs` -> `crashed_owner_is_recovered_by_next_process` | The next idle tick restores the original value and clears the journal. |
| TC-5 | The originals survive a crash and a later engagement | `crates/jcode-companion/src/lid_override.rs` -> `crashed_owner_originals_are_kept_when_next_process_engages` | The restored value is the user's value, not the value the crash left behind. |
| TC-6 | A live foreign owner is left alone | `crates/jcode-companion/src/lid_override.rs` -> `live_foreign_owner_is_left_alone` | The second process does not engage and does not undo the owner's override. |
| TC-7 | A re-exec with the same pid reuses the saved originals | `crates/jcode-companion/src/lid_override.rs` -> `reexec_with_same_pid_reuses_saved_originals` | The re-exec'd process engages and restores the original value. |
| TC-8 | A failed block rolls back and stops retrying until idle | `crates/jcode-companion/src/lid_override.rs` -> `failed_block_rolls_back_and_stops_retrying_until_idle` | The override is not engaged, the journal is removed, and the retry latch resets on the idle transition. |
| TC-9 | The `pmset -g` sleep flag is parsed | `crates/jcode-companion/src/lid_override.rs` -> `pmset_output_parsing` | `SleepDisabled 1` is detected, and the other shapes are not. |
| TC-10 | The Windows power-scheme GUID round-trips | `crates/jcode-companion/src/lid_override.rs` -> `guid_round_trips` | A canonical GUID parses into its parts and formats back unchanged, and a bad string is rejected. |
| TC-11 | The recovery journal format is stable | `crates/jcode-companion/src/lid_override.rs` -> `snapshot_journal_format_is_stable` | The journal serializes with the platform tag and deserializes back to the same snapshot. |
| TC-12 | The power-activity lease expires without renewal | `crates/jcode-companion/src/server.rs` -> `power_lease_expires_without_renewal` | The lease is live halfway through the window and released once it expires. |
| TC-13 | The status reply carries the protocol and the capabilities | `crates/jcode-companion/src/server.rs` -> `status_reports_protocol_and_capabilities` | The reply is successful and lists the configured capabilities. |
| TC-14 | Voice failures map to short labels | `crates/jcode-companion/src/voice.rs` -> `failure_labels_are_short` | A missing configuration and a timeout each map to their own short message. |
| TC-15 | A target is classified as a URL or a local path | `crates/jcode-desktop-open/src/lib_tests.rs` -> `target_parse_distinguishes_urls_and_paths` | A URL stays a URL, an existing directory is a local directory target, and a missing path is an error. |
| TC-16 | A desktop entry is normalized into application id stems | `crates/jcode-desktop-open/src/lib_tests.rs` -> `normalize_desktop_entry_strips_suffix_and_adds_stem` | The `.desktop` suffix is stripped and the last segment is added as a second stem. |
| TC-17 | Browser application ids are matched case-insensitively | `crates/jcode-desktop-open/src/lib_tests.rs` -> `app_id_matches_is_case_insensitive_and_guards_short_ids` | A matching id matches, a different id does not, and very short ids never match. |
| TC-18 | A newly created browser window is preferred | `crates/jcode-desktop-open/src/lib_tests.rs` -> `select_window_prefers_newly_created_browser_window` | The window that appeared after the open wins over the more recently focused one. |
| TC-19 | The most recently focused window is the fallback | `crates/jcode-desktop-open/src/lib_tests.rs` -> `select_window_falls_back_to_most_recently_focused` | With no new window, the window with the newest focus timestamp is chosen. |
| TC-20 | No browser window means nothing to raise | `crates/jcode-desktop-open/src/lib_tests.rs` -> `select_window_returns_none_without_browser_windows` | The selection returns no window. |
| TC-21 | The dictation command output is trimmed | `crates/jcode-voice/src/dictation_tests.rs` -> `run_command_trims_trailing_newlines` | The printed transcript comes back without its trailing newline. |
| TC-22 | The session short name is read from the window title | `crates/jcode-voice/src/dictation_tests.rs` -> `extract_session_short_name_from_jcode_window_title` | The title format with live metrics still yields the short name. |
| TC-23 | The session short name is normalized | `crates/jcode-voice/src/dictation_tests.rs` -> `normalize_session_short_name_strips_wrapping_punctuation` | Bracketed and hyphenated names become the bare lowercase token. |
| TC-24 | The client candidate matching the title is selected | `crates/jcode-voice/src/dictation_tests.rs` -> `select_candidate_prefers_title_match` | The candidate whose name appears in the title wins. |
| TC-25 | The parent pid is read from the process status | `crates/jcode-voice/src/dictation_tests.rs` -> `parse_ppid_from_proc_status` | The `PPid` field is parsed. |
| TC-26 | A resumed session id is read from the command line | `crates/jcode-voice/src/dictation_tests.rs` -> `read_resumed_session_id_from_cmdline_for_current_process` | The reader runs against a live process command line without error. |
| TC-27 | The push-to-talk chord is decoded | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `decoder_chords_repeat_and_release` | A press and a release are produced, repeats and modifier noise are ignored, and the assistant key works alone. |
| TC-28 | Shift plus the push-to-talk key spawns instead of holding | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `shift_before_copilot_spawns_but_synthetic_shift_holds` | A user Shift before the key produces a spawn edge, and right Shift is never synthesized. |
| TC-29 | A key already held when the listener opens is ignored | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `held_at_open_is_ignored` | The snapshot of the held keys suppresses the spurious press, and a later press is still detected. |
| TC-30 | The global chord rejects control, alt and partial modifiers | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `global_chord_rejects_control_alt_and_partial_synthetic_modifiers` | The chord is refused for every disallowed modifier, and only keyboard event device paths are allowed. |
| TC-31 | The capability bitmap and the native input ABI are correct | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `capability_bitmap_and_native_abi` | The advertised bitmap decodes the expected keys, and the event struct sizes and the ioctl number match the kernel ABI. |
| TC-32 | The newest focus wins and the lease is stable | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `newest_focus_and_stable_lease` | A newer registrant takes the capture, a repeated heartbeat does not steal it back, and the lease is released on drop. |
| TC-33 | Stale and unready registrations are excluded | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `stale_and_unready_registrations_are_excluded` | A registration that is not ready or whose timestamp is expired never wins the capture. |
| TC-34 | A delayed press cannot recapture after the focus changed | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `delayed_press_cannot_recapture_after_focus_changes` | A press stamped before the focus change is refused, and a later stamp succeeds. |
| TC-35 | The heartbeat is throttled but focus and eligibility publish at once | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `heartbeat_is_throttled_but_focus_and_eligibility_publish_immediately` | A repeated active update does not rewrite the registration, and an eligibility change does. |
| TC-36 | A malformed peer registration does not block a valid capture | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `malformed_peer_registration_does_not_block_valid_capture` | The unreadable peer file is ignored and the capture still succeeds. |
| TC-37 | An unsafe routing directory is rejected | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `unsafe_directory_is_rejected` | A world-readable routing directory is refused at registration. |
| TC-38 | A poisoned event queue keeps its wakeup and its final event | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `poisoned_event_queue_preserves_original_wakeup_and_finished_event` | The queue recovers from a panicking producer and still delivers the finished event. |
| TC-39 | A cancelled constructor never opens the microphone | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `cancelled_constructors_never_open_microphone` | Both the native recorder and the streaming recorder refuse to start and report the cancellation. |
| TC-40 | The chunks are bounded, downmixed, and fail on backpressure | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `bounded_chunks_downmix_and_fail_on_backpressure` | Every chunk stays within the bound, the samples are downmixed, and a full queue marks the capture failed. |
| TC-41 | The filter tail never exceeds the duration cap | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `filter_tail_never_exceeds_duration_cap` | The delivered sample count equals the cap at every supported sample rate. |
| TC-42 | The final upsampled frame cannot exceed the cap | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `upsampling_final_frame_cannot_exceed_cap` | The sample count stops exactly at the cap with one residual sample buffered. |
| TC-43 | The reported level is the latest RMS | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `callback_level_is_latest_rms_not_peak_or_signed_average` | The level matches the RMS of the newest samples and returns to zero for silence. |
| TC-44 | The level downmixes and normalizes the native formats | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `callback_level_downmixes_and_normalizes_native_formats` | Stereo, integer, and float samples all produce the expected level. |
| TC-45 | The level stays finite for invalid float samples | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `callback_level_is_finite_and_bounded_for_invalid_float_samples` | Out-of-range and non-finite samples produce a bounded level. |
| TC-46 | The level is read without consuming events | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `recording_level_reads_callback_atomic_without_consuming_events` | The level is stable across reads, the queued event survives, and it drops to zero after stop or cancel. |
| TC-47 | Stop unparks the capture thread at once | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `stop_unparks_capture_thread_immediately` | The finish call returns well under the parked timeout. |
| TC-48 | The event wait wakes on push and keeps an early permit | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `event_ready_wakes_on_push_and_keeps_early_permit` | An event pushed before the wait is not lost, and a later push wakes a pending wait. |
| TC-49 | Events coalesce but the lifecycle is preserved | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `events_coalesce_but_preserve_lifecycle` | A thousand transcript revisions collapse to one, and the started and finished events stay in place. |
| TC-50 | Stop keeps the token and drop cancels without joining | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `stop_preserves_token_drop_cancels_without_joining` | A successful stop leaves the shared token untouched, and a drop sets the cancel token. |
| TC-51 | Native samples are downmixed and capped without a device | `crates/jcode-voice/src/lib.rs` -> `downmix_and_cap_without_microphone_access` | The buffer downmixes to mono, clamps, and stops at the cap. |
| TC-52 | A cancelled start never opens a device | `crates/jcode-voice/src/lib.rs` -> `cancelled_start_never_opens_a_device` | The constructor reports the cancellation before any device call. |
| TC-53 | Stop joins the worker and returns the audio | `crates/jcode-voice/src/lib.rs` -> `stop_joins_and_returns_audio` | The audio comes back and the shared cancel token is not set. |
| TC-54 | Cancel and drop signal the worker and join it | `crates/jcode-voice/src/lib.rs` -> `cancel_and_drop_signal_worker_and_join` | Both paths set the cancel token and wait for the worker to finish. |
| TC-55 | The WAV encoding and its bounds are enforced | `crates/jcode-voice/src/lib.rs` -> `wav_encoding_and_bounds` | The header is written correctly, every truncation is rejected, and the duration cap is enforced. |
| TC-56 | Invalid input is rejected before the network call | `crates/jcode-voice/src/lib.rs` -> `invalid_input_is_rejected_before_network` | Empty audio, a malformed language code, and an unreachable host all fail without leaking the input. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-57 | A missing socket reports that the companion is unavailable | `crates/jcode-base/src/companion_client.rs` -> `missing_socket_reports_unavailable` | The request returns the `Unavailable` error so the caller can fall back. |
| TC-58 | A failure reply is mapped to the failed error | `crates/jcode-base/src/companion_client.rs` -> `failed_reply_maps_to_failed_error` | The request returns the `Failed` error carrying the companion's message. |
| TC-59 | The companion serves requests over the socket | `crates/jcode-companion/src/server.rs` -> `serves_requests_over_the_socket` | A status request over a bound socket returns a successful reply. |
| TC-60 | A second companion refuses to replace a live one | `crates/jcode-companion/src/server.rs` -> `refuses_to_replace_a_live_companion` | The second bind fails with an "already running" error, and a stale socket file is replaced. |
| TC-61 | Opening a missing path fails without launching anything | `crates/jcode-companion/src/server.rs` -> `open_rejects_missing_paths_without_launching` | The reply is a failure that names the missing path. |
| TC-62 | The configured transcription API needs a key and uses the configured base | `crates/jcode-voice/src/lib.rs` -> `configured_public_api_requires_key_and_uses_configured_base` | Without a key the call is refused, and with a key the request carries the bearer token. |
| TC-63 | The multipart upload matches the backend contract | `crates/jcode-voice/src/lib.rs` -> `multipart_and_bearer_auth_match_backend_contract` | The request posts the WAV as a file part with the bearer token and the optional language field. |
| TC-64 | The language field is optional | `crates/jcode-voice/src/lib.rs` -> `language_is_optional` | No language field is sent when none is requested. |
| TC-65 | The capability probe defaults to false | `crates/jcode-voice/src/lib.rs` -> `capabilities_default_false_and_use_bearer_header` | Only an explicit `voice_transcription: true` makes voice available, and the probe uses the bearer header. |
| TC-66 | Failures never expose credentials or server bodies | `crates/jcode-voice/src/lib.rs` -> `failures_never_expose_credentials_or_server_bodies` | Each error status maps to a typed error whose rendering contains no key and no base URL. |
| TC-67 | Requests time out and redirects are not followed | `crates/jcode-voice/src/lib.rs` -> `requests_time_out_and_redirects_are_not_followed` | A slow response times out, and a redirect is reported as an HTTP error. |
| TC-68 | An oversized response is rejected | `crates/jcode-voice/src/lib.rs` -> `oversized_response_is_rejected` | A body above the size limit is refused. |
| TC-69 | The focused session is resolved from the niri window title | `crates/jcode-voice/src/dictation_tests.rs` -> `focused_jcode_session_uses_niri_window_title_when_process_name_is_generic` | A fake niri and a named child process resolve the session from the title. |
| TC-70 | The focused session is resolved from the client registry | `crates/jcode-voice/src/dictation_tests.rs` -> `focused_cli_session_uses_client_registry_for_task_titled_windows` | A task-titled window still resolves the session through the registry. |
| TC-71 | The last focused session is remembered and read back | `crates/jcode-voice/src/dictation_tests.rs` -> `remember_and_read_last_focused_session` | The session id survives the write and the read. |
| TC-72 | The hotkey listener survives a dropped event stream, a disconnect and a deadline | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `poll_dropped_disconnect_deadline_and_drop` | Each condition produces a cancel edge, and the capture lock is released afterwards. |
| TC-73 | A resync after dropped events keeps a held key and releases a lifted one | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `dropped_events_resync_keeps_a_held_key_and_releases_a_lifted_one` | The resync reports the held state, and the trigger is set only while the key is down. |
| TC-74 | Losing eligibility cancels, but a physical key-up still releases | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `eligibility_cancels_but_physical_key_up_releases` | The eligible case yields a release edge, and the ineligible case yields a cancel edge. |
| TC-75 | A registry failure cancels, and an invalid device list is refused | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `registry_failure_cancels_and_invalid_allowlist_fails` | The capture is cancelled, the listener reports not ready, and the constructor rejects the bad paths. |
| TC-76 | Routing contention retries only while the key is still down | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `routing_contention_retries_only_while_physical_key_remains_down` | The press is delivered after the contention clears when the key is held, and dropped when it was released. |
| TC-77 | A spawned window adopts the held key, or falls back to a tap | `crates/jcode-voice/src/global/hotkey/tests.rs` -> `spawned_window_adopts_a_held_key_or_falls_back_to_a_tap` | The adoption produces a press when the key is held and a tap otherwise, and it happens only once. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-78 | The capture opens during the transcription handshake and is released on a network error | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `orchestration_opens_capture_during_handshake_then_releases_on_network_error` | The microphone is live before the session is configured, the provider error is reported as a rejection, and the capture is released. |
| TC-79 | A setup error releases the capture and reports the provider error | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `orchestration_setup_error_releases_capture_and_reports_provider_error` | The exhausted-credit error surfaces and the capture is released. |
| TC-80 | The construction returns before the microphone or the network are ready | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `construction_returns_before_microphone_or_network_are_ready` | The call returns in under 100 ms while the handshake is still pending. |
| TC-81 | A cancelled slow factory finishes cancelled, without a stale capture | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `cancelled_slow_factory_finishes_cancelled_without_starting_stale_capture` | The recording finishes as cancelled, and the factory observes the cancel token so no stale capture starts. |
| TC-82 | The unified stop finalizes the session, and a drop afterwards keeps the token | `crates/jcode-voice/src/streaming_capture/tests.rs` -> `unified_stop_finalizes_and_drop_after_finished_preserves_token` | The commit is sent, the final empty transcript is delivered, and the drop leaves the shared token untouched. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-83 | No companion is listening, on a headless or remote server | The caller falls back to its own local behavior, and the request reports the companion as unavailable (TC-57, TC-58). |
| TC-84 | The target path does not exist | The open request fails with a message naming the path, and no opener is launched (TC-61, TC-15). |
| TC-85 | A second companion starts while one is already running | The second bind is refused with an "already running" error, and a stale socket file is replaced (TC-60). |
| TC-86 | The server stops renewing the activity lease | The override is released when the lease expires, and the release is logged (TC-12). |
| TC-87 | The owner is killed while holding the lid override | The next process restores the original settings from the journal, and never restores the blocked value (TC-4, TC-5, TC-7). |
| TC-88 | The macOS `pmset` call fails because the sudoers rule is missing | The override is skipped, the failure is logged once, and the sudoers hint is shown; the retry latch resets on the idle transition (TC-8, TC-9). |
| TC-89 | The block fails and the rollback also fails | The journal is kept so a later run can restore it, and the combined failure is reported. This branch has no automated test and is verified manually. |
| TC-90 | No global device is configured | The companion starts no push-to-talk listener at all. This path has no automated test and is verified manually. |
| TC-91 | The desktop notification daemon is unavailable | The recording is refused before the microphone is opened. This path has no automated test and is verified manually. |
| TC-92 | The desktop session is locked | The press is denied and the transcript is not delivered. This path has no automated test and is verified manually. |
| TC-93 | The Nari key is missing, the credits are exhausted, or the request times out | Each failure maps to its own short message, and the capture is released in every case (TC-14, TC-66, TC-67, TC-79). |
| TC-94 | The focused window is not a jcode client | No session is resolved, and the press is ignored (TC-71, and `focused_cli_session_ignores_unrelated_windows` in `crates/jcode-voice/src/dictation_tests.rs`). |
| TC-95 | An ordinary key is pressed, or a control, alt or partial modifier is held | The chord is refused, and only the configured keyboard event devices are ever opened (TC-30, TC-31, TC-37). |
| TC-96 | The request line is not valid JSON, or is longer than 64 KiB | The companion answers with an error instead of dropping the connection, and the server keeps serving later requests. The malformed-request reply has no automated test. |
| TC-97 | The transcript contains a key, and the provider returns a body with a key | Neither the rendered error nor the log contains the key or the base URL (TC-66). |

## Test Infrastructure

- The test files that back this plan, all of which exist in the repository:
  - `crates/jcode-base/src/companion_client.rs`, inline `#[cfg(test)] mod tests`: the socket client.
  - `crates/jcode-companion/src/server.rs`, inline `#[cfg(test)] mod tests`: the socket server and its request handlers.
  - `crates/jcode-companion/src/lid_override.rs`, inline `#[cfg(test)] mod tests`: the lid override, its journal, and the platform parsers.
  - `crates/jcode-companion/src/voice.rs`, inline `#[cfg(test)] mod tests`: the global voice failure labels.
  - `crates/jcode-desktop-open/src/lib_tests.rs`: the target parsing and the browser window selection.
  - `crates/jcode-voice/src/dictation_tests.rs`: the dictation command, the session resolution, and the process inspection helpers.
  - `crates/jcode-voice/src/global/hotkey/tests.rs`: the evdev hotkey decoder, the routing registry, and the device allowlist.
  - `crates/jcode-voice/src/streaming_capture/tests.rs`: the streaming orchestration, the event queue, and the audio level.
  - `crates/jcode-voice/src/lib.rs`, inline `#[cfg(test)] mod tests`: the transcription HTTP client, the WAV validation, and the native capture buffer.
- The `Fake` backend in the lid override tests stands in for the macOS and Windows power settings, so no test touches the machine's power plan.
- The hotkey tests use a private anonymous pipe and a fake `niri` script, so no test opens a physical input device or touches a live compositor.
- The transcription tests use a local TCP mock server, so no test reaches the live transcription service.
- The `voice-capture` feature gates the native capture and level tests, and the `linux` and `unix` targets gate the evdev, socket, and `/proc` tests.
- Fixtures needed: a temporary `JCODE_HOME` with an `active_pids` directory and a `client_sessions` registry, a temporary socket directory, and a temporary routing directory.
- Run the whole area with `cargo test -p jcode-companion -p jcode-voice -p jcode-desktop-open`, and the client with `cargo test -p jcode-base companion_client`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-13, TC-59, TC-60 |
| FR-2 | TC-1, TC-57, TC-58, TC-59 |
| FR-3 | TC-13, TC-31, TC-85 |
| FR-4 | TC-15, TC-61, TC-84 |
| FR-5 | TC-15, TC-16 |
| FR-6 | TC-1, TC-59 |
| FR-7 | TC-57, TC-58, TC-83 |
| FR-8 | TC-2, TC-3, TC-6, TC-12, TC-86 |
| FR-9 | TC-4, TC-5, TC-7, TC-8, TC-11, TC-87, TC-88, TC-89 |
| FR-10 | TC-22, TC-23, TC-24, TC-25, TC-26, TC-27, TC-28, TC-29, TC-69, TC-70, TC-72, TC-73, TC-74, TC-77, TC-94 |
| FR-11 | TC-30, TC-37, TC-75, TC-90, TC-95 |
| FR-12 | TC-90, TC-91 |
| FR-13 | TC-21, TC-22, TC-23, TC-24, TC-25, TC-26, TC-71 |
| FR-14 | TC-38, TC-39, TC-40, TC-48, TC-55, TC-62, TC-63, TC-64, TC-78, TC-79, TC-81, TC-82 |
| FR-15 | TC-18, TC-19, TC-20 |
| FR-16 | TC-17, TC-18, TC-19, TC-20 |
| FR-17 | TC-32, TC-33, TC-34, TC-35, TC-36, TC-75, TC-76, TC-77 |
| NFR-1 | TC-59, TC-80 |
| NFR-2 | TC-38, TC-39, TC-41, TC-42, TC-43, TC-44, TC-45, TC-46, TC-47, TC-49, TC-50, TC-51, TC-52, TC-53, TC-54, TC-81, TC-82 |
| NFR-3 | TC-14, TC-55, TC-56, TC-65, TC-66, TC-67, TC-68, TC-97 |
| NFR-4 | TC-30, TC-31, TC-37, TC-64, TC-65, TC-68, TC-95, TC-96 |
| NFR-5 | TC-4, TC-5, TC-8, TC-12, TC-85, TC-87 |
| NFR-6 | TC-92 |
| NFR-7 | TC-14, TC-57, TC-83, TC-88, TC-93 |
| NFR-8 | TC-9, TC-10, TC-11, TC-13 |
