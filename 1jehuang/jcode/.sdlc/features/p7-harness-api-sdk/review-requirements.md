---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
The following discrepancies were found by comparing the document against the current code.

### Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall expose native runtime commands to SDK clients without turning them into agent prompts. | `crates/jcode-harness-api/src/runtime_commands.rs:7-37` (29 variants), `crates/jcode-harness-api/src/requests.rs:188`, `crates/jcode-sdk/src/client.rs:1043`, `sdk/typescript/src/client.ts:787`. |
| FR-10 | The system shall support transferring a session between clients. | `crates/jcode-harness-api/src/requests.rs:85` (`TransferSession`), `crates/jcode-sdk/src/client.rs:812`, `sdk/typescript/src/client.ts:798`. |
| FR-11 | The system shall expose global user-session connection presence to SDK clients. | `crates/jcode-harness-api/src/events.rs:464-468` (`user_connected`), `crates/jcode-harness-api-server/src/lib.rs:370,398` (`session_connections` capability). |
| FR-12 | The system shall negotiate the `user_response` capability during the handshake so only opted-in clients receive Markdown responses. | `crates/jcode-harness-api/src/requests.rs:39-41` (`hello.supports_user_response`), `crates/jcode-harness-api-server/src/translate.rs:607`. |
| FR-13 | The system shall support an stdio transport for SSH-based SDK clients. | `crates/jcode-harness-api-server/src/lib.rs:300` (`run_bridge_stdio`), `crates/jcode-sdk/src/ssh.rs:41`, `tests/api_stdio_cli.rs`. |
| FR-14 | The system shall let the server perform account failover for API clients rather than the client. | `crates/jcode-protocol/src/wire.rs:154-158` (`supports_server_failover`), `crates/jcode-harness-api-server/src/translate.rs:611`. |

### Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-7 | "The system shall expose session control (start, send message, cancel) and structured events." | The request surface is now 45 request variants and 48 event variants, including fork, transfer, rewind, archive, restore, compact, soft interrupt, and tool configuration. The wording understates the contract. | "The system shall expose session control (create, attach, fork, transfer, detach, send message, soft interrupt, cancel, compact, rewind, archive/restore, model and tool configuration) and structured events." |

### Stakeholders

The "Desktop/iOS app teams" row states that the iOS app consumes sessions through the harness API.
The iOS app instead mirrors the internal protocol over a paired WebSocket gateway (`ios/Sources/JCodeKit/Wire.swift:5`, `ios/Sources/JCodeKit/Gateway.swift:6-8`).
Split the row into "Desktop app teams" (harness API) and "iOS app teams" (internal protocol over the gateway).

### Testability

The acceptance criteria list ends at NFR-4 and covers no requirement for any of the six new capabilities above.
Each added FR needs at least one Gherkin acceptance criterion.

### Open questions

Open Question 1 is partly answerable: the current API version is v1.11 (`API_VERSION_MAJOR = 1`, `API_VERSION_MINOR = 11` in `crates/jcode-harness-api/src/lib.rs:54-56`; mirrored at `sdk/typescript/src/protocol.ts:11`).
Only the deprecation policy for older versions remains inferred from code.

## Clarity

No other clarity issues found.

## Conflicts

No issues found.
