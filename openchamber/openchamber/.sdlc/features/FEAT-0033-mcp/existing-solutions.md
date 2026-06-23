---
issue: ""
title: "MCP (Model Context Protocol)"
status: draft
---

# Existing Solutions: MCP (Model Context Protocol)

## Overview

MCP support is already substantially implemented across the OpenChamber codebase. Server-side CRUD routes exist at `/api/config/mcp*` in `config-entity-routes.js`. A Zustand store (`useMcpStore`) manages connection status, connect/disconnect/startAuth/completeAuth/clearAuth operations, per-directory status, and diagnostics. Complete MCP settings pages exist (`McpPage.tsx`, `McpSidebar.tsx`) with OAuth callback support (`McpOAuthCallbackPage.tsx`), JSON import/export, and a header dropdown (`McpDropdown.tsx`). The MCP protocol itself is an open Anthropic-led standard with TypeScript/Python SDKs at 86K+ GitHub stars. Requirements FR-01 through FR-06 and FR-08/FR-09 are covered. FR-07 (auto-discovery on local network) is the main gap. The recommended direction is to build on the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/opencode/config-entity-routes.js` (MCP CRUD routes), `packages/ui/src/stores/useMcpStore.ts`, `packages/ui/src/components/sections/mcp/` (McpPage, McpSidebar, mcpOAuth, mcpImport, McpOAuthCallbackPage), `packages/ui/src/components/mcp/McpDropdown.tsx`, `packages/ui/src/lib/settings/metadata.ts` (MCP settings section), `packages/vscode/src/bridge-config-runtime.ts` and `packages/vscode/src/opencodeConfig.ts` (VS Code MCP CRUD) |
| Open-source | Yes | MCP specification, MCP SDKs (TypeScript, Python), reference servers |
| Commercial / SaaS | Yes | MCP Registry (Anthropic), Google MCP servers, various SaaS MCP integrations |
| Standards / protocols | Yes | Model Context Protocol (MCP) specification (2025-06-18, with 2026-07-28 RC) |
| Reference material | Yes | modelcontextprotocol.io, GitHub `modelcontextprotocol/servers` (86K stars), `modelcontextprotocol/registry` |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber's existing MCP implementation | Internal | MIT | Production (v1.11.7) | FR-01 through FR-06, FR-08, FR-09 | FR-07 (auto-discovery) |
| MCP TypeScript SDK (@modelcontextprotocol/sdk) | Library | MIT | Mature (v1.x, official) | MCP client/server implementation, transports, protocol handling | SDK for building servers/clients, not config UI |
| MCP Python SDK | Library | MIT | Mature (v1.x, official) | Same as TS SDK, Python | Not applicable (TypeScript codebase) |
| MCP Registry | Service | Apache 2.0 | Preview | Server discovery/catalog | Not a UI component, API-based |

## Evaluation

### OpenChamber's existing MCP implementation

- **Strengths:** Full CRUD lifecycle (add/edit/remove/enable/disable). Connect, disconnect, test connection, OAuth auth flow (startAuth, completeAuth, clearAuth). Per-directory status tracking. JSON import/export for config snippets. Status dropdown in header with connected/error/disabled/needsAuth states. OAuth callback page with code exchange. Supports both local (command-based) and remote (HTTP/SSE) server types. Uses `@opencode-ai/sdk` for the actual MCP client communication.
- **Weaknesses:** FR-07 (auto-discovery on local network) not implemented. No multicast DNS or mDNS-based discovery. The OAuth flow works but needs careful testing across different MCP server implementations.
- **Integration effort:** Low for existing features, medium for FR-07 (auto-discovery).
- **Cost:** None.
- **Risks:** MCP specification is evolving rapidly — the 2026-07-28 release candidate introduces stateless HTTP, removes the initialize handshake, adds extensions framework. The implementation must track spec changes.

### MCP TypeScript SDK

- **Strengths:** Official Anthropic-maintained SDK. Full protocol implementation. Multiple transport support (stdio, SSE, Streamable HTTP). Used under the hood by `@opencode-ai/sdk`.
- **Weaknesses:** Already used indirectly via `@opencode-ai/sdk`. Does not provide UI configuration components. Not relevant for the config/settings UI layer.
- **Integration effort:** Already integrated (upstream dependency).
- **Cost:** Free (MIT).
- **Risks:** Breaking spec changes in 2026-07-28 RC (stateless transport, removed initialize handshake, OAuth hardening) will require SDK updates.

### MCP Registry

- **Strengths:** Community registry for discovering MCP servers. API-based with GitHub OAuth auth for publishing. Could inform FR-07 (auto-discovery).
- **Weaknesses:** Not a UI component. API-focused on publishing and listing servers. Auto-discovery on the local network (mDNS/SSDP) is different from registry-based discovery.
- **Integration effort:** N/A — useful as reference for discovery patterns.
- **Cost:** Free.
- **Risks:** Still in preview (API freeze at v0.1), may have breaking changes before GA.

## Recommendation

**Direction:** Adopt and extend

The existing MCP implementation already covers FR-01 through FR-06, FR-08, and FR-09. The main new work is FR-07 (auto-discovery on local network), which is a well-understood problem with existing solutions (mDNS via `multicast-dns` npm package, SSDP, or Zeroconf/Bonjour). The MCP specification does not standardize discovery — it is a client-side concern. For auto-discovery, use a lightweight mDNS library (e.g., `multicast-dns` on npm) to probe for MCP servers on the local network, or listen for DNS-SD advertisements. Track the 2026-07-28 MCP spec changes (stateless HTTP transport, deprecation of roots/sampling/logging) to ensure the OAuth and transport configuration remains compatible.

## Sources of Information

- MCP Specification (`modelcontextprotocol.io/specification/2025-06-18`): Defines transport types (stdio, SSE, Streamable HTTP), capability negotiation, OAuth, and tool/resource/prompt primitives.
- MCP 2026-07-28 Release Candidate (`blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate`): Stateless HTTP transport, removed initialize handshake, extensions framework, OAuth hardening (iss validation, application_type), deprecation of roots/sampling/logging.
- GitHub `modelcontextprotocol/servers` (86K stars): Reference implementations showing server configuration patterns (command + args + env).
- GitHub `modelcontextprotocol/registry`: Registry API for server discovery — useful reference for structured discovery but not local network auto-discovery.
- Google MCP servers (`github.com/google/mcp`): Official Google MCP servers, Streamable HTTP on Cloud Run pattern.
- npm `multicast-dns` package: Standard approach for local network service discovery (used by home automation tools, Chromecast, etc.).

## Open Questions

1. FR-07 (auto-discovery): Should this use mDNS (DNS-SD / Bonjour), SSDP, or a custom UDP broadcast? mDNS is the most widely supported for local network service discovery. What MCP-specific metadata should be advertised (server name, transport type, port)?
2. How should the 2026-07-28 MCP spec changes be handled — support both 2025-11-25 and 2026-07-28 versions, or migrate to 2026-07-28 only? The SDK (`@opencode-ai/sdk`) will likely handle protocol version negotiation, but the config UI may need to expose new fields (stateless mode, cache TTL, endpoint paths).
