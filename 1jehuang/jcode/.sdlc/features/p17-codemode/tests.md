---
title: "Codemode"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Codemode

## Scope

Two test files cover this feature.
`crates/jcode-codemode/src/tests.rs` drives the sandbox crate through its public `run` API with a mock `Host`, and the file is compiled only on non-FreeBSD targets through `#[cfg(all(test, not(target_os = "freebsd")))]`.
`crates/jcode-app-core/src/tool/codemode_tests.rs` drives the `codemode` tool through `Registry::execute` with a registry that holds two stub tools.
Out of scope: the internals of the QuickJS engine, the harness tools that a script calls, the persistence of the store file on disk, and provider behavior.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tool output decoding, `decode_tool_output_parses_json_only_when_structured` in `crates/jcode-codemode/src/tests.rs` | `decode_tool_output` called with `{"a":1}`, ` [1,2] `, `plain`, and `{not json}` | A parsed object, a parsed array, the string `plain`, and the raw string `{not json}` |
| TC-2 | Report rendering, `report_renders_strings_raw_and_lists_store_keys` in `crates/jcode-app-core/src/tool/codemode_tests.rs` | `render_report` called with a string result, one tool call, and one stored key | The report starts with `result:\nplain text`, contains `[1 tool call, `, and contains `stored: k]` |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-3 | Return value is captured, `returns_json_value` in `crates/jcode-codemode/src/tests.rs` | A script that returns an object and a mapped array | The result is `{"a":1,"b":[2,4,6]}` and no error is reported |
| TC-4 | An undefined return is reported, `undefined_return_is_none` in `crates/jcode-codemode/src/tests.rs` | A script that only assigns a variable | The result is `None` and no error is reported |
| TC-5 | Tool calls through the proxy and through `callTool`, `calls_tools_via_proxy_and_call_tool` in `crates/jcode-codemode/src/tests.rs` | A script that awaits `tools.echo({x:1})` and `callTool("echo",{y:2})` | Both results reach the script and the tool call count is 2 |
| TC-6 | Independent tool calls run concurrently, `parallel_tool_calls_run_concurrently` in `crates/jcode-codemode/src/tests.rs` | A script that starts 20 slow calls with `Promise.all` | 20 results are returned and the run finishes in under 800 ms |
| TC-7 | A tool failure is catchable inside the script, `tool_errors_throw_and_can_be_caught` in `crates/jcode-codemode/src/tests.rs` | A script that catches the failing tool and returns the error message | The result is `fail: boom` and no run error is reported |
| TC-8 | An uncaught error is reported, `uncaught_errors_are_reported` in `crates/jcode-codemode/src/tests.rs` | A script that throws `new Error('nope')` | The run error contains `nope` |
| TC-9 | A syntax error is reported, `syntax_errors_are_reported` in `crates/jcode-codemode/src/tests.rs` | A script with invalid syntax | The run reports an error |
| TC-10 | An unknown tool name suggests alternatives, `unknown_tools_suggest_alternatives` in `crates/jcode-codemode/src/tests.rs` | A script that calls `tools.ech({})` | The error names `ech`, suggests `echo`, and the tool call count is 0 |
| TC-11 | Console output is captured with level prefixes, `console_output_is_captured` in `crates/jcode-codemode/src/tests.rs` | A script that logs one line at level `log` and one at level `warn` | The captured lines are `hi {"a":1}` and `[warn] careful` |
| TC-12 | Console capture is bounded, `log_capture_is_bounded` in `crates/jcode-codemode/src/tests.rs` | 100 console lines and a 100 byte log limit | The output is marked as truncated and fewer than 100 lines are kept |
| TC-13 | The store persists across runs, `store_persists_across_runs` in `crates/jcode-codemode/src/tests.rs` | A first script that stores a value, and a second script that loads it | The first run lists the key, the second run returns the incremented value, and a missing key loads as `undefined` |
| TC-14 | The discovery helpers work, `discovery_helpers_work` in `crates/jcode-codemode/src/tests.rs` | A script that calls `listTools()`, `listTools("slo")`, `describeTool("echo")`, and checks `'echo' in tools` | The script receives the tool names, the filtered names, the first description line, the input schema, and `true` |
| TC-15 | A busy loop hits the wall-clock limit, `busy_loops_time_out` in `crates/jcode-codemode/src/tests.rs` | An infinite loop and a 300 ms timeout | The run error contains `timed out` |
| TC-16 | A hung tool call hits the wall-clock limit, `hung_tool_calls_time_out` in `crates/jcode-codemode/src/tests.rs` | A tool that never returns and a 300 ms timeout | The run error contains `timed out` and the test finishes in under 5 s |
| TC-17 | The heap limit is enforced, `memory_limit_is_enforced` in `crates/jcode-codemode/src/tests.rs` | An unbounded allocation loop and an 8 MB limit | The run reports an error |
| TC-18 | The tool call limit is enforced, `tool_call_limit_is_enforced` in `crates/jcode-codemode/src/tests.rs` | 5 tool calls and a limit of 3 | The run error contains `limit` |
| TC-19 | No host API is exposed, `no_host_apis_are_exposed` in `crates/jcode-codemode/src/tests.rs` | A script that checks `require`, `process`, `fetch`, `setTimeout`, `std`, and `os` | Every one of them is `undefined` |
| TC-20 | Dropping the run future cancels the script, `dropping_the_future_cancels` in `crates/jcode-codemode/src/tests.rs` | A run future waiting on a tool that never returns | The surrounding timeout fires, and the test runtime is not blocked |
| TC-21 | A script composes registry tools, `script_composes_registry_tools` in `crates/jcode-app-core/src/tool/codemode_tests.rs` | A registry holding a `lookup` tool and a `shout` tool, and a script that calls both in parallel | The report contains the computed total, the uppercased text, the console line, and a 4 tool call count |
| TC-22 | A script cannot call `codemode` or `batch`, `script_cannot_call_itself_or_batch` in `crates/jcode-app-core/src/tool/codemode_tests.rs` | A script that lists the tools and a script that calls `tools.codemode` | `codemode` is absent from the listed tools, and the recursive call fails with `unknown tool 'codemode'` |
| TC-23 | Session policy applies inside scripts, `session_policy_applies_inside_scripts` in `crates/jcode-app-core/src/tool/codemode_tests.rs` | A session policy that denies `shout` | `shout` is absent from the listed tools, and `'shout' in tools` is `false` |
| TC-24 | A pure failure is surfaced as a tool error, `uncaught_errors_without_side_effects_are_tool_errors` in `crates/jcode-app-core/src/tool/codemode_tests.rs` | A script that throws before calling any tool | The tool call fails and the error contains `broken script` |

## End-to-End Tests

None exist today.
- The sandbox tests call `jcode_codemode::run` directly with a mock host, so they never touch the harness registry.
- The harness tests call `Registry::execute("codemode", ...)` with stub tools, so they never reach a real provider or a real model turn.
- The gap is the join between the two, which is a model turn that emits a `codemode` tool call and receives the rendered report.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-4 | The script returns `undefined` | The result is `None` and the run reports no error |
| TC-7 | The script calls a tool that fails | The failure becomes a thrown `Error` that the script can catch |
| TC-9 | The script has a syntax error | The run reports an error and the script never starts |
| TC-10 | The script calls a tool that does not exist | The error names the tool, suggests similar names, and counts no tool call |
| TC-12 | The script logs more than the log budget allows | The console output is truncated and the truncation is reported |
| TC-13 | The script loads a key that was never stored | `load` returns `undefined` |
| TC-15 | The script loops forever | The wall-clock limit stops the run and the error names the timeout |
| TC-16 | A tool call never returns | The wall-clock limit stops the run while the tool call is still in flight |
| TC-17 | The script allocates without bound | The heap limit stops the run and the run reports an error |
| TC-18 | The script calls tools past the call limit | The call is refused with a limit error |
| TC-19 | The script reaches for a host API | Every host API is `undefined`, so the script can only act through a tool |
| TC-20 | The caller drops the run future | The script is cancelled and the test runtime is not blocked |
| TC-22 | The script tries to call `codemode` | The recursive call is refused as an unknown tool |
| TC-23 | The session policy denies a tool | The denied tool is absent from the tools a script can reach |
| TC-24 | The script fails before any side effect | The tool call fails, so the model can retry |

## Test Infrastructure

- The mock host in `crates/jcode-codemode/src/tests.rs` implements the `Host` trait with the tools `echo`, `fail`, `slow` (50 ms), and `hang` (1 hour), and it counts the calls it receives.
- The stub registry in `crates/jcode-app-core/src/tool/codemode_tests.rs` builds a `Registry::empty()` that holds a JSON tool named `lookup` and a text tool named `shout`, plus the `codemode` tool itself.
- The sandbox test module only builds on non-FreeBSD targets, so the FreeBSD availability path is asserted by reading the `AVAILABLE` constant rather than by running a script.
- `crates/jcode-app-core/src/tool/tests.rs` exempts `codemode` from the shared 20 token tool-description cap, because the description documents the sandbox API.
- Run the suites with `cargo test -p jcode-codemode` and `cargo test -p jcode-app-core codemode`.

## Coverage Matrix

Requirements with no automated test are listed with the reason, so the gaps stay visible.

| Requirement | Test Cases |
|---|---|
| FR-1 | Not covered, because no test asserts the config or environment enablement gate |
| FR-2 | TC-3, TC-4, TC-5 |
| FR-3 | TC-5, TC-7, TC-21 |
| FR-4 | TC-21, TC-23 |
| FR-5 | TC-21 |
| FR-6 | TC-8, TC-9, TC-24 |
| FR-7 | TC-13, TC-2 |
| FR-8 | TC-14, TC-22 |
| FR-9 | TC-1, TC-21 |
| FR-10 | TC-22 |
| FR-11 | TC-2, TC-21 |
| FR-12 | Not covered, because the report truncation helper has no test |
| FR-13 | TC-10 |
| FR-14 | TC-11, TC-12 |
| NFR-1 | TC-19 |
| NFR-2 | TC-15, TC-16, TC-17, TC-18 |
| NFR-3 | Not covered, because the sandbox test module is compiled out on FreeBSD |
| NFR-4 | Not asserted directly, because TC-5 and TC-20 exercise the bridge between the script thread and the caller's runtime without checking the thread itself |
| NFR-5 | TC-16, TC-20 |
| NFR-6 | TC-6 |
| NFR-7 | Not covered, because the run is logged to the log file rather than to the test output |
| NFR-8 | Not covered, because the optional dependency is a build configuration property |
