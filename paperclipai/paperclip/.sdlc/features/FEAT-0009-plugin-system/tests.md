---
title: "Plugin System"
status: done
session_link: "reverse-engineered during 2026-10-13 sync; no live session"
---

# Test Plan: Plugin System

## Scope

Covers instance-wide plugin install/config, capability-gated host services, dynamic external adapter loading with zero hardcoded imports, `createServerAdapter()` field completeness, plugin DB namespaces, jobs/logs/webhooks, and UI static assets.
Out of scope: cloud-grade marketplace and packaged public distribution.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Plugin loader retry (`server/src/__tests__/plugin-loader-error-retry.test.ts`) | Failing plugin load | Retry behavior per contract |
| TC-2 | Plugin install guard (`server/src/__tests__/plugin-install-guard.test.ts`) | Install requests | Guard accepts or rejects correctly |
| TC-3 | Plugin database (`server/src/__tests__/plugin-database.test.ts`) | Namespace and migration ops | Isolated plugin DB state correct |
| TC-4 | Adapter registry reconcile (`server/src/services/adapter-registry-bootstrap.reconcile.test.ts`) | Registry plus adapter-plugin store | External adapters reconcile without hardcoded imports |
| TC-5 | Bundled plugins (`server/src/__tests__/bundled-plugins.test.ts`) | Bundled catalog | Plugins load as expected |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Plugin routes authz (`server/src/__tests__/plugin-routes-authz.test.ts`) | Caller with varying permissions | Install/config/state endpoints enforce authz |
| TC-7 | Host services span (`server/src/__tests__/plugin-host-services-span.test.ts`) | Plugin invoking host services | Capability gating enforced; ungranted calls denied |
| TC-8 | Secrets handler (`server/src/__tests__/plugin-secrets-handler.test.ts`) | Plugin secret access | Handled per capability policy |
| TC-9 | UI static assets (`server/src/__tests__/plugin-ui-static.test.ts`) | Plugin UI contribution | Static assets served correctly |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-10 | External adapter install flow | Operator adds adapter-plugins.json entry, loader runs | Adapter dynamically registered with all optional fields |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Plugin exceeds granted capability | Call denied |
| TC-12 | Built-in parser shadowing plugin parser | Externalized parser takes precedence once coordinated |

## Test Infrastructure

- Vitest suite under `server/src/__tests__/` and `server/src/services/`.
- Adapter plugin store doubles and `~/.paperclip/adapter-plugins.json` fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-2, TC-6 |
| FR-02 | TC-4, TC-10 |
| FR-03 | TC-7, TC-8 |
| FR-04 | TC-4, TC-10 |
| FR-05 | TC-3 |
| FR-06 | TC-1, TC-9 |
| FR-07 | TC-4, TC-10 |
| NFR-01 | TC-7, TC-11 |
| NFR-02 | TC-12 |
