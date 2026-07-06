---
title: "CodeMode"
status: draft
---

# Specification: CodeMode

## Overview

CodeMode provides an Effect-native confined execution environment where a model can write JavaScript programs that call only explicitly host-supplied tools.
The implementation lives in `packages/codemode` and exposes two modes: one-shot execution and a reusable runtime with configured limits.

## Architecture

```
Host Application
    │
    ├── CodeMode.execute({ tools, code })
    │       │
    │       ▼
    │   Sandbox (confined JS runtime)
    │       │
    │       ▼
    │   Tool calls (only provided tools)
    │       │
    │       ▼
    │   Structured result │ ToolError
    │
    ├── CodeMode.make({ tools, limits })
    │       │
    │       ▼
    │   ReusableRuntime
    │       ├── runtime.execute(code)
    │       └── runtime.execute(otherCode)
    │
    Host owns: authorization, persistence, external authority, tool delivery semantics
```

## Data Models

No durable models; CodeMode is a transient execution engine.

### ToolInterface

| Property | Type | Description |
|---|---|---|
| name | string | Tool name used in the program |
| schema | Schema | Effect Schema for the tool's input/output |
| handler | (input) => Effect | The tool implementation |

### Limits

| Field | Type | Default | Description |
|---|---|---|---|
| timeout | number | 30000 | Max execution time in ms |
| maxOutputSize | number | 1048576 | Max output size in bytes |

## API Contracts

### CodeMode.execute

**Signature:** `Effect<unknown, ToolError, CodeModeContext>`

**Input:** `{ tools: ToolInterface[], code: string }`

**Output:** The program's return value, or a `ToolError` on failure.

### CodeMode.make

**Signature:** `Runtime { execute(code: string): Effect<unknown, ToolError> }`

**Input:** `{ tools: ToolInterface[], limits?: Limits }`

**Output:** A reusable runtime object.

## Sequences

### Basic Execution

```
Model --> Host --> CodeMode.execute({ tools, code })
                    |
                    ├── Parse program
                    ├── Set up sandbox with tools
                    ├── Execute program
                    │   ├── Tool call 1 --> handler --> result
                    │   ├── Tool call 2 (parallel) --> handler --> result
                    │   └── Return combined result
                    └── Return structured result or ToolError
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Execution mode | Effect-native, synchronous within sandbox | Matches host's Effect-based tool ecosystem; no async complexity in sandbox |
| Capability model | Explicit opt-in per tool, no ambient authority | Security by default; host decides what to expose |
| Error taxonomy | Parse, runtime, tool refusal, tool failure, timeout, internal defect | Allows agents to recover accurately instead of generic failure handling |

## Risks and Unknowns

1. Binary data (Blob, ArrayBuffer) support is not yet designed.
2. Public/private error split for tool authors (model-visible vs host-diagnostic) needs design.
3. The package is currently private; the public API may change during exploration.
4. Future `fetch` capability would need policy controls (allowed origins, methods, size limits).

## Out of Scope

- Host-level authorization or permission model (host's responsibility).
- Persistent storage or state across executions.
- Network access by default (must be opt-in by host).
