---
title: "Rust node host"
status: done
session_link: "http://localhost:10000/?session=ses_sync_sdlc_p11"
---

# Requirements: Rust node host

## Overview

Remote browser, worker, and companion machines need a small native agent that can pair with the Gateway, receive authorized command invocations, and execute them under strict local bounds.
This feature provides that agent as a Rust workspace: a reusable Gateway client library, a headless node host binary, a bounded command runtime, and an authenticated local sidecar protocol for embedding a runtime behind a product supervisor.
The Gateway-side pairing, approval, and registry surface belongs to FEAT-p1; this feature covers only the Rust node side of that connection.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Node operator | Runs one config file plus env secrets and gets a self-reconnecting host with local health probes |
| Gateway operator | Receives attested node connections with declared command manifests and revocable device tokens |
| Embedding developer | Reuses the client, runtime, and sidecar crates without owning transport or protocol details |
| Security reviewer | Gets channel retirement on any auth failure and no secret material in logs, CLI args, or config files |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a headless `openclaw-node` binary that loads a secret-free JSON config file, loads identity and auth secrets from the environment, and runs until shutdown or a terminal pause. |
| FR-2 | Must | The system shall connect to the Gateway over WebSocket with a challenge-signed connect envelope carrying protocol range, client identity, auth material, and (once activated) the declared command manifest. |
| FR-3 | Must | The system shall negotiate the node wire dialect, preferring protocol v4 with serialized `paramsJSON` and falling back to protocol v3 with legacy platform naming when the Gateway requires it. |
| FR-4 | Must | The system shall frame all sidecar IPC traffic as authenticated `OCSC` v1 frames with HMAC-SHA-256, direction binding, nonzero generation, and strictly increasing per-direction sequence numbers. |
| FR-5 | Must | The system shall complete a two-frame supervisor/runtime handshake that negotiates protocol minor version, feature bits, frame ceilings, and deadlines before any configuration or invocation traffic flows. |
| FR-6 | Must | The system shall exchange exactly one supervisor configuration and one runtime acknowledgement to build an immutable connection manifest, then dispatch typed invocations with admission checks, results, cancellation, and status through the runtime bridge. |
| FR-7 | Must | The system shall drive connect, reconnect with exponential backoff, graceful shutdown with draining, and secret-free typed lifecycle events through a single canonical lifecycle driver. |
| FR-8 | Must | The system shall classify every connection failure into retry-after, stored-device-token retry, keep-session, or a terminal pause (device-pairing, authentication, protocol, configuration, local-identity). |
| FR-9 | Must | The system shall own an Ed25519 device identity that signs the canonical v3 connect payload, supports caller-owned key storage via external signing requests, and never exposes private key material. |
| FR-10 | Must | The system shall execute commands in a bounded runtime with concurrency, input/output byte, and timeout limits, embedding-owned admission policies, duplicate-invocation rejection, and duplex ordered input with progress output. |
| FR-11 | Should | The system shall adopt a Gateway-issued device token into process memory, prefer it on the next attempt, and fall back to configured auth exactly once when the Gateway rejects it. |
| FR-12 | Should | The system shall serve loopback-only local health probes (`/healthz`, `/readyz`) plus 404/405 handling without ever binding a non-loopback address. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall keep secrets out of command-line arguments, environment inheritance, logs, crash reports, world-readable files, and `Debug` output. |
| NFR-2 | Must | Reliability | The system shall retire the channel or pause reconnect on any framing, authentication, replay, generation, or terminal protocol failure, and callers shall not continue on a retired channel. |
| NFR-3 | Must | Performance | The system shall enforce all byte ceilings before allocation and shall never fully materialize an oversized payload into a second plaintext buffer. |
| NFR-4 | Should | Observability | The system shall emit structured JSONL lifecycle and health events to stderr with stable secret-free reason codes. |
| NFR-5 | Must | Maintainability | The system shall forbid `unsafe` code across the workspace and keep clippy pedantic warnings clean. |

## Constraints

- The `system.*` command namespace stays reserved for OpenClaw-owned handlers and cannot be claimed by ordinary registrations.
- Command names use the shared ASCII grammar `[A-Za-z0-9._-]{1,128}` with no duplicates.
- Sidecar feature masks must fit in `2^53 - 1` so JSON implementations preserve every bit exactly.
- Gateway pairing approval, committed-policy reconciliation, and pairing-generation leases remain Gateway authority (see FEAT-p1) and must never be inferred from sidecar state.
- An `IssuedDeviceToken` is never placed in sidecar configuration or status traffic.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: host runs from config plus environment
      Given a valid secret-free JSON config and env secrets
      When the operator runs openclaw-node --config <path>
      Then the host connects, serves loopback health probes, and exits only on shutdown or a terminal pause
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: challenge-signed connect
      Given a Gateway challenge nonce and timestamp
      When the node connects
      Then the envelope carries min/max protocol, node role, client metadata, device proof, and auth material
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: protocol fallback to v3
      Given a Gateway that rejects the v4 hello with a v3 mismatch
      When the node retries
      Then it reconnects once with fresh legacy connect material and continues on v3
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: frame authentication and replay protection
      Given an established sidecar channel
      When a frame is forged, replayed, reordered, or carries the wrong generation or direction
      Then the receiver rejects it and permanently retires the channel
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: handshake negotiates shared selection
      Given complementary supervisor and runtime offers
      When the offer/accept exchange completes
      Then both peers independently derive the same minor version, intersected features, and minimum ceilings
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: configuration activates the bridge once
      Given a negotiated sidecar channel
      When the supervisor sends one configuration and the runtime acknowledges the derived manifest
      Then the bridge activates irreversibly and dispatches only manifested, admitted invocations
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: lifecycle reconnects and shuts down cleanly
      Given a transient transport failure followed by shutdown
      When the lifecycle driver runs
      Then it emits connecting, disconnected, backing-off, and stopped events and drains the active session
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: terminal failures pause with typed reasons
      Given a Gateway rejection with pauseReconnect or a non-retryable auth code
      When the reconnect policy classifies it
      Then it returns a typed pause instead of retrying forever
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: identity signs the canonical payload
      Given a 32-byte identity secret
      When the node signs a connect challenge
      Then the device proof verifies against the canonical v3 payload and the device id derives from the public key
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: bounded execution with admission
      Given a registered command with an admission policy
      When invocations arrive beyond concurrency, byte, or timeout limits, or admission denies them
      Then the runtime returns structured OVERLOADED, INPUT_TOO_LARGE, HANDLER_TIMEOUT, or ADMISSION_DENIED failures without running the handler
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: issued device token adoption
      Given an issued device token from hello-ok
      When the next attempt uses it and the Gateway rejects it with AUTH_DEVICE_TOKEN_MISMATCH
      Then the host clears it once and retries with configured auth
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: loopback health probes
      Given a running host
      When a client requests /healthz and /readyz
      Then /healthz reports ok and /readyz reflects lifecycle readiness, while non-loopback binds are rejected at config validation
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: secrets never leak
      Given any Debug formatting, log line, or config file
      When inspected
      Then no session key, token, signature payload, or private key material appears
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: fail-closed channels
      Given any HMAC, sequence, or generation violation
      When detected
      Then the channel poisons itself and rejects every later send or receive
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: ceilings enforced before allocation
      Given a length prefix above the local ceiling
      When the reader processes it
      Then it rejects before allocating or reading the frame body
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: structured diagnostics
      Given lifecycle transitions and health failures
      When observed on stderr
      Then each line is JSON with level, event, and secret-free fields
    ```

- [x] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: unsafe-free build
      Given the workspace source
      When compiled with the crate lints
      Then no unsafe code exists and clippy pedantic reports no warnings
    ```

## Conflicts

None identified yet.

## Open Questions

1. What packaging, artifact verification, and restart/rollback policy should the production supervisor provide around the binary, since the crate explicitly excludes them?
2. Should Windows integration and PTY/MCP/skills/host-statistics support extend this feature or a follow-up one, given the protocol marks them not yet implemented?
3. Where should Gateway-issued device tokens be durably persisted, since the host currently keeps them in process memory only?
