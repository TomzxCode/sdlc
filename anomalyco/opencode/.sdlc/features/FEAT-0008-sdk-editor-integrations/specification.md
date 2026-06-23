---
title: "SDK & Editor Integrations"
status: draft
---

# Specification: SDK & Editor Integrations

## Overview

A TypeScript SDK is generated from the Hono server routes, an MCP layer composes external tool/context servers (with OAuth), and a VSCode extension plus a distributable CLI bring OpenCode into editors and automation.

## Architecture

```
Hono server routes ──generate──▶ TypeScript SDK (packages/sdk/js) ──▶ clients
packages/opencode/src/mcp ──▶ MCP catalog · auth · oauth provider/callback ──▶ MCP servers
sdks/vscode ──▶ VSCode extension ──▶ local server
packages/cli / build.ts --single ──▶ standalone `opencode` executable
packages/slack ──▶ Slack integration
```

## Data Models

### mcp_server

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | MCP server identity |
| auth | json | nullable | Auth/OAuth state |
| status | enum | not null | connected, pending, error |

## API Contracts

These integrations consume the HTTP API (see FEAT-0006) and expose editor/MCP-specific contracts.

## Sequences

### MCP OAuth connect

```
session requests MCP server -> catalog lookup
auth needed -> oauth-provider initiates flow
oauth-callback completes -> credentials stored
MCP server usable by tool registry
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| SDK | Generated from server routes | Type safety in lockstep with API |
| Standalone build | `build.ts --single` | Single-asset executable per platform |
| MCP auth | OAuth provider + callback | Supports providers requiring user consent |

## Risks and Unknowns

1. SDK and extension versioning cadence relative to the server is not specified here.
2. MCP OAuth reliability depends on provider-specific flows.

## Out of Scope

- Server route definitions (see FEAT-0006).
- Plugin-provided tools and providers (see FEAT-0007).
