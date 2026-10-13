---
title: "Browser Control"
status: done
---

# Requirements: Browser Control

## Overview

The browser-control subsystem carries agent `browser.*` actions from the server to the client that owns the in-app browser view, and the result back, because the browser lives in a renderer and the server can only ask and wait.
It is shared by three server pieces (`broker.js` for request lifetime, `provider.js` for builtin-versus-extension routing, `routes.js` for claim and result callbacks) and one client half (`controlClient.ts` plus page scripts), all invoked through the `openchamber-control` service which owns `browser.*` parameter validation.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agents | Drive the in-app browser (open, read, click, type, scroll, inspect, capture, resize) without touching the user's view |
| Users | Keep keyboard focus, visible tab, and clipboard private while an agent works a page in the background |
| Extension authors | Serve `browser.*` actions from an extension service that provides the `browser` role |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall publish one browser action through the injected `emitRequest` and hold the pending request until a client result, a timeout, or an abort signal settles it. |
| FR-2 | Must | The system shall grant the right to perform a request to exactly one client via first-claim-wins, refusing claims for already-settled requests. |
| FR-3 | Must | The system shall reject immediately with a 503 environment description when no client is listening instead of blocking for the full timeout. |
| FR-4 | Must | The system shall expose a result callback that validates the envelope and accepts results for unknown request ids with `matched: false` rather than an error. |
| FR-5 | Must | The system shall expose a claim callback that grants or refuses the right to act before the client touches the page. |
| FR-6 | Must | The system shall support the ten `browser.*` actions (`open`, `snapshot`, `click`, `type`, `scroll`, `back`, `forward`, `inspect`, `capture`, `resize`) with per-action parameter validation that fails as a usage error without waking a client. |
| FR-7 | Must | The system shall route each action on every call from the `browserProvider` setting: `builtin` goes to the broker and an extension id goes to that extension's service. |
| FR-8 | Must | The system shall reset the provider setting to `builtin`, emit `openchamber:browser-provider-reset`, and run the action in-app when the selected extension can no longer serve. |
| FR-9 | Must | The system shall fail the action with 503 and run nothing anywhere when the settings or catalog read fails, leaving the provider choice unchanged. |
| FR-10 | Must | The system shall report a sent-but-unanswered action (`REQUEST_FAILED`) as "may or may not have run, read the page first", never as unchanged. |
| FR-11 | Must | The system shall thread the caller `context` (`directory`, `sessionId`, each `null` when unknown) from the tool call through to the provider and the client event. |
| FR-12 | Must | The system shall derive capability from the connection (`browser=1`, Chromium hosts only), requiring any client for `browser.open` and a declared-capable client for every other action. |
| FR-13 | Should | The system shall resolve the target tab as the named `tabId` tab, else the calling session's tab, else the user's shown tab in the session's project, and `browser.open` without `tabId` shall open a new background tab without switching the user. |
| FR-14 | Should | The system shall list visible tabs (`id`, `title`, `url`, `owner`, `active`) in `browser.snapshot` answers, scoped to the caller's own tabs plus other tabs of its project. |
| FR-15 | Should | The system shall refuse an extension-provider action with 409 while the user holds the shared surface and report every provider action that runs as agent activity. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Timeouts are bounded (1s minimum, 120s maximum, 20s default, 45s for `browser.open`) and a vanished claimer still times out rather than reporting assumed success. |
| NFR-2 | Must | Security | Clipboard contents never cross the broker: the page writes directly to the host clipboard and native paste reads from it. |
| NFR-3 | Must | Correctness | Request payload limits are sized for a page snapshot (4kb claim, 2mb result) and snapshot answers are capped (6000 text chars, 120 elements, 80 label chars) with dropped content reported. |
| NFR-4 | Should | Usability | Agent work never takes keyboard focus from the user: pages get emulated focus for `click`/`type`, hidden panes are drawn at zero opacity for `capture`, and `scroll` on a hidden page waits at most 100ms for paint frames. |

## Constraints

- The server never acts on a page itself; it only asks connected clients and waits.
- The result route parses its own body because the server has no global body parser.
- A successful `browser.open` result states `drivable` per claimer and it is never inferred from configuration.
- `browser.capture` returns a server-written file path, never the base64 image, to the caller.
- Cancellation propagates via abort signal and surfaces as status 499.

## Acceptance Criteria

```gherkin
@FR-1
Feature: Broker request lifetime
  Scenario: Client answers in time
    Given a pending browser request
    When the owning client posts its result
    Then the waiting agent call resolves with the client's data
```

```gherkin
@FR-2
Feature: Exactly one client acts
  Scenario: Two clients receive one request
    Given two connected clients that could serve a request
    When both claim it
    Then the first claim is granted and the second is refused
```

```gherkin
@FR-3
Feature: Fail fast with nobody listening
  Scenario: No client connected
    Given zero reachable clients
    When a browser action is requested
    Then it rejects immediately with 503 instead of blocking for the timeout
```

```gherkin
@FR-4
Feature: Late results are not errors
  Scenario: Result arrives after timeout
    Given a request that already timed out
    When the client posts its result
    Then the route answers with matched false and no error
```

```gherkin
@FR-6
Feature: Parameter validation precedes round trip
  Scenario: Invalid browser input
    Given a browser.click call with neither selector nor text
    When the control service validates it
    Then it throws a usage error without waking any client
```

```gherkin
@FR-7 @FR-8
Feature: Provider routing and reset
  Scenario: Selected extension cannot serve
    Given a browserProvider extension that is paused or unapproved
    When a browser action runs
    Then the setting resets to builtin, the reset event fires, and the action runs in-app
```

```gherkin
@FR-9
Feature: Read failures change nothing
  Scenario: Settings read fails
    Given an unreadable browserProvider setting
    When a browser action runs
    Then it fails with 503, nothing runs anywhere, and the choice stays
```

```gherkin
@FR-10
Feature: Ambiguous sends stay ambiguous
  Scenario: Request sent but unanswered
    Given a provider request lost after sending
    When the failure reaches the agent
    Then it says the action may or may not have run and to read the page first
```

```gherkin
@FR-12
Feature: Capability belongs to the connection
  Scenario: Display-only client
    Given a client without the browser capability flag
    When it opens a page
    Then the open succeeds and reports drivable false for that claimer
```

```gherkin
@FR-13
Feature: Tab resolution never disturbs the user
  Scenario: Open without tabId
    Given an agent session with no tabId
    When browser.open runs
    Then a new background tab opens in the session's project and the user's visible tab is unchanged
```

```gherkin
@NFR-1
Feature: Vanished claimer times out
  Scenario: Claimer disappears
    Given a claimed request whose client disconnected
    When the timeout expires
    Then the agent call fails with 504 rather than reporting success
```

## Conflicts

None identified yet.

## Open Questions

1. How should `browser.snapshot` tab listings behave when an extension provider (rather than the in-app browser) serves actions, given `tabId` currently passes through untouched?
