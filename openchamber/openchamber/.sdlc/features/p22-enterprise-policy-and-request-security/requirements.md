---
title: "Enterprise policy and request security"
status: done
---

# Requirements: Enterprise policy and request security

## Overview

Enterprise mode lets an administrator constrain an OpenChamber instance with a machine policy file or an environment switch, so conversation content stays with model providers configured in OpenCode.
Request-security rules constrain which browser origins the server and UI accept, which hosts the server may bind, which URL a session cookie belongs to, and which documents may frame the app.
Settings expose the trusted app-link schemes and the public part of the enterprise policy, while pinned endpoints and keys stay on the server.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Enterprise administrators | Apply one policy across managed machines and keep provider, relay, Jev, extension, and network choices under administrative control |
| Users | See when a policy applies, who set it, and which app-link schemes they have trusted |
| Operators | Expose OpenChamber behind a proxy or on a LAN without accepting cross-origin socket connections or unauthenticated access by default |
| Extension and client authors | Keep packaged client origins and embedder origins working without opening the UI to arbitrary pages |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall read a machine policy file from the fixed path for macOS, Windows, and Linux, and on Windows shall read the fixed ProgramData path before an environment-redirected path. |
| FR-2 | Must | The system shall turn enterprise mode on from a policy file or from `OPENCHAMBER_ENTERPRISE_MODE`, shall let a file that sets enterprise mode govern the policy, and shall not let the environment turn a file-enabled mode off. |
| FR-3 | Must | The system shall validate the policy file with a schema that trims text, caps `allowedExtensions` at 200 entries, requires a `jev.url` when `jev` carries a model or key, accepts a byte-order mark, and ignores unknown keys. |
| FR-4 | Must | The system shall fail closed when the policy file is unreadable or invalid by keeping enterprise mode on, clearing every pinned value, blocking network access, hiding built-in skill catalogs, and reporting a policy error. |
| FR-5 | Must | The system shall watch the effective policy and notify consumers when it changes without requiring a restart, with a stoppable timer that does not keep the process alive. |
| FR-6 | Must | The system shall expose a public policy projection to the UI and VS Code webview containing only the mode, source, organization, policy error, network block state, and pinned OpenCode binary. |
| FR-7 | Must | The system shall refuse OpenCode provider-connect and credential-list route variants in enterprise mode and outside it, while allowing MCP sign-in and credential management routes that do not reach those handlers. |
| FR-8 | Must | The system shall block network-exposed bind hosts in enterprise mode unless the policy explicitly allows network access, and shall require UI authentication or an explicit risk opt-in before serving an unauthenticated LAN bind. |
| FR-9 | Must | The system shall decide browser origins from packaged client origins, development origins only in development, the request host and forwarded host, and a validated stored `publicOrigin`, and shall return that decision as a promise on every path. |
| FR-10 | Must | The system shall refuse an opaque `Origin: null` and a foreign browser origin on socket upgrades even when no UI password is set, while accepting clients that send no origin. |
| FR-11 | Must | The system shall read the UI session cookie from the slot matching the request host and port, without borrowing a cookie belonging to another instance on the same host. |
| FR-12 | Must | The system shall build a `frame-ancestors` policy that allows the app and packaged shells, adds development origins only in development, and accepts only plain origins or the explicit wildcard from configured additions. |
| FR-13 | Must | The system shall reject a WebSocket upgrade with an HTTP status line and then destroy the socket, including when writing the rejection fails. |
| FR-14 | Should | The system shall derive a rate-limit key from the peer address, relay provenance, and forwarded hops only when the previous hop is a trusted proxy. |
| FR-15 | Must | The system shall load the public policy in the UI with schema validation, a generation guard against stale responses, and a reset on runtime change. |
| FR-16 | Must | The system shall let a user review and remove previously trusted app-link schemes in Settings, with an empty state when none are trusted. |
| FR-17 | Should | The system shall accept an `OPENCHAMBER_LAN_URL` override only as an HTTP or HTTPS origin and shall warn and ignore malformed values. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Pinned relay and Jev URLs, Jev model and API key, extension lists, and local-extension switches shall never appear in a client-facing policy payload. |
| NFR-2 | Must | Reliability | Invalid headers and failed settings reads shall fail closed or preserve request-derived candidates, and an origin decision shall reject its promise instead of throwing synchronously. |
| NFR-3 | Must | Compatibility | A failed parse, unreadable settings, or absent policy file shall not remove origins derived from the current request, and origin checks shall be awaited by consumers through the `RequestOriginChecker` contract. |
| NFR-4 | Must | Security | Route matching shall mirror OpenCode's case-insensitive, separator-flexible, percent-decoding router and shall refuse dot segments and malformed escapes. |
| NFR-5 | Should | Compatibility | Policy and request-security helpers shall stay shared by the web server, the CLI, and the VS Code extension host without new runtime dependencies. |
| NFR-6 | Should | Usability | Settings text shall use localized strings and existing theme tokens. |

## Constraints

- The policy file lives outside the application install and is read on every policy evaluation.
- The machine user can read the policy file, so an administrator accepts the risk before putting an API key in it.
- `opencodeBinary` and `hideBuiltinSkillCatalogs` are file-only settings with no environment variable.
- `OPENCHAMBER_ALLOW_UNAUTHENTICATED_LAN` requires the literal value `true`.
- Packaged client origins are `openchamber-ui://app`, `capacitor://localhost`, and `https://localhost`.
- OpenCode policy configuration is the authoritative lock on which providers may be used, and this feature closes only the paths exposed by OpenChamber.
- Changes apply to a running instance through polling, with a 15-second default interval.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Policy paths are fixed per platform
      Given a platform of darwin, linux, or win32
      When the policy paths are resolved
      Then macOS uses /Library/Application Support/OpenChamber/policy.json
      And Linux uses /etc/openchamber/policy.json
      And Windows uses C:\ProgramData\OpenChamber\policy.json first

    @FR-1
    Scenario: A Windows ProgramData redirect cannot hide the policy
      Given ProgramData points to D:\Elsewhere
      And the fixed path enables enterprise mode while the redirected path disables it
      When the policy is read
      Then the fixed path is read first and enterprise mode stays on

    @FR-1
    Scenario: Windows falls back to a redirected ProgramData
      Given the fixed path is absent
      And D:\ProgramData\OpenChamber\policy.json enables enterprise mode
      When the policy is read
      Then enterprise mode is on from the redirected path
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: A file turns enterprise mode on
      Given a policy file with enterpriseMode true
      When the policy is read
      Then enterpriseMode is true and source is policy-file

    @FR-2
    Scenario: The environment cannot turn a file policy off
      Given a policy file with enterpriseMode true
      And OPENCHAMBER_ENTERPRISE_MODE is 0
      When the policy is read
      Then enterpriseMode is true

    @FR-2
    Scenario: The environment turns it on when the file leaves it off
      Given a policy file with enterpriseMode false
      And OPENCHAMBER_ENTERPRISE_MODE is 1
      When the policy is read
      Then enterpriseMode is true and source is environment

    @FR-2
    Scenario: A governing file ignores user-settable pins
      Given a policy file with enterpriseMode true
      And environment variables for relay, Jev, network access, and extensions
      When the policy is read
      Then the relay URL, Jev, and network access are unset
      And the allowed extension list is empty
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Valid policy values are trimmed and applied
      Given a policy file with whitespace around organization and opencodeBinary
      When the policy is read
      Then both values are trimmed and retained

    @FR-3
    Scenario: A byte-order mark and unknown keys are tolerated
      Given policy text beginning with a byte-order mark and an unknown future key
      When the policy is read
      Then policyError is null and the known values apply

    @FR-3
    Scenario: A Jev object without a URL is rejected
      Given a policy file with jev.model but no jev.url
      When the policy is read
      Then the file is invalid and no Jev values are pinned

    @FR-3
    Scenario: More than 200 allowed extensions are rejected
      Given a policy file with 201 allowed extension entries
      When the policy is read
      Then the file is invalid and no extensions are pinned
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Invalid JSON fails closed
      Given a policy file with malformed JSON
      When the policy is read
      Then enterpriseMode is true and source is policy-file
      And policyError names the file path
      And relayUrl, jev, and opencodeBinary are null
      And networkAccessBlocked is true and hideBuiltinSkillCatalogs is true

    @FR-4
    Scenario: An unreadable file fails closed
      Given a policy file that raises a permission error
      When the policy is read
      Then enterpriseMode is true
      And policyError contains the permission error

    @FR-4
    Scenario: A broken file never lifts network blocking
      Given a policy file with an invalid boolean for allowNetworkAccess
      And a network exposure check
      When network access blocking is evaluated
      Then network access stays blocked
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A policy change triggers one notification
      Given a watcher with a one-second interval and a read function that changes on the third call
      When three intervals elapse
      Then the change callback has been called once

    @FR-5
    Scenario: An unchanged policy triggers no notification
      Given a watcher whose read function returns the same policy
      When several intervals elapse
      Then the change callback has not been called

    @FR-5
    Scenario: Stopping the watcher ends polling
      Given a started watcher
      When its stop function is called and time advances
      Then no further reads occur
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: The public policy includes only safe fields
      Given a policy with an organization and a pinned OpenCode binary
      When the public projection is read
      Then it contains enterpriseMode, source, organization, policyError, networkAccessBlocked, and opencodeBinary
      And it contains no other fields

    @FR-6
    Scenario: The webview receives the public policy
      Given the GET /api/openchamber/enterprise-policy route
      When the UI store fetches it
      Then the response is parsed with the public policy schema
      And a 404 response yields the no-policy state
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Provider connect paths are refused
      Given a POST to /api/integration/openai/connect/key
      When enterprise mode classifies the request
      Then it is a provider-connect request and the route answers 403 enterprise_mode

    @FR-7
    Scenario: Obfuscated provider paths are still refused
      Given POST paths with mixed case, doubled separators, backslashes, percent escapes, or a semicolon suffix
      When they are classified
      Then each is a provider-connect request

    @FR-7
    Scenario: MCP sign-in is allowed
      Given a POST to /api/integration/mcp_0123456789abcdef/connect/oauth or its attempt completion path
      When it is classified
      Then it is not a provider-connect request

    @FR-7
    Scenario: Credential list variants are refused
      Given GET or HEAD requests to /api/credential in any router-equivalent spelling
      When they are classified
      Then each is a credential-list request and the route answers 403 credential_list_refused

    @FR-7
    Scenario: Credential management is left alone
      Given POST, PATCH, or DELETE requests to credential routes and GET requests to other paths
      When they are classified
      Then none is a credential-list or provider-connect request
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Enterprise mode refuses a network bind
      Given enterprise mode with allowNetworkAccess false
      And an effective bind host of 0.0.0.0
      When the server starts
      Then startup refuses the bind with the network access blocked error

    @FR-8
    Scenario: An allowed policy permits a network bind
      Given enterprise mode with allowNetworkAccess true
      When the server starts on a network-exposed host
      Then the enterprise block does not apply

    @FR-8
    Scenario: Only proven loopback hosts count as local
      Given bind hosts localhost, 127.25.1.2, ::1, and ::ffff:127.0.0.1
      When they are classified
      Then all are loopback
      And wildcard, LAN, link-local, and unknown hosts are network-exposed

    @FR-8
    Scenario: Unauthenticated LAN binding needs an explicit opt-in
      Given a network-exposed bind host and no UI password
      When OPENCHAMBER_ALLOW_UNAUTHENTICATED_LAN is not the literal true
      Then the bind is refused with a message naming the password and opt-in options
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A packaged client origin is allowed
      Given an origin of openchamber-ui://app, capacitor://localhost, or https://localhost
      When the origin decision is requested
      Then the promise resolves to true

    @FR-9
    Scenario: A foreign origin is refused
      Given an origin of https://evil.example.com and a host of 192.168.1.130:1202
      When the origin decision is requested
      Then the promise resolves to false

    @FR-9
    Scenario: TLS ending before an HTTP proxy hop still works
      Given an origin of https://devchamber.example.com and a host of devchamber.example.com
      And x-forwarded-proto of http
      When the origin decision is requested
      Then the promise resolves to true

    @FR-9
    Scenario: A forwarded host does not trust an unrelated origin
      Given a host of 127.0.0.1:3000 and x-forwarded-host of devchamber.example.com
      When origins for devchamber.example.com and evil.example.com are checked
      Then the first resolves to true and the second to false

    @FR-9
    Scenario: A loopback alias matches its equivalent host
      Given a host of localhost:3000 and an origin of http://127.0.0.1:3000
      When the origin decision is requested
      Then the promise resolves to true

    @FR-9
    Scenario: A stored public origin is validated before use
      Given a stored publicOrigin of https://public.example/path
      And a request from that origin to an internal host
      When the origin decision is requested
      Then the promise resolves to true
      And a stored non-string or unparseable publicOrigin does not add a candidate
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: An opaque origin is refused on a socket
      Given a socket upgrade with Origin set to null
      When the upgrade is checked
      Then it is refused

    @FR-10
    Scenario: A foreign page cannot open a passwordless socket
      Given no UI password and an origin of https://evil.example.com
      When the passwordless socket check runs
      Then the promise resolves to false

    @FR-10
    Scenario: A non-browser client sends no origin
      Given no UI password and no Origin header
      When the passwordless socket check runs
      Then the promise resolves to true
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The cookie slot for the request port is read
      Given a host of 192.168.0.1:3001 and cookies for ports 3000 and 3001
      When the session cookie is extracted
      Then the token for port 3001 is returned

    @FR-11
    Scenario: A cookie for another port is not borrowed
      Given a host of 192.168.0.1:3001 and only a cookie for port 3000
      When the session cookie is extracted
      Then no token is returned

    @FR-11
    Scenario: A host without a port uses the bare cookie
      Given a host of 192.168.0.1 and a bare UI session cookie
      When the session cookie is extracted
      Then the bare token is returned

    @FR-11
    Scenario: A malformed escape keeps its raw value
      Given a cookie value with an invalid percent escape
      When the session cookie is extracted
      Then the raw value is returned instead of throwing
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: The default frame ancestors contain only app and packaged origins
      Given no development flag and no extra origins
      When the policy is built
      Then it contains self, openchamber-ui://app, capacitor://localhost, and https://localhost

    @FR-12
    Scenario: Development origins are added only in development
      Given allowLocalDevOrigins false and then true
      When the policy is built each time
      Then only the development build contains http://127.0.0.1:* and http://localhost:*

    @FR-12
    Scenario: Only plain origins or the wildcard are accepted as additions
      Given extra origins of https://dash.example.com and *
      When the policy is built
      Then both are appended
      And a string carrying a directive such as script-src is not appended
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: A rejected upgrade writes a status line and destroys the socket
      Given a writable socket
      When an upgrade is rejected with 403 and a reason
      Then a valid HTTP/1.1 response is written
      And the socket is destroyed

    @FR-13
    Scenario: An unknown status code falls back to Bad Request
      Given a writable socket
      When an upgrade is rejected with 503
      Then the status text is Bad Request

    @FR-13
    Scenario: Write and destroy failures are tolerated
      Given a socket whose write and destroy functions throw
      When an upgrade is rejected
      Then no exception escapes and the rejection path completes
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Relay traffic gets a stable rate-limit key
      Given a loopback peer with relay provenance
      When the key is derived
      Then the key is relay

    @FR-14
    Scenario: Forwarded hops are trusted only from a trusted proxy
      Given an untrusted peer and an x-forwarded-for chain
      When the key is derived
      Then the peer address is kept
      And a configured trusted proxy allows the last valid forwarded address to be used
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: A valid policy response is stored
      Given a 200 response with a valid public policy body
      When the UI store loads
      Then the store fields match the response

    @FR-15
    Scenario: A failed or stale load does not overwrite current state
      Given a non-404 error response and an older in-flight load that resolves later
      When both loads settle
      Then the warning is logged and the older response is ignored

    @FR-15
    Scenario: A runtime reset clears the policy
      Given a populated enterprise policy store
      When resetForRuntime is called
      Then all policy fields return to the no-policy values

    @FR-15
    Scenario: Enterprise mode combines both sources
      Given a false policy flag and a true routing flag
      When enterprise mode is read
      Then it is true
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Trusted schemes are listed with a remove control
      Given two trusted app-link schemes
      When the Settings section renders
      Then each scheme is shown with scheme:// and a localized remove control

    @FR-16
    Scenario: Removing a scheme updates the trust store
      Given a listed trusted scheme
      When the user activates its remove control
      Then the scheme is removed through the trust store

    @FR-16
    Scenario: No trusted schemes shows the empty state
      Given an empty trusted scheme list
      When the Settings section renders
      Then the localized empty message is shown
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: A valid LAN URL is reduced to its origin
      Given OPENCHAMBER_LAN_URL of http://192.168.1.20:3000/
      When the advertised URL is read
      Then the result is http://192.168.1.20:3000 with no warning

    @FR-17
    Scenario: A non-origin LAN URL is ignored
      Given OPENCHAMBER_LAN_URL with a path, query, non-HTTP scheme, or bare address
      When the advertised URL is read
      Then the result is null and a configuration warning is logged

    @FR-17
    Scenario: An unset LAN URL is ignored silently
      Given no OPENCHAMBER_LAN_URL
      When the advertised URL is read
      Then the result is null and no warning is logged
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The public projection hides pinned secrets
      Given a policy with a relay URL, a Jev URL, model, and API key, and an extension allowlist
      When the public projection is produced
      Then none of those values appears in the payload or its serialized form

    @NFR-1
    Scenario: The UI schema rejects unexpected public fields
      Given a policy response containing pinned endpoints
      When the UI store parses the response
      Then only the declared public fields are retained
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A failed settings read keeps request-derived origins
      Given a settings reader that throws
      And a request whose origin matches its own host
      When the origin decision is requested
      Then the promise resolves to true

    @NFR-2
    Scenario: Malformed forwarded-host headers reject instead of throwing synchronously
      Given an empty x-forwarded-host array
      When the origin decision is requested
      Then a promise is returned and it rejects with a TypeError

    @NFR-2
    Scenario: An invalid policy file still leaves a readable error
      Given a policy file with invalid JSON
      When the policy is read
      Then policyError describes the file path and the parse problem
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: The origin checker is asynchronous on every path
      Given a packaged origin and a settings-dependent origin
      When both checks are started
      Then each return value is a Promise before it is awaited

    @NFR-3
    Scenario: A consumer that awaits the check sees the decision
      Given a socket upgrade path using RequestOriginChecker
      When the origin decision resolves to false
      Then the upgrade is rejected rather than treated as allowed
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Unsafe path spellings fail closed
      Given provider or credential paths with a dot segment or malformed percent escape
      When they are classified
      Then each is treated as a protected request

    @NFR-4
    Scenario: Paths OpenCode does not route to the protected handler are left alone
      Given encoded separators that resolve to a different first segment
      When they are classified
      Then they are not treated as protected requests
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The same helpers serve each runtime
      Given the web server and the VS Code extension host
      When either needs a policy or route classification
      Then both import the shared enterprise-mode helper
      And no new dependency is added for policy parsing or origin decisions
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Settings text follows existing UI conventions
      Given the app-link security Settings section
      When the section renders
      Then every label and message comes from the i18n catalog
      And the section uses existing Settings and theme components
    ```

## Conflicts

None identified.

## Open Questions

None. The artifacts were reverse-engineered from the existing implementation, tests, and documentation.
