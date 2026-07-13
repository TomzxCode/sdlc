---
title: "Agent Runtime"
status: done
---

# Test Plan: Agent Runtime

## Scope

Tests cover agent conversation loop, tool execution, context management, subagent spawning, model provider integration, and system prompts. Does not cover individual provider implementations or channel behavior.

## Unit Tests

| File | Description |
|---|---|
| `src/agents/cli-session.test.ts` | CLI session lifecycle |
| `src/agents/agent-scope.test.ts` | Agent scope resolution |
| `src/agents/system-prompt.test.ts` | System prompt construction |
| `src/agents/tool-catalog.test.ts` | Tool catalog and discovery |
| `src/agents/context.test.ts` | Context window management |
| `src/agents/subagent-spawn.test.ts` | Subagent spawning lifecycle |
| `src/agents/model-runtime-policy.test.ts` | Model runtime policy enforcement |
| `src/agents/agent-run-terminal-outcome.test.ts` | Agent run terminal state handling |
| `src/agents/transcript-policy.test.ts` | Transcript recording policy |

## End-to-End Tests

| File | Description |
|---|---|
| `src/agents/embedded-agent-runner.e2e.test.ts` | Embedded agent runner end-to-end |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Provider API failure | Model fallback within 30 seconds |
| Context window exceeded | Compaction triggered, conversation continues |
| Tool execution timeout | Tool call terminated, error returned to model |
| Subagent spawn failure | Parent agent recovers gracefully |

## Test Infrastructure

- Vitest unit test runner with project matrix
- Mock model providers for deterministic testing
- In-memory SQLite for transcript persistence
- Embedded runner for end-to-end agent turns

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (Model provider support) | `model-runtime-policy.test.ts` |
| FR-2 (Context compaction) | `context.test.ts` |
| FR-3 (Tool execution) | `tool-catalog.test.ts` |
| FR-4 (Subagent spawning) | `subagent-spawn.test.ts` |
| FR-7 (Transcript persistence) | `transcript-policy.test.ts` |
| FR-8 (System prompt customization) | `system-prompt.test.ts` |
