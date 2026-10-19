---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Stale test references

- Key Test Files names `packages/core/src/__tests__/automation.test.ts`. That file only covers cron automations and presets (`packages/core/src/__tests__/automation.test.ts:1` to `:20` imports `AUTOMATION_PRESETS` and `CronExpressionParser` from `../automation/automation.js`) and has no secrets, settings, MCP, or provider assertion.
- TC-10 "Settings memory routes" has no matching test file. `packages/dashboard/src/routes/register-settings-memory-routes.ts` has no dedicated test in `packages/dashboard/src/routes/__tests__/`, only `register-settings-memory-worktrunk.test.ts` and `packages/dashboard/src/__tests__/settings-workspace-mode-route.test.ts`, which cover single settings keys rather than the read/write round-trip TC-10 describes.

### Uncovered test areas

- The master key lifecycle has a test file that no TC references. `packages/core/src/__tests__/master-key.test.ts` covers the keychain-first resolution, the `~/.fusion/master.key` fallback, the `0600` permission check, rotation, and corruption detection implemented at `packages/core/src/secrets/master-key.ts:49` to `:208`.
- The secret access policy resolver has a test file that no TC references. `packages/core/src/__tests__/secret-access-policy.test.ts` covers the row policy, global default, and `prompt` fallback order implemented at `packages/core/src/secrets/secret-access-policy.ts:35` to `:48`.
- The shared redaction helper has a test file that no TC references. `packages/core/src/__tests__/redact-secrets.test.ts` covers `redactSecrets` at `packages/core/src/secrets/redact-secrets.ts:13`.
- The OAuth credential interop has a test file that no TC references. `packages/core/src/__tests__/oauth-credential-interop.test.ts` covers `packages/core/src/secrets/oauth-credential-interop.ts`.
- The provider instance key grammar has a test file that no TC references. `packages/core/src/provider-instance.test.ts` covers `formatProviderInstanceKey` and `parseProviderInstanceKey` at `packages/core/src/provider-instance.ts:45` and `:51`, which TC-14 depends on.
- The agent secret read tool has test files that no TC references. `packages/cli/src/__tests__/extension-secret-get-value-delivery.test.ts` and `packages/cli/src/__tests__/extension-permission-gates.test.ts` cover the `fn_secret_get` policy outcomes implemented at `packages/cli/src/extension.ts:3647` to `:3779`.
- The secrets sync passphrase reserved row has no test file. `packages/core/src/secrets/secrets-sync-passphrase.ts` has no matching test, and `docs/secrets.md:154` names `packages/core/src/__tests__/store-settings-sync-passphrase-probe.test.ts`, which does not exist in the repository.
- The secrets store PostgreSQL round-trip has a test file that no TC references. `packages/core/src/__tests__/postgres/secrets-roundtrip.test.ts` covers the `secrets` and `secrets_global` tables defined at `packages/core/src/postgres/schema/project.ts:1519` and `packages/core/src/postgres/schema/central.ts:276`.
- The MCP effective-server resolution has test files that no TC references. `packages/core/src/__tests__/mcp-config.test.ts`, `mcp-discovery.test.ts`, `mcp-builtin-servers.test.ts`, and `packages/engine/src/__tests__/mcp-resolution.test.ts` cover the global, plugin, and project resolution order and the `enabled:false` tombstone behavior at `packages/core/src/config/mcp-config.ts:93` to `:149`. Only TC-9, the route, is listed.
- The credential rotation tests are not in Key Test Files even though TC-13 depends on them. `packages/engine/src/__tests__/credential-instance-rotation.test.ts` and `packages/engine/src/__tests__/credential-rotation-lanes.test.ts` cover `packages/engine/src/credential-instance-rotation.ts:119` to `:135`.
- The TC-14 dangling instance fallback test files are not in Key Test Files. The behavior is at `packages/engine/src/agents/agent-session-helpers.ts:1110`, covered by `packages/engine/src/__tests__/agent-session-helpers.test.ts` and `packages/core/src/__tests__/postgres/credential-instance-selection.pg.test.ts`.
- The worktree env materialization acquisition and cleanup tests are not in Key Test Files. `packages/engine/src/__tests__/worktree-acquisition-secrets-env.test.ts` and `packages/engine/src/__tests__/worktree-pool-secrets-env-cleanup.test.ts` cover `packages/engine/src/worktree/worktree-acquisition.ts:870`.
- The model lane effective-settings test is not in Key Test Files. `packages/engine/src/__tests__/effective-settings-model-lane.test.ts` covers the lane overlay implemented at `packages/core/src/config/effective-settings-overlay.ts:12`.
