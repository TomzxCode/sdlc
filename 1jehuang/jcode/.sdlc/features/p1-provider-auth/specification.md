---
title: "Provider Authentication"
status: done
---

# Specification: Provider Authentication

## Overview

Auth is implemented in the `jcode-base` layer (crate `jcode-base/src/auth/`) and driven by CLI commands in `src/cli/login/`, `src/cli/account.rs`, `src/cli/auth.rs`, and `src/cli/auth_test/`. The login CLI orchestrates provider-specific flows: OAuth browser flows with a local callback server, API-key prompts, and external credential detection. Stored credentials live under `~/.jcode/` with platform-appropriate hardening (macOS Keychain where applicable), and a refresh coordinator deduplicates token refreshes. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
src/cli/login.rs ─┐
src/cli/login/   ─┼─► jcode-base/src/auth/ (per-provider modules)
src/cli/auth.rs  ─┤     ├─ claude.rs / codex.rs / gemini.rs / google.rs
src/cli/auth_test ┘     ├─ azure.rs / copilot.rs / cursor.rs / antigravity.rs
                         ├─ external.rs (external credential sources)
                         ├─ oauth.rs + refresh_coordinator.rs
                         └─ doctor.rs (auth diagnostics)
                          │
                          ▼
               ~/.jcode/auth.json, openai-auth.json,
               gemini_oauth.json, external CLIs' stores,
               macOS Keychain
```

## Data Models

### Auth State

| Field | Type | Constraints | Description |
|---|---|---|---|
| provider_key | string | PK | Identifier of the provider (e.g. `anthropic`, `openai`). |
| account | string | not null | Account label for multi-account support. |
| credential | object | not null | Provider-specific token/key material and metadata. |
| source | enum | not null | e.g. `oauth`, `api-key`, `external`. |

## API Contracts

### CLI: `jcode login [provider]`

Flags: `--account`, `--no-browser`, `--print-auth-url`, `--callback-url`, `--auth-code`, `--complete`, `--json`, `--no-validate`, `--api-base`, `--api-key`, `--api-key-env`, `--google-access-tier`.

**Behavior** | Description
|---|---|
| No browser flag | Opens the OAuth URL in the default browser and starts a local callback server. |
| `--print-auth-url` | Prints the URL and waits for `--auth-code` to complete the flow. |
| `--api-key` / `--api-key-env` | Validates and stores an API key directly. |

### CLI: `jcode auth status` / `jcode auth doctor`

Reports per-provider auth state and common failure causes.

### CLI: `jcode auth-test`

End-to-end auth validation with options `--login`, `--all-configured`, `--coverage`, `--context-audit`.

## Sequences

### Browser OAuth login

```
User → jcode login → open browser / print URL
User authorizes in browser
Provider → local callback server → auth code
jcode → token exchange → refresh_coordinator → store credential
jcode → validates token (unless --no-validate) → success
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Auth lives in `jcode-base` | Downward-closed foundational layer | All upper layers and the CLI can rely on auth without layering issues. |
| Per-provider modules | One module per provider | Isolates provider-specific OAuth quirks; experimental providers are clearly separated. |
| External credential reuse | Read other CLIs' auth files with consent | Lets users reuse subscriptions without maintaining duplicate tokens. |
| Refresh coordinator | Single coordinated refresh | Avoids concurrent double-refresh storms on shared tokens. |
| Multiple storage backends | Files + macOS Keychain | Balances portability with platform security. |

## Risks and Unknowns

1. External credential formats change without notice when upstream CLIs change.
2. OAuth callback flows are hard to test end to end in CI; most coverage relies on local HTTP test servers and API-key providers.

## Out of Scope

- A hosted identity service for jcode accounts (the `jcode account` command is unrelated account/billing surface).
- New experimental provider integrations beyond what the codebase already ships.
