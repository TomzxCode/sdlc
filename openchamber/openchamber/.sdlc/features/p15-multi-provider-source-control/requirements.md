---
title: "Multi-provider source control"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Requirements: Multi-provider source control

## Overview

OpenChamber needs source control workflows that work across GitHub, GitLab, Gitea, Gerrit, and Forgejo without naming a provider in shared UI code.
The feature introduces a provider registry, public descriptors, a generic HTTP route shell, provider-owned authentication and resource modules, and repository bindings that keep accounts and transport credentials separate.
The UI reads descriptors to render provider-specific labels, links, icons, reference prefixes, and terminology.
Extension providers join the same registry through `ext-<guestId>` identifiers.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| OpenChamber users | Review change requests, issues, and repository context from several source control hosts |
| Shared UI maintainers | Render provider-specific behavior without provider branches in components |
| Server maintainers | Keep one HTTP contract and one provider contract for all source control hosts |
| Extension authors | Add source control providers through the guest extension contract |
| Release maintainers | Keep behavior consistent across web, desktop, VS Code, hosted mobile, and Capacitor mobile |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall register built-in descriptors for GitHub, GitLab, Gitea, Gerrit, and Forgejo in that order. |
| FR-2 | Must | The system shall validate provider IDs against `^[a-z][a-z0-9-]{0,31}$` and reject reserved IDs, shell-route IDs, and duplicate IDs. |
| FR-3 | Must | The system shall publish public provider descriptors through `GET /api/source-control/providers`. |
| FR-4 | Must | The system shall derive UI labels, icons, reference prefixes, URLs, and terminology from provider descriptors. |
| FR-5 | Must | The UI shall keep a runtime provider list with a remembered snapshot, refresh state, and retry behavior. |
| FR-6 | Must | The server shall select and load provider implementations lazily through the provider registry. |
| FR-7 | Must | The server shall expose the generic provider shell endpoints for capabilities and authentication. |
| FR-8 | Must | The server shall expose bound read endpoints for change requests, references, review state, issues, labels, reviewers, and repository metadata. |
| FR-9 | Must | The server shall expose mutation endpoints for change requests, issues, comments, review threads, labels, reviewers, discussions, and state changes. |
| FR-10 | Must | The server shall reject unsupported provider operations with `501` and `SOURCE_CONTROL_CAPABILITY_UNSUPPORTED`. |
| FR-11 | Must | The system shall keep provider tokens in provider auth stores and persist bindings with references and redacted endpoint metadata only. |
| FR-12 | Must | The server shall resolve repository context and bindings through the shared binding service. |
| FR-13 | Must | The server shall normalize instances through each descriptor and keep instance aliases separate from default instances. |
| FR-14 | Must | The web adapter shall expose provider APIs to shared UI runtimes and fall back to built-in GitHub and GitLab descriptors for older servers. |
| FR-15 | Must | The source board shall resolve repository items through the provider registry and stamp each item with its provider identity. |
| FR-16 | Should | Extension providers shall register descriptors with `ext-<guestId>` IDs and mount routes under `/api/source-control/ext-*`. |
| FR-17 | Should | The system shall support multiple accounts per provider when the descriptor declares that capability. |
| FR-18 | Should | The server shall cache change request status by provider, instance, account, credential revision, binding revision, directory, branch, and remote, and allow force refresh. |
| FR-19 | Should | The UI shall support path-style projects and top-level projects for providers that declare path repositories. |
| FR-20 | Should | Providers shall map link templates and reference prefixes to their own change request and issue terminology. |
| FR-21 | May | The system shall support CLI authentication for providers that declare a CLI auth method. |
| FR-22 | May | The system shall support SSH URL inspection and updates for providers that declare SSH transport. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall redact secrets in bindings, logs, and error messages. |
| NFR-2 | Must | Reliability | The system shall propagate failed provider lookups as errors and never return authoritative empty results. |
| NFR-3 | Must | Compatibility | Descriptor-driven clients shall work against older servers through the GitHub and GitLab fallback. |
| NFR-4 | Should | Performance | Status reads shall use a 90 second cache and a 12 second upstream timeout, and implementations shall load only when needed. |
| NFR-5 | Should | Availability | An unavailable provider shall fail its own routes without blocking another provider. |
| NFR-6 | Must | Integrity | Mutation replay shall use idempotency keys and reject conflicting key reuse with `409`. |

## Constraints

- GitHub-specific behavior stays in FEAT-0002-git-github-integration.
- This feature covers the provider-neutral layer and the GitLab, Gitea, Gerrit, and Forgejo implementations.
- OpenChamber has no persistent database, so bindings, aliases, and auth state live in JSON stores or memory.
- Shared UI code must work in web, desktop, VS Code, hosted mobile, and Capacitor mobile.
- Provider IDs `guest`, `link`, `external`, `repository`, and `linear` stay reserved in the UI schema.
- Provider tokens must not be written into repository bindings.
- No normative OpenAPI file exists for this feature.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first, then NFRs.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Built-in providers are listed in a fixed order
      Given a running OpenChamber server
      When the client requests GET /api/source-control/providers
      Then the response lists github, gitlab, gitea, gerrit, and forgejo in that order
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Invalid provider IDs are rejected
      Given a descriptor with the id "Guest"
      When the descriptor set validates the id
      Then registration fails with an invalid provider id error

    @FR-2
    Scenario: Reserved and shell-route IDs are rejected
      Given descriptors with the ids "guest", "binding", and "providers"
      When each descriptor is validated
      Then every registration fails
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Public descriptors are published
      Given a server with the built-in descriptors
      When the client requests GET /api/source-control/providers
      Then each response entry has an id, label, order, terminology, icon, repository rules, instance rules, auth methods, settings, URLs, and features
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: UI text and links follow the descriptor
      Given a descriptor with a change request term, reference prefixes, icon, and URL templates
      When the shared UI renders a repository item for that provider
      Then the labels, icon, prefixes, and links match the descriptor
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A failed refresh keeps the remembered list
      Given the UI has a remembered provider list
      When the provider read fails
      Then the UI status is stale and the remembered list stays available

    @FR-5
    Scenario: A failed first refresh retries
      Given the UI has no remembered provider list
      When the provider read fails
      Then the UI status is error and a delayed retry starts
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: An implementation loads on first use
      Given a request to a GitLab provider route
      When the registry needs the GitLab implementation
      Then the registry returns a loaded implementation
      And a later request reuses that implementation
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Capabilities combine static and dynamic values
      Given a connected GitHub instance
      When the client requests GET /api/source-control/github/capabilities
      Then the response contains descriptor capability flags and dynamic authentication capabilities

    @FR-7
    Scenario: Authentication routes answer for a provider
      Given a configured provider instance
      When the client requests auth status, auth accounts, or posts an auth token
      Then the route delegates to that provider implementation and returns its response
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: A bound status read uses trusted context
      Given a directory bound to a provider account and repository
      When the client requests GET /api/source-control/{provider}/pr/status
      Then the route supplies repository id, binding revision, primary remote, account, credential revision, and directory to the provider
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Reference reads are capability gated
      Given a provider whose descriptor disables the reference picker
      When the client requests GET /api/source-control/{provider}/references
      Then the route returns 501 with SOURCE_CONTROL_CAPABILITY_UNSUPPORTED
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A declared mutation runs through the executor
      Given a provider whose implementation lists /pr/create
      When the client posts a change request create body with an idempotency key
      Then the mutation executor records the mutation and returns the provider result
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: An unsupported mutation is rejected
      Given a provider whose implementation does not list /pr/merge
      When the client posts to /api/source-control/{provider}/pr/merge
      Then the response is 501 with SOURCE_CONTROL_CAPABILITY_UNSUPPORTED
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Tokens stay out of bindings
      Given a connected account with a provider token
      When a repository binding is persisted
      Then the binding contains references and redacted endpoint metadata only
      And the token remains in the provider auth store
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Managed and auxiliary bindings keep separate credentials
      Given a repository with a managed HTTPS transport and an auxiliary checkout
      When the binding is written
      Then the transport and auxiliary records hold separate opaque credential references
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Repository context resolves from a directory
      Given a directory with a stored repository binding
      When the client requests GET /api/source-control/repository-context
      Then the response contains provider, instance, account id, repository id, binding revision, and primary remote
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Instances are normalized and aliased
      Given an instance alias for a non-default Forgejo host
      When the client requests GET /api/source-control/instances
      Then the alias appears with the normalized instance
      And default instances are not repeated as aliases
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: An older server uses the built-in fallback
      Given a server without GET /api/source-control/providers
      When the web adapter loads providers
      Then the adapter returns built-in GitHub and GitLab descriptors
      And it does not add descriptors for other providers

    @FR-14
    Scenario: A malformed descriptor list fails
      Given a server that returns a malformed provider list
      When the web adapter validates the response
      Then the adapter raises an error and returns no descriptor list
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Source board items carry provider identity
      Given a source board repository with a bound GitLab project
      When the board loads an issue and a merge request
      Then each item carries provider id, instance, and account identity
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: An extension provider is mounted
      Given an extension guest with id "acme"
      When its source control descriptor and implementation are registered
      Then the provider id is ext-acme
      And its routes answer under /api/source-control/ext-acme
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: The active account changes
      Given a provider with multipleAccounts and two connected accounts
      When the client posts /auth/activate for the second account
      Then later bound reads use the second account
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Repeated status reads reuse the cache
      Given a cached change request status for the same context
      When the client repeats the read within 90 seconds
      Then the server returns the cached status

    @FR-18
    Scenario: Force refresh and invalidation clear the cache
      Given a cached change request status
      When the client requests force refresh or an account is invalidated
      Then the next read calls the provider again
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: A top-level path project is linked
      Given a path-style provider with a top-level project
      When the UI builds a repository link and thread key
      Then both use the project path from the descriptor rules
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Provider terminology is rendered
      Given descriptors that declare different change request terms and issue prefixes
      When the UI renders items from both providers
      Then each provider uses the term and prefix from its descriptor
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: CLI authentication reports status
      Given a provider that declares a CLI auth method
      When the client posts /auth/cli
      Then the response reports availability and disabled state from the provider implementation
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: SSH URL is read and written
      Given a provider that declares SSH transport
      When the client posts /auth/ssh-url with a valid string
      Then the provider stores the value and the response returns it

    @FR-22
    Scenario: SSH URL input is invalid
      Given a provider that declares SSH transport
      When the client posts /auth/ssh-url without a string
      Then the response is 400
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Sensitive values are redacted
      Given an error from a provider auth store or binding operation
      When the server logs the error
      Then tokens, credentials, and sensitive user data are redacted
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A failed lookup is preserved
      Given a provider lookup that fails
      When the client requests a bound read
      Then the response carries the failure
      And no completed empty result is reported as authoritative
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Shared UI works with an older server
      Given a UI runtime connected to a server without the provider descriptors route
      When the runtime loads source control providers
      Then GitHub and GitLab remain available through the adapter fallback
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Status reads use bounded caching
      Given an uncached change request status read
      When an upstream provider takes longer than 12 seconds
      Then the route stops the read and reports a timeout
      And a matching later read can use a fresh cache entry
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: One provider failure stays local
      Given a request for an unavailable provider
      When the client calls that provider route
      Then the response is 404 for that provider
      And other provider routes continue to answer
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Conflicting mutation replay is rejected
      Given a recorded mutation for an idempotency key
      When a different mutation uses the same key
      Then the response is 409 with SOURCE_CONTROL_MUTATION_CONFLICT
    ```

## Conflicts

None identified.

## Open Questions

1. None. This feature was documented from the implementation present during the 2026-11-23 sync.
