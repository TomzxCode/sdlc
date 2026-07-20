---
title: "MCP Server"
status: done
---

# Specification: MCP Server

## Overview

The MCP server (`internal/mcp/`) implements the Model Context Protocol using the Go MCP SDK. It registers six read-only tools that wrap the existing session service interface. The server supports two transport modes: stdio for direct subprocess invocation and StreamableHTTP for REST-based MCP clients.

## Architecture

```
MCP Client (AI Assistant) ↔ MCP Server (agentsview)
                                 ↓
                          Internal/Service Backend
                                 ↓
                          SQLite / PG / DuckDB
```

## API Contracts

### Tools

| Tool | Description | Parameters |
|---|---|---|
| search_sessions | Full-text search across sessions | query, agent, project, limit |
| list_sessions | List sessions with filters | agent, project, limit, offset |
| get_session_overview | Get session summary | session_id |
| get_messages | Get messages for a session | session_id, limit, offset |
| search_content | Search within message content | query, session_id, mode |
| get_usage_summary | Get usage/cost summary | since, until, agent |

## Sequences

### MCP Tool Invocation
```
Client → JSON-RPC Request → MCP Server → Service Backend → Response
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| SDK | Go MCP SDK (modelcontextprotocol/go-sdk) | Official SDK, spec-compliant |
| Transports | stdio + StreamableHTTP | Covers local AI tool integration and remote clients |
| Architecture | Thin wrapper over service layer | Reuses existing query logic, no data duplication |

## Risks and Unknowns

1. MCP protocol version compatibility as the spec evolves
