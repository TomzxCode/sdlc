---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

- The Architecture block names `tools/mcp_serve.py` (line 11) and `mcp_serve.py` (line 19) as the MCP server that serves Hermes tools, and Out of Scope (line 67) refers to it again. No file by that name exists in the checkout. The implementation is `agent/transports/hermes_tools_mcp_server.py` (line 5: `python -m agent.transports.hermes_tools_mcp_server`), `agent/transports/codex_app_server_session.py`, and the `hermes_cli/mcp_*.py` family. The replacement serves a curated tool subset (`EXPOSED_TOOLS`, `hermes_tools_mcp_server.py:57`) over stdio for the codex_app_server runtime.
- The Architecture tree (lines 22-25) lists optional MCP servers as `linear/`, `n8n/`, `unreal-engine/`. `optional-mcps/n8n/` does not exist. `optional-mcps/n8n-official/` is the replacement, with a manifest that records the retired n8n stdio bridge (lines 3-4) and an HTTP + OAuth transport (lines 8-13). The tree also omits the roughly 60 other optional MCP servers shipped in `optional-mcps/`.
- The Data Model (line 38) says `transport` is "stdio or SSE" and Technical Decisions (line 53) says "Transport | stdio + SSE". The code supports a third transport, Streamable HTTP: `tools/mcp_tool.py:2-4`, `tools/mcp_tool_transport.py:575-684` (`_streamable_http_transport`, `_run_http` with latched SSE fallback), and `optional-mcps/n8n-official/manifest.yaml:8-10` (`type: http`).
- The Data Model field `circuit_breaker.threshold` (line 43) and Technical Decisions row "Circuit breaker | Configurable threshold per server" (line 56) claim per-server configurability. The implementation uses fixed module constants `_CIRCUIT_BREAKER_THRESHOLD, _CIRCUIT_BREAKER_COOLDOWN_SEC = 3, 60.0` in `tools/mcp_tool.py:557`, read directly by `tools/mcp_tool_handlers.py:310-319`. No per-server circuit-breaker config field exists.
