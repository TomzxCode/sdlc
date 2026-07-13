---
title: "Agent Runtime"
status: done
---

# Test Plan: Agent Runtime

## Scope

Covers `pi-agent-core` agent loop, tool execution, message queues, abort, events, and the `AgentHarness` layer including compaction, skills, sessions, and system prompts.

## Unit Tests

Test files under `packages/agent/test/` cover:
- Agent loop and state machine (agent.test.ts, agent-loop.test.ts)
- Abort and cancellation flow
- Tool execution (sequential/parallel)
- Message queue steering and follow-up
- AgentHarness session lifecycle (harness/session.test.ts, harness/agent-harness.test.ts, harness/agent-harness-stream.test.ts)
- Compaction (harness/compaction.test.ts)
- Skills loading and injection (harness/skills.test.ts)
- Prompt templates (harness/prompt-templates.test.ts)
- System prompt building (harness/system-prompt.test.ts)
- Resource formatting (harness/resource-formatting.test.ts)
- Node execution environment (harness/nodejs-env.test.ts)
- Storage layer (harness/storage.test.ts)
- Session UUID generation (harness/session-uuid.test.ts)
- Truncation utilities (harness/truncate.test.ts)
- Repo-level logic (harness/repo.test.ts)

## Test Infrastructure

- Injectable `StreamFn` with controlled behavior (mock stream event sequences)
- In-memory session storage for deterministic testing
- `NodeExecutionEnv` for filesystem and shell tool testing

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (Agent class) | agent.test.ts |
| FR-02 (Agent loop) | agent-loop.test.ts |
| FR-03 (Injectable StreamFn) | agent-loop.test.ts |
| FR-04 (Sequential/parallel tool execution) | agent-loop.test.ts |
| FR-05 (Tool hooks) | agent.test.ts |
| FR-06 (Message queues) | agent.test.ts |
| FR-07 (Abort) | agent.test.ts |
| FR-08 (Event taxonomy) | agent-loop.test.ts |
| FR-09 (AgentHarness) | harness/agent-harness.test.ts |
| FR-10 (Extensible AgentMessage) | agent.test.ts |
| FR-11 (Proxy streaming) | harness/agent-harness-stream.test.ts |
| FR-12 (Compaction) | harness/compaction.test.ts |
| FR-13 (Branch summarization) | (covered in coding-agent test suite) |
| FR-14 (NodeExecutionEnv) | harness/nodejs-env.test.ts |
| NFR-01 (Single concurrent run) | agent.test.ts |
| NFR-02 (Failure as assistant message) | agent.test.ts |
| NFR-04 (Platform-agnostic core) | (module structure) |
