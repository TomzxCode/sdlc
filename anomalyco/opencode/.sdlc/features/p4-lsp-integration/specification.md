---
title: "LSP Integration"
status: done
---

# Specification: LSP Integration

## Overview

The LSP integration (`packages/opencode/src/lsp/`) maintains a catalog of typed `Info` entries describing built-in language servers (`server.ts`), a JSON-RPC client implementation (`client.ts`), a launcher that spawns server processes with piped stdio (`launch.ts`), a language-extension mapping (`language.ts`), and a diagnostic formatter (`diagnostic.ts`). The top-level `lsp.ts` service orchestrates per-instance clients via `InstanceState`, watching file opens through the config and instance context, and publishing `lsp.updated` events on state changes.

## Architecture

```
                Config (lsp: true | object | unset)
                        │
                        ▼
   ┌───────────────────────────────────────────────────────────┐
   │  LSP service (lsp.ts, per-instance via InstanceState)      │
   │  ┌─────────────┐   ┌─────────────┐   ┌──────────────────┐  │
   │  │  client.ts  │──▶│  launch.ts  │──▶│  server catalog   │  │
   │  │  (JSON-RPC) │   │  (spawn)    │   │  (server.ts Info) │  │
   │  └──────┬──────┘   └─────────────┘   └──────────────────┘  │
   │         │ diagnostics / symbols / definitions              │
   │         ▼                                                  │
   │  diagnostic.ts → <diagnostics file=…> block                │
   │         ▼                                                  │
   │  EventV2Bridge → lsp.updated events                        │
   └───────────────────────────────────────────────────────────┘
```

## Data Models

### LSP Info (server catalog entry)

| Field | Type | Description |
|---|---|---|
| name | string | Server name |
| command | string | Executable to launch |
| extensions | string[] | File extensions this server handles |
| autoInstall | boolean | Whether the server auto-downloads when requirements are met |
| requirements | array | Files/dependencies that must exist in the project |

### Range / Position

| Field | Type | Description |
|---|---|---|
| start.line / start.character | number | Zero-based start position |
| end.line / end.character | number | Zero-based end position |

### Symbol

| Field | Type | Description |
|---|---|---|
| name | string | Symbol name |
| kind | number | LSP symbol kind |
| location.uri / location.range | string / Range | Symbol location |

## API Contracts

LSP is internal (not an HTTP endpoint). The primary interface is the `LSP` Effect service with:

- `init()` — start per-instance clients.
- `status(file)` — current server/client status.
- `diagnostics(file)` — diagnostics for a file.
- `workspaceSymbol(query)` — symbol search.
- `definition(file, position)` — definition lookup.
- `hasClients(file)` — whether an LSP client exists for a file.

## Sequences

### Server launch on file open

```
File opened (supported extension, in instance)
   └─ config lsp enabled? ── no → no clients
   └─ server catalog match (extension + requirements) ── no → skip
   └─ spawn(cmd, args, {env}) via launch.ts
   └─ client initializes (initialize → initialized)
   └─ publish lsp.updated event
   └─ server sends diagnostics → formatted via diagnostic.ts
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Per-instance scoping | `InstanceState` | Clients are scoped to a worktree and cleaned up on disposal |
| Process launch | Piped stdio spawn | Standard LSP transport over stdin/stdout |
| Catalog | Typed `Info` entries in `server.ts` | Declarative, extendable, self-documenting |
| Disabled by default | `lsp` unset spawns nothing | Avoids memory/CPU cost unless the user opts in |
| Feedback format | `<diagnostics file=…>` block | Structured input the agent loop can consume |
| Events | `lsp.updated` via EventV2Bridge | Observable server lifecycle for UI and session |

## Risks and Unknowns

1. Language servers can get out of sync with the project, use significant memory, or slow down workflows.
2. Auto-installed binaries depend on the host platform and network availability.
3. `OPENCODE_DISABLE_LSP_DOWNLOAD` is the only escape hatch for auto-download; behavior on download failure must degrade gracefully.

## Out of Scope

- A full LSP client supporting every server feature (code actions, refactoring, inlay hints).
- Language-server installation for every ecosystem.
- Surfacing symbols/definitions directly to the model (currently only through the service API and diagnostics).
