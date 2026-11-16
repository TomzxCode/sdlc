---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Specification (ACP Protocol (IDE Integration))

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Architecture diagram lists a "WebSocket endpoint" and an "HTTP endpoint" under `acp_adapter/server.py`.** The actual server is an async JSON-RPC stdio server (`acp_adapter/entry.py`, `website/docs/developer-guide/acp-internals.md`); no WebSocket or HTTP endpoint exists in `acp_adapter/`.
2. **Architecture diagram lists "ACP Registry (`acp_registry/`) — Server catalog and discovery".** No `acp_registry/` package exists. `acp_adapter/catalog.py` is a read-only catalog of historical ACP sessions from SessionDB, not a server catalog or discovery service.
3. **API Contracts state "JSON-RPC 2.0 specification over WebSocket transport" and "Methods include query submission, file context updates, and tool execution requests."** The transport is stdio, and the implemented methods are initialize/authenticate, session lifecycle (new/load/resume/fork/list/cancel), prompt execution, model switching and MCP-related controls. There is no standalone "file context update" method.
4. **Technical Decisions "Transport | WebSocket primary, HTTP fallback | WebSocket enables streaming responses" is contradicted.** The decision should record stdio as the sole transport, with streaming delivered as ACP `session_update` notifications over that stdio channel.
5. **Data Model "Code Context" (file_path, cursor_position, project_root, selection) has no corresponding type in code.** No such structured context is defined or consumed under `acp_adapter/`; the adapter binds an editor cwd to each session and otherwise extracts text from ACP content blocks, ignoring non-text blocks.

Resync `specification.md` to reflect the stdio server, remove the non-existent registry package and code-context model, then re-review.
