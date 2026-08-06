---
title: "Secrets, Settings & Provider Configuration"
status: done
---

# Test Plan: Secrets, Settings & Provider Configuration

## Scope

Covers secrets encryption and scopes, settings merge/precedence and sync, provider/model resolution and rotation, MCP configuration and validation, and the CLI/dashboard surfaces.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Secret scope validation | scoped secret | Scope accepted/rejected per policy |
| TC-2 | Secrets crypto (AES-256-GCM) | plaintext | Round-trip encrypt/decrypt |
| TC-3 | Effective settings merge | global+project | Merged with correct precedence |
| TC-4 | Configuration revision store | revision write | Revision recorded |
| TC-5 | Custom provider registry | provider def | Registered/validated |
| TC-6 | Run-audit secret taxonomy | audit rows | Secret material never present |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Secrets env writer | scoped secret | Env written per access policy |
| TC-8 | Secrets sync across nodes | two nodes | Secrets synced with auth parity |
| TC-9 | MCP config route | mcp config | 200 valid / 400 invalid |
| TC-10 | Settings memory routes | settings | Read/write round-trip |
| TC-11 | Custom provider routes | provider | CRUD works |
| TC-12 | Settings export/import (CLI) | settings file | Round-trip preserved |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Rotation exhaustion | Append-only exhaustion recorded, starting instance excluded |
| TC-14 | Dangling credential instance | Falls back to provider default with metadata |

## Test Infrastructure

- Vitest core/engine/dashboard/CLI suites

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-3, TC-4, TC-8 |
| FR-3 | TC-5, TC-11, TC-13, TC-14 |
| FR-4 | TC-9 |
| FR-5 | TC-10, TC-12 |
| NFR-1 | TC-6 |

## Key Test Files

- `packages/core/src/__tests__/secrets-*.test.ts`, `is-secret-scope.test.ts`, `automation.test.ts`, `configuration-revision-store.test.ts`
- `packages/engine/src/__tests__/secrets-env-writer.test.ts`, `run-audit-secret-taxonomy.test.ts`, `effective-settings-merge.test.ts`
- `packages/dashboard/src/routes/__tests__/register-secrets-routes.test.ts`, `register-config-mcp-pi-settings-routes.test.ts`, `custom-provider-routes*.test.ts`
- `packages/cli/src/commands/__tests__/settings.test.ts`, `settings-export.test.ts`, `mcp.test.ts`, `provider-auth.test.ts`, `provider-settings.test.ts`, `custom-provider-registry.test.ts`