---
title: "Session Runtime"
status: done
---

# Test Plan: Session Runtime

## Scope

The session lifecycle, prompt admission and promotion, execution coordination, compaction, history projection, and run coordinator.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Session creation persists metadata | New session request | Session stored with correct id/project |
| TC-2 | Prompt admission creates durable session_input row | Prompt message | Row exists before any provider call |
| TC-3 | Prompt promotion at safe boundary | Admitted prompt + continuation | Prompt appended to history once |
| TC-4 | Compaction starts new epoch | History exceeds threshold | Fresh baseline, new epoch |
| TC-5 | Run coordinator coalesces wakeups | Multiple concurrent wakes | Single drain per session |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Session runner executes full prompt-to-response | Active session, configured provider | Response received, tool calls executed |
| TC-7 | Session history reload before continuation | Mid-drain interruption | Projected history correct on resume |
| TC-8 | Session runner tool registry integration | Tool calls in model response | Tools executed, output bounded |
| TC-9 | Run coordinator joins same-session resumes | Two concurrent prompt calls | Single drain, both prompts admitted |
| TC-10 | Mid-conversation system message on context change | Context source changes mid-drain | System message emitted lazily at safe boundary |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Idle session interruption | No-op, no error |
| TC-12 | Prompt message ID reuse with different session | Rejected as conflict |
| TC-13 | Compacted session with no new input | No provider turn, history preserved |
| TC-14 | Session crash mid-drain | Durable artifacts survive, resume on restart |

## Test Infrastructure

- Effect-based test layer with fake storage and provider
- Recorded HTTP fixtures for deterministic provider responses
- Location-scoped test context with mock filesystem

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-2 |
| FR-02 | TC-3 |
| FR-03 | TC-4 |
| FR-04 | TC-6 |
| FR-05 | TC-8 |
| FR-06 | TC-8 |
| FR-07 | TC-4, TC-13 |
| FR-08 | TC-10 |
| FR-09 | TC-11 |
| FR-10 | TC-9 |
| FR-11 | TC-9 |
| NFR-01 | TC-14 |

## Test Files

- `packages/core/test/session-create.test.ts`
- `packages/core/test/session-compaction.test.ts`
- `packages/core/test/session-history.test.ts`
- `packages/core/test/session-projector.test.ts`
- `packages/core/test/session-prompt.test.ts`
- `packages/core/test/session-runner.test.ts`
- `packages/core/test/session-runner-message.test.ts`
- `packages/core/test/session-runner-model.test.ts`
- `packages/core/test/session-runner-recorded.test.ts`
- `packages/core/test/session-runner-tool-events.test.ts`
- `packages/core/test/session-runner-tool-registry.test.ts`
- `packages/core/test/session-run-coordinator.test.ts`
- `packages/core/test/session-todo.test.ts`
- `packages/core/test/session-tool-progress.test.ts`
- `packages/core/test/state.test.ts`
