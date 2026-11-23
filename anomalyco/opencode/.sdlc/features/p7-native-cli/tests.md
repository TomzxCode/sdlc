---
title: "Native Rust CLI"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Test Plan: Native Rust CLI

## Scope

This plan covers the Rust CLI and TUI under `packages/cli-rs`, its plugin system, its server and client-local file behavior, and the parity harnesses that compare it with the TypeScript client.
Test coverage was found in 326 Rust files with test annotations, including 151 files under `crates/*/tests/`, and in 2 TypeScript test files.
The harnesses also contain 4 parity runners, 448 scenario files, 529 committed fixture files, and 136 deviation files.
Manual Windows terminal checks and the optional live service tests are documented but are not part of an automated run.
The package has no `test` script, so repository `turbo test` does not run its slow plugin machine suite.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | CLI inline unit tests in `crates/cli/src/tests/mod.rs` cover argument logging, redaction and shared test helpers | Parsed argument lists and logged argument lists | Secrets are replaced by `<redacted>` and readable diffs are produced |
| TC-2 | CLI parse tests in `crates/cli/src/tests/parse.rs` cover parser branches and flag semantics | Command line invocations and generated parser cases | Parsed commands, flags and usage errors match the TypeScript parser |
| TC-3 | CLI output tests in `crates/cli/src/tests/output.rs` cover help and usage output | Recorded command invocations | Colored and plain output match committed goldens |
| TC-4 | CLI tree tests in `crates/cli/src/tests/tree.rs` cover the static command table | Generated TypeScript command tree | The Rust tree has the same commands, aliases and flags |
| TC-5 | API type and event-name unit tests in `crates/api-types/src` and `crates/api-types/tests/event_names.rs` cover generated types and raw event names | Encoded events and generated schemas | Names and decodings match the TypeScript client |
| TC-6 | API client unit tests in `crates/api/src` cover errors, memory transport and request construction | Scripted responses and transport errors | Declared errors, unknown fields and request builders behave as specified |
| TC-7 | Local file unit tests in `crates/local/src` cover JSONC, locks, paths, channels, JSONL and service files | JSONC and client-local file contents | Comments and formatting survive, locks interoperate and strict decoding yields `{}` on a type error |
| TC-8 | Service unit tests in `crates/service/src` cover discovery, probing, startup and handoff behavior | Registration files and fake server processes | Compatible services are selected and incompatible or dead registrations are handled |
| TC-9 | Store unit tests in `crates/store/src` cover state folding, event application and change tracking | Event batches and store reads | One flush records changes, revision history is bounded and stale reads are refreshed |
| TC-10 | UI unit tests in `crates/ui/src` cover themes, keymap, content widgets and dialogs | Theme tokens, key events and content data | Semantic tokens, input modes and rendered content match expectations |
| TC-11 | Plugin and ABI unit tests in `crates/plugin/src`, `crates/plugin-abi/src`, `crates/latex/src` and `crates/mermaid/src` cover limits, messages and render trees | ABI messages, plugin calls and built-in plugin inputs | Limits hold, trees decode and built-in output matches committed cases |
| TC-12 | TUI unit tests in `crates/tui/src` cover route views, widgets, prompts, tabs and plugin mounts | Mounted test apps, keys and store changes | Views sync only named changes and rendered cells match committed expectations |
| TC-13 | Mini and drive unit tests in `crates/mini/src` and `crates/drive/src` cover scrollback rendering and headless control | Mini keys and drive messages | The transcript stays in scrollback and headless steps address the TUI |

## Integration Tests

| ID | Test File | Coverage |
|---|---|---|
| TC-14 | `crates/acp/tests/acp/additional_directories.rs` | ACP behavior with additional working directories |
| TC-15 | `crates/acp/tests/acp/catalog.rs` | Catalog and command updates that arrive after a session opens |
| TC-16 | `crates/acp/tests/acp/compaction.rs` | ACP compaction flow |
| TC-17 | `crates/acp/tests/acp/config_option.rs` | ACP config option reads |
| TC-18 | `crates/acp/tests/acp/elicitation.rs` | ACP elicitation requests |
| TC-19 | `crates/acp/tests/acp/error.rs` | ACP error mapping |
| TC-20 | `crates/acp/tests/acp/main.rs` | Linked ACP integration test binary |
| TC-21 | `crates/acp/tests/acp/permission.rs` | ACP permission decisions |
| TC-22 | `crates/acp/tests/acp/prompt.rs` | A held prompt, stream failure, retry wait and interruption |
| TC-23 | `crates/acp/tests/acp/replay.rs` | ACP replay behavior |
| TC-24 | `crates/acp/tests/acp/session.rs` | Wire order from a request through follow-up commands |
| TC-25 | `crates/acp/tests/acp/translate.rs` | Translation between ACP content and server messages |
| TC-26 | `crates/acp/tests/acp/turn.rs` | A background shell notice that wakes a session after a prompt response |
| TC-27 | `crates/acp/tests/acp/wire.rs` | In-process ACP client and server over in-memory pipes |
| TC-28 | `crates/api-types/tests/event_names.rs` | Raw string event names used outside the typed event union |
| TC-29 | `crates/api/tests/all/api.rs` | Generated type decoding and request core over a scripted transport |
| TC-30 | `crates/api/tests/all/live.rs` | Optional live GET endpoint decoding with `OPENCODE_LIVE=1` |
| TC-31 | `crates/api/tests/all/main.rs` | Linked API integration test binary |
| TC-32 | `crates/api/tests/all/oracle.rs` | Generated requests compared with the TypeScript Promise client |
| TC-33 | `crates/api/tests/all/review.rs` | API review regressions |
| TC-34 | `crates/api/tests/all/sse.rs` | Event stream reading and batching |
| TC-35 | `crates/cli/src/tests/mod.rs` | CLI inline unit tests and shared assertion helpers |
| TC-36 | `crates/cli/src/tests/output.rs` | Help and usage-error goldens |
| TC-37 | `crates/cli/src/tests/parse.rs` | Parser flags and usage errors |
| TC-38 | `crates/cli/src/tests/tree.rs` | Command tree parity |
| TC-39 | `crates/cli/tests/askpass.rs` | OpenSSH askpass helper mode |
| TC-40 | `crates/cli/tests/delegate.rs` | Delegated `serve`, `uninstall` and `plugin` arguments, streams and exit codes |
| TC-41 | `crates/cli/tests/deps.rs` | Target-specific dependency allowlist and crate layers |
| TC-42 | `crates/cli/tests/scratch.rs` | Non-UTF-8 arguments, stale `PWD` and log file channel in a scratch home |
| TC-43 | `crates/cli/tests/service.rs` | Service and pairing commands with an isolated home, channel and fake server |
| TC-44 | `crates/cli/tests/windows_smoke.rs` | Windows pseudoconsole start and Ctrl+C behavior |
| TC-45 | `crates/local/tests/all/config_interop.rs` | Config edits and shared file contents compared with the TypeScript client |
| TC-46 | `crates/local/tests/all/interop.rs` | Locks, registrations and service configs across both clients |
| TC-47 | `crates/local/tests/all/main.rs` | Linked client-local integration test binary |
| TC-48 | `crates/local/tests/all/shared_files.rs` | Concurrent writers and valid intermediate file contents |
| TC-49 | `crates/local/tests/all/support/mod.rs` | Shared TypeScript oracle helper |
| TC-50 | `crates/mermaid/tests/all/limits.rs` | Mermaid diagram limits |
| TC-51 | `crates/mermaid/tests/all/main.rs` | Linked Mermaid integration test binary |
| TC-52 | `crates/mermaid/tests/all/markdown.rs` | Mermaid fences inside Markdown |
| TC-53 | `crates/mermaid/tests/all/oracle.rs` | Mermaid output compared with committed cases |
| TC-54 | `crates/parity/tests/component.rs` | Cell fixture parsing, reformatting and injected differences |
| TC-55 | `crates/plugin-abi/tests/sdk.rs` | ABI SDK examples in the guide |
| TC-56 | `crates/service/tests/discover.rs` | Service discovery across two installations and registrations |
| TC-57 | `crates/service/tests/interop.rs` | Rust starts an isolated service and the TypeScript CLI discovers it |
| TC-58 | `crates/service/tests/lifecycle.rs` | Service lifecycle with the TypeScript fake service and accelerated clock |
| TC-59 | `crates/store/tests/all/common/mod.rs` | Scripted HTTP transport for store tests |
| TC-60 | `crates/store/tests/all/compaction.rs` | Store compaction |
| TC-61 | `crates/store/tests/all/data.rs` | Store read API behavior and regressions |
| TC-62 | `crates/store/tests/all/eviction.rs` | Cached read eviction |
| TC-63 | `crates/store/tests/all/fold_oracle.rs` | Event folds compared with recorded results |
| TC-64 | `crates/store/tests/all/inbox_race.rs` | Inbox admission and delivery races |
| TC-65 | `crates/store/tests/all/jobs.rs` | Running-job store behavior |
| TC-66 | `crates/store/tests/all/live.rs` | Optional live event stream test with `OPENCODE_LIVE=1` |
| TC-67 | `crates/store/tests/all/live_rest.rs` | Optional live read-only service test with `OPENCODE_LIVE=1` |
| TC-68 | `crates/store/tests/all/location.rs` | Location-scoped state |
| TC-69 | `crates/store/tests/all/main.rs` | Linked store integration test binary |
| TC-70 | `crates/store/tests/all/model.rs` | Delayed model reads and events across reconnects and deletions |
| TC-71 | `crates/store/tests/all/pending_status.rs` | Pending status behavior |
| TC-72 | `crates/store/tests/all/reconnect.rs` | Rediscovery of a stale registration during reconnect |
| TC-73 | `crates/store/tests/all/refresh.rs` | Stale read refresh |
| TC-74 | `crates/store/tests/all/review_fixes.rs` | Store review regressions |
| TC-75 | `crates/store/tests/all/target_oracle.rs` | Session target resolution compared with recorded results |
| TC-76 | `crates/tui/tests/all/actions.rs` | Session commands through a request-recording server |
| TC-77 | `crates/tui/tests/all/animations.rs` | Animation and idle-frame behavior on the app clock |
| TC-78 | `crates/tui/tests/all/app.rs` | Replayed P-APP scenarios, screen checkpoints and requests |
| TC-79 | `crates/tui/tests/all/attach.rs` | Clipboard reads, attachments and stash requests |
| TC-80 | `crates/tui/tests/all/attention.rs` | Notification sounds through the test audio engine |
| TC-81 | `crates/tui/tests/all/click_focus.rs` | Focus follows handled clicks |
| TC-82 | `crates/tui/tests/all/cold_catalogs.rs` | Catalog reads before plugins load |
| TC-83 | `crates/tui/tests/all/complete.rs` | Completion keys, submitted parts and persisted recents |
| TC-84 | `crates/tui/tests/all/composer.rs` | Composer tabs, shell output and client MCP tools |
| TC-85 | `crates/tui/tests/all/config_live.rs` | Settings writes and external config file replacements |
| TC-86 | `crates/tui/tests/all/diffs.rs` | Diff viewer lifecycle and controls |
| TC-87 | `crates/tui/tests/all/drive.rs` | Headless TUI control over the simulation endpoint |
| TC-88 | `crates/tui/tests/all/editor.rs` | External editor flow |
| TC-89 | `crates/tui/tests/all/form.rs` | Session and global forms with visible fields and submitted answers |
| TC-90 | `crates/tui/tests/all/home_footer.rs` | Home footer claims across carriers and sizes |
| TC-91 | `crates/tui/tests/all/hover_pointer.rs` | Pointer cursor over clickable and other cells |
| TC-92 | `crates/tui/tests/all/integrations.rs` | Integration dialogs and credential requests |
| TC-93 | `crates/tui/tests/all/main.rs` | Linked TUI integration test binary |
| TC-94 | `crates/tui/tests/all/mcp.rs` | MCP and skill dialogs |
| TC-95 | `crates/tui/tests/all/messages.rs` | Transcript messages, notices, errors and retries |
| TC-96 | `crates/tui/tests/all/models.rs` | Model and usage dialogs against cells and server responses |
| TC-97 | `crates/tui/tests/all/navigate.rs` | Window and route navigation |
| TC-98 | `crates/tui/tests/all/perf.rs` | Fixed TUI workloads that print performance markers |
| TC-99 | `crates/tui/tests/all/permission.rs` | Permission decisions and server requests |
| TC-100 | `crates/tui/tests/all/plugin_behave.rs` | Plugin scroll commands, sticky headers and windowed lists |
| TC-101 | `crates/tui/tests/all/plugin_builtins.rs` | Built-in plugin surfaces across mounts, revisions, themes and sizes |
| TC-102 | `crates/tui/tests/all/plugin_canvas.rs` | Replayed canvas lists and live draw tracking |
| TC-103 | `crates/tui/tests/all/plugin_claim.rs` | Renderer claims on a streaming transcript |
| TC-104 | `crates/tui/tests/all/plugin_compat.rs` | V2 JSX plugins on the JS host with input and callbacks |
| TC-105 | `crates/tui/tests/all/plugin_fences.rs` | JavaScript Markdown renderers, adoption, fallback, quotas and teardown |
| TC-106 | `crates/tui/tests/all/plugin_fetch.rs` | Built-in plugin fetches, results, errors and mount cancellation |
| TC-107 | `crates/tui/tests/all/plugin_field_echo.rs` | A delayed field echo that does not overwrite a newer edit |
| TC-108 | `crates/tui/tests/all/plugin_flood.rs` | Mailbox fairness and per-frame work under repeated wakes |
| TC-109 | `crates/tui/tests/all/plugin_input.rs` | Input ownership across panels, fields, modes, holds and overlays |
| TC-110 | `crates/tui/tests/all/plugin_limits.rs` | Plugin resource admission and release at limits |
| TC-111 | `crates/tui/tests/all/plugin_luau.rs` | Luau plugins in the TUI compared with a Rust twin |
| TC-112 | `crates/tui/tests/all/plugin_machines.rs` | Plugin lifecycle, manager and viewer against the shared state machine |
| TC-113 | `crates/tui/tests/all/plugin_mail.rs` | Plugin worker threads and mailbox delivery |
| TC-114 | `crates/tui/tests/all/plugin_manager.rs` | Plugin manager actions, subscriptions and resources held while disabled |
| TC-115 | `crates/tui/tests/all/plugin_npm.rs` | npm plugin loading through the JS host |
| TC-116 | `crates/tui/tests/all/plugin_ownership.rs` | Request and effect ownership across carriers |
| TC-117 | `crates/tui/tests/all/plugin_p0a.rs` | Composer edits, dialogs and styled nodes of a linked plugin |
| TC-118 | `crates/tui/tests/all/plugin_p0a/probe.rs` | Linked plugin fixture for dialogs, composer edits and a styled footer |
| TC-119 | `crates/tui/tests/all/plugin_pending_focus.rs` | Focus requested before a plugin field's first view |
| TC-120 | `crates/tui/tests/all/plugin_pipe.rs` | Plugin requests, frames, reloads, faults and backpressure against the JS host |
| TC-121 | `crates/tui/tests/all/plugin_reads.rs` | Host reads and actions of a linked plugin |
| TC-122 | `crates/tui/tests/all/plugin_reconcile.rs` | Reconciled trees compared with fresh mounts, cells and hit regions |
| TC-123 | `crates/tui/tests/all/plugin_routing.rs` | Key and pointer delivery to plugin owners |
| TC-124 | `crates/tui/tests/all/plugin_surface.rs` | Plugin surface lifecycle, visible frames, callback logs and resources |
| TC-125 | `crates/tui/tests/all/plugin_timers.rs` | Host-clock timers, cancellation and idle frame close |
| TC-126 | `crates/tui/tests/all/plugins.rs` | Linked plugins in the TUI across rendering, effects, faults and storage |
| TC-127 | `crates/tui/tests/all/prompt.rs` | Prompt editing and submission over a request-recording transport |
| TC-128 | `crates/tui/tests/all/prompt_footer.rs` | Goal footer updates across reads and mounts |
| TC-129 | `crates/tui/tests/all/pump.rs` | Store-to-UI delivery while the UI queue is full |
| TC-130 | `crates/tui/tests/all/queue.rs` | Queued prompts through the dock and message dialogs |
| TC-131 | `crates/tui/tests/all/reconnect.rs` | Reconnect refresh when the disconnected status is never observed |
| TC-132 | `crates/tui/tests/all/resize.rs` | TUI layout across terminal sizes |
| TC-133 | `crates/tui/tests/all/review_ms1.rs` | Session key ownership and permission refresh across route changes |
| TC-134 | `crates/tui/tests/all/review_ms34.rs` | Saved model and fallback selection |
| TC-135 | `crates/tui/tests/all/root.rs` | Terminal-environment uploads through root command arguments |
| TC-136 | `crates/tui/tests/all/session_links.rs` | Session links in Markdown and mouse input |
| TC-137 | `crates/tui/tests/all/session_view.rs` | Session viewport behavior and store subscriptions |
| TC-138 | `crates/tui/tests/all/sessions.rs` | Session list and open-dialog navigation |
| TC-139 | `crates/tui/tests/all/settings.rs` | Settings, experiments, debug and developer tools |
| TC-140 | `crates/tui/tests/all/shared_state.rs` | Session-scoped selection and shared-file merges across writers |
| TC-141 | `crates/tui/tests/all/shell.rs` | Shell pane behavior |
| TC-142 | `crates/tui/tests/all/sidebar.rs` | MCP sidebar actions and persisted section state |
| TC-143 | `crates/tui/tests/all/support/heap.rs` | Counting allocator used by the TUI test binary |
| TC-144 | `crates/tui/tests/all/support/ide.rs` | Fake IDE MCP server shared by editor tests and app replay |
| TC-145 | `crates/tui/tests/all/support/mod.rs` | Shared TUI mount, fake server and default route helpers |
| TC-146 | `crates/tui/tests/all/support/model.rs` | Deterministic command traces, ABI checks and failure shrinking |
| TC-147 | `crates/tui/tests/all/support/probe.rs` | Shared performance probe for TUI and mini |
| TC-148 | `crates/tui/tests/all/system.rs` | System dialogs, plugin management and update notices |
| TC-149 | `crates/tui/tests/all/system_commands.rs` | System commands, clipboard actions and working-directory changes |
| TC-150 | `crates/tui/tests/all/tabs.rs` | Session tabs and panes over temporary shared storage |
| TC-151 | `crates/tui/tests/all/terminal.rs` | Terminal panes against a fake socket and recorded requests |
| TC-152 | `crates/tui/tests/all/tools.rs` | Tool transcript rows, states and click actions |
| TC-153 | `crates/tui/tests/all/transcript.rs` | Transcript view behavior |
| TC-154 | `crates/tui/tests/all/tui_drop.rs` | TUI teardown behavior |
| TC-155 | `crates/tui/tests/all/user_keys.rs` | User keybinds and tabs from `cli.json` fed as terminal bytes |
| TC-156 | `crates/tui/tests/all/worktrees.rs` | Worktree selection, creation and session moves |
| TC-157 | `crates/ui/tests/all/content.rs` | Content widget behavior |
| TC-158 | `crates/ui/tests/all/dialogs.rs` | Dialog backdrops and dialog behavior |
| TC-159 | `crates/ui/tests/all/grammars.rs` | Static tree-sitter grammars and highlight queries |
| TC-160 | `crates/ui/tests/all/main.rs` | Linked UI kit integration test binary |
| TC-161 | `crates/ui/tests/all/motion_frames.rs` | Motion frames against transparent and themed backgrounds |
| TC-162 | `crates/ui/tests/all/motion_oracle.rs` | Motion behavior compared with committed cases |
| TC-163 | `crates/ui/tests/all/theme_oracle.rs` | Theme token behavior compared with committed cases |
| TC-164 | `crates/ui/tests/all/tool_info_oracle.rs` | Tool info rendering compared with committed cases |

## End-to-End Tests

| ID | Test File | Steps | Expected Outcome |
|---|---|---|---|
| TC-165 | `parity/app/scenarios.test.tsx` | Record P-APP scenarios under `TZ=UTC`, serving scenario routes and TypeScript TUI defaults | Committed cells, requests and responses are stable across two recordings |
| TC-166 | `parity/machines/plugins.test.tsx` | Drive the TypeScript TUI through the shared plugin state machine | Each edge and seeded walk matches the state machine fixture |
| TC-167 | `parity/acp/run.ts` | Run each ACP subprocess suite once against the TypeScript agent and once against `opencode-native acp` | Tests pass on both sides and normalized JSON-RPC transcripts match |
| TC-168 | `parity/cli/run.ts` | Run each CLI scenario in fresh homes with fake servers on both clients | Exit code, stdout, stderr and requests match after normalization |
| TC-169 | `parity/pty/run.ts` | Run each PTY scenario in a pseudo-terminal on both clients | Screen checkpoints, OSC output, exit code and requests match after masking |
| TC-170 | `parity/sim/run.ts` | Run each simulation scenario through the TypeScript server and both clients with headless rendering | Screen checkpoints and writes match after masks and deviations |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-171 | A parity difference has no file under `parity/deviations/` | The run fails and reports the differing cell or request |
| TC-172 | A recorded deviation now matches on both sides | The runner prints a note to remove the deviation |
| TC-173 | A service registration points to a dead process or an incompatible version | The registration is evicted or skipped and another compatible service is chosen |
| TC-174 | A restarted service changes its port or password | A connect failure or 401 triggers rediscovery and the request is sent once to the new service |
| TC-175 | An event batch queue fills | The event loop reconnects and the consumer resynchronizes on `server.connected` |
| TC-176 | Store flushes arrive faster than frames | The pump queues at most one `DataChanged` and every task-to-UI queue stays bounded |
| TC-177 | `cli.json` contains comments or an unknown key | Comments survive an edit and strict decoding treats a wrong type as `{}` |
| TC-178 | Both clients write the same state files | Locks and atomic writes keep intermediate contents valid and shared fields survive writes |
| TC-179 | An argument is not UTF-8 or `PWD` is stale | The scratch-home CLI run still behaves as the TypeScript client does |
| TC-180 | A plugin exceeds frame, call, memory or message limits | The plugin fails alone, its effects do not apply and its registrations are removed |
| TC-181 | A project plugin has not been approved | It claims nothing and the approval dialog shows the directory and the start of its SHA-256 |
| TC-182 | A JS host owes an answer and stays silent | The host is restarted and the plugin call fails without stopping the client |
| TC-183 | A scenario uses nondeterministic text, durations or relative times | Masks blank the cells on both sides and record a reason |
| TC-184 | A Windows pseudoconsole run reaches home and receives Ctrl+C | The TUI leaves the alternate screen and the process exits |
| TC-185 | `OPENCODE_LIVE=1` is not set | Optional live API and store tests stay disabled |

## Test Infrastructure

- Run cargo through `bun run cargo` from `packages/cli-rs` so the pinned OpenTUI native library is installed and `.cargo/config.toml` is read.
- Run the workspace suite with `bun run cargo test --locked --workspace --no-fail-fast`.
- Select an area with `cargo test -p opencode-tui --test all <module>::` or the matching command for another crate.
- `opencode-tui` and `opencode-ui` each use one integration binary at `tests/all/main.rs`, with shared helpers under `tests/all/support/`.
- The parity runners require `bun install` at the repository root and build the debug binary unless `OPENCODE_RS_BIN` names one.
- Rust tests that call TypeScript helpers skip without Bun or `node_modules`; `OPENCODE_RS_REQUIRE_TS=1` makes them fail.
- Committed fixtures live under `parity/fixtures/`, scenario files under `parity/scenarios/`, and intended differences under `parity/deviations/`.
- `bun run fixtures` rewrites oracle, component and app fixtures. Fixtures are never edited by hand.
- `bun run check:drift` runs generators and fixture writers, then lists files that changed.
- `bun run parity:machines` runs the plugin state machine suite. The package has no `test` script by design.
- `bun run check:deny`, `bun run check:advisories` and `bun run check:luau-types` cover dependency policy, advisories and Luau plugin typing.
- `sh script/check-windows.sh` and `sh script/check-target.sh` compile the workspace for other targets without linking or running it.
- Manual Windows terminal checks in `docs/testing.md` cover keys, mouse, paste, resize, themes, links, sounds and editor integration.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-35, TC-36, TC-37, TC-38, TC-40, TC-168 |
| FR-2 | TC-76 through TC-156, TC-165, TC-169, TC-170 |
| FR-3 | TC-43, TC-56, TC-57, TC-58, TC-72, TC-174 |
| FR-4 | TC-45, TC-46, TC-48, TC-85, TC-140, TC-177, TC-178 |
| FR-5 | TC-28 through TC-34, TC-59 through TC-75, TC-131, TC-175, TC-176 |
| FR-6 | TC-54, TC-55, TC-100 through TC-126, TC-166, TC-180, TC-181, TC-182 |
| FR-7 | TC-14 through TC-27, TC-167 |
| FR-8 | TC-28, TC-32, TC-38, TC-54, TC-55, TC-63, TC-75, TC-157 through TC-164 |
| FR-9 | TC-40, TC-43, TC-87, TC-169 |
| FR-10 | TC-41 covers the dependency allowlist, the installer itself has no dedicated test and needs manual build review |
| FR-11 | TC-108, TC-110, TC-113, TC-114, TC-120, TC-121, TC-124, TC-125, TC-180, TC-182 |
| FR-12 | TC-78, TC-165 through TC-170 |
| FR-13 | TC-54, TC-78, TC-171, TC-172, TC-165, TC-169, TC-170 |
| FR-14 | Format, clippy, test, drift and machine checks are package commands, not a single automated test |
| FR-15 | TC-44, TC-98, TC-184, and the live script needs manual review |
| NFR-1 | TC-29, TC-30, TC-32, TC-33 |
| NFR-2 | TC-106, TC-111, TC-114, TC-116, TC-121, TC-181 |
| NFR-3 | TC-98, TC-108, TC-120, TC-125, TC-129, TC-176 |
| NFR-4 | TC-41, TC-44, and the target and Windows scripts need manual review |
