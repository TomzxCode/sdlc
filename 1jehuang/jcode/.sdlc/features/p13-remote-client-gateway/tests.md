---
title: "Remote Client Gateway"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Remote Client Gateway

## Scope

Covers pairing code minting and consumption, device registration and token validation, the WebSocket upgrade authorization path, the newline-delimited JSON bridge, device listing, revocation, the `/remote` control surface, and the dial-address resolution helper.

Test files that exist for this feature:

- `crates/jcode-base/src/gateway_tests.rs`, mounted as `mod gateway_tests` from `crates/jcode-base/src/gateway.rs`.
- The inline `mod tests` block in `crates/jcode-base/src/gateway/control.rs`.
- The inline `mod tests` block in `crates/jcode-tui/src/tui/app/commands_remote.rs`.
- `src/cli/commands_tests.rs`, for the Tailscale MagicDNS helper that the gateway re-exports.
- `tests/e2e/transport.rs`, with the gateway helpers in `tests/e2e/test_support/mod.rs`.

Crates and files with no test coverage for this feature:

- `crates/jcode-gateway-types/` has no test file and no test module.
  It only holds the `PairedDevice` and `PairingCode` structs, so its behavior is covered indirectly through `crates/jcode-base/src/gateway_tests.rs`.
- `crates/jcode-base/src/gateway/registry.rs` and `crates/jcode-base/src/gateway/auth.rs` have no inline test modules.
  Their behavior is covered from `crates/jcode-base/src/gateway_tests.rs`.
- There is no test file for the `jcode pair` CLI command itself.
  `run_pair_command` in `src/cli/commands.rs` is not exercised by any test.
- `crates/jcode-app-core/src/server.rs` and `crates/jcode-app-core/src/server/runtime.rs` have no gateway-specific test file.
  The gateway startup and accept loop are covered only through the end-to-end scenario.

Out of scope: the versioned harness API bridge, the iOS app, and the Tailscale or network layer itself.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Bearer token parsing | `crates/jcode-base/src/gateway_tests.rs` (`test_parse_bearer_token`) | `Bearer <token>` is accepted whatever the case of the scheme; `Basic`, a missing token, and extra parts are rejected |
| TC-2 | Query token parsing | `crates/jcode-base/src/gateway_tests.rs` (`test_parse_query_token`) | The `token` parameter is extracted from a query string; an empty value and a query without `token` yield nothing |
| TC-3 | Token shape validation | `crates/jcode-base/src/gateway_tests.rs` (`test_hex_token_validation`) | A 64-character hexadecimal string is accepted; short and non-hexadecimal strings are rejected |
| TC-4 | WebSocket auth extraction and source tracking | `crates/jcode-base/src/gateway_tests.rs` (`test_extract_ws_auth_prefers_header_and_falls_back_to_query`) | The header token wins and is reported as the header source; the query token is used and reported as the query source when there is no header |
| TC-5 | Conflicting auth sources | `crates/jcode-base/src/gateway_tests.rs` (`test_extract_ws_auth_rejects_conflicting_sources`) | A request that carries a different token in the header and in the query string is rejected |
| TC-6 | HTTP header terminator detection | `crates/jcode-base/src/gateway_tests.rs` (`test_find_header_end`) | The offset of the `\r\n\r\n` terminator is returned; incomplete headers and empty input return nothing |
| TC-7 | Device authorization for a paired token | `crates/jcode-base/src/gateway_tests.rs` (`test_authorize_ws_device_valid_token`) | The paired device name and id are returned for a valid token |
| TC-8 | Device authorization for an unknown or revoked token | `crates/jcode-base/src/gateway_tests.rs` (`test_authorize_ws_device_rejects_unknown_and_revoked_with_401`) | A 401 error response is produced and its body tells the client to re-pair |
| TC-9 | `/remote` subcommand parsing | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) | The subcommands, their aliases, case-insensitive input, and the error cases for a missing revoke target and stray arguments parse as documented |
| TC-10 | `/remote` command boundary | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) | `/remote-release`, `/remotely`, `/resume`, and unrelated input are not claimed by the parser |
| TC-11 | Gateway status rendering | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) | The status markdown reports the gateway state, the dial address, the paired devices, and the setup guidance for an empty device list |
| TC-12 | Wildcard bind and unknown host warnings | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) | A wildcard bind produces the trusted-network warning, an explicit bind address is used verbatim, and an undeterminable host is flagged |
| TC-13 | Pairing code display format | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) | A six-digit code is grouped as `082 641` for reading aloud |
| TC-14 | Tailscale MagicDNS name parsing | `src/cli/commands_tests.rs` (`test_parse_tailscale_dns_name_trims_trailing_dot`, `test_parse_tailscale_dns_name_handles_missing_or_empty`, `test_parse_tailscale_dns_name_invalid_json`) | The trailing dot is trimmed; a missing, blank, or non-JSON payload yields no name |
| TC-15 | `/remote` parser boundary and help text in the TUI | `crates/jcode-tui/src/tui/app/commands_remote.rs` (`mod tests`) | `/remote-release` is not claimed, and the help text lists every subcommand the parser accepts |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-16 | Pairing code minting, consumption, and single use | `crates/jcode-base/src/gateway_tests.rs` (`test_device_registry_pairing`) | A six-digit code is minted, validates once, is removed from the pending list, and fails on the second attempt |
| TC-17 | Device pairing and token authentication | `crates/jcode-base/src/gateway_tests.rs` (`test_device_registry_token_auth`) | The issued token validates, a wrong token does not, and the device record holds a `sha256:` hash rather than the token |
| TC-18 | Re-pairing the same device id | `crates/jcode-base/src/gateway_tests.rs` (`test_device_re_pairing`) | The earlier record is replaced, the earlier token stops validating, and the new token validates |
| TC-19 | Gateway enable and disable persistence | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) with a temporary `JCODE_HOME` | The config file is rewritten with the new value, unrelated settings survive the rewrite, and a no-op toggle reports `Unchanged` |
| TC-20 | Revocation removes only the named device | `crates/jcode-base/src/gateway/control.rs` (`mod tests`) with a temporary `JCODE_HOME` | Only the targeted device is removed, the result is persisted, and an unknown target removes nothing |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-21 | WebSocket transport parity with the Unix socket | `tests/e2e/transport.rs` (`test_websocket_transport_matches_unix_socket_for_subscribe_history_message_and_resume`) with the helpers in `tests/e2e/test_support/mod.rs` | A paired device opens `ws://127.0.0.1:<port>/ws` with a bearer token, subscribes, sends a message, reads history, and resumes, and the history and resume payloads match the Unix-socket run |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-22 | A pairing code is replayed after it was consumed | The second `POST /pair` with the same code is refused with 401 and no token is issued |
| TC-23 | A pairing code is used after the five-minute expiry | The code is refused with 401 and no token is issued |
| TC-24 | A WebSocket upgrade carries no token | The upgrade is refused with 401 and the body names the missing token |
| TC-25 | A WebSocket upgrade carries a malformed token | The upgrade is refused with 401 before any session stream is created |
| TC-26 | A WebSocket upgrade carries a revoked device token | The upgrade is refused with 401 and the client is told to re-pair |
| TC-27 | A WebSocket upgrade targets a path other than `/ws` | The upgrade is refused with 404 |
| TC-28 | The header token and the query token disagree | The upgrade is refused with 401 |
| TC-29 | The `POST /pair` body is not valid JSON | The request is refused with 400 and no token is issued |
| TC-30 | A second client connects while the first is attached | Both clients keep their own session stream and both receive their own events |
| TC-31 | One gateway client disconnects mid-session | The relay tasks stop, the disconnect is logged, and the listener keeps serving the other clients |
| TC-32 | The gateway is disabled while devices are paired | The paired device records are kept, so the devices can reconnect once the gateway is enabled again |
| TC-33 | `devices.json` is missing, empty, or malformed | The registry loads as empty instead of failing the gateway |
| TC-34 | A pairing code is minted while expired codes are pending | The expired codes are pruned and only the new code stays pending |

## Test Infrastructure

- The gateway unit tests run under `cargo test` in the `jcode-base` crate, and the `jcode-tui` and root-crate tests run in their own crates.
- The end-to-end scenario runs under `cargo test` in the root crate, in the `tests/e2e` suite, with a `MockProvider` and a reserved TCP port.
- The end-to-end helper `pair_test_device` in `tests/e2e/test_support/mod.rs` writes a device record with a known token hash, so the test does not need a real pairing exchange.
- The registry helpers in `crates/jcode-base/src/gateway/registry.rs` persist to `~/.jcode/devices.json` as a side effect, so the registry tests touch the real jcode home.
- The config and revocation tests in `crates/jcode-base/src/gateway/control.rs` redirect `JCODE_HOME` to a temporary directory and serialize on the shared test environment lock.
- The `jcode pair` CLI command has no automated test, so its output and its `--list` and `--revoke` branches are checked manually.
- The edge cases TC-23, TC-24, TC-25, TC-27, TC-29, TC-30, TC-31, TC-32, TC-33, and TC-34 record required behavior that no automated test proves today.
  In the coverage matrix they are listed as the expected-behavior reference rather than as an automated proof.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-19, TC-21 |
| FR-2 | TC-13, TC-16, TC-34 |
| FR-3 | TC-17, TC-21 |
| FR-4 | TC-16, TC-22, TC-23 |
| FR-5 | TC-3, TC-7, TC-8, TC-26 |
| FR-6 | TC-21 |
| FR-7 | TC-11, TC-20 |
| FR-8 | TC-20, TC-8, TC-26 |
| FR-9 | TC-27 |
| FR-10 | TC-30 |
| FR-11 | TC-1, TC-2, TC-4, TC-5, TC-28 |
| FR-12 | none, see TC-6 for the header parsing that the endpoints rely on |
| FR-13 | TC-12, TC-14 |
| FR-14 | TC-9, TC-10, TC-15, TC-19, TC-20 |
| FR-15 | none, see TC-21 for the connection that triggers the update |
| FR-16 | none, see TC-31 for the connection lifecycle |
| NFR-1 | TC-16, TC-22, TC-23 |
| NFR-2 | TC-17 |
| NFR-3 | TC-5, TC-7, TC-8, TC-24, TC-25, TC-26 |
| NFR-4 | TC-12 |
| NFR-5 | TC-31 |
| NFR-6 | TC-21 |
| NFR-7 | TC-21 |
| NFR-8 | none, verified by reading the gateway log during a manual run |
