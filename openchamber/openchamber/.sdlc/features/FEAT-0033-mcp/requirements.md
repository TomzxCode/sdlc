---
title: "MCP (Model Context Protocol)"
status: done
---

# Requirements: MCP (Model Context Protocol)

## Overview

OpenChamber supports Model Context Protocol (MCP) server configuration, allowing users to connect external tool servers that extend agent capabilities. The settings UI provides configuration for MCP server endpoints, OAuth authentication, and import/export of configurations. A quick-access dropdown shows MCP server status from the header.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Connect custom tool servers to extend agent capabilities |
| Teams | Share MCP configurations across team members |
| Integration builders | Build and test MCP servers against OpenChamber |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a settings page for configuring MCP server connections. |
| FR-02 | Must | The system shall support MCP server lifecycle: add, edit, remove, enable/disable. |
| FR-03 | Must | The system shall display MCP server connection status (connected, error, disabled). |
| FR-04 | Must | The system shall provide a quick-access MCP status dropdown in the header. |
| FR-05 | Should | The system shall support OAuth authentication for MCP servers. |
| FR-06 | Should | The system shall support importing and exporting MCP configurations. |
| FR-07 | May | The system shall support auto-discovery of MCP servers on the local network. |
| FR-08 | Must | The system shall support two MCP server types: local (command-based) and remote (HTTP/SSE). |
| FR-09 | Should | The system shall support importing MCP server configurations from JSON snippets without a built-in catalog. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | MCP server connection failures shall not crash the app or block other features. |

## Constraints

- MCP configuration is stored in OpenCode's config format
- OAuth callbacks require a dedicated route (`McpOAuthCallbackPage.tsx`)
- MCP servers run as separate processes managed by OpenCode


## Acceptance Criteria

- [ ] FR-01: Given the MCP settings page, the user can add a new MCP server with URL and auth config
- [ ] FR-02: Given configured MCP servers, the user can edit or remove them
- [ ] FR-03: Given MCP servers, the status dropdown shows connected/error/disabled for each
- [ ] FR-04: Given configured MCP servers, a quick-access dropdown in the header shows their connection status
- [ ] FR-05: Given an MCP server requiring OAuth, the user can authenticate via the callback flow
- [ ] FR-06: Given MCP configurations, the user can export to JSON and import from JSON
- [ ] FR-07: Given MCP servers on the local network, the system discovers them automatically
- [ ] FR-08: Given a local MCP server, it runs via command on the local machine; given a remote server, it connects via HTTP/SSE
- [ ] FR-09: Given a JSON config snippet, the user can import MCP server configurations without a built-in catalog
- [ ] NFR-01: Given an MCP server connection failure, the app continues running and other features are not blocked

