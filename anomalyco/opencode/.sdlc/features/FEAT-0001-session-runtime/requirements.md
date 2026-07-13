---
title: "Session Runtime"
status: done
---

# Requirements: Session Runtime

## Overview

The Session Runtime is the core engine of OpenCode.
It preserves durable conversational history while assembling the system context an agent needs to act in its environment, and it executes provider turns with tool settlement and compaction.
The V2 design separates durable prompt admission from process-local model execution so sessions survive restarts and can later be clustered.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Sessions that survive crashes and restart with full history replay |
| Core team | Clean separation of durable admission from execution; no legacy tool loops |
| Operators | Introspectable, replayable sessions; interruption that targets the right process |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall persist each user prompt as a durable `session_input` row before scheduling execution. |
| FR-02 | Must | The system shall promote admitted prompts into session history only at a safe provider-turn boundary. |
| FR-03 | Must | The system shall render a baseline system context at the start of each context epoch and reuse it across restarts. |
| FR-04 | Must | The system shall make exactly one `llm.stream(request)` call per provider turn and reload projected history before durable continuation. |
| FR-05 | Must | The system shall execute tool calls through the Location-scoped tool registry and persist bounded model tool output to history. |
| FR-06 | Must | The system shall spill oversized tool output to managed tool-output files while retaining a bounded preview in history. |
| FR-07 | Must | The system shall start a new context epoch with a fresh baseline on completed compaction. |
| FR-08 | Must | The system shall emit durable mid-conversation system messages when context sources change, admitted lazily at the next safe boundary. |
| FR-09 | Must | The system shall interrupt the active process-local ownership chain for a session and treat idle/missing interruption as a no-op. |
| FR-10 | Should | The system shall treat steering prompts and queued prompts with distinct promotion semantics at safe boundaries. |
| FR-11 | Should | The system shall coalesce prompt wakeups and allow different sessions to run concurrently via the run coordinator. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Session drains shall be process-local and resumable from durable artifacts after a crash. |
| NFR-02 | Must | Correctness | Context source rendering shall be deterministic regardless of concurrent producer evaluation. |
| NFR-03 | Should | Performance | Provider-turn allowance shall reset once per batch of promoted inputs, not per input. |
| NFR-04 | Should | Observability | Each drain and compaction shall be traceable through Effect telemetry. |

## Constraints

- Prompt admission and execution must remain separate; `SessionV2.prompt(...)` admits one durable row then schedules advisory `SessionExecution.wake`.
- Reusing a session ID adopts the existing session; reusing a prompt message ID reconciles an exact retry only when session, prompt, and delivery mode match.
- `SessionExecution` is process-global and session-ID based; no layer may take a session ID into execution plumbing.
- Local session drains remain process-local until clustering is implemented.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a client posts a prompt to an existing session
    - **When** the server receives it
    - **Then** a durable `session_input` row exists before any provider call is scheduled
- [ ] **FR-02**
    - **Given** an admitted prompt and an in-progress drain requiring continuation
    - **When** the runner reaches a safe provider-turn boundary
    - **Then** the prompt is promoted into session history exactly once
- [ ] **FR-04**
    - **Given** a provider turn is running
    - **When** it executes
    - **Then** exactly one `llm.stream` call occurs and projected history was reloaded beforehand
- [ ] **FR-07**
    - **Given** history exceeds compaction thresholds
    - **When** compaction completes
    - **Then** a new context epoch begins with a freshly rendered baseline and earlier mid-conversation system messages leave projected model history
- [ ] **FR-08**
    - **Given** a context source value changes during a drain
    - **When** the next safe provider-turn boundary is reached
    - **Then** one combined mid-conversation system message is admitted durably
- [ ] **FR-09**
    - **Given** an active ownership chain for a session
    - **When** an interruption is requested
    - **Then** the active chain is targeted and an idle session yields a no-op
- [ ] **NFR-02**
    - **Given** multiple context sources registered with stable keys
    - **When** the system context is rendered
    - **Then** the output is identical regardless of producer evaluation order

## Conflicts

None identified yet.

## Open Questions

1. How should post-crash continuation recovery retry provider work (explicitly deferred design)?
2. When will clustered session execution move beyond process-local drains?
