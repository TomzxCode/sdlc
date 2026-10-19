---
title: "Hosted Account and Plans"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Hosted Account and Plans

## Overview

The first-party Jcode account is the user's identity for everything the Jcode service hosts.
Signing in is a browser-based device authorization: the user approves the request on `https://jcode.sh/account`, and Jcode exchanges a single-use device code for an account key that is stored on the machine with owner-only permissions.
The account carries a metered plan rather than a fixed subscription fee.
The user picks a monthly spending limit in the browser, usage is billed in progressively larger tranches starting at $20, and the account service enforces that limit server-side.
Jcode surfaces the canonical account, the plan tier, the spend against the limit, and the daily feature allowances so the user always knows what the account is spending.
This feature documents already-implemented functionality that was reverse-engineered from the existing codebase during an SDLC sync.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| CLI user | One command to sign in, one command to see the plan and the spend, and one command to leave |
| TUI user | A hosted-model entry point, a status surface, and a visible spending balance while the session runs |
| Desktop user | The same account and plan surfaces through the shared account login library |
| Account API owner | A single device-authorization contract that the CLI, the TUI and Desktop all speak |
| Finance | A monthly limit the user controls, a predictable tranche schedule, and a server-side enforcement point |
| Support | A way to tell whether a credential is present, revoked, or offline without reading the user's credential file |
| Maintainer | A catalog and a route policy that the server, not a stale client-side tier, decides |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall sign a user in with a browser-based device authorization flow that requests a device code with the `jcode-cli` client name, opens the public approval URL, and polls the token endpoint with bounded backoff until the browser approves, the user denies, the device code expires, or the flow times out, and a Ctrl-C during the wait shall cancel the flow without saving a credential. |
| FR-2 | Must | The system shall wait for plan activation after the browser approval by polling `/v1/me` until the account reports an active plan with a spending limit, a canceled checkout, a revoked or denied key, or the activation timeout elapses. |
| FR-3 | Must | The system shall persist the approved account key together with the non-secret account id, email and tier in the owner-only hosted-account file, and shall not write any credential before the browser approval is confirmed. |
| FR-4 | Must | The system shall keep the valid account key and print recovery actions when activation is canceled or times out, and shall clear the local credentials when the key is revoked or the account server denies the activation check. |
| FR-5 | Must | The system shall report the canonical account email, the plan tier and status, and the monthly spending usage from `/v1/me` on `jcode account status`, and shall offer a `--json` form of the same account payload. |
| FR-6 | Must | The system shall tell the user to run `jcode account login` when no account credential is configured, and shall clear the local credentials and report a revoked or expired key when `/v1/me` answers unauthorized. |
| FR-7 | Must | The system shall open the public Jcode account management page from `jcode account manage`, and shall print the URL instead of launching a browser when browser launch is suppressed. |
| FR-8 | Must | The system shall always clear the local account credential, the cached account identity and the cached tier on `jcode account logout`, and shall revoke the key remotely when the account API is reachable. |
| FR-9 | Must | The system shall report the outcome of each logout step, distinguishing no local credential, a revoked key, an already revoked key, an offline account API, and a remote revocation that could not be confirmed. |
| FR-10 | Must | The system shall write the hosted-account credential file with owner-only permissions and shall re-harden and re-verify the permission mode after every credential mutation. |
| FR-11 | Must | The system shall offer exactly the curated hosted models, shall offer every curated model at the base plan, and shall pin every hosted model to the managed Jcode router route so a hosted model id never falls through to a direct provider credential. |
| FR-12 | Must | The system shall expose `/hosted` and its `/subscribe` alias for the hosted-model pitch, and `/hosted status` with its `/subscription` and `/subscription status` aliases for the hosted account status. |
| FR-13 | Must | The system shall show the credential state, the router base, the billing model, the runtime mode, the curated catalog and the billing rules including the tranche schedule on the hosted account status surface, and shall fetch `/v1/me` in the background to publish the account email, the billing status, the spend against the monthly limit, the amount already billed, the next tranche amount and the reset time. |
| FR-14 | Must | The system shall clear the local credentials and tell the user to sign in again when the hosted account status surface finds that the account key was revoked. |
| FR-15 | Must | The system shall report the Jcode inference spending balance, the remaining amount against the monthly limit, the daily feature allowances and the reset time on the usage surface, shall mark the hard limit as reached when the monthly spend reaches the monthly limit, shall not mark it reached when the limit is unknown, and shall suggest an upgrade when a daily allowance passes 80 percent of its limit and an upgrade target is offered. |
| FR-16 | Must | The system shall produce a subscription notice when a plan or allowance changes that names the exhausted feature, the current plan and the upgrade target with a link, and shall deliver the notice once per occurrence. |
| FR-17 | Must | The system shall expose the hosted account in the TUI through `/login jcode` and `/account jcode login`, and shall expose the account status, the management page and the logout as `/account jcode status`, `/account jcode manage` and `/account jcode logout`. |
| FR-18 | Must | The system shall enable the hosted runtime mode when the hosted account is activated, and shall clear the hosted runtime mode when the credentials are cleared or the user selects another provider. |
| FR-19 | Should | The system shall offer an email-code sign-in that sends a code to the address, keeps the code token in memory only, and reports the remaining attempts when the typed code is wrong. |
| FR-20 | Should | The system shall surface a hosted-model nudge when a provider rate-limits the user and after a long fully completed task, at most once per session and at most once per week, and never for a user who already holds account credentials. |
| FR-21 | May | The system shall accept a monthly hard cap, a billing portal session, a subscription checkout and a plan change from the account API, and shall accept only an https billing portal URL and only a Stripe Checkout URL. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The account key shall never appear in a URL, in a debug rendering, in a log line or in an error message, and shall be sent only in an authorization header. |
| NFR-2 | Must | Security | The browser approval URL shall be restricted to the allowlisted public https origins with the account path and a single flow query parameter, and the account management URL shall be restricted to the same origins, so a URL carrying credentials, a non-default port, an unexpected path or extra query parameters is rejected. |
| NFR-3 | Must | Security | The monthly spending limit and the model policy shall be enforced server-side by the Jcode router, and the client shall not decide from a cached tier which models an account may use or how much it may spend. |
| NFR-4 | Must | Security | The account key shall be revoked on the server when the user logs out and the account API is reachable, and the local credential shall be cleared even when the revocation cannot be confirmed. |
| NFR-5 | Must | Privacy | The account email, the account id and the spending limit shall not be sent to the telemetry service, and the only telemetry emitted for this feature shall be the coarse authentication success event. |
| NFR-6 | Must | Availability | A failed `/v1/me` fetch shall keep the local credential and shall degrade to a quiet message rather than failing the session, and an unreachable account API during the device poll shall be retried with backoff rather than aborting the flow. |
| NFR-7 | Must | Performance | The account status fetch shall use a 5 second timeout, the device authorization request shall use a 15 second timeout, and the polling backoff shall stay deterministic and bounded. |
| NFR-8 | Should | Availability | The activation wait shall be bounded to 10 minutes, and a polling request that is already in flight shall be allowed to finish so a single-use device code is not stranded. |
| NFR-9 | Should | Usability | A user who has not signed in shall be pointed at `/login jcode`, and the hosted account status shall state plainly that hosted usage is not enabled until a spending limit exists. |
| NFR-10 | Should | Privacy | The browser approval URL and the account management URL shall be the only links the client opens, and the client shall never open a URL returned by the account API without checking its scheme and origin. |
| NFR-11 | Should | Compatibility | The account service contract shall be versioned by endpoint, and a legacy backend that only offers the old email-based login shall produce a specific compatibility error rather than a generic failure. |

## Constraints

- The account API is a remote service at `https://api.jcode.sh/v1` by default, overridable with `JCODE_API_BASE`.
- The account key lives in `jcode-subscription.env` under the jcode config directory, with the API base kept separately because it is endpoint configuration and not a credential.
- The hosted models are served by the Jcode router over the OpenRouter transport, pinned to the `jcode-subscription` transport state.
- The spending limit is set by the user in the browser at `https://jcode.sh/account`, not in the terminal.
- The terminal never asks for an account key, and the browser never receives the account key.
- Tranche billing starts at $20 of usage and then uses progressively larger tranches, with any remaining usage billed at the limit or at month end.
- The user can change the spending limit at any time from the account page.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).
Write each criterion as a fenced `gherkin` block with a tag matching its requirement ID, so the criteria are parseable and later executable via BDD tooling (pytest-bdd, cucumber).
Multiple scenarios per requirement are allowed; tag each with the requirement ID.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Browser approval completes the device flow
      Given a running account API that returns a device authorization
      When the user runs `jcode account login` and approves the request in the browser
      Then the client sends `POST /v1/auth/device` with the client name `jcode-cli`
      And the client sends `POST /v1/auth/token` with the device code
      And no further request is sent before the approval
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Activation is confirmed from the account payload
      Given an approved account key
      When the client polls `/v1/me`
      Then the client stops polling when the payload reports an active status with a spending limit
      And the client reports the monthly spending limit to the user
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Canceled checkout stops the activation wait
      Given an approved account key
      When `/v1/me` reports a canceled status
      Then the client stops polling and reports that hosted usage is not enabled
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The credential is written only after approval
      Given a device flow that is waiting for the browser
      When the user has not approved yet
      Then no account credential exists on the machine
      When the user approves and the client saves the credential
      Then the hosted-account file holds the account key, the account id, the email and the tier
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A revoked key clears the local credentials
      Given a saved account credential
      When the activation check reports an unauthorized key
      Then the local credentials are cleared
      And the user is told to run `jcode account login` again
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A timed-out activation keeps the key
      Given a saved account credential
      When the activation wait times out without an active plan
      Then the account key remains saved
      And the client prints the status, manage and logout recovery commands
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Status shows the account, the plan and the spend
      Given a configured account credential
      When the user runs `jcode account status`
      Then the output shows the account email
      And the output shows the plan display name with the account status
      And the output shows the used amount and the monthly limit
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Status can emit the raw account payload
      Given a configured account credential
      When the user runs `jcode account status --json`
      Then the output is the parsed account payload as JSON
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Status without a credential points at the login command
      Given no configured account credential
      When the user runs `jcode account status`
      Then the command fails with a message telling the user to run `jcode account login`
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Status detects a revoked key
      Given a configured account credential
      When `/v1/me` answers unauthorized
      Then the local credentials are cleared
      And the command fails with a message that the key was revoked or expired
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Manage opens the public account page
      Given browser launch is allowed
      When the user runs `jcode account manage`
      Then the client opens `https://jcode.sh/account`
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Manage prints the URL when the browser is suppressed
      Given browser launch is suppressed
      When the user runs `jcode account manage`
      Then the client prints the account page URL and does not launch a browser
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Logout clears local state and revokes the key
      Given a configured account credential
      When the user runs `jcode account logout` and the account API is reachable
      Then the key is revoked on the server
      And the local credential, account id, email and tier are cleared
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Logout clears local state when the account API is offline
      Given a configured account credential and an unreachable account API
      When the user runs `jcode account logout`
      Then the local credential is still cleared
      And the client states that remote revocation could not be confirmed
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Logout reports the outcome of each step
      Given a machine with no account credential
      When the user runs `jcode account logout`
      Then the client reports that no local credential was present
      And the client reports that the local account cache is clear
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: The credential file stays owner-only
      Given a saved account credential
      When the credential file is inspected
      Then the file mode is owner-read and owner-write only
      And the same mode holds after a credential mutation
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Only the curated hosted models are offered
      Given the hosted model catalog
      When the model list is enumerated
      Then the list holds exactly the curated hosted models
      And every curated model is available at the base plan
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Hosted models stay on the managed route
      Given a hosted model id
      When the route is built for that model
      Then the route provider is the Jcode Subscription display name
      And the route api method is `jcode-subscription`
      And the route is marked available
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: The hosted commands and their aliases resolve
      Given a running TUI
      When the user types `/hosted`
      Then the hosted-model pitch is shown
      When the user types `/subscribe`
      Then the hosted-model pitch is shown
      When the user types `/hosted status`, `/subscription` or `/subscription status`
      Then the hosted account status surface is shown
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The status surface explains the billing model
      Given a configured account credential
      When the hosted account status is shown
      Then the surface shows the credential state, the router base and the runtime mode
      And the surface shows the curated catalog
      And the surface states that charges begin at $20 and then use progressively larger tranches
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The status surface publishes the live spend
      Given a configured account credential
      When `/v1/me` returns an account with a used amount, a monthly limit, a billed amount, a next tranche amount and a reset time
      Then the background activity shows the account email and the billing status
      And the background activity shows the spend against the monthly limit
      And the background activity shows the amount already billed and the next tranche amount
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The status surface reacts to a revoked key
      Given a configured account credential
      When `/v1/me` answers unauthorized
      Then the local credentials are cleared
      And the activity says the key was revoked or expired and to sign in again
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: The usage surface shows the inference balance
      Given an account with a used amount of 12.50 and a monthly limit of 50.00
      When the usage report is built
      Then the report has an inference spending limit row at 25 percent
      And the report shows the remaining amount as $37.50
      And the report shows the spend as $12.50 / $50.00
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: An unknown monthly limit is not exhaustion
      Given an account whose monthly limit is zero, negative, or not a finite number
      When the usage report is built
      Then the report does not mark the hard limit as reached
      And the report omits the remaining amount row
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: An upgrade is suggested near a daily allowance limit
      Given a daily memory allowance used at 850 of 1000 with an upgrade tier and an upgrade link
      When the usage report is built
      Then the report carries an upgrade row naming the tier and the link
      And the report does not mark the hard limit as reached
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: A plan limit notice names the feature and the upgrade
      Given a memory allowance on the Plus plan with a Pro upgrade target
      When the notice is rendered
      Then the notice names the memory recall feature and the Plus plan
      And the notice names the Pro upgrade target with its link
      And the notice is taken exactly once
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: The TUI account commands parse to the hosted account actions
      Given a running TUI
      When the user types `/account jcode login`
      Then the hosted account login starts
      When the user types `/account jcode status`
      Then the hosted account status is shown
      When the user types `/account jcode manage`
      Then the account management page is opened
      When the user types `/account jcode logout`
      Then the hosted account logout starts
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: The runtime mode follows the account state
      Given no hosted account
      When the runtime mode is read
      Then the hosted runtime mode is inactive
      When the hosted account is activated
      Then the hosted runtime mode is active
      When the credentials are cleared
      Then the hosted runtime mode is inactive
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: A wrong emailed code reports the remaining attempts
      Given a started email sign-in for an address
      When the user types a wrong code
      Then the client reports that the code is incorrect with the remaining attempt count
      And the client persists nothing
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: The nudge is rate limited
      Given the nudge was already shown this session
      When a rate limit happens
      Then no nudge line is added
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Unsafe payment URLs are rejected
      Given the account API returns a billing portal URL that is not https
      When the client reads the portal URL
      Then the client refuses the reply
      Given the account API returns a checkout URL that is not a Stripe Checkout URL
      When the client reads the checkout URL
      Then the client refuses the reply
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The account key never leaks
      Given a device flow and an approved login
      When the flow, the approval and the error renderings are formatted
      Then the device code, the account key and the login token do not appear
      And the account API request carries the key in an authorization header
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Unsafe browser URLs are refused
      Given browser URLs over plain http, on a foreign host, with credentials, with a port, on a non-account path, with extra query parameters, with a fragment, and with a malformed flow value
      When the client validates each URL
      Then every one of them is refused as an invalid response
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A cached tier cannot widen the hosted catalog
      Given a stale cached tier of Ultra on the machine
      When the hosted catalog is consulted
      Then the available hosted models are unchanged
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Local state is cleared even when revocation fails
      Given a configured account credential and an account API that cannot be reached
      When the user logs out
      Then the local credential is cleared
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The telemetry event carries no account data
      Given a completed hosted account sign-in
      When the telemetry event is recorded
      Then the event names the hosted account provider and the device-code browser method
      And the event carries no email, no account id and no spending limit
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: An unreachable account API does not lose the credential
      Given a configured account credential
      When the account status fetch fails
      Then the local credential is retained
      And the user sees a quiet message that the status could not be loaded
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: The polling backoff stays bounded
      Given a poll that returns pending, then a slow-down, then an offline error
      When the delay is read after each response
      Then the delay grows to a bounded maximum and returns to the base delay after a pending response
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: An in-flight exchange is allowed to finish
      Given a token exchange that is already in flight
      When the user cancels the login
      Then the exchange still completes and the approved key is returned
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: A signed-out user is told how to sign in
      Given no configured account credential
      When the hosted account status is shown
      Then the surface tells the user to sign in with `/login jcode` to set a spending limit
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: Only allowlisted origins are opened
      Given an account payload whose management URL points at a foreign origin or carries credentials
      When the client picks the management URL
      Then the client falls back to the public Jcode account page
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: A legacy backend gets a specific error
      Given the account API answers the device request with the old email-based contract
      When the client starts the device flow
      Then the client reports that the configured account API uses the legacy login contract
      And the response body is not echoed
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified yet.

## Open Questions

1. The metered plan and the legacy `JcodeTier` ladder (Plus, Pro, Max, Ultra, Solo) both exist in the code, but only the metered plan is used for the hosted catalog and the spending limit.
   Should the tier ladder be retired, or kept as a separate cloud entitlement ladder as `docs/JCODE_CLOUD_AWS.md` describes?
2. The `SubscriptionUsage` field `budget_usd` is the canonical name on the wire, with `spend_limit_usd` and `limit_usd` accepted as aliases for older servers.
   Should the canonical name become `spend_limit_usd` so the wire field matches the user-facing "spending limit" wording?
3. The account API exposes `PUT /v1/billing/hard-cap`, `POST /v1/billing/portal`, `POST /v1/billing/subscribe` and `POST /v1/billing/plan`, but the current user flow sets the limit in the browser and never calls them from the client.
   Should the terminal expose a limit-setting command, or keep the browser as the only place the limit changes?
