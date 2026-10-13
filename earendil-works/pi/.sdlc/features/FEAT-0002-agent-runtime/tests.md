---
title: "Agent Runtime"
status: done
---

# Test Plan: Agent Runtime

## Scope

Covers `pi-agent-core` agent loop, tool execution, message queues, abort, events, and proxy streaming.
Durable sessions, compaction, skills, and system prompts are covered in the `@earendil-works/pi-durable` test suite.

## Unit Tests

Test files under `packages/agent/test/` cover:
- Agent loop and state machine (agent.test.ts, agent-loop.test.ts)
- Abort and cancellation flow
- Tool execution (sequential/parallel)
- Message queue steering and follow-up
- Proxy streaming (proxy.test.ts)
- End-to-end loop behavior (e2e.test.ts)
- Shared fixtures (utils/)

## Test Infrastructure

- Injectable `StreamFn` with controlled behavior (mock stream event sequences)
- Direct `Agent` construction with caller-supplied tools and queue modes

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
| FR-09 (AgentHarness) | (moved to `@earendil-works/pi-durable` in 1.0.0; covered in its test suite) |
| FR-10 (Extensible AgentMessage) | agent.test.ts |
| FR-11 (Proxy streaming) | proxy.test.ts |
| FR-12 (Compaction) | (moved to `@earendil-works/pi-durable` in 1.0.0; covered in its test suite) |
| FR-13 (Branch summarization) | (covered in pi-durable test suite) |
| FR-14 (NodeExecutionEnv) | (moved to `@earendil-works/pi-durable` in 1.0.0; covered in its test suite) |
| NFR-01 (Single concurrent run) | agent.test.ts |
| NFR-02 (Failure as assistant message) | agent.test.ts |
| NFR-04 (Platform-agnostic core) | (module structure) |
