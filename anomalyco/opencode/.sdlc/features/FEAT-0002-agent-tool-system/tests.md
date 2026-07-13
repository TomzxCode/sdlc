---
title: "Agent & Tool System"
status: done
---

# Test Plan: Agent & Tool System

## Scope

Agent definitions, built-in tool execution, tool registry output bounding, permission model, and skill dispatcher.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Built-in build agent selects correct permissions | Agent name "build" | Full-access permissions |
| TC-2 | Built-in plan agent selects read-only permissions | Agent name "plan" | Read-only permissions |
| TC-3 | Tool output bounding truncates oversized results | Tool result > max bytes | Truncated within limit |
| TC-4 | Bash tool executes shell command | `echo hello` | stdout "hello\n" |
| TC-5 | Read tool reads file contents | File path | File text content |
| TC-6 | Write tool writes file contents | File path + content | File created with content |
| TC-7 | Skill tool invokes registered skill | Skill name | Skill executed |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Tool registry bounds model-visible output | Tool call with large output | Bounded model tool output persisted |
| TC-9 | Permission prompt for dangerous tools | Unapproved tool call | Permission requested before execution |
| TC-10 | Managed tool output file for oversized text | Tool output > history limit | File created, preview in history |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Non-existent tool called | ToolError returned to model |
| TC-12 | Tool throws runtime exception | ToolError, model can retry |
| TC-13 | Tool output exactly at boundary | Not truncated |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2 |
| FR-02 | TC-4, TC-5, TC-6 |
| FR-03 | TC-3, TC-8 |
| FR-06 | TC-7 |
| NFR-01 | TC-9 |
| NFR-02 | TC-11, TC-12 |

## Test Files

- `packages/core/test/agent.test.ts`
- `packages/core/test/application-tools.test.ts`
- `packages/core/test/tool-apply-patch.test.ts`
- `packages/core/test/tool-bash.test.ts`
- `packages/core/test/tool-edit.test.ts`
- `packages/core/test/tool-question.test.ts`
- `packages/core/test/tool-read.test.ts`
- `packages/core/test/tool-read-filesystem.test.ts`
- `packages/core/test/tool-skill.test.ts`
- `packages/core/test/tool-todowrite.test.ts`
- `packages/core/test/tool-webfetch.test.ts`
- `packages/core/test/tool-websearch.test.ts`
- `packages/core/test/tool-write.test.ts`
- `packages/core/test/tool-output-store.test.ts`
- `packages/core/test/permission.test.ts`
