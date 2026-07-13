---
title: "ACP Protocol (IDE Integration)"
status: done
---

# Specification: ACP Protocol (IDE Integration)

## Architecture

```
ACP Adapter (acp_adapter/)
    │
    ├── ACP Server (acp_adapter/server.py)
    │   ├── WebSocket endpoint
    │   ├── HTTP endpoint
    │   └── JSON-RPC message handling
    │
    ├── ACP Registry (acp_registry/)
    │   └── Server catalog and discovery
    │
    └── Editor integrations
        ├── VS Code extension protocol
        ├── Zed extension protocol
        └── JetBrains plugin protocol
```

## Data Models

### ACP Message

| Field | Type | Description |
|---|---|---|
| method | string | RPC method name |
| params | dict | Method parameters |
| id | string | Request correlation ID |

### Code Context

| Field | Type | Description |
|---|---|---|
| file_path | string | Current file path |
| cursor_position | object | Line and column |
| project_root | string | Project root directory |
| selection | string | Selected text |

## API Contracts

ACP follows the JSON-RPC 2.0 specification over WebSocket transport. Methods include query submission, file context updates, and tool execution requests.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Protocol | JSON-RPC 2.0 | Standard, language-agnostic, supports both HTTP and WebSocket |
| Transport | WebSocket primary, HTTP fallback | WebSocket enables streaming responses |
| Context sharing | File path + cursor + selection | Lightweight, respects user privacy (no full file upload) |
| Auth | Same credential pool as gateway | Reuses existing auth infrastructure |

## Risks and Unknowns

1. Editor-specific protocol differences may require adapter customization per editor
2. Large project context may exceed token limits when sent as agent context
3. ACP adoption depends on editor ecosystem support

## Out of Scope

- Full file system access from editor
- Multi-editor collaboration session
