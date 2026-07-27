---
title: "Config System"
status: done
---

# Test Plan: Config System

## Scope

Config file discovery, parsing, validation, merging, hot-reload, and typed namespace resolution.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Parse valid opencode.jsonc | JSONC with comments | Parsed config object |
| TC-2 | Parse invalid JSONC | Malformed JSON | ConfigError returned |
| TC-3 | Merge global + project config | Two config sources | Deep-merged result |
| TC-4 | Project-local override wins | Same key in both sources | Project-local value used |
| TC-5 | Config namespace returns typed values | ConfigAgent access | Typed agent settings |
| TC-6 | Environment variable interpolation | Config with ${VAR} | Interpolated value |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Config discovery from multiple paths | Files in global, ancestor, project dirs | All sources discovered and merged |
| TC-8 | Hot-reload detects file change | Config file modified | New config emitted on stream |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | Config file not found anywhere | Default config returned |
| TC-10 | Type mismatch in config value | ConfigError with details |
| TC-11 | Invalid environment variable reference | Variable left as-is or error |
| TC-12 | Concurrent config reads during hot-reload | Consistent state returned |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-7 |
| FR-02 | TC-1, TC-2 |
| FR-03 | TC-3, TC-4 |
| FR-04 | TC-5 |
| FR-05 | TC-10 |
| FR-06 | TC-6 |
| FR-07 | TC-8 |
| NFR-01 | TC-9, TC-12 |

## Test Files

- `packages/opencode/test/config/config.test.ts`
- `packages/opencode/test/config/plugin.test.ts`
- `packages/opencode/test/config/tui.test.ts`
- `packages/opencode/test/config/lsp.test.ts`
- `packages/opencode/test/config/agent-color.test.ts`
- `packages/opencode/test/config/entry-name.test.ts`
- `packages/opencode/test/config/markdown.test.ts`
- `packages/opencode/test/config/fixtures/`
