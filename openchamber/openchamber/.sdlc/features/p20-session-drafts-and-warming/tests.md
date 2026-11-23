---
title: "Session drafts and warming"
status: done
---

# Test Plan: Session drafts and warming

## Scope

Tests cover the draft routes and their file store, the warming routes and their runtime, and the two shared UI stores with stubbed transport.
Server route tests exercise validation, file writes, attachment bytes, mode and duration mapping, and error responses.
Runtime tests use a fake clock and a fake OpenCode to exercise timers, event handling, cache-lifetime reads, restarts, and broadcasts.
UI store tests cover the offline draft queue and snapshot ordering.
There is no browser-level end-to-end suite, and the sync modules and warming UI components have no dedicated test files in this set.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Rejects ids that could leave the drafts folder | Draft ids `../x`, `..`, `.`, `-x` and attachment id `..` | 400 for saves and deletes, and the data folder is untouched |
| TC-2 | Does not read a broken draft store as an empty list | `session-drafts.json` containing `{"broken"` | GET answers 500 |
| TC-3 | Preserves unchecked thrown messages from mode config writes | `null`, a string, an empty message, a numeric message, an inherited message, and a proxy | 500 with the original message or the fallback text |
| TC-4 | Preserves an unchecked thrown message from a duration config write | Thrown object with `message: { reason: 'read-only' }` | 500 with that object as the error |
| TC-5 | Rejects an unoffered warming duration step | `{ scope: 'session', minutes: 45 }` | 400 |
| TC-6 | Rejects malformed mode and session bodies | Mode `sometimes`, missing directory, session id `x` | 400 for each request |
| TC-7 | Ignores unrelated and malformed event payloads | `null`, a string, `{}`, unknown status type, deletion without id | Snapshot unchanged and no pings |
| TC-8 | Broadcasts a rising revision on every change | Enable, warm, and unwarm a session | Three broadcasts with clock-based then +1 revisions |
| TC-9 | Keeps the newest warming snapshot and ignores an older one that arrives late | Snapshot revision 5 then revision 4 | State from revision 5 remains |
| TC-10 | Forgets the revision on reset | Apply revision 50, reset, apply revision 3 | Revision 3 applies after reset |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-11 | Round trips a folder target and the lead flag, and accepts older drafts | PUT with `targetFolderId` and `lead: true`, then PUT without them | Both fields survive in the saved draft and the list; the older draft is accepted |
| TC-12 | Stores attachment bytes, serves them, and announces the change | PUT with a base64 PNG attachment | 200, `onChanged` called once, byte route returns the original bytes |
| TC-13 | Removes files no longer listed in a draft | Saved draft with one data attachment, then PUT without it | The attachment file is gone |
| TC-14 | Keeps an attachment sent by id alone | Saved draft with bytes, then PUT with only id, filename, MIME type, and size | Attachment stays with `kind: 'data'` |
| TC-15 | Discards a draft and its files | Saved draft with one data attachment | `{ deleted: true }`, empty list, draft folder gone |
| TC-16 | Switches between OpenCode warming and per-session warming | Runtime with a stub config writer | `all` writes warming true, `session` removes it, `off` leaves no sessions |
| TC-17 | Leaves per-session state alone when the config write fails | Config writer throws on mode change | 500 and runtime still disabled |
| TC-18 | Toggles one session and refuses while warming is off | Warming off, then on | 409 while off, then a session with `warmUntil: null`, then no sessions after `warm: false` |
| TC-19 | Refuses a session in an isolated space | Directory `/spaces/0123456789ab/repo` | 400 |
| TC-20 | Pings an idle warmed session at the default interval | Warming on, busy then idle event, fake clock | First ping at four minutes with keep-alive prompt and directory query, none after the window |
| TC-21 | Stops pinging while a turn runs and restarts the window when it ends | Warmed session goes busy for 10 minutes, then idle | `warmUntil` null while busy, no pings, then a new window and a ping |
| TC-22 | Times the first ping from the turn that just ended | Idle event one minute before the toggle | First ping one interval after the turn end |
| TC-23 | Asks OpenCode when no event was seen for the session | Unknown session, active list idle or busy | Idle pings at once with a window; busy waits until an idle event |
| TC-24 | Settles every warmed session again after a reconnect | Turn ended while the stream was down, then `server.connected` | One ping and a live window, then pings stop if a new unseen turn is busy |
| TC-25 | Keeps pinging after a failed ping | Generate route answers 503 once | One failed ping, then a second at the next interval and the session retained |
| TC-26 | Forgets sessions OpenCode no longer knows or deleted | Generate answers 404, or `session.deleted` arrives | Empty session list and a broadcast |
| TC-27 | Forgets every session and sends no pings when warming turns off | Warmed session, then `setEnabled(false)` | Empty state and no pings through the window |
| TC-28 | Moves running windows by the new step and keeps the duration across a restart | Warmed session, 30 then 180 minutes, stop, start on the same data dir | Window shifted, missed ping sent once it fits, 180 minutes restored |
| TC-29 | Drives the ping interval from the model cache lifetime | Claude Agent subscription, configured `ttl: '10m'`, invalid ttls, billed Claude Agent, and a window that grows | Pings at 54 minutes, 9 minutes, 4 minutes, 4 minutes, and after the longer window starts |
| TC-30 | Counts a warmed session as warm for one cache lifetime after the window | 60-minute window and 5-minute cache lifetime | Warm through the window plus 4 minutes, then cold; another session is cold |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-31 | Unreadable warming state file | Runtime starts empty and keeps the old bytes under `session-warming.json.corrupt-<time>` |
| TC-32 | Restarted session whose activity is unknown | Status is read after 30 seconds; an idle answer pings, and a busy answer waits with `warmUntil` null |
| TC-33 | Event stream while per-session warming is off | Events are ignored and only the status read for a toggle is sent |
| TC-34 | Reconnect while an interval read is pending | The first ping keeps the turn-end beat after the read resolves |
| TC-35 | Duration change while a ping is in flight | No second ping is armed; the next ping follows after the in-flight one resolves |
| TC-36 | Draft saved while the server is unreachable | Local row shows text and attachment metadata, stored copy omits bytes, load shows the row, and a later load resends with bytes |
| TC-37 | Draft discarded while the server is unreachable | Row and local unsynced copy are both gone |
| TC-38 | Move to the directory a draft already uses | No request is sent, and the move waits behind the retry queued before it |

## Test Infrastructure

- `packages/web/server/lib/session-drafts/routes.test.js` uses vitest with a fake Express app, temporary data directories, real `fs/promises`, and a fixed clock.
- `packages/web/server/lib/session-warming/routes.test.js` uses vitest, supertest, an Express app, a temporary data directory, and a fake config writer.
- `packages/web/server/lib/session-warming/runtime.test.js` uses vitest fake timers, a fake OpenCode fetch, a fake broadcast callback, and temporary data directories.
- `packages/ui/src/stores/useSessionDraftsStore.test.ts` uses bun:test with a stubbed global fetch and `getDeferredSafeStorage`.
- `packages/ui/src/stores/useSessionWarmingStore.test.ts` uses bun:test and the Zustand store directly.
- All runtime tests call `stop()` before removing their temporary directories so pending writes finish first.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-11 |
| FR-2 | TC-11, TC-14 |
| FR-3 | TC-12 |
| FR-4 | TC-12, TC-13, TC-14 |
| FR-5 | TC-1 (draft and attachment caps are implemented but not asserted) |
| FR-6 | TC-15 |
| FR-7 | TC-12 (sync subscriptions have no dedicated test) |
| FR-8 | TC-11, TC-36, TC-38 |
| FR-9 | TC-15, TC-37 |
| FR-10 | TC-3, TC-16, TC-17 |
| FR-11 | TC-4, TC-5, TC-28 |
| FR-12 | TC-6, TC-18, TC-19 |
| FR-13 | TC-20, TC-22, TC-29 |
| FR-14 | TC-21, TC-22 |
| FR-15 | TC-23, TC-32 |
| FR-16 | TC-24, TC-34 |
| FR-17 | TC-25, TC-26 |
| FR-18 | TC-34, TC-35 |
| FR-19 | TC-28, TC-31, TC-32 |
| FR-20 | TC-8, TC-9, TC-10 |
| FR-21 | TC-30 |
| FR-22 | TC-27, TC-33 (config fallback and VS Code skip are implemented but not asserted) |
| NFR-1 | TC-1, TC-12 |
| NFR-2 | TC-2, TC-31 |
| NFR-3 | TC-36, TC-37 |
| NFR-4 | TC-8, TC-9, TC-10 |
| NFR-5 | TC-20, TC-29 |
| NFR-6 | TC-16 (no cross-runtime matrix exists) |
