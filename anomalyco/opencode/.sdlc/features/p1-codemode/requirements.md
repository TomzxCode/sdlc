---
title: "CodeMode"
status: draft
---

# Requirements: CodeMode

## Overview

CodeMode is a confined code execution engine for OpenCode.
It lets a model write a small JavaScript program that can call only the tools supplied by the host.
The program can sequence calls, transform plain data, branch, loop, and run independent calls in parallel without receiving ambient filesystem, process, network, module, or application authority.
This enables safe, deterministic tool orchestration by the model without granting full code execution privileges.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Models can execute multi-step tool sequences efficiently and safely within a confined sandbox |
| Core team | A clean, schema-described execution boundary that does not grant ambient authority |
| Tool authors | Expose tools through CodeMode with minimal friction, with clear sandbox limits and error taxonomy |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a one-shot `execute` API accepting tools and code. |
| FR-2 | Must | The system shall provide a reusable `make` API that creates a runtime with fixed tools and limits, then supports multiple `execute` calls. |
| FR-3 | Must | Programs shall only call tools explicitly supplied by the host; no ambient filesystem, process, network, or module access. |
| FR-4 | Must | Programs shall run synchronously and return structured results to the model. |
| FR-5 | Must | Programs shall support parallel execution of independent calls. |
| FR-6 | Should | The system shall enforce configurable execution limits (timeout, memory, output size). |
| FR-7 | Should | The system shall provide a distinct error taxonomy separating parse errors, runtime errors, tool refusal, tool failures, timeouts, and internal defects. |
| FR-8 | Should | Tool schemas shall be the model-facing interface with minimal, natural arguments. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Programs must have no ambient authority; all capabilities must be explicitly provided by the host. |
| NFR-2 | Must | Reliability | A program crash must not affect the host process or other sessions. |
| NFR-3 | Should | Performance | Multi-step tool sequences should complete without unnecessary round-trips to the LLM. |

## Constraints

- The package is currently private to the workspace (`packages/codemode`).
- Depends on Effect for typed tool results.
- No speculative generic permission model; authorization is per-tool and host-enforced.

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a set of tools and a JavaScript program
    - **When** `CodeMode.execute({ tools, code })` is called
    - **Then** the program runs with only those tools available and returns the result
- [ ] **FR-2**
    - **Given** a reusable runtime created with `CodeMode.make({ tools, limits })`
    - **When** `runtime.execute(code)` is called multiple times
    - **Then** each execution shares the same tool set and limits
- [ ] **FR-3**
    - **Given** a CodeMode program
    - **When** it attempts to access `fs`, `process`, `require`, or `fetch`
    - **Then** the access is denied or unavailable
- [ ] **NFR-1**
    - **Given** a CodeMode program
    - **When** it attempts to read the filesystem or network
    - **Then** it has no ambient access to these capabilities

## Conflicts

None identified yet.

## Open Questions

1. Should CodeMode support async tool calls natively or wrap them synchronously?
2. Should there be a `fetch` capability provided opt-in by the host with policy controls?
3. How should binary data (Blob, ArrayBuffer) be handled across the sandbox boundary?
