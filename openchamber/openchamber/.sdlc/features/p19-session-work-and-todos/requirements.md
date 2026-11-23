---
title: "Session work and todos"
status: done
---

# Requirements: Session work and todos

## Overview

Sessions carry a server-owned work state and a server-owned todo list.
The work state records whether a session is open or done, what opened it, and whether Jev suggested that it is finished.
The todo list comes from the agent's `todowrite` calls and appears in the chat work status panel.
The server owns the state and its synchronization, while every UI runtime reads the same contracts.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | See what the agent is doing and what remains without scanning the transcript. |
| In work users | Keep sessions they are working on grouped until they mark them done. |
| Agent authors | Get a stable todo list that survives transcript truncation and client eviction. |
| VS Code users | Track and finish work by hand through the extension's metadata bridge. |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall store work state in `metadata.openchamber.work` with `state`, `openedAt`, `openedBy`, `doneAt` and `suggestDoneAt`, and read missing or malformed records as none. |
| FR-2 | Must | The system shall open an eligible session on a sent user message or a user shell command with `openedBy: auto`, and handle each message id once without asking Jev. |
| FR-3 | Must | The system shall limit work to top-level, unarchived project sessions outside chat roots, review sessions, side questions, scheduled runs and pinned sessions. |
| FR-4 | Must | The system shall reopen a done session only for a message created after `doneAt`, and a user's Track or Done shall decide the final state. |
| FR-5 | Must | The system shall send one turn-end Jev request containing only the applicable signs, review and recap questions, and return an assist gate from the answers. |
| FR-6 | Must | The system shall write a done hint only after ten quiet minutes, only for the current turn, and shall retire the hint when the user continues. |
| FR-7 | Must | The system shall offer a review without requiring a session in work, write that offer at once, and retire it on the next turn. |
| FR-8 | Must | The system shall suppress done hints and next-step suggestions while the agent waits on its own background work, and shall leave state unchanged when Jev fails. |
| FR-9 | Must | The system shall read `sessionWorkEnabled` and `sessionReviewOfferEnabled` at every use, and VS Code shall keep only manual track and done. |
| FR-10 | Must | The system shall retry a failed open at two, ten and sixty seconds, wait for an archived session to be restored, and clear pending work on stop. |
| FR-11 | Must | The system shall keep a validated, bounded per-session todo list from `todowrite` calls and persist it atomically in `session-todos.json`. |
| FR-12 | Must | The system shall resolve OpenCode's `todo` flag from `OPENCODE_FLAGS`, config documents, `all_flags`, a seen call and the build version in that order. |
| FR-13 | Must | The system shall expose `GET /api/session-todos/:sessionId` with a required directory, return `off` or `ready` with a revision, and answer 502 when OpenCode fails. |
| FR-14 | Must | The system shall follow tool calls from input start to success, handle reverts, deletions, config changes and reconnects, and broadcast `openchamber:session-todos` events. |
| FR-15 | Must | The system shall read todo history lazily in pages of fifty assistant messages, stop at `checkedThrough` or a revert boundary, and discard a walk overtaken by an event. |
| FR-16 | Must | The UI shall load each session's todos once, share in-flight loads, order commits by revision, retry failures with capped backoff and reset on runtime switch. |
| FR-17 | Must | The UI shall apply `openchamber:session-todos` events from the current runtime and reload affected entries when the event carries no todos. |
| FR-18 | Must | The work status Tasks section shall list ready todos, hide cancelled items, rank active work first while keeping the agent's order, and show a done count. |
| FR-19 | Must | The UI shall keep live tool calls and context readings per session from stream events, extract named file paths and clear stale calls on new turns and idle. |
| FR-20 | Must | The system shall answer `off` and read no history for isolated spaces and directories where the tool is off. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | A failed metadata read, Jev call, session read or write shall leave work state unchanged and return an unknown assist gate. |
| NFR-2 | Must | Performance | History reads shall be lazy and serial per session, and live work maps and event buffers shall stay bounded. |
| NFR-3 | Must | Security | External metadata, events, flags and route inputs shall be parsed with Zod, and directory headers shall be percent-encoded. |
| NFR-4 | Should | Availability | An OpenCode stream reconnect or server restart shall invalidate affected lists and trigger one fresh read without losing unrelated entries. |
| NFR-5 | Should | Usability | The Tasks section shall appear only for a ready list and shall update from events without refetching the transcript. |

## Constraints

- OpenChamber has no persistent database, so work lives in session metadata and todos live in a JSON file under the data directory.
- OpenCode v2 takes the directory in the `x-opencode-directory` header and rejects non-ASCII header values.
- The work status panel is shared by web, desktop, hosted mobile, Capacitor mobile and VS Code.
- VS Code has no OpenChamber server and no session todos route.
- Jev wording and thresholds came from a measurement of 881 turns and change only with a new measurement.
- The done hint waits in the current process, so a server restart drops a pending hint.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Read a work record
      Given session metadata holds an open work record with openedAt and openedBy
      When the state module reads it
      Then it returns the parsed record with state open
      And a missing or malformed record reads as none
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Open work on a sent message
      Given an eligible session that is not in work
      When the user sends a user message or starts a shell command
      Then metadata.openchamber.work becomes open with openedBy auto
      And Jev receives no request
      And a repeat of the same message id changes nothing
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Refuse ineligible sessions
      Given a session that is a child, archived, pinned, a chat, a review, a side question or a scheduled run
      When the user sends a message in it
      Then the runtime writes no work record
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Reopen work after a user closed it
      Given a done session whose doneAt is 40 and a message created at 50
      When the runtime handles the message
      Then the session is open again
      And a message created before doneAt leaves it done
      And a user's Done keeps openedAt and clears the suggestion
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Ask one combined turn-end question set
      Given a turn in a session in work with recap enabled and the review offer on
      When session assist calls evaluateTurnEnd
      Then Jev receives one request with the four done signs, review_ready and recap
      And the assist gate follows the measured thresholds
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Hint that work looks done
      Given Jev answered all four done signs in favour of finishing and the user stayed quiet for ten minutes
      When the hint timer fires
      Then suggestDoneAt is written on the open work record
      And a new message or turn before the timer cancels it
      And an answer from an older turn writes nothing
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Offer a review
      Given the review offer is on and the turn reports project changes at a score of 0.7 or higher
      When Jev answers
      Then reviewOffer.at is written at once even when the session is out of work
      And the next turn removes it
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Wait on the agent's own work
      Given a subagent, image, working child or fresh shell is still running for this turn
      When Jev says the work looks done and wants a next step
      Then no done hint is scheduled
      And the next-step suggestion is false
      And a failed Jev call leaves metadata unchanged
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Apply settings at use time
      Given sessionWorkEnabled was turned off after a session opened
      When the user sends another message in that session
      Then no open is attempted
      And VS Code still accepts manual Track and Done through its metadata bridge
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Recover a failed open
      Given a metadata read fails once for a sent message
      When the runtime retries after two seconds
      Then the session opens
      And a session OpenCode no longer has is not retried
      And stop clears every pending timer
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Keep a bounded validated todo list
      Given a completed todowrite call with two hundred todos and one empty item
      When the runtime processes the success event
      Then the stored list holds the two hundred valid todos in order
      And an unknown status becomes pending
      And the file write uses a temporary file and rename
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Resolve the todo flag
      Given config documents where the highest one setting experimental has all_flags true and no todo key
      When the flag is resolved for a directory
      Then the tool counts as on
      And OPENCODE_FLAGS of -todo turns it off
      And a seen todowrite call turns it on for that directory
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Read todos over HTTP
      Given a valid session id and a directory of /repo
      When the client requests the todos route
      Then the response carries a revision and either off or ready with todos
      And a missing or blank directory returns 400
      And a failed OpenCode request returns 502 with OpenCode did not answer
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Follow a todowrite call
      Given a tool input start event for todowrite followed by a success event with metadata todos
      When the runtime processes both events
      Then the session list is replaced and an event with the new revision is broadcast
      And a revert invalidates the list and announces null todos
      And a config change or reconnect announces a null session or null directory
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Walk history lazily
      Given a session whose newest agent message has no completed todowrite call
      When the route first reads it
      Then the runtime pages backwards in batches of fifty assistant messages
      And it stops at checkedThrough or before a revert boundary
      And an event that arrives during the walk wins over its result
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Load todos in the UI
      Given the Tasks section is shown for a session and directory
      When the loader runs twice before the first request resolves
      Then one request is shared
      And a later event with a lower revision is ignored
      And a failed load retries after two seconds with a cap of thirty seconds
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Apply an event from the current runtime
      Given the UI is subscribed to openchamber:session-todos events
      When an event carries sessionId null and directory null
      Then every loaded entry is read again
      And events from a runtime that is no longer current are ignored
      And VS Code installs no subscription
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Show the Tasks section
      Given a ready list with one in_progress, one pending, one completed and one cancelled todo
      When the work status panel renders the Tasks section
      Then cancelled items are absent
      And in_progress leads and the other states keep the agent's order
      And the header shows one out of three
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Track live tool calls and context
      Given a tool part becomes pending, streams a path in its input and succeeds
      When the live work events are applied
      Then the running call carries the path and becomes the last call
      And a new user message, idle status, reconnect or deletion clears stale calls
      And a completed compaction marks the context as compacted
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Answer off without reading history
      Given a session in an isolated space or in a directory where the tool is off
      When the client reads its todos
      Then the response is off with a revision
      And no OpenCode history request is made
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Keep state stable on failure
      Given Jev times out during a turn-end check
      When the check returns
      Then no metadata patch is written
      And the assist gate is unknown
      And other sessions keep their state
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Bound background work
      Given two thousand sessions with live work state and a session with no todo call in its history
      When events arrive and the list is read
      Then the oldest live work entries are evicted
      And the history walk runs once for that session
      And at most one walk runs per session
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Validate external input
      Given a route query with a blank directory and an event with an invalid session id
      When the route and event parser run
      Then the route answers 400
      And the event is dropped
      And a non-ASCII directory is sent as an encoded header value
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Recover from a stream gap
      Given OpenCode reconnects after a missed todowrite call and revert
      When the runtime handles the connect status
      Then verified lists become unchecked
      And clients are told to read again
      And the next read walks back to checkedThrough
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Update Tasks without a transcript refetch
      Given a session with a ready todo list and an open work status panel
      When a new list arrives on the event stream
      Then the Tasks section updates from the store
      And the transcript stores receive no new request
    ```

## Conflicts

None identified.

## Open Questions

1. None. The reverse-engineered behavior is taken from the implemented modules and their documentation.
