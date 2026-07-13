---
title: "MCP Server Integration"
status: done
---

# Specification: MCP Server Integration

## Architecture

```
MCP Tools (tools/mcp_tool.py, tools/mcp_serve.py)
    │
    ├── MCP Client (tools/mcp_client/ or tools/*mcp*.py)
    │   ├── stdio transport
    │   ├── SSE transport
    │   ├── OAuth authentication
    │   └── Circuit breaker
    │
    ├── MCP Server (mcp_serve.py)
    │   └── Serves Hermes tools as MCP tools
    │
    ├── Optional MCP Servers (optional-mcps/)
    │   ├── linear/ — Linear issue tracking
    │   ├── n8n/ — n8n workflow automation
    │   └── unreal-engine/ — Unreal Engine integration
    │
    └── MCP Config (config.yaml → tools/mcp_config/hermes_cli)
        └── Server definitions with URL, auth, transport type
```

## Data Models

### MCP Server Configuration

| Field | Type | Description |
|---|---|---|
| name | string | Server identifier |
| transport | string | stdio or SSE |
| url | string | Server URL (for SSE) |
| command | string | Shell command (for stdio) |
| auth.type | string | OAuth or none |
| timeout | int | Connection timeout |
| circuit_breaker.threshold | int | Failure count before opening |

## API Contracts

MCP follows the Model Context Protocol specification. Tools are defined using JSON Schema and called via JSON-RPC messages over the configured transport.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport | stdio + SSE | Covers local servers and remote servers equally |
| Auth | OAuth via credential pool | Reuses existing credential management infrastructure |
| Discovery | Connect at startup + dynamic refresh | Tools available from session start; dynamic refresh handles late-joining servers |
| Circuit breaker | Configurable threshold per server | Prevents a single failing MCP server from degrading the agent |
| Tool surface | Same schema format as built-in tools | LLM doesn't distinguish between MCP and built-in tools |

## Risks and Unknowns

1. MCP server reliability depends on the external server — circuit breaker mitigates but does not eliminate this
2. OAuth token refresh for long-lived sessions may require re-authentication
3. MCP tool schemas are fixed at connection time — dynamic tool addition mid-session may not be reflected

## Out of Scope

- Hosting MCP servers (except mcp_serve.py which serves Hermes tools)
- MCP registry or marketplace
