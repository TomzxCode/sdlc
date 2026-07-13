---
title: "Agent Client Protocol (ACP)"
status: done
---

# Requirements: Agent Client Protocol (ACP)

## Overview

The Agent Client Protocol (ACP) implementation provides interoperable agent-to-agent communication within OpenCode.
It defines agent, session, tool, event, permission, content, directory, usage, profile, and config operations as a structured protocol, enabling external agents and tools to interact with OpenCode sessions programmatically.
ACP is independent from MCP and addresses a different use case: driving an OpenCode agent from another agent or automation tool.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Automation users | Drive OpenCode agents from external scripts and CI pipelines |
| Agent developers | Interoperable protocol for cross-agent communication |
| Core team | Clean separation from MCP; protocol evolves independently |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall define ACP operations for agent lifecycle: create, list, describe, delete. |
| FR-02 | Must | The system shall define ACP operations for session lifecycle: start, send message, list, get, abort. |
| FR-03 | Must | The system shall define ACP operations for tool discovery and invocation. |
| FR-04 | Must | The system shall define ACP operations for event streaming from active sessions. |
| FR-05 | Must | The system shall define ACP permission resolution operations. |
| FR-06 | Must | The system shall define ACP content and directory operations for file access. |
| FR-07 | Should | The system shall profile agent usage and expose telemetry via ACP. |
| FR-08 | Should | The system shall expose agent configuration via ACP operations. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | ACP shall be implemented as a distinct protocol surface, separate from MCP. |
| NFR-02 | Should | Usability | ACP operations shall follow consistent naming and response patterns. |

## Constraints

- ACP implementation lives in `packages/opencode/src/acp/`.
- ACP is a separate protocol from MCP (`packages/opencode/src/mcp/`).

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** an ACP client
    - **When** it lists agents
    - **Then** available agents are returned with their capabilities
- [ ] **FR-02**
    - **Given** an ACP client
    - **When** it starts a session and sends a message
    - **Then** a response is streamed back with message content
- [ ] **FR-07**
    - **Given** an ACP session
    - **When** usage data is requested
    - **Then** token counts and provider usage are returned

## Conflicts

None identified yet.

## Open Questions

1. Should ACP be published as a standalone protocol spec, or remain an internal OpenCode implementation?
2. How does ACP interact with the permission system when driven by an external agent?
