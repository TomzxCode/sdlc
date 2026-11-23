---
title: "Issue trackers and tracked items"
status: done
---

# Requirements: Issue trackers and tracked items

## Overview

OpenChamber needs one provider-neutral way to connect work-item trackers such as Linear and to show the live state of linked issues, pull requests and merge requests on sidebar rows, worktree headers and context sources.
The tracker layer owns auth, item reads and writes, project mapping and optional session status comments, while the tracked-items layer announces what each connection shows and publishes state changes over the event stream.
The same neutral contract serves web, desktop and mobile, and an older server that only speaks Linear stays usable through a legacy adapter.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users | Connect a tracker once, switch workspaces, see current statuses beside sessions and worktrees, and update an item without leaving OpenChamber |
| Agents | Receive attached tracker items in a stable context shape and act on the right project after mapping |
| Extension authors | Serve a tracker through an installed extension with the same routes and capabilities as a built-in |
| Maintainers | Add a tracker as one registry entry without changing every surface |
| Paired mobile clients | Read linked item state from the host without duplicating credentials |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall keep one server-side registry of tracker descriptors and load each implementation once on first use. |
| FR-2 | Must | The system shall expose tracker auth status, browser sign-in, token connect, account activation and disconnect through provider-named routes. |
| FR-3 | Must | The system shall list, get and update tracker items and list workflow states through neutral shapes, gated by the tracker's capabilities. |
| FR-4 | Must | The system shall store a default project path plus per-container project paths and a server-side session-comments preference per tracker. |
| FR-5 | Must | The system shall post started, completed and failure comments on a linked item when the tracker offers comments, the user opted in and the session origin is public. |
| FR-6 | Must | The system shall map Linear workspaces, states, priorities, teams, labels, parent and sub-issues into the neutral tracker contract and match Linear URLs by the served pattern. |
| FR-7 | Must | The system shall answer live summaries of linked work items per tracker for sidebar rows, worktree headers and Context sources. |
| FR-8 | Must | The system shall keep the legacy Linear routes and let the web client fall back to them when the server predates the tracker routes. |
| FR-9 | Must | The system shall attach and detach extension trackers from the extension catalog and serve them through the same registry, routes and event fan-out. |
| FR-10 | Must | The system shall let each event-stream connection declare its visible items and publish changed states only to connections that show them. |
| FR-11 | Must | The system shall parse source-control threads and work items into stable keys while keeping legacy GitHub and kindless Linear records readable. |
| FR-12 | Must | The system shall refresh only followed items, batched per provider and account, with state-based cadence, backoff after failure and immediate refresh after local changes. |
| FR-13 | Must | The system shall restore and persist the last known item states in bounded caches on both server and client. |
| FR-14 | Should | The system shall draw every served tracker in shared UI surfaces from its descriptor, offering working surfaces only for trackers with a connected account and hiding them where no tracker API exists. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Credentials stay on the server and only reach a guest through host access on its own API origin. |
| NFR-2 | Must | Reliability | A failed read, a failed descriptor refresh or an unreadable credential never becomes authoritative empty success. |
| NFR-3 | Must | Performance | Bounded batches, caps and summary limits keep refresh work proportional to visible items and tracker batch limits. |
| NFR-4 | Compatibility | Must | Stored identity strings, link kinds and legacy state shapes stay readable by older bundled clients. |
| NFR-5 | Correctness | Must | Unknown state is null or absent, capability gaps are explicit, and one failed item or tracker does not erase unrelated states. |

## Constraints

- Repository issues and pull requests stay on the source-control side, not in the tracker registry.
- `packages/ui` is shared by web, desktop, hosted mobile and Capacitor mobile; VS Code has no tracker API and no OpenChamber event stream.
- `/api/tracker` is host-only, and session-status fan-out receives host events only.
- JSON bodies on tracker routes are limited to 16kb, and tracked-item bodies to 128kb.
- Translated text and icons cannot come from the server, so presentation is per id in the UI.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: List the registered trackers
      Given a server with the Linear tracker as a built-in
      When a client calls GET /api/tracker/providers
      Then the answer contains the Linear descriptor as plain JSON
      And an implementation is loaded only when a route first needs it and is reused afterwards
      And a failed load is retried on the next request
    ```

    ```gherkin
    @FR-1
    Scenario: Refuse an invalid registration
      Given a tracker id that is malformed, reserved, duplicated or owned by source control
      When the registry is created
      Then startup throws an error naming that id
      And unknown ids answer null instead of throwing
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Connect a Linear workspace
      Given a user on the Integrations page with no stored workspace
      When the client starts authorization and completes the browser callback
      Then auth status reports connected with the current account and no token
      And switching to another stored workspace activates it
      And disconnect removes only the current workspace
    ```

    ```gherkin
    @FR-2
    Scenario: Connect an extension tracker
      Given an extension tracker that accepts tokens and OAuth clients
      When the client posts a token with an instance or saves a client and signs in
      Then the answer carries the stored accounts and connect information
      And a missing or over-long field is refused before the service is called
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Read and update an item
      Given a connected tracker whose descriptor allows state updates
      When the client lists items with valid filters, gets one item, reads its workflow states and posts a state change
      Then each answer uses neutral item shapes and the updated item is returned
      And an unsupported filter or capability answers 400 or 404 with a code
    ```

    ```gherkin
    @FR-3
    Scenario: Disconnected or unknown tracker
      Given no current account or an unregistered provider id
      When the client reads items
      Then a disconnected tracker answers HTTP 200 with connected false
      And an unknown tracker answers 404 UNKNOWN_TRACKER
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Map containers to projects
      Given a connected tracker with a mapped default project and one mapped team
      When the mapping is read and later replaced
      Then the answer lists containers with their paths and the default path
      And an issue from that team resolves to its team path before the default path
      And an issue with neither path asks the user to map the team
    ```

    ```gherkin
    @FR-4
    Scenario: Toggle session comments
      Given a tracker with the session-comments capability
      When the client writes a non-boolean preference or a tracker without the capability is asked
      Then the write is refused with 400 or 404
      And a valid preference is stored on the server and survives a UI restart
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Comment on a session only when allowed
      Given a session whose first message carries a linked item, comments enabled and a public session origin
      When the message is sent and the session later goes idle or errors
      Then a started comment with a session link is posted once
      And a completed or failure comment is posted once with the stored link
    ```

    ```gherkin
    @FR-5
    Scenario: Skip a comment that nobody else could use
      Given comments enabled but a loopback or private session origin
      When a session status is posted
      Then no comment is created and the answer says the origin is not public
      And a disconnected tracker still answers with the connect prompt
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Map a Linear issue to the neutral contract
      Given a Linear issue with state type started, priority 1, labels, a parent and sub-issues
      When the tracker adapter lists and gets the issue
      Then the item reads with category in-progress, priority urgent, container from its team and progress with a more flag
      And a Linear state type this build does not know reads as the todo category in live summaries
    ```

    ```gherkin
    @FR-6
    Scenario: Match a Linear link
      Given a pasted Linear issue URL with a www host or a trailing slash
      When the server or client matcher reads it
      Then both return the same upper-case identifier
      And a URL on another host returns no identifier
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Read linked work item states
      Given sidebar rows and a worktree header that show a linked Linear issue
      When the tracked-items work-items reader asks the registry for that identifier
      Then the answer carries title and state with a category
      And a tracker the registry does not know answers disconnected
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Talk to an older server
      Given a web client connected to a server with no /api/tracker routes
      When the client asks for providers and reads or writes a Linear item
      Then it uses its built-in Linear descriptor and the /api/linear routes
      And the shared UI still receives neutral shapes
    ```

    ```gherkin
    @FR-8
    Scenario: Keep the Linear alias
      Given an older bundled phone UI or an SDK host-Linear guest
      When it calls /api/linear/issues/get or /api/linear/oauth/callback
      Then the same Linear functions answer as through the tracker routes
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Attach an extension tracker
      Given an enabled extension with an approved effective service grant that provides a tracker
      When the catalog is read at startup or on an activation change
      Then an ext- tracker is attached after the built-ins with a descriptor built from its manifest
      And clients receive openchamber:tracker-providers-changed
      And pausing or removing the guest detaches it
    ```

    ```gherkin
    @FR-9
    Scenario: Service failure on an extension tracker
      Given an extension tracker whose service does not answer within its deadline
      When a read or write is made
      Then the error is reported as unavailable without writing off an account
      And a removed tracker forgets its accounts, client, mapping and session records
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Follow what is on screen
      Given a connection with an event stream and visible sidebar rows
      When it posts interest with its connection id and items
      Then the answer carries the states already known
      And a state change reaches only connections that show the item and only when it moved
    ```

    ```gherkin
    @FR-10
    Scenario: Connection lifetime and presence
      Given a connection that closed and a window that was hidden
      When a client sends interest for the old id or flips visibility
      Then the old id is refused with 409 and presence updates the visible set
      And a reconnect resends interest with the new connection id
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Keep one key per item
      Given a work item from any tracker and a pull request on an enterprise host
      When the server and client parse them
      Then both compute the same provider and upper-case identifier key or the same host-qualified thread key
      And a kindless Linear record or an instance-less GitHub record parses to the same key as its modern shape
    ```

    ```gherkin
    @FR-11
    Scenario: Drop invalid items independently
      Given an interest list with a malformed identifier, an unregistered source-control provider and one valid item
      When the list is parsed
      Then only the valid item is followed
      And a discussion on a provider without discussions parses as nothing
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Refresh on cadence and after changes
      Given a visible open pull request, an open work item and a settled work item
      When time passes and an agent turn finishes
      Then the pull request is read every 60 seconds and the open work item every 2 minutes
      And the settled item is read every 5 minutes and open items are re-read 3 seconds after the turn settles
    ```

    ```gherkin
    @FR-12
    Scenario: Back off after a failure
      Given a provider that fails or is rate-limited
      When the next refresh is due
      Then its last known states stay on screen
      And retries back off from 30 seconds to 15 minutes
      And an explicit refresh reads only the named item
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Restore last known colours after restart
      Given a server cache and a client store holding states from the past 12 hours
      When the app restarts
      Then both show the last known states at once with their fetched timestamps
      And a restored entry never overwrites a newer answer from a client
    ```

    ```gherkin
    @FR-13
    Scenario: Bound and discard the cache
      Given more than 500 server entries or a malformed and expired client record
      When persistence loads or saves
      Then the server trims only unfollowed entries oldest first
      And the malformed or expired record is dropped without dropping unrelated records
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Draw the connected trackers only
      Given a served tracker with a connected account and another that is not connected
      When the board, composer attach menu and New Worktree list their sources
      Then only the connected tracker is offered
      And Settings still shows both cards with mapping and comments where the capabilities allow
    ```

    ```gherkin
    @FR-14
    Scenario: Handle a runtime without trackers
      Given VS Code with no tracker API or a runtime whose list fetch failed
      When the UI renders
      Then tracker surfaces hide or keep the last held list and retry
      And an authoritative empty list or a missing API never appears as a fetch failure
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Keep credentials on the host
      Given an extension tracker account and a host-Linear guest
      When a client reads auth status or a guest asks for host access
      Then no token or client secret appears in a client answer
      And a guest uses the token only through its own API origin
    ```

    ```gherkin
    @NFR-1
    Scenario: Reject a stale OAuth callback
      Given a public tracker callback URL with a state that is missing, expired or already used
      When it is opened
      Then no account is attached and the callback page reports a failed sign-in
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Preserve state through failures
      Given one tracker list read that fails and another that succeeds
      When the UI refreshes trackers and tracked items
      Then the failed tracker's held list and last known item states remain
      And unreadable credentials propagate as an error rather than a disconnected success
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Bound read cost
      Given a large sidebar, 50 linked work identifiers and a provider batch limit
      When a refresh runs
      Then interest beyond 300 items is rejected rather than truncated
      And work items are requested in batches of at most 50 and summary requests never exceed their provider limit
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Keep old data readable
      Given a session link stored as kind linear with provider linear, a kindless tracked record and a live state with only a Linear type
      When a current client reads and rewrites them
      Then the link keeps its kind, the record keeps its key and the state reads by category
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Keep unrelated items independent
      Given one tracker that is unavailable, one item whose provider no longer answers it and one valid item
      When states are published
      Then the unknown state is null, the valid item keeps its state
      And a listener that throws is logged while other listeners and refreshes continue
    ```

## Conflicts

None identified.

## Open Questions

1. None. These artifacts were reverse-engineered from the implementation and its module documentation.
