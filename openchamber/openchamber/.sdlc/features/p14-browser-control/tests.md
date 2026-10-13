---
title: "Browser Control"
status: done
---

# Test Plan: Browser Control

## Scope

Tests cover the broker request lifetime (publish, claim, resolve, timeout, abort), the provider routing (builtin versus extension, reset, surface lease, error mapping), the claim/result HTTP routes with per-route body parsing, and the client half (tab resolution, claim-then-act, sleeping tabs, snapshot tab listings, open-creates-tab).
Page-script behavior (snapshot caps, click replay, scroll settle) is covered alongside the client.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Broker resolves with the data the client posts back | `browser.snapshot` request plus `{ ok: true, data }` resolve | Waiting promise fulfills with the client data |
| TC-2 | Broker threads caller context, defaulting to unknown | Context with directory/sessionId, then a contextless call | First event carries both values, second carries nulls |
| TC-3 | First claim wins, settled claims refused | Two claims on one id, one claim on a settled id | First granted, rest refused |
| TC-4 | Unknown result ids settle nothing and report unmatched | Resolve with an unknown requestId | Returns false, no promise affected |
| TC-5 | Abort signal cancels the pending request | Aborted signal on `request()` | Rejects with status 499 |
| TC-6 | Service validates each `browser.*` action before the round trip | Invalid open/click/type/scroll/resize/inspect inputs | Usage error naming the missing or bad input, broker never called |
| TC-7 | Provider delegates to the broker for `builtin` | Setting `browserProvider: builtin` | `broker.request` called with action, parameters, and options |
| TC-8 | Provider proxies to the extension service with context | Extension-selected setting plus action | POST carries requestId, action, parameters, and context with open/action timeouts |
| TC-9 | Unservable extension resets to builtin and runs in-app | Paused, removed, or unapproved guest | Setting persisted to builtin, reset emitted, broker path runs |
| TC-10 | Surface held by the user refuses with 409 | `userControls` true for the guest | Action refused, nothing changed |
| TC-11 | Snapshot caps bound cost and report drops | Large page with thousands of nodes | At most 6000 text chars and 120 elements with drops reported |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-12 | Result route parses JSON and resolves the waiting request | Live Express app with a pending broker request | 200 `{ matched: true }` and the agent promise fulfills |
| TC-13 | Result route accepts snapshot-sized payloads | 2mb-limit route with a large snapshot body | Accepted and resolved, not a timeout |
| TC-14 | Client claims before acting and losers stay idle | Two subscribed clients, one request | Winner acts, loser posts nothing |
| TC-15 | Named-tab action runs in that tab regardless of the shown tab | Registered tabs in several projects | Action executes in the named tab, visible tab unchanged |
| TC-16 | `browser.open` without `tabId` opens a background tab | Registered opener, no target tab | New session-owned tab opens, answer carries its `tabId`, no tab switch |
| TC-17 | Sleeping tab wakes on demand | Sleeping-registered tab named by an action | Tab wakes, pane attaches, action runs |
| TC-18 | `browser.capture` returns a server-side file path | Successful capture result | Image written beside the project, caller receives the path not base64 |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-19 | No client listening | Immediate 503 describing the desktop capability, never a full-timeout wait |
| TC-20 | Claimer disappears after claiming | Request still times out with 504, never assumed success |
| TC-21 | Result arrives after the timeout | Accepted with `matched: false`, not an error |
| TC-22 | Settings or catalog read fails | 503, nothing runs anywhere, provider choice unchanged |
| TC-23 | Provider sends but never answers | Agent told the action may or may not have run and to read the page first |
| TC-24 | Provider answers a non-result shape or non-200 status | Reported as unknown page state with nothing assumed |
| TC-25 | Session with no usable tab | Agent receives the no-tab error listing the tabs it could name |
| TC-26 | Unknown `tabId` with no holder | Delayed claim then "no such tab" error pointing at `browser.snapshot` |
| TC-27 | Missing claim `requestId` or result body | 400 usage error from the route |

## Test Infrastructure

- `packages/web/server/lib/browser-control/broker.test.js` (bun:test, injectable emitRequest/createId/timers).
- `packages/web/server/lib/browser-control/provider.test.js` (bun:test, stubbed broker/settings/catalog/service-proxy/surface-control).
- `packages/web/server/lib/browser-control/routes.test.js` (vitest plus supertest against a real Express app to prove per-route body parsing).
- `packages/ui/src/lib/browser/controlClient.test.ts` (bun:test with mocked runtime-fetch and event subscription, module-global registration unwound per test).
- `packages/ui/src/lib/browser/pageActions.test.ts` (page-script builders: snapshot caps, selectors, scroll settle).
- Adjacent, not owned here: `contract.test.ts` covers the general browser surface contract, and `openchamber-control/service.test.js` covers `browser.*` validation and capture persistence from the caller side.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-3, TC-14 |
| FR-3 | TC-19 |
| FR-4 | TC-4, TC-12, TC-21 |
| FR-5 | TC-3, TC-27 |
| FR-6 | TC-6 |
| FR-7 | TC-7, TC-8 |
| FR-8 | TC-9 |
| FR-9 | TC-22 |
| FR-10 | TC-23 |
| FR-11 | TC-2, TC-8 |
| FR-12 | TC-13 |
| FR-13 | TC-15, TC-16, TC-17, TC-25, TC-26 |
| FR-14 | TC-15, TC-25 |
| FR-15 | TC-10 |
| NFR-1 | TC-5, TC-20 |
| NFR-2 | TC-18 |
| NFR-3 | TC-11, TC-13 |
| NFR-4 | TC-16, TC-17 |
