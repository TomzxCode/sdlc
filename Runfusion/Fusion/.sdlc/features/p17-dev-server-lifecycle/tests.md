---
title: "Dev Server Lifecycle Management"
status: done
---

# Test Plan: Dev Server Lifecycle Management

## Scope

This plan covers the dev-server subsystem in `@fusion/dashboard`: script detection, the persisted store, preview-URL detection and port probing, the child-process lifecycle, the `/api/dev-server/*` routes, the disconnected `devserver-*` family, and the dashboard Dev Server view with its log viewer, preview iframe, and hooks.

Out of scope:
- The engine mission verification app harness and the CLI dev-source restart command, which reuse the port-detection rules for their own purposes.
- The right-dock placement of the view, which is covered by the dock and navigation tests.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Detect scripts in the root manifest and rank them | A root `package.json` with `dev` and `serve` scripts | Both candidates returned, `dev` ranked above `serve` |
| TC-2 | Scan workspace manifests | `packages/*/package.json` and `apps/*/package.json` | Workspace candidates returned with their relative source path |
| TC-3 | Score candidates | A manifest with a framework dependency, and one that is `private` or has no `main` | The framework and private heuristics raise the confidence score |
| TC-4 | Tolerate a malformed manifest | A `package.json` that is not valid JSON | Empty candidate list, no throw |
| TC-5 | Read and write the persisted state | A state and a config written to `.fusion/dev-server.json` | Both round-trip through the store |
| TC-6 | Normalize a corrupt state file | A `.fusion/dev-server.json` that is not valid JSON | Default state and default config, no throw |
| TC-7 | Bound the persisted log history | More than 500 appended lines | The history holds the last 500 lines |
| TC-8 | Survive a removed project directory | A save after the project directory was deleted | The save is a no-op, no throw |
| TC-9 | Parse a Vite URL line | A `Local: http://localhost:5173` line | The URL and port 5173 are detected, source `vite` |
| TC-10 | Parse Next.js, Storybook, and Angular lines | The startup lines of each framework | The URL and port are detected, source `nextjs`, `storybook`, or `angular` |
| TC-11 | Parse a generic URL line and a keyword-plus-port line | A plain `http://127.0.0.1:3000` line and a `listening on port 4321` line | Both are detected, source `generic-url` and `generic-port` |
| TC-12 | Strip ANSI codes and skip inspector lines | A colored URL line and a Node inspector line | The colored line is detected, the inspector line is ignored |
| TC-13 | Exclude the reserved port | A line announcing port 4040 | No preview URL is detected |
| TC-14 | Search the logs from newest to oldest | A list of log lines | The newest matching line wins |
| TC-15 | Probe fallback ports in order | Two open common ports | The earlier port in the fixed list is reported, source `fallback-probe` |
| TC-16 | Reject an unsafe start command | A command containing `$(...)` | The start is refused before a child is spawned |
| TC-17 | Refuse a duplicate start | A manager that already holds a running child | The start throws and no second child is spawned |
| TC-18 | Start, persist output, and detect the announced URL | An injected child that writes a URL line | The state moves to `running`, the line is persisted, and the URL is detected once |
| TC-19 | Stop through the process-tree signal | An injected child and an injected kill function | The termination signal is sent and the fallback probe timer is cleared |
| TC-20 | Escalate to the kill signal | A child that ignores the termination signal | The kill signal is sent after the stop timeout |
| TC-21 | Clean up on failure and restart | A child that emits an error | The state is `failed`, the timer is cleared, and a restart produces a fresh child |
| TC-22 | Reconcile a stale persisted process id | A persisted `running` state whose process id is not alive | The state becomes `stopped` with exit code 1 and a recovery line is appended |
| TC-23 | Rehydrate the persisted state and logs | A persisted state and log history | The snapshot carries the state and the restored logs |
| TC-24 | Detect the preview URL from a session log | A session whose child writes `http://localhost:3000` | The session carries the detected preview URL |
| TC-25 | Probe a fallback port in a session | A session with no announced URL and an open common port | The session preview URL points at the open port |
| TC-26 | Keep the manual override and the detected fields apart | A session with both a manual URL and a detected URL | The manual URL stays effective while the detected fields keep updating |
| TC-91 | Brand the session id | A plain string | The branded id is a string and equals the input |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-27 | Serve the detected candidates | A router mounted on a temporary project root | `GET /api/dev-server/detect` returns 200 with a `candidates` array |
| TC-28 | Serve the default config | A project root with no config file | `GET /api/dev-server/config` returns 200 with all fields null |
| TC-29 | Store a config update | A router on a project root | `PUT /api/dev-server/config` returns 200 and the stored values are read back |
| TC-30 | Reject an invalid config update | An empty body, and a `previewUrlOverride` that is not a URL | Both return 400 |
| TC-31 | Serve the default status | A router on an empty project root | `GET /api/dev-server/status` returns 200 with status `stopped`, `previewUrl` null, `detectedPort` null, `manualPreviewUrl` null, and `isRunning` false |
| TC-32 | Resolve the preview URL in the status response | A store with a detected URL, a detected port, and a manual URL | The manual URL is the resolved `previewUrl`, and the detected port is reported |
| TC-33 | Fall back to the detected URL | A store with a detected URL and no manual URL | The detected URL is the resolved `previewUrl` |
| TC-34 | Start through the route | A router and a long-lived command | `POST /api/dev-server/start` returns 200 with status `running` and the requested working directory |
| TC-35 | Reject an invalid start | A start request without a command, and one without a working directory | Both return 400 |
| TC-36 | Refuse a concurrent start | A running dev server | The second `POST /api/dev-server/start` returns 409 |
| TC-37 | Stop through the route | A running dev server | `POST /api/dev-server/stop` returns 200 with status `stopped` |
| TC-38 | Keep stop idempotent | No running dev server | `POST /api/dev-server/stop` returns 200 with the unchanged state |
| TC-39 | Restart through the route | A dev server started with a command, a working directory, and a script id | `POST /api/dev-server/restart` returns 200 with the same command and script id |
| TC-40 | Refuse a restart with no stored command | No stored command | `POST /api/dev-server/restart` returns 400 |
| TC-41 | Set and clear the preview override | A router on a project root | `PUT /api/dev-server/preview-url` stores the manual URL, and an empty URL clears it |
| TC-42 | Reject a malformed preview URL | A URL of `localhost:5173` | `PUT /api/dev-server/preview-url` returns 400 |
| TC-43 | Open the log stream | A client subscribed to the stream | The response carries the `text/event-stream` content type, a `: connected` comment, and a `history` event with the stored lines |
| TC-44 | Forward live output | A subscribed client and a manager that emits an output event | The stream carries a `log` event with the line |
| TC-45 | Forward the URL-detected event | A subscribed client and a manager that emits a url-detected event | The stream carries a `dev-server:url-detected` event whose payload has exactly `url`, `port`, `source`, and `detectedAt` |
| TC-46 | Release the stream listeners | A subscribed client that disconnects | The manager listener count for `output` and `url-detected` returns to zero |
| TC-47 | Load the Dev Server view | A view with detected candidates | The candidate buttons render, and the no-candidates message renders when the list is empty |
| TC-48 | Drive the lifecycle from the view | A stopped server | Start, stop, and restart each call the matching hook action, and the start button is disabled while running |
| TC-49 | Select a candidate | A candidate click | The selected-script summary renders and the candidate list can be re-shown |
| TC-50 | Save the preview URL override | The preview URL input | The saved value is sent to the preview URL action |
| TC-51 | Target a task worktree | One task in a work-in-progress column with a worktree and one without | Only the task with a worktree is listed, and starting the server runs in that worktree |
| TC-52 | Guide the operator on a task switch | A running server | Switching the selected task shows the restart guidance message |
| TC-53 | Restore the typed command after a remount | An unmount and remount of the view | The typed command and the selected script are restored |
| TC-54 | Render the narrow dock preview launcher | A dock host narrower than 480 pixels | The inline preview is replaced by the launcher, and a true mobile viewport keeps the inline preview |
| TC-55 | Report the embed states | A preview URL | The states are `loading`, `embedded`, `blocked`, and `error`, and the blocked and error states offer open-in-new-tab and retry |
| TC-56 | Refresh the preview | A preview URL | The refresh action resets the embed state, and the fallback clears when the embed succeeds after a retry |
| TC-57 | Render the log viewer | A set of log entries | The entries, the timestamps, and the stderr badge render, the ANSI codes are stripped, the severity filter and the search work, the load-more button fires, and the fullscreen class toggles |
| TC-58 | Follow the log stream | New entries arriving while pinned | The view scrolls to the bottom while pinned, and the jump-to-latest action re-pins |
| TC-59 | Load and stream logs | The logs hook enabled for a project | The initial history loads, live entries append, entries deduplicate by id, the history caps at the maximum, and load-more fetches older entries |
| TC-60 | Reopen the log subscription on a project change | A project id change | The entries clear and a new subscription opens |
| TC-61 | Catch up after a reconnect | A reconnect event with the last seen event id | The hook fetches the entries after the last seen id |
| TC-62 | Instrument the log stream lifecycle | An open and a reconnect | Resume instrumentation records the stream open and the reconnect with the replay event id |
| TC-63 | Poll the session status | A running server | The status is fetched on a 3 second interval, and no poll runs while the server is stopped |
| TC-64 | Apply the session events | A `dev-server:status` event | The session status and process id update |
| TC-65 | Clean up on unmount | An unmounted view | The server-sent events subscription is released |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-66 | The project has no `package.json` | Detection returns an empty candidate list, and the view shows the no-candidates message |
| TC-67 | The project has no matching script name | Detection returns an empty candidate list |
| TC-68 | A workspace manifest is unreadable | That manifest is skipped and the other candidates are still returned |
| TC-69 | The state file holds an unknown status value | The status normalizes back to `stopped` |
| TC-70 | The state file holds a non-string log entry | The entry is filtered out of the history |
| TC-71 | The command is empty after trimming | The start is refused with 400 |
| TC-72 | The command contains command substitution | The start is refused before a child process is spawned |
| TC-92 | The command contains a backtick or a control character | The start is refused before a child process is spawned. No test covers these two guard branches today. |
| TC-73 | The child writes a line after the server was stopped | The late line does not reach the current state or the current log history |
| TC-74 | The fallback probe resolves after a stop | The probe does not write a detected URL into the stopped state |
| TC-75 | The detected URL write fails | The detection flag is reset so a later detection can run |
| TC-76 | The dev server prints an inspector line with a loopback URL | The line is not treated as a preview URL |
| TC-77 | The dev server prints a URL on a host other than localhost or 127.0.0.1 | The URL is not treated as a preview URL |
| TC-78 | The dev server prints a URL on a port above 65535 or 0 | The URL is not treated as a preview URL |
| TC-79 | No fallback port is open | The probe returns no result and the state keeps a null detected URL |
| TC-80 | The preview URL does not start with http:// or https:// | The preview URL update is refused with 400 |
| TC-81 | The preview URL is set to an empty string | The manual override is cleared and the detected URL becomes effective again |
| TC-82 | The config update body is not a JSON object | The update is refused with 400 |
| TC-83 | The config update body carries no known field | The update is refused with 400 |
| TC-84 | The client disconnects from the log stream | The heartbeat interval is cleared and the manager listeners are removed |
| TC-85 | The child process is killed externally | The close handler moves the state to `stopped` and records the exit code |
| TC-86 | The dashboard server shuts down | The running dev servers are stopped and cleaned up |
| TC-87 | The Dev Server view is hosted in a narrow right dock | The preview moves into a modal and the configuration and log panels stay usable |
| TC-88 | The browser tab is hidden while the server runs | The status polling is suspended and the view refreshes once when the tab becomes visible again |
| TC-89 | The operator selects a different task while the server runs | The view shows the restart guidance instead of silently changing the target |
| TC-90 | The selected task leaves the work-in-progress list | The selection is cleared |

## Test Infrastructure

- The backend route tests build an Express app in-process with `express.json()` and mount the router at `/api/dev-server`, then drive it with the `request` helper from `packages/dashboard/src/test-request.ts`.
- The server-sent events tests use a mock socket over `http.IncomingMessage` and `http.ServerResponse` to capture the written chunks.
- The process tests inject a fake child process through the `spawn` and `killManagedProcess` options, so no shell child runs.
- The store tests use a temporary project root created with `mkdtempSync` under the OS temp directory and removed in `afterEach`.
- The port-probe tests stub the `node:net` connection to control which ports answer.
- The frontend tests use Vitest with the React Testing Library, and stub the API client and the server-sent events bus.
- The narrow-dock tests drive the host width through a mocked `ResizeObserver` and `matchMedia`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-3, TC-4, TC-27, TC-66, TC-67, TC-68 |
| FR-2 | TC-28, TC-29, TC-30, TC-82, TC-83, TC-47, TC-49 |
| FR-3 | TC-17, TC-34, TC-35, TC-36, TC-48, TC-71 |
| FR-4 | TC-37, TC-38, TC-39, TC-40, TC-48 |
| FR-5 | TC-31, TC-32, TC-33, TC-63, TC-64 |
| FR-6 | TC-5, TC-6, TC-7, TC-8, TC-69, TC-70, TC-22, TC-23 |
| FR-7 | TC-43, TC-44, TC-45, TC-46, TC-59, TC-60, TC-61, TC-62, TC-65 |
| FR-8 | TC-9, TC-10, TC-11, TC-12, TC-13, TC-14, TC-15, TC-24, TC-25, TC-26, TC-76, TC-77, TC-78, TC-79 |
| FR-9 | TC-41, TC-42, TC-50, TC-80, TC-81 |
| FR-10 | TC-47, TC-48, TC-49, TC-50 |
| FR-11 | TC-51, TC-52, TC-89, TC-90 |
| FR-12 | TC-55, TC-56 |
| FR-13 | TC-57, TC-58 |
| FR-14 | TC-47 |
| FR-15 | TC-54, TC-87 |
| FR-16 | TC-53 |
| FR-17 | TC-63, TC-88 |
| NFR-1 | TC-16, TC-72, TC-92 |
| NFR-2 | TC-19, TC-20, TC-86 |
| NFR-3 | TC-19, TC-21, TC-74 |
| NFR-4 | TC-46, TC-84 |
| NFR-5 | TC-22 |
| NFR-6 | TC-73, TC-74, TC-75, TC-85 |
| NFR-7 | TC-13 |
| NFR-8 | TC-7, TC-59 |
| NFR-9 | TC-15, TC-25 |
| NFR-10 | TC-5, TC-18, TC-22, TC-23, TC-31 |
| NFR-11 | TC-6, TC-69, TC-70 |
| NFR-12 | TC-1, TC-2, TC-3, TC-4, TC-24, TC-25, TC-91 |

No automated guard asserts the import-graph boundary, so NFR-12 rests on the disconnected family's unit tests plus review.

## Key Test Files

Backend, canonical family:

- `packages/dashboard/src/__tests__/dev-server-detect.test.ts`
- `packages/dashboard/src/__tests__/dev-server-store.test.ts`
- `packages/dashboard/src/__tests__/dev-server-port-detect.test.ts`
- `packages/dashboard/src/__tests__/dev-server-process.test.ts`
- `packages/dashboard/src/__tests__/dev-server-manager.test.ts`
- `packages/dashboard/src/__tests__/dev-server-manager-persistence.test.ts`
- `packages/dashboard/src/__tests__/dev-server-routes.test.ts`
- `packages/dashboard/src/__tests__/dev-server-config-routes.test.ts`

Backend, disconnected family:

- `packages/dashboard/src/__tests__/devserver-types.test.ts`
- `packages/dashboard/src/__tests__/devserver-detect.test.ts`
- `packages/dashboard/src/__tests__/devserver-persistence.test.ts`
- `packages/dashboard/src/__tests__/devserver-manager.test.ts`
- `packages/dashboard/src/__tests__/devserver-preview-detect.test.ts`

Frontend:

- `packages/dashboard/app/components/__tests__/DevServerView.test.tsx`
- `packages/dashboard/app/components/__tests__/DevServerView.preview.test.tsx`
- `packages/dashboard/app/components/__tests__/DevServerLogViewer.test.tsx`
- `packages/dashboard/app/components/__tests__/PreviewIframe.test.tsx`
- `packages/dashboard/app/hooks/__tests__/useDevServer.test.ts`
- `packages/dashboard/app/hooks/__tests__/useDevServerLogs.test.ts`
- `packages/dashboard/app/hooks/__tests__/useDevServerLogs.resume-instrumentation.test.ts`
