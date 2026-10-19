---
title: "Remote Client Gateway"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Remote Client Gateway

## Overview

The remote client gateway exposes a running jcode server to devices on other machines, currently the iOS app and a web client.
It listens on a TCP port, accepts a WebSocket upgrade from a client, and bridges that connection onto the same newline-delimited JSON session protocol that local Unix-socket clients use.
Trust is established by a short-lived pairing code that the operator mints on the machine running the server, and by a per-device auth token that the server stores only as a hash.
This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator running jcode on their own machine | Reach a running session from a phone or a second computer without extra network setup |
| iOS and web client authors | A stable pairing and WebSocket contract to build a client against |
| Security-conscious operator | Only explicitly authorized devices may open a session, and revocation takes effect on the next connection |
| Maintainer | One owner for the remote-access trust boundary so the CLI and the TUI cannot drift apart |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall run a WebSocket gateway listener on the configured TCP port, 7643 by default, whenever the gateway is enabled. |
| FR-2 | Must | The system shall mint a random six-digit pairing code that expires five minutes after it is minted, and shall show the operator the code, the address to dial, and a `jcode://pair` URI. |
| FR-3 | Must | The system shall exchange a valid pairing code for a per-device auth token over `POST /pair`, and shall persist only a SHA-256 hash of that token. |
| FR-4 | Must | The system shall reject a `POST /pair` request whose code is unknown, already consumed, or expired with HTTP 401, and shall not issue a token. |
| FR-5 | Must | The system shall validate the auth token of every WebSocket upgrade against the device registry, and shall reject an unknown, malformed, or revoked token with HTTP 401 during the handshake. |
| FR-6 | Must | The system shall bridge each authorized WebSocket connection onto the newline-delimited JSON session protocol over a virtual socket pair, so a remote client drives a session exactly like a local client. |
| FR-7 | Must | The system shall list the paired devices with their id, name, pairing time, and last-seen time. |
| FR-8 | Must | The system shall revoke a paired device by id or by exact name, and a revoked device's token shall be rejected on its next connection attempt. |
| FR-9 | Must | The system shall reject a WebSocket upgrade whose path is not `/ws` with HTTP 404. |
| FR-10 | Must | The system shall serve several remote clients at the same time, giving each client its own session stream. |
| FR-11 | Should | The system shall accept the auth token from an `Authorization: Bearer <token>` header or from a `token=` query parameter, and shall reject a request that carries two different tokens. |
| FR-12 | Should | The system shall answer `GET /health` with the server status and version, and shall answer CORS preflight requests so that browser clients can reach the gateway. |
| FR-13 | Should | The system shall resolve the address a remote client should dial, preferring the explicit bind address, then `JCODE_GATEWAY_HOST`, then the Tailscale MagicDNS name, then the system hostname. |
| FR-14 | Should | The system shall let an operator enable the gateway, disable the gateway, pair a device, and revoke a device from the TUI through `/remote`, using the same logic as the `jcode pair` CLI. |
| FR-15 | Should | The system shall record the time of the most recent successful connection as the device's last-seen timestamp. |
| FR-16 | May | The system shall send a WebSocket ping every 20 seconds and answer a client ping with a pong, so that idle and broken connections are detected. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | A pairing code shall expire five minutes after it is minted and shall be consumed on first successful use, so that a leaked or replayed code cannot mint a second token. |
| NFR-2 | Must | Security | The system shall never persist a raw auth token, and shall store only a SHA-256 hash of a 32-byte random token. |
| NFR-3 | Must | Security | The system shall reject every WebSocket upgrade that carries no token, a malformed token, an unknown token, or a revoked token with HTTP 401, before any session stream is created. |
| NFR-4 | Must | Security | The gateway shall rely on the underlying network for transport confidentiality, and the system shall warn the operator when the bind address is a wildcard address. |
| NFR-5 | Should | Availability | One failing client shall not stop the gateway listener, and the gateway shall keep serving the remaining clients. |
| NFR-6 | Should | Performance | The bridge shall add no framing beyond the newline delimiter, and shall emit a keepalive ping every 20 seconds. |
| NFR-7 | Should | Compatibility | The WebSocket transport shall carry the same newline-delimited JSON protocol as the Unix-socket transport, so that one client implementation works over both. |
| NFR-8 | Should | Operability | The system shall log gateway lifecycle events, covering listener start, pairing, connection, disconnection, and revocation, through `crate::logging`. |

## Constraints

- The gateway binds its port when the server starts, so enabling the gateway requires a server restart.
- The default bind address is `0.0.0.0`, which listens on every interface.
- The pairing code is six decimal digits, short enough to read aloud and to type on a phone.
- The gateway speaks plain TCP and is expected to sit on a trusted network such as Tailscale.
- The paired device registry lives in `~/.jcode/devices.json`, next to the rest of the jcode home state.
- The gateway is disabled by default.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Gateway listens when it is enabled
      Given the gateway is enabled with a configured port
      When the server starts
      Then a TCP listener accepts connections on that port
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Pairing code is minted
      Given an operator on the machine running the server
      When the operator runs the pairing command
      Then a six-digit code is shown together with the dial address and a jcode://pair URI
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: A code is exchanged for a token
      Given a valid pairing code
      When a client posts it to /pair with a device id and a device name
      Then the response carries an auth token and the server stores only a hash of it
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A consumed code is refused
      Given a pairing code that was already consumed
      When a client posts it to /pair
      Then the response is 401 and no token is issued
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A revoked device cannot upgrade
      Given a paired device whose token was revoked
      When the device requests a WebSocket upgrade on /ws
      Then the upgrade is rejected with 401 and no session stream is created
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: WebSocket frames drive a session
      Given an authorized remote client
      When the client sends a session request as a WebSocket text frame
      Then the server answers with session events in the same newline-delimited JSON format used by local clients
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Paired devices are listed
      Given two paired devices
      When the operator lists the paired devices
      Then each device is shown with its id, name, pairing time, and last-seen time
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: A revoked device cannot reconnect
      Given a paired device
      When the operator revokes it by name
      Then the device is removed from the registry and its token is refused on the next connection attempt
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: The wrong upgrade path is refused
      Given a client holding a valid token
      When the client requests a WebSocket upgrade on a path other than /ws
      Then the upgrade is rejected with 404
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Two clients at the same time
      Given one authorized remote client attached to a session
      When a second authorized remote client connects
      Then both clients receive their own session events
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A token in the query string
      Given a browser client that cannot set request headers
      When the client connects with a token query parameter
      Then the upgrade is authorized
    ```

    ```gherkin
    @FR-11
    Scenario: Conflicting tokens are refused
      Given a request that carries a different token in the header and in the query string
      When the client requests a WebSocket upgrade
      Then the upgrade is rejected with 401
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Health check
      Given a running gateway
      When a client requests GET /health
      Then the response reports an ok status and the server version
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The dial address is resolved
      Given the gateway binds to a wildcard address on a machine that has a Tailscale MagicDNS name
      When the operator asks for the address to dial
      Then the Tailscale name is used
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The gateway is toggled from the TUI
      Given a user in a TUI session
      When the user runs the remote on command
      Then the gateway setting is persisted and the pairing and revocation logic of the CLI is used
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Last seen is recorded
      Given a paired device
      When the device connects to the gateway
      Then the last-seen timestamp of the device is updated
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Keepalive ping
      Given an idle gateway connection
      When 20 seconds pass without traffic
      Then the server sends a WebSocket ping and the connection stays open
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Pairing code lifetime
      Given a pairing code that was minted five minutes ago
      When a client posts it to /pair
      Then the response is 401 and no token is issued
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: The raw token is not persisted
      Given a device that has been paired
      When the device registry file is read
      Then it holds a hash of the token and not the token itself
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A missing token is refused
      Given a WebSocket upgrade request that carries no token
      When the client requests the upgrade
      Then the upgrade is rejected with 401 before any session stream is created
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Wildcard bind warning
      Given the gateway binds to a wildcard address
      When the operator views the remote status
      Then the status warns that the port accepts connections from any address
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: One client fails
      Given a gateway with one client attached
      When the connection of that client fails
      Then the listener keeps serving the other clients
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Bridge framing
      Given an authorized remote client
      When the client sends one request as a text frame
      Then the server reads exactly one newline-terminated request from the bridge
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Protocol parity
      Given a client that speaks the newline-delimited JSON protocol
      When the same client runs over the Unix socket and over the WebSocket gateway
      Then both runs produce the same session payloads
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Lifecycle logging
      Given a gateway that pairs a device and then receives a connection from it
      When the events are recorded
      Then the pairing and the connection are written to the log
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should an open WebSocket session be terminated when its device is revoked?
   Today revocation only blocks new connections.
2. Should the gateway terminate TLS itself, or is a trusted network such as Tailscale the intended transport?
   Today it speaks plain TCP.
3. Should `POST /pair` rate-limit pairing-code attempts?
   A six-digit code can be guessed within its five-minute lifetime.
4. Is the remote protocol meant to be versioned for third-party clients, or is the versioned harness API the surface intended for them?
   The answer decides whether the remote protocol needs a compatibility policy.
