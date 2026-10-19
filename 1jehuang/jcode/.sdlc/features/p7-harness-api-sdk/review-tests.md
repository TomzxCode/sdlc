---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

Two documented entries point at the wrong files:

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-5 | `crates/jcode-harness-api/src/capability_coverage.rs` | The file does not exist at that path. It is at `crates/jcode-harness-api/src/harness_api_tests/capability_coverage.rs`. | Correct the path. |
| TC-4 | "SDK connects, drives sessions, streams events" over `crates/jcode-sdk/src/sdk_tests/` | `crates/jcode-sdk/src/sdk_tests/` contains only `parity.rs` (capability parity) and `turn_retry.rs` (retry policy). The described behavior lives in `crates/jcode-sdk/tests/client_behavior.rs`, `crates/jcode-sdk/tests/lifecycle_events.rs`, `crates/jcode-sdk/tests/structured_output.rs`, `crates/jcode-sdk/tests/edit_stats.rs`, and `crates/jcode-sdk/tests/client_behavior/soft_interrupt_tests.rs`. | Split TC-4 into a parity entry over `crates/jcode-sdk/src/sdk_tests/parity.rs` and a behavior entry over the `crates/jcode-sdk/tests/` files. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-harness-api-server/src/runtime_command_compat_tests.rs` (v0.97.0 native runtime commands)
- `crates/jcode-harness-api-server/src/session_presence_tests.rs` (v0.98.0 session presence)
- `crates/jcode-harness-api-server/src/user_response_capability_tests.rs` (v0.98.0 `user_response` capability)
- `crates/jcode-harness-api-server/src/stdio_tests.rs` (stdio transport)
- `crates/jcode-harness-api-server/src/translate_tests/text_framing_tests.rs`
- `crates/jcode-harness-api/src/harness_api_tests/schema_snapshot.rs` and `crates/jcode-harness-api/src/harness_api_tests/swarm_metadata.rs`
- `crates/jcode-sdk/tests/user_response_capability.rs`
- `crates/jcode-sdk/src/sdk_tests/turn_retry.rs`, `crates/jcode-sdk/src/launch_upgrade_tests.rs`, `crates/jcode-sdk/src/shared_ssh_tests.rs`, `crates/jcode-sdk/src/ssh_integration_tests.rs`
- `sdk/typescript/test/runtime-commands.test.ts`, `session-presence.test.ts`, `user-response-capability.test.ts`, `tools.test.ts`, `model-usage.test.ts`, `text-framing.test.ts`, `pipe-name.test.ts`, `system-prompt.test.ts`, `error-docs.test.ts`
- `tests/api_stdio_cli.rs` (repository-level integration test for `jcode api --stdio`)

## Quality

The existing entries (TC-1 framing, TC-2 translate, TC-3 background progress, TC-6 TypeScript client tests, TC-7 schema parity, TC-8 and TC-9 shell scripts, TC-10 CI parity jobs) all still exist and remain accurate.

## Correctness

No issues found.

## Maintainability

No issues found.
