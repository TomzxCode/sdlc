---
title: "Configuration System"
status: draft
---

# Specification: Configuration System

## Overview

Configuration is loaded from `openclaw.json` (the canonical file) with optional environment variable overrides. The schema is defined in TypeScript using zod and generates a JSON Schema for IDE support. Config mutation uses a merge-patch strategy to allow partial updates.

## Architecture

```
File System (openclaw.json)
     │
     ▼
Config Loader → Schema Validation (zod)
     │
     ├── Env Var Substitution
     ├── Merge-Patch
     └── Snapshot / Redaction
     │
     ▼
Runtime Config Object → Gateway / Agents / Channels / Plugins
```

## Data Models

### Config Schema (top-level)

| Field | Type | Description |
|---|---|---|
| agents | object | Agent-specific configuration |
| channels | object | Channel plugin configuration |
| models | object | Model provider configuration |
| plugins | object | Plugin settings |
| hooks | object | Hook scripts |
| cron | object | Cron job definitions |
| logs | object | Logging configuration |
| sandbox | object | Tool sandbox policies |

## Sequences

### Config Load Flow

```
Gateway Start → Config Loader: read openclaw.json
Config Loader → File System: parse JSON
Config Loader → Zod: validate against schema
Config Loader → Runtime: if valid, apply config; if invalid, report errors
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Schema definition | Zod | Runtime validation, TypeScript type inference, good DX |
| Config format | JSON | Universal, well-supported, no transpilation needed |
| Merge strategy | Custom merge-patch | Partial updates without overwriting unrelated keys |
| Secret redaction | Pattern-based snapshot redaction | Prevents credential leakage in logs and diagnostics |
| Legacy migration | Doctor --fix command | One-time migration, not runtime compat shims |

## Risks and Unknowns

1. Environment variable precedence can be confusing when multiple sources set the same key
2. Plugin config schemas must be validated at plugin registration time, which may fail if the plugin is not yet installed
3. JSON format does not support comments, which can be a pain point for users

## Out of Scope

- YAML/TOML config format support
- Config UI (web-based config editor)
- Config versioning/history
