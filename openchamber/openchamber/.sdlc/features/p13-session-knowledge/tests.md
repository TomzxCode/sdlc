---
title: "Session Knowledge"
status: done
---

# Test Plan: Session Knowledge

## Scope

Tests cover the knowledge runtime's owed-state decision, signature construction, text assembly, pin and delivery recording, failure isolation, the memory switch, and flagged-entry withholding.
Route-level and sender-level behavior (pending, summary, pin, delivered endpoints; UI, queue, session-route, and compaction senders) is covered indirectly through consumer suites.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tool-gated link guidance is told even with nothing else to tell | Linking on, empty pins and memory | Text equals link plus ask guidance, signature `l:on\|w:ask`, second resolve owes nothing |
| TC-2 | Link and worktree guidance stay out without the tool or on check failure | Linking off or throwing | Text omits guidance and move rule, empty input builds empty text and signature |
| TC-3 | Worktree rule asks by default and on unreadable setting | Linking on, setting unset, false, or throwing | Text carries the ask form with signature `l:on\|w:ask` |
| TC-4 | Worktree auto form re-sends the rule on setting flip | Prior signature `l:on\|w:ask`, setting true | Text carries the auto form with signature `l:on\|w:auto` |
| TC-5 | Owed block carries pinned notes, plan bodies, and memory index | Pinned note, plan, and memory entry | Text contains note body, plan title and body, and memory title |
| TC-6 | Memory is indexed by title never by body | Memory entry with distinct body | Text omits the full body text |
| TC-7 | Unpinned notes and plans stay out | Pin sets excluding stored items | Text omits the unpinned bodies |
| TC-8 | Empty signature round-trips to nothing owed | Fresh resolve then resolve with its signature | Second text is empty with identical signature |
| TC-9 | Edited note and new memory change the signature | Revision bumps and added entries | Recomputed signatures differ, order-insensitive for identical sets |
| TC-10 | Empty memory store still tells when to save | Both scopes loaded and empty | Text states save guidance plus nothing-stored marker, then owes nothing |
| TC-11 | Failed memory scope is not called empty | One scope failed | Text states save guidance without the nothing-stored marker |
| TC-12 | Broken memory store still delivers pins | Memory read throwing, pins present | Text contains the pinned note body |
| TC-13 | Failed scope entries are left out | Failed global scope with entries | Text omits the failed-scope titles |
| TC-14 | Unreadable plan is marked not dropped | Plan read throwing | Text contains plan title plus content-unavailable marker |
| TC-15 | Broken project context still delivers memory | Context read throwing | Text contains the memory title |
| TC-16 | Memory off leaves memory out and nothing pinned owes nothing | Memory disabled | Text omits memory, empty pins yield empty signature and text |
| TC-17 | Pins are isolated per session and pin changes clear delivery | Metadata stub with prior signature | Pin returns merged set, patch carries new pins plus cleared signature |
| TC-18 | Delivery records as a merge patch and readers handle missing metadata | Record call, empty or null sessions | Patch carries only the signature, readers return empty values |
| TC-19 | Missing metadata store raises plainly | Runtime without store seams | `setPin` and `recordDelivered` reject with a store error |
| TC-20 | Oversized block is cut and marked | 20000-character note body | Text stays within budget and contains the truncation marker |
| TC-21 | Flagged memory is withheld from the block | Mixed clean and flagged entries | Text contains the clean title and omits the flagged title |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-22 | UI send attaches knowledge and reports after resolve | Session UI store with stubbed knowledge endpoints | Synthetic part sent with the message, delivery reported only after acceptance |
| TC-23 | Queued server prompt carries and records knowledge | Message-queue runtime with knowledge stub | Synthetic preamble admitted before the prompt, signature recorded after acceptance |
| TC-24 | Session-route dispatch carries and records knowledge | Session routes with knowledge stub | Prompt carries the block and delivery is recorded on success |
| TC-25 | Compaction tick re-sends knowledge with pinned messages | Context-obligatory runtime with knowledge stub | Combined synthetic turn posted and cursor plus signature merge-patched |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-26 | Knowledge endpoints unreachable or failing | Send proceeds without the block, panel shows nothing |
| TC-27 | Delivery report in flight when the next send starts | Next send awaits the report so the block is not carried twice |
| TC-28 | Rejected send carrying the block | Nothing recorded, retry carries the block again |
| TC-29 | Session directory under the chats root | Context and memory resolve to the chats root owner |
| TC-30 | Draft session with no id yet | Pending endpoint treats everything as still owed |

## Test Infrastructure

- `packages/web/server/lib/session-knowledge/runtime.test.js` (29 tests, bun:test, in-memory metadata stub plus stubbed context, memory, and settings seams)
- `packages/web/server/lib/openchamber-sessions/routes.test.js` (session-route knowledge stub)
- `packages/web/server/lib/message-queue/runtime.test.js` (queue knowledge stub)
- `packages/ui/src/sync/session-ui-store.test.js` (UI attach-and-report flow with stubbed knowledge endpoints)
- `packages/ui/src/sync/opencode-startup-gate.test.ts` (startup hold with knowledge fetch stubs)
- `packages/ui/src/stores/useMultiRunStore.test.ts` (multi-run knowledge mock)

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-5, TC-6, TC-7 |
| FR-2 | TC-7, TC-17 |
| FR-3 | TC-8, TC-18 |
| FR-4 | TC-8, TC-9 |
| FR-5 | TC-8, TC-30 |
| FR-6 | TC-24, TC-28 |
| FR-7 | TC-22, TC-23, TC-24, TC-25 |
| FR-8 | TC-6, TC-10, TC-11 |
| FR-9 | TC-12, TC-13, TC-14, TC-15, TC-21 |
| FR-10 | TC-29 |
| FR-11 | TC-20 |
| FR-12 | TC-25 |
| FR-13 | TC-26, TC-27 |
| FR-14 | TC-1, TC-2, TC-3, TC-4 |
| NFR-1 | TC-22, TC-26 |
| NFR-2 | TC-24, TC-28 |
| NFR-3 | TC-25 |
| NFR-4 | TC-21 |
