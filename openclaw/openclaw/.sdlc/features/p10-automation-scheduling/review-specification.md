---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-10-19

### The `extensions/webhooks/` architecture block no longer exists

- Status: BLOCKING
- Evidence:
  - `src/plugins/config-state.ts:30-36` lists `"webhooks"` in `RETIRED_PLUGIN_IDS`; `isRetiredPluginId` (line 43) rejects the id.
  - `ls extensions/webhooks` returns "No such file or directory".
  - `src/gateway/hooks.ts` (685 lines) and `src/gateway/hooks-mapping.ts` (683 lines) implement the inbound webhook path; `src/gateway/server/hooks-request-handler.ts` and `src/gateway/server/hooks-event-dispatch.ts` handle the request.
  - `src/gateway/hooks.ts:36`: `const DEFAULT_HOOKS_PATH = "/hooks";`
  - `src/gateway/hooks.ts:85-95` resolves `basePath`, `token`, `maxBodyBytes`, `mappings`, agent policy, and session policy from the core `hooks` config.
- Artifact currently says:
  ```
  Webhook Receiver ───→ Agent Session
  (extensions/webhooks/)  (HTTP body as context)
  ```
  and the Technical Decisions table row: "Webhook plugin | Extension (extensions/webhooks/) | Follows plugin architecture for optional functionality".
- What the code actually does: there is no webhook extension plugin. Inbound webhooks are a core Gateway subsystem that resolves its base path (default `/hooks`), bearer token, body-size ceiling, path mappings, and agent/session policy from the top-level `hooks` config block, and dispatches into agent sessions. The Technical Decisions row that justifies the design ("Follows plugin architecture for optional functionality") is now false.
- Needed change: replace the `extensions/webhooks/` block with the core `hooks` config plus `src/gateway/hooks.ts`, and rewrite the Technical Decisions row to record that webhook ingress is core-owned and not optional.

### The `WebhookConfig` data model describes a record that does not exist

- Status: BLOCKING
- Evidence:
  - No `WebhookConfig` type exists anywhere in the repository (`grep` for `WebhookConfig` returns nothing outside the artifact).
  - The actual shape is `HooksConfig` in `src/config/types.hooks.ts`, built on `OpenClawSchemaShape.hooks` from `src/config/zod-schema.hooks.ts`, with fields `enabled`, `token`, `path`, `allowedAgentIds`, `allowRequestSessionKey`, and `mappings` (each `HookMappingConfig`), plus `gmail` and `internal` sub-blocks.
  - `src/gateway/hooks.ts:41-56` defines the resolved runtime view: `basePath`, `token`, `maxBodyBytes`, `maxBodyBytesByPath`, `mappings`, `agentPolicy`, `sessionPolicy`.
  - `src/gateway/hooks.ts:36`: `const DEFAULT_HOOKS_MAX_BODY_BYTES = 256 * 1024;`
- Artifact currently says:
  ```
  ### WebhookConfig

  | Field | Type | Constraints | Description |
  |---|---|---|---|
  | id | string | PK | Webhook identifier |
  | path | string | not null, unique | URL path segment |
  | agent_id | string | not null | Target agent for the session |
  ```
- What the code actually does: webhook configuration is a single shared Gateway config object, not a per-webhook record with an id. There is no `agent_id` field; the target agent comes from the per-mapping `agentId` and from the `allowedAgentIds` allowlist, and the mapping list is what makes paths unique.
- Needed change: replace the `WebhookConfig` table with the `HooksConfig` shape, its resolved runtime view, and the per-mapping fields.

### `src/flows/` no longer contains a flow engine

- Status: BLOCKING
- Evidence:
  - `src/flows/` (123 files) contains doctor health checks and setup flows only: `doctor-core-checks.ts`, `doctor-health.ts`, `doctor-repair-flow.ts`, `doctor-lint-flow.ts`, `doctor-health-contributions.ts`, `health-check-registry.ts`, `channel-setup.ts`, `provider-flow.ts`, `model-picker.ts`, `search-setup.ts`, `memory-setup.ts`.
  - `extensions/lobster/src/lobster-runner.ts` and `extensions/lobster/src/lobster-tool.ts` implement the multi-step pipeline runtime; `docs/tools/lobster.md:69-70` states "The separately installed official `@openclaw/lobster` plugin runs Lobster workflows **in-process** using its embedded `@clawdbot/lobster` runtime."
  - `docs/automation/index.md:80-81`: "The shared Tasks ledger, TaskFlow orchestration API, and TaskFlow Webhooks plugin have been removed."
- Artifact currently says:
  ```
  Flow Engine ───→ Health Checks / Doctor / Setup
  (src/flows/)
  ```
  and "Flows (`src/flows/`) implement multi-step automation scripts typically used for doctor checks and setup."
- What the code actually does: the first clause still holds, but "multi-step automation scripts" is no longer what `src/flows/` provides. There is no core multi-step automation engine; the multi-step pipeline capability is the optional Lobster plugin, and the core Tasks/TaskFlow orchestration surface was removed outright.
- Needed change: narrow the flow block to doctor and setup flows, and either remove the multi-step claim or attribute it to the optional Lobster plugin.

### The `CronJob` data model is out of date

- Status: BLOCKING
- Evidence:
  - `packages/gateway-protocol/src/schema/cron.ts:463-499` defines the current `CronJobSchema`: `id`, `declarationKey`, `displayName`, `owner`, `scheduledToolPolicy`, `agentId`, `sessionKey`, `name`, `description`, `enabled`, `deleteAfterRun`, `createdAtMs`, `updatedAtMs`, `configRevision`, `schedule`, `pacing`, `trigger`, `sessionTarget`, `wakeMode`, `payload`, `delivery`, `failureAlert`, `state`, `nextRunAtMs`, `lastRunAtMs`, `lastRunStatus`, `lastRunError`, `lastDelivered`, `lastDeliveryStatus`, `lastDeliveryError`, `deliverySuppressionReason`, and the failure-notification delivery fields.
  - `packages/gateway-protocol/src/schema/cron.ts:138-180` defines `CronScheduleSchema` as the union of `event`, `at`, `every`, `cron`, `on-exit`, and `stream`.
  - `packages/gateway-protocol/src/schema/cron.ts:205-250` shows `model`, `toolsAllow`, `fallbacks`, `thinking`, and `timeoutSeconds` live on the payload variants, not at the job root.
  - `src/cron/types.ts:364-384` defines the TypeScript `CronJob` with `owner`, `scheduledToolPolicy`, `trigger`, and `state`; `src/cron/types.ts:410-425` defines `CronStoredJob` with the store-only fields.
  - `src/cron/store/schema.ts:1-50` shows the persisted shape: `job_json` plus `state_json` in the `cron_jobs` table, not one column per field.
- Artifact currently says:
  ```
  ### CronJob

  | Field | Type | Constraints | Description |
  |---|---|---|---|
  | id | string | PK | Unique job identifier |
  | schedule | string | not null | Cron expression |
  | model | string | optional | Model override for job execution |
  | tools | string[] | optional | Tool allowlist for job |
  | enabled | boolean | not null | Whether the job is active |
  | last_run | timestamp | nullable | Last execution timestamp |
  ```
- What the code actually does: `schedule` is a discriminated union object rather than a cron string; `model` and `tools` are payload-level fields on the `agentTurn`/`command`/`script` payload variants, not job-level columns; `last_run` is split into `lastRunAtMs`, `lastRunStatus`, `lastRunError`, and a rich `state` object that also carries `consecutiveErrors` and `autoDisabled`; and the job carries owner, delivery, failure-alert, pacing, trigger, session-target, and wake-mode fields the table does not mention.
- Needed change: replace the `CronJob` table with the current protocol shape, and add a table for the `state` object and for the payload variants.

### The isolated-session model has grown past "model, tools, sandbox"

- Status: ADVISORY
- Evidence:
  - `src/cron/isolated-agent/` (100 files) implements the isolated runner, including `run-fallback-policy.ts`, `run-sandbox-admission.ts`, `model-selection.ts`, `run-timeout.ts`, `channel-output-policy.ts`, and `delivery-dispatch.ts`.
  - `src/cron/isolated-agent/run-sandbox-admission.test.ts` and `src/cron/isolated-agent/run-fallback-policy.test.ts` cover the sandbox-admission and fallback behavior.
  - `packages/gateway-protocol/src/schema/cron-shared.ts` shows payload-level `fallbacks`, `thinking`, `timeoutSeconds`, and `toolsAllow`.
- Artifact currently says: "Isolated Agent Sessions (per-job config: model, tools, sandbox)" and the Technical Decisions row "Isolated sessions | Per-job agent session with configurable model/tools | Prevents cron jobs from interfering with user sessions".
- What the code actually does: the per-job configuration surface now includes model, model fallbacks, thinking level, tool allowlist, timeout, sandbox admission, and the target session (main, isolated, current, or a named session). The "sandbox" mention in the diagram has no counterpart in the per-job config; sandbox admission is a separate runtime gate.
- Needed change: expand the per-job config list to include fallbacks, thinking, timeout, and session target, and drop "sandbox" from the per-job config list.

### The failure path gained a repair stage that the sequences do not describe

- Status: ADVISORY
- Evidence:
  - `src/cron/service/notification-dispatch.ts:108-118` routes the failure notification to `runCronFailureRepair` first and only falls back to the alert when the repair request cannot be made.
  - `src/cron/service/failure-repair-brief.ts:40-66` builds the repair brief with the transient/fixable/ask-the-user branch instructions and the `SILENT_REPLY_TOKEN` contract.
  - `src/cron/service/state.ts:261,266` define `failureRepairTimeoutMs` and the `runCronFailureRepair` dependency.
  - `src/cron/service/skipped-runs.ts:50` and `src/cron/service/timer-outcome-finalization.ts:62` thread the repair timeout into both the skipped-run and finalization paths.
- Artifact currently says: the architecture block ends at "Cron Service ───→ SQLite Store ───→ Isolated Agent Sessions" and the Technical Decisions table has no row for failure handling; the Risks section only says "Cron precision may drift under heavy system load" and "Webhook endpoint security requires careful configuration".
- What the code actually does: a failed run can open a repair turn in the owner's conversation before the operator is alerted, and the repair brief itself is a user-visible contract with a silent-reply token.
- Needed change: add the repair stage to the failure sequence and record it as a Technical Decision, since it changes when an operator hears about a failure.

### `src/hooks/` and `src/routing/` are not represented in the architecture

- Status: ADVISORY
- Evidence:
  - `src/hooks/` (66 files) implements internal event hooks: `hooks.ts`, `loader.ts`, `internal-hooks.ts`, `configured.ts`, `gmail-watcher.ts`, `install.ts`, `installs.ts`, `hooks-status.ts`.
  - `src/routing/` (22 files) implements session and route resolution: `resolve-route.ts`, `bindings.ts`, `session-key.ts`, `route-binding-index.ts`, `account-lookup.ts`.
  - `docs/automation/hooks.md` and `docs/automation/index.md` document both as separate operator surfaces.
- Artifact currently says: nothing about either directory; the architecture block only covers cron, webhooks, and flows.
- What the code actually does: `src/hooks/` is an operator-visible internal-hook subsystem with its own CLI and config, and `src/routing/` owns the route and session resolution that decides which agent a delivery targets. A reader would have no map of either.
- Needed change: add both to the architecture, and decide whether they are in scope for this feature or need an explicit out-of-scope pointer.

### The job-persistence decision is now shared-state SQLite with worker isolation

- Status: ADVISORY
- Evidence:
  - `src/cron/store.ts:1-30` loads and saves through the shared OpenClaw state database (`runOpenClawStateWriteTransaction`, `runOpenClawStateWorkerOperation`) rather than a dedicated cron store.
  - `src/cron/store/schema.ts:15-50` defines `CRON_JOB_READ_COLUMNS` against the `cron_jobs` table plus `cron_job_scratch` and `operator_approval_standing_grant*` tables.
  - `src/cron/store/load.worker.ts`, `src/cron/store/save.worker.ts`, and `src/cron/store/read-only.worker.ts` run the store operations in workers.
- Artifact currently says: "Job persistence | SQLite via Kysely | Consistent with project-wide storage convention" and the diagram labels the box "SQLite Store (cron jobs, schedules)".
- What the code actually does: jobs live in the shared state database, not a cron-owned store, and reads and writes are dispatched to workers, including a dedicated read-only worker path. The Kysely choice is unchanged.
- Needed change: clarify that cron jobs are rows in the shared state database and that store I/O runs in workers, so a reader does not expect a cron-owned SQLite file.
