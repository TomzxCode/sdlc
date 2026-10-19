---
title: "Session Hibernation"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Session Hibernation

## Overview

An open terminal is not evidence of active work, so a long-idle session keeps memory resident that nothing will read.
Session hibernation frees that memory without closing the terminal, without losing the input draft, and without interrupting a tool, an agent turn, or a scheduled wake.
The daemon reclaims lazy reproducible caches for idle sessions, and the terminal client reclaims its derived render caches and its retained heap.
The canonical transcript stays live on both sides, so waking is transparent: the next interaction restores the session.
Three hibernation depths are offered, from dropping rebuildable caches to exiting the client process entirely.
This feature documents already-implemented functionality that was reverse-engineered from the existing codebase during an SDLC sync.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Terminal user | Memory that is freed while the session is idle, without a visible loss of the session |
| Terminal user | A wake that is invisible, so the first typed character is not swallowed |
| Operator | A daemon that does not hold provider caches for sessions nobody is using |
| Operator | Measured memory release rather than an estimated one |
| Maintainer | A boundary that keeps authoritative state resident and only discards derived state |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall release reloadable memory for a session that has had no work and no interaction for the configured idle period, and shall treat an idle period of `0` as hibernation disabled. |
| FR-2 | Must | The system shall read the idle period and the hibernation depth from the `[session]` configuration table, using the key `hibernation_idle_secs` for the period and `hibernation_mode` for the depth. |
| FR-3 | Must | The daemon shall sweep idle sessions on a 10 second interval and shall reclaim only lazy reproducible caches, namely the provider message cache and the reconstructible tool output indexes. |
| FR-4 | Must | The daemon shall refuse to hibernate a session that has an active turn, pending input, a queued alert or soft interrupt, an in-flight compaction, an in-flight tool, or a migration lease. |
| FR-5 | Must | The daemon shall reset the idle window of a session it declines to hibernate because work is pending, and shall re-arm the idle window when a turn starts and finishes entirely between two sweeps. |
| FR-6 | Must | The daemon shall keep the canonical transcript live across hibernation, retaining the original messages, the frozen tool definitions, the captured instructions, the rewind undo snapshot, and the provider session handle. |
| FR-7 | Must | The daemon shall purge retained heap once per sweep, after releasing every session lock, and shall record the released session ids, the released provider cache bytes, the released tool index entries, and the before and after resident memory. |
| FR-8 | Must | The terminal client shall release its derived render caches, namely the prepared transcript and body frames, the rendered message lines, the syntax highlighting cache, the copy viewport snapshot, the derived side panel, diff and image state, the incremental markdown renderer, and the local provider message cache. |
| FR-9 | Must | The terminal client shall retain the authoritative source data across hibernation, keeping the input draft, the cursor position, the scroll offset, the scroll lock state, the attachments, the pasted contents, and the local-only display messages. |
| FR-10 | Must | The terminal client shall keep a bounded copy of the last completed terminal frame, and shall refuse to freeze a frame that is missing or that exceeds the cell or symbol bounds. |
| FR-11 | Must | The terminal client shall measure its own memory before and after the release and shall report the measured change in the hibernation notice, showing an increase as an increase and an unchanged reading as unchanged. |
| FR-12 | Must | The next interaction shall wake the session transparently, processing the waking event normally including its first character, and leaving the draft, the cursor, the scroll position and the session state untouched by the wake. |
| FR-13 | Must | The terminal client shall re-check every queued and active work guard at the moment of eviction, and shall not evict anything when work has arrived since the idle timer was scheduled. |
| FR-14 | Must | The terminal client shall not wake on presence traffic, on acknowledgments, or on read-only debug queries, and shall wake on any event that may change the conversation content or start active work. |
| FR-15 | Must | The terminal client shall trim its retained heap with a per-client growth budget of 16 MiB, an idle trim after 60 seconds of quiet, and a re-trim cadence of 300 seconds while the client stays idle. |
| FR-16 | Should | The system shall offer three hibernation depths selected by `hibernation_mode`, namely `caches` for rebuildable render caches only, `transcript` for the in-memory transcript as well, and `exit` for the client process, with `caches` as the default. |
| FR-17 | Should | In `transcript` mode the terminal client shall drop the in-memory transcript, clear the remote side pane images, and mark the history as needing a reload so that it is refetched from the server on wake. |
| FR-18 | Should | In `exit` mode an idle remote client shall re-exec the process into a tiny waiter that resumes the session on the next key press. |
| FR-19 | Should | The system shall expose a read-only debug query that returns the hibernation state, the scope, the measured memory readings, the hibernation and wake counts and the last wake reason, and a debug command that requests an immediate hibernation. |
| FR-20 | May | The `JCODE_HIBERNATION_IDLE_SECS` and `JCODE_HIBERNATION_MODE` environment variables shall override the corresponding file configuration values, and an invalid override shall leave the file value in place. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Resource | The released memory shall be measured, not estimated. A flat or unavailable reading shall never be displayed as a positive saving. |
| NFR-2 | Must | Availability | The wake shall be transparent. Rebuilding a released cache shall not invoke resume hooks, shall not cancel work, and shall not append a new environment snapshot. |
| NFR-3 | Must | Reliability | Hibernation shall not write the session file, and no disk-backed authoritative state shall be dropped on the strength of a queued save or of a save skipped because of a migration lease. |
| NFR-4 | Must | Performance | The idle detection cost shall be bounded. The daemon shall sweep on a fixed 10 second interval, and the client shall poll on its existing tick, so no extra thread or timer is created per session. |
| NFR-5 | Must | Resource | The frozen terminal frame shall be bounded to 128 thousand cells and 8 MiB of symbol bytes, and the per-client retained heap growth budget shall be capped at 16 MiB even when the global threshold is larger. |
| NFR-6 | Must | Availability | Hibernation shall not discard or cancel active work, pending input, or a scheduled wake. |
| NFR-7 | Should | Availability | The session shall survive hibernation with its identity, model settings, draft, transcript and scroll state intact. |
| NFR-8 | Should | Performance | Repeated idle ticks shall not repeatedly rebuild and discard the same caches. |
| NFR-9 | Should | Compatibility | A configuration file without a `[session]` table shall inherit the default idle period of 30 minutes and the default mode of `caches`, and the settings shall round-trip through the configuration file. |
| NFR-10 | Should | Resource | The exit-mode waiter shall hold only a few hundred KiB of private memory while it waits, and shall resume the session in about one second. |
| NFR-11 | Should | Observability | The daemon shall record the hibernation outcome in its log, and the client shall record the wake reason and the measured change, so an operator can tell an idle release from a failed one. |

## Constraints

- The idle period and the mode are read from the `[session]` table of the jcode configuration file.
- The daemon sweep reclaims derived caches only. The canonical transcript, the frozen prompts and tools, the rewind undo state, the provider handle and the hook state stay resident.
- Reloading a session from disk is not a wake operation, and is not used as one.
- The client keeps a bounded copy of the last frame instead of repainting the transcript into new caches on every idle tick.
- The daemon measures its own process separately from the client, and the client measurement is not attributed to the daemon or to other sessions.
- Hibernation is not process suspension, and it does not promise a near-zero-memory session.
- The exit mode applies to a remote client, because the daemon owns the session that the waiter resumes.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).
Write each criterion as a fenced `gherkin` block with a tag matching its requirement ID, so the criteria are parseable and later executable via BDD tooling (pytest-bdd, cucumber).
Multiple scenarios per requirement are allowed; tag each with the requirement ID.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: An idle session releases its reloadable memory
      Given a session whose configured idle period has elapsed without work or interaction
      When the idle sweep runs
      Then the session releases its reloadable memory
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: The idle period and the mode come from the session configuration table
      Given a configuration file with "[session]" holding an idle period and a mode
      When the daemon and the client read their idle policy
      Then both read the same idle period and the same mode from the session table
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The daemon sweep reclaims only reproducible caches
      Given an idle session with a populated provider message cache and tool output indexes
      When the daemon sweep runs
      Then the provider message cache and the tool output indexes are released
      And the original messages are still resident
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A session with pending work is not hibernated
      Given an idle session with a queued alert, an in-flight compaction or an in-flight tool
      When the daemon sweep runs
      Then the session keeps its provider message cache
      And the sweep reports that no release happened for that session
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The idle window is reset when work is pending
      Given a session that was declined for hibernation because work was pending
      When the work settles and the sweep runs again before the original idle period elapses
      Then the session is not hibernated yet
    ```

    ```gherkin
    @FR-5
    Scenario: A turn that starts and finishes between two sweeps is detected
      Given a session whose turn started and finished between two sweeps
      When the next sweep runs
      Then the idle window is re-armed from the moment the turn finished
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: The canonical transcript survives hibernation
      Given an idle session with frozen tool definitions, captured instructions, a rewind undo snapshot and a provider session handle
      When the daemon hibernates the session
      Then the messages, the frozen tools, the captured instructions, the undo snapshot and the provider handle are unchanged
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: One sweep purges retained heap once and records the outcome
      Given two idle sessions that are both released in the same sweep
      When the sweep completes
      Then the retained heap purge runs once after the session locks are released
      And the log records both session ids, the released cache bytes, the released tool index entries and the before and after resident memory
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: The client releases its derived render caches
      Given an idle terminal client with prepared frames, rendered message lines and a populated local provider message cache
      When the client hibernates
      Then the prepared frames, the rendered message lines, the highlighting cache, the copy viewport, the derived side panel, diff and image state, the incremental markdown renderer and the local provider message cache are released
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: The draft, the cursor and the scroll state survive hibernation
      Given an idle terminal client with a draft, a cursor position, a scroll offset, an attachment and a pasted content
      When the client hibernates
      Then the draft, the cursor, the scroll offset, the attachment and the pasted content are unchanged
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A frame that is too large to freeze is refused
      Given an idle terminal client whose last frame exceeds the cell or the symbol bound
      When the client hibernates
      Then no frame is frozen
      And the client does not retry the oversized frame on every idle tick
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The notice reports the measured change
      Given an idle terminal client that measured a lower private memory after the release
      When the hibernation notice is rendered
      Then the notice shows the measured decrease and the resulting private memory
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: The first typed character wakes the session and is not swallowed
      Given a hibernated terminal client with a draft and a cursor position
      When the user types one character
      Then the client is awake
      And the character is appended to the draft at the original cursor position
      And the scroll position is unchanged
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Work that arrives after the timer prevents the eviction
      Given an idle terminal client whose idle timer already elapsed
      When work is queued before the paint happens
      Then nothing is evicted
      And the client stays awake
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Presence traffic does not wake the client
      Given a hibernated terminal client
      When a heartbeat acknowledgment and a read-only debug query arrive
      Then the client stays hibernated
      And the wake count does not change
    ```

    ```gherkin
    @FR-14
    Scenario: A conversation event wakes the client
      Given a hibernated terminal client
      When a text delta arrives from the server
      Then the client is awake
      And the wake count increased by one
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: The client trims its retained heap while it stays idle
      Given a terminal client that has been quiet for longer than the idle trim delay
      When the periodic tick runs
      Then the client trims its retained heap against the per-client budget
      And it trims again on the re-trim cadence while the client stays idle
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: The mode selects the hibernation depth
      Given a configuration file that sets no mode
      When the hibernation policy is resolved
      Then the depth is the caches mode
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: The transcript mode refetches the history on wake
      Given a remote terminal client in the transcript mode that hibernated
      When the client wakes
      Then the history is marked as needing a reload
      And the in-memory transcript was released at hibernation time
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: The exit mode re-execs into a waiter and resumes on the next key press
      Given an idle remote terminal client in the exit mode
      When the client hibernates
      Then the client process is replaced by a waiter that holds the session id
      And the first byte of input resumes the session from the daemon
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: The debug query reports the state without changing it
      Given a hibernated terminal client
      When the read-only debug query runs
      Then it returns the state, the scope, the measured readings, the hibernation and wake counts and the last wake reason
      And the client stays hibernated
    ```

    ```gherkin
    @FR-19
    Scenario: The debug command hibernates immediately
      Given an idle terminal client with no queued work
      When the debug hibernation command runs
      Then the client hibernates without waiting for the idle period
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: The environment override replaces the file value
      Given a configuration file that sets an idle period
      When the environment sets a different idle period
      Then the environment value wins
      And an invalid environment value leaves the file value in place
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: An unchanged or unavailable reading is not shown as a saving
      Given a client whose memory reading did not change or could not be taken
      When the hibernation notice is rendered
      Then the notice shows an unchanged or unavailable reading
      And it does not claim a positive saving
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Waking rebuilds caches without resume side effects
      Given a hibernated session whose caches were released
      When the next turn runs
      Then the provider receives the retained tool pairs
      And no resume hook ran and no new environment snapshot was appended
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Hibernation does not write the session file
      Given a session file saved before hibernation
      When the session is hibernated
      Then the session file bytes and its modification time are unchanged
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Idle detection uses a fixed cadence
      Given a running daemon with connected sessions
      When the daemon idles
      Then the sweep runs on a fixed 10 second interval
      And no extra thread or timer is created per session
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The frozen frame and the client budget stay bounded
      Given a terminal frame with more cells than the bound or with more symbol bytes than the bound
      When the client considers freezing it
      Then the frame is refused
    ```

    ```gherkin
    @NFR-5
    Scenario: The per-client budget caps the global threshold
      Given a global retained heap threshold of 64 MiB
      When the client resolves its own growth budget
      Then the client budget is 16 MiB
      And a lower global threshold is honored and a disabled threshold stays disabled
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Active work is never discarded
      Given a session with a running turn and a tool in flight
      When the idle sweep runs
      Then the turn and the tool are not cancelled
      And the session caches are untouched
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: The session identity and the local transcript survive hibernation
      Given a client with a session id, stored source messages and local-only display messages
      When the client hibernates
      Then the session id, the stored source messages and the local-only display messages are unchanged
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Repeated idle ticks do not rebuild the caches
      Given a hibernated client that is repainted several times
      When the renderer draws the frozen frame again
      Then the prepared frame caches stay released
      And they are rebuilt only after the client wakes
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: A configuration file without a session table inherits the defaults
      Given a configuration file with no session table
      When the configuration is parsed
      Then the idle period is 30 minutes and the mode is the caches mode
      And the settings round-trip through the file unchanged
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: The waiter is small and resumes quickly
      Given a client that hibernated in the exit mode
      When the waiter waits for a key press
      Then the waiter holds only a few hundred KiB of private memory
      And the session resumes in about one second
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: The outcome of a release is recorded
      Given an idle session that was released by the daemon
      When the sweep completes
      Then the log records the release with its session id and its measured memory change
      And a client wake records its reason
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified yet.

## Open Questions

1. The exit mode applies only to a remote client today, because the daemon must own the session that the waiter resumes. Should a local client be able to exit into a waiter as well?
2. The daemon sweep reads the idle period from the configuration on every tick, so a configuration change takes effect within 10 seconds. Should the daemon log a notice when the period changes under it?
3. The transcript mode drops local-only display messages and the exact scroll position, and reloads the history from the server on wake. Should that mode be deprecated in favour of the caches mode?
