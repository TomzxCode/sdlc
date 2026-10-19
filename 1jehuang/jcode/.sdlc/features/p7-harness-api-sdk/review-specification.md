---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.
The following discrepancies were found by comparing the document against the current code.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Data Models | "`capability_coverage.rs` — capability negotiation." | The file is at `crates/jcode-harness-api/src/harness_api_tests/capability_coverage.rs` and is test-only (`crates/jcode-harness-api/src/lib.rs:45-51`). | Rename to `harness_api_tests/capability_coverage.rs` and mark it test-only. |
| Data Models | "`schema_snapshot.rs` — schema snapshots for parity." | The file is at `crates/jcode-harness-api/src/harness_api_tests/schema_snapshot.rs` and is test-only. | Rename to `harness_api_tests/schema_snapshot.rs` and mark it test-only. |
| Data Models | Lists only `requests.rs`, `events.rs`, `capability_coverage.rs`, `schema_snapshot.rs`. | Five production modules are missing: `client.rs` (frame read/write plus `HarnessClient`), `runtime_commands.rs` (`RuntimeCommand`, `RuntimeCommandOutput`), `sockets.rs` (`api_socket_path`, `legacy_socket_path`, `runtime_dir`), `edit_stats.rs` (`SessionEditStats`), `swarm_metadata.rs` (swarm parent/status enrichment). | Append the five missing modules to the crate listing. |
| API Contracts | "### CLI: `jcode api-bridge` (alias `jcode api`, Unix only) / Serves the versioned harness API on a Unix socket for SDK clients." | The command has two flags: `--api-socket <path>` and `--stdio` (`src/cli/args.rs:603-618`). | Document both flags, including that `--stdio` serves one API connection on stdin/stdout for SSH SDK clients and creates no socket. |
| Technical Decisions | "Schema parity testing \| `schema-parity.test.ts`, `capability_coverage.rs`". | `capability_coverage.rs` lives under `harness_api_tests/`, and a second gate exists at `crates/jcode-sdk/src/sdk_tests/parity.rs`, enforced in CI at `.github/workflows/ci.yml:111`. | Cite all three paths. |
| Risks and Unknowns | "The bridge is Unix-only by design; Windows support relies on the named-pipe transport behind the same API." | The bridge library is cross-platform (`crates/jcode-harness-api-server/src/lib.rs:36` uses `jcode_transport`); only the CLI subcommand is Unix-only (`src/cli/args.rs:602` is `#[cfg(unix)]`). A second transport (stdio) now serves SSH SDK clients. | Reword to: "The `jcode api-bridge` CLI command is Unix-only; the bridge library itself runs on Windows over the named-pipe transport behind the same API. A second transport (stdio) serves SSH SDK clients." |

## Missing Information

- The wire protocol surface is undocumented: 45 `ApiRequest` variants and 48 `ApiEvent` variants (`crates/jcode-harness-api/src/requests.rs:32-343`, `events.rs:8-450`). Capability negotiation happens in the `hello`/`hello_ok` handshake, and the bridge advertises its capability list at `crates/jcode-harness-api-server/src/lib.rs:374-409`.
- The handshake now carries `supports_user_response`, which the bridge forwards into the daemon `subscribe` (`crates/jcode-harness-api-server/src/translate.rs:607`).
- The bridge always sets `supports_server_failover` for API clients (`crates/jcode-harness-api-server/src/translate.rs:611`), so the daemon performs account failover (`crates/jcode-app-core/src/server/turn_failover.rs`).
- The bridge takes an exclusive `flock` beside the socket and forces the API socket to mode 0600 (`crates/jcode-harness-api-server/src/lib.rs:197-212, 266-270`). This belongs in Technical Decisions.

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
