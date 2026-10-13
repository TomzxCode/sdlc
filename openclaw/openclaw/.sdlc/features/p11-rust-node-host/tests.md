---
title: "Rust node host"
status: done
session_link: "http://localhost:10000/?session=ses_sync_sdlc_p11"
---

# Test Plan: Rust node host

## Scope

This plan covers the Rust workspace only: `openclaw-gateway-client` transport tests and `openclaw-node-host` unit plus integration tests.
Gateway-side pairing and registry behavior belongs to FEAT-p1 and is out of scope here.
Cross-language JSON fixtures under `test/fixtures/` serve as shared oracles for both Rust tests and future non-Rust adapters.

## Unit Tests

Node-host unit suites live inline in `src/*.rs` (99 cases); gateway-client unit suites live inline in `src/*.rs` (9 cases).

| ID | Suite file | Cases | Representative cases |
|---|---|---|---|
| TC-U-protocol | `crates/openclaw-node-host/src/sidecar_protocol.rs` | 16 | shared_wire_fixture_is_byte_exact_and_decodable, authenticated_frame_round_trips_and_replay_fails_closed, authentication_failure_permanently_retires_channel, outbound_serialization_stops_at_frame_ceiling_without_advancing_sequence, bounded_reader_rejects_length_before_payload_allocation |
| TC-U-handshake | `crates/openclaw-node-host/src/sidecar_handshake.rs` | 14 | supervisor_and_runtime_authenticate_the_same_selection, cross_language_handshake_vector_is_exact, forged_selection_fails_and_retires_supervisor, runtime_commits_selection_only_after_acceptance_delivery, handshake_cannot_move_to_another_channel_instance |
| TC-U-bridge | `crates/openclaw-node-host/src/sidecar_runtime.rs` | 19 | bridge_routes_admission_then_native_invocation, admission_denial_never_dispatches_native_work, adapter_errors_obey_complete_sidecar_message_budget, nonportable_json_has_a_distinct_runtime_failure, configuration_rejects_unknown_fields_instead_of_ignoring_secrets |
| TC-U-runtime | `crates/openclaw-node-host/src/runtime.rs` | 17 | shared_authority_handoff_contract_matches_openclaw, enforces_input_and_output_limits, rejects_saturation_without_queueing, rejects_duplicate_active_invocation_ids, converts_panics_to_structured_failure |
| TC-U-reconnect | `crates/openclaw-node-host/src/reconnect.rs` | 13 | pairing_pauses_with_sanitized_device_request, transient_backoff_is_bounded_and_resets, rejected_device_token_and_protocol_mismatch_pause, stored_device_token_fallback_is_explicit_and_bounded, auth_rate_limit_pauses_despite_wait_then_retry_advice |
| TC-U-node | `crates/openclaw-node-host/src/node.rs` | 7 | shared_invocation_lifecycle_contract_matches_openclaw, invocation_params_json_is_strict_across_protocol_versions, native_invocation_preserves_original_parameter_identity, external_signing_request_uses_final_connect_metadata_and_auth |
| TC-U-host | `crates/openclaw-node-host/src/host.rs` | 5 | config_defaults_are_bounded_local_and_collision_free, config_rejects_reserved_commands_remote_health_and_secret_ambiguity, identity_accepts_only_exact_base64url_material, stalled_health_request_does_not_starve_other_probes, rejected_adopted_device_token_retries_configured_auth_once |
| TC-U-lifecycle | `crates/openclaw-node-host/src/lifecycle.rs` | 3 | shutdown_cancels_an_in_progress_connection_attempt, shutdown_interrupts_backoff_without_another_attempt, terminal_failure_emits_a_typed_pause |
| TC-U-identity | `crates/openclaw-node-host/src/identity.rs` | 3 | identity_round_trips_and_signs_the_gateway_v3_payload, external_signing_request_rejects_a_signature_for_other_bytes, signing_request_debug_redacts_the_canonical_payload |
| TC-U-duplex | `crates/openclaw-node-host/src/duplex.rs` | 1 | input_is_ordered_bounded_and_closes |
| TC-U-main | `crates/openclaw-node-host/src/main.rs` | 1 | CLI argument validation for --config usage |
| TC-U-gwclient | `crates/openclaw-gateway-client/src/lib.rs` + `session.rs` | 9 | connect detail parsing, device-token invalidation, pin-mismatch classification, dispatch guards |
| TC-U-gwsession | `crates/openclaw-gateway-client/tests/session.rs` | 22 | connects_publishes_events_and_correlates_requests, protocol_fallback_reconnects_once_with_a_fresh_challenge, protocol_mismatch_after_fallback_is_terminal, oversized_retained_event_lags_without_closing_the_session, connect_rejection_preserves_recovery_details |
| TC-U-gwtls | `crates/openclaw-gateway-client/tests/tls_policy.rs` | 4 | pinned_trust_rejects_plaintext_before_connecting, native_policy_cannot_bypass_tls_handshake_signature_verification, builtin_pin_mismatch_still_rejects_before_http_upgrade |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-I-lifecycle | `crates/openclaw-node-host/tests/node_lifecycle.rs`: lifecycle_reacquires_each_attempt_delivers_token_and_stops_cleanly | Mock Gateway WebSocket fixture | Each attempt carries fresh material, issued token is delivered, shutdown drains |
| TC-I-session-1 | `tests/node_session.rs`: public_runtime_completes_allowed_work_and_suppresses_wire_cancelled_effects | Mock Gateway with public runtime | Allowed work completes, wire-cancelled effects suppressed |
| TC-I-session-2 | `tests/node_session.rs`: runtime_rejects_buffered_invocation_after_session_retirement_is_requested | Retired session | Buffered invocation rejected with SESSION_RETIRED |
| TC-I-session-3 | `tests/node_session.rs`: wire_cancellation_during_admission_prevents_handler_construction | Cancel during admission | Handler never constructed |
| TC-I-session-4 | `tests/node_session.rs`: sidecar_bridge_preserves_authority_through_the_public_runtime | Sidecar channel plus public runtime | Authority preserved end to end |
| TC-I-session-5 | `tests/node_session.rs`: node_protocol_fallback_uses_fresh_legacy_connect_material_and_recovers_to_v4 | v3-only mock Gateway | Fallback connects with legacy material, recovers to v4 |
| TC-I-session-6 | `tests/node_session.rs`: duplex_runtime_routes_ordered_input_and_progress | Duplex command fixture | Ordered input routed, progress emitted |
| TC-I-session-7 | `tests/node_session.rs`: duplex_input_overflow_forces_a_terminal_failure | Oversized duplex input | Terminal INPUT_BUFFER_OVERFLOW failure |
| TC-I-session-8 | `tests/node_session.rs`: direct_dispatch_rejects_duplex_without_running_an_event_loop | Duplex command via dispatch | DUPLEX_REQUIRES_RUN without an event loop |
| TC-I-session-9 | `tests/node_session.rs`: runtime_enforces_the_manifest_of_each_connection | Unmanifested command | COMMAND_NOT_ADVERTISED rejection |
| TC-I-session-10 | `tests/node_session.rs`: native_signed_connect_preserves_product_fields_and_rejects_invalid_node_manifests | Externally signed envelope | Product fields preserved, bad manifests rejected |
| TC-I-sidecar-1 | `tests/sidecar_process.rs`: authenticated_sidecar_crosses_a_real_process_boundary | Spawned child process | Exact frames verify across the process boundary |
| TC-I-sidecar-2 | `tests/sidecar_process.rs`: sidecar_process_child | Child harness entry | Child speaks the real wire protocol |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-E-sidecar | Real-process sidecar round trip via `tests/sidecar_process.rs` | Spawn child, run offer/accept plus config exchange over inherited transport | Authenticated activation completes across OS processes |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Forged HMAC tag or replayed sequence | Channel retires permanently, later traffic rejected |
| TC-E2 | Generation mismatch or wrong direction | Frame rejected, channel retired |
| TC-E3 | Length prefix above local ceiling | Rejected before allocation |
| TC-E4 | Feature bits above `2^53 - 1` | Offer invalid, handshake terminal |
| TC-E5 | Non-portable JSON integers in runtime traffic | Distinct SIDECAR_NON_PORTABLE_JSON failure, not a size error |
| TC-E6 | Oversized complete message inside logical limits | Stable SIDECAR_MESSAGE_TOO_LARGE without transport attempt |
| TC-E7 | Handler panic or admission panic | Structured HANDLER_PANIC or ADMISSION_PANIC failure, handler not entered |
| TC-E8 | Duplicate invocation id | DUPLICATE_INVOCATION rejection |
| TC-E9 | Delivery queue saturation | Session restarted with DeliverySaturated, no unbounded queue |
| TC-E10 | Rejected adopted device token | Token cleared once, configured auth retried |
| TC-E11 | AUTH_RATE_LIMITED with wait_then_retry advice | Typed authentication pause anyway |
| TC-E12 | TLS pin mismatch | Configuration pause before HTTP upgrade |
| TC-E13 | Stalled health client | Independent probes still answered within budget |

## Test Infrastructure

- Mock Gateway WebSocket servers built with `tokio-tungstenite` inside the test suites.
- Shared cross-language fixtures: `node-sidecar-protocol-v1.json`, `node-sidecar-negotiation-v1.json`, `node-sidecar-handshake-v1.json`, `node-sidecar-runtime-v1.json`, `node-invoke-lifecycle-contract.json`, `node-runtime-integration-contract.json` under `test/fixtures/`.
- Real child-process harness for the sidecar boundary test.
- `cargo test` across the workspace; no external services required.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-U-host, TC-U-main, TC-I-lifecycle |
| FR-2 | TC-U-node, TC-U-gwsession, TC-I-session-5, TC-I-session-10 |
| FR-3 | TC-U-gwsession, TC-U-node, TC-I-session-5 |
| FR-4 | TC-U-protocol, TC-E1, TC-E2, TC-E3, TC-I-sidecar-1 |
| FR-5 | TC-U-handshake, TC-E4, TC-I-sidecar-1 |
| FR-6 | TC-U-bridge, TC-I-session-4, TC-I-sidecar-1, TC-E-sidecar, TC-E5, TC-E6 |
| FR-7 | TC-U-lifecycle, TC-I-lifecycle |
| FR-8 | TC-U-reconnect, TC-E10, TC-E11, TC-E12 |
| FR-9 | TC-U-identity, TC-U-node |
| FR-10 | TC-U-runtime, TC-U-duplex, TC-I-session-1, TC-I-session-2, TC-I-session-3, TC-I-session-6, TC-I-session-7, TC-I-session-8, TC-I-session-9, TC-E7, TC-E8, TC-E9 |
| FR-11 | TC-U-host, TC-U-reconnect, TC-E10 |
| FR-12 | TC-U-host, TC-E13 |
| NFR-1 | TC-U-protocol (redacted session key Debug), TC-U-identity (redacted payload Debug) |
| NFR-2 | TC-U-protocol, TC-U-handshake, TC-U-bridge, TC-U-lifecycle |
| NFR-3 | TC-U-protocol, TC-U-bridge, TC-E3, TC-E6 |
| NFR-4 | TC-U-host (structured health and lifecycle events) |
| NFR-5 | Workspace lints (`unsafe_code = forbid`, clippy pedantic) enforced at compile time |
