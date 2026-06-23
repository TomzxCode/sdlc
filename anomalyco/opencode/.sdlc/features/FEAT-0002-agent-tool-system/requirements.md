---
title: "Agent & Tool System"
status: draft
---

# Requirements: Agent & Tool System

## Overview

The Agent & Tool System defines how OpenCode selects an agent configuration, resolves model and permissions, and executes tool calls returned by the model.
It provides a Location-scoped tool registry of built-in tools, a permission model for local and provider-executed tools, and the skill mechanism for invoking specialized workflows.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Tools that act correctly within the current directory; safe permission prompts |
| Plugin/agent authors | Stable agent definition format and tool extension points |
| Core team | Tool registry invariants; bounded output; permission model integrity |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide built-in agents including a full-access `build` agent and a read-only `plan` agent. |
| FR-02 | Must | The system shall expose built-in tools for filesystem access (`read`, `write`, `edit`, `apply_patch`, `glob`, `grep`), shell execution (`shell`), and web access (`webfetch`, `websearch`). |
| FR-03 | Must | The system shall enforce a tool registry that bounds every tool's model-visible output using a configured maximum lines or bytes. |
| FR-04 | Must | The system shall enforce Location-scoped filesystem authority, allowing absolute paths only within managed tool-output storage. |
| FR-05 | Must | The system shall retain the effective agent of the provider turn that issued a tool call so a later agent switch cannot change that call's policy. |
| FR-06 | Must | The system shall select the agent and model when a provider turn starts and apply later changes only to the next turn. |
| FR-07 | Must | The system shall provide auxiliary tools: `task`, `todo`/`todowrite`, `question`, `plan`, `lsp`, and `skill`. |
| FR-08 | Should | The system shall allow tools to apply tool-specific truncation before the registry enforces the final limit. |
| FR-09 | Should | The system shall expose a permission API for deferring and resolving pending permission requests per session. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Tools shall not read or write outside Location-scoped authority except managed tool-output paths. |
| NFR-02 | Must | Reliability | A successful tool operation shall remain successful even if its managed output file cannot be retained. |
| NFR-03 | Should | Performance | Tool settlement bounding shall be interruption-safe so raw oversized success is never published before a correction. |

## Constraints

- Provider-executed tool results are provider-native transcript facts outside generic registry bounding and need provider-aware pruning.
- Local tool authorization and pending permission requests retain the effective agent of the issuing provider turn.
- Custom agents and tools may be contributed under `.opencode/agent` and `.opencode/tool`.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a fresh install
    - **When** the user lists agents
    - **Then** `build` (full access) and `plan` (read-only, denies edits) are available
- [ ] **FR-03**
    - **Given** a tool returns very large text output
    - **When** the registry settles the result
    - **Then** the model-visible output is bounded to the configured line/byte limit with a managed output path retained
- [ ] **FR-04**
    - **Given** a tool attempts to read an arbitrary absolute path
    - **When** the path is outside Location-scoped authority and not a managed output path
    - **Then** the operation is denied
- [ ] **FR-05**
    - **Given** a tool call is in flight and the user switches agents
    - **When** a permission check runs for that call
    - **Then** the policy of the original agent still applies
- [ ] **NFR-02**
    - **Given** a tool operation succeeded
    - **When** retaining its managed output file fails
    - **Then** the operation remains successful and a lossy bounded output is recorded with diagnostics

## Conflicts

None identified yet.

## Open Questions

1. How should provider-executed tool results be context-controlled given some providers require exact structured round-trip payloads?
