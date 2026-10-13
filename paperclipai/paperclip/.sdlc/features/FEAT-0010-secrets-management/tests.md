---
title: "Secrets Management"
status: done
session_link: "reverse-engineered during 2026-10-13 sync; no live session"
---

# Test Plan: Secrets Management

## Scope

Covers company-scoped secret CRUD, versioning with SHA256 fingerprints, bindings via config paths, pluggable provider vaults, inline `${{ secrets.key }}` refs, runtime resolution with env overlays, metadata-only API responses, and audit events.
Out of scope: automatic rotation/expiry notification, cross-company sharing.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Secrets service (`server/src/__tests__/secrets-service.test.ts`) | Create/version/read/delete ops | Metadata-only payloads, version rows with fingerprints |
| TC-2 | JSON schema secret refs (`server/src/__tests__/json-schema-secret-refs.test.ts`) | Configs with inline refs | Refs parsed and resolved correctly |
| TC-3 | AWS provider (`server/src/__tests__/aws-secrets-manager-provider.test.ts`) | Provider vault ops | Material stored and fetched via AWS backend |
| TC-4 | Secret proposals migration (`packages/db/src/company-secret-proposals-migration.test.ts`) | Pending migration | Schema migrates safely |
| TC-5 | Run secret redaction (`server/src/__tests__/run-secret-redaction.test.ts`) | Run context with resolved secrets | No plaintext in snapshots |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Secrets routes (`server/src/__tests__/secrets-routes.test.ts`) | Authenticated company context | CRUD/version/binding/access-event endpoints; value never returned |
| TC-7 | Agent secret bindings (`server/src/__tests__/agents-service-secret-bindings.test.ts`) | Agent with bindings | Resolution scoped to owning company |
| TC-8 | Agent secrets routes (`server/src/__tests__/agent-secrets-routes.test.ts`) | Agent execution context | Env injection without plaintext in configs |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-9 | Creation-to-injection flow | Board creates secret, binds to agent, agent runs | Agent receives value via env; API never returns value; access event recorded |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-10 | Duplicate secret key within company | 409 CONFLICT |
| TC-11 | Cross-company access attempt | 403 UNAUTHORIZED |
| TC-12 | Logs inspected after resolution | No plaintext secret values present |

## Test Infrastructure

- Vitest suite under `server/src/__tests__/` and `packages/db/src/`.
- Provider doubles (local encrypted default, AWS) and company-scoped fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-6 |
| FR-02 | TC-1, TC-4 |
| FR-03 | TC-7 |
| FR-04 | TC-6, TC-9 |
| FR-05 | TC-3 |
| FR-06 | TC-1, TC-6, TC-9 |
| FR-07 | TC-2 |
| FR-08 | TC-8 |
| FR-09 | TC-7, TC-8 |
| NFR-03 | TC-5, TC-12 |
