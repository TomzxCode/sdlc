---
title: "Orchestrator"
status: done
---

# Requirements: Orchestrator

## Overview

`@earendil-works/pi-orchestrator` is an experimental daemon and CLI that manages multiple pi-coding-agent instances as child processes, providing a supervision layer for spawning, monitoring, stopping, and communicating with pi instances via IPC. It supports a Radius presence integration for remote machine registration and an RPC stream bridge for session event forwarding. The package is under active development and its API is not yet stable.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operators / automation users | Spawn and manage multiple pi instances from scripts or orchestration tooling |
| Maintainers | A supervision layer for multi-instance pi deployments without modifying the coding-agent core |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `serve` daemon command that starts a Unix socket IPC server for managing pi instances. |
| FR-02 | Must | The system shall support spawning new pi-coding-agent RPC instances with a specified cwd and optional label. |
| FR-03 | Must | The system shall support listing all managed instances with their status (starting, online, stopping, stopped, error). |
| FR-04 | Must | The system shall support querying the status of a specific instance by ID. |
| FR-05 | Must | The system shall support stopping a specific instance by ID, cleaning up its resources. |
| FR-06 | Must | The system shall support sending RPC commands to a running instance and receiving responses. |
| FR-07 | Must | The system shall support opening an RPC stream to an instance for bidirectional JSONL communication (commands, session events, extension UI requests). |
| FR-08 | Should | The system shall persist instance records to disk for recovery after restart. |
| FR-09 | Should | The system shall support Radius presence registration for remote machine discovery. |
| FR-10 | Should | The system shall recover instances on restart by marking previously-online instances as stopped and cleaning up Radius connections. |
| FR-11 | Should | The system shall support session metadata synchronization (sessionId, sessionFile) after commands that can change the session identity. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Correctness | Instance lifecycle transitions shall be consistent: starting -> online -> stopping -> stopped, with error as a terminal failure state. |
| NFR-02 | Must | Reliability | Unexpected RPC process exit shall mark the instance as error and clean up resources (Radius disconnect, subscriber notification). |
| NFR-03 | Should | Security | IPC shall use local Unix sockets only; no network exposure by default. |

## Constraints

- Experimental; the CLI, APIs, and behavior are not yet stable and may change without notice.
- Depends on `@earendil-works/pi-coding-agent` for RPC protocol types and process management.
- Unix socket IPC only (no Windows named pipe support at this stage).

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** the orchestrator CLI
    - **When** `orchestrator serve` is run
    - **Then** a Unix socket IPC server starts, listening on the configured socket path.
- [ ] **FR-02**
    - **Given** a running serve daemon
    - **When** `orchestrator spawn --cwd /path` is called
    - **Then** a new pi-coding-agent RPC instance is spawned and its ID is returned.
- [ ] **FR-06**
    - **Given** a running instance
    - **When** `orchestrator rpc <id> '{"type":"get_state"}'` is called
    - **Then** the response from the pi instance is returned.
- [ ] **NFR-02**
    - **Given** a running instance whose RPC process crashes
    - **When** the exit is detected
    - **Then** the instance status is set to error and persisted.

## Conflicts

None identified yet.

## Open Questions

1. What is the stabilization path for the orchestrator, and should its APIs be aligned with the coding-agent's SDK or be independent?
2. Should the orchestrator gain built-in support for non-Unix platforms (Windows named pipes, TCP with auth)?
