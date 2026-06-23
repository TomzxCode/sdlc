---
title: "Plugin System"
status: draft
---

# Specification: Plugin System

## Overview

Plugins are TypeScript packages depending on `@opencode-ai/plugin`.
A loader discovers and installs them, a direct runtime registry registers their namespaced hooks, and the runtime awaits readiness before serving sessions.
Plugins extend providers, PTY environment, tools, context sources, and TUI behavior.

## Architecture

```
@opencode-ai/plugin SDK ──▶ plugin package
plugin package ──load/install──▶ loader.ts
loader ──▶ runtime registry (direct)
runtime registry ──await readiness──▶ server ready
hooks ──▶ providers · pty-environment · tools · context sources · tui
```

## Data Models

### plugin_meta

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | text | PK | Plugin package name |
| namespace | text | not null | Hook namespace |
| ready | boolean | not null | Readiness state |

## API Contracts

Plugins integrate via the SDK, not a public HTTP contract.

## Sequences

### Plugin load and readiness

```
server start -> loader.discover -> registry.register(namespaced hooks)
registry -> await readiness
registry ready -> server serves sessions
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Registry | Direct runtime registry | Avoids indirection; fast lookups |
| Hooks | Namespaced API | Prevents collisions across plugins |
| Readiness | Awaited before serving | Guarantees plugins are initialized |
| Context sources | Same scoped registry seam as built-ins | Uniform composition; future hot-reload |

## Risks and Unknowns

1. Hot-reload of plugin-defined Context Sources is not yet implemented.
2. Legacy baseline mutation (`experimental.chat.system.transform`) has no plugin equivalent yet.

## Out of Scope

- Built-in context source producers (see FEAT-0001).
- Provider catalog data (see FEAT-0003).
