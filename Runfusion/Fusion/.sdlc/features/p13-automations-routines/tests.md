---
title: "Scheduled Automations & Routines"
status: done
---

# Test Plan: Scheduled Automations & Routines

## Scope

This plan covers the shipped behaviour of automations and routines: the domain types and presets, the store contracts, the engine schedulers and runners, the dashboard HTTP routes, and the React surfaces for the Automations view.

Out of scope: the task lifecycle a create-task step feeds into, the external signal connectors, the knowledge graph and memory subsystems, and the plugin management endpoints that share the same route registrar.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | The preset map holds every schedule type except custom, and each value is a valid 5-field cron expression | `AUTOMATION_PRESETS` | Ten presets, each mapping to the expected cron expression, and no `custom` key |
| TC-2 | The schedule type union covers the preset keys plus custom | `ScheduleType` | Every non-custom preset is a valid schedule type, and `custom` is a schedule type without a preset |
| TC-3 | The selectable tool list is unique and holds the builtin coding tools | `AUTOMATION_SELECTABLE_TOOLS` | The seven named tools with no duplicate |
| TC-4 | The run history cap is a positive integer | `MAX_RUN_HISTORY` | 50 |
| TC-5 | The domain types accept every documented field combination | `ScheduledTaskCreateInput`, `AutomationStep`, `AutomationRunResult`, `AutomationStepResult`, `ScheduledTask` | Each type accepts the documented fields, including an explicit empty `allowedTools` array |
| TC-6 | The preset cron expressions land on the expected dates | Each preset expression over the next seven runs | The weekdays preset never lands on a weekend, the monthly preset lands on day one, the 15-minute and 2-hour presets advance by their interval, and every preset produces a future time |
| TC-7 | A routine step with a thinking level is forwarded to the AI executor and an omitted level stays unset | A routine with an `ai-prompt` step | The executor receives the explicit level, and an omitted level is passed as undefined |
| TC-8 | A create-task step maps its thinking level onto the spawned task | A routine and a schedule with a `create-task` step | The explicit level reaches the task input and an omitted level stays undefined |
| TC-9 | A create-task step that names no column sends no column | A routine and a schedule with a `create-task` step | The task input carries no column so the workflow intake resolves it, while an explicit column is honoured |
| TC-10 | The dashboard client builds the automation and routine URLs with the requested scope | A client call for a global and a project scope | The URLs carry `/api/automations` and `/api/routines` with the matching `scope` and `projectId` |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-11 | The automation routes list, create, read, update, delete, toggle, and reorder | A dashboard app with an automation store | Each route answers with the stored automation, and a create answers 201 |
| TC-12 | The automation route rejects invalid input | A dashboard app with an automation store | A missing name, a missing command, an invalid schedule type, a missing custom cron, an invalid cron, an unknown allowed tool, and an invalid thinking level all answer 400 |
| TC-13 | The manual automation run executes steps and records the result | A dashboard app with an automation store and a live run registry | The response carries the schedule, the result, and the live run id, and the per-step results are recorded |
| TC-14 | The manual run streams buffered live events and a terminal error for an unknown run | A dashboard app with a live run registry | A completed run replays its buffered events, and an unknown run id produces a terminal error event |
| TC-15 | The routine routes list, create, read, update, delete, trigger, and read runs | A dashboard app with a routine store and a routine runner | Each route answers with the stored routine, and a create answers 201 |
| TC-16 | The routine route rejects invalid input | A dashboard app with a routine store | A missing name, a missing trigger, an invalid trigger type, a missing or invalid cron, a short webhook secret, an invalid catch-up policy, an invalid execution policy, and an invalid thinking level all answer 400 |
| TC-17 | The webhook route authenticates the caller | A dashboard app with a webhook-triggered routine | A valid signature runs the routine, a missing or wrong signature answers 401, and a routine without a secret answers 401 |
| TC-18 | The scope-aware routes keep the lanes apart | A dashboard app with both a global and a project store | A wrong-scope read answers 404, a wrong-scope write answers 404, a project read never returns a global entity, and a project mutation never reaches the global lane |
| TC-19 | The store-unavailable paths answer 503 | A dashboard app without a resolvable store | A project-scoped read answers 503, while an omitted or global read falls back to an empty array |
| TC-20 | The cron runner polls, claims, and executes due automations | A cron runner with a store and an automation store | A due schedule is claimed and executed, a lost claim is skipped, and a schedule with no next run time is neither claimed nor executed |
| TC-21 | The cron runner does not run the same due window twice across two runners | Two cron runners sharing one store | The due window executes once for a legacy command, once for a step schedule, and once for an in-process intercept |
| TC-22 | The cron runner executes multi-step automations | A schedule with several steps | The steps run in order, a failure stops the sequence unless `continueOnFailure` is set, and the per-step timeout overrides the schedule timeout |
| TC-23 | The cron runner resolves the model for an AI prompt step | A schedule with an AI prompt step | The step override wins, then the execution lane, then the settings default, and the allowed tool list and thinking level are forwarded |
| TC-24 | The cron runner honours the poll interval floor and the pause settings | A cron runner with a short poll interval and a paused store | The poll interval is clamped to 10 seconds, and a paused store or engine produces no execution |
| TC-25 | The routine runner executes a routine and persists the outcome | A routine runner with a store, a heartbeat monitor, and a routine store | The heartbeat runs with the routine source and trigger detail, the run state is persisted, and the in-flight map is cleared |
| TC-26 | The routine runner applies the concurrency policies | A routine runner with an in-flight execution | A parallel routine runs again, a queue routine waits, and a reject routine returns a failed result |
| TC-27 | The routine runner applies the catch-up policy | A routine with a missed occurrence | A run-one routine runs once for the missed interval, a run routine runs for each missed interval, and a skip routine runs only for the current occurrence |
| TC-28 | The routine scheduler polls the right lane and isolates failures | A routine scheduler with both a project and a central store | The central routine is claimed and completed once, a due routine is processed in order, and a failing routine does not stop the loop |
| TC-29 | The routine scheduler verifies the webhook signature | A routine scheduler with a configured secret | A valid signature is accepted, and a wrong or missing signature is refused |
| TC-30 | The routine command runs in the sandbox and is audited | A routine runner with a task store | The run audit holds the sandbox prepare and sandbox run rows, and a failure produces a sandbox failure row |
| TC-31 | The backup routine is reconciled and its outcome is surfaced | A backup settings surface with a global routine | The routine keeps its next run when the cron is unchanged, and the surface shows the last run result |
| TC-32 | The Automations view lists, edits, runs, toggles, and deletes | A dashboard app with the Automations view | The view reloads on a scope change, a run shows inline output, a delete asks for confirmation, and a toggle calls the update route |
| TC-33 | The Automations view reconciles a successful run that ends with a stream error | A dashboard app with a failed stream on a successful run | The card shows the complete state and never the failed state |
| TC-34 | The routine editor builds the trigger and the scope for each trigger type | The routine editor with the cron, webhook, API, and manual trigger modes | Each mode sends the matching trigger, the scope toggle is submitted, and the name and cron fields are validated |
| TC-35 | The step editor adds, edits, deletes, and reorders steps | The step editor with an existing step list | A step is added for each of the three types, a step moves up and down, the first and last move buttons are disabled, and the step count is shown |
| TC-36 | The step editor stores the tool allowlist and the thinking level | The step editor with an advanced AI prompt step | All tools selected stores an undefined allowlist, a narrowed selection stores that list, and a cleared selection stores an empty list |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-37 | A custom schedule type is created without a cron expression | The request answers 400 and no automation is stored |
| TC-38 | A reorder names a step id that does not exist | The request answers 400 and the stored steps are unchanged |
| TC-39 | A reorder names a different number of step ids than the stored steps | The request answers 400 with a step ID count mismatch |
| TC-40 | An update empties the name or leaves neither a command nor steps | The request answers 400 and the stored automation is unchanged |
| TC-41 | A run of a routine that is disabled is requested | The request answers 400 and no run is recorded |
| TC-42 | A webhook call reaches a routine that is not webhook-triggered | The request answers 400 |
| TC-43 | A webhook routine carries no secret | The request answers 401 and no run is recorded |
| TC-44 | An unknown step type is executed | The step result reports an unknown step type failure and the run is recorded as failed |
| TC-45 | A command step carries no command, an AI step carries no prompt, or a create-task step carries no description | The step result reports the missing field and the sequence stops unless `continueOnFailure` is set |
| TC-46 | An AI prompt step runs with no executor configured | The step result reports that AI execution is not configured |
| TC-47 | A command times out | The run result reports a failure naming the timeout and the partial output is kept |
| TC-48 | A run produces more output than the stored cap | The stored output is truncated and marked as truncated |
| TC-49 | A run history exceeds the cap | The oldest entries are dropped and the newest are kept |
| TC-50 | A recordRun call fails after a successful execution | The tick continues to the next schedule and the failure is logged |
| TC-51 | A post-run callback throws | The callback error is logged and the returned run result is unchanged |
| TC-52 | The step identifier generator is unavailable | A step is still added with a fallback identifier |
| TC-53 | A run is started and the stream attaches with no run id | The stream waits for the next run of that entity and does not replay an unrelated finished run |

## Test Infrastructure

- The dashboard route tests mount the router under `/api` with an Express app and use in-memory store doubles.
- The engine scheduler and runner tests use in-memory store doubles and an injected AI prompt executor, so no shell command and no model call reaches a network.
- The React component tests use a testing-library render with mocked fetch, so no dashboard server is needed.
- The sandbox audit tests use a fake run auditor and a fake sandbox backend.
- The core domain tests are pure type and value assertions with no database.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-11, TC-15, TC-31 |
| FR-2 | TC-1, TC-2, TC-6, TC-34 |
| FR-3 | TC-12, TC-16, TC-37, TC-40 |
| FR-4 | TC-1, TC-6, TC-11 |
| FR-5 | TC-22, TC-35, TC-44, TC-45 |
| FR-6 | TC-7, TC-10, TC-23, TC-36 |
| FR-7 | TC-8, TC-9, TC-23, TC-25 |
| FR-8 | TC-13, TC-20 |
| FR-9 | TC-11, TC-34 |
| FR-10 | TC-38, TC-39 |
| FR-11 | TC-15, TC-34 |
| FR-12 | TC-16, TC-34 |
| FR-13 | TC-27 |
| FR-14 | TC-26 |
| FR-15 | TC-13, TC-15, TC-25 |
| FR-16 | TC-17, TC-42, TC-43 |
| FR-17 | TC-20, TC-24, TC-28 |
| FR-18 | TC-20, TC-21, TC-28 |
| FR-19 | TC-14, TC-32, TC-33, TC-53 |
| FR-20 | TC-18, TC-19, TC-32 |
| FR-21 | TC-31 |
| FR-22 | TC-32, TC-33, TC-34, TC-35 |
| NFR-1 | TC-16, TC-17, TC-43 |
| NFR-2 | TC-30 |
| NFR-3 | TC-18 |
| NFR-4 | TC-22, TC-47 |
| NFR-5 | TC-20, TC-21 |
| NFR-6 | TC-48 |
| NFR-7 | TC-49 |
| NFR-8 | TC-28, TC-50 |
| NFR-9 | TC-14, TC-53 |
| NFR-10 | TC-24, TC-28 |
| NFR-11 | TC-50, TC-51 |
| NFR-12 | TC-31 |

## Key Test Files

| File | Covers |
|---|---|
| `packages/core/src/__tests__/automation.test.ts` | The presets, the schedule type union, the selectable tools, the run history cap, the domain type contracts, and the preset cron edge cases |
| `packages/core/src/__tests__/backup-schedule-status.test.ts` | The backup routine sync planning, the reconciliation, and the surfaced schedule status |
| `packages/engine/src/__tests__/cron-runner.test.ts` | The cron runner start and stop, the poll tick, the due-window claim, the multi-step execution, the AI prompt and create-task steps, the scoped lane polling, and the output truncation |
| `packages/engine/src/__tests__/routine-runner.test.ts` | The routine execution, the heartbeat contract, the concurrency policies, the catch-up behaviour, and the manual and cron backup parity |
| `packages/engine/src/__tests__/routine-scheduler.test.ts` | The scheduler tick, the central global routine claim, the scoped lane polling, the pause regressions, the lane isolation, and the webhook signature checks |
| `packages/engine/src/__tests__/routine-runner-sandbox-audit.test.ts` | The sandbox prepare, run, and failure audit events for command routines and command steps |
| `packages/engine/src/__tests__/sandbox-wiring.test.ts` | The sandbox wiring for the routine runner |
| `packages/engine/src/__tests__/sandbox-wiring-audit.test.ts` | The sandbox wiring audit for the routine runner |
| `packages/dashboard/src/__tests__/routes-automation.test.ts` | The automation and routine HTTP routes, the validation errors, the manual run, the live stream, the webhook verification, and the scope isolation |
| `packages/dashboard/app/__tests__/api-settings.test.ts` | The automation and routine request URLs and their scope parameters |
| `packages/dashboard/app/components/__tests__/ScheduledTasksModal.test.tsx` | The Automations view presentation, the scope controls, the run flow, the live output reconciliation, and the delete and toggle actions |
| `packages/dashboard/app/components/__tests__/ScheduleForm.test.tsx` | The automation form create, edit, validation, cron auto-fill, submission, cancel, scope toggle, multi-step, and simple-mode cases |
| `packages/dashboard/app/components/__tests__/ScheduleStepsEditor.test.tsx` | The step addition, deletion, reordering, editing state, validation, empty state, tool selection, and model selection |
| `packages/dashboard/app/components/__tests__/ScheduleCard.test.tsx` | The schedule card rendering, the last run badge, the action buttons, and the run history |
| `packages/dashboard/app/components/__tests__/RoutineEditor.test.tsx` | The routine editor create, edit, trigger modes, scope selector, validation, submission, and cancel cases |
| `packages/dashboard/app/components/__tests__/RoutineCard.test.tsx` | The routine card rendering, the policy badges, the live output states, the action buttons, and the run history |
