---
title: "Configuration System"
status: done
---

# Test Plan: Configuration System

## Scope

Tests cover configuration loading, schema validation, merge-patch, environment variable substitution, file parsing, config mutation, and runtime overrides. Does not cover CLI or gateway integration.

## Unit Tests

| File | Description |
|---|---|
| `src/config/schema.test.ts` | Schema validation rules |
| `src/config/validation.test.ts` | Config validation logic |
| `src/config/merge-patch.test.ts` | Merge-patch update strategy |
| `src/config/paths.test.ts` | Config path resolution |
| `src/config/io.parse.test.ts` | Config file parsing |
| `src/config/mutate.test.ts` | Config mutation operations |
| `src/config/runtime-overrides.test.ts` | Runtime config overrides |
| `src/config/dead-config-keys.test.ts` | Dead/deprecated key detection |
| `src/config/config.env-vars.test.ts` | Environment variable substitution |
| `src/config/includes.test.ts` | Config include/inheritance resolution |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Invalid JSON file | Parse error with location info |
| Missing required key | Schema validation error |
| Environment variable not set | Default value or clear error |
| Circular includes | Detected and rejected |
| Deprecated config key | Warning issued, migration suggested |

## Test Infrastructure

- Vitest unit test runner
- Mock filesystem for config loading tests
- Zod schema validation fixtures

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (Config loading) | `io.parse.test.ts`, `paths.test.ts` |
| FR-2 (Schema validation) | `schema.test.ts`, `validation.test.ts` |
| FR-3 (Env var substitution) | `config.env-vars.test.ts` |
| FR-5 (Merge-patch) | `merge-patch.test.ts` |
| FR-8 (Includes/inheritance) | `includes.test.ts` |
| FR-9 (Secret redaction) | Covered by general redaction tests |
| NFR-2 (Deprecated key errors) | `dead-config-keys.test.ts` |
