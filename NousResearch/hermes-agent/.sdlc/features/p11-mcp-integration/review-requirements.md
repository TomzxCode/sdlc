---
artifact: requirements.md
verdict: changes-requested
reviewed_at: 2026-11-23
---

## Sync drift: 2026-11-16

- FR-6 (line 29), its acceptance criterion (lines 57-60), and the Overview (line 10) name a root-level `mcp_serve.py` as the entry point for serving Hermes tools as MCP. No `mcp_serve.py` exists anywhere in the checkout. The function now lives in `agent/transports/hermes_tools_mcp_server.py` (run as `python -m agent.transports.hermes_tools_mcp_server`, line 5), `agent/transports/codex_app_server_session.py`, and the `hermes_cli/mcp_*.py` family (`mcp_catalog.py`, `mcp_config.py`, `mcp_picker.py`, `mcp_security.py`, `mcp_startup.py`). The replacement is narrower than FR-6: `hermes_tools_mcp_server.py:53-60` exposes a curated `EXPOSED_TOOLS` subset over stdio for the codex_app_server runtime, registered under `[mcp_servers.hermes-tools]` in `~/.codex/config.toml`.
- FR-8 (line 31) names the installable optional MCP servers as linear, n8n, unreal-engine. `optional-mcps/` has no `n8n/` directory. It ships `n8n-official/` instead, whose manifest (lines 3-4) states the n8n stdio bridge was retired and this is a separate connection, and which uses `transport.type: http` with OAuth (lines 8-13). The directory also holds roughly 60 optional MCP servers, not just the three named.
- FR-3 (line 26) requires "both stdio and SSE transport for MCP connections". The implementation supports a third transport, Streamable HTTP: `tools/mcp_tool.py:2-4` documents "stdio, Streamable HTTP or SSE", `tools/mcp_tool_transport.py:613-684` implements `_run_http` with Streamable HTTP and an SSE fallback, and `optional-mcps/n8n-official/manifest.yaml:8-10` uses `type: http`. The HTTP transport is not reflected in the requirement.

## Sync drift: 2026-11-23

- Constraints (line 45) says "OAuth tokens for MCP servers are stored in the credential pool". MCP OAuth tokens are stored in the active profile's MCP token store at `~/.hermes/mcp-tokens/<server>.json`, or `~/.hermes/profiles/<name>/mcp-tokens/` for a named profile. Evidence: `tools/mcp_oauth.py:407-423` (`HermesTokenStorage` writes the token file), `website/docs/reference/mcp-config-reference.md:350`, and `website/docs/user-guide/features/mcp.md:376`. Credential pools are for model-provider key rotation, not MCP tokens.
