---
title: "Plugin SDK and Extension System"
status: done
---

# Specification: Plugin SDK and Extension System

## Overview

The plugin system uses a facade pattern: plugins import only from `@openclaw/plugin-sdk` barrels (e.g., `api.ts`, `runtime-api.ts`). Import boundary scripts (`check-*-extension-import-boundary.mjs`) enforce this at build time. The plugin registry manages installed plugins, their manifests, and lifecycle state.

## Architecture

```
Plugin Package (npm)
     │
     ▼
@openclaw/plugin-sdk (facade)
     │
     ├── api.ts               → public API types
     ├── runtime-api.ts       → runtime hooks
     ├── channel-contract.ts  → channel interface
     └── plugin-types.ts      → manifest and config types
     │
     ▼
Plugin Registry → Lifecycle Manager → Gateway Runtime
     │
     ▼
ClawHub Marketplace (discovery)
```

## Data Models

### PluginManifest

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Unique plugin identifier |
| name | string | not null | Human-readable name |
| version | string | not null | Semver version |
| type | string | not null | channel, provider, tool, etc. |
| entry | string | not null | Main entry point |
| configSchema | JSON | nullable | Zod schema for plugin config |

## Sequences

### Plugin Installation

```
User → CLI: openclaw plugins install <package>
CLI → npm: resolve and download package
CLI → Plugin Registry: register plugin
CLI → Config: add plugin entry to openclaw.json
Gateway → Plugin Registry: activate on next start
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Import boundary | Output-checked facade pattern | Enforced at build time, no runtime overhead |
| Plugin distribution | npm packages | Existing ecosystem, familiar tooling |
| Lifecycle management | Registry with state SQLite | Durable across restarts |
| Marketplace | ClawHub (separate service) | Decoupled from core, community-owned |

## Risks and Unknowns

1. Breaking changes in the SDK public API affect all community plugins
2. Untrusted plugins could introduce security vulnerabilities
3. npm dependency conflicts across plugins may be hard to resolve

## Out of Scope

- Plugin sandbox/containerization (e.g., separate process)
- Paid plugin marketplace
- Plugin dependency resolution across multiple plugins
