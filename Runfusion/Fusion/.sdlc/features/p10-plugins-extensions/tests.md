---
title: "Plugins & Extension Ecosystem"
status: done
---

# Test Plan: Plugins & Extension Ecosystem

## Scope

Covers plugin runner execution and skill-body delivery, plugin management routes/UI, pi extension CLI routing (Claude CLI, Droid CLI, Llama.cpp), and skill/CLI command surfaces.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Plugin runner | plugin manifest | Lifecycle hooks run, skill body delivered |
| TC-2 | Merger plugin runner wiring | merge + plugin | Plugin invoked during merge |
| TC-3 | In-process runtime plugin MCP discovery isolation | plugin set | Per-plugin MCP discovery isolated |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Plugin skill integration | plugin skill | Skill body delivered |
| TC-5 | Plugin skill body delivery | skills | Body delivered per contract |
| TC-6 | Claude CLI extension | command | Routed into Claude CLI |
| TC-7 | Droid CLI extension | command | Routed into Droid CLI |
| TC-8 | Llama.cpp extension | command | Routed into Llama.cpp |
| TC-9 | Plugin manager routes | plugin store | CRUD supported |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-10 | Broken plugin manifest | Runner reports and does not crash host |
| TC-11 | Missing extension binary | CLI surfaces clear error |

## Test Infrastructure

- Vitest engine/dashboard/CLI suites; `packages/cli/src/commands/__tests__/*extension*`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-9 |
| FR-2 | TC-1, TC-2, TC-4, TC-5 |
| FR-3 | TC-10 |
| FR-4 | TC-6, TC-7, TC-8, TC-11 |
| NFR-2 | plugin-interop-drift check |

## Key Test Files

- `packages/engine/src/__tests__/plugin-runner.test.ts`, `plugin-skill-integration.test.ts`, `plugin-skill-body-delivery.test.ts`, `merger-plugin-runner-wiring.test.ts`, `in-process-runtime-plugin-mcp-discovery-isolation.test.ts`
- `packages/cli/src/commands/__tests__/plugin.test.ts`, `claude-cli-extension.test.ts`, `droid-cli-extension.test.ts`, `llama-cpp-extension.test.ts`
- `packages/dashboard/src/routes/__tests__/register-approval-routes...` + plugin route tests, `packages/dashboard/app/__tests__/api-plugins`, `PluginManager.test`