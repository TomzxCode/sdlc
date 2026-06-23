---
title: "Agent & Tool System"
status: draft
---

# Specification: Agent & Tool System

## Overview

Agents bind a system instruction set, model selection, and permission policy.
Tool calls flow through a Location-scoped registry that validates results, bounds model-visible output, and manages oversized output as temporary files.
Permissions and agent selection are pinned to the provider turn that issued the call.

## Architecture

```
provider turn starts -> select agent + model (sampled)
model returns tool calls ──────────────▶ Tool Registry (Location-scoped)
                                              │ validate structured result
                                              │ tool-specific truncation (optional)
                                              │ generic bounding (max lines/bytes)
                                              ▼
                                  bounded model tool output ─▶ session history
                                  oversized text ────────────▶ managed output file
permission: effective agent of issuing turn retained until settlement
```

## Data Models

### tool_result

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | ulid | PK | Result identity |
| session_id | id | FK | Owning session |
| tool | text | not null | Tool name |
| structured | json | nullable | Validated structured result |
| bounded_text | text | not null | Model-visible bounded output |
| managed_path | text | nullable | Managed output file path |

### permission_request

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | ulid | PK | Request identity |
| session_id | id | FK | Owning session |
| agent | text | not null | Effective agent at issue time |
| status | enum | not null | pending, allowed, denied |

## API Contracts

### POST /project/:projectID/session/:sessionID/permission/:permissionID

Resolves a pending permission request for a session.

| Status | Code | Description |
|---|---|---|
| 200 | OK | Permission resolved, session updated |

## Sequences

### Tool call settlement

```
Model -> tool call -> Registry.validate(structured)
Registry -> optional tool-specific truncation
Registry -> generic bounding (lines or bytes, whichever first)
Registry -> bounded output to history + managed path for overflow
settlement is interruption-safe; raw oversized success never published pre-correction
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Bounding | Provider-independent aggregate limit per settlement | Token pressure belongs to context assembly, not the tool |
| Truncation strategy | Preserve beginning and end by default | Maximizes signal in bounded preview |
| Managed output | Flat shared dir, globally unique names, temporary | Keeps history compact; absolute paths readable by ordinary tools |
| Permission scope | Pinned to issuing provider turn's agent | Agent switches mid-call cannot change policy |

## Risks and Unknowns

1. Provider-executed tool results need provider-aware pruning and are exempt from generic bounding.
2. Managed tool-output files may expire; the bounded output, not the file, is the durable record.

## Out of Scope

- MCP-provided tools (see FEAT-0007 / MCP integration).
- Session lifecycle and compaction (see FEAT-0001).
