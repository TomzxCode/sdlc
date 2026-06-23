---
title: "Agent Runtime"
status: draft
---

# Specification: Agent Runtime

## Overview

`pi-agent-core` is split into a low-level layer (`Agent`, `agentLoop`) and a high-level `AgentHarness`.
The low-level layer is transport-agnostic and delegates LLM calls to an injectable `StreamFn`.
The harness adds durable session storage, compaction, skills, system prompts, and a rich provider/session hook surface.

## Architecture

```
+---------------------------------------------------+
|                  AgentHarness                     |
|  sessions, compaction, skills, system-prompt,     |
|  provider/session hooks (before_provider_request, |
|  tool_call, session_before_compact, ...)          |
+-------------------------+-------------------------+
                          | owns
                          v
+---------------------------------------------------+
|                    Agent                          |
|  transcript, tools, model/thinking, message       |
|  queues, lifecycle (prompt/continue/abort)        |
+-------------------------+-------------------------+
                          | drives
                          v
+---------------------------------------------------+
|                   agentLoop                       |
|  stream -> extract tools -> execute -> continue   |
+-------------------------+-------------------------+
                          | calls
                          v
                +---------------------+
                |   StreamFn (inject) |  default: pi-ai streamSimple
                +---------------------+  alt: streamProxy (server)
```

## Data Models

### AgentState

| Field | Type | Constraints | Description |
|---|---|---|---|
| systemPrompt | string | optional | Active system prompt |
| model | Model | not null | Active LLM model |
| thinkingLevel | ThinkingLevel | not null | Reasoning effort |
| tools | AgentTool[] | not null | Registered tools |
| messages | AgentMessage[] | not null | Transcript (app-extensible) |
| isStreaming | boolean | readonly | True while a run is active |
| streamingMessage | AssistantMessage | readonly | Partial message during stream |
| pendingToolCalls | Set | readonly | Tool calls in flight |
| errorMessage | string | readonly | Last run error, if any |

### AgentTool

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | not null | Tool name |
| description | string | not null | LLM-facing description |
| parameters | TSchema | not null | TypeBox parameter schema |
| label | string | optional | UI label |
| execute | function | not null | `(id, args, signal, onUpdate) -> result` |
| prepareArguments | function | optional | Pre-execution arg transform |
| executionMode | enum | optional | `sequential` or `parallel` |

### AgentMessage

A union of pi-ai `Message` types plus app-injected custom message types via declaration merging.
`convertToLlm` bridges `AgentMessage[]` to pi-ai `Message[]` for the stream; `transformContext` optionally rewrites the `AgentMessage[]` before conversion.

### AgentEvent

| Type | Emitted | Carries |
|---|---|---|
| agent_start / agent_end | run begin / end | - |
| turn_start / turn_end | each turn | - |
| message_start / update / end | stream lifecycle | partial/full assistant message |
| tool_execution_start / update / end | per tool | tool id, params, progress, result |

## API Contracts

### Agent.prompt(messages) / Agent.continue()

**Request**: `AgentMessage[]` for `prompt`; none for `continue` (resumes from current context; last message must be user/toolResult).

**Response**: an async subscription; results arrive via `subscribe()` events. Throws if an agent is already running.

### StreamFn

| Field | Type | Required | Description |
|---|---|---|---|
| model | Model | yes | Target model |
| context | Context | yes | Messages, tools, system prompt, reasoning |
| apiKey | ModelAuth | optional | Explicit auth |
| signal | AbortSignal | optional | Cancellation |

**Response**: an `AssistantMessageEventStream`. Must never throw; failures are terminal stream events.

## Sequences

### Agent loop (single turn)

```
turn_start
  -> transformContext (AgentMessage[])
  -> convertToLlm (-> Message[])
  -> StreamFn(context)
  -> stream deltas -> message_update events
  -> done -> message_end
  -> extract tool calls
  -> beforeToolCall (can block)
  -> execute tools (sequential|parallel) -> tool_execution_* events
  -> afterToolCall (can override/terminate)
  -> append tool results to context
turn_end
  -> drain steering messages? loop
  -> else drain follow-up messages? outer loop
agent_end (after listeners settle)
```

### Failure handling

```
run executor throws
  -> handleRunFailure: synthesize assistant message (stopReason: aborted|error)
  -> emit message_end, agent_end
  -> finishRun: clear runtime state
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport boundary | Injectable `StreamFn` | Enables direct, proxy, and custom backends without coupling to pi-ai |
| Message extensibility | Declaration-merged `AgentMessage` | Apps add custom types without forking; `convertToLlm` is the bridge |
| Parallel tool execution | Completion-order events, source-order results | Parallelism for speed, deterministic transcript ordering |
| Idle definition | After `agent_end` listeners settle | Listeners can perform async cleanup before idle |
| Core vs Node | `./node` entrypoint | Keeps core platform-agnostic; Node fs/shell isolated |

## Risks and Unknowns

1. Overlap between `AgentHarness` and coding-agent's `AgentSession` could lead to duplicated session/compaction logic.
2. The declaration-merge extensibility model is powerful but can make type errors hard to localize.
3. Parallel tool execution ordering semantics are subtle; regressions here are hard to detect without targeted tests.

## Out of Scope

- LLM provider abstraction and streaming protocol (FEAT-0001).
- Terminal rendering (FEAT-0003).
- Interactive TUI, slash commands, and the CLI product (FEAT-0004).
- Coding-agent-specific session format and branching UI (FEAT-0006).
