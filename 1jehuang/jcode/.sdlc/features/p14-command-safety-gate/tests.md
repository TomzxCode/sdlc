---
title: "Command Safety Gate"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Command Safety Gate

## Scope

Tests the two-stage command safety gate: the deterministic blast-radius classifier in `crates/jcode-command-risk` and the wiring of that classifier into the `bash` and `apply_patch` tools.
Out of scope: the rest of the tool suite, the ambient-mode permission system described in `docs/SAFETY_SYSTEM.md`, and any OS-level confinement of the agent's processes.

Test files referenced below, all verified to exist in the repository:

- `crates/jcode-command-risk/src/assess_tests.rs`
- `crates/jcode-command-risk/src/gate_tests.rs`
- `crates/jcode-command-risk/src/paths_tests.rs`
- `crates/jcode-command-risk/src/tokenize_tests.rs`
- `crates/jcode-app-core/src/tool/bash_destructive_gate.rs` (inline `mod tests`)
- `crates/jcode-app-core/src/tool/bash_tests.rs`
- `crates/jcode-app-core/src/tool/apply_patch_tests.rs`

## Unit Tests

The classifier crate is exercised through pure functions, so the assessment tests are unit tests at the crate boundary.

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Blast-radius classification rather than command name | `crates/jcode-command-risk/src/assess_tests.rs` (`non_rm_destructive_tools_are_covered`, `deleting_concrete_paths_outside_the_project_runs_immediately`, `concrete_truncating_redirect_outside_cwd_runs_immediately`) | `find /home/u -delete` is Catastrophic, `dd if=/dev/zero of=/dev/sda` does not run immediately, a concrete out-of-workspace delete is Low |
| TC-2 | The catastrophic target set | `crates/jcode-command-risk/src/assess_tests.rs` (`the_issue_604_command_is_blocked_outright`, `root_destruction_is_blocked_outright`, `credential_theft_or_destruction_is_blocked`, `files_inside_system_directories_are_protected_too`) | Every spelling of the home directory, `/`, `/etc`, `/usr`, `~/.ssh`, `~/.gnupg`, `~/.aws`, and files inside the recursively protected system paths are Catastrophic |
| TC-3 | Chaining and separators | `crates/jcode-command-risk/src/assess_tests.rs` (`chaining_does_not_bypass_the_gate`, `no_separator_launders_a_catastrophic_command`, `the_worst_finding_in_a_chain_wins`, `shell_constructs_do_not_hide_catastrophic_commands`) | No separator form (`&&`, `||`, `;`, `|`, newline) launders a catastrophic command, and the worst finding in a chain wins |
| TC-4 | Routine in-project work is not interrupted | `crates/jcode-command-risk/src/assess_tests.rs` (`routine_cleanup_inside_the_project_is_not_blocked`, `no_routine_project_command_triggers_a_prompt`, `issue_725_read_only_and_bounded_commands_run_immediately`) | Cleanup inside the project, bounded globs, and read-only commands all run immediately |
| TC-5 | Unknown targets escalate | `crates/jcode-command-risk/src/assess_tests.rs` (`runtime_computed_targets_require_justification`, `destructive_command_without_a_visible_target_escalates`) | An unresolved variable, a command substitution, and a destructive verb with no visible target all reach at least Confirm |
| TC-6 | Wrapper unwrapping | `crates/jcode-command-risk/src/assess_tests.rs` (`wrapper_commands_do_not_hide_the_real_program`, `nested_wrappers_are_unwrapped_all_the_way_down`, `a_wrapper_hiding_an_unparseable_payload_escalates`, `ordinary_wrapped_commands_still_run_immediately`, `wrapper_value_flags_and_unbounded_globs_remain_guarded`) | The destructive program under any wrapper is Catastrophic, an unparseable payload escalates, and ordinary wrapped commands stay quiet |
| TC-7 | Inline shell scripts and command substitution | `crates/jcode-command-risk/src/assess_tests.rs` (`inline_shell_scripts_are_assessed_not_skipped`, `issue_1753_substitutions_are_assessed_like_top_level_commands`, `issue_1753_inert_text_stays_safe`) | `sh -c "rm -rf ~"` and `$(rm -rf ~)` are Catastrophic, while quoted heredoc bodies and single-quoted text stay Safe |
| TC-8 | Operands supplied by a pipe | `crates/jcode-command-risk/src/assess_tests.rs` (`piped_deletes_cannot_launder_their_targets`) | `find ~ -type f \| xargs rm -rf` does not run immediately, because the affected set is invisible to the parser |
| TC-9 | `find` actions | `crates/jcode-command-risk/src/assess_tests.rs` (`read_only_find_actions_do_not_delete_search_roots`, `find_mutating_and_unknown_actions_remain_protected`, `find_output_actions_write_only_their_destinations`) | Read-only `-exec` payloads are Safe, mutating or unknown payloads are held or denied, and `-fprint` writes only its destination |
| TC-10 | Redirects and sinks | `crates/jcode-command-risk/src/assess_tests.rs` (`appending_is_not_treated_as_destructive`, `harmless_command_operands_are_not_redirect_targets`, `safe_redirect_sink_does_not_make_explicit_deletion_safe`, `read_only_find_with_stderr_redirect_is_safe`, `read_only_early_returns_preserve_redirect_checks`) | Only `>` marks a truncating target, `>>` and `/dev/null` do not, and a redirect to a protected path is still caught after a read-only early return |
| TC-11 | Environment printing and command lookup | `crates/jcode-command-risk/src/assess_tests.rs` (`environment_printing_and_command_lookup_are_read_only`, `reassignment_does_not_override_trusted_protection`, `env_split_strings_cannot_be_mistaken_for_printing`) | `env`, `env -u`, and `command -v` are Safe, a `HOME=` reassignment does not weaken the protected paths, and `env -S` is held |
| TC-12 | Heredoc bodies are data, not shell source | `crates/jcode-command-risk/src/assess_tests.rs` (`issue_922_heredoc_payload_does_not_trip_the_gate`, `heredoc_inside_double_quoted_command_substitution_is_data`) | A heredoc body that mentions `rm` does not trip the gate, while a real command after the terminator is still assessed |
| TC-13 | Assessment totality, ordering, and explanations | `crates/jcode-command-risk/src/assess_tests.rs` (`assessment_is_total_over_garbage_input`, `severity_ordering_is_monotonic`, `catastrophic_cannot_be_unlocked_but_confirm_can`, `explanation_names_the_offending_target`) | Garbage input never panics, the level ordering is monotonic, Catastrophic is an absolute deny while Confirm is not, and the explanation names the path |
| TC-14 | Protected path resolution | `crates/jcode-command-risk/src/paths_tests.rs` (`home_directory_is_catastrophic_in_every_spelling`, `parent_traversal_out_of_home_reaches_root_and_is_caught`, `root_and_system_paths_are_catastrophic`, `credential_stores_inside_home_are_catastrophic`, `ordinary_project_paths_are_not_catastrophic`, `home_subdirectory_is_not_itself_catastrophic`, `individual_credential_files_are_protected_not_just_their_directory`, `ordinary_config_files_remain_editable`, `missing_home_context_does_not_panic_or_misfire`, `normalize_never_escapes_above_root`) | Every spelling of the home directory resolves to the same verdict, `..` traversal reaches and is caught at root, credential files are protected, and ordinary config files stay editable |
| TC-15 | Target classification tiers | `crates/jcode-command-risk/src/paths_tests.rs` (`inside_working_directory_is_low_risk_not_confirm`, `non_recursive_delete_inside_cwd_is_unremarkable`, `concrete_outside_working_directory_target_is_low_risk`, `temp_paths_are_exempt`, `glob_over_a_protected_directory_is_catastrophic`, `unresolvable_targets_escalate_rather_than_pass`, `known_variable_logs_are_bounded_but_unknown_expansions_still_confirm`, `known_variables_do_not_bypass_protected_paths`) | A recursive delete inside the working directory is Low, a temp path produces no finding, a glob over a protected directory is Catastrophic, and an unknown expansion is Confirm |
| TC-16 | Tokenizer quoting, chaining, and flag detection | `crates/jcode-command-risk/src/tokenize_tests.rs` (all thirteen tests) | Quoting and escaping resolve to one target word, chained and piped commands split into separate segments, `>` is marked while `>>` is not, recursive flags are detected in bundles, and malformed input never panics |
| TC-17 | Gate outcomes and justification substance | `crates/jcode-command-risk/src/gate_tests.rs` (all nine tests) | Safe and Low allow, Catastrophic denies even with a perfect justification, Confirm reflects with a prompt that names the target, a blind retry is held again, and bare affirmations do not unlock the gate |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-18 | The gate policy at the tool seam | `crates/jcode-app-core/src/tool/bash_destructive_gate.rs` inline `mod tests` (`scratch_log_and_backup_commands_do_not_require_justification`, `protected_writes_and_unknown_variables_remain_blocked`) | Scratch log and backup commands are not held, while `rm -rf /etc`, `echo bad > /etc/passwd`, `find /etc -type f -exec rm {} \;`, and `echo test > "$UNKNOWN/tests.log"` are all refused |
| TC-19 | The bash schema exposes the `justification` field | `crates/jcode-app-core/src/tool/bash_tests.rs` (`bash_optional_nulls_use_omitted_defaults`, `bash_executes_with_null_optional_arguments`) | An explicit `null` justification is treated as absent, and a call carrying a null justification still runs |

## End-to-End Tests

These drive the real tool entry points and observe filesystem effects.

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-20 | The bash tool refuses to delete the home directory | `crates/jcode-app-core/src/tool/bash_tests.rs` (`bash_refuses_to_delete_the_home_directory`): set `HOME` to a temp directory, place a canary file in it, call `bash` with `rm -rf $HOME` | The call fails with a refusal that says the command is blocked, and the canary file still exists |
| TC-21 | The bash tool holds a risky delete until it is justified | `crates/jcode-app-core/src/tool/bash_tests.rs` (`bash_holds_a_risky_delete_until_justified_then_runs_it`): call `bash` with a glob delete outside the workspace, then repeat it, then repeat it with a `justification` | The first attempt and the blind retry are both held with a prompt naming the justification, and the justified attempt runs and deletes the target |
| TC-22 | The bash tool does not interfere with ordinary commands | `crates/jcode-app-core/src/tool/bash_tests.rs` (`bash_does_not_interfere_with_ordinary_commands`): run `echo hello`, `rm -rf build`, and `ls -la` in a temp working directory | All three run untouched |
| TC-23 | Background dispatch cannot bypass the gate | `crates/jcode-app-core/src/tool/bash_tests.rs` (`indirect_dispatch_paths_cannot_bypass_the_gate`): call `bash` with `run_in_background` set and the command `rm -rf $HOME` | The call fails with a refusal, and the canary file still exists |
| TC-24 | `apply_patch` refuses a protected path | `crates/jcode-app-core/src/tool/apply_patch_tests.rs` (`apply_patch_refuses_to_delete_a_protected_path`): set `HOME` to a temp directory, create `.ssh/id_ed25519`, delete it by absolute path through a patch | The tool reports a refusal, and the credential file still exists |
| TC-25 | `apply_patch` still deletes ordinary files | `crates/jcode-app-core/src/tool/apply_patch_tests.rs` (`apply_patch_still_deletes_ordinary_files`): delete an ordinary file by absolute path through a patch | The delete succeeds and the file is gone |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-26 | Empty, whitespace-only, or unbalanced-quote command input | The assessment returns a verdict and never panics, because `assess` is total over its input (`crates/jcode-command-risk/src/assess_tests.rs::assessment_is_total_over_garbage_input`, `crates/jcode-command-risk/src/tokenize_tests.rs::tokenizing_is_total_and_never_panics`) |
| TC-27 | `HOME` is unset on the host | The system-path tier still applies and the classifier does not panic or misfire on ordinary paths (`crates/jcode-command-risk/src/paths_tests.rs::missing_home_context_does_not_panic_or_misfire`) |
| TC-28 | Pathological `..` input such as `/../../../../..` | Normalization stops at `/`, and the result stays catastrophic (`crates/jcode-command-risk/src/paths_tests.rs::normalize_never_escapes_above_root`) |
| TC-29 | The command reassigns `HOME=` or `JCODE_SCRATCH_DIR=` | The trusted protected paths still apply and the command is held (`crates/jcode-command-risk/src/assess_tests.rs::reassignment_does_not_override_trusted_protection`) |
| TC-30 | The model retries the identical held command | The same refusal is returned and nothing is deleted (`crates/jcode-app-core/src/tool/bash_tests.rs::bash_holds_a_risky_delete_until_justified_then_runs_it`, `crates/jcode-command-risk/src/gate_tests.rs::a_blind_retry_does_not_satisfy_the_gate`) |
| TC-31 | The justification is a bare affirmation such as `yes`, `ok`, or `proceed.` | The command stays held, because the justification carries no information about intent (`crates/jcode-command-risk/src/gate_tests.rs::empty_affirmations_are_rejected`, `crates/jcode-command-risk/src/gate_tests.rs::justification_substance_check_is_a_low_but_real_bar`) |
| TC-32 | The command is dispatched in the background | The background path is gated as well, because the check sits at the single `Tool::execute` chokepoint (`crates/jcode-app-core/src/tool/bash_tests.rs::indirect_dispatch_paths_cannot_bypass_the_gate`) |
| TC-33 | The host runs Windows, where the `bash` tool drives `cmd.exe` | The gate still runs and denies a syntactically recognised destructive command, but `cmd.exe`-specific destructive verbs are not classified. The gate module's own tests are compiled only on non-Windows hosts, so this scenario has no automated coverage today |

## Test Infrastructure

- A synthetic `RiskContext` with `working_dir=/home/u/proj`, `home_dir=/home/u`, and `scratch_dir=/home/u/.jcode/scratch` drives the crate-level tests.
- The tool-level tests use a real `tempfile::tempdir()` as the home directory, with a canary file as the observable effect.
- The tool-level tests set and restore the `HOME` environment variable, so they mutate process-global state and must not run concurrently with other tests that read `HOME`.
- `jcode-command-risk` declares `tempfile` as its only dev-dependency and no runtime dependencies, so the classifier is exercised without the agent runtime.
- Test environment: `cargo test -p jcode-command-risk` and `cargo test -p jcode-app-core`.
- The gate module's own tests and the destructive-gate bash tests are compiled only on non-Windows hosts, so the Windows build has no direct coverage of the policy seam.
- No benchmark harness pins the latency budget in NFR-1, and no test asserts the absence of file reads in NFR-2, because both properties are enforced by construction rather than by an assertion.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-13, TC-20 |
| FR-2 | TC-1, TC-9, TC-10 |
| FR-3 | TC-2, TC-3, TC-17 |
| FR-4 | TC-2, TC-14 |
| FR-5 | TC-5, TC-17, TC-21 |
| FR-6 | TC-17, TC-21, TC-30 |
| FR-7 | TC-5, TC-6, TC-8, TC-9, TC-15 |
| FR-8 | TC-24, TC-25 |
| FR-9 | TC-6 |
| FR-10 | TC-3, TC-16 |
| FR-11 | TC-10, TC-15 |
| FR-12 | TC-4, TC-22 |
| FR-13 | TC-20, TC-23 |
| FR-14 | TC-18 |
| FR-15 | TC-14 |
| NFR-1 | TC-13 |
| NFR-2 | TC-13, TC-14 |
| NFR-3 | TC-13, TC-16, TC-26 |
| NFR-4 | TC-13 |
| NFR-5 | TC-1 |
| NFR-6 | TC-17, TC-20 |
| NFR-7 | TC-4, TC-22 |
| NFR-8 | TC-18 |
