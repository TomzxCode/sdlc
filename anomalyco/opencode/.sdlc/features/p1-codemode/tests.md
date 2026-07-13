---
title: "CodeMode"
status: done
---

# Test Plan: CodeMode

## Scope

Confined JavaScript execution: one-shot and reusable execution, tool interface, sandbox limits, error taxonomy, OpenAPI tool generation.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | One-shot execute with tools | `execute({ tools, code })` | Program runs, result returned |
| TC-2 | Reusable runtime with limits | `make({ tools, limits }), execute` | Multiple calls share toolset |
| TC-3 | Program denied ambient access | `require('fs')` | Access denied |
| TC-4 | Structured result returned | Tool results | Result typed correctly |
| TC-5 | Parallel tool calls | Independent tools | Both executed, results combined |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | OpenAPI tool schema generation | OpenAPI spec | Schema generated |
| TC-7 | Standard library functions | stdlib call | Expected output |
| TC-8 | Enumeration support | Enum type | Enum handled |
| TC-9 | Promise-based tool calls | async tool | Promises settled |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-10 | Parse error in program | ToolError: parse |
| TC-11 | Runtime error in program | ToolError: runtime |
| TC-12 | Tool refusal by host | ToolError: tool_refusal |
| TC-13 | Timeout exceeded | ToolError: timeout |
| TC-14 | Output exceeds max size | ToolError: output_limit |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-2 |
| FR-3 | TC-3 |
| FR-4 | TC-4 |
| FR-5 | TC-5 |
| FR-6 | TC-13, TC-14 |
| FR-7 | TC-10, TC-11, TC-12 |
| NFR-1 | TC-3 |
| NFR-2 | TC-11 |
| NFR-3 | TC-5 |

## Test Files

- `packages/codemode/test/codemode.test.ts`
- `packages/codemode/test/enumeration.test.ts`
- `packages/codemode/test/openapi.test.ts`
- `packages/codemode/test/parity.test.ts`
- `packages/codemode/test/promise.test.ts`
- `packages/codemode/test/signature.test.ts`
- `packages/codemode/test/stdlib.test.ts`
