---
title: "Diagnostics timeline"
status: done
---

# Test Plan: Diagnostics timeline

## Scope

The plan covers the server journal, fixed-vocabulary classification, local file and SSH collection, OpenCode load accounting, opt-in startup phase logging, and the UI capture, validation, merge, and formatting path.
It covers local and remote export paths, coverage reporting, redaction, and buffer limits.
It does not cover the status dialog rendering, the shortcut binding, or the command palette registration, because no automated test file exercises those UI surfaces.
It does not cover dedicated mobile or VS Code debug buffers, which are separate app processes.

## Unit Tests

| ID | Test file | Description | Input | Expected Output |
|---|---|---|---|---|
| TC-1 | `packages/web/server/lib/diagnostics/vocabulary.test.js` | Error-message coercion and allowlist | Objects with `length` and `toString`, `null`, `7`, and a symbol | Known messages become fixed templates, invalid values return `null`, and coercion counts stay unchanged |
| TC-2 | `packages/web/server/lib/diagnostics/server-journal.test.js` | HTTP response grouping and redaction | 120 failed requests to session-specific paths, one 503, one 200, and one secret-bearing 401 | One grouped 404 event with route template, count, and span, plus the 503 and `/api/other` events, with no private text |
| TC-3 | `packages/web/server/lib/diagnostics/server-journal.test.js` | Lifecycle allowlist and bounds | Secret action text, bad failure class, valid attempt and class, and a two-event journal with a short age | Only fixed actions and enum details appear and the snapshot reports truncation and expiry |
| TC-4 | `packages/web/server/lib/diagnostics/startup-performance.test.js` | Startup logging disabled by default | `OPENCHAMBER_STARTUP_PERF` unset and one phase call | `console.info` is not called |
| TC-5 | `packages/web/server/lib/diagnostics/startup-performance.test.js` | Approved phases and metadata | `OPENCHAMBER_STARTUP_PERF=1` and `proxy.readiness-hold` with valid durations, attempt, outcome, route class, and secret fields | One event with approved fields and a finite timestamp, and no secret text |
| TC-6 | `packages/web/server/lib/diagnostics/startup-performance.test.js` | Reject unknown labels and invalid values | Unknown phase, negative duration, fractional attempt, and secret outcome and route class | Only the known phase is logged and invalid fields are omitted |
| TC-7 | `packages/web/server/lib/diagnostics/opencode-load.test.js` | Process tree summary | Parsed `ps` table with grandchildren, the bundled executable case, and unrelated pids | Megabyte totals and child counts for valid trees, and `null` for a pid that is not OpenCode here |
| TC-11 | `packages/web/server/lib/diagnostics/local-files.test.js` | Fixed log-line classification | Known startup, lifecycle, relay, updater, proxy, stream, access, and health lines mixed with secret text | Recognized lines become fixed categories with bounded details, and every unrecognized line returns `null` |
| TC-16 | `packages/web/server/lib/diagnostics/local-files.test.js` | SSH line classification | Bracketed millisecond timestamps, known phases, injected phase names, and secret output | Only known phases and SSH messages become events, with severity prefixes and no host or password text |
| TC-19 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Merge ordering | Three event lists with equal timestamps | Events sort by timestamp and ties keep their original order |
| TC-20 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Renderer buffer limit | 1,600 recorded events | The buffer holds 1,500 events, the oldest retained event is `event-100`, and 100 are reported omitted |
| TC-21 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Buffer clear and scope advance | `clearDiagnosticEvents` after prior events | Events and omitted count are zero and the scope start time does not move backwards |
| TC-22 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Identity labels and cap | Session, directory, and message values plus 5,001 distinct sessions | Values map to sequential labels, a repeated value keeps its label, oversized values become `unavailable`, and the oldest label is evicted at the cap |
| TC-23 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Console capture allowlist | Tagged calls, untagged warnings and errors with secret errors, and an unclassified info call | Only vetted tags and warnings or errors are recorded, all arguments are discarded, and known error messages use fixed templates |
| TC-24 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Renderer error details | Same-origin asset URLs, off-origin URLs, allowed error names, and secret messages | Only allowlisted error names and a verified same-origin asset location with line and column appear |
| TC-25 | `packages/ui/src/lib/diagnostics/timeline.test.ts` | Rejection details | Typed error with a templated message, arbitrary error text, and `null` | Type and fixed message templates are retained and arbitrary text is dropped |
| TC-29 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Console wrapping is opt in | Capture started with `captureConsole` false and then true, with a `console.warn` call in each | The development case leaves `console.warn` untouched and records nothing, the production case records a tagged event, and the stop function restores the original |
| TC-38 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Start error classification | Signal exit, `ENOENT`, external server failure, and arbitrary secret text | Each known form becomes a fixed label and unknown text becomes `unclassified` |

## Integration Tests

| ID | Test file | Description | Preconditions | Expected Outcome |
|---|---|---|---|---|
| TC-8 | `packages/web/server/lib/diagnostics/opencode-load.test.js` | Load counts with injected dependencies | Stubbed OpenCode `fetchImpl`, `ps` output, auth headers, and `darwin` platform | Directory count and process totals are returned, no path appears, and auth headers are passed |
| TC-9 | `packages/web/server/lib/diagnostics/opencode-load.test.js` | Process counting unavailable | `win32` platform and a throwing process lister | Directory count is kept and `processes` is `null` |
| TC-10 | `packages/web/server/lib/diagnostics/opencode-load.test.js` | Unknown versus empty values | Failed location read, malformed OpenCode info, and valid empty locations | Failed reads become `null`, valid empty arrays become `0`, and no process walk runs without a valid pid |
| TC-12 | `packages/web/server/lib/diagnostics/local-files.test.js` | Access-failure burst grouping | Temporary log directory with repeated 404s, a distinct 503, and a later 404 | One event carries `count=3` and `spanMs`, the 503 and later 404 stay separate, and no secret text appears |
| TC-13 | `packages/web/server/lib/diagnostics/local-files.test.js` | Stream failures grouped by reporter | Temporary log with message-stream and PushWatcher failures, a secret line, and a later burst | Each reporter gets its own bounded group, other warnings remain visible, and the secret line is filtered |
| TC-14 | `packages/web/server/lib/diagnostics/local-files.test.js` | Filtered and empty coverage | A web log with only unclassified text and then an empty file | Coverage reports `filtered` with a count and then `empty`, and the secret text never appears |
| TC-15 | `packages/web/server/lib/diagnostics/local-files.test.js` | Journal and file merge | Injected journal with a launch event and a temp web log with a health line | Events are ordered by timestamp and the journal coverage is `read` |
| TC-17 | `packages/web/server/lib/diagnostics/local-files.test.js` | SSH buffer cap | 8,001 classified SSH lines | The newest 8,000 events remain and coverage reports `truncated` with `omitted: 1` |
| TC-18 | `packages/web/server/lib/diagnostics/local-files.test.js` | SSH filtered coverage | One unclassified SSH info line and an invalid phase | No events are emitted and coverage reports `filtered` with the line count |
| TC-26 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Local runtime detection | Stubbed `window`, local origin, and three runtime resolver bases | Local base is accepted, another loopback port and a remote host are rejected |
| TC-27 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Remote export | Stubbed remote fetch for health and probes, a local buffer entry, a secret session error, and a runtime switch | The log holds remote health and probe events, states that local sources were skipped, contains no private text, and an interrupted export has no health section |
| TC-28 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Selection and failure correlation | Stubbed local runtime, capture started, session and directory changes, a turn error, and a rejected send | The log uses sequential labels for selections and failures and contains none of the original ids, paths, or bearer text |
| TC-30 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Malformed transport records | Valid SSH event and coverage mixed with secret actions, sources, and counts | Valid records stay, invalid records are dropped, and one `invalid records omitted` coverage entry is added |
| TC-31 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Journal action allowlist | Lifecycle actions with valid details, OpenCode child output, and secret action or detail text | Only the two valid journal events survive and the rest are counted as omitted |
| TC-32 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Proxy detail allowlist | Known proxy details, unknown routes, unknown handlers, and secret messages | Only allowlisted proxy details survive and omitted count covers the rest |
| TC-33 | `packages/ui/src/lib/diagnostics/capture.test.ts` | HTTP burst bounds | Counts and spans inside and outside the allowed range, plus a wrong source | Only bounded bursts from allowed sources survive |
| TC-34 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Completed response details | Valid downstream journal response plus wrong source, private route, extra text, wrong stage, and a 200 response | Only valid 4xx and 5xx downstream journal events survive |
| TC-35 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Stream reporter bounds | Two known reporters with valid stages and messages plus unknown sources, stages, counts, and spans | Only known reporters with bounded details survive |
| TC-36 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Updater message allowlist | Known updater template and variants with a URL, wrong source, or extra text | Only the known updater event survives |
| TC-37 | `packages/ui/src/lib/diagnostics/capture.test.ts` | Health snapshot and probes | Stubbed health body, version payload, proxy event, failed health, and invalid JSON body | The log carries one health probe, fixed health fields, classified start error, probe status and content class, and no secret text |

## End-to-End Tests

No dedicated end-to-end test file covers the dialog entry points, the copy button, or the download button.
Those paths are verified in the running app through the shortcut, the palette item, the failed-turn link, and the copied or downloaded `.log` file.
The generated log text itself is covered by TC-27, TC-28, and TC-37.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior | Verified by |
|---|---|---|---|
| EDGE-1 | A reused pid belongs to an unrelated process | Process summary is `null` unless the command names OpenCode or the pid is a direct child of this server | TC-7 |
| EDGE-2 | OpenCode runs on Windows, another host, or inside WSL | Process counts are not reported and the load line says they were not counted | TC-9 |
| EDGE-3 | An OpenCode read fails but another read succeeds | Failed parts are `null` and do not turn into zero while valid parts remain | TC-10 |
| EDGE-4 | A bracketed log timestamp has no timezone | The event keeps the wall-clock instant without a UTC shift | TC-11 |
| EDGE-5 | A known log message has neighboring private text | The line is rejected as a whole rather than partially matched | TC-11 |
| EDGE-6 | An identity value exceeds 1,024 characters | The label is `unavailable` and the value is not stored | TC-22 |
| EDGE-7 | A runtime switch happens during export | The log is replaced by an "Export interrupted" notice | TC-27 |
| EDGE-8 | A health request or probe fails or returns HTML | The export says health is unavailable or records a probe failure and keeps other sources | TC-27, TC-37 |
| EDGE-9 | A response carries invalid records beside valid ones | Only invalid records are dropped and counted under diagnostic transport | TC-30 |
| EDGE-10 | A file contains only unclassified lines | Coverage is `filtered`, not `empty` or `read` | TC-14, TC-18 |
| EDGE-11 | A sustained failure burst exceeds a cap | The count is capped at 4,000 and the snapshot reports truncation when events are evicted | TC-2, TC-3, TC-17 |
| EDGE-12 | An error object has a custom message getter that throws | Renderer detail helpers catch it and return no message | TC-24, TC-25 |
| EDGE-13 | Startup diagnostics are left at their default | No startup phase lines are written | TC-4 |
| EDGE-14 | Console capture is disabled in a development build | The original console functions receive calls and DevTools keeps call sites | TC-29 |

## Test Infrastructure

- Server tests use Vitest and `.js` import specifiers that resolve to TypeScript implementations.
- UI tests use `bun:test` and the `@/` path alias from `packages/ui`.
- Temporary directories from `fs.mkdtemp` provide isolated log files for collector tests.
- Injected clocks, `fetchImpl`, `listProcesses`, `platform`, and journal objects avoid spawning processes and network calls.
- Stubbed `window`, `document`, runtime URL resolver, and `globalThis.fetch` isolate the UI capture and export paths.
- Store state is saved and restored around capture tests so shared Zustand state does not leak between cases.

## Coverage Matrix

| Requirement | Test cases |
|---|---|
| FR-1 | TC-27, TC-37 |
| FR-2 | TC-20, TC-23, TC-29 |
| FR-3 | TC-22, TC-28 |
| FR-4 | TC-2, TC-3, TC-31, TC-34 |
| FR-5 | TC-11, TC-14, EDGE-5 |
| FR-6 | TC-7, TC-8, TC-9, TC-10 |
| FR-7 | TC-30, TC-31, TC-32, TC-33, TC-34, TC-35, TC-36 |
| FR-8 | TC-19, TC-27, TC-37, TC-38 |
| FR-9 | TC-26 |
| FR-10 | TC-27 |
| FR-11 | TC-21, TC-27, EDGE-7 |
| FR-12 | TC-37 |
| FR-13 | TC-2, TC-12, TC-13, TC-33, TC-35 |
| FR-14 | TC-4, TC-5, TC-6 |
| FR-15 | TC-16, TC-17, TC-18 |
| FR-16 | No dedicated automated test file exists. The counters are inspected through `window.__openchamberSyncPerformance` at runtime. |
| NFR-1 | TC-1, TC-2, TC-8, TC-11, TC-16, TC-23, TC-24, TC-25, TC-28, TC-30, TC-32, TC-37 |
| NFR-2 | TC-3, TC-17, TC-20, TC-22 |
| NFR-3 | TC-10, TC-14, TC-18, TC-27, TC-37 |
| NFR-4 | TC-27, TC-37 |
| NFR-5 | TC-26, TC-27 |
| NFR-6 | TC-11 |
| NFR-7 | TC-37 |
| NFR-8 | TC-29 |
