---
title: "Dev Server Lifecycle Management"
status: done
---

# Requirements: Dev Server Lifecycle Management

## Overview

Fusion detects a project's dev-server command from its package manifests, starts, stops, and restarts that command for the current task, streams its output as live logs, and embeds a preview of the running app in a dashboard panel.
The dashboard detects candidate scripts from the project root and from workspace packages, scores and ranks them, and lets the operator pick one.
The dashboard can target the checked-out worktree of an executing task so the preview reflects in-progress work instead of the integration branch.
A background probe and per-framework log parsers discover the app's local URL so the preview opens without operator input, and the operator can override that URL by hand.
The whole surface sits behind the `devServerView` experimental feature flag and is reachable from the right dock.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Solo developer | Runs the project's dev server from the dashboard and sees the app without leaving the board |
| Operator / power user | Chooses which script runs, points the server at a task worktree, and manages the preview URL |
| Maintainer / contributor | Keeps the canonical `dev-server-*` module family free of drift against the disconnected `devserver-*` family |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall detect candidate dev-server scripts from the project root `package.json` and from workspace `packages/*` and `apps/*` manifests, and rank them by a confidence score derived from script-name priority, framework dependency indicators, and the `private`/missing-`main` heuristic |
| FR-2 | Must | The system shall expose the detected candidates over `GET /api/dev-server/detect`, read the persisted selection with `GET /api/dev-server/config`, and update the selected script, source, command, and preview URL override with `PUT /api/dev-server/config` |
| FR-3 | Must | The system shall start the dev server with `POST /api/dev-server/start`, spawning the command with a shell in the requested working directory, and shall reject the request with `400` when `command` or `cwd` is missing and with `409` when a server is already running |
| FR-4 | Must | The system shall stop the dev server with `POST /api/dev-server/stop` by sending `SIGTERM` to the process group and escalating to `SIGKILL` after the stop timeout, and shall restart it with `POST /api/dev-server/restart` using the stored command and working directory |
| FR-5 | Must | The system shall report the current dev-server state over `GET /api/dev-server/status`, including status, command, working directory, process id, timestamps, exit code, the detected preview URL and port, the manual preview URL override, the resolved preview URL, and whether the process is running |
| FR-6 | Must | The system shall persist the dev-server state and configuration to `.fusion/dev-server.json` in the project directory, and shall restore that state on load, capping the stored log history at 500 lines |
| FR-7 | Must | The system shall stream dev-server output to the dashboard over the `GET /api/dev-server/logs/stream` server-sent events endpoint, sending the stored history first and then live `log`, `stopped`, `failed`, and `dev-server:url-detected` events, with a heartbeat comment every 30 seconds |
| FR-8 | Must | The system shall detect the app's local preview URL from the process output, first by parsing framework-specific patterns (Vite, Next.js, Storybook, Angular) and then generic URL and keyword-plus-port patterns, and shall fall back to probing a fixed list of common local ports when no URL is announced |
| FR-9 | Must | The system shall let the operator override the preview URL with `PUT /api/dev-server/preview-url`, accepting only `http://` or `https://` URLs and clearing the override when the URL is empty |
| FR-10 | Must | The system shall render a Dev Server view in the dashboard that lists detected candidates, shows a status badge, starts, stops, and restarts the server, shows the running command, and exposes the preview URL override field |
| FR-11 | Must | The system shall let the operator point the dev server at the worktree of an executing task, listing only tasks in a work-in-progress column that have a worktree path, and using that worktree as the working directory of the started process |
| FR-12 | Must | The system shall embed the running app in an iframe preview that reports a loading, embedded, blocked, or error state, and shall offer an open-in-new-tab fallback when the app cannot be embedded |
| FR-13 | Must | The system shall show the dev-server output in a log panel that strips ANSI escape codes, filters by severity, searches the text, loads older lines, and can toggle fullscreen |
| FR-14 | Must | The system shall show the Dev Server panel only when the `devServerView` experimental feature flag is enabled, and shall accept the legacy `devServer` flag as an alias for it |
| FR-15 | Should | The system shall show the preview in a modal when the right dock that hosts the view is narrower than 480 pixels, keeping the configuration and log panels usable |
| FR-16 | Should | The system shall restore the typed command, the selected script, and the selected task when the Dev Server view remounts, per project |
| FR-17 | Should | The system shall poll the dev-server status every 3 seconds while the server is running or starting, and shall suspend that polling while the browser tab is hidden |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall reject a dev-server command that contains command substitution (`$(...)`, backticks, process substitution) or control characters, because the command is spawned with a shell |
| NFR-2 | Must | Resource cleanup | The system shall terminate the whole child process tree on stop, restart, cleanup, and dashboard server shutdown, so no dev-server process outlives the dashboard |
| NFR-3 | Must | Resource cleanup | The system shall clear the fallback port probe timer on stop, close, failure, restart, and cleanup, so a stopped server leaves no pending timer |
| NFR-4 | Must | Resource cleanup | The system shall release the server-sent events listeners and the heartbeat interval when the client disconnects from the log stream |
| NFR-5 | Must | Availability | The system shall mark a persisted running or starting server as stopped when its recorded process id is no longer alive, and shall log that recovery |
| NFR-6 | Must | Availability | The system shall ignore late lifecycle callbacks, stale stdout detection, and stale fallback probes from a previous run, so a restart cannot write into the previous run's state |
| NFR-7 | Must | Correctness | The system shall never suggest the reserved dashboard port 4040 as a preview port |
| NFR-8 | Should | Performance | The system shall keep the persisted and in-memory log history bounded to 500 lines |
| NFR-9 | Should | Performance | The system shall probe fallback ports sequentially in a fixed order so the first responsive port wins deterministically |
| NFR-10 | Should | Observability | The system shall record dev-server lifecycle transitions, the resolved preview URL and port, and the process exit code in the persisted state so an operator can inspect them after the fact |
| NFR-11 | Should | Availability | The system shall tolerate a malformed or missing `.fusion/dev-server.json` file by falling back to default state and configuration |
| NFR-12 | Should | Maintainability | The dashboard API shall use only the canonical `dev-server-*` module family, and the `devserver-*` family shall stay isolated from the runtime import graph |

## Constraints

- The feature is gated behind the `devServerView` experimental feature flag, with `devServer` accepted as a legacy alias
- The canonical runtime family is `dev-server-*` under `packages/dashboard/src` (`dev-server-routes.ts`, `dev-server-process.ts`, `dev-server-store.ts`, `dev-server-detect.ts`, `dev-server-port-detect.ts`)
- The `devserver-*` family under `packages/dashboard/src` (`devserver-detect.ts`, `devserver-manager.ts`, `devserver-persistence.ts`, `devserver-types.ts`) has no production importer and only its own unit tests
- The two families persist to different files, `.fusion/dev-server.json` and `.fusion/devserver.json`
- The dashboard API mounts the router at `/api/dev-server` through the `registerIntegratedDevServerRouter` registrar
- The child process is spawned through `superviseSpawn` from `@fusion/core` with `shell: true` and a 24 hour maximum lifetime
- Port 4040 is reserved for the dashboard and is never a preview port
- The persisted state file lives under the project directory and is not part of the task store

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Detect and rank candidate scripts
      Given a project root package.json with a "dev" script and a "serve" script
      When the operator requests the detected candidates
      Then the "dev" script is ranked above the "serve" script by confidence
      And the candidates for workspace packages are included with their relative source path
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Persist the selected script
      Given a detected candidate named "dev" in the root package
      When the operator saves a config update with selectedScript "dev" and selectedCommand "vite"
      Then GET /api/dev-server/config returns the saved values
      And GET /api/dev-server/config returns all null fields when no config file exists
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Start the dev server
      Given no dev server is running
      When the operator posts a command and a working directory to /api/dev-server/start
      Then the response status is "running" with the process id and the requested working directory
    ```

    ```gherkin
    @FR-3
    Scenario: Reject an invalid start request
      Given no dev server is running
      When the operator posts a start request without a command
      Then the response status is 400
    ```

    ```gherkin
    @FR-3
    Scenario: Refuse a second start
      Given a dev server is already running
      When the operator posts a start request
      Then the response status is 409
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Stop the dev server
      Given a dev server is running
      When the operator posts to /api/dev-server/stop
      Then the response status is "stopped" with an exit code
    ```

    ```gherkin
    @FR-4
    Scenario: Stop is idempotent
      Given no dev server is running
      When the operator posts to /api/dev-server/stop
      Then the response status is 200 and the current state is returned unchanged
    ```

    ```gherkin
    @FR-4
    Scenario: Restart uses the stored command
      Given a dev server was started with a command and a working directory
      When the operator posts to /api/dev-server/restart
      Then a new process runs with the same command and working directory
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Report the current status
      Given a dev server with an auto-detected URL and a manual URL override
      When the operator requests /api/dev-server/status
      Then the response carries the manual URL as the resolved preview URL
      And the response carries the detected port and the running flag
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Persist and restore the state
      Given a dev server that has produced more than 500 log lines
      When the store is written and loaded again
      Then the persisted file is at .fusion/dev-server.json and the log history holds the last 500 lines
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Stream logs to the dashboard
      Given a client subscribed to /api/dev-server/logs/stream
      When the dev server writes a line to stdout
      Then the stream emits a "log" event carrying the line
      And the stream emitted the stored history before the live events
    ```

    ```gherkin
    @FR-7
    Scenario: Release the stream on disconnect
      Given a client subscribed to /api/dev-server/logs/stream
      When the client disconnects
      Then the manager no longer holds the stream listeners
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Detect the preview URL from output
      Given a dev server that prints a Vite "Local: http://localhost:5173" line
      When the line is parsed
      Then the detected preview URL is http://localhost:5173 with port 5173
    ```

    ```gherkin
    @FR-8
    Scenario: Probe a fallback port when no URL is announced
      Given a running dev server that printed no URL and has an open local port
      When the fallback probe grace period elapses
      Then the detected preview URL points at the first open common port
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Set and clear the preview URL override
      Given a dev server with an auto-detected URL
      When the operator sets a manual URL of https://localhost:3000
      Then the state carries the manual URL
      And an empty URL clears the override
    ```

    ```gherkin
    @FR-9
    Scenario: Reject a malformed preview URL
      Given a dev server
      When the operator sets a preview URL of "localhost:3000"
      Then the response status is 400
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Show the detected candidates
      Given the detection endpoint returns two candidates
      When the operator opens the Dev Server view
      Then the view renders a candidate button for each detected script
    ```

    ```gherkin
    @FR-10
    Scenario: Drive the server from the view
      Given a stopped dev server
      When the operator clicks Start, Stop, and Restart in turn
      Then the view calls the matching lifecycle action for each click
      And the start button is disabled while the server is running
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Target an executing task worktree
      Given one task in a work-in-progress column with a worktree path and one without a worktree path
      When the operator opens the Dev Server view
      Then only the task with a worktree appears in the task picker
      And selecting it and starting the server runs the command in that worktree
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Embed the running app
      Given a running dev server with a preview URL
      When the preview iframe loads
      Then the embed status becomes "embedded"
    ```

    ```gherkin
    @FR-12
    Scenario: Offer a fallback when embedding is blocked
      Given a preview URL that cannot be embedded
      When the embed status becomes "blocked"
      Then the fallback panel offers "Open in new tab" and "Retry embedded preview"
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Filter and search the logs
      Given a set of log entries including stderr output
      When the operator filters by the error severity
      Then only the error entries remain
      And the ANSI escape codes are not rendered
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Hide the panel when the flag is off
      Given the devServerView experimental feature flag is disabled
      When the right dock entries are computed
      Then the Dev Server entry is not visible
      And it is visible when the flag is enabled
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Use a modal preview in a narrow dock
      Given the right dock body that hosts the view is narrower than 480 pixels
      When the Dev Server view renders
      Then the inline preview is replaced by an "Open preview" launcher that opens the preview in a modal
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Restore the typed command after a remount
      Given the operator typed a custom command and selected a script
      When the Dev Server view unmounts and mounts again for the same project
      Then the typed command and the selected script are restored
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Poll only while the server runs
      Given a running dev server
      When the status poll runs
      Then the status is fetched every 3 seconds
      And no poll happens while the server is stopped
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Reject command substitution
      Given a dev-server command of "echo $(whoami)"
      When the operator starts the dev server
      Then the start is refused and no child process is spawned
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Terminate the process tree on stop
      Given a running dev server
      When the operator stops it
      Then a termination signal is sent to the child's process group
    ```

    ```gherkin
    @NFR-2
    Scenario: Stop the servers on dashboard shutdown
      Given a running dev server
      When the dashboard HTTP server closes
      Then the dev server is stopped and cleaned up
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Clear the probe timer on stop
      Given a running dev server with a pending fallback probe timer
      When the operator stops it
      Then no pending probe timer remains
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Release the heartbeat on disconnect
      Given a client subscribed to the log stream
      When the client disconnects
      Then the heartbeat interval is cleared
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Recover a stale persisted process id
      Given a persisted state with status "running" and a process id that is no longer alive
      When the store is loaded
      Then the status becomes "stopped" with exit code 1
      And a recovery line is appended to the log history
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Ignore late output from the previous run
      Given a dev server that was restarted
      When output from the previous process arrives afterwards
      Then the current run's state and logs are not modified
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Never suggest the reserved port
      Given a dev server that prints "listening on port 4040"
      When the line is parsed
      Then no preview URL is detected for that port
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Bound the log history
      Given a dev server that has produced more than 500 log lines
      When the lines are appended
      Then only the last 500 lines are retained
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: Probe ports in a fixed order
      Given two common local ports are open
      When the fallback probe runs
      Then the earlier port in the fixed list is reported
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: Record the lifecycle in the persisted state
      Given a dev server that was started and later stopped
      When the persisted state is read
      Then it carries the start timestamp, the stop timestamp, and the exit code
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: Fall back on a corrupt state file
      Given a .fusion/dev-server.json file that is not valid JSON
      When the store is loaded
      Then the state and the configuration fall back to their defaults
    ```

- [ ] **NFR-12**

    ```gherkin
    @NFR-12
    Scenario: Keep the canonical family on the runtime path
      Given the dashboard API route registrars
      When the import graph is inspected
      Then the dev-server routes resolve only to the dev-server-* module family
    ```

## Conflicts

None identified yet.

## Open Questions

1. The dashboard client calls `/api/devserver/*` session endpoints first and falls back to `/api/dev-server/*`, but no `/api/devserver` router is registered in the backend, so the fallback is always taken. The intended owner of the session endpoint family is unresolved.
2. The client also requests `/api/dev-server/candidates` and `/api/dev-server/logs/history`, which the canonical router does not serve, so the client falls back to `/detect` and to the status response.
3. The disconnected `devserver-*` family and the `dev-server-manager.ts` wrapper both carry capabilities the canonical path lacks (event buffering with replay, stale process id recovery). Whether those are ported or dropped is undecided.
4. The Dev Server view hard-codes its manual-override flag to false, so the preview badge always reads "Auto" even after the operator saves a manual override that the backend does store. Whether the badge should read the backend's manual override is undecided.
