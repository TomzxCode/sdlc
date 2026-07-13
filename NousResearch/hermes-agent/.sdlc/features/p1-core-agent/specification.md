---
title: "Core Agent Loop"
status: done
---

# Specification: Core Agent Loop

## Overview

The core agent loop is a synchronous cycle inside AIAgent.run_conversation() that sends the message history plus tool schemas to the LLM, processes tool calls or text responses, and repeats until a terminal condition is met.

## Architecture

```
User Message
     │
     v
┌──────────────────────────────────────────┐
│  AIAgent.run_conversation()             │
│                                          │
│  while (budget.remaining > 0 and         │
│         api_call_count < max_iterations):  │
│    response = client.create(             │
│      messages=messages,                 │
│      tools=get_tool_definitions())      │
│                                          │
│    if response.tool_calls:                 │
│      for call in response.tool_calls:    │
│        result = handle_function_call(    │
│          call.name, call.args, task_id) │
│        messages.append(tool_result)      │
│      api_call_count++                    │
│    else:                                │
│      return response.content             │
│                                          │
│  return fallback response                  │
└──────────────────────────────────────────┘
```

## Data Models

### Conversation Message

| Field | Type | Constraints | Description |
|---|---|---|---|
| role | string | one of system/user/assistant/tool | Message role |
| content | string | nullable | Message text content |
| tool_calls | array | nullable | List of tool call objects from the LLM |
| tool_call_id | string | present on tool responses | Correlation ID for the tool call being responded to |
| name | string | present on tool responses | Name of the tool that was called |

## API Contracts

The agent communicates with LLM providers via the OpenAI chat completions format. No internal API contracts exist beyond the function call dispatch mechanism.

### handle_function_call(name, args)

**Input:** tool name + JSON arguments dict + optional task_id
**Output:** JSON string result

| Field | Type | Description |
|---|---|---|
| name | string | Tool name matching a registered schema |
| args | dict | JSON-serializable params matching the schema's parameters |
| task_id | string | Optional subagent task ID for delegation |

## Sequences

### Basic turn (no tool calls)
```
User → Agent → LLM → text response → User
```

### Tool-calling turn
```
User → Agent → LLM → tool_call(name, args)
Agent → registry.dispatch(name, args) → handler → JSON result
Agent → messages.append(tool role)
Agent → LLM (next turn) → text response → User
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Synchronous loop | Single-threaded blocking loop | Simpler state management, no race conditions on message history, easy interrupt handling |
| OpenAI format | OpenAI chat completions schema | Universal compatibility — most providers support it natively |
| Tool results as messages | Append tool-role messages to history | Standard OpenAI pattern; preserves full context for next LLM call |
| Budget grace call | One extra turn after budget exhaustion | Ensures the agent can summarize/clean up instead of being cut off mid-response |
| Interrupt check | Injected check at top of each iteration | No need for threading or signals; the check is just a boolean flag read |

## Risks and Unknowns

1. Large tool call loops can exhaust the iteration budget before producing a final response — the budget grace call mitigates this
2. Synchronous loop blocks the calling thread; the gateway uses asyncio to wrap the call, but long tool operations (browser, terminal) still block the agent

## Out of Scope

- Streaming response delivery (handled by surfaces, not by AIAgent)
- Async agent loop (future consideration)