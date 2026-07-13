---
title: "MCP Server Integration"
status: done
---

# Requirements: MCP Server Integration

## Overview

Hermes implements the Model Context Protocol (MCP) as a first-class integration pattern for connecting with external tool servers. MCP servers can be configured in config.yaml, auto-discovered, and their tools are surfaced alongside built-in tools through the MCP client. The system includes an mcp_serve.py entry point for serving MCP tools and optional MCP servers (linear, n8n, unreal-engine) shipped in optional-mcps/.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users | Connect their agent to external tools and data sources via MCP without modifying core Hermes code |
| MCP server developers | Write standard MCP servers that any MCP host can consume |
| Hermes developers | The MCP client is the canonical path for adding structured tool integrations without growing the core toolset |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall connect to configured MCP servers and discover their tools |
| FR-2 | Must | MCP tools shall be surfaced alongside built-in tools in the agent's tool schemas |
| FR-3 | Must | The system shall support both stdio and SSE transport for MCP connections |
| FR-4 | Must | The system shall support OAuth authentication for MCP servers |
| FR-5 | Must | The system shall support dynamic discovery of MCP tools at runtime |
| FR-6 | Must | The system shall support mcp_serve.py for serving Hermes tools as MCP |
| FR-7 | Should | The system shall support circuit breaker patterns for unreliable MCP servers |
| FR-8 | Should | Optional MCP servers (linear, n8n, unreal-engine) shall be available for installation |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | An unresponsive MCP server must not block the agent (timeout + circuit breaker) |
| NFR-2 | Must | Security | MCP server URLs and authentication must be user-configurable in config.yaml |
| NFR-3 | Should | Performance | MCP tool discovery should complete in under 2 seconds |

## Constraints

- MCP servers are configured in config.yaml under a dedicated section
- MCP tools use the same tool schema format as built-in tools
- OAuth tokens for MCP servers are stored in the credential pool

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** an MCP server is configured in config.yaml
    - **When** the agent starts
    - **Then** the MCP server is connected and its tools are discovered
- [ ] **FR-2**
    - **Given** the agent has discovered MCP tools
    - **When** tool schemas are collected for the LLM
    - **Then** MCP tool schemas appear alongside built-in tool schemas
- [ ] **FR-6**
    - **Given** mcp_serve.py is running
    - **When** an external MCP client connects
    - **Then** it can discover and call Hermes tools via MCP
- [ ] **NFR-1**
    - **Given** an MCP server is unresponsive
    - **When** the agent tries to call the MCP tool
    - **Then** the circuit breaker opens and the agent continues without blocking

## Conflicts

None identified yet.

## Open Questions

1. Should MCP servers be configurable per-profile?
