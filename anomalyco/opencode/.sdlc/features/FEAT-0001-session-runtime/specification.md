---
title: "Session Runtime"
status: done
---

# Specification: Session Runtime

## Overview

The V2 session runtime admits durable prompts, promotes them at safe boundaries, renders an immutable baseline system context per epoch, and runs one provider turn at a time with tool settlement and compaction.
Execution is coordinated by a process-global `SessionExecution` that discovers placement through `SessionStore` and a location map; drains have no durable identity.

## Architecture

```
SessionV2.prompt() ──admit──▶ session_input (durable)
                                   │ advisory wake
                                   ▼
                         SessionExecution (process-global)
                                   │ drain
                          SessionRunCoordinator
                          (joins resumes, coalesces wakeups)
                                   │
                         SessionRunner (Location-scoped)
                  ┌────────────────┼─────────────────┐
                  ▼                ▼                 ▼
          prompt promotion   system context     llm.stream (1x)
          (safe boundary)    registry/epoch          │
                                                     ▼
                                          tool registry (Location)
                                                     │
                                        bounded model tool output
                                        + managed output files
```

## Data Models

### session_input

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | ulid | PK, not null | Prompt/message identity |
| session_id | id | FK, not null | Owning session |
| delivery | enum | not null | `steer` or `queue` |
| status | enum | not null | admitted, promoted, etc. |

### context_epoch

| Field | Type | Constraints | Description |
|---|---|---|---|
| session_id | id | FK, not null | Owning session |
| baseline | text | not null | Immutable baseline system context |
| snapshot | json | not null | Context snapshot per source key |

### mid_conversation_system_message

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | ulid | PK | Message identity |
| session_id | id | FK | Owning session |
| rendered | text | not null | Exact combined text sent to the model |

## API Contracts

Internal runtime contracts (not HTTP; the HTTP surface is covered by FEAT-0006).

### SessionV2.prompt(request) -> Prompt

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| sessionID | id | yes | Target session |
| messageID | id | yes | Prompt identity (reused for exact-retry reconciliation) |
| delivery | enum | no | Defaults to `steer` |

**Behavior:** admits one durable `session_input` row, then schedules `SessionExecution.wake(sessionID)` unless `resume: false` requests admit-only behavior.

## Sequences

### Prompt admission and promotion

```
Client -> SessionV2.prompt -> session_input (admitted)
SessionV2.prompt -> SessionExecution.wake (advisory)
SessionExecution -> SessionRunCoordinator (join/coalesce)
SessionRunner -> promote eligible input at safe boundary
SessionRunner -> render baseline if new epoch
SessionRunner -> llm.stream (single call)
Model -> tool calls -> Tool Registry -> bounded output -> history
```

### Compaction

```
SessionRunner detects threshold -> compaction
compaction complete -> new Context Epoch -> fresh baseline + snapshot
earlier mid-conversation system messages leave projected model history
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Admission vs execution | Separate; prompt admits then wakes | Survives crashes; enables future clustering |
| Drains | Process-local, no durable identity | Clustering deferred; durable recovery reasons from artifacts |
| Provider turns | One `llm.stream` per turn, history reloaded | Avoids bridging legacy tool loops |
| Interruption | Targets active process-local ownership chain | Idle/missing interruption is a no-op |
| Context admission | Lazy at safe boundary | Deterministic; never pushed asynchronously |

## Risks and Unknowns

1. Post-crash continuation recovery has no durable drain identity and requires a separate explicit design before it may retry provider work.
2. Clustering moves drains off a single process; placement semantics for explicit workspace identity are reserved for the future.
3. `experimental.chat.system.transform` can mutate the baseline arbitrarily and has no V2 plugin equivalent yet.

## Out of Scope

- HTTP API surface (see FEAT-0006).
- Provider/model catalog resolution (see FEAT-0003).
- Tool execution semantics beyond bounded output (see FEAT-0002).
