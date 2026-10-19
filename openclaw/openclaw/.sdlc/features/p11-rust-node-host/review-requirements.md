---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-10-19

### The Gateway-side pairing boundary now belongs to FEAT-p14, not FEAT-p1

- Status: BLOCKING
- Evidence:
  - `.sdlc/features/p11-rust-node-host/requirements.md:12` states: "The Gateway-side pairing, approval, and registry surface belongs to FEAT-p1; this feature covers only the Rust node side of that connection."
  - `.sdlc/features/p1-gateway-server/requirements.md:31` (FR-8) says only: "The gateway shall support node pairing for external agent runtime hosts". The p1 specification contains no node registry, pairing-approval, or auto-approve model, and `grep -n -i "node\|pairing\|registry" .sdlc/features/p1-gateway-server/tests.md` returns nothing.
  - `.sdlc/features/p14-node-host-device-execution/specification.md:11` states: "The Gateway side of the pairing and invocation surface lives in `src/gateway/server-methods/nodes*.ts` and the node registry, and is described here only where the node contract depends on it."
  - `.sdlc/features/p14-node-host-device-execution/requirements.md:42` (FR-14) claims the Gateway-side node surface: "pairing request list, approve, reject, and remove, node rename, node list, node describe, plugin surface refresh, plugin tool update, and skill update over the `node.*` RPC methods".
  - `.sdlc/features/p14-node-host-device-execution/requirements.md:29` (FR-1) and the p14 Overview claim the TypeScript node host in `src/node-host/` (212 files), which p11 never mentions.
- Artifact currently says: "The Gateway-side pairing, approval, and registry surface belongs to FEAT-p1; this feature covers only the Rust node side of that connection."
- What the code actually does: the Gateway-side node surface is now described in detail by FEAT-p14, whose specification maps it to `src/gateway/server-methods/nodes*.ts` and the node registry, and whose FR-14 enumerates the pairing, registry, and approval RPC methods. FEAT-p1 mentions node pairing only as a single Should-level line with no supporting model or tests. A reader of p11 would look to FEAT-p1 for the Gateway-side contract and find nothing there.
- Needed change: repoint the boundary statement to FEAT-p14, and note that FEAT-p1 carries only a thin FR-8 mention.

### The `src/node-host/` TypeScript tree is a separate node host implementation that p11 does not mention

- Status: BLOCKING
- Evidence:
  - `src/node-host/` contains 212 files and is the shipped node host: `src/node-host/runner.ts` (foreground runner), `src/node-host/worker.ts` (macOS app JSONL entry), `src/node-host/runtime.ts` (shared runtime), `src/node-host/invoke-system-run.ts`, `src/node-host/exec-policy.ts`, `src/node-host/node-worker-supervisor.ts`, `src/node-host/auto-update.ts`, `src/node-host/host-stats.ts`, `src/node-host/invoke-mcp-result.ts`.
  - `.sdlc/features/p14-node-host-device-execution/requirements.md:29` (FR-1) and the p14 Overview claim exactly that tree: "The TypeScript node host in `src/node-host/` ships a foreground runner (`src/node-host/runner.ts`), a private JSONL entry point for the macOS companion app (`src/node-host/worker.ts`), a transport-independent runtime (`src/node-host/runtime.ts`) that both share, the `node.invoke` command surface including `system.run` with an approval plan and an allowlist, a supervisor that hosts agent sessions as worker children, workspace staging with git, quiescence, and retention, and an automatic runtime update path."
  - p11's Overview says: "This feature provides that agent as a Rust workspace: a reusable Gateway client library, a headless node host binary, a bounded command runtime, and an authenticated local sidecar protocol for embedding a runtime behind a product supervisor."
  - `docs/nodes/node-host.md:11-19` documents the operator-facing node host as the `system.run` / `system.which` executor, which is the TypeScript implementation, not the Rust crate.
- Artifact currently says: p11 never mentions `src/node-host/`. Its Overview presents the Rust workspace as "that agent", implying the Rust host is the node host an operator runs.
- What the code actually does: there are two distinct node host implementations. The TypeScript one under `src/node-host/` is the one documented for operators (`openclaw connect`, `openclaw node run`, service install, `system.run` with exec approvals). The Rust crate under `crates/openclaw-node-host/` is a separate headless host plus a reusable sidecar runtime for embedding. A reader of p11 would assume the Rust crate is the production node host and would not know a second, larger implementation exists.
- Needed change: state explicitly that the Rust crate is a distinct implementation from the TypeScript node host, and cross-reference FEAT-p14 for the shipped TypeScript host.

### The workspace Rust version no longer matches the CI toolchain

- Status: ADVISORY
- Evidence:
  - `crates/openclaw-node-host/Cargo.toml:6` and `crates/openclaw-gateway-client/Cargo.toml:6` both declare `rust-version = "1.93"`.
  - `.github/workflows/node-runtime-conformance.yml:148` installs `rustup toolchain install 1.99.0`, and lines 161, 164, 168, and 180 all invoke `cargo +1.99.0` for fmt, test, clippy, and doc.
  - `.sdlc/features/p11-rust-node-host/specification.md` (Technical Decisions) says: "Language | Rust workspace, edition 2021, Rust 1.93".
- Artifact currently says: "Language | Rust workspace, edition 2021, Rust 1.93 | Memory safety without GC for a long-lived host; `unsafe_code = forbid`".
- What the code actually does: the declared MSRV is still 1.93, but the conformance workflow that proves the workspace builds and tests cleanly runs Rust 1.99.0, so the toolchain the artifact names is not the one that gates the build.
- Needed change: record both the MSRV and the conformance toolchain version.

### The "Windows integration and PTY/MCP/skills/host-statistics" open question has a partial answer in the sibling feature

- Status: ADVISORY
- Evidence:
  - `.sdlc/features/p11-rust-node-host/requirements.md` Open Question 2 asks: "Should Windows integration and PTY/MCP/skills/host-statistics support extend this feature or a follow-up one, given the protocol marks them not yet implemented?"
  - The Rust crate still does not implement them: `crates/openclaw-node-host/src/` has no PTY, MCP, skills, or host-statistics module.
  - The TypeScript host does implement several of them: `src/node-host/host-stats.ts`, `src/node-host/invoke-mcp-result.ts`, `src/node-host/invoke-agent-cli-claude.ts`, `src/node-host/exec-policy.ts`.
  - `crates/openclaw-node-host/src/host.rs:806` shows the Rust host's default `statusCommand` is `system.run`.
- Artifact currently says: the question is open and the protocol "marks them not yet implemented".
- What the code actually does: the capability gap is real on the Rust side, but the sibling TypeScript host covers host statistics, MCP results, and skills, so "not yet implemented" is a Rust-crate fact rather than a product fact.
- Needed change: note that the gap is scoped to the Rust crate and that the TypeScript host covers part of it, so the open question is about the Rust crate's parity rather than product coverage.

### The durable device-token storage open question is still accurate

- Status: ADVISORY (no change required)
- Evidence:
  - `crates/openclaw-node-host/src/host.rs:175` declares `issued_device_token: Option<String>` in the credentials struct, and lines 334-343 move it into an `Arc<Mutex<Option<String>>>`.
  - `crates/openclaw-node-host/src/host.rs:476-482` shows the adoption handler writing the token into that in-memory cell only.
- Artifact currently says: "Where should Gateway-issued device tokens be durably persisted, since the host currently keeps them in process memory only?"
- What the code actually does: unchanged. The token is still in-process only.
- Needed change: none. This row records that the question was re-checked and still stands.
