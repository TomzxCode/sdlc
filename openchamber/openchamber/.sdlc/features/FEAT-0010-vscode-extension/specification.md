---
title: "VS Code Extension"
status: draft
---

# Specification: VS Code Extension

## Overview

The VS Code extension splits into two parts: an extension host (`packages/vscode/src/extension.ts`) that manages the OpenCode server lifecycle and VS Code integration, and a webview (`packages/vscode/webview/main.tsx`) that renders the shared UI from `@openchamber/ui`. Communication between host and webview uses VS Code's `postMessage` API.

## Architecture

```
VS Code Extension Host (packages/vscode/src/extension.ts)
    |
    +---> OpenCode server lifecycle management
    +---> VS Code context menu and command registration
    +---> Settings management
    |
    v  postMessage bridge
Webview (packages/vscode/webview/main.tsx)
    |
    +---> @openchamber/ui (shared React components)
    +---> Theme mapping from VS Code to OpenChamber tokens
```

## Data Models

### ExtensionSettings

| Field | Type | Constraints | Description |
|---|---|---|---|
| apiUrl | string | nullable | External API URL (empty = auto-start local) |
| opencodeBinary | string | nullable | Custom OpenCode binary path |

## API Contracts

### VS Code Commands

| Command | Description |
|---|---|
| `openchamber.openSidebar` | Open the sidebar chat panel |
| `openchamber.focusChat` | Focus the chat input |
| `openchamber.explain` | Send selected code with "explain" prompt |
| `openchamber.improveCode` | Send selected code with "improve" prompt |
| `openchamber.addToContext` | Add selected code to current chat context |
| `openchamber.openAgentManager` | Open the Agent Manager panel |

### Webview <-> Host Messages

| Direction | Type | Payload |
|---|---|---|
| Host -> Webview | `settings` | Extension settings |
| Host -> Webview | `theme` | VS Code theme colors |
| Host -> Webview | `selection` | Currently selected code |
| Webview -> Host | `openFile` | File path + line number |
| Webview -> Host | `ready` | Webview initialization complete |

## Sequences

### Right-click "Explain" action

```
User selects code -> Right-click -> "OpenChamber: Explain"
    |
    v
Extension host captures selection text and file context
    |
    v  postMessage to webview
Webview creates a new prompt with the selection + "explain this code"
    |
    v
Chat processes the prompt normally
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Build tool | esbuild for extension, Vite for webview | esbuild for fast Node.js bundling; Vite for HMR during development |
| UI reuse | @openchamber/ui as workspace dependency | Maintains feature parity across all runtimes |
| Theme mapping | VS Code theme colors -> OpenChamber tokens | Seamless visual integration with the editor |

## Risks and Unknowns

1. VS Code webview API restrictions may limit some shared UI features
2. Extension review process on Marketplace may delay releases

## Out of Scope

- Inline code completions (Copilot-style)
- Language server features
- Debug integration
