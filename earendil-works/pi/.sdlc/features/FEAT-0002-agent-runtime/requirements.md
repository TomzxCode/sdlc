---
title: "Agent Runtime"
status: draft
---

# Requirements: Agent Runtime

## Overview

`pi-agent-core` provides the stateful agent runtime that sits between the LLM abstraction (`pi-ai`) and application UIs.
It owns the transcript, runs the prompt-stream-tool-continue loop, executes tools (sequentially or in parallel), manages message queues (steering and follow-up), and exposes a higher-level `AgentHarness` with sessions, compaction, skills, and provider hooks.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Coding agent (pi-coding-agent) | A reliable `Agent`/`AgentHarness` to drive prompts, tools, and session lifecycle |
| SDK / embedding users | A transport-agnostic runtime they can point at any `StreamFn` |
| Extension authors | Typed hooks (`tool_call`, `tool_result`, `before_provider_request`, etc.) to observe and mutate behavior |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide an `Agent` class owning the transcript, tools, model, and thinking level, with `prompt`, `continue`, `abort`, and `subscribe` methods. |
| FR-02 | Must | The system shall run an agent loop that streams an assistant response, extracts tool calls, executes them, and continues until no more tool calls or queued messages remain. |
| FR-03 | Must | The system shall call an injectable `StreamFn` (default pi-ai `streamSimple`) to reach the LLM, keeping the runtime transport-agnostic. |
| FR-04 | Must | The system shall execute tool calls either sequentially or in parallel based on config and per-tool `executionMode`, emitting `tool_execution_*` events in completion order while persisting tool results in source order. |
| FR-05 | Must | The system shall validate tool arguments before execution and support `beforeToolCall`/`afterToolCall` hooks that can block, override, or terminate a tool call. |
| FR-06 | Must | The system shall support message queues for steering (delivered after the current tool batch) and follow-up (delivered after the agent stops). |
| FR-07 | Must | The system shall support abort via an `AbortController` whose signal flows to `streamFn` and tool `execute`. |
| FR-08 | Must | The system shall emit a stable event taxonomy: `agent_start/end`, `turn_start/end`, `message_start/update/end`, `tool_execution_start/update/end`. |
| FR-09 | Must | The system shall provide an `AgentHarness` wrapping `Agent` with sessions, compaction, skills, system-prompt building, and provider hooks. |
| FR-10 | Must | The system shall support app-extensible `AgentMessage` types via declaration merging, with `convertToLlm` bridging to pi-ai messages and an optional `transformContext` hook. |
| FR-11 | Should | The system shall provide a `streamProxy` function for routing LLM calls through a server with bandwidth-reduced events. |
| FR-12 | Should | The system shall include compaction utilities (`compact`, `shouldCompact`, `estimateTokens`, `findCutPoint`). |
| FR-13 | Should | The system shall include branch-summarization utilities. |
| FR-14 | Should | The system shall provide a `NodeExecutionEnv` (filesystem + shell) via the `./node` entrypoint. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Exactly one active run per `Agent` shall be allowed; concurrent `prompt` calls shall throw. |
| NFR-02 | Must | Reliability | Run failures shall be surfaced as a synthetic failure assistant message with `stopReason: "aborted" \| "error"` followed by `agent_end`. |
| NFR-03 | Must | Correctness | The run shall not be considered idle until `agent_end` listeners have settled. |
| NFR-04 | Must | Portability | Core modules shall be platform-agnostic; Node-specific code shall live behind the `./node` entrypoint. |
| NFR-05 | Should | Maintainability | A stable, backend-independent error taxonomy (`FileErrorCode`, `ExecutionErrorCode`, `CompactionErrorCode`, `SessionErrorCode`) shall be used for fallible operations. |

## Constraints

- Built on `pi-ai` via the `StreamFn` boundary; does not import provider SDKs directly.
- Erasable TypeScript syntax only; ESM only.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-02**
    - **Given** an agent with tools and a prompt that triggers tool calls
    - **When** the agent loop runs to completion
    - **Then** it streams the response, executes the tool calls, appends results, and continues until there are no more tool calls or queued messages.
- [ ] **FR-04**
    - **Given** a batch of parallel-capable tool calls plus one sequential tool
    - **When** the batch executes
    - **Then** the whole batch runs sequentially and `tool_execution_end` events fire in completion order, while persisted tool-result messages preserve assistant source order.
- [ ] **FR-05**
    - **Given** a `beforeToolCall` hook returning `{ block: true }`
    - **When** the tool is about to execute
    - **Then** the call is blocked and an error tool result is recorded.
- [ ] **FR-06**
    - **Given** a streaming agent and an incoming steering message
    - **When** the current tool batch completes
    - **Then** the steering message is delivered to the agent before it stops.
- [ ] **FR-07**
    - **Given** an in-progress run
    - **When** `abort()` is called
    - **Then** the abort signal propagates to the active stream and executing tools.
- [ ] **NFR-01**
    - **Given** an agent with an active run
    - **When** `prompt` is called again concurrently
    - **Then** the second call throws rather than interleaving.
- [ ] **NFR-02**
    - **Given** a run that throws unexpectedly
    - **When** the error is caught
    - **Then** a synthetic failure assistant message with an appropriate `stopReason` is emitted, followed by `agent_end`.

## Conflicts

None identified yet.

## Open Questions

1. Should `streamProxy` remain a first-class supported deployment mode, or is it expected to migrate to an extension?
2. What is the long-term relationship between `AgentHarness` and the coding-agent's own `AgentSession` (overlap, merge, or distinct layers)?
