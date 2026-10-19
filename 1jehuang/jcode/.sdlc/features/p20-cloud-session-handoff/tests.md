---
title: "Cloud Session Handoff"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Cloud Session Handoff

## Scope

Covers the lease that decides which machine owns a session, the move that hands a session to a cloud host, the return that merges the cloud work back, the `where` and `attach` commands, the `/cloud` and `/local` TUI commands, and the Jade cloud session upload surface that shares the `jcode cloud` command tree.

Test files that exist for this feature:

- `crates/jcode-storage/src/session_lease.rs`, the inline `mod tests` block, covering the lease read, write, and block decision.
- `crates/jcode-tui/src/tui/app/commands_cloud.rs`, the inline `mod tests` block, covering the `/cloud` and `/local` parser.
- `crates/jcode-app-core/src/agent/idle_hibernation.rs`, the inline `mod tests` block, covering the lease guard on the session save path.
- `src/cli/args/tests.rs`, covering the parsing of the `jcode cloud sessions` subcommands.
- `src/cli/commands_tests.rs`, covering the Jade config, the helper argument contract, the sync candidate selection, the sync throttle, and the dashboard rendering.
- `scripts/test_cloud_move_e2e.sh`, a two-machine end-to-end script for `jcode cloud move` and `jcode cloud return`.
- `scripts/test_cloud_move_agent_e2e.sh`, an agent-level end-to-end script with real model turns on both machines.
- `scripts/test_cloud_move_tui_e2e.sh`, an interactive end-to-end script that drives the TUI over SSH.

Files and paths with no test coverage for this feature:

- `src/cli/cloud_move.rs` has no `mod tests` block at all. Every function in it, including `run_move`, `run_return`, `run_receive`, `run_activate`, `run_export`, `run_where`, `snapshot_repo`, `restore_repo`, and `merge_back`, is covered only by the three shell scripts.
- `src/cli/args/tests.rs` does not parse `jcode cloud move`, `jcode cloud return`, `jcode cloud where`, or `jcode cloud attach`, so the flags of the handoff commands have no parsing test.
- `crates/jcode-app-core/src/agent/turn_execution.rs`, `crates/jcode-app-core/src/agent/turn_loops.rs`, and `crates/jcode-app-core/src/agent/turn_streaming_mpsc.rs` have no test that asserts the lease block stops a turn.
- `crates/jcode-app-core/src/agent_tests.rs` calls `ensure_session_lease()` in `saved_account_restore_mismatch_blocks_model_turn` and in the account-route test, but both assert the account-restore error, not the lease block.
- `crates/jcode-base/src/session/persistence.rs` has a test module, but it does not exercise the lease guard in `save_inner`. That guard is covered by the idle hibernation test.
- No Rust integration test under `tests/` covers the handoff. The three shell scripts are not referenced by any workflow in `.github/workflows/`, so they run only when a person invokes them.

Out of scope: the Jade cloud index and its S3 storage, the managed AWS control plane described in `docs/JCODE_CLOUD_AWS.md`, the native SSH attach implementation that `jcode cloud attach` reuses, and the migration of background processes and dev servers.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | A session with no lease is never blocked | `crates/jcode-storage/src/session_lease.rs` (`no_lease_never_blocks`) | With no lease file, `session_lease_block` returns nothing for any epoch |
| TC-2 | A moved-away lease blocks every copy | `crates/jcode-storage/src/session_lease.rs` (`moved_away_blocks_every_copy`) | With a lease at epoch 3 and an away host, a copy at epoch 3 is blocked with the `MovedAway` variant |
| TC-3 | A returned lease blocks only stale copies | `crates/jcode-storage/src/session_lease.rs` (`returned_session_blocks_only_stale_copies`) | With a lease at epoch 4 and no away host, a copy at epoch 2 is blocked with the `StaleCopy` variant and a copy at epoch 4 is not |
| TC-4 | A path-like session id is rejected | `crates/jcode-storage/src/session_lease.rs` (`rejects_path_like_ids`) | Reading the lease for `../x` returns nothing and writing it fails with an invalid session id error |
| TC-5 | The `/cloud` and `/local` parser | `crates/jcode-tui/src/tui/app/commands_cloud.rs` (`parses_cloud_commands`) | `/cloud` moves with no host, `/cloud my-box` moves to that host, `/local` and `/cloud back` return, `/cloud status` reports the location, and `/cloudy` is not claimed |
| TC-6 | A blocked copy does not write the session | `crates/jcode-app-core/src/agent/idle_hibernation.rs` (`idle_hibernation_does_not_write_session_and_refuses_migration_lease`) | With a lease that names an away host, `save_prepared` succeeds without writing, the file on disk is byte for byte unchanged, and the hibernation is refused |
| TC-7 | The Jade helper argument contract | `src/cli/commands_tests.rs` (`cloud_sessions_args_match_jade_helper_contract`) | The helper is called with the documented subcommand, the user id, the profile, the region, and the format flags, in that order |
| TC-8 | The Jade config keeps the secret out of the arguments | `src/cli/commands_tests.rs` (`cloud_sessions_config_persists_secret_and_feeds_helper_env_without_args`) | The config file is written with mode `0o600`, the token is passed to the helper through the environment, the token never appears in the argument list, and `--clear` removes the file |
| TC-9 | The syncable session file filter | `src/cli/commands_tests.rs` (`is_syncable_session_stem_filters_non_session_files`) | `session_abc_123` and `imported_codex_456` are syncable, and `req`, `test_selfdev_session`, and `session_abc.journal` are not |
| TC-10 | The sync candidate collection | `src/cli/commands_tests.rs` (`collect_sync_candidates_picks_only_session_json`) | Only the real session JSON files in the directory are collected, and the backups and journals are skipped |
| TC-11 | A sync dry run does not upload and does not write state | `src/cli/commands_tests.rs` (`cloud_sessions_sync_dry_run_reports_without_uploading_or_writing_state`) | The run succeeds, the helper that would fail is never invoked, and no sync state file is created |
| TC-12 | The sync throttle | `src/cli/commands_tests.rs` (`cloud_sessions_sync_respects_min_interval_throttle`) | With a recent `last_sync_at` and `--min-interval-mins 60`, the run returns successfully without invoking the helper and without recording the session as uploaded |
| TC-13 | The dashboard HTML escapes the session data | `src/cli/commands_tests.rs` (`render_cloud_sessions_dashboard_html_escapes_and_lists_rows`) | The title markup is escaped, both sessions are listed, and numeric and string message counts both render |
| TC-14 | The dashboard HTML with no sessions | `src/cli/commands_tests.rs` (`render_cloud_sessions_dashboard_html_handles_empty`) | The page reports zero sessions and the empty-state message |
| TC-15 | The dashboard HTML links the generated viewers | `src/cli/commands_tests.rs` (`render_cloud_sessions_dashboard_html_links_rows_with_view_files`) | A session with a viewer file gets an anchor to it, and a session without one stays plain text |
| TC-16 | The `jcode cloud sessions` argument parsing | `src/cli/args/tests.rs` (`cloud_sessions_subcommands_parse`, and the `jcode cloud sessions dashboard` assertions in `model_list_subcommand_parses`) | `configure`, `status`, `upload-latest`, `view`, and `sync` parse with their flags, and `dashboard` parses with `--limit`, `--open`, `--with-view`, and `--user-id` |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-17 | The staged move and the cloud checkout | `scripts/test_cloud_move_e2e.sh`, steps 1 to 4, with `JCODE_BIN` pointing at the binary under test | A dry run writes no lease and leaves the working tree and the index unchanged. The real move writes a local lease with `away_host` set, restores the repository on the cloud host at the same absolute path with the same uncommitted, untracked, and staged files, copies the allowlisted `.env` but not the ignored build output, keeps the same HEAD, branch, and git identity, installs the transcript and the todos, and writes a cloud lease with no away host. The shipped transcript carries the migration notice, the dangling tool call is closed, and the migration epoch is 1. A second move is refused, and `jcode cloud where` shows the cloud host |
| TC-18 | The return merges both sides | `scripts/test_cloud_move_e2e.sh`, step 5, after the cloud side commits and the local side edits a different hunk | The report says the merge was applied, the local branch is fast-forwarded to the cloud commits, the cloud file and the cloud uncommitted edit are present, the local edit in the same file survives, the local-only file survives, the ignored build output is untouched, the local lease names no away host, the cloud lease records `away_host` as `returned`, and the returned transcript holds the cloud turn, the return notice, and migration epoch 2 |
| TC-19 | A second round trip with a real conflict | `scripts/test_cloud_move_e2e.sh`, step 6 | The second move reuses the cloud checkout, the return reports conflicts and names the conflicting file, the local file is byte for byte unchanged, and the cloud work is reachable at `refs/jcode-cloud/session_abc/cloud` |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-20 | A real turn on each side of the handoff | `scripts/test_cloud_move_agent_e2e.sh`, with the fake OpenAI-compatible server in `scripts/fake_openai_server.py` | A real local turn runs, the session moves, the local copy is then refused with a message that names the cloud host, the cloud model sees the migration notice and the full earlier conversation, the return reports the merge as applied, the cloud file is present locally, and the final local turn sees the laptop turn, the cloud turn, the return notice, and the new prompt, with the blocked prompt absent from the transcript |
| TC-21 | The interactive TUI handoff over SSH | `scripts/test_cloud_move_tui_e2e.sh`, with a user-level `sshd` as the cloud host and the TUI in `tmux` | The local turn is answered, `/cloud` reattaches over SSH and the agent auto-continues on the cloud and sees the migration notice, the laptop lease names the cloud host, the cloud checkout holds the uncommitted laptop edit, `/local` brings the session back with the cloud edit merged into the laptop checkout, the laptop lease names no away host, and the final local context holds the whole history including the return notice |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-22 | Neither `--host` nor `JCODE_CLOUD_HOST` is set | The move fails and the message names both sources |
| TC-23 | The cloud host runs a jcode that does not know `cloud receive` | The move fails in the preflight, before any state changes, and the message names the host and the remedy |
| TC-24 | The session already lives on another host | The move is refused and the message says to run `jcode cloud return` first. Proven by TC-17, which checks that a second move is refused |
| TC-25 | A turn is in flight and `--allow-active` is absent | The move is refused and the message says the session is mid-turn |
| TC-26 | A dry run | The cloud copy is staged and verified, no lease is written locally, and the working tree and the index are unchanged. Proven by TC-17 |
| TC-27 | The cloud host stages the move but fails to activate | The local lease is restored to its previous value, or removed when there was none, and the session stays local |
| TC-28 | The cloud checkout holds work jcode did not place there | The receive is refused, the message names the path, and the existing files are left alone |
| TC-29 | The incoming transfer format version is not supported | The receive is refused and the expected format version is named |
| TC-30 | The old machine tries to run the session after the move | The turn is refused with a message that names the new host. Proven by TC-20 |
| TC-31 | The return merges conflicting edits | The local working tree is untouched, no conflict markers are written, the cloud work stays reachable at `refs/jcode-cloud/session_abc/cloud`, and the transcript names the conflicting files. Proven by TC-19 |
| TC-32 | A stale in-memory copy tries to save after the session came back | The save is skipped, the on-disk transcript is unchanged, and the block reason says the copy is stale. Partly proven by TC-6 |
| TC-33 | The export is asked for an epoch that is not newer than the host epoch | The export is refused and both epochs are reported |
| TC-34 | The export fails after the host stopped owning the session | The host takes ownership back, so the session stays usable there |
| TC-35 | A turn is in flight on the cloud host when the export runs | The export is refused and the host keeps ownership |
| TC-36 | The repository has no commits yet | The move fails in the prepare stage and asks for one commit first |
| TC-37 | A session id contains a path separator or starts with a dot | The lease write fails and nothing is written outside the lease directory. Proven by TC-4 |

## Test Infrastructure

- The three shell scripts take the binary under test through the `JCODE_BIN` environment variable, and they run the binary with `--no-update --no-selfdev` so no daemon is restarted.
- `scripts/test_cloud_move_e2e.sh` and `scripts/test_cloud_move_agent_e2e.sh` build a fake cloud host with `bubblewrap`, giving it its own `HOME`, its own `JCODE_HOME`, and its own private copy of the repository at the same absolute path. They need `bwrap` and `python3` on the machine.
- `scripts/test_cloud_move_e2e.sh` and `scripts/test_cloud_move_agent_e2e.sh` stand in for `ssh cloud-e2e` with a transport script, driven by `JCODE_CLOUD_TRANSPORT`, and point the remote binary at a copy of the binary under test.
- `scripts/test_cloud_move_agent_e2e.sh` and `scripts/test_cloud_move_tui_e2e.sh` use the fake OpenAI-compatible server in `scripts/fake_openai_server.py`, which logs every request so the test can assert what the model actually saw.
- `scripts/test_cloud_move_tui_e2e.sh` needs a user-level `sshd`, `ssh-keygen`, and `tmux`, and it drives the TUI by sending keys and capturing panes.
- The lease tests redirect `JCODE_HOME` to a temporary directory and take the shared test-home lock from `crates/jcode-storage/src/lib.rs`, so they never touch the real `~/.jcode`.
- The Jade command tests take the shared environment lock and a temporary `JCODE_HOME`, and they use a helper script that exits non-zero to prove the helper is never invoked.
- The three shell scripts are not referenced by any workflow in `.github/workflows/`, so they are not part of the CI run today and have to be started by hand.
- The edge cases TC-22, TC-23, TC-25, TC-27, TC-28, TC-29, TC-33, TC-34, TC-35, and TC-36 record required behavior that no automated test proves today. In the coverage matrix they are listed as the expected-behavior reference rather than as an automated proof.
- The handoff has no Rust test module of its own, so every function in `src/cli/cloud_move.rs` depends on the shell scripts for coverage.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-17, TC-18, TC-19, TC-20, TC-21 |
| FR-2 | TC-17, TC-24 |
| FR-3 | none, see TC-25 and TC-35 for the required behavior |
| FR-4 | TC-17, TC-26 |
| FR-5 | TC-17, TC-18, TC-20, TC-33 |
| FR-6 | none, see TC-23 for the required behavior |
| FR-7 | TC-17, TC-36 |
| FR-8 | TC-17 |
| FR-9 | TC-17 |
| FR-10 | TC-17, TC-20 |
| FR-11 | TC-17 |
| FR-12 | TC-17, TC-27, TC-34, TC-35 |
| FR-13 | none, see TC-28 for the required behavior |
| FR-14 | TC-18, TC-20 |
| FR-15 | TC-18, TC-20 |
| FR-16 | TC-18, TC-19, TC-20 |
| FR-17 | TC-19, TC-31 |
| FR-18 | none, see TC-19 for the ref that the same merge path writes |
| FR-19 | TC-18, TC-20, TC-21 |
| FR-20 | TC-18, TC-21 |
| FR-21 | none, see TC-24 for the parallel move refusal |
| FR-22 | TC-17 |
| FR-23 | TC-21 |
| FR-24 | TC-20, TC-21, TC-22 |
| FR-25 | TC-2, TC-3, TC-4, TC-17, TC-18, TC-21 |
| FR-26 | TC-2, TC-20, TC-30 |
| FR-27 | TC-3, TC-6, TC-32 |
| FR-28 | TC-1, TC-6 |
| FR-29 | TC-5, TC-21 |
| FR-30 | none, see TC-5 for the parser and TC-21 for the TUI round trip |
| FR-31 | TC-7, TC-8, TC-13, TC-14, TC-15, TC-16 |
| FR-32 | TC-8, TC-16 |
| FR-33 | TC-9, TC-10, TC-11, TC-12 |
| NFR-1 | TC-17, TC-18, TC-20 |
| NFR-2 | TC-2, TC-3, TC-6, TC-20, TC-30 |
| NFR-3 | TC-18, TC-19, TC-31 |
| NFR-4 | none, see TC-17 and TC-18 for the lease reads that depend on it |
| NFR-5 | TC-8, TC-9, TC-17 |
| NFR-6 | TC-4, TC-37 |
| NFR-7 | TC-17, TC-27 |
| NFR-8 | TC-17 |
| NFR-9 | none, see TC-23 for the required behavior |
| NFR-10 | none, see TC-29 for the required behavior |
| NFR-11 | none, the stage lines are visible in the shell script output but not asserted |
| NFR-12 | none, the divergence count is printed by `jcode cloud where` in TC-17 but not asserted |
