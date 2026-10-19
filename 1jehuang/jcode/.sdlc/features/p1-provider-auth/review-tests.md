---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

The existing entries (TC-1 `tests/auth_login_flow.rs`, TC-2 `crates/jcode-base/src/provider_catalog_tests.rs`, TC-3 `crates/jcode-base/src/registry_tests.rs`, TC-4 `crates/jcode-base/src/auth/*_tests.rs`, TC-5 the refresh coordinator tests, TC-6 `tests/provider_matrix.rs`, TC-7 `scripts/test_auth_e2e.sh`, and the TC-8 to TC-10 edge cases) all still exist and remain accurate.

## Quality

The Test Infrastructure section claims live provider tests are "guarded behind `live_tests`".
There is no `live_tests` Cargo feature in any manifest.
`crates/jcode-base/src/live_tests.rs` is a coverage-ledger module (`JCODE_LIVE_TEST_LEDGER`, `JCODE_LIVE_TEST_COVERAGE`), not a test gate.
Live provider tests are `#[ignore]`d in the provider runtime crates (for example `crates/jcode-provider-openrouter-runtime/src/openrouter_tests.rs:1706` and `crates/jcode-provider-bedrock/src/tests.rs:508`).
Reword to: "Live provider tests are `#[ignore]`d in the provider runtime crates and are not run in CI by default; `crates/jcode-base/src/live_tests.rs` is the live-coverage ledger, not a test gate."

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-base/src/auth/tests.rs` (1090 lines, the main auth test module; the TC-4 glob does not match it)
- `crates/jcode-base/src/auth/oauth_tests/{mod,basic,flow,openai_refresh_deadline}.rs`
- `src/cli/login/tests.rs` and `src/cli/login/existing_key_notice_tests.rs`
- `src/cli/auth_test/choice.rs:195-671` (auth-test target resolution)
- `crates/jcode-base/src/auth/transfer.rs:1016-1090` (credential transfer and symlink refusal)
- `crates/jcode-base/src/auth/account_pool.rs` and `crates/jcode-provider-core/src/saved_account_route_tests.rs` (account pool and saved-account routing)
- `crates/jcode-base/src/provider/tests/account_failover.rs` (account failover attribution)
- `crates/jcode-provider-doctor/src/lifecycle_driver.rs:966-1060` (provider switch and reauth matrix)
- `tests/test_auth_import_cli.py` and `tests/test_login_qr_cli.py`
- `scripts/auth_regression_matrix.sh`
- `crates/jcode-base/src/account_login/tests.rs`

## Correctness

No issues found.

## Maintainability

No issues found.
