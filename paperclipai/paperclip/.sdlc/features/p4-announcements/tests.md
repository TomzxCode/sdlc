---
title: "In-app announcements"
status: done
---

# Test Plan: In-app announcements

## Scope

Tests cover the shared manifest contract and eligibility, feed fetching with caching and backoff, animation allowlist validation, publisher staging and digest checks, board routes with durable dismissals, and the UI lifecycle from settling through optimistic dismissal to placement gating.
Out of scope: live remote feed content and production publishing runs.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-S1 | Empty feed and plain-text card parse | `{schemaVersion: 1, announcement: null}` and a minimal card | Null announcement and parsed card ID |
| TC-S2 | Unsupported route actions rejected | Six bad route paths (`/api/companies`, `//evil.test`, traversal, query, unknown, `javascript:`) | All fail schema validation |
| TC-S3 | Unsafe external URLs rejected | Non-URL, http, `javascript:`, credentialed HTTPS | All fail schema validation |
| TC-S4 | Unsafe image paths rejected | Traversal, absolute URL, root path, `.svg` extension | All fail schema validation |
| TC-S5 | Animation requires content-addressed HTML plus static fallback | Valid image plus animation pair, animation alone, four bad animation paths | Only the valid pair passes |
| TC-S6 | Unknown schema versions, oversized copy, and unknown fields rejected | `schemaVersion: 2`, 401-char description, five extra-field variants | All fail schema validation |
| TC-S7 | Expiration and minimum-version gating | Dated and versioned card against older, prerelease, unknown, and newer versions | Only adequate versions before expiry are eligible |
| TC-A1 | CSS keyframes and visual HTML/SVG preserved | Document with keyframes, styled div, inline SVG | Sanitized output keeps keyframes and viewBox |
| TC-A2 | Active and resource-loading markup rejected | Fourteen fixtures (script, onclick, anchor, form, meta refresh, base, iframe, img, link, foreignObject, xlink, animate, object, button) | Every fixture throws |
| TC-A3 | Empty, oversized, and invalid UTF-8 animation files rejected | Zero bytes, 128 KiB plus one, `0xff` byte | Every input throws |

Files: `packages/shared/src/announcements.test.ts`, `server/src/__tests__/announcement-animation.test.ts`

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-F1 | 404 is quiet empty content, drops stale ETags, recovers after cooldown | Served card, then 404, then restored card with controlled clock | Null during outage, no warning logged, recovery fetch omits If-None-Match |
| TC-F2 | Concurrent requests deduplicate, cache for an hour, revalidate with ETag | Fresh service with controlled clock | One fetch for concurrent reads, no refetch before one hour, revalidation sends ETag with `credentials: omit` |
| TC-F3 | Withdrawal, same-ID copy update, and new-ID discovery | Sequential feeds across cache windows | Corrected title served, withdrawal empties, new ID appears |
| TC-F4 | Invalid and unavailable feeds suppressed with failure cooldown | Five bad responses (bad JSON, schema 9, 64 KiB plus one, redirect, 503) | Null until cooldown, then recovery; one fetch per window |
| TC-F5 | Hung fetch bounded to three seconds | Never-resolving fetch with fake timers | Current resolves null after 3000 ms |
| TC-F6 | Disabled feed and invalid operator URLs never fetch | `enabled: false`, http URL, credentialed URL | Null from current, image, and animation with zero fetches |
| TC-F7 | Expiry enforced and version-incompatible content filtered | Expired card with advancing clock, card requiring version 2.0.0 | Expired card flips to null; incompatible card never serves |
| TC-F8 | Only the current digest-verified image is proxied and cached | Content-addressed PNG fixture | Wrong ID returns null, concurrent reads share one fetch on the feed host path |
| TC-F9 | Image digest mismatches rejected with retry cooldown | Manifest pointing at zero-digest path with wrong bytes | Null twice with only one asset fetch |
| TC-F10 | Validated animations deduplicated and cached on the configured host | Content-addressed HTML fixture on a mirror feed URL | Wrong ID returns null, concurrent reads share one fetch with `redirect: error` and text/html Accept |
| TC-F11 | Rejected animation assets fall back with retry cooldown | Four bad assets (script, wrong type, 404, oversized) | Null twice per asset with two total fetches while the card stays served |
| TC-P1 | Staging feeds stay separate from production and default to dry-run | Staging source directory and name | Staging keys, parsed args, production prefix, rejected bad prefixes and flags |
| TC-P2 | Content-addressed assets upload before the short-lived manifest | Image bytes with digest path, then mutated bytes | Asset key before manifest key, immutable cache control, five-minute manifest, SHA-256 error on change |
| TC-P3 | HTML animation fixtures validated with both assets before the manifest | Animated example versus meta-refresh fixture | Three content types in order; unsafe markup rejected as non-visual |
| TC-P4 | Withdrawal supported; symlinks and unsupported schemas rejected | Null manifest, symlinked dir, schema 2, extra array field | One file for withdrawal; each abuse case throws |
| TC-R1 | Empty remote announcement returns successful null for HTTP 200 and 404 | Null feed at both statuses | 200 with null body and `private, no-store` |
| TC-R2 | Animation served with sandbox network-denying CSP | Digest-pinned HTML animation fixture | 200 text/html with sandbox CSP, no-referrer, nosniff; wrong ID 404s |
| TC-R3 | Dismissals persist across restarts, browsers, and companies, isolated by user | Dismiss by alice, reread as alice and bob, dismiss under second company | Alice sees null, bob still sees the card, one audit row total |
| TC-R4 | Viewers and concurrent duplicates yield one row and one audit | Membership as viewer, five parallel dismissals | Five 204s, one dismissal row, one `announcement.dismissed` entry |
| TC-R5 | Dismissal rolls back when its audit cannot commit | Registered ID with an impossible company UUID | Dismiss throws and `isDismissed` stays false |
| TC-R6 | Dismissed ID never resurrects on copy change or rollback while a new ID appears | Dismissed ID with edited copy, then a fresh ID | Null for edited copy, new ID served, feed without registry entry serves null |
| TC-R7 | Local-board identity works without an auth user row | Implicit local board actor | Dismiss 204 and `isDismissed` true for `local-board` |
| TC-R8 | Invented IDs rejected without rows or audits | Three unknown IDs after a valid fetch | Three 404s, zero dismissal rows, zero audits, registry holds only the real ID |
| TC-R9 | Offline retries accepted for validated IDs after withdrawal and restart | Published ID, then withdrawn feed on a restarted service | Dismiss 204, `isDismissed` true, one audit row |
| TC-R10 | Anonymous, agent, and inaccessible-company callers rejected | None and agent actors, unknown company, extra body field | 401 and 403 per actor on all endpoints, 404 for unknown company, 400 for schema violation |

Files: `server/src/__tests__/announcement-feed.test.ts`, `server/src/__tests__/announcement-publisher.test.ts`, `server/src/__tests__/announcements-routes.test.ts`

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-H1 | Card settles before showing and never polls during uninterrupted work | Render, advance 3 s, advance one hour, change company prop | Card appears after settle, one fetch total, company change alone refetches nothing |
| TC-H2 | Card survives blur and focus without refetching | Settle, dispatch blur then focus, settle again | Card stable, one fetch, first signal unaborted |
| TC-H3 | Focus during settling does not restart the settle period | Render, advance 2.5 s, blur and focus, advance 0.5 s | Card appears on schedule with one fetch |
| TC-H4 | Dismiss hides immediately and survives remount plus copy edit | Settle, dismiss, unmount, remount with corrected copy, settle | Empty immediately, dismiss called once with company and signal, still empty |
| TC-H5 | Tab return refreshes: withdrawn card hides, new ID shows | Settle, hide and show with null feed, then with new ID | Empty after withdrawal, new ID after republish |
| TC-H6 | Returning tab withholds until the fresh check completes | Hide, return with pending fetch, focus, settle, resolve null | One additional fetch, empty throughout |
| TC-H7 | Late pre-hide response ignored after return | Pending fetch, hide (aborts), resolve late, return with new ID | Empty until the fresh fetch settles on the new ID |
| TC-H8 | Failed writes stay pending and retry on reconnect | Dismiss with failing API, go online | Failure callback with saved-locally true, pending then synced storage |
| TC-H9 | No cross-account leakage from a late fetch | Pending fetch, switch user, resolve old card | New account sees nothing |
| TC-H10 | Another tab's dismissal closes this tab's card | Settle, storage event for the card key | Card hides |
| TC-H11 | Broadcast dismissal honored without browser storage | Broken localStorage, broadcast message, hide and show cycle | Card hides, stays hidden, dismiss API called |
| TC-H12 | Unknown, disabled, and hidden-tab states withhold the card | Rejected fetch, disable, focus, hidden tab with re-enable | Empty in each state with no fetch when disabled or hidden |
| TC-H13 | Visible card expires on time | Card expiring in four seconds, advance one second past | Card shows then clears |
| TC-W1 | Identity, company, onboarding gates with local-board fallback | Unsettled identity, loading company, open onboarding, no user, local trusted mode | Hidden until ready; local-board identity enables in no-login mode |
| TC-W2 | Toasts and modal dialogs yield without dismissing | Toast present, then cleared, dialog opened, then removed | Hidden under toast and dialog, restored after, dismiss never called |
| TC-C1 | Animated media isolated with announcement-only controls | Rendered animated card with stubbed animation fetch | Sandboxed unfocusable iframe with CSP and alt label, one dismiss button, two links |
| TC-C2 | Reduced motion skips the animation fetch | Reduced-motion media query match | No fetch, no iframe, poster image present |
| TC-C3 | Failed animation HTTP keeps poster and actions usable | Animation fetch 404 and 503 | No iframe, poster present, dismiss works |
| TC-C4 | Pending animation fetch aborted on dismiss | Hanging animation fetch, unmount | Fetch signal aborted while poster stays |
| TC-C5 | Plain-text card is accessible with safe navigation and dismissal | Script-like title, link clicks, image error, Escape key, aux clicks | No script element, labelled region, noreferrer external link, image hides on error, button plus Escape plus primary aux clicks dismiss, context-menu click does not |

Files: `ui/src/hooks/useAnnouncement.test.tsx`, `ui/src/components/AnnouncementWell.test.tsx`, `ui/src/components/AnnouncementCard.test.tsx`

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Feed 404 after a served card | Quiet empty card with stale ETag dropped (TC-F1) |
| TC-E2 | Oversized manifest, asset, or animation | Bounded abort with cooldown and no partial content (TC-F4, TC-F11, TC-A3) |
| TC-E3 | Digest mismatch on proxied asset | Rejection with retry cooldown (TC-F9) |
| TC-E4 | Unsafe animation markup at publish and at serve time | Rejected by publisher validation and DOMPurify sanitizer (TC-P3, TC-A2) |
| TC-E5 | Concurrent duplicate dismissals | One row and one audit entry (TC-R4) |
| TC-E6 | Audit commit failure | Full rollback, dismissal not recorded (TC-R5) |
| TC-E7 | Offline dismissal of withdrawn but known ID | Accepted via registry with audit (TC-R9) |
| TC-E8 | Caller-invented dismissal ID | 404 with no row and no audit (TC-R8) |
| TC-E9 | Agent or anonymous caller | 403 or 401 on every endpoint (TC-R10) |
| TC-E10 | Reduced motion or animation fetch failure | Static poster stays usable (TC-C2, TC-C3) |

## Test Infrastructure

- Vitest suites with fake timers and controlled clocks for cache, cooldown, settle, and expiry windows.
- Embedded Postgres test database for route and dismissal durability tests.
- Mocked remote fetch fixtures with digest-pinned asset bytes.
- jsdom harness with a full localStorage stub, BroadcastChannel stubs, and visibility and online event dispatch.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-S1, TC-S6, TC-F4 |
| FR-2 | TC-F4, TC-F11, TC-A3 |
| FR-3 | TC-F1, TC-F2, TC-F4, TC-F5, TC-F6 |
| FR-4 | TC-S7, TC-F7, TC-H13 |
| FR-5 | TC-F8, TC-F9, TC-F10, TC-R2 |
| FR-6 | TC-A1, TC-A2, TC-C1, TC-C2, TC-C3, TC-C4, TC-R2 |
| FR-7 | TC-R3, TC-R4, TC-H4 |
| FR-8 | TC-R4, TC-R7, TC-R10 |
| FR-9 | TC-R3, TC-R4, TC-R5 |
| FR-10 | TC-R6, TC-R8, TC-R9 |
| FR-11 | TC-R1, TC-F1, TC-F6, TC-F7, TC-H5, TC-H12, TC-W1 |
| FR-12 | TC-H1, TC-H2, TC-H3, TC-H4, TC-H6, TC-H7, TC-H8, TC-H9, TC-H10, TC-H11, TC-H12, TC-W2 |
| FR-13 | TC-P1, TC-P2, TC-P3, TC-P4 |
| NFR-1 | TC-R10, TC-S2, TC-S3 |
| NFR-2 | TC-F5, TC-F6, TC-F1 |
| NFR-3 | TC-F2, TC-F8, TC-F10, TC-H1 |
| NFR-4 | TC-F4, TC-H12, TC-C3 |
| NFR-5 | TC-C1, TC-C2, TC-C5 |
