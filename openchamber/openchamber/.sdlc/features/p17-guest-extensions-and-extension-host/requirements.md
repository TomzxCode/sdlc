---
title: "Guest extensions and extension host"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Requirements: Guest extensions and extension host

## Overview

Third-party panels need to run inside OpenChamber without sharing the app origin, session credentials, or native bridges.
The feature publishes a guest SDK, installs app-owned and user-installed extensions, parses their manifests, brokers guest API calls, renders guest surfaces, and coordinates extension waits.
The host keeps authority over installation, approval, network access, local processes, and session writes.
Extensions run on web, desktop, and the mobile clients connected to an OpenChamber server.
VS Code does not load them.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Extension authors | A small published SDK, a stable manifest, and a documented host API for panels and background services. |
| End users | Install, approve, use, pause, and remove extensions from Settings without exposing their credentials. |
| Agents | Declare waits on extension-owned conditions and receive one wake message when a condition fires. |
| OpenChamber maintainers | One shared contract in `packages/sdk`, bounded runtime behavior, and consistent behavior across surfaces. |
| Enterprise administrators | Allow only approved extension sources and keep sensitive capabilities refused. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall publish `@openchamber/sdk` as the guest contract with `connectHost`, wire types, and pure helpers, and `@openchamber/sdk/schemas` as the host-facing manifest and message parsers. |
| FR-2 | Must | The system shall install extensions from an absolute folder, a local or HTTPS ZIP, an HTTPS or SSH Git URL, or the app-owned built-in registry, and expose a per-instance catalog. |
| FR-3 | Must | The system shall parse the `openchamber` manifest from `package.json` or a bare block, validate declared contributions, and fail installation on invalid manifests, missing built scripts, or an unsupported host version. |
| FR-4 | Must | The system shall derive requested capabilities from the manifest, require the user to grant the exact set, and narrow stored grants when the package's declared scope changes. |
| FR-5 | Must | The system shall serve package files from a confined path behind a scoped frame grant with a sandbox CSP, and support the legacy scoped token and relay documents for older and tunneled clients. |
| FR-6 | Must | The system shall open a guest connection with `hello`, answer with `ready` and the host context, and correlate later guest calls and host results by id with a request timeout. |
| FR-7 | Must | The system shall expose host calls for workspace and session projection, storage, compose, attach, session start, prompts, toasts, service access, files, generation, status controls, popovers, blocks, and microphone capture. |
| FR-8 | Must | The system shall render active guests as rail panels, dialogs, full-screen pages, status sections, file editors, UI blocks, popovers, and shared surfaces, with folder scope and phone opt-ins. |
| FR-9 | Must | The system shall spawn a host-owned local service on first use, proxy guest requests to it over loopback, report service status, and stop it on pause, withdrawal, removal, or shutdown. |
| FR-10 | Must | The system shall register service roles declared through `provides` (browser, source-control, notifications, tracker, quota, and opencode) and withdraw them when the guest deactivates. |
| FR-11 | Must | The system shall let an agent start, list, and stop waits, poll the extension service for declared wait types, and deliver one synthetic wake message to the session when a wait fires. |
| FR-12 | Must | The system shall announce catalog, mark, and extension-wait changes on the control stream and let the UI reload the affected projection. |
| FR-13 | Must | The system shall gate network, filesystem, service, transcript, session-control, instruction, skill, and plugin capabilities by enterprise policy, and reserve the `openchamber-builtin-` id prefix. |
| FR-14 | Must | The system shall keep web, desktop, and server-backed mobile behavior aligned, and report extensions as unsupported in VS Code and isolated spaces instead of as an empty list. |
| FR-15 | Should | The system shall provide integrations with OAuth or pasted tokens, declared settings, instance and device storage, and optional folder limits from Settings. |
| FR-16 | Should | The system shall check Git installs for newer package versions and refresh them while keeping grants, tokens, settings, pause state, and installation identity. |
| FR-17 | Should | The system shall document the SDK, installation, guest services, and extension waits for authors and users, alongside per-package ownership documentation. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall keep secrets on the server, confine guest file paths to the package root, refuse undeclared origins and scopes, and never place a runtime bearer credential in a frame. |
| NFR-2 | Must | Availability | The system shall treat an unreadable catalog or failed fetch as failure, not as an empty result, and one broken extension or catalog row shall not block unrelated extensions. |
| NFR-3 | Must | Performance | The system shall bound guest requests, storage, uploads, waits, and frame documents with the limits defined in the SDK and server modules. |
| NFR-4 | Must | Compatibility | The system shall keep the wire channel and API version at 1, accept manifest `apiVersion` 1, check `engines.openchamber`, and parse optional fields defensively for older and newer hosts. |
| NFR-5 | Should | Observability | The system shall report lifecycle listener failures in logs, keep monotonic catalog and wait revisions, and never log tokens, bearer values, file contents, prompts, or archive contents. |
| NFR-6 | Should | Maintainability | The system shall define guest types once in `packages/sdk`, keep UI policy in the UI module and server policy in the server modules, and record ownership in per-package documentation. |

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: A panel imports the published contract
      Given an extension bundles `@openchamber/sdk`
      When it calls `connectHost` and imports a guest type
      Then the bundle resolves the guest entry without a schema library
      And the host validates the same messages with `@openchamber/sdk/schemas`
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Install from a folder and a Git URL
      Given an OpenChamber data directory with no such extension
      When the user installs a local folder and then a Git URL with a semver package
      Then the catalog lists both with their source and version
      And each data directory keeps its own catalog
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Invalid packages fail installation
      Given a package with an unknown `apiVersion` or a script that was never built
      When the user installs it
      Then the install answers `invalid-manifest` or `missing-build`
      And no catalog row is added
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Approval covers the declared scope
      Given an extension that declares `filesystem` patterns and a `service`
      When the user grants its full requested capability list
      Then the catalog marks it active
      And a later package version with widened patterns is shown as needing approval
      And proxies refuse the widened grant until the dialog runs again
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A frame loads only its own files
      Given an installed extension with a panel entry
      When the host mints a frame grant and the frame requests its scripts
      Then the asset route serves files under that grant with `Content-Security-Policy: sandbox allow-scripts`
      And a path with `..` or a URL returns 404
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Guest connect
      Given a sandboxed frame with an installed `connectHost` client
      When the guest sends `hello`
      Then the host accepts only the parent frame and sends `ready` with theme, locale, directory, session, surface, connection, settings, and item
      And a later guest call receives a result with the same id or a typed error after the timeout
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A guest calls a host capability
      Given an active guest with the required grant
      When it calls `compose`, `serviceRequest`, or `readFile`
      Then the host bridge answers with a result through `HostBridgeEffects`
      And an unapproved or malformed call answers with `NOT_GRANTED`, `BAD_PATH`, or `UNSUPPORTED`
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Scope and phone opt-in
      Given a guest with `folders` and a panel without `mobile`
      When the user opens a project outside those folders on a phone
      Then no rail or attach surface for that guest is shown
      And a guest with `page.mobile` shows its full-screen page there
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Service starts on demand and stops on pause
      Given an approved extension that declares `contributes.service`
      When the guest sends its first `service-request`
      Then the host spawns the process and proxies to loopback
      And pausing the extension stops the process and later requests answer `DISABLED`
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A browser role is handed back
      Given an extension providing `browser` that is enabled and approved
      When the user withdraws its approval
      Then the host role is withdrawn and an activation or deactivation event is announced
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A wait fires once
      Given an agent has started a declared wait on an approved extension
      When the service answers `/waits/check` with `fired: true`
      Then one synthetic steer message is posted to that session
      And the wait is removed from the composer and the wake is not sent twice
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A pause updates every client
      Given several clients show the catalog and a session's waits
      When the user pauses an extension
      Then `openchamber:guests-changed` and `openchamber:extension-waits.updated` are broadcast with rising revisions
      And each client replaces its projection with the new snapshot
    ```

- [x] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Enterprise policy refuses a capability source
      Given enterprise mode with an allowlist that does not include a ZIP package
      When the user installs or approves that package
      Then the request is refused with `enterprise-mode`
      And a package from an allowed Git repository keeps only the grants the policy permits
    ```

- [x] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Runtime parity and unsupported hosts
      Given the same extension catalog on web, desktop, mobile clients, and VS Code
      When each host renders its extension surface
      Then web, desktop, and server-backed mobile show the extension
      And VS Code and isolated spaces report extensions as unsupported rather than empty
    ```

- [x] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Connect an account and keep device preferences
      Given an extension with OAuth and a secret integration setting
      When the user completes the callback and saves a device-scoped preference
      Then the iframe receives only `secretsSet`, the proxy uses the stored token
      And the preference stays in the renderer's partition keyed by runtime and installation identity
    ```

- [x] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Refresh a Git install
      Given a Git install whose origin has a newer semver version
      When the update check runs and the user updates
      Then the service stops before the package swap and the catalog row refreshes
      And grants, tokens, settings, pause state, and storage identity are preserved
    ```

- [x] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Authors find the contract
      Given an extension author reading the documentation
      When they open the SDK, extensions, guest services, and extension waits pages
      Then the manifest fields, host API, service contract, and wait wire format match `packages/sdk` and the server modules
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: A guest cannot reach a host credential
      Given a frame with an opaque origin and a running host service
      When the frame requests a script, a proxy call, or a file operation
      Then the asset grant holds only package files, the proxy adds only the declared token to the declared origin
      And no bearer, pairing credential, or secret setting appears in the frame message or the logs
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A broken row does not empty the catalog
      Given one installed row from a newer server and a failed catalog fetch
      When the renderer parses the response
      Then the unknown row is listed as unreadable and removable
      And the failed fetch reports an error instead of showing no extensions
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Resource budgets hold
      Given a guest sending requests, writing storage, or starting waits
      When values exceed the SDK and server caps
      Then the host rejects the call with the defined code, such as `RESPONSE_TOO_LARGE`, `TOO_MANY_MARKS`, or 409 for a full wait store
      And no oversized body or extra wait is accepted
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: A newer manifest is parsed defensively
      Given a host on SDK wire version 1 reading a row with an unknown optional field
      When the catalog is parsed
      Then that field is dropped and the row stays available
      And a manifest with `apiVersion: 2` is refused with `unsupported-api-version`
    ```

- [x] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Lifecycle failures are visible
      Given a deactivation listener that throws after a guest pause
      When the runtime settles the listeners
      Then the failure is logged, other listeners still run, and the stored pause is not reversed
    ```

- [x] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: One contract definition
      Given a contributor adding a guest request field
      When they change the guest and host sides
      Then both import the type from `packages/sdk`
      And the owning module documentation records the change
    ```

## Conflicts

None identified.

## Open Questions

None. The feature is already implemented and this document records the implemented behavior.
