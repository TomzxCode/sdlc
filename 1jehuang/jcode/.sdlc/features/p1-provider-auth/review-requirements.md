---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-1 | "The system shall support logging in to multiple built-in providers, including Anthropic Claude, OpenAI/Codex, Gemini, Azure OpenAI, and OpenAI-compatible API-key providers." | The login catalog now also registers Jcode Subscription, Grok Build, Google, Bedrock, OpenRouter, Cursor, GitHub Copilot, Antigravity, Muse subscription, auto-import, and about 40 named OpenAI-compatible profiles (`crates/jcode-provider-metadata/src/catalog.rs`, `LoginProviderTarget` at `crates/jcode-provider-metadata/src/lib.rs:25-42`). | "The system shall support logging in to multiple built-in providers, including Anthropic Claude, OpenAI/Codex, Gemini, Azure OpenAI, Jcode Subscription, Grok Build, Google, and OpenAI-compatible API-key providers." |
| FR-5 | "The system shall store credentials securely (e.g. `~/.jcode/auth.json`, macOS Keychain) and support multiple accounts per provider." | jcode never writes to the Keychain. There is no keyring dependency in any manifest. The Keychain is read only when importing Claude Code's credentials (`crates/jcode-base/src/auth/claude.rs:728-772`). jcode's own stores are owner-only files: `~/.jcode/auth.json`, `~/.jcode/openai-auth.json`, `~/.jcode/gemini_oauth.json`, `~/.jcode/antigravity_oauth.json`, plus `~/.config/jcode/*.env` for API keys (`crates/jcode-base/src/auth/claude.rs:295`, `codex.rs:111`, `gemini.rs:192`, `antigravity.rs:124`; hardening at `crates/jcode-storage/src/lib.rs:550-570`). | "The system shall store credentials securely in owner-only files under `~/.jcode/` (e.g. `auth.json`, `openai-auth.json`, `gemini_oauth.json`, `antigravity_oauth.json`) and `~/.config/jcode/*.env` for API keys, and support multiple accounts per provider." |
| FR-8 | "The system shall support experimental CLI providers (Cursor, GitHub Copilot, Antigravity) and named OpenAI-compatible provider profiles." | Cursor, GitHub Copilot, and Antigravity carry no experimental gate in the catalog (`crates/jcode-provider-metadata/src/catalog.rs:1145-1213`). The only experimental provider is Muse subscription, gated by `JCODE_EXPERIMENTAL_MUSE_SUBSCRIPTION=1` (`crates/jcode-base/src/auth/muse.rs:64,108-120`). | "The system shall support CLI-backed providers (Cursor, GitHub Copilot, Antigravity), the experimental Muse subscription device flow, and named OpenAI-compatible provider profiles." |

## Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-10 | The system shall maintain an auto-switch account pool and retry a turn on the next pool account when the active one hits a usage limit. | `crates/jcode-base/src/auth/account_pool.rs:16-26` (`~/.jcode/account-pool.json`), `crates/jcode-provider-core/src/failover.rs:72-146` (`classify_failover_error_message`), `crates/jcode-app-core/src/server/turn_failover.rs:1-21,48-115` (server-side retry for Desktop and SDK clients). |
| FR-11 | The system shall let the user reauthenticate a saved account from the login picker and show saved accounts, cached quotas, and available resets in the startup account router. | `crates/jcode-tui/src/tui/app/auth_account_picker_saved_accounts.rs:5-65,69-98,138-179`, `crates/jcode-tui/src/tui/ui_header/account_router.rs:101-199`. |
| FR-12 | The system shall support device-code login flows and explicit credential import, and shall refuse to import into a symlinked or foreign-provider store. | `src/cli/login/device_login.rs:1-70`, `src/cli/login/jcode_device.rs:109-214`, `src/cli/auth_import.rs:1-40`, `crates/jcode-base/src/auth/transfer.rs:1-24,478,521`. |
| FR-13 | The system shall provide a strict provider and model diagnostic tier that walks catalog, picker, switch, chat, stream, and tool checkpoints. | `src/cli/args.rs:515-530` (`jcode provider-doctor`, alias `provider-strict-e2e`), `src/cli/provider_doctor.rs:1-30`, `crates/jcode-provider-doctor/src/provider_e2e.rs`. |

## Conflicts

| Requirements | Type | Description | Suggested Resolution |
|---|---|---|---|
| FR-5, NFR-1 | Direct contradiction | FR-5 names the macOS Keychain as a jcode storage backend, but NFR-1 forbids reading credential files through symlinks and the code never writes to the Keychain. | Reword FR-5 to name the owner-only file stores, and describe the Keychain only as a read-only external source. |

## Open questions

None outstanding; the remaining unknown is how the auto-switch pool should be surfaced and ordered in the TUI beyond the startup account router.

## Testability

The acceptance criteria list covers FR-1 through FR-9 and NFR-1 through NFR-4, but the coverage matrix in `tests.md` has no row for FR-2, FR-3, FR-5, FR-8, FR-9, NFR-2, NFR-3, or NFR-4.
Each added FR needs at least one Gherkin acceptance criterion.

## Feasibility

No issues found.
