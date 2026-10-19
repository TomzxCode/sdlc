---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-2 | `crates/jcode-telemetry-core/src/lifecycle.rs` | The file exists but contains zero test functions. The session-lifecycle coverage lives in `crates/jcode-telemetry-core/src/tests.rs` (`test_session_end_event_serialization`, `test_session_reason_labels`, `test_error_counters`). | Point TC-2 at `crates/jcode-telemetry-core/src/tests.rs` and name the three test functions; drop `lifecycle.rs` as a test file. |

## Missing Scenarios

The provider OAuth account email path (v0.97.0) has no coverage in the plan at all.
These test files exist and cover it:

- `crates/jcode-telemetry-core/src/oauth_account.rs` (in-module tests, about 11 cases: the preflight state machine, opt-out before and after the notice renders, strict email validation, the digest, and the 0600 marker and lease)
- `telemetry-worker/test/oauth-account.test.mjs` (12 tests, including the nightly retention that removes only expired private account records, and strict payload validation that rejects raw-email preflight and non-hashed values)

Other existing test files that cover this feature and are absent from the plan:

- `crates/jcode-telemetry-core/src/concurrency/tests.rs`
- `crates/jcode-telemetry-core/tests/session_creation_latency.rs`
- `telemetry-worker/test/concurrency.test.mjs`
- `telemetry-worker/test/model-pricing.test.mjs`
- `telemetry-worker/test/model-price-report.test.mjs`
- `telemetry-worker/test/usage-report.test.mjs`

## Quality

The existing entries (TC-1 core telemetry tests, TC-3 onboarding trace, TC-4 app-core telemetry tests, TC-5 app-core usage tests, TC-6 worker tests, TC-7 token-value tests) all still exist and remain accurate.

## Correctness

No issues found.

## Maintainability

No issues found.
