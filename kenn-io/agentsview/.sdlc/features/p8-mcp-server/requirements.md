---
title: "MCP Server"
status: draft
---

# Requirements: MCP Server

## Overview

The MCP (Model Context Protocol) server exposes agentsview's session data as read-only tools for AI coding assistants. It supports stdio and StreamableHTTP transports, providing tools for searching sessions, listing sessions, viewing session details and messages, content search, and usage summaries.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| AI agent user | Query session data directly from within an AI coding assistant |
| Developer | Integrate agentsview data into MCP-compatible tools |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide an MCP server with stdio transport |
| FR-2 | Must | The system shall provide an MCP server with StreamableHTTP transport |
| FR-3 | Must | The system shall expose a `search_sessions` tool for FTS5 search |
| FR-4 | Must | The system shall expose a `list_sessions` tool for session listing |
| FR-5 | Must | The system shall expose a `get_session_overview` tool for session details |
| FR-6 | Must | The system shall expose a `get_messages` tool for message retrieval |
| FR-7 | Must | The system shall expose a `search_content` tool for content search |
| FR-8 | Must | The system shall expose a `get_usage_summary` tool for usage data |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | MCP server operates on existing auth; no additional credentials required |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** agentsview is running
    - **When** `agentsview mcp` is run
    - **Then** an MCP server starts on stdio, providing the defined tools

## Open Questions

None.
