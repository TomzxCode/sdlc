---
title: "Plugins (OpenCode Plugin Management)"
status: draft
---

# Specification: Plugins

## Overview

Plugins are managed through the OpenCode plugin system. The server provides routes for listing, adding, removing, and configuring plugins via the OpenCode SDK plugin API. Plugins can be npm packages (`npm:package-name`) or local files (`path:/path/to/plugin.js`), stored as entries in the OpenCode config or as files in the plugin directory.

## Architecture

```
User manages plugins in PluginsPage/PluginsSidebar
    |
    v  HTTP request
Express Server → opencode/plugins.js + opencode/plugin-routes.js
    |
    v  OpenCode config API
OpenCode plugin system (plugin entries and files)
```

## Data Models

### PluginEntry

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, base64url encoded | Unique plugin identifier |
| spec | string | not null | npm spec or file path |
| options | Record<string, unknown> | optional | Plugin configuration |
| scope | string | `user` or `project` | Installation scope |
| kind | string | `config` | Plugin source type |
| parsedKind | string | `npm` or `path` | Resolved plugin type |

### PluginFile

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, base64url encoded | Unique file identifier |
| fileName | string | not null, pattern: `^[a-z0-9][a-z0-9-_.]*\.(js|ts|mjs|cjs)$` | Plugin file name |
| scope | string | `user` or `project` | File scope |

## API Contracts

Plugin operations are exposed through OpenCode config routes (`/api/openchamber/plugin/*`) and managed via `packages/web/server/lib/opencode/plugins.js`.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Plugin sources | npm packages + local files | Covers both community plugins and custom development |
| Plugin spec format | `npm:package` and `path:/path` | Clear distinction between install sources |
| Refresh pattern | Server-side agent refresh | Avoids requiring full OpenCode restart for plugin changes |

## Out of Scope

- Plugin marketplace/catalog (beyond the registry badge displaying install counts)
- Plugin development tooling (scaffolding, testing)
