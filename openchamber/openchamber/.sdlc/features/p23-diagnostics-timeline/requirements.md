---
title: "Diagnostics timeline"
status: done
---

# Requirements: Diagnostics timeline

## Overview

The server captures performance and lifecycle diagnostics in a fixed vocabulary and the UI renders them as a timeline.
A user or developer opens the timeline from a shortcut, a command palette item, or a failed-turn link, then copies or downloads a log for a bug report.
The export combines renderer state changes, server journal events, classified local log lines, OpenCode load counts, health samples, and API probes.
The log is an operator and developer tool, not an analytics platform, and it must not carry session identifiers, paths, prompts, raw log lines, or response bodies.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users reporting a problem | Attach one self-contained log that explains where time went during session work |
| Developers and maintainers | Diagnose startup failures, health failures, API failures, and renderer errors from a shared timeline |
| Support triagers | Compare coverage and failure bursts across web, desktop, and remote runtimes without reading private logs |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The UI shall open a dialog with the generated timeline log from Ctrl/Cmd+Shift+L, the "Show diagnostic timeline" command palette item, and the link under a failed turn. |
| FR-2 | Must | The UI shall capture local renderer state changes, resource errors, uncaught exceptions, unhandled rejections, CSP violations, and vetted console calls into an in-memory buffer. |
| FR-3 | Must | The UI shall replace session, directory, and message identifiers with local sequential labels such as `session-1` and `directory-2`. |
| FR-4 | Must | The server shall keep a process-local journal of fixed lifecycle actions and completed 4xx and 5xx HTTP responses with route templates instead of request paths. |
| FR-5 | Must | The server shall map known local log lines to fixed categories and exclude unrecognized lines from the timeline. |
| FR-6 | Must | The server shall report OpenCode load as loaded-directory count and process-tree counts with memory in megabytes, with no paths, process names, or commands. |
| FR-7 | Must | The UI shall re-validate every server-supplied event and coverage record against the fixed vocabulary and count rejected records under `Sources`. |
| FR-8 | Must | The export shall build one log containing an environment header, a current health summary, an OpenCode load line, source coverage, and all events sorted by time. |
| FR-9 | Must | The server shall serve local diagnostics only to a loopback socket with local tunnel scope after UI auth, and refuse tunnel and private-relay forwarded requests. |
| FR-10 | Must | A remote-runtime export shall read only the remote health endpoint and the remote OpenCode probes, and shall skip local files, the journal, SSH history, and the renderer buffer. |
| FR-11 | Must | An export shall be replaced by an "Export interrupted" log when the active runtime changes while it is collected. |
| FR-12 | Must | The dialog shall offer copy and download of the log as a `.log` file, and the OpenCode heap snapshot shall stay a separate file outside the log. |
| FR-13 | Should | The system shall group adjacent repeated HTTP failures and upstream stream failures into bounded bursts with a count and span in milliseconds. |
| FR-14 | Should | The server shall support opt-in startup phase diagnostics with approved phase names and allowlisted numeric or enumerated metadata. |
| FR-15 | Should | The desktop shell shall classify SSH manager history in the Electron main process and join it into the local export. |
| FR-16 | May | The UI shall expose opt-in sync performance counters for developer inspection without adding them to the export. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The export shall contain no session or message IDs, titles, paths, URLs, prompts, raw log lines, console arguments, stacks, stderr, or response bodies. |
| NFR-2 | Must | Performance | Diagnostic buffers shall be bounded to 1,500 renderer events or 24 hours, 4,000 server journal events or 24 hours, 512 KB and 4,000 lines per local file, and 8,000 collected file or SSH events. |
| NFR-3 | Must | Reliability | A failed, filtered, truncated, or unavailable source shall be reported in `Sources` and shall never look like an empty successful read. |
| NFR-4 | Must | Performance | Diagnostic network operations shall use timeouts of 5 seconds for health, 6 seconds for probes, 8 seconds for local transport, and 4 seconds for OpenCode requests and the process listing. |
| NFR-5 | Must | Portability | Local and remote collection rules shall hold in web, desktop, VS Code, hosted mobile, and Capacitor runtimes, and the dialog link shall be hidden where the dialog is not mounted. |
| NFR-6 | Should | Compatibility | Timestamps without a timezone, including bracketed Electron timestamps, shall be treated as local wall time so export formatting does not shift them. |
| NFR-7 | Should | Performance | Server health shall be sampled at startup, on runtime switch, and on export, with no polling loop. |
| NFR-8 | Must | Security | Console wrapping shall run only in production builds so development builds keep the original console call sites. |

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Open the timeline from each entry point
      Given the shared status dialog is mounted in the main layout
      When the user presses Ctrl/Cmd+Shift+L, selects "Show diagnostic timeline", or clicks the link under a failed turn
      Then OpenCodeStatusDialog shows the text produced by buildDiagnosticLog
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Record local renderer diagnostics
      Given a local runtime with diagnostic capture started from App
      When connection state changes, a selection changes, an uncaught exception fires, a rejection is unhandled, or a tagged console call occurs
      Then the timeline buffer holds a timestamped event with an allowlisted source and action
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Correlate selections without exporting identifiers
      Given a session id, directory path, and message id exist only in memory
      When they appear in a snapshot, a selection change, a turn error, or a rejected send
      Then the export shows only sequential labels and the same original value maps to the same label in that scope
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Journal lifecycle and failed responses
      Given the server journal is empty
      When OpenCode launches and a client receives 120 failed requests to session-specific paths
      Then the snapshot holds fixed lifecycle actions and one HTTP event with a route template, a count, and a span, with no private path or id
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Classify known log lines
      Given application logs contain known startup, lifecycle, updater, relay, IPC, proxy, and access-failure messages
      When the collector classifies each line
      Then each recognized line becomes a fixed category and each unrecognized line is counted under `Sources` without being copied
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Report OpenCode load
      Given OpenCode reports a pid and exposes loaded locations, and one `ps` call returns a process tree
      When the load route is read
      Then the result holds only a loaded-directory count and megabyte totals, and an unknown count is `null` rather than zero
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Reject unsafe transport records
      Given an IPC or HTTP response carries valid and fabricated events side by side
      When `parseFileDiagnostics` validates the response
      Then valid events remain, invalid records are dropped one by one, and a "diagnostic transport" coverage entry lists the omitted count
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Build the timeline log
      Given health, probes, load, coverage, and events from several sources are available
      When the export is built
      Then the log has the environment header, `Current health`, `OpenCode load`, `Sources`, and an `Events` section ordered by timestamp
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Refuse non-local diagnostics reads
      Given a request reaches a diagnostics route through a tunnel or the private relay
      When the route checks the socket and tunnel scope after UI auth
      Then no local file, journal, or SSH data is returned
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Export from a remote runtime
      Given the active runtime points to a server on another machine
      When the user exports the timeline
      Then only remote health history and the three OpenCode probes appear, and `Sources` states that local files, journal, SSH manager, renderer buffer, turn errors, and rejected sends were skipped
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Runtime changes during collection
      Given an export has started collecting health and probes
      When the active runtime key changes before collection finishes
      Then the log says "Export interrupted: the active runtime changed while it was collected; export again" and contains no health section
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Deliver the log without the heap snapshot
      Given the dialog holds generated log text
      When the user clicks copy or download
      Then the clipboard or a timestamped `.log` file receives that text, and a heap snapshot remains on the OpenCode machine outside the log
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Group repeated failures
      Given 120 identical failed access lines occur within ten minutes and an identical line occurs eleven minutes later
      When the collector reads the file
      Then one event carries `count=120` and `spanMs`, the later line forms a separate event, and the burst count is capped at 4,000
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Record opt-in startup phases
      Given `OPENCHAMBER_STARTUP_PERF` is unset
      When `recordStartupPerformance` is called
      Then nothing is logged, and when it is set to `1` only approved phases with finite non-negative durations and enum metadata are logged
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Join desktop SSH history
      Given the Electron main process holds classified SSH buffer lines and a current phase
      When the desktop collection IPC runs
      Then the export contains phase and action events labeled `SSH connection 1` and no host names, remote stderr, passwords, or commands
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Inspect sync counters on demand
      Given sync performance diagnostics are disabled by default
      When a developer enables them and calls `window.__openchamberSyncPerformance.getSnapshot()`
      Then a copy of the zeroed counter object is returned, `reset()` zeroes it again, and disabling it makes the global return `null`
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: No private data in the export
      Given logs, health bodies, console arguments, and error messages contain tokens, paths, session ids, and stderr
      When the timeline is captured, classified, re-validated, and formatted
      Then no value from that private data appears in the exported text
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Bounded memory under sustained diagnostics
      Given 1,600 renderer events, 9,000 failed responses, and 8,001 SSH lines are produced
      When each buffer is read
      Then the renderer keeps 1,500 events, the journal reports truncation with an omitted count, and the SSH snapshot keeps the newest 8,000 events
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Distinguish missing, filtered, and unavailable sources
      Given one log directory is absent, one file contains only unclassified text, and one read throws
      When coverage is collected
      Then the entries report `missing`, `filtered`, and `unavailable` respectively, with filtered and omitted counts where they apply
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Diagnostic requests time out
      Given a health request, a probe, a local-file read, and a process listing never respond
      When collection runs
      Then each call is aborted at its configured limit and the export records `health probe failed` or a `probe failed` event instead of hanging
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Runtime-appropriate availability
      Given VS Code, hosted mobile, and Capacitor roots do not mount MainLayout
      When `SessionErrorNotice` reads `DiagnosticDialogAvailableContext`
      Then it hides the status link in those runtimes while web and desktop retain the dialog and its local or remote collection path
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Preserve local wall time
      Given a bracketed Electron timestamp with no timezone and an ISO timestamp with a timezone appear in one log
      When lines are classified and events are formatted
      Then both retain their parsed instant and the ISO event line reflects the same wall-clock reading used by the source
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: No health polling
      Given diagnostic capture is active and no export has been requested
      When a developer inspects the renderer buffer over a period of time
      Then health probe events appear only for the startup snapshot, a runtime switch, or an export
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Leave the development console untouched
      Given a Vite development build starts capture with console capture off
      When `console.warn` is called
      Then the original function receives the call and no `console.warn` diagnostic event is recorded
    ```

## Conflicts

None identified yet.

## Open Questions

None.
