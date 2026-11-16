---
artifact: tests.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

- Scope (line 10) lists "mcp_serve.py" among the areas covered. No `mcp_serve.py` exists in the checkout; MCP serving now lives in `agent/transports/hermes_tools_mcp_server.py`, `agent/transports/codex_app_server_session.py`, and the `hermes_cli/mcp_*.py` family. All test files named in the Test Files section were verified to exist; the drift is the stale module name in Scope.
- Scope (line 10) describes transport coverage as "stdio/SSE" only. The code also implements Streamable HTTP (`tools/mcp_tool.py:2-4`, `tools/mcp_tool_transport.py:575-684`), and HTTP-specific tests exist (`tests/tools/test_mcp_streamable_http_arity.py`, `tests/tools/test_mcp_http_body_cap.py`, `tests/tools/test_mcp_http_proxy.py`) but are not listed in the Test Files section.
