---
title: "Message Search"
status: done
---

# Requirements: Message Search

## Overview

Full-text search over this server's conversations exists because OpenCode 2 searches session titles only, so the server keeps its own trigram FTS5 index of user messages and settled agent replies for root sessions.
Search is strictly opt-in through `messageSearchEnabled`, with agent reasoning behind a second opt-in switch, and the UI, routes, and runtime all stay dormant while search is off.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Chat users | Find past user messages and agent replies across all conversations |
| Readers of long reasoning traces | Keep reasoning out of results while the reader hides reasoning |
| Operators of weak hardware | Pay zero indexing cost unless search is explicitly turned on |
| Maintainers | Keep the index derived, dependency-free, and rebuildable at any time |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall keep search off until `messageSearchEnabled` is turned on, and while off it shall open no index file, listen to no events, run no backfill, answer queries with 503, and show no message search in the UI. |
| FR-2 | Must | The system shall index user messages and the text of settled agent replies for root sessions only, and it shall exclude tool calls and their output, attached context records, and subagent sessions. |
| FR-3 | Must | The system shall gate agent reasoning behind `messageSearchReasoningEnabled` (off by default), store reasoning as its own row with `role = 'reasoning'`, row id `<messageId>:reasoning`, and `message_id` pointing at its message, and record the state in `meta.reasoning`. |
| FR-4 | Must | The system shall queue a session for sync on `session.idle` and on a settled assistant step (`message.updated` with `time.completed`), debounced, and read each message type from its stored cursor onward without assuming a cursor format. |
| FR-5 | Must | The system shall not index an assistant record without `time.completed` and shall not move the cursor past it, so the next sync reads it again. |
| FR-6 | Must | The system shall recover from history rewrites by resetting a session and reading it again from the start (at most once per sync) when its cursor anchor message is gone or rejected, and it shall index nothing at or after a set revert boundary while dropping stored cursors. |
| FR-7 | Must | The system shall walk the session list on every (re)connect, queue sessions changed since they were read (`time.updated`) behind live work one at a time with a short pause, and drop indexed sessions the list no longer has only when the whole list arrived. |
| FR-8 | Must | The system shall apply `session.updated` (rename, move) and `session.deleted` directly to the index. |
| FR-9 | Must | The system shall require every query word to occur, drop words shorter than three characters, answer `query-too-short` for queries made only of them, page newest-first by default with a `<createdAt>:<id>` cursor that never repeats or skips, filter by session, directory, and role, leave reasoning hits out when `reasoning=0`, and return plain-text snippets with matches marked by U+E000 / U+E001. |
| FR-10 | Must | The system shall report index state, file size, and progress from the status endpoint and delete the index file from the delete endpoint, starting a fresh index at once while search is on. |
| FR-11 | Must | The system shall version the index schema in `meta` and drop and rebuild the file on mismatch, since the file is derived data. |
| FR-12 | Should | The system shall parse server answers once at the client boundary, map 503/404 to `unavailable`, and throw on failed or unknown-shaped responses instead of showing an empty result. |
| FR-13 | May | The system shall centre long-message snippets on the first match of the longest query word, merge overlapping terms, and flatten line breaks. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Should | Performance | A rare word shall answer in about 1 ms and a very common one in about 15 ms (max 25 ms) on a 9072-session / 196k-message index, with single-session search in about 12 ms. |
| NFR-2 | Should | Resource utilization | The trigram index shall stay around five times the indexed text, and enabling reasoning may multiply index size several times. |
| NFR-3 | Must | Responsiveness | Indexing shall never block the event loop over 50 ms by bounding work per page rather than by session count. |
| NFR-4 | Must | Portability | The runtime shall use the builtin SQLite (`node:sqlite` on Node and Electron, `bun:sqlite` on Bun) with no dependency, and report `unsupported` with 503 answers where neither exists. |
| NFR-5 | Must | Reliability | Start, stop, and delete transitions shall run serialized in the order asked, and a failed session-list page shall never be treated as an empty list. |

## Constraints

- No new dependency: only the platform SQLite builtin may be used.
- Only root sessions are indexed; tool output is excluded by maintainer decision (2026-10-01) because it dwarfs conversation text (~200 MB vs ~3 MB on the maintainer's machine).
- Setting keys are instance scope in `settings.json`: `messageSearchEnabled` and `messageSearchReasoningEnabled`.
- Turning reasoning on clears every session's agent cursor for a re-read; turning it off deletes reasoning rows at once.
- The UI asks with `reasoning=0` while the reader hides reasoning traces.

## Acceptance Criteria

```gherkin
@FR-1
Feature: Search stays off until enabled
  Scenario: Setting off
    Given messageSearchEnabled is false
    When the server runs and a query arrives
    Then no index file is opened and the route answers 503
```

```gherkin
@FR-2
Feature: Only conversation text is indexed
  Scenario: Mixed session content
    Given a session with user text, agent text, tool calls, and a subagent session
    When the session is indexed
    Then user and agent text are searchable and tool, context, and subagent content is not
```

```gherkin
@FR-3
Feature: Reasoning is a second opt-in
  Scenario: Reasoning enabled then disabled
    Given messageSearchReasoningEnabled is turned on
    When reasoning rows are indexed and the switch is turned off
    Then reasoning rows exist while on and are deleted at once when off
```

```gherkin
@FR-4
Feature: Live sync follows settled activity
  Scenario: Turn ends
    Given a session with a settled assistant step carrying time.completed
    When session.idle arrives
    Then the session is queued and read from its stored cursor onward
```

```gherkin
@FR-5
Feature: Unfinished replies wait
  Scenario: Reply still streaming
    Given an assistant record without time.completed
    When a sync runs
    Then the record is not indexed and the cursor does not move past it
```

```gherkin
@FR-6
Feature: Rewrites recover by reset
  Scenario: Cursor anchor deleted after revert
    Given a stored cursor pointing after a deleted message
    When a sync reads an empty page
    Then the session is reset and read again from the start once per sync
```

```gherkin
@FR-7
Feature: Background walk catches up
  Scenario: Reconnect after changes
    Given sessions changed while the indexer was away and one session deleted
    When the session list walk completes
    Then changed sessions are re-read and the deleted session is dropped
```

```gherkin
@FR-8
Feature: Rename, move, and delete apply directly
  Scenario: Session renamed
    Given a session.updated event with a new title
    When the event is processed
    Then the indexed session row carries the new title without a full re-read
```

```gherkin
@FR-9
Feature: Query semantics and paging
  Scenario: Short-word query
    Given the query "ab cd"
    When it is searched
    Then the answer is query-too-short with no hits
```

```gherkin
@FR-10
Feature: Status and delete endpoints
  Scenario: Delete while on
    Given search is on with a populated index
    When DELETE message-search/index runs
    Then the file is removed and a fresh index starts at once
```

```gherkin
@FR-11
Feature: Schema mismatch rebuilds
  Scenario: Version bump
    Given an index file with an older schema version in meta
    When the store opens
    Then the file is dropped and rebuilt
```

```gherkin
@FR-12
Feature: Client never lies about failures
  Scenario: Network error
    Given a failed search request
    When searchMessages settles
    Then it throws instead of returning an empty result
```

```gherkin
@FR-13
Feature: Snippet windowing
  Scenario: Long message with a match
    Given a long message and a multi-word query
    When a snippet is built
    Then it centres on the longest query word with merged marks and no line breaks
```

## Open Questions

None known.
