---
title: "Session work and todos"
status: done
---

# Test Plan: Session work and todos

## Scope

This plan covers the server work runtime, the work state patches, the todo route and runtime, the todo loader, the live work reducer and the work status section order.
It excludes In work sidebar rendering, Jev prompt measurement and the Small Model requests that consume the assist gate.
The cases below are the tests present in the repository at the time these artifacts were reverse-engineered.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `state.test.js` reads a work record and treats missing or malformed data as none. | Valid, absent and invalid work metadata. | Parsed record, null and null. |
| TC-2 | `state.test.js` opens a session that is not in work. | Empty metadata with requestAt 5 and now 10. | State open, openedAt 10, openedBy auto and cleared timestamps. |
| TC-3 | `state.test.js` refuses to open a pinned session and still closes one an older build left open. | Pinned metadata and pinned metadata with an open work record. | No open patch, and a done patch. |
| TC-4 | `state.test.js` reopens a done session only for a later message. | doneAt 7 with requestAt 5, 7 and 8. | Null, null and an open patch. |
| TC-5 | `state.test.js` hints done only in work and retires the hint once. | Open work, done work and a record with a hint. | Hint patch, null and a clearing patch. |
| TC-6 | `state.test.js` offers a review on any session and clears both hints on a new turn. | Empty metadata and metadata with both hints. | Review offer patch and a patch clearing both. |
| TC-7 | `runtime.test.js` keeps an assist field Jev did not answer and drops only a clear no. | Empty, partial and threshold-crossing Jev answers. | Allowed gates and a false hint for an unanswered sign. |
| TC-8 | `session-todos/runtime.test.js` reads OPENCODE_FLAGS the way OpenCode does. | `todo`, `all,-todo`, `all`, unrelated flags and undefined. | True, false, true, undefined and undefined. |
| TC-9 | `session-todos/runtime.test.js` takes experimental from the highest document that sets it. | Config documents with todo, all_flags and a non-document entry. | Undefined, true, false and undefined. |
| TC-10 | `session-todos/runtime.test.js` defaults on only for local and dev builds. | `local`, `0.0.0-dev-*`, `0.0.0-feature-x-12` and `2.2.7`. | True, true, false and false. |
| TC-11 | `session-live-work.test.ts` follows a tool call from start to input to end. | Pending tool part, raw input and a success transition. | One running call becomes the last call with a named path. |
| TC-12 | `session-live-work.test.ts` handles a start, input and end in one batch and reads a streamed path. | Batched tool events and a partially streamed path. | The call keeps its file name. |
| TC-13 | `session-live-work.test.ts` keeps shell commands out and handles parallel calls and stale ends. | Tool calls without paths, two parallel calls and a new turn or reconnect. | No path is invented and stale calls are cleared. |
| TC-14 | `session-live-work.test.ts` reads context from step totals, falls back to breakdowns and forgets it on compaction. | Token patches, assistant tokens and a completed compaction. | Measured reading, compacted reading and no repeated publishing. |
| TC-15 | `session-live-work.test.ts` clears maps on deletion and keeps them bounded. | A deleted session and more than the bound of sessions. | Both maps drop the session and the oldest entries are evicted. |
| TC-16 | `sections.test.ts` places Tasks after Subagents in default and saved section orders. | Default, saved legacy and custom orders. | Tasks follows Subagents in each order. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-17 | `session-work/runtime.test.js` opens on a sent message without asking Jev. | Stubbed OpenCode and an in-memory metadata store. | Work state is open with openedBy auto and Jev has no call. |
| TC-18 | `session-work/runtime.test.js` opens nothing in a pinned session or pinned worktree. | Pinned metadata or a pinned worktree directory. | No metadata write and the pin check sees the worktree path. |
| TC-19 | `session-work/runtime.test.js` opens on an attachment-only message and a user shell command. | User message with empty text and a shell started event. | Both open the session. |
| TC-20 | `session-work/runtime.test.js` reopens a session closed before the message and keeps one closed after it. | doneAt 40 and doneAt 60 with a message created at 50. | The first reopens and the second stays done. |
| TC-21 | `session-work/runtime.test.js` reads nothing for work already open and handles a message once. | Existing open work and a repeated message id. | No OpenCode call, no write and one handling. |
| TC-22 | `session-work/runtime.test.js` skips a known subsession and learns one it had to read. | A lineage with a known parent and one unknown child. | No reads or Jev call for the known child, and the unknown child is remembered. |
| TC-23 | `session-work/runtime.test.js` opens nothing when In work is off or in a child, review, /btw, scheduled or chat session. | Each ineligible setup in turn. | No metadata write. |
| TC-24 | `session-work/runtime.test.js` recovers a failed metadata read, session read or write. | One injected failure and fake timers at two seconds. | The session opens with no second event delivery. |
| TC-25 | `session-work/runtime.test.js` gives up after bounded retries and does not retry a missing session. | Persistent write failure and a SessionNotFoundError response. | Three writes then a warning, and one session read. |
| TC-26 | `session-work/runtime.test.js` waits for an archived session and respects a later user Done, a settings change or stop. | Archived session, unarchive event and changed metadata or settings. | Open only when still owed, and no write after stop. |
| TC-27 | `session-work/runtime.test.js` asks only assist and review questions for a session not in work. | Session with no work record and both assist fields on. | Four question ids and an assist gate, with no work written. |
| TC-28 | `session-work/runtime.test.js` asks about done and review in work, then retires the hint on a new turn. | Open work, looks-done answers and busy events. | Hint written after the pause and removed on the turn. |
| TC-29 | `session-work/runtime.test.js` offers a review at once and lets looks done replace it. | Review-ready answers with and without looks done. | Review offer written immediately, then replaced by suggestDoneAt. |
| TC-30 | `session-work/runtime.test.js` cancels a hint on a new message or stop and drops a late answer. | Next message inside the pause, several turns and runtime stop. | No hint for overtaken turns and no write after stop. |
| TC-31 | `session-work/runtime.test.js` suppresses hints and suggestions during background work. | Subagent, fresh shell, working child and a Jev timeout. | No done hint and suggestion false, including on failure. |
| TC-32 | `session-work/runtime.test.js` asks about a review only for changed files or absent snapshots. | Empty, nonempty and missing file snapshots. | Review question only in the latter two cases. |
| TC-33 | `session-work/runtime.test.js` answers unknown on a Jev failure and changes nothing. | Jev throws after a valid context read. | Null gate and no metadata write. |
| TC-34 | `session-work/runtime.test.js` makes no call when In work, review and both assist fields are off. | All toggles off. | No Jev call and no OpenCode fetch. |
| TC-35 | `session-todos/routes.test.js` validates the session id and directory before reading. | Short id, missing directory and blank directory. | 400 with no runtime read. |
| TC-36 | `session-todos/routes.test.js` returns the runtime response unchanged. | Off and ready runtime results with a trimmed directory. | 200 with the same body and a trimmed read argument. |
| TC-37 | `session-todos/routes.test.js` keeps arbitrary runtime failures as a 502. | Error objects, odd thrown values, strings and null. | 502 with OpenCode did not answer and a warning. |
| TC-38 | `session-todos/runtime.test.js` stays off and reads no history when the tool is off or the directory is an isolated space. | Empty config and a space directory. | Off result, no message reads and no fetch. |
| TC-39 | `session-todos/runtime.test.js` finds the newest list in history a page at a time and reads it once. | Two pages with an older and newer todowrite call. | Newer list and no further page reads on the next read. |
| TC-40 | `session-todos/runtime.test.js` remembers that a session has no list. | Two pages without a call. | Ready with an empty list and no second walk. |
| TC-41 | `session-todos/runtime.test.js` takes a completed call from the event stream without reading history. | Input start, called and success events for todowrite. | Broadcast with the list and a ready read with no history. |
| TC-42 | `session-todos/runtime.test.js` counts the tool as on where a call was seen. | Empty config plus a completed call. | Ready list for that directory. |
| TC-43 | `session-todos/runtime.test.js` reads only history newer than the stored list after a gap. | Stored call, reconnect and newer or older pages. | Walk stops at checkedThrough and a newer call wins. |
| TC-44 | `session-todos/runtime.test.js` looks again at a message that was streaming during the gap. | A message with a completed time after the stored call. | The second call in that message becomes the list. |
| TC-45 | `session-todos/runtime.test.js` tells clients to read again on reconnect and on config change. | Connect status and config.updated events. | Broadcast with null session or null directory. |
| TC-46 | `session-todos/runtime.test.js` looks the list up again before a revert boundary. | Revert at 200 with calls at 100 and 300. | The call before the boundary is restored. |
| TC-47 | `session-todos/runtime.test.js` keeps a list an event wrote while history was being read. | A blocked history fetch and a live success event. | The live list wins. |
| TC-48 | `session-todos/runtime.test.js` turns off on config change and keeps the list across a restart. | Stored list, config removal, stop and a new runtime on the same data dir. | Off while config is empty and ready with the list after restart. |
| TC-49 | `session-todos/runtime.test.js` forgets a deleted session. | Stored list and a session.deleted event. | Empty list and one history read. |
| TC-50 | `useLoadSessionTodos.test.tsx` never reads the list in VS Code. | Registered VS Code runtime APIs and a mounted probe. | The store load spy has no calls. |
| TC-51 | `useLoadSessionTodos.test.tsx` reads the shown session once in other runtimes. | Registered web runtime APIs and a mounted probe. | One load call with ses_1 and /repo. |

## End-to-End Tests

No browser end-to-end test file covers this feature.
The work status panel is exercised through its section order and loader hook tests.

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-3, TC-18 | Pinned session or worktree. | No open patch and the worktree check receives the resolved directory. |
| TC-4, TC-20 | A message sent before the user closed the work. | The session stays done. |
| TC-21, TC-22 | Repeated message ids and known subsessions. | One handling and no reads for the child. |
| TC-24, TC-25, TC-26 | Failed reads, writes, missing sessions and archived sessions. | Bounded retries, no retry for a missing session and a retry after restore. |
| TC-28, TC-30, TC-32 | Late Jev answers, a new message inside the pause and background work. | No hint is written for an overtaken turn or while the agent waits. |
| TC-33, TC-37 | Jev or OpenCode failure. | Unknown gate or 502 and no state change. |
| TC-8, TC-9, TC-10, TC-42 | Flag overrides, config precedence, dev builds and observed calls. | The same flag decision OpenCode would make. |
| TC-43, TC-44, TC-46 | Reconnect and revert boundaries. | Only history after the stored point is read and a reverted call is replaced. |
| TC-47 | An event lands during a history walk. | The event's list wins. |
| TC-48, TC-49 | Restart and deletion. | Lists survive a restart and deleted sessions are forgotten. |
| TC-13, TC-15 | Parallel tool calls, reconnect and more than 2000 sessions. | Stale calls clear and maps stay bounded. |
| TC-35, TC-36, TC-37, TC-50 | Bad route input and VS Code. | 400, 502 and no client load where no route exists. |

## Test Infrastructure

- Vitest runs the server work state, work runtime, todo route and todo runtime suites.
- `supertest` drives the Express route in `routes.test.js`.
- Bun test with `happy-dom` and React `act` mounts the loader probe in `useLoadSessionTodos.test.tsx`.
- Fake timers cover the two, ten and sixty second open retries and the done hint pause.
- Stubbed `fetch`, in-memory metadata records and temporary data directories isolate OpenCode and the file store.
- `registerRuntimeAPIs` selects the VS Code and web runtime paths in the loader test.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-17, TC-19, TC-21 |
| FR-3 | TC-3, TC-22, TC-23 |
| FR-4 | TC-3, TC-4, TC-20 |
| FR-5 | TC-7, TC-27, TC-33 |
| FR-6 | TC-5, TC-28, TC-30 |
| FR-7 | TC-6, TC-29 |
| FR-8 | TC-31, TC-33 |
| FR-9 | TC-23, TC-34, TC-50 |
| FR-10 | TC-24, TC-25, TC-26 |
| FR-11 | TC-41, TC-48, TC-49 |
| FR-12 | TC-8, TC-9, TC-10, TC-42 |
| FR-13 | TC-35, TC-36, TC-37, TC-38 |
| FR-14 | TC-41, TC-45, TC-46, TC-48 |
| FR-15 | TC-39, TC-40, TC-43, TC-44, TC-47 |
| FR-16 | TC-50, TC-51 |
| FR-17 | TC-45, TC-50, TC-51 |
| FR-18 | TC-16 covers placement; no rendering test covers filtering and ranking. |
| FR-19 | TC-11, TC-12, TC-13, TC-14, TC-15 |
| FR-20 | TC-38 |
| NFR-1 | TC-33, TC-37, TC-47 |
| NFR-2 | TC-15, TC-21, TC-39, TC-40 |
| NFR-3 | TC-1, TC-35, TC-37 |
| NFR-4 | TC-26, TC-43, TC-45, TC-48 |
| NFR-5 | TC-41, TC-50, TC-51; no test asserts an update deadline. |
