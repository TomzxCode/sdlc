---
title: "Message Search"
status: done
---

# Test Plan: Message Search

## Scope

Tests cover the FTS store (match expressions, search filters, paging, snippets), the indexer (content selection, cursors, reverts, background walks, events), the runtime lifecycle (off/on/delete, reasoning switch), and the client helpers (searchable-query check, snippet splitting).
There is no dedicated routes test file; routes are thin zod validation over the runtime.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Indexes user messages and agent text, not tools, reasoning, or subagents | Session with user, agent, tool, reasoning, and subagent parts | Only user and agent text searchable |
| TC-2 | Indexes reasoning as its own row of the same message, excludable from search | Reasoning parts with include on/off | Reasoning row found when included, absent when `includeReasoning` is false |
| TC-3 | Re-reads agent records after `rereadAssistantRecords` | Reasoning skipped, then re-read requested | Previously skipped reasoning becomes searchable |
| TC-4 | Matches inside words in any script, ignoring case | In-word and CJK queries | Hits on substring and cross-case matches |
| TC-5 | Reads only what came after the cursor on the next sync | Second sync with no changes | No duplicate rows, cursor advanced |
| TC-6 | Leaves an unfinished reply for later without skipping it | Assistant record without `time.completed` | Not indexed, cursor held, indexed after completion |
| TC-7 | Marks every whole occurrence in any case | Text with repeated mixed-case terms | All occurrences wrapped in U+E000/U+E001 |
| TC-8 | Centres a long message on its first match and marks the edges | Long text, single term | Window around first match with edge markers |
| TC-9 | Merges overlapping terms and flattens line breaks | Overlapping terms, multiline text | Single merged marks, no newlines in snippet |
| TC-10 | Centres on the longest word of the query | Multi-word query, long text | Window centred on the longest term's match |
| TC-11 | Requires one word the index can look up | `ab`, `ab cd`, `ab світ`, blank | False, false, true, false |
| TC-12 | Splits a snippet into plain runs and matches | Marked snippet with two matches | Alternating plain/match segments |
| TC-13 | Keeps markup-looking text as text | `<b>not bold</b>` snippet | Single plain segment, no markup interpretation |
| TC-14 | Tolerates an unterminated match | Snippet with start marker only | Trailing text returned as a match segment |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-15 | Off means no file, no listeners, no answers | Setting off, disconnected hub | Status `off`, no index file, `search()` returns null |
| TC-16 | Starts from the saved setting and keeps the file when switched off | Setting on, then `setEnabled(false/true)` | `on` with listeners, off keeps file, back on re-subscribes |
| TC-17 | Deletes the file while off, starts fresh while on | Populated index in both states | File removed while off; zeroed index running while on |
| TC-18 | Records reasoning state and follows its switch only while running | Reasoning toggles across restarts | `meta.reasoning` reflects last applied value |
| TC-19 | Restarts a session whose cursor anchor message is gone | Cursor points after a deleted message | Session reset and read from the start |
| TC-20 | Keeps its cursor when there is simply nothing new | Empty page, anchor message present | No reset, cursor retained |
| TC-21 | Forgets what a revert took back | Revert boundary set, then new prompt | Tail rows removed, re-read from boundary |
| TC-22 | Drops sessions OpenCode no longer lists, but not on a failed list | Deleted session; failed list call | Deleted session dropped; failed list drops nothing |
| TC-23 | Skips sessions unchanged since they were read | Walk with identical `time.updated` | No message-list calls for unchanged sessions |
| TC-24 | Follows renames, moves, and deletions from events | `session.updated` / `session.deleted` | Title/directory updated, deleted session dropped |
| TC-25 | Indexes a session when its turn ends | `session.idle` after new messages | New content searchable after debounce |
| TC-26 | Filters by session, directory, and author, paging without repeats | Multi-session index with `before` cursor | Filtered pages with no repeats or skips |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-27 | Session list fetch fails mid-walk | No sessions dropped; failure is not an empty list |
| TC-28 | OpenCode rejects a cursor | Session reset and read again, at most once per sync |
| TC-29 | No SQLite builtin on the platform | Status `unsupported`, queries answer 503 / `unavailable` |
| TC-30 | Query of only sub-3-character words | `query-too-short` with empty hits, never the full index |
| TC-31 | Lower/upper-casing changes string length (rare scripts) | Snippet returned unmarked rather than with drifted offsets |
| TC-32 | Delete asked while a session is being read | In-flight read finishes before the file closes |

## Test Infrastructure

- `packages/web/server/lib/message-search/indexer.test.js` (vitest, fake OpenCode paging like v2, `:memory:` store; TC-1 to TC-10, TC-19 to TC-26).
- `packages/web/server/lib/message-search/runtime.test.js` (vitest, temp data dir, disconnected hub; TC-15 to TC-18).
- `packages/ui/src/lib/messageSearch.test.ts` (bun:test; TC-11 to TC-14).
- `store.js` snippet constants (`MATCH_START`/`MATCH_END`) shared with the client for marker parsing.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-15, TC-16 |
| FR-2 | TC-1 |
| FR-3 | TC-2, TC-3, TC-18 |
| FR-4 | TC-5, TC-25 |
| FR-5 | TC-6 |
| FR-6 | TC-19, TC-20, TC-21, TC-28 |
| FR-7 | TC-22, TC-23, TC-27 |
| FR-8 | TC-24 |
| FR-9 | TC-4, TC-26, TC-30 |
| FR-10 | TC-17 |
| FR-11 | TC-17 |
| FR-12 | TC-11, TC-29 |
| FR-13 | TC-7, TC-8, TC-9, TC-10, TC-12, TC-13, TC-14 |
| NFR-3 | TC-32 |
| NFR-4 | TC-29 |
| NFR-5 | TC-16, TC-27 |
