---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-10-19

### Webhook receivers are now core Gateway HTTP hooks, not an extension plugin

- Status: BLOCKING
- Evidence:
  - `src/plugins/config-state.ts:30-36` lists `"webhooks"` in `RETIRED_PLUGIN_IDS`, so no `extensions/webhooks/` plugin can load.
  - `src/gateway/hooks.ts:36` sets `DEFAULT_HOOKS_PATH = "/hooks"` and `src/gateway/hooks.ts:90` resolves the path from `cfg.hooks?.path`.
  - `src/gateway/server/hooks-request-handler.ts` and `src/gateway/server/hooks-event-dispatch.ts` implement the request handling.
  - `src/config/types.hooks.ts` defines the `HooksConfig` shape consumed by the Gateway, and `docs/automation/cron-jobs/webhooks.md` documents `POST /hooks/wake`, `POST /hooks/agent`, and `POST /hooks/<name>`.
  - `ls extensions/webhooks` returns "No such file or directory".
- Artifact currently says: "OpenClaw provides a cron-based job scheduling system, a webhook receiver for external triggers, a workflow/flow engine, and auto-reply capabilities." and "FR-3 | Must | The system shall support webhook receivers for external HTTP triggers".
- What the code actually does: inbound webhooks are a core Gateway subsystem under the top-level `hooks` config block (`hooks.enabled`, `hooks.token`, `hooks.path`, `hooks.allowedAgentIds`, `hooks.allowRequestSessionKey`, `hooks.mappings`), served by `src/gateway/hooks.ts` and `src/gateway/server/hooks-request-handler.ts`. The `webhooks` plugin id is explicitly retired, so a reader following the artifact would look for an extension that can no longer load and would miss that the feature is gated by a core config block plus a bearer token.
- Needed change: state that inbound webhooks are core Gateway HTTP hooks gated by the `hooks` config block, and that the `webhooks` plugin id is retired.

### The flow engine now lives in a separately installed plugin, not in `src/flows/`

- Status: BLOCKING
- Evidence:
  - `src/flows/` contains only doctor health checks and setup flows (`doctor-core-checks.ts`, `doctor-health.ts`, `doctor-repair-flow.ts`, `channel-setup.ts`, `provider-flow.ts`, `model-picker.ts`, `search-setup.ts`, `memory-setup.ts`); there is no flow-execution engine left there.
  - `extensions/lobster/src/lobster-runner.ts` and `extensions/lobster/src/lobster-tool.ts` implement the multi-step pipeline runner, and `docs/tools/lobster.md:237` documents "Workflow files (.lobster)".
  - `docs/automation/index.md:79-81` states: "Lobster runs local pipelines with resumable approvals. The shared Tasks ledger, TaskFlow orchestration API, and TaskFlow Webhooks plugin have been removed."
  - `docs/plugins/sdk-migration/removed-surfaces.md:481` records the same removal.
- Artifact currently says: "FR-4 | Must | The system shall provide a flow/workflow engine for multi-step automations" and the Overview lists "a workflow/flow engine" as a first-class capability.
- What the code actually does: there is no core multi-step flow engine. The Tasks ledger and TaskFlow orchestration API were removed, `src/flows/` is doctor and setup code only, and multi-step pipelines now run through the separately installed `@openclaw/lobster` plugin (`extensions/lobster/`). A reader would believe the shipped product has a core workflow engine and would look for it in `src/flows/`.
- Needed change: either narrow FR-4 to the doctor/setup flows that remain in `src/flows/`, or restate it as the optional Lobster plugin, and record the TaskFlow removal.

### The "automation repair" failure path is missing from FR-7

- Status: BLOCKING
- Evidence:
  - `CHANGELOG/2026.10.5.md:23`: "**Automation repair:** let a failing automation's owner conversation repair it before alerting, give a second repair turn when the error changes, and post a clear warning when a repair turn times out. (#161007, #162702, #162772)".
  - `src/cron/service/failure-repair-brief.ts:1` documents "The repair request the scheduler posts into a failing automation's owner conversation" and builds a brief that instructs the agent to diagnose and either fix the workspace or stay silent.
  - `src/cron/service/notification-dispatch.ts:108-118` dispatches the repair request through `state.deps.runCronFailureRepair` before any alert is sent, and falls back to the alert only if the repair request fails.
  - `src/cron/service/failure-alerts.ts:481` passes `failureRepairTimeoutMs` into the repair path.
- Artifact currently says: "FR-7 | Must | The system shall support failure notification and retry for failed scheduled jobs".
- What the code actually does: on repeated failure the scheduler first posts a repair brief into the job owner's own conversation and withholds the failure alert while that repair turn is outstanding. The alert only fires when the repair path is unavailable or the repair does not resolve the failure. A reader of the artifact would expect a straight notify-and-retry flow and would not know that a repair turn can preempt the alert.
- Needed change: extend FR-7 to cover the owner-conversation repair turn that runs before the alert, including the second-repair-on-changed-error behavior and the repair-timeout warning.

### FR-5 and FR-8 name capabilities the artifact never covers

- Status: ADVISORY
- Evidence:
  - FR-5 ("auto-reply rules for common message patterns") maps to `src/auto-reply/` (114 files, including `heartbeat.ts`, `heartbeat-filter.ts`, `group-activation.ts`, `command-detection.ts`).
  - FR-8 ("heartbeat-style recurring jobs in addition to cron") maps to `src/cron/heartbeat-monitor.ts`, which projects heartbeat config into system-owned cron monitor jobs, and `src/auto-reply/heartbeat.ts`, which owns the heartbeat prompt and interval defaults.
  - `docs/automation/index.md:66-74` documents heartbeat as "a system-owned monitor automation" and "the system-owned ambient monitor automation".
- Artifact currently says: "FR-5 | Should | The system shall support auto-reply rules for common message patterns" and "FR-8 | Should | The system shall support heartbeat-style recurring jobs in addition to cron".
- What the code actually does: heartbeat is implemented as a system-owned cron monitor job rather than a separate scheduler, and the auto-reply surface is a large subsystem with its own trigger, filter, and heartbeat machinery. The requirement wording is not contradicted, but the artifact does not tell a reader which module owns either capability, and neither FR-5 nor FR-8 has a row in the test coverage matrix.
- Needed change: name the owning modules for FR-5 and FR-8, and add coverage-matrix rows for both.

### FR-10 (job history and status) is under-specified relative to the code

- Status: ADVISORY
- Evidence:
  - `src/cron/run-history.ts` and `src/cron/service/run-history.ts` implement run history reads.
  - `src/cron/service/run-queue.ts`, `src/cron/service/run-receipts.ts`, and `src/cron/store/run-receipt-store.ts` implement a durable run queue and receipt store.
  - `src/cron/service/list-page-types.ts` and `src/cron/service/list-page-sort.ts` implement paginated job listing with sort guards.
  - `src/cron/run-diagnostics.ts` and `src/cron/service/run-recovery.ts` implement per-run diagnostics and recovery.
- Artifact currently says: "FR-10 | Should | The system shall expose job history and status for operator visibility".
- What the code actually does: history and status are backed by a durable receipt store, a run queue, paginated and sortable listings, per-run diagnostics, and a recovery path. The requirement is satisfied but the artifact undersells the surface, and FR-10 has no coverage-matrix row.
- Needed change: state that history and status are served from the durable run-receipt store with paginated listing, and add a coverage-matrix row.

### "Cron expression" is no longer the only schedule form

- Status: ADVISORY
- Evidence:
  - `packages/gateway-protocol/src/schema/cron.ts:138-180` defines `CronScheduleSchema` as a union of `event`, `at`, `every`, `cron`, `on-exit`, and `stream` variants, not a bare cron string.
  - `src/cron/source-schedule.ts` and `src/cron/stream-schedule.ts` implement the non-cron schedule sources.
- Artifact currently says: "FR-1 | Must | The system shall support cron-based job scheduling with standard cron expressions" and "Acceptance Criteria: **FR-1**: A job scheduled with `0 9 * * *` runs at 9 AM daily".
- What the code actually does: cron expressions are one of six schedule kinds; one-shot, interval, event, on-exit, and stream schedules are equally first-class. The acceptance criterion still holds, but the artifact's framing implies cron is the scheduling model rather than one option.
- Needed change: note that cron is one schedule kind among several, and keep the existing acceptance criterion as one example.

### The artifact does not mention internal event hooks (`src/hooks/`)

- Status: ADVISORY
- Evidence:
  - `src/hooks/` contains 66 files implementing the internal hook subsystem: `src/hooks/hooks.ts`, `src/hooks/loader.ts`, `src/hooks/internal-hooks.ts`, `src/hooks/configured.ts`, `src/hooks/gmail-watcher.ts`, `src/hooks/install.ts`.
  - `docs/automation/hooks.md` documents `openclaw hooks list`, `openclaw hooks info`, `openclaw hooks enable`, and the `HOOK.md` handler model.
  - `docs/automation/hooks.md` explicitly separates "Internal hooks" from "Webhooks" ("Let another service start work through an HTTP request | Webhooks").
- Artifact currently says: nothing. The artifact's Overview lists cron, webhooks, flows, and auto-reply, and no requirement or acceptance criterion mentions internal event hooks.
- What the code actually does: `src/hooks/` is a distinct, operator-visible subsystem with its own CLI, config, install records, and bundled hook packs. A reader of the artifact would not know it exists, and would conflate internal hooks with the HTTP webhook receivers that FR-3 covers.
- Needed change: add a requirement and data model for internal event hooks, or explicitly scope them out and point at where they are documented. Note that this subsystem is a plausible candidate for its own feature directory, since nothing in FEAT-p1..FEAT-p12 covers it.

## Sync drift: 2026-11-16

### Previously recorded drifts still hold

- Status: BLOCKING.
- The retired webhook plugin, the move of multi-step flows to Lobster, the failure-repair stage in FR-7, the missing owner modules for FR-5, FR-8, and FR-10, the six schedule kinds behind FR-1, and the undocumented internal hook subsystem all remain accurate.
- The code_index paths in `.sdlc/sync-meta.yml` are `src/cron/`, `src/flows/`, `src/gateway/hooks.ts`, and `extensions/lobster/`, which confirms the webhook and flow architecture described in the artifact is not the shipped one.

### FR-8 no longer describes the shipped code

- Status: BLOCKING.
- Evidence:
  - `src/cron/heartbeat-monitor.ts` no longer exists and no heartbeat-monitor file remains under `src/cron/`.
  - `docs/automation/cron-jobs/schedules.md:40-45` documents a heartbeat task migration that converts heartbeat configuration and system-owned monitor jobs into ordinary editable `agentTurn` jobs with `openclaw doctor --fix`.
  - `docs/automation/cron-jobs/schedules.md:63` states "no separate heartbeat runner is involved".
  - `docs/automation/index.md:95-97` states existing heartbeat monitors migrate into ordinary editable jobs and setup provisions one proactive check.
  - `src/cron/default-proactive-job.worker.ts` and `src/cron/proactive-job-receipt.kernel.ts` implement provisioning of the default proactive check.
- Artifact currently says: "FR-8 | Should | The system shall support heartbeat-style recurring jobs in addition to cron".
- What the code actually does: heartbeat monitoring has been folded into ordinary cron jobs and there is no separate heartbeat scheduler.
- Needed change: retire FR-8 or restate it as a migration path into ordinary automation jobs, and record that no separate heartbeat runner remains.

### Execution-window behavior is implemented but not required

- Status: ADVISORY.
- Evidence:
  - `CronJobSchema` in `packages/gateway-protocol/src/schema/cron.ts` carries `activeHours` and `idleOnly` job-level fields.
  - `src/cron/active-hours.ts` and `src/cron/active-jobs.ts` implement the quiet-hours gate and active-job management.
  - `src/cron/active-hours.test.ts` covers the window logic.
  - `docs/automation/index.md:48-52` tells readers to use `activeHours` and `idleOnly` when a check should respect quiet hours and foreground work.
- Artifact currently says: no requirement mentions execution windows, quiet hours, or idle-only gating.
- What the code actually does: jobs can be restricted to an active-hours window and gated on agent idleness.
- Needed change: add a functional requirement for job-level execution windows and idle-only gating.

## Sync drift: 2026-11-23

Fresh analysis of `src/cron/`, `src/flows/`, `src/gateway/hooks.ts`, and `extensions/lobster/` confirms the recorded drift still stands. No new discrepancy was found beyond the items below.

### FR-3 still names a retired webhook plugin

- Status: BLOCKING
- Evidence:
  - `src/plugins/config-state.ts:31-34` lists `"webhooks"` in `RETIRED_PLUGIN_IDS`; `isRetiredPluginId` at line 44 rejects it.
  - `extensions/webhooks/` does not exist in this checkout.
  - `src/gateway/hooks.ts:41` sets `DEFAULT_HOOKS_PATH = "/hooks"`; lines 93-94 return `null` unless `cfg.hooks?.enabled === true`.
  - `src/gateway/server/hooks-request-handler.ts` and `src/gateway/server/hooks-event-dispatch.ts` carry the inbound HTTP handling.
- Artifact still says: "FR-3 | Must | The system shall support webhook receivers for external HTTP triggers" with no mention of the core `hooks` config block or the retired plugin id.
- Needed change: restate FR-3 as core Gateway HTTP hooks gated by `hooks.enabled` and a bearer token, and record that the `webhooks` plugin id is retired.

### FR-4 still claims a core multi-step workflow engine

- Status: BLOCKING
- Evidence:
  - `src/flows/` holds 144 files, all doctor and setup code; no flow-execution engine remains there.
  - `extensions/lobster/src/lobster-runner.ts` implements the multi-step pipeline runtime; `docs/tools/lobster.md:69` calls it "The separately installed official `@openclaw/lobster` plugin".
  - `docs/automation/index.md:75` records removal of "The shared Tasks ledger, TaskFlow orchestration API, and TaskFlow Webhooks plugin".
- Artifact still says: "FR-4 | Must | The system shall provide a flow/workflow engine for multi-step automations" and the Overview lists a workflow/flow engine as a first-class capability.
- Needed change: narrow FR-4 to the doctor/setup flows in `src/flows/`, or restate it as the optional Lobster plugin, and record the TaskFlow removal.

### FR-8 still describes a separate heartbeat scheduler

- Status: BLOCKING
- Evidence:
  - `src/cron/heartbeat-monitor.ts` is absent from `src/cron/`.
  - `docs/automation/cron-jobs/schedules.md:63` states "no separate heartbeat runner is involved"; `docs/automation/index.md:97` says existing monitors migrate into ordinary editable jobs.
  - `src/cron/isolated-agent.heartbeat-migration.test.ts` and `src/cron/default-proactive-job.worker.ts` cover migration and default-proactive provisioning.
- Artifact still says: "FR-8 | Should | The system shall support heartbeat-style recurring jobs in addition to cron".
- Needed change: retire FR-8 or restate it as a Doctor-driven migration path into ordinary automation jobs.

### FR-1 still frames cron as the only schedule form

- Status: ADVISORY
- Evidence:
  - `packages/gateway-protocol/src/schema/cron.ts:52-58` defines the schedule kinds as `event`, `at`, `every`, `cron`, `on-exit`, and `stream`.
- Artifact still says: "FR-1 | Must | The system shall support cron-based job scheduling with standard cron expressions".
- Needed change: note that cron is one schedule kind among six, and keep the existing acceptance criterion as one example.
