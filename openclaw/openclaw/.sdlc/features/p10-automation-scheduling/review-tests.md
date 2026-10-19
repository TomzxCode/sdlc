---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-10-19

### Six of the listed test files no longer exist

- Status: BLOCKING
- Evidence:
  - `extensions/webhooks/src/http.test.ts` (TC-8), `extensions/webhooks/src/config.test.ts` (TC-9), and `extensions/webhooks/index.test.ts` (TC-16): `extensions/webhooks/` does not exist; `src/plugins/config-state.ts:30-36` retires the `webhooks` plugin id. The corresponding coverage now lives in `src/gateway/hooks.test.ts`, `src/gateway/hooks-mapping.test.ts`, `src/gateway/server/hooks-request-handler.fanout.test.ts`, `src/gateway/server/hooks.agent-trust.test.ts`, `src/gateway/server/hooks.early-failure.test.ts`, `src/gateway/server/hooks.terminal-target.test.ts`, and `src/gateway/server/hooks.wake-admission.test.ts`.
  - `src/cron/pacing.test.ts` (TC-5): the file is gone. `src/cron/pacing.ts` still exists and is covered by `src/cron/service/timer.pacing.test.ts` and `src/cron/service/ops.pacing.test.ts`.
  - `src/cron/heartbeat-policy.test.ts` (TC-17): the file is gone. Heartbeat policy is now covered by `src/cron/heartbeat-monitor.test.ts` (desired-state planning for the system-owned monitor), `src/cron/service.heartbeat-busy-poll.test.ts`, `src/cron/service.heartbeat-payload.test.ts`, and `src/cron/service.startup-heartbeat.test.ts`.
  - `src/cron/service.prevents-duplicate-timers.test.ts` (TC-20): the file is gone. The nearest surviving coverage is `src/cron/service.armtimer-tight-loop.test.ts` ("joins a scheduled tick waiting for admission without reopening suspension") and `src/cron/cron-state-contracts.e2e.test.ts:151` ("deduplicates isolated scheduler execution and persisted run history across reload").
  - `src/cron/service.store-load-invalid-main-job.test.ts` (TC-22): the file is gone. Invalid main-job handling is now covered by `src/cron/service.jobs.test.ts:345` (`invalidMainJob` fixture, exercised at line 368) and `src/cron/service.stream-validation.test.ts:326` ("skips invalid main jobs with agentTurn payloads loaded from disk").
- Artifact currently says: TC-5, TC-8, TC-9, TC-16, TC-17, TC-20, and TC-22 all cite these paths.
- What the code actually does: the suites moved or were renamed as the subsystem was reworked. A reader following the coverage map would try to open six files that are not there and would conclude the corresponding behavior is untested when it is in fact covered elsewhere.
- Needed change: repoint TC-5, TC-8, TC-9, TC-16, TC-17, TC-20, and TC-22 at the surviving files, and rename the TC-13 glob (see next finding).

### The TC-13 glob no longer covers the isolated-agent suites

- Status: BLOCKING
- Evidence:
  - The artifact cites `src/cron/isolated-agent.*.test.ts`. Eight such files still exist at the `src/cron/` root (`isolated-agent.auth-continuity.integration.test.ts`, `isolated-agent.auth-profile-propagation.test.ts`, `isolated-agent.delivery-awareness.test.ts`, `isolated-agent.helpers.test.ts`, `isolated-agent.hook-content-wrapping.test.ts`, `isolated-agent.model-formatting.test.ts`, `isolated-agent.model-preflight.test.ts`, `isolated-agent.session-identity.test.ts`).
  - The bulk of the isolated-agent coverage has moved into the `src/cron/isolated-agent/` directory (100 files), including `run.sandbox-admission.test.ts`, `run.fallback-policy.test.ts`, `run.model-policy-config-preserved.test.ts`, `run.session-key-isolation.test.ts`, `run.tools-allow.test.ts`, `model-preflight.runtime.test.ts`, `model-preflight.runtime.transport.test.ts`, `session.preparation.test.ts`, `session.preparation.storage-env.test.ts`, `run.diagnostic-events.test.ts`, `run.terminal-error-identity.test.ts`, `delivery-dispatch.double-announce.test.ts`, and `delivery-target-context.sqlite.test.ts`.
  - The directory also holds the production modules, so the directory name now collides with the old file glob.
- Artifact currently says: "| TC-13 | Cron isolated agent runs | src/cron/isolated-agent.*.test.ts | Isolated sessions start correctly |".
- What the code actually does: the glob still matches the eight root-level files but silently misses the entire `src/cron/isolated-agent/` suite tree, which is where the substantive isolated-session behavior (sandbox admission, model preflight, fallback policy, session isolation, tool allowlists, delivery dispatch) is now tested. The artifact's stated coverage for FR-6 is therefore much narrower than reality.
- Needed change: cite both the root-level glob and the `src/cron/isolated-agent/` directory, and enumerate the behaviors the directory now covers.

### The failure-repair path has no test row

- Status: BLOCKING
- Evidence:
  - `src/cron/service.failure-repair.test.ts` (6 cases) exercises the repair-before-alert behavior, including the second repair turn on a changed error and the repair-timeout warning.
  - `src/cron/service/failure-alert.test.ts` (7 cases) and `src/cron/service/failure-alerts.outcome.test.ts`, `src/cron/service/failure-alerts.persistence.test.ts`, and `src/cron/service/failure-alerts.account-routing.test.ts` cover the alert side.
  - `src/cron/service/failure-repair-brief.ts` and `src/cron/service/notification-dispatch.ts:108-118` are the implementation under test.
  - `CHANGELOG/2026.10.5.md:23` records the shipped behavior.
- Artifact currently says: "| TC-12 | Cron failure alerts | src/cron/service.failure-alert.test.ts | Alerts on job failure |" and the FR-7 coverage row maps only to TC-4, TC-12, and TC-14.
- What the code actually does: the failure path has two distinct stages, a repair turn in the owner's conversation and the operator alert, and only the alert stage is covered by the artifact. A reader would conclude the repair behavior is untested and would not know it exists.
- Needed change: add a row for `src/cron/service.failure-repair.test.ts` and map FR-7 to it.

### Large uncovered areas in `src/cron/` are absent from the plan

- Status: ADVISORY
- Evidence:
  - The `src/cron/service/` subtree holds 200+ files with dedicated suites, including `run-queue.test.ts`, `run-recovery.test.ts`, `run-receipts.test.ts`, `timer.test.ts`, `timer.pacing.test.ts`, `timer.regression.test.ts`, `scheduler-actor.test-support.ts`, `ops.test.ts`, `ops.pacing.test.ts`, `ops.run-admission.test.ts`, `store.test.ts`, `startup-run-repair.test.ts`, `auto-disable.ts` and `failure-alerts.*.test.ts`.
  - `src/cron/store/` holds 40+ worker and codec suites, including `run-queue.worker.test.ts`, `run-receipt-store.test.ts`, `run-receipt-retention.test.ts`, `run-history.kernel.ts`, `quarantine.test.ts`, and `readonly-worker.test.ts`.
  - `src/cron/trigger-script.*.test.ts` covers the script-payload trigger runtime, and `src/cron/inference-binding.*.test.ts` covers inference binding.
  - `src/cron/scratch-store.test.ts`, `src/cron/session-reaper.test.ts`, `src/cron/maintenance.test.ts`, and `src/cron/command-runner.test.ts` cover the scratch store, session reaper, maintenance, and command runner.
  - `src/cron/cron-protocol-conformance.test.ts` and `src/cron/cron-state-contracts.e2e.test.ts` are cross-cutting conformance suites.
- Artifact currently says: the plan covers 22 test cases across `src/cron/`, `src/flows/`, and `extensions/webhooks/`.
- What the code actually does: the cron subsystem is roughly 563 files with a much larger test surface, and several of the plan's most load-bearing behaviors (run queueing, run recovery, receipt retention, state quarantine, startup repair) have no row at all. The plan reads as complete coverage of cron when it is a thin slice.
- Needed change: extend the plan to cover the run-queue, run-recovery, receipt, quarantine, and startup-repair areas, and note the conformance suites.

### No coverage rows for FR-5, FR-8, or FR-10

- Status: ADVISORY
- Evidence:
  - FR-5 (auto-reply) maps to `src/auto-reply/`, whose suites include `heartbeat.test.ts`, `heartbeat-filter.test.ts`, `group-thread.test.ts`, `command-detection.runtime-types.ts`, `dispatch.test.ts`, and `reply.triggers.trigger-handling.e2e.test.ts`.
  - FR-8 (heartbeat recurring jobs) maps to `src/cron/heartbeat-monitor.test.ts` and the `src/cron/service.heartbeat-*.test.ts` family.
  - FR-10 (job history and status) maps to `src/cron/run-history.test.ts`, `src/cron/service/run-history.ts`, `src/cron/service/list-page-sort-guards.test.ts`, and `src/cron/run-diagnostics.test.ts`.
- Artifact currently says: the coverage matrix lists FR-1, FR-2, FR-3, FR-4, FR-6, FR-7, and FR-9 only.
- What the code actually does: three requirements have real, test-backed implementations but no row in the matrix, so a reader cannot tell whether they are covered or simply forgotten.
- Needed change: add matrix rows for FR-5, FR-8, and FR-10 pointing at the surviving suites.

### The `src/flows/` doctor row understates the current coverage

- Status: ADVISORY
- Evidence:
  - `src/flows/doctor-core-checks.test.ts` still exists and is the file the artifact cites for TC-15.
  - The directory now also holds `doctor-core-checks.e2e.test.ts`, `doctor-core-checks.runtime.test.ts`, `doctor-core-checks.runtime.bundled.test.ts`, `doctor-health.test.ts`, `doctor-health-contributions.test.ts`, `doctor-health.contribution*` suites, `doctor-repair-flow.test.ts`, `doctor-lint-flow.test.ts`, `channel-setup.test.ts`, `provider-flow.test.ts`, and `bundled-health-checks.test.ts`.
- Artifact currently says: "| TC-15 | Flow engine doctor checks | src/flows/doctor-core-checks.test.ts | Doctor checks run and report |".
- What the code actually does: the file still exists, so the row is not wrong, but it names one of a dozen doctor and setup suites. The label "Flow engine doctor checks" is also a misnomer now that `src/flows/` holds no flow engine.
- Needed change: relabel the row and point it at the broader doctor and setup suite set.
