---
title: "Plugin SDK and Extension System"
status: done
---

# Test Plan: Plugin SDK and Extension System

## Scope

Tests cover the plugin SDK facade, runtime abstractions, plugin lifecycle management, import boundary enforcement, and plugin registry. Does not cover individual plugin implementations.

## Unit Tests

| File | Description |
|---|---|
| `src/plugin-sdk/facade-runtime.test.ts` | Facade runtime abstraction |
| `src/plugin-sdk/gateway-method-runtime.test.ts` | Gateway method runtime for plugins |
| `src/plugin-sdk/agent-core.test.ts` | Agent core SDK exports |
| `src/plugin-sdk/runtime.test.ts` | Runtime abstraction layer |
| `src/plugin-sdk/directory-runtime.test.ts` | Directory-based runtime resolution |
| `src/plugins/plugin-lifecycle-trace.test.ts` | Plugin lifecycle tracing |
| `src/plugins/plugin-scope.test.ts` | Plugin scope enforcement |
| `src/plugins/plugin-registry.test.ts` | Plugin registry CRUD operations |
| `src/plugins/loader.test.ts` | Plugin loading and resolution |
| `src/plugins/discovery.test.ts` | Plugin discovery mechanism |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Plugin import from core internals | Import boundary check fails |
| Missing plugin dependency | Graceful error, installation blocked |
| Duplicate plugin registration | Registry rejects duplicate ID |
| Plugin config schema validation | Invalid config produces clear error |

## Test Infrastructure

- Vitest unit test runner
- Mock filesystem for plugin installation tests
- Import boundary test helpers
- In-memory plugin registry store

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (SDK types and interfaces) | `facade-runtime.test.ts`, `agent-core.test.ts` |
| FR-2 (npm package installation) | `plugin-registry.test.ts` |
| FR-3 (Plugin lifecycle) | `plugin-lifecycle-trace.test.ts` |
| FR-4 (Import boundaries) | `plugin-scope.test.ts` |
| FR-6 (Plugin registry) | `plugin-registry.test.ts`, `discovery.test.ts` |
| NFR-1 (Boundary enforcement) | `plugin-scope.test.ts`, `extension-import-boundaries.test.ts` |
