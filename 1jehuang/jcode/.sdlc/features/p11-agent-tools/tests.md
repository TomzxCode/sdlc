---
title: "Agent Tool Suite"
status: done
session_link: "http://localhost:10000/?session=ses_sync_sdlc_20261019"
---

# Test Plan: Agent Tool Suite

## Scope

This plan covers the tool runtime: the `Tool` trait and `ToolContext` in `jcode-tool-core`, the shared output model and alias table in `jcode-tool-types`, the `Registry` in `crates/jcode-app-core/src/tool/mod.rs`, and the tool implementations in `crates/jcode-app-core/src/tool/`.
The command-safety gate, the Codemode sandbox runtime, and the agent applet runtime are separate features and are not covered here, except where a tool test exercises the boundary.
The provider runtimes, the turn loop, the compaction engine, and the session store are covered by their own plans.
This plan was reverse-engineered from the existing test suite during an SDLC sync, so every file listed below already exists.

Known gaps in the current suite:

- The `ls` tool has no dedicated test file, and is only covered indirectly through registry-level tests.
- The `write` tool has no test that exercises the per-path file lock, so concurrent-write serialization is not proven.
- The `webfetch` tool has no test that exercises a response larger than the 5 MB cap.
- The `patch` tool is retained without being registered, but no test asserts its absence.
- The `codemode` tool is registered only when it is enabled in the configuration, but no test asserts that the disabled state leaves it unregistered.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | The registry publishes sorted definitions and injects the required `intent` property | `crates/jcode-app-core/src/tool/tests.rs` | Definitions are sorted by name and every object schema lists `intent` as required |
| TC-2 | Tool descriptions and parameter descriptions stay under the token cap | `crates/jcode-app-core/src/tool/tests.rs` | No tool description and no parameter description exceeds the cap |
| TC-3 | Provider-facing schemas avoid constructs that strict-mode providers reject | `crates/jcode-app-core/src/tool/tests.rs` | No array is typed as a union, no required entry lacks a matching property, and every built-in schema is sendable to every registered provider dialect |
| TC-4 | Alias resolution maps provider names, `functions.` prefixes, and PascalCase OAuth names | `crates/jcode-app-core/src/tool/tests.rs`, `crates/jcode-tool-types/src/lib.rs` | Each alias resolves to its canonical registry name |
| TC-5 | Registry execution enforces the session allow and deny policy after alias resolution | `crates/jcode-app-core/src/tool/tests.rs` | A denied or non-allowed tool fails with a policy error |
| TC-6 | The pre-tool hook can block a call and can allow a call | `crates/jcode-app-core/src/tool/tests.rs` | A blocked call never reaches the tool and the reason is reported |
| TC-7 | The context guard withholds a huge result by default and truncates it on opt-in | `crates/jcode-app-core/src/tool/tests.rs` | The default result is a refusal, the opted-in result is truncated with a notice |
| TC-8 | The context guard refuses when the context is exhausted and reports the real cost | `crates/jcode-app-core/src/tool/tests.rs` | The refusal states the cost and the context level, and spends no more than it reports |
| TC-9 | An unknown tool name produces an error with the available tools and near-miss suggestions | `crates/jcode-app-core/src/tool/tests.rs` | The error names the unknown tool, lists the available tools, and suggests the near match |
| TC-10 | MCP allow and deny lists cover dynamic server tools and the fixed surfaces | `crates/jcode-app-core/src/tool/mod.rs` (inline `mcp_allow_list_tests`) | `mcp` in a list covers `mcp__server__tool` names, and a lookalike prefix does not match |
| TC-11 | MCP alias collisions, catalog refresh, and legacy deny precedence | `crates/jcode-app-core/src/tool/tests/mcp_collision.rs` | A colliding name gets a distinct alias, a refresh drops the stale alias, and a legacy deny still blocks |
| TC-12 | Session SDK tool selection, replacement, validation, and isolation | `crates/jcode-app-core/src/tool/tests/sdk.rs` | A client-defined tool is selected, validated, and scoped to its own session |
| TC-13 | The read tool normalizes line ranges and advertises a provider-safe schema | `crates/jcode-app-core/src/tool/read/tests.rs` | `start_line`/`end_line` and `offset`/`limit` are both supported, mixing them is rejected, and the schema has no union-typed array |
| TC-14 | The read tool converts images and refuses undecodable ones | `crates/jcode-app-core/src/tool/read/tests.rs` | A BMP becomes a PNG image block, and an undecodable image is refused without an image block |
| TC-15 | The write tool summarizes diffs and previews file touches | `crates/jcode-app-core/src/tool/write.rs` (inline tests) | The diff uses the `42- old` / `42+ new` form, truncates after 20 lines, and is empty for identical content |
| TC-16 | The edit tool applies every edit or none | `crates/jcode-app-core/src/tool/edit.rs` (inline tests) | A partially matching edit set leaves the file unchanged |
| TC-17 | The replace tool applies every replacement or none | `crates/jcode-app-core/src/tool/replace.rs` (inline tests) | A replacement that cannot apply to one file leaves every file unchanged |
| TC-18 | The bash tool advertises search guidance and handles optional arguments | `crates/jcode-app-core/src/tool/bash_tests.rs` | The description points at `agentgrep`, omitted optionals take their defaults, and an invalid optional type is rejected |
| TC-19 | The bash tool forwards standard input and captures standard error | `crates/jcode-app-core/src/tool/bash_tests.rs` | A command that reads one line receives it, and standard error appears in the output |
| TC-20 | The bash tool promotes a timed-out or reload-persistable command to the background | `crates/jcode-app-core/src/tool/bash_tests.rs` | The call returns a background task identifier and the command keeps running |
| TC-21 | The bash tool terminates the whole process group on timeout | `crates/jcode-app-core/src/tool/bash_tests.rs` | A descendant process of a timed-out command does not survive |
| TC-22 | Progress markers and heuristics are parsed into task progress | `crates/jcode-app-core/src/tool/bash_tests/progress_parsing.rs` | Marker payloads, ratios, percentages, phases, and byte ratios are all classified correctly |
| TC-23 | The agentgrep builders scope searches to the requested paths | `crates/jcode-app-core/src/tool/agentgrep_tests.rs` | Scope flags are included, a match-all glob is dropped, and an unscoped empty query is rejected |
| TC-24 | The agentgrep executor runs each mode and compacts large output | `crates/jcode-app-core/src/tool/agentgrep_tests.rs` | Grep runs when the mode is omitted, a file field excludes sibling files, and long lines are compacted |
| TC-25 | The apply_patch tool parses and applies Codex and unified-diff patches | `crates/jcode-app-core/src/tool/apply_patch_tests.rs` | Add, update, delete, move, multiple-chunk, and end-of-file patches apply correctly |
| TC-26 | The apply_patch tool refuses to delete a protected path | `crates/jcode-app-core/src/tool/apply_patch_tests.rs` | The protected path survives while an ordinary file is still deleted |
| TC-27 | The batch tool normalizes malformed subcall shapes and keeps a generic schema | `crates/jcode-app-core/src/tool/batch_tests.rs` | `name`, `arguments`, and flat parameters are all normalized, and the schema stays generic |
| TC-28 | The batch tool dispatches through a surviving registry clone and fails cleanly when the registry is gone | `crates/jcode-app-core/src/tool/batch_tests.rs` | A surviving clone still executes, and a dropped registry produces a clean error |
| TC-29 | The custom web search builds requests and maps JSON pointers | `crates/jcode-app-core/src/tool/websearch_tests.rs` | GET encodes the query, POST merges the body and the count, and nested and escaped pointers resolve |
| TC-30 | The custom web search validates configuration without exposing credentials | `crates/jcode-app-core/src/tool/websearch_tests.rs` | A bad configuration fails with a message that contains no credential |
| TC-31 | The local search engines parse results and detect anti-bot pages | `crates/jcode-app-core/src/tool/websearch_tests.rs` | Bing HTML, Bing API, DuckDuckGo, and SearXNG results parse, and a captured anti-bot fixture is detected |
| TC-32 | The webfetch extraction satisfies the corpus invariants | `crates/jcode-app-core/src/tool/webfetch_corpus_tests.rs` | The extracted text drops tags, keeps code blocks intact, and matches the corpus expectations |
| TC-33 | The MCP management and deferred search tools behave as specified | `crates/jcode-app-core/src/tool/mcp_tests.rs` | Listing shows a disabled server, an unknown action fails, and the search results fit an adaptive budget |
| TC-34 | The session search ranks, filters, groups, and locates matches | `crates/jcode-app-core/src/tool/session_search_tests.rs` | Phrase and token matches are ranked, the current session is excluded by default, and locators are stable |
| TC-35 | The todo tool tracks structured items and goal assessments | `crates/jcode-app-core/src/tool/todo.rs` (inline tests) | Item status, grouping, confidence, and the goal assessment fields round-trip |
| TC-36 | The initiative tool round-trips and keeps its schema stable | `crates/jcode-app-core/src/tool/goal_tests.rs` | An initiative can be created and resumed, and the schema omits the public enums |
| TC-37 | The memory tool stores and queries long-lived memory | `crates/jcode-app-core/src/tool/memory.rs` (inline tests) | A remembered entry is recalled with its category and scope |
| TC-38 | The skill tool loads, lists, reads, and reloads skills | `crates/jcode-app-core/src/tool/skill.rs` (inline tests) | Each action returns the expected result and an unknown action is rejected |
| TC-39 | A write that lands on the active config reports what changed | `crates/jcode-app-core/src/tool/config_edit_notice_tests.rs` | The notice names the changed settings, says when a restart is required, and reports a broken config loudly |
| TC-40 | The open tool parses and resolves its target | `crates/jcode-app-core/src/tool/open_tests.rs` | A file URL becomes a local path, a missing path is rejected, and a removed parameter is rejected |
| TC-41 | The panel and side_panel tools manage their lifecycle | `crates/jcode-app-core/src/tool/panel_tests.rs`, `crates/jcode-app-core/src/tool/side_panel_tests.rs` | A panel registers, is listed, and validates its inputs |
| TC-42 | The applet tool requires the desktop capability and validates its shapes | `crates/jcode-app-core/src/tool/applet_tests.rs` | The call is refused without the capability, and the documented shapes validate |
| TC-43 | The codemode script composes registry tools and respects the session policy | `crates/jcode-app-core/src/tool/codemode_tests.rs` | A script calls registry tools, a policy inside the script is enforced, and an uncaught error becomes a tool error |
| TC-44 | The swarm tool runs plans and guards the driver | `crates/jcode-app-core/src/tool/communicate_tests.rs` | The driver guard blocks a second live driver, releases on drop, and the summary reports failed nodes |
| TC-45 | The swarm tool assigns tasks and spawns workers | `crates/jcode-app-core/src/tool/communicate_tests/assignment.rs` | The next runnable task is assigned, slots are topped up, and a fresh spawn can be preferred |
| TC-46 | The swarm tool detects a credential-failure wave | `crates/jcode-app-core/src/tool/communicate_tests/credential_failures.rs` | A wave needs at least two recent auth failures and ignores stale or foreign members |
| TC-47 | The swarm tool input format and member rendering | `crates/jcode-app-core/src/tool/communicate_tests/input_format.rs` | The delivery and share flags are accepted and duplicate member names are disambiguated |
| TC-48 | The ambient tools parse their inputs and build the permission context | `crates/jcode-app-core/src/tool/ambient/tests.rs` | String numbers and booleans are coerced, the schedule target defaults correctly, and a non-ambient session is rejected |
| TC-49 | The compile_remote tool gates access and bounds responses | `crates/jcode-app-core/src/tool/compile_remote/tests.rs` | Signed-out, subscription-required, and ready states are distinguished, and the response is bounded |
| TC-50 | The macOS computer-use tool validates actions and its schema | `crates/jcode-app-core/src/tool/computer/tests.rs` | An unknown action is rejected, a move needs coordinates, a dry run does not mutate, and the schema declares every field |
| TC-51 | The macOS computer-use tool covers the platform surface | `crates/jcode-app-core/src/tool/computer/coverage_tests.rs` | Text editing, observation, input, accessibility, windows, apps, clipboard, and scripting are all reachable |
| TC-52 | The self-dev tool queues builds and saves the reload context | `crates/jcode-app-core/src/tool/selfdev/tests.rs` | The build lock is released on drop, the request history is archived, and the reload context round-trips |
| TC-53 | The desktop self-dev tool builds, reloads, and screenshots safely | `crates/jcode-app-core/src/tool/desktop_selfdev_tests.rs` | Every action refuses a non-desktop context, the reload is read-only, and a symlinked screenshot destination is rejected |
| TC-54 | The browser tool maps requests and exposes the advanced fields | `crates/jcode-app-core/src/tool/browser_tests.rs` | A snapshot maps to an annotated content request, an eval maps to a script, and the advanced fields are in the schema |
| TC-55 | The browser fast path observes, decides, and hands back | `crates/jcode-app-core/src/tool/browser_fast_tests.rs` | The loop observes after each action, an uncertain decision never executes, and a stall returns control |
| TC-56 | The browser session reuses one daemon across calls | `crates/jcode-app-core/src/tool/browser_session_tests.rs` | Five calls share one daemon and concurrent calls start only one |
| TC-57 | The browser user-browser surfaces every window | `crates/jcode-app-core/src/tool/browser_user_browser_tests.rs` | A closed agent window is restarted and retried once, and an explicit tab is not retried |
| TC-58 | The integration catalog is searched and filtered | `crates/jcode-app-core/src/tool/discover.rs` (inline tests) | Search, details, select, and suggest each return their expected shape |
| TC-59 | The Gmail and calendar tools parse their inputs and render results | `crates/jcode-app-core/src/tool/gmail.rs`, `crates/jcode-app-core/src/tool/calendar.rs` (inline tests) | Each action parses and its result renders |
| TC-60 | The shared intent and escape-hatch injection applies to every object schema | `crates/jcode-tool-core/src/lib.rs` | `intent` is added and required, the escape hatch is optional, and a tool's own declaration survives |
| TC-61 | The shared output model and alias table behave as specified | `crates/jcode-tool-types/src/lib.rs` | The output builders set their fields and the alias table maps every documented alias |
| TC-62 | Background task management, in-flight tracking, and per-path locking | `crates/jcode-app-core/src/tool/bg.rs`, `crates/jcode-app-core/src/tool/inflight.rs`, `crates/jcode-app-core/src/tool/file_lock.rs` (inline tests) | A task is listed and cancelled, an in-flight call is marked and cleared, and a path lock is exclusive |
| TC-63 | The conversation history search filters and formats | `crates/jcode-app-core/src/tool/conversation_search.rs` (inline tests) | A query returns the matching turns and an empty history returns no result rather than panicking |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-64 | The swarm tool drives a real agent session end to end | `crates/jcode-app-core/src/tool/communicate_tests/end_to_end.rs` | Members are listed and awaited, a background await returns immediately, a spawn reports back to the spawner, and a direct message is routed as a direct message |
| TC-65 | The browser live handoff completes local navigation and search | `crates/jcode-app-core/src/tool/browser_fast_live_tests.rs`, against the local fixture server | The handoff navigates, searches, and resumes after a requested script, and a sensitive fixture is handed back without actions |
| TC-66 | The browser live acceptance check for the reported defect passes | `crates/jcode-app-core/src/tool/browser_live_1743_tests.rs`, against a live browser | Every acceptance item reports success |
| TC-67 | A browser observation timeout retains the last connection error and dispatches nothing | `crates/jcode-app-core/src/tool/browser_fast_tests/reconnect_timeout.rs` | The result is a hand-back whose reason carries the last connection error, and the transport receives no request |
| TC-68 | The custom web search exchanges a real request with a local HTTP server | `crates/jcode-app-core/src/tool/websearch_tests.rs`, with a local HTTP server | The query and count arrive as configured, a redirect is not followed, and the transport and JSON errors hide the URL and its secrets |
| TC-69 | Remote MCP management connects, discovers, calls, and disconnects over real HTTP | `crates/jcode-app-core/src/tool/mcp_remote_management_tests.rs`, with a local HTTP server | The transport and static headers are preserved, the call reaches the server, and the status output carries no secret |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-70 | The ambient end-cycle tool runs inside a full agent turn | `tests/e2e/ambient.rs`: a mock provider queues an `end_ambient_cycle` tool call, the agent runs, the provider is called again | The turn completes and the cycle result holds the summary and counters the tool reported |
| TC-71 | The ambient request-permission tool runs inside a full agent turn | `tests/e2e/ambient.rs`: a mock provider queues a `request_permission` tool call | The permission request reaches the caller with the action, the description, the rationale, and the urgency |
| TC-72 | The ambient schedule tool runs inside a full agent turn | `tests/e2e/ambient.rs`: a mock provider queues a `schedule` tool call | The wake-up is scheduled with the requested target and priority |
| TC-73 | Tool names are classified into permission tiers | `tests/e2e/safety.rs`: classify a list of tool names | Read, glob, grep, memory, and the todo tools are auto-allowed, while bash, edit, and write require permission, and the classification is case-insensitive |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-74 | The read tool is given both range styles, or a zero start line | The call is rejected with a message naming the two styles, and a zero `start_line` is rejected as one-based |
| TC-75 | The read tool is given a path that does not exist | The error names the missing file and suggests the closest existing path when one is close enough |
| TC-76 | The write tool is given a path whose parent directory does not exist | The parent directories are created and the file is written |
| TC-77 | The apply_patch tool is asked to delete a protected path | The deletion is refused and the file is untouched, while an ordinary file is still deleted |
| TC-78 | The bash tool is given a timeout of 5000 ms or less | The timeout message spells out the seconds and states that the parameter is in milliseconds |
| TC-79 | Every web search engine returns nothing | The tool returns a no-results message that names the SearXNG workaround instead of failing silently |
| TC-80 | A custom search header names an environment variable that is missing or empty | The call fails before any network access and the message contains no credential |
| TC-81 | The webfetch tool is given a URL that is not HTTP or HTTPS | The call is rejected before any request is made |
| TC-82 | An MCP tool is denied under its legacy name but called through the deferred surface | The dispatch is refused, and a deny on either spelling wins |
| TC-83 | Two MCP servers expose a tool with the same name | The two tools get distinct aliases and each alias maps back to its own server |
| TC-84 | The batch tool is given more than ten calls, or is asked to call itself | The oversized batch is rejected, and a function-namespaced or self-referential batch is refused |
| TC-85 | A codemode script calls the codemode tool or the batch tool | The call is refused, so a script cannot recurse into itself or fan out through the batch |
| TC-86 | The initiative tool is absent from the registry | `crates/jcode-app-core/src/tool/tests.rs` | The tool name list and the published definitions both exclude the initiative tool |
| TC-87 | The registry is built without the desktop UI capability | The applet tool and the user_response tool are absent, and a call to either name fails as an unknown tool |
| TC-88 | The request_permission tool is called from a session that is not an ambient session | The call is rejected |
| TC-89 | The compile_remote tool is pointed at an insecure or credential-bearing endpoint | The endpoint is rejected before any upload happens |
| TC-90 | The browser fast path is handed a sensitive page | The page never reaches the transport and the result is a hand-back |
| TC-91 | A batch subcall returns an image while a sibling subcall fails (`crates/jcode-app-core/src/tool/batch_tests.rs`) | The images are preserved in input order despite the failure |
| TC-92 | Integration discovery is disabled | The `integration_tools` tool is never registered and no discovery endpoint is contacted |

## Test Infrastructure

- Tests are in-crate `#[cfg(test)]` modules, with the larger suites mounted with `#[path = "..."] mod tests;` so that a file stays inside the CI test-size budget.
- The tool registry is built with `Registry::new(provider)` in the tests, and a `ToolContext` is built per test with the session, message, tool-call, and working-directory fields the tool needs.
- `crates/jcode-app-core/src/tool/testdata/` holds the captured DuckDuckGo fixtures: `ddg_results.html` and `ddg_anomaly.html`.
- The browser suites use a mock browser and a mock transport so that no real browser is required; the live suites need a browser daemon and a local fixture server and are skipped otherwise.
- The custom web search and the remote MCP suites run a local HTTP server on a loopback port.
- The webfetch corpus is a directory of captured pages, and the corpus test is skipped when the directory is absent.
- The macOS computer-use suites need a macOS host with accessibility permissions and are skipped elsewhere.
- The ambient end-to-end tests use the mock provider in `tests/e2e/mock_provider.rs` to queue a tool call and then a final answer.
- The per-path file lock and the in-flight registry are exercised through their own modules, so no external service is needed.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-27, TC-28, TC-63 |
| FR-2 | TC-1, TC-60 |
| FR-3 | TC-7, TC-27, TC-60 |
| FR-4 | TC-4, TC-27 |
| FR-5 | TC-5, TC-10, TC-11, TC-12, TC-82 |
| FR-6 | TC-9 |
| FR-7 | TC-7, TC-8 |
| FR-8 | TC-13, TC-14, TC-74, TC-75 |
| FR-9 | TC-15, TC-39, TC-76 |
| FR-10 | TC-16 |
| FR-11 | TC-25, TC-26, TC-77 |
| FR-12 | TC-17 |
| FR-13 | Not covered. The `ls` tool has no dedicated test file. |
| FR-14 | TC-23, TC-24 |
| FR-15 | TC-18, TC-19 |
| FR-16 | TC-19 |
| FR-17 | TC-20, TC-78 |
| FR-18 | TC-22, TC-31, TC-79 |
| FR-19 | TC-29, TC-30, TC-68, TC-80 |
| FR-20 | TC-31, TC-79 |
| FR-21 | TC-29, TC-32, TC-81 |
| FR-22 | TC-30, TC-68, TC-80 |
| FR-23 | TC-32, TC-81 |
| FR-24 | TC-33, TC-69 |
| FR-25 | TC-33, TC-82 |
| FR-26 | TC-11, TC-83 |
| FR-27 | TC-11 |
| FR-28 | TC-27, TC-84 |
| FR-29 | TC-44, TC-45, TC-46, TC-47, TC-64 |
| FR-30 | TC-35, TC-36 |
| FR-31 | TC-62 |
| FR-32 | TC-37 |
| FR-33 | TC-34, TC-63 |
| FR-34 | TC-38 |
| FR-35 | TC-1, TC-58 |
| FR-36 | TC-1, TC-9, TC-5, TC-6 |
| FR-37 | TC-6 |
| FR-38 | TC-41 |
| FR-39 | TC-42, TC-87 |
| FR-40 | TC-54, TC-55, TC-56, TC-57, TC-65, TC-66, TC-67, TC-90 |
| FR-41 | TC-49, TC-89 |
| FR-42 | TC-43, TC-85 |
| FR-43 | TC-58, TC-92 |
| FR-44 | TC-59 |
| FR-45 | TC-40 |
| FR-46 | TC-52, TC-53 |
| FR-47 | TC-48, TC-88, TC-70, TC-71, TC-72 |
| FR-48 | TC-50, TC-51 |
| FR-49 | TC-12 |
| FR-50 | TC-58, TC-73 |
| FR-51 | TC-86 |
| NFR-1 | TC-1 |
| NFR-2 | TC-7, TC-8 |
| NFR-3 | TC-13, TC-40, TC-48 |
| NFR-4 | TC-30, TC-68, TC-80, TC-89 |
| NFR-5 | Not covered. The per-path file lock has a unit test but no concurrent-write test. |
| NFR-6 | TC-11 |
| NFR-7 | TC-1 |
| NFR-8 | TC-2 |
| NFR-9 | TC-3, TC-13 |
| NFR-10 | TC-1, TC-9 |
| NFR-11 | TC-43 |
| NFR-12 | TC-50, TC-87 |
