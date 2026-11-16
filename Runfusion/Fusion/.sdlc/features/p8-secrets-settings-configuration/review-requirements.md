---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-10-19

### Missing requirements

- Secrets environment materialization into task worktrees is implemented but no FR requires it. `ProjectSettings.secretsEnv` (`packages/core/src/types/settings/settings-scope.ts:1400`), the env-exportable secret list with project-over-global override (`packages/core/src/secrets/secrets-store.ts:153`), and the atomic `.env` writer plus fingerprint cleanup (`packages/engine/src/worktree/secrets-env-writer.ts:330`, `packages/engine/src/worktree/worktree-acquisition.ts:870`) are outside FR-1, which only covers encryption, scopes, and access policies.
- Master key lifecycle is implemented but no FR requires it. `MasterKeyManager` resolves the keychain first with a `~/.fusion/master.key` file fallback, enforces mode `0600`, detects corruption, and can rotate the key (`packages/core/src/secrets/master-key.ts:36`, `:66`, `:195`). FR-1 says nothing about master key storage or rotation.
- Cross-node secrets sync is implemented but no FR requires it. `wrapSecretsBundle` and `unwrapSecretsBundle` use scrypt plus AES-256-GCM (`packages/core/src/secrets/secrets-sync.ts:60`, `:81`), the passphrase lives in the reserved `__sync_passphrase__` row (`packages/core/src/secrets/secrets-sync-passphrase.ts:3`), and the push/pull/export/receive routes are registered (`packages/dashboard/src/routes/register-secrets-sync-routes.ts:52`, `packages/dashboard/src/routes/register-secrets-sync-inbound-routes.ts:92`). FR-2 covers settings sync only.
- The agent-facing secret read tool is implemented but no FR requires it. `fn_secret_get` is registered in the pi extension with the auto, prompt, and deny policy outcomes and the approval flow (`packages/cli/src/extension.ts:3647`, `:3698`, `:3725`). FR-5 lists CLI, dashboard API, and Settings modal surfaces and does not mention the agent tool, and no FR describes the approval gate.
- Settings export, import, and organization bundles are implemented but no FR requires them. `exportSettings` and `importSettings` (`packages/core/src/config/settings-export.ts:188`, `:367`), the CLI commands (`packages/cli/src/bin.ts:1741`, `:1756`), and the credential-scrubbed org bundle (`packages/core/src/agents/org-bundle.ts:85`, `packages/cli/src/commands/org-export.ts:1`) have no requirement. TC-12 in `tests.md` covers the behavior while no FR states it.
- Configuration revision history is implemented but no FR requires it. `ConfigurationRevisionStore` appends and pages immutable revisions (`packages/core/src/config/configuration-revision-store.ts:16`), and the Settings modal renders them (`packages/dashboard/app/components/settings/sections/ConfigurationVersionsSection.tsx`). TC-4 covers the store while no FR states it.
- The custom provider registry is implemented but no FR requires it. The CRUD and model-refresh routes for user-defined OpenAI-compatible, Anthropic-compatible, and Google Generative AI providers are shipped (`packages/dashboard/src/routes/register-custom-provider-routes.ts:609`, `:722`). FR-3 covers credential instances and fallback resolution, not user-defined provider definitions.

### Stale requirements

- FR-6 states the model-selection hierarchy as global, then project, then task, then lane. The shipped order is task-specific selection, then project workflow-lane baseline, then global lane, then selected-workflow value, then project default, then global default, then automatic resolution (`docs/settings-reference.md:1189`, and the per-lane lists at `docs/settings-reference.md:1219` to `:1318`). FR-6 puts the lowest-precedence source first and omits the workflow tiers.
- FR-5 states that secrets and provider operations are exposed via CLI. There is no `fn secrets` command and no provider command. `packages/cli/src/bin.ts` registers `fn settings` at line 1724 and `fn mcp` at line 1782 and no other settings-adjacent command, while secret and provider CRUD live only in the dashboard (`packages/dashboard/src/routes/register-secrets-routes.ts:79`, `packages/dashboard/src/routes/register-custom-provider-routes.ts:609`).
- NFR-3 states that settings sync must reconcile across nodes. On the default PostgreSQL backend the node settings sync routes refuse to reconcile and return HTTP 409 with code `settings-sync-disabled-postgres` (`packages/dashboard/src/routes/register-settings-sync-routes.ts:152`), because all nodes share one database (`packages/core/src/task-store/settings-ops-2.ts:26`).
- Open Question 1 asks how secrets sync between nodes authenticates. The inbound route already requires a matching Bearer `apiKey` and returns HTTP 401 otherwise (`packages/dashboard/src/routes/register-secrets-sync-inbound-routes.ts:100`, `:114`, `:117`), so the question is answered by the code.

## Sync drift: 2026-11-16

Re-verified against current code; the artifacts still carry `status: done` with unchecked acceptance criteria and the same gaps:

- FR-5 still claims a CLI surface for secrets and provider operations. `packages/cli/src/bin.ts` registers settings and mcp commands but no `fn secrets` or provider command; secret and provider CRUD live only in dashboard routes (`register-secrets-routes.ts`, `register-custom-provider-routes.ts`).
- FR-6 still inverts the model hierarchy. `docs/settings-reference.md:337` documents task-specific selections and the project-lane baseline winning over global and per-workflow values; the requirement states global → project → task → lane.
- NFR-3 still claims cross-node settings reconciliation, but the default PostgreSQL backend returns 409 with code `settings-sync-disabled-postgres` (`packages/dashboard/src/routes/register-settings-sync-routes.ts:156`).
- Implemented behavior still has no FR: worktree secret env materialization (`packages/engine/src/worktree/secrets-env-writer.ts`), master key lifecycle (`packages/core/src/secrets/master-key.ts`), cross-node secrets sync (`secrets-sync.ts`, `secrets-sync-passphrase.ts`), the `fn_secret_get` agent tool with approval policy (`packages/cli/src/extension.ts`), and configuration revisions (`packages/core/src/config/configuration-revision-store.ts`).
- Open Question 1 is still answered in code: the inbound sync route requires a Bearer `apiKey` and returns 401 otherwise (`register-secrets-sync-inbound-routes.ts:101-118`).
