---
title: "Plugin System"
status: draft
---

# Specification: Plugin System

## Overview

Plugins are out-of-process workers registered instance-wide. A capability-gated host exposes services (tools, jobs, webhooks, UI contributions, database namespaces) to plugins. The adapter plugin loader is the dynamic-loading path for external adapters and external adapter plugins. An SDK and scaffolder (`create-paperclip-plugin`) support authoring.

## Architecture

```
Operator ──► /api/plugins (install/config/state)
                │
                ▼
           plugins table + plugin_config/state/entities/jobs/logs/webhooks
                │
                ▼
           plugin-loader (dynamic) ──► external adapters (zero hardcoded imports)
Host services (capability-gated) ◄── plugin worker ──► plugin_database namespaces/migrations
SDK (packages/plugins/sdk) + create-paperclip-plugin scaffolder
```

## Data Models

### plugins and plugin support tables

| Field | Type | Constraints | Description |
|---|---|---|---|
| plugins.id / company/instance scope | - | - | Plugin registration |
| plugin_config / plugin_state | - | - | Config and runtime state |
| plugin_entities / plugin_jobs / plugin_logs / plugin_webhooks | - | - | Plugin-owned artifacts |
| plugin_database (namespaces/migrations) | - | - | Isolated plugin DB |
| plugin_managed_resources / plugin_company_settings | - | - | Managed resources and per-company settings |

## API Contracts

### /api/plugins, /api/plugin-ui-static

Plugin installation, configuration, state, jobs, logs, webhooks, and UI static assets. Route: `server/src/routes/plugins.ts`.

### Adapter plugin loading

External adapters via `~/.paperclip/adapter-plugins.json`; `createServerAdapter()` includes all optional fields. Loader: `server/src/adapters/plugin-loader.ts`, store: `server/src/services/adapter-plugin-store.ts`.

## Sequences

### External adapter install

```
operator → Adapter manager → adapter-plugins.json entry → plugin-loader dynamic load → createServerAdapter (all fields) → adapter registered
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Loader purity | Zero hardcoded adapter imports | Enables fully external adapters without core changes |
| Adapter registration | Include all optional fields (`detectModel`) | Avoid silent capability loss for external adapters |

## Risks and Unknowns

1. Built-in UI parsers can shadow external plugin parsers; removing built-ins when externalized needs coordination.

## Out of Scope

- Cloud-grade plugin marketplace and packaged public distribution.
