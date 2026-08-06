---
title: "Plugins & Extension Ecosystem"
status: done
---

# Specification: Plugins & Extension Ecosystem

## Overview

The plugin SDK (`packages/plugin-sdk/`) defines the authoring contract; core plugin management stores manifests and lifecycle; the engine plugin runner executes plugins with skill-body delivery; and first-party pi extensions route commands into Claude CLI, Droid CLI, and Llama.cpp. Dashboard surfaces include PluginManager and PiExtensionsManager.

## Architecture

```
Dashboard (PluginManager, PiExtensionsManager) + CLI (plugin)
      │  register-plugin-routes, register-plugins-automation-routes
      ▼
@fusion/core/plugins (manifest, lifecycle, storage)
      │
      ▼
@fusion/engine (plugin-runner, plugin-skill-integration, in-process-runtime
                plugin MCP discovery isolation)
      │
      ▼
pi extensions (pi-claude-cli, droid-cli, pi-llama-cpp) ──► coding-agent CLIs
```

## API Contracts

### GET /api/plugins

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| plugins | array | Installed plugins with manifest/config |

### POST /api/plugins/:id/enable

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| id | string | yes | Plugin id |

**Response**

| Status | Code | Description |
|---|---|---|
| 200 | OK | Plugin enabled |
| 404 | NOT_FOUND | Unknown plugin |

## Sequences

### Plugin run

```
plugin-runner → load manifest → lifecycle hooks → deliver skill body → routes/tools active
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| SDK contract | `packages/plugin-sdk/` | Shared authoring types/helpers |
| Runner in engine | `plugin-runner.ts` | Isolates plugin execution from core |
| Interop lint | `check-plugin-interop-drift` | Catches drift at lint time |
| Version pinning | `check-pi-versions-pinned` | Keeps extension versions aligned |

## Risks and Unknowns

1. In-process plugin MCP discovery isolation is covered by engine tests; confirm the canonical plugin inventory.

## Out of Scope

- Fleet orchestration (FEAT-p9) and settings/provider config (FEAT-p8)