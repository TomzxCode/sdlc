---
title: "Plugin System"
status: done
---

# Test Plan: Plugin System

## Scope

Tests covering PluginManager discovery, plugin lifecycle hooks, tool registration, CLI subcommand registration, model provider lazy discovery, and memory provider ABC conformance.

## Test Files

- tests/hermes_cli/test_plugins.py — Plugin discovery and registration
- tests/hermes_cli/test_plugins_cmd*.py — Plugin CLI commands
- tests/hermes_cli/test_plugin_scanner_recursion.py — Plugin scanner depth
- tests/hermes_cli/test_plugin_runtime_disable_gate.py — Runtime disable gating
- tests/hermes_cli/test_plugin_auxiliary_tasks.py — Auxiliary plugin tasks
- tests/hermes_cli/test_plugin_cli_registration.py — CLI subcommand registration
- tests/plugins/ — 15+ plugin-specific test directories
- tests/tools/test_mcp_*.py — MCP plugin integration tests (30+ files)
- tests/hermes_cli/test_memory_providers.py — Memory provider registration
- tests/hermes_cli/test_startup_plugin_gating.py — Plugin gating at startup

## Unit Tests

- Plugin discovery from filesystem and entry points
- Hook registration and invocation order
- Tool schema collection from registered plugins
- CLI subcommand tree wiring
- Provider profile registration (last-writer-wins)

## Integration Tests

- Full plugin lifecycle: discover → register → hook → tool call
- Model provider lazy discovery via providers.register_provider()
- Memory provider ABC conformance testing
- Plugin hook failure isolation (try/except wrapping)
- Plugin CLI subcommand discovery and dispatch

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Plugin with missing register() | Skipped with warning |
| Hook callback crashes | Error logged, other hooks and agent continue |
| Duplicate plugin name | Last-writer-wins merge |
| Plugin modifies core file | No mechanism to prevent (policy relies on convention) |
| Circular plugin dependency | Unresolved (no dependency manager yet) |

## Test Infrastructure

- Temp plugin directories for discovery testing
- Mock plugin packages with controlled hooks
- Isolated import scope per test

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (discovery from sources) | test_plugins.py |
| FR-2 (lifecycle hooks) | test_plugins.py hook tests |
| FR-3 (register_tool) | test_plugins.py tool registration tests |
| FR-4 (register_cli_command) | test_plugin_cli_registration.py |
| FR-5 (lazy provider discovery) | Model provider tests |
| FR-6 (MemoryProvider ABC) | test_memory_providers.py |
| NFR-1 (no core file modification) | Plugin policy enforcement tests |
