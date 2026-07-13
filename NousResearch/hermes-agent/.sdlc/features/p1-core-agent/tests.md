---
title: "Core Agent Loop"
status: done
---

# Test Plan: Core Agent Loop

## Scope

Tests covering the AIAgent class, conversation loop, tool calling, budget tracking, interrupt handling, message role alternation, provider adapters, and error recovery.

## Test Files

- tests/run_agent/ — 115+ test files covering run_agent.py core loop behavior
- tests/agent/ — 226 test files covering provider adapters, memory, compression, tool calling, streaming, error recovery
- tests/run_agent/test_run_agent.py — Main test suite for conversation loop
- tests/run_agent/test_streaming.py — Streaming response tests
- tests/run_agent/test_tool_call_guardrail_runtime.py — Tool call guardrail tests
- tests/run_agent/test_iteration_budget_race.py — Budget tracking tests
- tests/run_agent/test_interactive_interrupt.py — Interrupt handling
- tests/run_agent/test_provider_fallback.py — Provider fallback and error recovery

## Unit Tests

Key unit test coverage areas:
- Tool call dispatch and argument coercion
- Message role alternation enforcement
- Iteration budget tracking and grace call
- System prompt byte-stability
- API error recovery and retry logic
- Stream interruption and circuit breaker

## Integration Tests

- Agent loop with real/fake LLM providers
- Tool result persistence in message history
- Multi-turn conversation flows
- Budget sharing with subagents
- Concurrent interrupt handling

## End-to-End Tests

- tests/run_agent/test_run_agent.py — Full conversation loop with tool calling
- tests/run_agent/test_codex_app_server_integration.py — Codex provider integration

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| LLM returns empty response | Agent retries or returns graceful error |
| Tool call with malformed JSON | JSON decode error recovery |
| Budget exhausted mid-tool-loop | Grace call allows one final turn |
| Interrupt during tool execution | Loop breaks at next safe point |
| Provider returns 429 rate limit | Retry with backoff |
| Message sequence gets two same-role messages | Sequence repair normalizes |

## Test Infrastructure

- pytest with hermetic runner (scripts/run_tests.sh)
- Mock providers for deterministic testing
- Temp HERMES_HOME isolation per test
- Subprocess-per-test-file isolation

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (accept message, return response) | test_run_agent.py basic flow tests |
| FR-2 (max_iterations limit) | test_iteration_budget_race.py |
| FR-3 (iteration budget) | test_iteration_budget_race.py |
| FR-4 (interrupt requests) | test_interactive_interrupt.py, test_exit_cleanup_interrupt.py |
| FR-5 (message role alternation) | test_message_sequence_repair.py |
| FR-6 (byte-stable system prompt) | Implicit in caching tests |
| FR-7 (tool call dispatch) | test_tool_call_guardrail_runtime.py, test_tool_arg_coercion.py |
| NFR-1 (50ms overhead) | Performance benchmark tests |
| NFR-2 (transient error recovery) | test_jsondecodeerror_retryable.py, test_nonretryable_error_html_summary.py |
| NFR-3 (OpenAI-compatible) | test_create_openai_client_*.py |
