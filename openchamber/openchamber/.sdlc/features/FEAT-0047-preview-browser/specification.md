---
title: "Preview & Embedded Browser"
status: draft
---

# Specification: Preview & Embedded Browser

## Overview

The preview system uses a server-side proxy middleware (`packages/web/server/lib/preview/`) to relay requests from an embedded iframe to the target dev server. The Electron desktop adds a full browser tab with webview capabilities.

## Architecture

```
Preview Iframe (context panel tab)
    |
    v  HTTP/WS requests
Server Proxy (packages/web/server/lib/preview/proxy-runtime.js)
    |
    v  http-proxy-middleware
Target Dev Server (localhost:<dev-port>)
    |
    +---> URL rewriting for same-origin paths
    +---> WebSocket upgrade proxying

Console Overlay (client-side)
    captures iframe window.console via postMessage bridge

Electron Browser Tab (desktop only)
    |
    v  Electron webview
Direct browser with inspect and annotation
```

## Data Models

### PreviewState

| Field | Type | Constraints | Description |
|---|---|---|---|
| url | string | not null | Current preview URL |
| title | string | nullable | Page title |
| loading | boolean | not null | Whether loading |
| consoleEntries | ConsoleEntry[] | not null | Captured console output |

### ConsoleEntry

| Field | Type | Constraints | Description |
|---|---|---|---|
| level | enum | not null | log, warn, error, info |
| message | string | not null | Log content |
| timestamp | number | not null | Capture time |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Proxy | http-proxy-middleware | Battle-tested proxy; handles WebSocket upgrades and header rewriting |
| Iframe | Sandboxed with proxy | Isolates preview from app context; prevents security leaks |
| Console capture | postMessage bridge | Works within iframe sandbox restrictions |

## Risks and Unknowns

1. Some SPAs with heavy client-side routing may break proxy URL rewriting
2. Electron webview API differences across platforms

## Out of Scope

- Performance profiling of previewed apps
- Network request interception (beyond proxy logging)
- Mobile device emulation
