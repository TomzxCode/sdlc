---
title: "Issue trackers and tracked items"
status: done
---

# Test Plan: Issue trackers and tracked items

## Scope

Tests cover the provider-neutral tracker registry and routes, the Linear adapter over stubbed Linear libraries, extension tracker attachment and connect errors, the web client's neutral wire and legacy fallback, and the server and client halves of tracked items.
Item parsing, identity strings, interest caps, cadence, backoff, persistence, link matching, project mapping, session origin rules and the Settings cards are covered in adjacent suites.
Starting a session from an issue is owned by FEAT-0022-github-issue-pr-starters and is not retested here.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | The registry serves the built-in descriptor as plain JSON | Default registry construction | Linear descriptor with frozen arrays and no implementation load |
| TC-2 | The registry refuses invalid registrations | Malformed, reserved, duplicate, source-control and ext- built-in ids | Error naming the id and null for unknown ids |
| TC-3 | The registry loads once and retries failures | Concurrent implementation requests, then a failed and repeated load | One loader call for concurrent requests and a fresh attempt after failure |
| TC-4 | The registry follows extension attach and detach | A valid ext- entry attached, replaced and detached | Built-ins stay first and fixed, and a detached id reads as unknown |
| TC-5 | Linear state, priority and filter mapping is complete | Every Linear state type, priority 0 to 4 and each descriptor filter | Neutral categories, priorities and Linear statuses, with duplicate as canceled |
| TC-6 | Linear accounts never expose tokens | Stored workspaces with users and organizations | Tracker accounts with ids, names and current flag only |
| TC-7 | Linear issues map to neutral items | Issue with state, priority, labels, team, parent and sub-issue progress | Summary with category, urgent priority, container, parent and progress flags |
| TC-8 | Linear get includes comments and children | Full issue with comments and ordered sub-issues | Description, authors, children in provider order and childrenMore |
| TC-9 | Linear live summaries carry category and legacy type | Issue state with a known type and an unmapped type | Category set, with unmapped state falling back to todo and type kept for older clients |
| TC-10 | Linear URL matching follows the descriptor | URL table with www host, path variants and other hosts | Same upper-case identifier on both sides and null for a non-match |
| TC-11 | Tracked items parse and key legacy shapes | Kindless Linear record, instance-less GitHub record, work item and pull request | Modern shapes under the same keys as the legacy records |
| TC-12 | Tracked item parsing drops invalid entries | Bad identifier, unregistered source-control provider, unsupported discussion | Only valid items survive, independently of each other |
| TC-13 | The client model reads records by state category | Server record with category, legacy type-only state and a mismatch of key and item | Records restore, legacy state maps to a category and invalid records drop alone |
| TC-14 | Client interest caps visible items first | Earlier background follower plus more visible items than the cap | On-screen items fill the cap and earlier declarations keep priority |
| TC-15 | Client interest survives reconnect and 409 | Connection ready, changed interest, reconnect and an unknown-connection reply | One union send per change, a resend after reconnect and a wait after 409 |
| TC-16 | Server persistence keeps and bounds cached states | Version 1 file with extra state fields, invalid records and expired entries | Arbitrary state fields survive, invalid records drop and saved data uses a sibling temp file |
| TC-17 | Descriptor validation and URL matching on the client | Valid, malformed, reserved and repeated descriptors plus extension link templates | Only valid descriptors remain and URLs match through the served patterns |
| TC-18 | Tracker helpers resolve context, origin and mapping | Item with comments, desktop loopback origin and container with a path | Neutral context text, local session origin and container path before default |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-19 | Tracker routes serve descriptors and auth lifecycle | Real Express app with a stub tracker registry | Providers listed, and status, start, activate and disconnect forwarded by provider id |
| TC-20 | Tracker routes check list options against the descriptor | Descriptor with a limited filter set | Defaults applied, valid filters forwarded and unknown or unsupported filters answered 400 |
| TC-21 | Tracker routes read and write items and preferences | Stub implementation with states, mapping, preferences and session status | Neutral bodies forwarded, disconnected answered 200 and capability gaps answered 404 |
| TC-22 | Tracker routes bound input and report provider errors | Over-long token, username, instance, client and path fields plus a provider error | 400 before the implementation is asked and 400 or 500 with the expected body |
| TC-23 | Extension tracker routes carry their own connect errors | Stub extension tracker with token, OAuth client and callback | Connect info with origin, owner codes on failure and a public callback page |
| TC-24 | Tracker routes over the real Linear tracker stay disconnected without a workspace | Empty Linear data directory | Auth status and item reads answer connected false without a Linear call |
| TC-25 | Tracked-items routes replace interest and answer known states | Live service with a known state | 200 with states, 409 for an unknown connection and 400 for malformed bodies |
| TC-26 | Tracked-items service batches and publishes only moved states | Two visible connections, one showing an item | One read per batch group and a changed event only to the showing connection |
| TC-27 | Tracked-items service groups by host and account | GitHub items on github.com and an enterprise host plus a bound account | Separate batches per host and account and no shared cooldown |
| TC-28 | Tracked-items service waits through hidden windows | Visible client, hidden client and a returning client | No polling while hidden and a catch-up read when it returns |
| TC-29 | Tracked-items service handles server followers and mutations | Follower with no window, merge, local provider change and explicit item refresh | Follower reads continue, merged items stop, provider refresh reads open items and single refresh targets one item |
| TC-30 | Tracked-items service keeps state after failure and rid of vanished items | Failing reader, rate limit and a provider that stops answering | Last states stay, backoff grows and a vanished item state becomes null |
| TC-31 | Tracked-items service reads work items on state-based cadence | Open, settled and refreshed work items | Open at 2 minutes, settled at 5 minutes and an explicit refresh by identifier |
| TC-32 | Web tracker API selects the wire per runtime | Stubbed fetch and runtime key | Providers read once per runtime, legacy server detected and neutral calls mapped to legacy routes |
| TC-33 | Web tracker API preserves rich auth answers | Extension status with written-off accounts and a connect block | All fields reach the UI and a failed or unreadable provider list throws |
| TC-34 | Settings card follows capabilities and connection state | Stub API and rendered TrackerSettings | Browser sign-in and settings shown only where offered, account switch where supported and disconnect targets the shown tracker |
| TC-35 | Extension Settings card connects with a token | Extension descriptor with a user instance and connect info | Instance, token and client forms shown and connect result reported in the tracker's name |

## End-to-end Tests

None.
The Settings tests render real components with a stubbed runtime API, and the route suites use real Express apps with stub providers.
There is no dedicated browser flow owned by this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-36 | A tracker id overlaps a source-control id or reserved id | Registration throws at startup and the client registry leaves that id out |
| TC-37 | An extension tracker load fails or its service misses a deadline | The load is retried later and an unavailable answer writes off no account and changes no state |
| TC-38 | A public OAuth callback has a missing, expired or reused state | No account is attached and the callback page reports a failed sign-in |
| TC-39 | A `TrackerRouteError` and a provider error with status and code arrive at the same route | The route error keeps its own code and the provider error answers 500 |
| TC-40 | A Linear GraphQL 401 or invalid grant is seen | Only that workspace is cleared and status falls back to another workspace or disconnected |
| TC-41 | Session comments are disabled or the session origin is loopback | No comment is posted and the answer says why |
| TC-42 | A session starts before the tracker list arrives or a tracker leaves the registry | The post waits for the list within a bound and a detached tracker's runtime is stopped |
| TC-43 | Interest names a closed connection or an oversized set | 409 asks for a new connection id and an oversized set is refused rather than truncated |
| TC-44 | A server listener throws while states are broadcast | The error is logged and other listeners and the refresh continue |
| TC-45 | A runtime has no tracker API or its list fetch fails | Tracker UI hides or keeps the last held list and retries with a growing wait |
| TC-46 | A malformed or expired persisted record restores | Only that record drops and current records win over restored ones |
| TC-47 | An item's provider no longer answers a state | The state is null rather than a guessed closed state and the item keeps its identity |

## Test infrastructure

- `packages/web/server/lib/trackers/registry.test.js` (bun:test with injected entries and extension attachments).
- `packages/web/server/lib/trackers/routes.test.js` (supertest against an Express app with a stub registry, plus real built-in and extension trackers).
- `packages/web/server/lib/trackers/session-status.test.js` and `session-status-runtime.test.js` (event hub fan-out and runtime lifetime).
- `packages/web/server/lib/trackers/extension-*.test.js` and `route-error.test.js` (catalog reconciliation, accounts, OAuth, adapter and error codes).
- `packages/web/server/lib/linear/tracker.test.js` with `issues.test.js`, `mapping.test.js`, `status.test.js`, `auth.test.js`, `oauth.test.js`, `teams.test.js` and `parse.test.js` (Linear adapter and provider libraries with stubbed GraphQL).
- `packages/web/server/lib/tracked-items/service.test.js`, `routes.test.js`, `persistence.test.js` and `readers.test.js` (injectable readers, timers, send function and file system, with item parsing covered in `service.test.js`).
- `packages/web/src/api/trackers.test.ts` (bun:test with stubbed fetch and runtime keys).
- `packages/ui/src/lib/trackedItems/model.test.ts` and `interest.test.ts` (record parsing, keys and interest union).
- `packages/ui/src/lib/trackers/*.test.ts` (registry, descriptor, URL matchers, item context, session origin and project mapping).
- `packages/ui/src/components/sections/integrations/TrackerSettings.test.tsx` (rendered Settings card with a stubbed tracker API).

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-3, TC-4, TC-19, TC-36 |
| FR-2 | TC-19, TC-22, TC-23, TC-34, TC-35, TC-38, TC-40 |
| FR-3 | TC-7, TC-8, TC-20, TC-21, TC-22 |
| FR-4 | TC-18, TC-21, TC-34 |
| FR-5 | TC-18, TC-21, TC-41, TC-42 |
| FR-6 | TC-5, TC-6, TC-7, TC-8, TC-9, TC-10, TC-24, TC-40 |
| FR-7 | TC-9, TC-30, TC-31, TC-47 |
| FR-8 | TC-32, TC-33 |
| FR-9 | TC-4, TC-23, TC-37, TC-42 |
| FR-10 | TC-14, TC-15, TC-25, TC-26, TC-43, TC-44 |
| FR-11 | TC-11, TC-12, TC-13 |
| FR-12 | TC-26, TC-27, TC-28, TC-29, TC-30, TC-31 |
| FR-13 | TC-13, TC-16, TC-46 |
| FR-14 | TC-17, TC-34, TC-35, TC-45 |
| NFR-1 | TC-6, TC-23, TC-34, TC-38 |
| NFR-2 | TC-3, TC-30, TC-33, TC-37, TC-45 |
| NFR-3 | TC-14, TC-26, TC-27, TC-31, TC-43 |
| NFR-4 | TC-10, TC-11, TC-13, TC-32 |
| NFR-5 | TC-12, TC-20, TC-26, TC-44, TC-47 |
