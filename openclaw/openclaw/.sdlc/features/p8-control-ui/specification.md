---
title: "Control UI"
status: done
---

# Specification: Control UI

## Overview

The Control UI is a Lit-based web component application served by the gateway's HTTP server. It communicates with the gateway via REST API and WebSocket for real-time updates. Components use legacy decorators for Lit reactive properties.

## Architecture

```
Browser (SPA)
     │
     ├── REST API (config, sessions, status)
     └── WebSocket (streaming chat, real-time updates)
     │
     ▼
Gateway Server
     │
     ├── control-ui.ts (serves the UI)
     ├── server-chat.ts (chat endpoints)
     └── server-methods.ts (admin API)
```

## Data Models

### ControlUIConfig

| Field | Type | Constraints | Description |
|---|---|---|---|
| title | string | nullable | Custom page title |
| theme | string | nullable | light or dark |
| allowedOrigins | string[] | nullable | CORS origins |

## Sequences

### Chat Flow

```
User → Browser: type message, click send
Browser → Gateway: POST /api/chat
Gateway → Agent Runtime: process message
Agent Runtime → Gateway: stream response
Gateway → Browser: WebSocket push response chunks
Browser → User: render incrementally
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Web framework | Lit (web components) | Native browser API, no build-time framework, legacy decorators for compatibility |
| Styling | CSS (no framework) | Minimal dependencies, full control |
| CSP | Strict CSP headers | Security hardening against XSS |
| Real-time | WebSocket push | Low-latency streaming for assistant responses |

## Risks and Unknowns

1. Legacy decorators are tied to TypeScript `experimentalDecorators`; future migration needed
2. CSP hardening may break inline script patterns used by some plugins
3. Mobile browser compatibility needs testing for the chat interface

## Out of Scope

- Standalone desktop electron app (use native macOS/Windows apps instead)
- Full config editor with schema-driven forms
- Plugin-provided UI components
