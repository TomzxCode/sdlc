---
title: "Orchestrator"
status: done
---

# Specification: Orchestrator

## Overview

The orchestrator is a daemon (`orchestrator serve`) that exposes a Unix socket IPC server. A CLI client communicates with the daemon to spawn, list, status-check, stop, and send RPC commands to pi-coding-agent instances. Each instance is a child process running `pi --mode rpc`. The supervisor persists instance records to JSON and optionally registers with a Radius presence service for remote machine discovery.

## Architecture

```
+-------------------+          +----------------------+
| orchestrator CLI  |  IPC     | orchestrator serve   |
| (list, spawn,     |<-------->| (Unix socket daemon) |
|  status, stop,    |          |                      |
|  rpc, rpc-stream) |          +----------+-----------+
+-------------------+                      |
                                           | manages
                                           v
                              +---------------------------+
                              | OrchestratorSupervisor    |
                              | - spawnInstance()         |
                              | - stopInstance()          |
                              | - handleRpc()             |
                              | - openRpcStream()         |
                              +----+---------------------+
                                   | owns
                                   v
                     +-----------------------------+
                     | RpcProcessInstance (child)  |
                     | pi --mode rpc               |
                     | Unix socket IPC             |
                     +-----------------------------+
```

## Data Models

### InstanceRecord

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | UUID | Unique instance identifier |
| status | InstanceStatus | enum | starting, online, stopping, stopped, error |
| cwd | string | not null | Working directory |
| createdAt | string | ISO 8601 | Creation timestamp |
| lastSeenAt | string | optional | Last update timestamp |
| label | string | optional | Human-readable label |
| sessionId | string | optional | Current pi session ID |
| sessionFile | string | optional | Current pi session file path |
| radiusPiId | string | optional | Radius presence registration ID |

### IPC Protocol (excerpt)

| Request type | Payload | Response type |
|---|---|---|
| spawn | cwd, label? | spawn_result |
| list | — | list_result (InstanceSummary[]) |
| status | instanceId | status_result |
| stop | instanceId | stop_result |
| rpc | instanceId, command | rpc_result (RpcResponse) |
| rpc_stream | instanceId | rpc_ready (then bidirectional stream) |

## API Contracts

### orchestrator serve

Starts the daemon. Recovers persisted instances, starts Radius presence if configured, and listens on a Unix socket.

### orchestrator spawn --cwd <path> [--label <label>]

Spawns a child pi-coding-agent process in RPC mode, registers with Radius, and returns the instance ID.

### orchestrator rpc <instance-id> <json-command>

Sends a single RPC command to the instance and returns the response. Session metadata is refreshed after mutating commands (new_session, switch_session, fork, clone, set_session_name, prompt).

### orchestrator rpc-stream <instance-id>

Opens a bidirectional stream: the CLI forwards stdin JSONL to the instance as RPC commands and extension UI responses, and writes instance events to stdout.

## Sequences

### Instance spawn flow

```
orchestrator CLI -> serve daemon: spawn {cwd, label}
serve -> supervisor.spawnInstance()
  supervisor: create InstanceRecord (status: starting)
  supervisor: createRpcProcessInstance (child pi --mode rpc)
  supervisor: syncInstanceRecord (get_state)
  supervisor: radiusPresence.registerPi()
  supervisor: setStatus(online)
serve -> orchestrator CLI: spawn_result {instance}
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| IPC transport | Unix socket | Local-only, fast, no network overhead |
| Child process | pi --mode rpc | Reuses existing coding-agent RPC protocol |
| Persistence | JSON file (instances.json) | Simple, portable, no database dependency |
| Session sync | On-demand after mutating commands | Avoids unnecessary get_state calls on every RPC |
| Experimental status | Explicit disclaimer | Allows API evolution without commitment |

## Risks and Unknowns

1. Experimental package: the API surface may change or be removed without notice. Consumers should pin a specific version.
2. No test suite exists for the orchestrator (no test files found).
3. Unix socket only: no Windows support at this stage.
4. Radius presence integration depends on an external service; behavior when the service is unreachable needs hardening.

## Out of Scope

- The pi-coding-agent RPC protocol itself (FEAT-0004).
- Session persistence and branching (FEAT-0006).
- Extension API internals (FEAT-0005).
