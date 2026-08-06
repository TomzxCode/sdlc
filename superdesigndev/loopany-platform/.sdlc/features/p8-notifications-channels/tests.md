---
title: "Notifications & Channel Bindings"
status: done
---

# Test Plan: Notifications & Channel Bindings

## Scope

Testing channel CRUD with the shared form and live test ping, exec-only notification rules, streak-based anti-spam, the deferred offline message with dedup, the autopause circuit breaker, the webhook guard SSRF containment, and the injectable notifier seam. Out of scope: the onboarding wizard flow and dashboard channel UI chrome.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Shared ChannelAddForm is used by both binding surfaces | Notifications modal + onboarding live step | Both render the same form component (single source) |
| TC-2 | createChannel runs a live test ping | Valid + invalid channel | Ping ok → saved; ping error → rejected |
| TC-3 | listChannels never returns tokens | Channel list with credentials | Payload has no token fields |
| TC-4 | Only exec runs notify | Exec success/failure + evolve/edit outcomes | Exec → push; evolve/edit → no user-facing notification |
| TC-5 | Failure streak notifies at 1 then every 5th | Series of exec failures | Notifications at streak 1, 6, 11, ...; success resets |
| TC-6 | skipped runs are transparent to the streak | streak with skipped runs interleaved | Count keys off phase `error` only; skipped never counted |
| TC-7 | notify:"never" silences everything | Loop with notify never + failure/autopause | No push at all, including the autopause note |
| TC-8 | Autopause subsumes the failure alert | Streak reaches threshold | `enabled=false` + unschedule + ONE note; re-enable resumes |
| TC-9 | Offline deferred exec run gets one calm message | Genuinely offline machine | One `deferredMessage`, deduped by the DEFERRED_LABEL stamp |
| TC-10 | Asleep machine is silent | Machine seen < 6h ago | No deferred message |
| TC-11 | Webhook guard rejects SSRF targets | Loopback/metadata/private-range/unsupported scheme | Rejected before any outbound request |
| TC-12 | Notifier is injectable | Gateway with a spy notifier | Tests observe pushes without network |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Streak threshold configured to 0 | Autopause disabled entirely |
| TC-14 | Interrupted running run vs skipped scheduled run | Failure copy names sleep as the likely cause, distinguishes the two |
| TC-15 | Deferred run claimed at next poll | No duplicate message; supersede retires as outcome `skipped` |
| TC-16 | Delete channel mid-delivery | Delivery handles the missing channel gracefully |

## Test Infrastructure

- vitest; gateway tests use an injected spy notifier (no network).
- Webhook guard tests run against a resolver-seam over private/loopback/metadata targets.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-4 |
| FR-3 | TC-5, TC-6 |
| FR-4 | TC-7 |
| FR-5 | TC-9, TC-10, TC-15 |
| FR-6 | TC-8, TC-13 |
| FR-7 | TC-11 |
| FR-8 | TC-12 |
| NFR-1 | TC-3 |
| NFR-2 | TC-11 |
| NFR-3 | TC-14 |
