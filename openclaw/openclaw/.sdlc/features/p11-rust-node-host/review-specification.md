---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-10-19

### The crate module layout omits `lib.rs` and the module set has not changed

- Status: ADVISORY
- Evidence:
  - `crates/openclaw-node-host/src/` contains `duplex.rs`, `host.rs`, `identity.rs`, `lib.rs`, `lifecycle.rs`, `main.rs`, `node.rs`, `reconnect.rs`, `runtime.rs`, `sidecar_handshake.rs`, `sidecar_protocol.rs`, and `sidecar_runtime.rs`.
  - The artifact's layout list names `node.rs`, `identity.rs`, `runtime.rs`, `duplex.rs`, `lifecycle.rs`, `reconnect.rs`, `host.rs`, `sidecar_protocol.rs`, `sidecar_handshake.rs`, `sidecar_runtime.rs`, and `main.rs`, and omits `lib.rs`.
  - `crates/openclaw-gateway-client/src/` contains `lib.rs` and `session.rs`, matching the artifact.
- Artifact currently says: the crate module layout paragraph lists eleven modules and does not mention `lib.rs`.
- What the code actually does: the module set is otherwise unchanged, so the artifact is nearly accurate; only `lib.rs` is missing from the list.
- Needed change: add `lib.rs` to the module layout list.

### The Gateway node connect envelope omits fields the wire now carries

- Status: ADVISORY
- Evidence:
  - `crates/openclaw-node-host/src/node.rs:247-256` declares the envelope fields `caps`, `commands`, and `permissions` (both advertised and declared variants).
  - `crates/openclaw-node-host/src/node.rs:353` exposes `pub fn activate(mut self) -> Self`, and lines 445-446 copy the declared capabilities, commands, and permissions into the advertised set.
  - `packages/gateway-protocol/src/schema/nodes.ts:245` defines `paramsJSON: Type.Optional(Type.String())` on the invoke params, and `packages/gateway-protocol/src/version.ts:6` sets `MIN_NODE_PROTOCOL_VERSION = 3` with `PROTOCOL_VERSION = 4`.
  - `crates/openclaw-node-host/src/node.rs:657-660` reads `minProtocol` and `maxProtocol` from the connect params, and lines 464-467 map `macos` to `darwin` and `windows` to `win32` for the v3 fallback.
- Artifact currently says: the connect envelope table lists `minProtocol/maxProtocol`, `client`, `role/scopes`, `device`, `auth`, and `commands/caps/permissions` (the last as a single grouped row), and states the range is `3..=4`.
- What the code actually does: the wire contract matches the artifact on the range, the v3 platform-name fallback, and the withheld-until-activated manifest. The envelope table's grouped `commands/caps/permissions` row is accurate but the artifact does not distinguish the advertised set (empty until `activate()`) from the declared set, which is the distinction the code makes at `node.rs:247-256` and `node.rs:445-446`.
- Needed change: split the grouped row into advertised and declared variants and note that activation is what copies declared into advertised.

### The "Local HTTP" health contract still matches, but the process-supervision gap widened

- Status: ADVISORY
- Evidence:
  - `crates/openclaw-node-host/src/host.rs:637-639` returns `200 OK` for `/healthz`, `200 OK` for `/readyz` when ready, and `503 Service Unavailable` otherwise, exactly as the artifact's API contract table describes.
  - `crates/openclaw-node-host/src/host.rs:778-779` sets the default handler timeout to `30_000` ms and the max timeout to `120_000` ms, matching the artifact's Risk 3 statement "defaults are 30 s with a 120 s cap for the binary".
  - `crates/openclaw-node-host/Cargo.toml:33` keeps `unsafe_code = "forbid"` and lines 35-37 keep `all = "warn"` and `pedantic = "warn"` under `[lints.clippy]`.
  - `.github/workflows/node-runtime-conformance.yml:168-175` runs clippy with `-D warnings` across the workspace and all targets, and lines 178-183 run `cargo doc` with `RUSTDOCFLAGS: -D warnings`.
- Artifact currently says: Risk 1 lists "Product supervisor duties (artifact verification, secret delivery, process creation, packaging, Windows integration)" as unimplemented.
- What the code actually does: the Rust crate still implements none of those duties, and the conformance workflow now also gates on rustdoc warnings, which the artifact's Test Infrastructure does not mention.
- Needed change: note the rustdoc gate in the test infrastructure description.

### The feature-mask risk statement about JavaScript adapters is still accurate

- Status: ADVISORY (no change required)
- Evidence:
  - `crates/openclaw-node-host/src/sidecar_protocol.rs:31` declares `pub const SIDECAR_MAX_FEATURE_BITS: u64 = (1 << 53) - 1;`.
  - `crates/openclaw-node-host/src/sidecar_runtime.rs:25-35` uses that constant as `MAX_PORTABLE_JSON_INTEGER` and rejects larger integers with "integer exceeds portable JSON range".
  - `test/fixtures/node-sidecar-negotiation-v1.json` pins `featureBits` of `4503599627370499` and `4503599627370501` with a selected value of `4503599627370497`, all above 2^32 and below 2^53.
- Artifact currently says: "JavaScript/TypeScript adapters must use `BigInt` for the feature-mask intersection because native `&` truncates to 32 bits; the negotiation fixture pins a bit above that range."
- What the code actually does: unchanged. The fixture still pins a bit above the 32-bit range and the Rust side still enforces the 2^53-1 ceiling.
- Needed change: none. This row records that the constraint was re-verified and still holds.

## Sync drift: 2026-11-16

### Previously recorded drift items remain unaddressed

- The crate module layout paragraph still omits `lib.rs` from the list of node-host source modules.
- The connect envelope table still groups commands, caps, and permissions into one row instead of separating the advertised set from the declared set that `activate()` copies.
- Risk 1 still omits the rustdoc deny-warnings gate that the conformance workflow enforces with `RUSTDOCFLAGS`.
- The feature-mask risk statement about JavaScript adapters still holds and needed no change.

No new discrepancies were found in specification.md during this reconciliation.

## Sync drift: 2026-11-23

### Previously recorded drift items remain unaddressed

- Status: ADVISORY
- Evidence:
  - `.sdlc/features/p11-rust-node-host/specification.md:32` still lists eleven node-host source modules and omits `crates/openclaw-node-host/src/lib.rs`, which exists on disk.
  - `specification.md:89` still groups `commands/caps/permissions` into one row, while `crates/openclaw-node-host/src/node.rs:246-257` declares separate advertised and declared fields and `node.rs:352` copies declared into advertised on activation.
  - `specification.md:106` and `specification.md:153` still assign the Gateway WebSocket surface to FEAT-p1, while `.sdlc/features/p14-node-host-device-execution/requirements.md:42` owns that surface.
  - `specification.md:191` still omits the rustdoc gate, while `.github/workflows/node-runtime-conformance.yml:261` sets `RUSTDOCFLAGS: -D warnings` and line 263 runs `cargo +1.99.0 doc`.
  - `specification.md:194` still states the JavaScript adapter constraint, and the constraint still holds because `crates/openclaw-node-host/src/sidecar_protocol.rs:31` sets `SIDECAR_MAX_FEATURE_BITS` to `2^53 - 1` and `test/fixtures/node-sidecar-negotiation-v1.json:12` pins 4503599627370499.
  - `specification.md:122-123` still matches `crates/openclaw-node-host/src/host.rs:637-639` for the health endpoints, so no new drift exists there.
- The artifact was not overwritten.
- No new discrepancies were found in specification.md during this reconciliation.
