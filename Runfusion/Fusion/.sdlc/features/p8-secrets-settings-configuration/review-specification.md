---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Architecture

- The diagram names `register-provider-routes` as a route registrar. No such file exists in `packages/dashboard/src/routes/`. The shipped registrars for this feature are `register-secrets-routes.ts`, `register-secrets-sync-routes.ts`, `register-secrets-sync-inbound-routes.ts`, `register-config-mcp-pi-settings-routes.ts`, `register-settings-memory-routes.ts`, `register-settings-sync-routes.ts`, `register-settings-sync-inbound-routes.ts`, `register-custom-provider-routes.ts`, `register-runtime-provider-routes.ts`, and `register-model-routes.ts`.
- The diagram omits the secrets sync, settings sync, runtime provider, and settings memory registrars, and the core modules `secrets-sync-passphrase.ts`, `oauth-credential-interop.ts`, `redact-secrets.ts` (`packages/core/src/secrets/index.ts:5` to `:12`), plus `packages/core/src/provider-instance.ts`, `packages/core/src/plugin-mcp-servers.ts`, and `packages/core/src/config/mcp-builtin-servers.ts`.
- The diagram omits the engine-side owners of this feature: `packages/engine/src/credential-instance-rotation.ts:119` (rotation run-audit) and `packages/engine/src/worktree/secrets-env-writer.ts:330` (env materialization).
- The bottom layer says "PostgreSQL / file-backed secrets + sync". Secrets are PostgreSQL-only, and the file-backed part is global settings rather than secrets. Global settings live in `~/.fusion/settings.json` (`packages/core/src/config/global-settings.ts:180`) and project settings live in the `config.settings` jsonb column (`packages/core/src/postgres/schema/project.ts:444`).

### Data Models

- The Secret model lists `name` as the primary key. The stored columns are `id` as primary key plus `key` as a unique key (`packages/core/src/postgres/schema/central.ts:276` to `:293`, `packages/core/src/postgres/schema/project.ts:1519` to `:1538`, and `SecretRecord` at `packages/core/src/secrets/secrets-store.ts:16`).
- The Secret model lists `ciphertext` as one field. The schema stores `value_ciphertext` and `nonce` as two separate bytea columns (`packages/core/src/postgres/schema/central.ts:279` to `:280`).
- The Secret model lists `scope` as an enum with a task scope. Scope is not a column. It is implied by the table, and only `project` and `global` exist (`packages/core/src/secrets/secrets-store.ts:9` to `:12`, `docs/secrets.md:48` to `:68`).
- The Secret model omits `description`, `envExportable`, `envExportKey`, `lastReadAt`, and `lastReadBy` (`packages/core/src/secrets/secrets-store.ts:16` to `:28`, `packages/core/src/postgres/schema/project.ts:1525` to `:1532`).
- The Secret model omits the access policy values and their resolution order. The policy enum is `auto`, `prompt`, `deny`, and the resolver is row policy, then global `secretsAccessPolicy`, then the fallback `prompt` (`packages/core/src/secrets/secret-access-policy.ts:28` to `:48`, `packages/core/src/postgres/schema/project.ts:1536`).
- The Settings model lists per-key rows with a `key` primary key, a `value` column, and a `level` enum. Settings are two JSON documents, not per-key rows (`packages/core/src/config/global-settings.ts:180`, `packages/core/src/postgres/schema/project.ts:444`, merged at `packages/core/src/task-store/settings-ops-2.ts:35` to `:43`).
- The Settings model lists a task level. `SettingsScope` is `"global" | "project"` (`packages/core/src/types/settings/settings-scope.ts:70`), and no task-scoped settings store exists. The task tier in the shipped model is the task's own model selection, overlaid through `packages/engine/src/project/effective-settings.ts:75`.

### API Contracts

- The documented `POST /api/settings/mcp` endpoint does not exist. The MCP endpoints are `GET /api/mcp/plugin-servers` (`packages/dashboard/src/routes/register-config-mcp-pi-settings-routes.ts:139`), `GET /api/mcp/discovered` (`:168`), and `POST /api/mcp/validate` (`:197`). Server definitions are written through the settings endpoints `PUT /api/settings` and `PUT /api/settings/global` (`packages/dashboard/src/routes/register-settings-memory-routes.ts:629`, `:1983`).
- The documented request body fields `name`, `command`, `secretRefs`, and `enabled` do not match `McpServerDefinition`. The shipped shape uses `transport` of `stdio`, `sse`, or `streamable-http`, `command` with `args` or `url`, and `env` or `headers` maps of `{ secretRef, scope }` (`packages/core/src/types/settings/settings-scope.ts:212` to `:262`, `packages/core/src/config/mcp-config.ts:16` to `:23`).
- The documented response "400 INVALID_INPUT on validation failure" does not match the route. Secret resolution failure returns HTTP 400 with an `errors` array (`packages/dashboard/src/routes/register-config-mcp-pi-settings-routes.ts:100` to `:102`), and the validation probe returns HTTP 200 with a `{ status, message }` payload (`packages/engine/src/mcp/mcp-validation-service.ts:37` to `:49`).

### Decisions

- The decision row "Model hierarchy, global then project then task then lane" is inverted versus the shipped precedence (`docs/settings-reference.md:1189`, and the per-lane lists at `docs/settings-reference.md:1219` to `:1318`).

### Risks and Unknowns

- The risk "Secrets sync between nodes authentication parity is an open security review area" is resolved. The inbound route requires a Bearer `apiKey` that matches the local node key and returns HTTP 401 on a missing or mismatched token (`packages/dashboard/src/routes/register-secrets-sync-inbound-routes.ts:100` to `:119`).
