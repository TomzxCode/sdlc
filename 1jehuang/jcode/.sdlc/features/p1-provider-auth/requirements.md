---
title: "Provider Authentication"
status: done
---

# Requirements: Provider Authentication

## Overview

jcode lets users authenticate with a wide range of LLM providers so they can use existing subscriptions (Claude Max, ChatGPT Pro, Gemini) or API keys. The auth layer supports OAuth flows, API keys, Azure Entra ID, and reuse of external credentials (e.g. Codex or Claude CLI auth files), with a browser-based login flow driven from the CLI (`jcode login`). This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Low-friction login with their existing subscriptions, multi-account support, and clear auth status |
| Maintainer | Accurate provider catalog, diagnosable auth failures, testable login flows |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall support logging in to multiple built-in providers, including Anthropic Claude, OpenAI/Codex, Gemini, Azure OpenAI, and OpenAI-compatible API-key providers. |
| FR-2 | Must | The system shall support browser-based OAuth login for providers that require it, including printing an auth URL and running a local callback server. |
| FR-3 | Must | The system shall support API-key login for providers that accept keys, via interactive prompt, `--api-key`, or environment variable. |
| FR-4 | Must | The system shall detect and reuse external credentials from other CLIs (e.g. Codex auth.json, Claude .credentials.json) with ask-before-read and symlink rejection. |
| FR-5 | Must | The system shall store credentials securely (e.g. `~/.jcode/auth.json`, macOS Keychain) and support multiple accounts per provider. |
| FR-6 | Must | The system shall refresh expired tokens, coordinating refreshes so concurrent requests do not double-refresh. |
| FR-7 | Should | The system shall provide auth status and diagnostics (`jcode auth status`, `jcode auth doctor`) and end-to-end auth validation (`jcode auth-test`). |
| FR-8 | Should | The system shall support experimental CLI providers (Cursor, GitHub Copilot, Antigravity) and named OpenAI-compatible provider profiles. |
| FR-9 | May | The system shall allow scriptable login via printed auth URL and callback (`--print-auth-url`, `--callback-url`, `--auth-code`). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall never read credential files through symlinks. |
| NFR-2 | Must | Security | The system shall keep tokens out of logs and error output. |
| NFR-3 | Should | Availability | A failed or missing login for one provider shall not prevent using other providers. |
| NFR-4 | Should | Usability | The default provider shall be auto-detected from available credentials. |

## Constraints

- Must support both subscription-based (OAuth) and API-key-based providers in one auth model.
- Must run without a hosted auth service; callbacks are handled locally.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).

- [ ] **FR-1**
    - **Given** a clean `~/.jcode` with no auth
    - **When** the user runs `jcode login` for a supported provider and completes the flow
    - **Then** the provider appears as authenticated and usable for sessions
- [ ] **FR-2**
    - **Given** an OAuth provider selected for login
    - **When** the browser flow completes against the local callback server
    - **Then** the returned token is stored and a session can start with that provider
- [ ] **FR-3**
    - **Given** an API-key provider
    - **When** a key is provided interactively or via `--api-key`/environment variable
    - **Then** the key is validated and stored
- [ ] **FR-4**
    - **Given** an external credential file (e.g. `~/.codex/auth.json`)
    - **When** the user consents to reading it
    - **Then** the credential is used without copying it into jcode's own store
- [ ] **FR-5**
    - **Given** stored credentials
    - **When** the user lists accounts or starts a session
    - **Then** multiple accounts are selectable and the chosen one is used
- [ ] **FR-6**
    - **Given** an expired token
    - **When** a request needs the token
    - **Then** it is refreshed once and concurrent requests share the refreshed token
- [ ] **FR-7**
    - **Given** an installed jcode with configured providers
    - **When** the user runs `jcode auth doctor` or `jcode auth-test`
    - **Then** it reports each provider's auth state and pinpoints failures
- [ ] **FR-8**
    - **Given** a configured named provider profile or experimental provider
    - **When** the user logs in with that profile
    - **Then** the profile is usable for sessions
- [ ] **FR-9**
    - **Given** a headless environment
    - **When** the user runs login with `--print-auth-url` and later supplies the auth code
    - **Then** the login completes without opening a browser
- [ ] **NFR-1**
    - **Given** a symlink placed where a credential file is expected
    - **When** credential detection runs
    - **Then** the symlink is rejected and not followed
- [ ] **NFR-2**
    - **Given** a login or token-refresh failure
    - **When** error output is produced
    - **Then** no token or secret material appears in logs or stderr
- [ ] **NFR-3**
    - **Given** one misconfigured provider
    - **When** a session targets a different provider
    - **Then** the session succeeds regardless of the misconfigured provider
- [ ] **NFR-4**
    - **Given** exactly one set of credentials available
    - **When** jcode starts without a provider flag
    - **Then** the matching provider is auto-selected

## Conflicts

None identified yet.

## Open Questions

1. Which provider/account selection UX should win when multiple credentials are available for the same provider? The current behavior is inferred from code, not verified end to end.
