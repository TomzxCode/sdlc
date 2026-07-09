---
title: "Plugin System"
status: draft
---

# Specification: Plugin System

## Overview

The PluginManager discovers plugins from multiple sources and provides a context (ctx) object through which plugins register hooks, tools, and CLI commands. A separate lazy discovery system handles model provider plugins, memory provider plugins, and other provider-type plugins.

## Architecture

```
PluginManager (hermes_cli/plugins.py)
    │
    ├── Discovery sources:
    │   ├── ~/.hermes/plugins/<name>/
    │   ├── ./.hermes/plugins/<name>/
    │   ├── pip entry points (hermes_plugins)
    │   └── Plugins/<name>/ (in-tree)
    │
    └── Each plugin provides register(ctx):
        ├── ctx.register_tool(name, schema, handler, ...)
        ├── ctx.register_cli_command(subparser)
        ├── ctx.register_hook(event, callback)
        └── ctx.register_provider(profile) (for model providers)

Provider registries (separate lazy discovery):
    ├── Model providers (plugins/model-providers/<name>/)
    │   └── providers.register_provider(ProviderProfile(...))
    ├── Memory providers (plugins/memory/<name>/)
    │   └── MemoryProvider ABC implementation
    ├── Context engines (plugins/context_engine/<name>/)
    ├── Image gen providers (plugins/image_gen/<name>/)
    ├── TTS providers
    ├── Transcription providers
    └── Web search providers
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Discovery timing | Lazy for providers, eager for general plugins | Provider registries are only scanned on first get/list, avoiding imports for unconfigured providers |
| Plugin isolation | No core file modification | Prevents conflicts and simplifies upgrades |
| Hook calling | Sequential, wrapped in try/except | A single failing hook should not block subsequent hooks or crash the agent |
| Model providers | Last-writer-wins | User plugins of the same name override bundled ones without patching the repo |

## Risks and Unknowns

1. General PluginManager and model-provider discovery systems are separate — plugins marked as kind: model-provider are discovered but not imported by PluginManager, which could lead to registration gaps
2. No versioning or compatibility checks for plugins (a plugin written for an older Hermes version may fail silently)
3. No plugin sandboxing outside of hook try/except wrapping

## Out of Scope

- Plugin marketplace/server
- Plugin version resolution and dependency management
- Sandboxed plugin execution