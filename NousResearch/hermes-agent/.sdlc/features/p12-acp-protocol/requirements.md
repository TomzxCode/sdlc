---
title: "ACP Protocol (IDE Integration)"
status: done
---

# Requirements: ACP Protocol (IDE Integration)

## Overview

Hermes implements the Agent Communication Protocol (ACP) for IDE integration with VS Code, Zed, and JetBrains editors. The ACP adapter (acp_adapter/) and ACP registry (acp_registry/) allow developers to interact with the agent directly from their editor, enabling code-aware conversations, file editing, and terminal commands within the IDE context.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Interact with the agent from their code editor for code-aware assistance |
| IDE integrators | Use the ACP protocol to build Hermes integrations for any editor |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The ACP adapter shall provide an API endpoint for editors to connect to the agent |
| FR-2 | Must | The ACP adapter shall support code-aware context (current file, cursor position, project structure) |
| FR-3 | Must | The ACP registry shall maintain a catalog of available ACP servers |
| FR-4 | Should | The adapter shall support file editing operations initiated from the IDE |
| FR-5 | Should | The adapter shall support terminal command execution from the IDE |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | ACP connections shall be authenticated and scoped to the user's session |
| NFR-2 | Should | Performance | ACP responses should be delivered with sub-second latency for simple queries |

## Constraints

- ACP uses a JSON-RPC protocol over WebSocket or HTTP
- Compatible with VS Code, Zed, and JetBrains editor protocols

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the ACP adapter is running
    - **When** an editor connects via the ACP endpoint
    - **Then** the editor can send queries and receive responses
- [ ] **FR-2**
    - **Given** the ACP adapter receives a query
    - **When** the query includes file context
    - **Then** the agent uses the file context to inform its response

## Conflicts

None identified yet.

## Open Questions

1. Should ACP support multiple simultaneous editor connections?
