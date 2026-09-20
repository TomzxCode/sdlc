---
title: "In-app announcements"
status: done
---

# Requirements: In-app announcements

## Overview

Board operators see at most one announcement card fed by a versioned remote JSON manifest.
The instance validates and caches the manifest, proxies its media under a strict sandbox, and stores per-user dismissals as instance-wide preferences.
Dismissal is idempotent, survives copy edits to the same announcement ID, and never resurrects once dismissed while a new ID appears normally.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator (any role, including viewer) | See the current announcement and dismiss their own card |
| Feed operator | Publish one validated announcement via the remote manifest |
| Agent caller | Explicitly denied announcement access |
| Paperclip user | Dismissal follows their account across companies on the instance |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall fetch a versioned remote manifest (`schemaVersion: 1`) from a configured HTTPS URL without credentials, query, or fragment, and validate it with strict schemas. |
| FR-2 | Must | The system shall enforce size caps (manifest 64 KiB, image 2 MiB, animation 128 KiB) with streaming bounded reads, content-type checks, and no redirects. |
| FR-3 | Must | The system shall cache the manifest for one hour, cool down fetch failures for 15 minutes, revalidate with ETag, treat 404 as quiet empty content (dropping the stale ETag), bound each fetch to 3 seconds, and deduplicate concurrent refreshes. |
| FR-4 | Must | The system shall serve the current announcement only when eligible (not expired and meeting `minimumPaperclipVersion` numerically, where a prerelease of the minimum is not yet that release), and return null otherwise. |
| FR-5 | Must | The system shall proxy only the current announcement's content-addressed image/animation assets, verifying the SHA-256 digest embedded in the asset path, caching bytes in one bounded slot per media kind, and cooling down asset failures. |
| FR-6 | Must | The system shall validate animations as visual-only HTML/CSS/SVG through an allowlist sanitizer, serve them as `text/html` with a sandbox CSP plus `nosniff` and `no-referrer`, re-apply the CSP inside the client `srcdoc` iframe sandbox, and honor reduced-motion with the static image fallback. |
| FR-7 | Must | The system shall persist per-user dismissals keyed by `(userId, announcementId)` as an instance-wide preference, idempotently, so concurrent duplicate dismissals store one row and one audit entry. |
| FR-8 | Must | The system shall restrict announcement writes to an authenticated board user context, deny anonymous and agent callers, and allow viewers to dismiss their own card with company read membership as audit context. |
| FR-9 | Must | The system shall audit each new dismissal transactionally as `announcement.dismissed` with the supplied company's context, and roll back the dismissal row if the audit cannot commit. |
| FR-10 | Must | The system shall maintain an instance-level publication-ID registry of validated feed IDs, accept offline retries for known IDs after withdrawal or restart, and reject caller-invented IDs with 404 without storing a dismissal row or audit entry. |
| FR-11 | Must | The system shall render nothing when the feed is disabled, empty, withdrawn, expired, version-incompatible, or dismissed, and mark announcement responses `private, no-store`. |
| FR-12 | Should | The client shall dismiss optimistically with per-user `pending`/`synced` local entries, retry failed writes on reconnect, synchronize across tabs, settle before showing, revalidate on tab return, expire a visible card on time, and suppress the card under modals, toasts, or onboarding. |
| FR-13 | May | Publisher tooling shall keep named staging feeds separate from production, default to dry-run, upload content-addressed assets before the short-lived manifest, and reject symlinks, digest mismatches, and unsafe animation markup. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Dismissal audit context shall validate company membership, returning 404 for unknown or inaccessible companies and 400 for strict-schema violations. |
| NFR-2 | Must | Security | The feed fetch shall be SSRF-guarded with timeouts, never follow redirects, never send credentials, and never log remote content or operator URLs. |
| NFR-3 | Should | Performance | Media caches shall stay bounded (one slot per kind, shared across board users), concurrent asset requests shall be deduplicated, and the client shall not poll during uninterrupted work. |
| NFR-4 | Should | Availability | Feed, asset, and animation failures shall degrade to an absent card without breaking the board or surfacing error popups. |
| NFR-5 | Should | Accessibility | The card shall expose a labelled region with a keyboard-accessible dismiss control, hide the decorative animation from assistive technology behind a labelled poster, and skip animation fetch under reduced motion. |

## Constraints

- Announcement IDs match `^[a-z0-9][a-z0-9-]{0,95}$`.
- Route actions are limited to an allowlist of stable board pages, and external actions require credential-free HTTPS URLs.
- An animation requires a static fallback image.
- Dismissals carry no company scope, while their audit context still validates company membership.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Fetch and validate the versioned manifest
      Given a configured HTTPS feed URL without credentials, query, or fragment
      When the service refreshes the feed
      Then a schemaVersion 1 manifest with a valid announcement is accepted and anything else is rejected
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Enforce size and type bounds
      Given a manifest or asset response exceeding its byte cap or content type
      When the service reads the response
      Then the fetch is aborted with an error and the board sees no card content from it
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Cache, revalidate, and cool down
      Given a fetched manifest with an ETag
      When the hour cache expires or a fetch fails or the feed 404s
      Then revalidation sends If-None-Match, failures cool down for 15 minutes, and a 404 quietly empties the card without resurrecting stale content
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Serve only eligible announcements
      Given a manifest announcement with an expiry or minimum version
      When the current announcement is requested past expiry or below the installed version
      Then the service returns null
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Proxy only current digest-verified assets
      Given the current announcement with content-addressed media paths
      When media is requested for a stale ID or a digest mismatch
      Then the service returns 404 or null and cools down retries while valid bytes stay cached
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Sandbox animation delivery
      Given an announcement with a validated animation
      When the animation endpoint is requested
      Then it responds with sandboxed CSP, nosniff, and no-referrer headers and the client renders it in a sandboxed srcdoc iframe or falls back to the poster under reduced motion
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Idempotent dismissal
      Given a visible current announcement
      When the same user dismisses it five times concurrently
      Then one dismissal row exists and the card stays hidden for that user only
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Board-only writes
      Given anonymous, agent, and viewer-board callers
      When each calls the dismiss endpoint
      Then anonymous gets 401, agent gets 403, and a viewer with company membership gets 204
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Transactional audit
      Given a new dismissal
      When the activity write cannot commit
      Then the dismissal row is rolled back and the announcement is not marked dismissed
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Registry allows retries and rejects invented IDs
      Given a previously published announcement ID withdrawn from the feed
      When the user dismisses the known ID offline and then an invented ID
      Then the known ID returns 204 and the invented ID returns 404 with no stored row or audit
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Empty states render nothing
      Given a disabled feed or an empty, withdrawn, expired, incompatible, or dismissed announcement
      When the board loads
      Then no card renders and responses carry private, no-store cache control
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Optimistic client dismissal
      Given a visible card and an offline dismissal write
      When the user dismisses and later reconnects or opens another tab
      Then the card hides immediately, the write stays pending locally, and the retry syncs without reshowing
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Safe staged publishing
      Given a staging feed name and changed asset bytes
      When publishing without --publish or with a digest mismatch
      Then nothing uploads to production and the mismatch fails with a SHA-256 error
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Audit company validation
      Given a dismiss request with an unknown company or extra body fields
      When the request is posted
      Then the service returns 404 or 400 respectively
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Guarded remote fetch
      Given a hung or redirecting feed URL
      When the service fetches it
      Then the request is bounded to 3 seconds, redirects are refused, and no URL or content is logged
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Bounded shared caches
      Given concurrent identical current and asset requests
      When they execute together
      Then the remote feed is fetched once and cached bytes are reused
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Graceful degradation
      Given an unavailable or invalid feed
      When the board loads
      Then no card appears, no error popup shows, and the board works normally
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Accessible card
      Given a rendered announcement card
      When inspected for accessibility
      Then it exposes a labelled region, an aria-labelled dismiss button with Escape support, and a labelled static image when animation plays
    ```

## Conflicts

None identified yet.

## Open Questions

1. Who owns the production manifest publishing cadence and approval (not determinable from code)?
2. Is impression or view telemetry desired, given no view events are stored today (not determinable from code)?
