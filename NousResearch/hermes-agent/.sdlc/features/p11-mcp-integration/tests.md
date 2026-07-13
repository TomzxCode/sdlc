---
title: "MCP Server Integration"
status: done
---

# Test Plan: MCP Server Integration

## Scope

Tests covering MCP client connection, tool discovery, tool calling, transport (stdio/SSE), OAuth authentication, circuit breaker, mcp_serve.py, and optional MCP server functionality.

## Test Files

- tests/tools/test_mcp_tool.py — Core MCP tool calling
- tests/tools/test_mcp_tool_401_handling.py — MCP auth error handling
- tests/tools/test_mcp_tool_session_expired.py — Session expiry handling
- tests/tools/test_mcp_cancelled_error_propagation.py — Cancellation propagation
- tests/tools/test_mcp_capability_gating.py — Capability gating
- tests/tools/test_mcp_circuit_breaker.py — Circuit breaker pattern
- tests/tools/test_mcp_client_cert.py — Client certificate auth
- tests/tools/test_mcp_dynamic_discovery.py — Dynamic tool discovery
- tests/tools/test_mcp_elicitation.py — MCP tool elicitation
- tests/tools/test_mcp_oauth_*.py — OAuth flow tests (4+ files)
- tests/tools/test_mcp_probe.py — Server probing
- tests/tools/test_mcp_sse_transport.py — SSE transport
- tests/tools/test_mcp_stdio_init_timeout.py — Stdio init timeout
- tests/tools/test_mcp_stability.py — Stability under load
- tests/tools/test_mcp_parked_self_probe.py — Self-probe behavior
- tests/tools/test_mcp_utility_capability_gating.py — Utility gating
- tests/hermes_cli/test_mcp_*.py — MCP CLI commands (5+ files)

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (connect to MCP servers) | test_mcp_tool.py, test_mcp_probe.py |
| FR-2 (surface MCP tools) | test_mcp_tool.py |
| FR-3 (stdio + SSE transport) | test_mcp_sse_transport.py, test_mcp_stdio_init_timeout.py |
| FR-4 (OAuth auth) | test_mcp_oauth_*.py |
| FR-5 (dynamic discovery) | test_mcp_dynamic_discovery.py |
| NFR-1 (circuit breaker) | test_mcp_circuit_breaker.py |
