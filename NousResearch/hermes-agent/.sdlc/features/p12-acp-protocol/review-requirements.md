---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Requirements (ACP Protocol (IDE Integration))

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Constraint "ACP uses a JSON-RPC protocol over WebSocket or HTTP" is contradicted by the implementation.** `acp_adapter/entry.py` builds a `hermes-acp` stdio server (description: "Run Hermes Agent as an ACP stdio server.") and reserves stdout for JSON-RPC. `website/docs/developer-guide/acp-internals.md` states the adapter "wraps Hermes' synchronous `AIAgent` in an async JSON-RPC stdio server." There is no WebSocket or HTTP endpoint anywhere under `acp_adapter/`. The constraint should name JSON-RPC over stdio as the transport.
2. **FR-3 "The ACP registry shall maintain a catalog of available ACP servers" has no implementation.** No `acp_registry/` package exists in the repository. `acp_adapter/catalog.py` is a read-only catalog of historical ACP *sessions* read from SessionDB, and the "registry commands" in `acp_adapter/gateway_commands.py` are gateway chat-command routes. Neither is a catalog of available ACP servers or a discovery service.
3. **FR-2 "code-aware context (current file, cursor position, project structure)" is not implemented.** No structured code-context type exists in the adapter: there are no `cursor_position`, `selection` (as text), `project_root` (as context) or `code_context` fields under `acp_adapter/`. The docs describe only editor cwd binding ("Working directory binding") and state that non-text prompt blocks are ignored for request text extraction. No cursor position or project structure is sent to the agent, so the FR-2 acceptance criterion ("the agent uses the file context to inform its response") is only partially met at best.

Resync `requirements.md` to describe the stdio transport, drop or re-scope FR-3 and FR-2 to what is implemented, then re-review.
