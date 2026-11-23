---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-10-19

### One named representative test no longer exists

- Status: BLOCKING
- Evidence:
  - The artifact's TC-U-runtime row lists `shared_authority_handoff_contract_matches_openclaw` as a representative case in `crates/openclaw-node-host/src/runtime.rs`.
  - `grep -rn "shared_authority_handoff" crates/` returns nothing, and no such identifier exists anywhere in the repository.
  - The corresponding test that exists today is `crates/openclaw-node-host/src/runtime.rs:1388` `shared_manifest_and_local_admission_match_openclaw`.
  - The cross-language contract that the old name referred to is still enforced on the TypeScript side: `src/infra/node-runtime-integration-contract.test.ts:1` opens with "Cross-language fixture pins the authority handoff shared with the Rust node runtime." and exercises `test/fixtures/node-runtime-integration-contract.json`.
- Artifact currently says: "| TC-U-runtime | `crates/openclaw-node-host/src/runtime.rs` | 17 | shared_authority_handoff_contract_matches_openclaw, enforces_input_and_output_limits, ... |"
- What the code actually does: the shared-authority contract assertion was renamed. A reader following the coverage map would grep for a test that is not there and would not find the replacement, which now lives in the runtime suite under a different name and is mirrored by the TypeScript-side contract test.
- Needed change: repoint the representative case at `shared_manifest_and_local_admission_match_openclaw` and note the TypeScript mirror.

### The per-file case counts no longer match the suites

- Status: ADVISORY
- Evidence:
  - Counting `#[test]` and `#[tokio::test]` attributes per file in `crates/openclaw-node-host/src/`: `duplex.rs` 1, `host.rs` 5, `identity.rs` 3, `lifecycle.rs` 3, `main.rs` 1, `node.rs` 6, `reconnect.rs` 13, `runtime.rs` 16, `sidecar_handshake.rs` 14, `sidecar_protocol.rs` 17, `sidecar_runtime.rs` 19. Total 98, not the stated 99.
  - The artifact's per-file counts disagree in three places: TC-U-protocol says 16 (actual 17), TC-U-runtime says 17 (actual 16), and TC-U-node says 7 (actual 6).
  - `crates/openclaw-gateway-client/src/lib.rs` has 3 test attributes and `src/session.rs` has 6, totaling 9, which matches the artifact's stated 9.
  - Integration suites: `crates/openclaw-node-host/tests/node_lifecycle.rs` has 1, `tests/node_session.rs` has 10, `tests/sidecar_process.rs` has 2; `crates/openclaw-gateway-client/tests/session.rs` has 22 and `tests/tls_policy.rs` has 4. All match the artifact.
- Artifact currently says: "Node-host unit suites live inline in `src/*.rs` (99 cases)" and the per-file table lists the counts above.
- What the code actually does: the suites were refactored, so three per-file counts and the total are off by one each. The integration counts are unchanged.
- Needed change: update the total to 98 and correct the protocol, runtime, and node rows.

### The two cross-language fixture contract tests are not listed

- Status: ADVISORY
- Evidence:
  - `src/infra/node-invoke-lifecycle-contract.test.ts:1` pins the invoke lifecycle against `test/fixtures/node-invoke-lifecycle-contract.json`, and `src/infra/node-runtime-integration-contract.test.ts:1` pins the authority handoff against `test/fixtures/node-runtime-integration-contract.json`.
  - Both files are in the conformance workflow's path filter: `.github/workflows/node-runtime-conformance.yml:17-18`, and the workflow runs them as a dedicated job at lines 120-132 ("Test shared node contracts").
  - The artifact's Test Infrastructure section names the six fixture files but lists only the Rust harnesses: "Mock Gateway WebSocket servers built with `tokio-tungstenite` inside the test suites", "Real child-process harness for the sidecar boundary test", and "`cargo test` across the workspace; no external services required".
- Artifact currently says: the fixture list includes `node-invoke-lifecycle-contract.json` and `node-runtime-integration-contract.json` but no TypeScript consumer is named, and the infrastructure list mentions only the Rust harnesses.
- What the code actually does: the two fixtures are consumed on both sides of the wire. The TypeScript consumers run in CI on every change to the listed paths, so a reader of the plan would not know that a TypeScript change can break the cross-language contract.
- Needed change: name the two TypeScript contract suites and the CI job that runs them.

### The "cargo test across the workspace" infrastructure line omits the fmt, clippy, and doc gates

- Status: ADVISORY
- Evidence:
  - `.github/workflows/node-runtime-conformance.yml:161` runs `cargo +1.99.0 fmt --manifest-path crates/Cargo.toml --all -- --check`.
  - Line 164 runs `cargo +1.99.0 test --manifest-path crates/Cargo.toml --workspace --locked --all-targets`.
  - Lines 166-175 run `cargo +1.99.0 clippy --workspace --locked --all-targets -- -D warnings`.
  - Lines 177-183 run `cargo +1.99.0 doc --workspace --locked --no-deps` with `RUSTDOCFLAGS: -D warnings`.
  - The artifact's Test Infrastructure says only: "`cargo test` across the workspace; no external services required."
- Artifact currently says: one line describing the Rust test invocation.
- What the code actually does: the conformance workflow enforces four separate Rust gates, including a `--locked` dependency lock check, a formatting check, a clippy pedantic deny-warnings gate, and a rustdoc deny-warnings gate. A reader of the plan would not know that formatting, clippy, and doc warnings are build-blocking.
- Needed change: enumerate the four gates and the toolchain version.

## Sync drift: 2026-11-16

### One documented integration test was split into two tests

- Status: BLOCKING
- Evidence:
  - The artifact's TC-I-session-10 row names `native_signed_connect_preserves_product_fields_and_rejects_invalid_node_manifests` in `crates/openclaw-node-host/tests/node_session.rs`.
  - That combined identifier does not exist anywhere in the repository.
  - The suite now holds 11 tests, and lines 1159 and 1213 of that file define `native_signed_connect_preserves_product_fields` and `native_signed_connect_rejects_invalid_node_manifests` as separate tests.
- Artifact currently says: TC-I-session-10 is one test covering both product-field preservation and invalid-manifest rejection, and the session suite has 10 tests.
- What the code actually does: those two checks are separate tests, so the plan undercounts the session suite by one and names a test that cannot be found.
- Needed change: split TC-I-session-10 into two rows for the two test names and raise the session suite count from 10 to 11.

### Previously recorded drift items remain unaddressed

- The representative case `shared_authority_handoff_contract_matches_openclaw` is still absent from the runtime suite.
- The per-file counts are still off by one for protocol at 17, runtime at 16, and node at 6, giving 98 unit cases instead of 99.
- The two TypeScript contract suites and their conformance job are still not named in the test infrastructure section.
- The infrastructure line still lists only `cargo test` and omits the fmt, clippy, and rustdoc gates on Rust 1.99.0.

## Sync drift: 2026-11-23

### Previously recorded drift items remain unaddressed

- Status: BLOCKING
- Evidence:
  - `.sdlc/features/p11-rust-node-host/tests.md:24` still names `shared_authority_handoff_contract_matches_openclaw`, which does not exist, while `crates/openclaw-node-host/src/runtime.rs:1388` defines `shared_manifest_and_local_admission_match_openclaw`.
  - `tests.md:17` still claims 99 inline node-host unit cases, while the twelve `src/*.rs` files hold 98 cases in total, with counts of 1, 5, 3, 0, 3, 1, 6, 13, 16, 14, 17, and 19.
  - `tests.md:21`, `tests.md:24`, and `tests.md:26` still report 16 protocol cases, 17 runtime cases, and 7 node cases, while the actual counts are 17, 16, and 6.
  - `tests.md:50` still names the single `native_signed_connect_preserves_product_fields_and_rejects_invalid_node_manifests`, while `crates/openclaw-node-host/tests/node_session.rs:1159` and `node_session.rs:1213` define two separate tests.
  - `tests.md:80-83` lists six fixtures but does not name `src/infra/node-invoke-lifecycle-contract.test.ts:7` or `src/infra/node-runtime-integration-contract.test.ts:4`, which consume two of them in the `.github/workflows/node-runtime-conformance.yml:209-213` job.
  - `tests.md:83` still says only `cargo test`, while `.github/workflows/node-runtime-conformance.yml:244`, `:247`, `:251`, and `:261-263` also gate on fmt, `--locked` test, clippy `-D warnings`, and rustdoc `-D warnings` with Rust 1.99.0.
- The artifact was not overwritten.
- No new discrepancies were found in tests.md during this reconciliation.
