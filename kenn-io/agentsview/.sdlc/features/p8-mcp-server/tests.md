---
title: "MCP Server"
status: done
---

# Test Plan: MCP Server

## Scope

Tests cover MCP server startup with stdio and StreamableHTTP transports, tool definitions for search_sessions, list_sessions, get_session_overview, get_messages, search_content, get_usage_summary, and tool invocation.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | MCP server starts with stdio transport | Server config | Server listening on stdio |
| TC-2 | MCP server starts with StreamableHTTP transport | Server config | HTTP endpoint available |
| TC-3 | Tool definitions are correctly shaped | Tool definitions | Valid MCP tool shapes |
| TC-4 | search_sessions tool | Search query | Ranked session results |
| TC-5 | list_sessions tool | Filter params | Session list |
| TC-6 | get_session_overview tool | Session ID | Session details |
| TC-7 | get_messages tool | Session ID | Message list |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Full MCP tool invocation cycle | Server running | Tools execute and return |

## Test Files

- `internal/mcp/server_test.go` - Server lifecycle tests
- `internal/mcp/shape_test.go` - Tool shape definition tests
- `internal/mcp/tools_test.go` - Tool invocation tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-2 |
| FR-3 | TC-3, TC-4 |
| FR-4 | TC-3, TC-5 |
| FR-5 | TC-3, TC-6 |
| FR-6 | TC-3, TC-7 |
| FR-7 | TC-3, TC-4 |
| FR-8 | TC-3 |
