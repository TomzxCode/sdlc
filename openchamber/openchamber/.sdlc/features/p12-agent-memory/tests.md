---
title: "Agent Memory"
status: done
---

# Test Plan: Agent Memory

## Scope

Tests cover the file store, the tool dispatch, the HTTP routes, the build flag, injection screening, and project resolution.
The UI client module has no dedicated test file; panel behavior is exercised through the HTTP route tests.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Build flag recognizes truthy values | `1`, `true`, `yes`, `on` in OPENCHAMBER_MEMORY_ENABLE | Feature reported available |
| TC-2 | Build flag rejects other values | Unset, empty, or other strings | Feature reported unavailable |
| TC-3 | Scopes are separate files | Same title saved in global and project | Two independent entries |
| TC-4 | Over-long project ids use the bounded stem | Long project id | Stored under the bounded folder name |
| TC-5 | Unknown scope rejected | Invalid scope | Error thrown |
| TC-6 | Traversal project id rejected | Path separator in projectId | Error thrown |
| TC-7 | Missing file reads as authoritative empty | No memory.json on disk | Empty store, not a failure |
| TC-8 | Malformed storage fails loudly | Corrupt memory.json | Read throws instead of returning empty |
| TC-9 | Malformed entries dropped without failing the read | Mixed valid and invalid entries | Only valid entries returned |
| TC-10 | Entries sorted by recency | Entries with varied updatedAt | Most recently updated first |
| TC-11 | Unknown type falls back to fact | Entry with unknown type | Type reads as fact |
| TC-12 | Empty title or body rejected | Blank title or body | Error thrown |
| TC-13 | Over-limit body rejected, never truncated | Body over 2000 chars | Clear error naming limit and length |
| TC-14 | Same title updates in place | Repeat save with same title | One entry, updated content |
| TC-15 | Reworded restatement replaces the entry | High-overlap rephrasing | Single updated entry, replaced reported |
| TC-16 | Vocabulary-sharing entries kept separate | Low-overlap entries | Both entries kept |
| TC-17 | Short entries use exact-title matching only | Few meaningful words | No fuzzy replacement |
| TC-18 | Global and project caps enforced | Saves past 60 global / 200 project | Refusal with consolidation instruction |
| TC-19 | Full store still corrects a held entry | Restatement save against a full store | Entry updated in place |
| TC-20 | Concurrent creates all survive | Parallel saves | No lost entries |
| TC-21 | Correction rewrites wording, keeps identity | Patch title or body | Same id, new content, bumped updatedAt |
| TC-22 | Emptying a field refused | Blank title or body patch | Error thrown |
| TC-23 | Project scope filed by session directory | Save with session directory | Entry in the resolved project store |
| TC-24 | Project save without a session directory fails | Empty directory | Failure, never written to global |
| TC-25 | Read by title works from the session index | Title string | Full entry returned |
| TC-26 | Unscoped read prefers project over global | Same title in both scopes | Project entry returned |
| TC-27 | Failed store never reported as absent memory | Broken scope on unscoped read | 503-style failure, not a miss |
| TC-28 | List carries no bodies | Stored entries | Summaries only |
| TC-29 | Broken scope reported, not shown as empty | One failing scope | Unavailability flag plus the healthy scope |
| TC-30 | Memory off refuses reads and writes | Setting disabled | All actions refused |
| TC-31 | Unreadable setting closes the surface | Setting read throws | Actions refused |
| TC-32 | Broken change listener never fails the write | Throwing onMemoryChanged | Write still succeeds |
| TC-33 | Injection text flagged on write | Instruction-like text | Entry stored with flagged marker and warning |
| TC-34 | Worktree directory resolves to the repository project | Worktree path | Primary-worktree project id |
| TC-35 | Configured project path wins over git topology | Registered worktree path | Its own project id |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-36 | Global and project read over HTTP | Server running, entries stored | Correct scoped entries returned |
| TC-37 | Project scope without id rejected over HTTP | Missing projectId | 400, store untouched |
| TC-38 | Both scopes read together | Entries in both scopes | Combined response with per-scope failure flags |
| TC-39 | Correction applied from a JSON body | Stored entry | Patched entry returned |
| TC-40 | Missing entry answers 404 | Unknown memoryId | 404 for patch and delete |
| TC-41 | Disabled surface flagged distinctly | Memory switched off | Disabled-flagged 404, not a missing-entry 404 |
| TC-42 | Async setting gate honored | Promise-based enabled check | Gate awaits the setting before serving |
| TC-43 | Unreadable setting closes HTTP surface | Setting read throws | 503 availability-unknown answer |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-44 | Delete of an unknown entry | Reported as no deletion, never claimed as success |
| TC-45 | Non-string title in a patch body | 400 naming the type violation |
| TC-46 | Delete without scope resolution | Rejected before the store is touched |
| TC-47 | Read with neither memoryId nor title | Usage error naming the requirement |
| TC-48 | Unsupported tool action | Rejection naming the unsupported action |

## Test Infrastructure

- `packages/web/server/lib/agent-memory/runtime.test.js`
- `packages/web/server/lib/agent-memory/actions.test.js`
- `packages/web/server/lib/agent-memory/routes.http.test.js`
- `packages/web/server/lib/agent-memory/feature-flag.test.js`
- `packages/web/server/lib/agent-memory/threat-patterns.test.js`
- `packages/web/server/lib/agent-memory/project-resolution.test.js`
- `packages/ui/src/lib/agentMemoryApi.ts` has no dedicated test file; coverage flows through the HTTP route tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-30, TC-31, TC-41, TC-42, TC-43 |
| FR-3 | TC-3, TC-4 |
| FR-4 | TC-12, TC-13 |
| FR-5 | TC-14, TC-15, TC-16, TC-17 |
| FR-6 | TC-18, TC-19 |
| FR-7 | TC-12, TC-13, TC-22 |
| FR-8 | TC-25, TC-26, TC-27 |
| FR-9 | TC-28, TC-29 |
| FR-10 | TC-44 |
| FR-11 | TC-36, TC-37, TC-38, TC-39, TC-40 |
| FR-12 | TC-33 |
| FR-13 | TC-23, TC-24, TC-34, TC-35 |
| FR-14 | TC-32 |
| FR-15 | TC-20 |
| FR-16 | TC-24, TC-37, TC-46 |
| NFR-1 | TC-5, TC-6 |
| NFR-2 | TC-7, TC-8 |
| NFR-3 | TC-29, TC-38 |
| NFR-4 | TC-19 |
| NFR-5 | TC-13, TC-45, TC-47, TC-48 |
