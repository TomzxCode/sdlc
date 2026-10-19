---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "driven by CLI commands in `src/cli/login/`, `src/cli/account.rs`, `src/cli/auth.rs`, and `src/cli/auth_test/`" | `src/cli/auth.rs` no longer exists. `jcode auth status` and `jcode auth doctor` live in `src/cli/commands/report_info.rs:157,215`, dispatched at `src/cli/dispatch.rs:398-405`. `AuthCommand` is defined in `src/cli/args.rs:961-992`. | Replace `src/cli/auth.rs` with `src/cli/commands/report_info.rs` (`jcode auth status` and `jcode auth doctor`). |
| Architecture map | row `src/cli/auth.rs  ─┤` | Same as above. | Replace the row. |
| Architecture map | row `src/cli/auth_test ┘` | The tree is `src/cli/auth_test.rs` (a 16-line `include!` aggregator for `auth_test/{types,run,probes,choice}.rs`) plus the `src/cli/auth_test/` directory. | Reword as `src/cli/auth_test.rs + src/cli/auth_test/`. |
| Architecture map | the `jcode-base/src/auth/` module list | Missing `grok_build.rs`, `muse.rs`, `google_oauth.rs`, `google/setup.rs`, `account_pool.rs`, `account_store.rs`, `lifecycle.rs`, `lifecycle_activation.rs`, `transfer.rs`, `active_method.rs`, `env_facts.rs`, `integration.rs`, `login_diagnostics.rs`, `login_ui.rs`, `refresh_state.rs`, `status_detail.rs`, `status_types.rs`, `validation.rs`, `commands.rs`, `test_sandbox.rs`. | Add rows for the subscription and device-code logins, the account pool and store, the lifecycle modules, and the credential transfer. |
| Architecture map | storage line names "macOS Keychain" | jcode only reads Claude Code's Keychain item; it never writes there. | Name the owner-only files under `~/.jcode` and `~/.config/jcode`, and list external CLI stores (including Claude Code's Keychain item) as read-only import sources. |
| Data Models | one "Auth State" table with `provider_key`, `account`, `credential`, `source` | No such struct exists. The real contracts are `AuthStatus` and `ProviderAuthAssessment` (`crates/jcode-base/src/auth/status_types.rs:14-95`), `AuthState` and `AuthCredentialSource` (`crates/jcode-auth-types/src/lib.rs:5-39`), `AnthropicAccount` and `JcodeAuthFile` (`crates/jcode-base/src/auth/claude.rs:60-93`), and `AccountPool` (`crates/jcode-base/src/auth/account_pool.rs:16-26`). | Replace the table with the four real models. |
| Technical Decisions | "Auth lives in `jcode-base`" | The contract now spans `jcode-auth-types` (shared enums), `jcode-provider-metadata` (login catalog), `jcode-provider-env` (API-key env store), `jcode-azure-auth` (Entra ID token), and `jcode-provider-doctor` (diagnostics). | Reword to describe the split by dependency layer. |
| Technical Decisions | "Multiple storage backends \| Files + macOS Keychain" | jcode owns only hardened files. | Reword to "Files (owner-only) plus external app stores", noting that other tools' stores are read-only import sources. |
| API Contracts | `jcode login` flag list | Missing `--flow-id` (`src/cli/args.rs:246-247`), `--cancel` (`:250-251`), and the flattened `GoogleLoginArgs` flags `--google-services`, `--setup`, `--google-client-json` (`src/cli/args/google.rs:20-32`). | Add the missing flags. |
| API Contracts | "`--print-auth-url` \| Prints the URL and waits for `--auth-code` to complete the flow." | The flags conflict: `print_auth_url` declares `conflicts_with_all = ["callback_url", "auth_code"]` (`src/cli/args.rs:226`). Completion happens in a later invocation via `--complete`, `--callback-url`, or `--auth-code` (`src/cli/login/scriptable.rs:882-990`). | Reword: "Prints a script-friendly auth URL and persists pending login state; a later invocation completes it with `--complete`, `--callback-url`, or `--auth-code` (these conflict with `--print-auth-url`)." |
| API Contracts | `jcode auth-test` option list | Missing `--no-smoke`, `--no-tool-smoke`, `--prompt`, `--json`, `--output`, `--coverage-file`, `--coverage-limit` (`src/cli/args.rs:532-576`). | Add the missing options. |
| Out of Scope | "A hosted identity service for jcode accounts (the `jcode account` command is unrelated account/billing surface)." | Jcode account login is a first-class provider in the auth layer: `LoginProviderTarget::Jcode` (`crates/jcode-provider-metadata/src/lib.rs:27`), `AuthStatus::jcode` (`crates/jcode-base/src/auth/status_types.rs:16`), the device flow at `src/cli/login/jcode_device.rs:109-214`, the browser account login at `crates/jcode-base/src/account_login.rs`, and the `jcode account` commands at `src/cli/account.rs`. | Replace with: "Subscription checkout, plan management, and billing UI for the Jcode account. Account login is in scope: `jcode login jcode` and `jcode account login` use the same auth layer." |

## Missing Information

- The device-code login sequence (GitHub Copilot, Muse subscription, Jcode account) is not documented; only "Browser OAuth login" is.
- `jcode auth import --provider <openai|claude> --stdin --json` is not in API Contracts.
- `jcode provider-doctor` (alias `provider-strict-e2e`) is not in API Contracts.
- The auth lifecycle path (login, validate, activate) in `crates/jcode-base/src/auth/lifecycle.rs` and `lifecycle_activation.rs` is not described.
- Google guided setup (`jcode login --setup`, `--google-client-json`, `crates/jcode-base/src/auth/google/setup.rs`, `docs/GOOGLE_GUIDED_SETUP.md`) is not described.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.
