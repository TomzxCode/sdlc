---
title: "Session drafts and warming"
status: done
---

# Requirements: Session drafts and warming

## Overview

The server keeps unsent session input as drafts so a draft started in one client opens in another with its text, mentions, target folder, lead flag, and attachments.
The server also keeps the provider prompt cache of sessions the user picked warm by sending OpenCode keep-alive requests while those sessions sit idle.
The shared UI shows drafts in the sidebar and shows each session's warm state, and it syncs both from server-owned state.
This feature was reverse-engineered from the shipped code and tests.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Chat users | Return to unsent input after a restart or a switch of device |
| Mobile users | Open a draft written on the desktop with its attachments |
| Users of long sessions | Start agent work again without rebuilding the provider prompt cache |
| Operators | Keep warm requests limited to chosen sessions and a chosen duration |
| Maintainers | Keep draft bytes and warming state in the server's data directory with defined limits |
| Isolated-space users | Know that sessions in a space cannot be kept warm by this server |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall persist the draft list in `session-drafts.json` under the OpenChamber data directory, return every draft from `GET /api/session-drafts`, and answer 500 when the stored file does not parse as a store. |
| FR-2 | Must | The system shall create or replace a draft through `PUT /api/session-drafts/:id` with directory, project id, optional target folder id, optional lead flag, text, mentions, and attachments, keeping `createdAt` from an existing draft and setting `updatedAt` to the write time. |
| FR-3 | Must | The system shall store uploaded attachment bytes under `session-drafts/<draftId>/<attachmentId>`, serve them by id with the recorded MIME type and `private, no-store` caching, and store path attachments as the server path alone, exposing that path only for path attachments in public responses. |
| FR-4 | Must | The system shall keep an attachment that a later save sends by id alone, decode a new `data:` URL with a `;base64` prefix, drop attachments that carry neither new bytes nor an existing id, and remove files no longer listed in the draft. |
| FR-5 | Must | The system shall accept draft and attachment ids made of letters, digits, `_`, `.`, and `-` starting with a letter or digit, recheck destination paths before writing bytes, and enforce at most 200 drafts, 20 attachments per draft, 25 MB of attachment bytes per draft, and a 40 mb request body. |
| FR-6 | Must | The system shall remove a draft and its attachment files through `DELETE /api/session-drafts/:id` and report whether a row was removed. |
| FR-7 | Must | The system shall serialize draft writes and announce `openchamber:session-drafts-changed` after each write that changes the store, and the UI shall reload drafts on that event and on `event-stream-ready` while VS Code shall not subscribe. |
| FR-8 | Must | The UI shall queue saves per draft, keep an offline copy of unsent text, mentions, attachments, target folder, and lead flag without the attachment bytes, retry that copy on load, and restore the saved values into a new session. |
| FR-9 | Must | The UI shall discard a draft locally and on the server, and a final discard shall prevent a later save of the same draft id. |
| FR-10 | Must | The system shall select one warming mode from `off`, `all`, and `session`, where `all` writes OpenCode's `warming` key and turns per-session warming off, `session` removes that key and turns per-session warming on, and `off` does both, with the OpenCode config write made before any per-session state change. |
| FR-11 | Must | The system shall accept only 30, 60, 120, and 180 minutes for warming duration, write OpenCode's `warming.duration` for scope `all` with 30 minutes written back as plain `true`, and shift every running window by the difference for scope `session`. |
| FR-12 | Must | The system shall toggle one session through `PUT /api/session-warming/sessions/:sessionId` only while per-session warming is on, require a session id and a directory, refuse sessions in an isolated space, and forget a session when `warm` is false. |
| FR-13 | Must | The system shall send a keep-alive `POST /api/session/:id/generate` with the OpenCode prompt from the end of the session's last turn until the chosen duration expires, passing the session directory and adding nothing to session history. |
| FR-14 | Must | The system shall clear `warmUntil` and stop pings while a turn runs, set `warmUntil` to the chosen duration when a turn ends, and time the first ping from that turn end. |
| FR-15 | Must | The system shall ask OpenCode's `/api/session/active` when it has seen no event for a session, ping at once when the session is idle, wait for the turn to end when it is busy, and retry a failed status read after 30 seconds. |
| FR-16 | Must | The system shall clear remembered activity and settle every warmed session again on `server.connected`, because a gap in the event stream can hide turns. |
| FR-17 | Must | The system shall forget a session on `session.deleted` or a 404 response to a ping, and shall keep the window and wait for the next interval after any other ping failure. |
| FR-18 | Must | The system shall use `epoch` and `pendingEpoch` so work in flight across a state change does not act on the new state and no second ping is armed while a ping or status read is pending. |
| FR-19 | Must | The system shall persist warming state to `session-warming.json` with atomic writes, read that file synchronously at start before routes or events change state, rename an unreadable file to `session-warming.json.corrupt-<time>`, and resolve `stop` after pending writes finish. |
| FR-20 | Must | The system shall persist and broadcast a full warming snapshot with a rising `revision` on every change, and the UI shall apply only snapshots at least as new as the one it holds. |
| FR-21 | Must | The system shall report a warmed session as warm until `warmUntil` plus one cache lifetime so routing keeps its cache hold. |
| FR-22 | Should | The UI shall fall back to `PUT /api/config/warming` for `all` and `off` when the warming service is unavailable, report per-session warming as unavailable there, and skip both draft and warming subscriptions in VS Code. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall keep draft and attachment writes inside the attachment root after validating ids and rechecking resolved paths, and shall hide the private byte storage path from list responses. |
| NFR-2 | Must | Reliability | The system shall write draft and warming state through a temporary file and rename, serialize draft writes, answer 500 on a malformed draft store, and preserve an unreadable warming file under a corrupt suffix. |
| NFR-3 | Must | Availability | The UI shall keep a failed draft save as a local row without attachment bytes and retry it on load, and shall never treat a failed fetch as an authoritative empty draft list. |
| NFR-4 | Must | Correctness | Warming revisions shall start from the clock so a snapshot after a restart is newer than the one a client last saw, and a late older snapshot shall be ignored. |
| NFR-5 | Should | Performance | The system shall ping at 90 percent of the model's cache lifetime, fall back to four minutes when the lifetime is unknown, and send no ping when the cache outlives the warming window. |
| NFR-6 | Should | Portability | The shared UI shall serve web, desktop, hosted mobile, and Capacitor mobile through the same routes and stores, with VS Code using only the OpenCode config fallback. |

## Constraints

- Draft bytes and state live under the OpenChamber data directory.
- The store format is `{ version: 1, drafts }`, and its Zod schema rejects malformed stored files.
- Attachment ids in the store are `data` with bytes on disk or `path` with a server file path.
- `session-warming.json` holds `enabled`, `minutes`, and a record of session id to `{ directory, warmUntil }`.
- Warming duration steps are 30, 60, 120, and 180 minutes, with 60 minutes as the default.
- Session ids match `^[A-Za-z0-9_-]{4,128}$`.
- Sessions in an isolated space use the space's own OpenCode and cannot be pinged by this server.
- OpenCode's own `warming` config key belongs to `opencode/websearch-config.js`, so the mode route only chooses the target of a config write.
- The UI sync modules run outside VS Code; there is no OpenChamber server in that runtime.

## Acceptance Criteria

```gherkin
@FR-1
Feature: Server-owned draft list
  Scenario: Reading drafts after a save
    Given a data directory with a version 1 draft store
    When a client calls GET /api/session-drafts
    Then every stored draft is returned without its private byte storage path
  Scenario: Broken store file
    Given session-drafts.json contains invalid JSON
    When a client calls GET /api/session-drafts
    Then the route answers 500 and never an empty list
```

```gherkin
@FR-2
Feature: Saving a draft
  Scenario: Saving folder target and lead flag
    Given a client sends a draft with directory, text, targetFolderId, and lead true
    When the server handles PUT /api/session-drafts/:id
    Then the response and the later list carry targetFolderId and lead
  Scenario: Saving an older shape
    Given a client sends a draft without target folder or lead fields
    When the server handles the request
    Then the draft is accepted with its text and directory
```

```gherkin
@FR-3
Feature: Attachment bytes
  Scenario: Upload and read back
    Given a draft carries an attachment with a base64 data URL
    When the server saves it and a client requests the attachment by id
    Then the bytes are served with the recorded MIME type and private no-store caching
  Scenario: Path attachment
    Given a draft carries a server path attachment
    When a client reads the draft list
    Then the response includes the server path and no private byte location
```

```gherkin
@FR-4
Feature: Attachment updates
  Scenario: Keeping an existing attachment
    Given a saved draft holds attachment bytes under an id
    When a later save lists that attachment by id alone
    Then the attachment stays in the draft with its kind and size
  Scenario: Removing an attachment
    Given a saved draft holds attachment bytes under an id
    When a later save omits that attachment
    Then its file is removed from the draft folder
  Scenario: Invalid data URL
    Given an attachment data URL without a ;base64 prefix
    When the server saves the draft
    Then the route answers 400
```

```gherkin
@FR-5
Feature: Draft limits and ids
  Scenario: Escaping id
    Given a draft id of ../x or an attachment id of ..
    When the server handles a save or delete
    Then the route answers 400 and no file outside the drafts folder changes
  Scenario: Cap reached
    Given the store already holds 200 drafts
    When a client saves a new draft id
    Then the route answers 409 and asks the client to send or discard one first
```

```gherkin
@FR-6
Feature: Discarding a draft
  Scenario: Removing row and files
    Given a saved draft holds a data attachment
    When a client calls DELETE /api/session-drafts/:id
    Then the response reports deleted true, the row is gone, and the draft folder is gone
```

```gherkin
@FR-7
Feature: Draft change broadcast
  Scenario: Saving then another client reloads
    Given two clients are connected to one server
    When one client saves a draft
    Then the write is serialized, session-drafts-changed is announced, and the other client reloads the list
  Scenario: Event stream ready
    Given a client has just reconnected its event stream
    When event-stream-ready arrives
    Then the client loads drafts again
```

```gherkin
@FR-8
Feature: Offline draft queue
  Scenario: Save without a server
    Given the server is unreachable
    When the user saves text with an attached image
    Then a local row keeps the text and mentions, the stored copy omits image bytes, and the row shows before any list arrives
  Scenario: Retry after reconnect
    Given an unsynced draft and a reachable server
    When the draft list is loaded
    Then the draft is sent again with its image bytes and the local unsynced copy is cleared
```

```gherkin
@FR-9
Feature: Discard while offline
  Scenario: Throwing away an unsynced draft
    Given a draft was saved while the server was unreachable
    When the user discards it
    Then the row and the local unsynced copy are gone
```

```gherkin
@FR-10
Feature: One warming mode
  Scenario: Switching modes
    Given per-session warming is off
    When the user selects all and then session
    Then OpenCode's warming key is written for all and removed for session, and only session enables per-session warming
  Scenario: Config write fails
    Given the OpenCode config write throws
    When a mode change is requested
    Then the route answers 500 and per-session state is unchanged
```

```gherkin
@FR-11
Feature: Warming duration
  Scenario: Setting a step for each scope
    Given warming is available
    When the client sets 180 minutes for session and 120 minutes for all
    Then the session runtime reports 180 minutes and the OpenCode duration write receives 120
  Scenario: Unsupported step
    Given a client sends 45 minutes
    When the duration route handles the request
    Then the route answers 400
```

```gherkin
@FR-12
Feature: Warming one session
  Scenario: Toggling a session
    Given per-session warming is on
    When a client sends warm true and then warm false for a session id with a directory
    Then the snapshot holds that session with warmUntil null and then holds no sessions
  Scenario: Warming is off or space is isolated
    Given per-session warming is off or the directory belongs to an isolated space
    When a client tries to warm a session
    Then the route answers 409 or 400 respectively
```

```gherkin
@FR-13
Feature: Keep-alive requests
  Scenario: Idle warmed session
    Given a session's last turn ended and its warm window is open
    When the interval elapses
    Then the server posts the OpenCode keep-alive prompt to the generate route with the session directory
  Scenario: Window expired
    Given the warmUntil time has passed
    When the timer would fire
    Then no further ping is sent
```

```gherkin
@FR-14
Feature: Turn boundaries
  Scenario: Turn starts during a window
    Given a warmed session is idle with a running window
    When a busy status event arrives
    Then warmUntil becomes null and pings stop
  Scenario: Turn ends again
    Given the session was busy
    When an idle status event arrives
    Then a new window starts from that turn end and the first ping follows its beat
```

```gherkin
@FR-15
Feature: Unknown activity
  Scenario: Toggle with no event seen
    Given the runtime has no activity record for a warmed session
    When it settles the session
    Then it reads /api/session/active first
  Scenario: Status read failed
    Given the status read throws
    When the runtime settles the session
    Then it retries after 30 seconds and does not treat the failure as idle
```

```gherkin
@FR-16
Feature: Reconnect
  Scenario: Event stream came back
    Given turns happened while the stream was disconnected
    When server.connected arrives
    Then activity is cleared and every warmed session is settled again against OpenCode
```

```gherkin
@FR-17
Feature: Forgetting sessions
  Scenario: Session deleted
    Given a warmed session is in the runtime
    When session.deleted arrives
    Then the session is forgotten and a snapshot is broadcast
  Scenario: Ping says gone
    Given the generate route answers 404
    When the runtime handles the response
    Then the session is forgotten
  Scenario: Other ping failure
    Given the generate route answers 503
    When the runtime handles the response
    Then the window keeps counting and a ping goes at the next interval
```

```gherkin
@FR-18
Feature: In-flight work
  Scenario: Duration changes during a ping
    Given a ping is still in flight
    When the warming duration changes
    Then no second ping is armed for the same window
  Scenario: Reconnect during an interval read
    Given a model interval read is pending
    When server.connected arrives
    Then the first ping keeps the turn-end beat once the read finishes
```

```gherkin
@FR-19
Feature: Warming state file
  Scenario: Restart with saved state
    Given warmed sessions and 180 minutes were saved
    When the runtime starts again
    Then the same sessions and duration are restored before routes or events change state
  Scenario: Unreadable file
    Given session-warming.json contains invalid JSON
    When the runtime starts
    Then it starts empty and the old file is kept under a corrupt suffix
```

```gherkin
@FR-20
Feature: Snapshot sync
  Scenario: Every change broadcasts
    Given per-session warming is on
    When a session is warmed and then unwarmed
    Then each change persists state and broadcasts a full snapshot with a higher revision
  Scenario: Late older snapshot
    Given the UI holds revision 5
    When a snapshot with revision 4 arrives
    Then the UI keeps the newer state
```

```gherkin
@FR-21
Feature: Cache hold
  Scenario: Warm after the window
    Given a session has warmed for the full hour and the model cache lasts five minutes
    When routing asks whether the session is warm four minutes later
    Then the session is still warm until warmUntil plus the cache lifetime
```

```gherkin
@FR-22
Feature: Runtime boundaries
  Scenario: Warming service unavailable
    Given the warming endpoint is unavailable in a runtime
    When the user selects all or off
    Then the UI writes the OpenCode warming config through /api/config/warming and reports per-session warming as unavailable
  Scenario: VS Code runtime
    Given the UI runs inside VS Code
    When sync subscriptions start
    Then neither draft nor warming subscriptions run
```

```gherkin
@NFR-1
Feature: Draft path safety
  Scenario: Rejected ids and hidden storage
    Given ids with slashes or dot segments and a draft with uploaded bytes
    When the server saves and lists drafts
    Then the writes stay inside the drafts folder and the list omits the byte location
```

```gherkin
@NFR-2
Feature: Durable writes
  Scenario: Malformed draft store and corrupt warming file
    Given a broken draft store and an unreadable warming file
    When drafts are read and the warming runtime starts
    Then drafts answer 500 and the warming file is kept under a corrupt suffix
```

```gherkin
@NFR-3
Feature: Failed fetch is not empty
  Scenario: Offline load
    Given a failed draft save and a failed list fetch
    When the UI loads drafts
    Then the local row stays visible and no empty server list erases it
```

```gherkin
@NFR-4
Feature: Monotonic revisions
  Scenario: Snapshot after restart
    Given a client saw a snapshot before the server restarted
    When a new snapshot arrives with a clock-based revision
    Then its revision is higher and the UI applies it
```

```gherkin
@NFR-5
Feature: Cache-aware interval
  Scenario: Long cache and short window
    Given a model with an hour-long cache and a 30-minute warming window
    When the window starts
    Then no ping is sent because the cache outlives the window
  Scenario: Unknown cache lifetime
    Given the server cannot read a model cache lifetime
    When the window starts
    Then the ping interval is four minutes
```

```gherkin
@NFR-6
Feature: Shared UI surfaces
  Scenario: Same stores in every server-backed runtime
    Given web, desktop, hosted mobile, and Capacitor mobile clients
    When each connects to an OpenChamber server
    Then the same draft and warming routes and stores drive the sidebar and warming controls
```

## Conflicts

None identified yet.

## Open Questions

None.
