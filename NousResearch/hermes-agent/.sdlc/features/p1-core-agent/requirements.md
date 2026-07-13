---
title: "Core Agent Loop"
status: done
---

# Requirements: Core Agent Loop

## Overview

The AIAgent class (run_agent.py) is the narrow waist of the entire system: a synchronous conversation loop that sends messages with tool schemas to an OpenAI-compatible API, processes tool calls, manages budgets and iterations, and returns final responses. All surfaces (CLI, gateway, TUI, desktop) funnel through it.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | The agent must respond correctly, handle multi-turn tool use, respect iteration budgets, and recover from API errors |
| Plugin/skill developers | The loop must correctly inject tool schemas from enabled toolsets and plugins |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The agent shall accept a user message and return a response after zero or more tool-calling iterations |
| FR-2 | Must | The agent shall support a configurable max_iterations limit and stop gracefully when exceeded |
| FR-3 | Must | The agent shall maintain an iteration budget that is shared with subagents and decr across turns |
| FR-4 | Must | The agent shall support interrupt requests that stop the loop at the next safe point |
| FR-5 | Must | The agent shall preserve strict message role alternation (never two same-role messages in a row) |
| FR-6 | Must | The agent shall maintain a byte-stable system prompt across turns for prompt caching |
| FR-7 | Must | The agent shall dispatch tool calls to registered handlers and append results as tool-role messages |
| FR-8 | Should | The agent shall support a predictive usage mode that estimates tokens before the API call |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | The loop shall not add more than 50ms overhead per turn beyond the LLM API call time |
| NFR-2 | Must | Reliability | Agent shall recover gracefully from transient API errors with configurable retry logic |
| NFR-3 | Must | Compatibility | The agent shall work with any OpenAI-compatible chat completions endpoint |

## Constraints

- Tool handlers must return JSON strings
- Message format must follow OpenAI chat completions schema
- Budget tracking must be consistent across parent and child (subagent) sessions

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a running agent
    - **When** a user sends a message that requires no tool calls
    - **Then** the agent returns the final response directly
- [ ] **FR-2**
    - **Given** an agent configured with max_iterations=3
    - **When** the LLM issues tool calls on every turn
    - **Then** the loop stops after 3 iterations and returns the last assistant response
- [ ] **FR-5**
    - **Given** a conversation with history
    - **When** the agent processes a tool call result and an assistant response
    - **Then** no two consecutive messages have the same role
- [ ] **NFR-1**
    - **Given** a call to run_conversation()
    - **When** the LLM returns immediately
    - **Then** the overhead between receiving the LLM response and appending the tool result is under 50ms

## Conflicts

None identified yet.

## Open Questions

1. Should the budget be configurable per-turn or only per-session?