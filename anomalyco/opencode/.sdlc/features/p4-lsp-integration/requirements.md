---
title: "LSP Integration"
status: done
---

# Requirements: LSP Integration

## Overview

OpenCode can integrate Language Server Protocol (LSP) servers to feed language diagnostics back into the agent loop as feedback.
A catalog of built-in LSP servers is auto-detected from project files and requirements; servers are launched per worktree, and diagnostics, symbols, and definitions are surfaced to the session.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Language-server diagnostics without extra tooling; configurable per server |
| Agent loop | Structured diagnostics injected as feedback so the agent can fix issues |
| Maintainers | Curated server catalog with auto-install and per-server environment handling |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall maintain a catalog of built-in LSP servers keyed by file extension and launch requirements. |
| FR-02 | Must | The system shall spawn an LSP server process when an enabled file extension is opened in an instance. |
| FR-03 | Must | The system shall support a `lsp` config that enables all servers, disables specific servers, or declares custom servers with command, extensions, env, and initialization options. |
| FR-04 | Must | The system shall be disabled by default and spawn no servers unless enabled. |
| FR-05 | Must | The system shall scope LSP clients to the instance directory and never spawn servers for files outside it. |
| FR-06 | Must | The system shall publish `lsp.updated` events when server state changes. |
| FR-07 | Should | The system shall format diagnostics into a structured feedback block with severity, line, column, and message. |
| FR-08 | Should | The system shall expose workspace symbols and definition lookups to consumers. |
| FR-09 | Should | The system shall support auto-download of servers when requirements are met, unless disabled by environment. |
| FR-10 | Should | The system shall track client status and expose it (e.g. whether clients exist for a file). |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Server startup failures must not crash the agent process. |
| NFR-02 | Should | Performance | Language servers must not be spawned for every file open; reuse running clients. |
| NFR-03 | Should | Security | Environment overrides for server processes must come from configuration, not ambient state. |
| NFR-04 | Should | Usability | Diagnostic reports must cap output per file to avoid flooding the agent context. |

## Constraints

- LSP integration lives in `packages/opencode/src/lsp/` (client, server, launch, language, diagnostic).
- The server catalog is declared as typed `Info` entries (e.g. `Deno`, `Typescript`, `RustAnalyzer`, `JDTLS`).
- Automatic downloads can be disabled via `OPENCODE_DISABLE_LSP_DOWNLOAD=true`.
- LSP is configured through the `lsp` config namespace.

## Acceptance Criteria

- [ ] **FR-02**
    - **Given** an instance with `lsp: true`
    - **When** a file with a supported extension is opened
    - **Then** a client is spawned for the matching server
- [ ] **FR-03**
    - **Given** a config disabling a built-in server
    - **When** a file for that server is opened
    - **Then** the server is not spawned
- [ ] **FR-04**
    - **Given** default configuration
    - **When** a file is opened
    - **Then** no LSP clients exist
- [ ] **FR-05**
    - **Given** a file outside the instance directory
    - **When** it is opened
    - **Then** no built-in LSP server is spawned
- [ ] **FR-06**
    - **Given** a custom LSP server initializing
    - **When** initialization completes
    - **Then** an `lsp.updated` event is published
- [ ] **FR-07**
    - **Given** diagnostics from a server
    - **When** they are reported
    - **Then** a structured `<diagnostics>` block with severity, line, column, and message is produced

## Conflicts

None identified yet.

## Open Questions

1. Should LSP symbol/definition data be surfaced directly to the model, or only through tools and diagnostics?
2. Should the catalog grow to cover more language servers over time, and what governs that expansion?
