---
title: "MCP (Model Context Protocol)"
status: draft
---

# Specification: MCP

## Overview

MCP configuration is managed through the settings UI (`sections/mcp/`) and stored in OpenCode's config. The UI supports adding servers with URL and auth parameters, OAuth flows, and import/export. Status monitoring reads from the OpenCode SDK.

## Architecture

```
MCP Settings (packages/ui/src/components/sections/mcp/)
    +---> McpPage (configuration form)
    +---> McpSidebar (server list navigation)
    +---> mcpImport (import/export logic)
    +---> mcpOAuth (OAuth flow handling)
    +---> McpOAuthCallbackPage (OAuth redirect target)

MCP Status Dropdown (packages/ui/src/components/sections/mcp/McpDropdown.tsx)
    Shows in header services menu

MCP Config Store (packages/ui/src/stores/useMcpConfigStore.ts)
MCP Status Store (packages/ui/src/stores/useMcpStore.ts)
```

## Data Models

### McpServerConfig

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Server identifier |
| name | string | not null | Display name |
| url | string | not null | Server endpoint URL |
| type | enum | not null | stdio, sse, http |
| auth | object | nullable | Auth configuration (OAuth, API key, etc.) |
| enabled | boolean | not null | Whether server is active |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | OpenCode config API | MCP is an OpenCode feature; config lives with it |
| OAuth | Dedicated callback route | Standard OAuth flow; handles redirect from external auth provider |
| Status | Read from SDK | OpenCode manages server lifecycle; UI reflects its state |

## Risks and Unknowns

1. MCP protocol is evolving; backward compatibility may break
2. OAuth providers may have varying callback requirements

## Out of Scope

- MCP server hosting
- MCP server development tools
- Local network auto-discovery
