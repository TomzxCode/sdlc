---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
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
