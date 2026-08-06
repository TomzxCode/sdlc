---
title: "Provider Authentication"
status: done
---

# Test Plan: Provider Authentication

## Scope

Covers provider login flows (OAuth and API key), auth status/diagnostics, external credential detection, and token refresh coordination. Out of scope: live tests against paid providers (guarded behind `live_tests`).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Login flow against a local HTTP test server for OpenAI-compatible providers | `tests/auth_login_flow.rs` with a local OpenRouter/OpenAI-compat server | Provider authenticated, session usable |
| TC-2 | Provider catalog invariants | `crates/jcode-base/src/provider_catalog_tests.rs` | Catalog entries valid and consistent |
| TC-3 | Registry behavior | `crates/jcode-base/src/registry_tests.rs` | Provider registration works |
| TC-4 | External credential review candidates | `crates/jcode-base/src/auth/*_tests.rs` | Detection and ask-before-read behave correctly |
| TC-5 | Refresh coordination | `crates/jcode-base/src/auth/refresh_coordinator.rs` tests | Concurrent refreshes deduplicate |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Provider matrix auth/endpoint sweep | `tests/provider_matrix.rs` | All configured providers behave per endpoint state |
| TC-7 | End-to-end auth validation suite | `scripts/test_auth_e2e.sh` | Each provider's login/refresh path passes |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Credential file is a symlink | Detection rejects it (never follows symlinks) |
| TC-9 | Expired token with concurrent requests | Token refreshed exactly once; requests share the result |
| TC-10 | One provider misconfigured | Other providers still work |

## Test Infrastructure

- Local HTTP test server for OpenAI-compatible login flows (used by `auth_login_flow.rs`).
- Script-based e2e suite (`scripts/test_auth_e2e.sh`).
- Live provider tests guarded behind `live_tests` and not run in CI by default.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-4 | TC-4, TC-8 |
| FR-6 | TC-5, TC-9 |
| FR-7 | TC-6, TC-7 |
| NFR-1 | TC-8 |
