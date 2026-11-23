---
title: "Session Assist (Recap and Suggestions)"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Session Assist (Recap and Suggestions)

## Scope

This plan records the test files that currently cover session assist generation, context reading, metadata freshness, event delivery, and pending-assist directory handling.
It covers the server runtime, the v2 context reader, the client freshness check, and the SSE event path.
It does not claim coverage for the recap spacer and suggestion chip components, the settings UI toggle, or a 5 second generation deadline, which have no tests in the current tree.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `packages/web/server/lib/session-assist/context.test.js` verifies that paging stops at three human turns. | A v2 newest-first message page with tools and injected instructions. | Only checked human turns appear in the context. |
| TC-2 | The same file finds the real user across page boundaries and compaction. | Compaction and attachment records around a user request. | The request is attached to the right user turn. |
| TC-3 | The same file retains interrupted requests as progress rather than completed turns. | An assistant record with `finish: 'tool-calls'`. | The turn is not treated as finished. |
| TC-4 | The same file bounds retrieval and excerpts from both ends. | A long answer and a long quote in a message page. | The comment and the conclusion survive within the model budget. |
| TC-5 | The same file refuses to invent a user for an orphaned answer. | A page holding an answer without a matching request. | No completed turn is produced. |
| TC-6 | The same file skips unfinished, failed, compaction, and user tails and names the newest content record of a newest-first page. | Mixed v2 record types and ordering. | Only usable records feed the prompt. |
| TC-7 | `packages/ui/src/lib/sessionAssistMetadata.test.ts` checks client freshness of stored assists. | An assist generated after the last turn, a later turn, a recap-only assist, and a reverted session. | The current assist is returned when fresh and `null` is returned when a later turn or revert retires it. |
| TC-8 | `packages/web/server/lib/session-work/runtime.contract.test.ts` checks the assist context type contract. | A page with a checked final assistant and a snapshot. | `assistant.text` is a string, `changedFiles` is a `Set` or `null`, and model fields stay undefined. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | `packages/web/server/lib/session-assist/runtime.test.js` verifies that no work happens while no assist store is injected. | An idle session status event with no `persistSessionAssist`. | No URL builder or small model service call is made. |
| TC-10 | The same file generates and saves an assist for a turn closed by a v2 idle marker. | An idle event, a stubbed session and message API, and an injected small model service. | Recap, suggestion, and `forMessageID` are persisted, and a new busy event clears the assist once. |
| TC-11 | The same file checks model resolution on local and hosted endpoints. | `describeSmallModel` reporting session-model, settings, and session-provider-small sources with local or hosted endpoints. | Local session models are skipped, a different small model or a hosted session model is used, and the skip is logged once. |
| TC-12 | The same file checks the turn-end gate and lineage handling. | A gate ruling out both fields, a known subsession, and a gate answer arriving after a new turn. | No timer is armed, no service is called, and a late gate answer is dropped. |
| TC-13 | The same file checks pending announcements. | Idle and busy events with a stubbed session API and injected store. | A pending change is announced at turn end and cleared after a write, a failure, or a new turn. |
| TC-14 | The same file checks generation failure handling. | A small model call that throws an Error with status and code, and a tagged non-Error SDK rejection. | Failures are logged with their cause, no assist is persisted, and the pending wait ends. |
| TC-15 | The same file checks the settings gate at runtime. | `getTargets` returning both recap and suggestion disabled. | No pending announcement is made. |
| TC-16 | `packages/ui/src/sync/event-pipeline.test.ts` passes the server's recap wait announcements through typed. | `openchamber:session-assist` events with a directory and with a null directory. | Typed `openchamber.session-assist` events are emitted for both pending and settled states. |
| TC-17 | `packages/ui/src/lib/openchamberEvents.test.ts` dispatches the session announcements an SSE main stream never carries. | An `openchamber:session-assist` payload on the mocked event source. | A `openchamber.session-assist` control event reaches subscribers. |
| TC-18 | `packages/ui/src/sync/__tests__/location-release.test.ts` checks pending-assist directory holds. | A pending assist event, a settled event, and a wait whose end never arrives. | The directory stays busy while the assist is pending and becomes free when it settles or ages out. |
| TC-19 | `packages/ui/src/sync/persist-cache.test.ts` checks cache pruning for session metadata. | A full session fixture carrying an assist recap in `metadata.openchamber.assist`. | The cached session keeps work metadata but drops the assist metadata. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-20 | No end-to-end test file drives a full 60 second idle-to-generation flow through a live server and rendered chat UI. | None. | No end-to-end coverage is recorded for this feature. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-21 | A session is archived before or during generation. | No context is loaded, no model is called, and a result in flight is discarded. |
| TC-22 | A new turn or busy status arrives while generation or the final archive check is running. | The timer clears and the generated result is not written. |
| TC-23 | Recap and suggestion are both ruled out by the turn-end gate. | Nothing is announced and no timer is armed. |
| TC-24 | A known subsession goes idle. | No gate call, timer, or read happens. |
| TC-25 | Small model resolution fails on an unauthenticated provider. | The generation failure is logged, no assist is persisted, and the pending wait ends. |
| TC-26 | A later user turn or a revert is present in session metadata. | The client hides the stored assist. |
| TC-27 | A pending assist never reports completion. | The directory hold expires after the maximum pending age. |

## Test Infrastructure

- Vitest runs the server tests with fake timers and a short `QUIET_MS` instead of the production 60 second delay.
- The runtime tests inject a persistence seam, a small model service, a turn-end gate, and session lineage, and stub global `fetch` with v2 session and message pages.
- The context tests build v2 message pages directly and use an `AbortController` signal.
- Bun test runs the client metadata test with a minimal `Session` fixture.
- The UI event tests use Bun test with a mocked event source and fake clock where needed.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2, TC-3, TC-4, TC-5, TC-6, TC-9, TC-10, TC-13, and TC-20 |
| FR-02 | TC-11 |
| FR-03 | TC-7 checks freshness only, with no test of the recap spacer rendering. |
| FR-04 | TC-7 checks suggestion freshness only, with no test of the tappable chip rendering. |
| FR-05 | TC-7, TC-10, TC-12, TC-13, TC-18, and TC-26 |
| FR-06 | TC-15 covers the runtime `getTargets` gate, with no test of the settings UI toggle. |
| FR-07 | TC-12, TC-13, TC-18, TC-22, and TC-27 |
| NFR-01 | TC-20 records that no 5 second deadline test exists. |
| NFR-02 | TC-14, TC-21, TC-23, and TC-25 |
