---
title: "Scheduled Automations & Routines"
status: done
---

# Requirements: Scheduled Automations & Routines

## Overview

Operators need recurring work to run without being asked. This feature covers two related capabilities. An automation is a named schedule that runs a shell command or a list of steps on a cron expression. A routine is the richer form, with a trigger that can be a cron expression, an HMAC-signed webhook, an API call, or a manual signal, plus catch-up and concurrency policies and an assigned agent. Both are stored in a global lane and a project lane, both keep a bounded run history, and both surface live run output to the dashboard. This feature was reverse-engineered from shipped code during sync-sdlc.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Solo developer | Wants recurring commands, prompts, and task creation to run on a schedule without manual intervention |
| Operator / power user | Defines schedules and routines, chooses trigger and policy settings, and reads run history to confirm work happened |
| Maintainer / contributor | Keeps the scheduler, the stores, and the dashboard surface consistent and covered by tests |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let operators create, read, update, and delete automations, each carrying a name, an optional description, a schedule type, a cron expression, either a command or a step list, an enabled flag, an optional timeout, and a global or project scope. |
| FR-2 | Must | The system shall offer the preset schedule types hourly, daily, weekly, monthly, every15Minutes, every30Minutes, every2Hours, every6Hours, every12Hours, and weekdays, plus a custom schedule type whose cron expression the operator supplies, and shall derive the cron expression from the preset when the type is not custom. |
| FR-3 | Must | The system shall reject an automation with an empty name, an automation with neither a command nor steps, an automation with an unrecognised schedule type, and a custom automation whose cron expression does not parse. |
| FR-4 | Must | The system shall compute and store the next run time of an automation from its cron expression in UTC, and shall clear the next run time while the automation is disabled. |
| FR-5 | Must | The system shall support multi-step automations whose steps run in order, where each step is a command step, an AI prompt step, or a create-task step, and shall stop the sequence after a failed step unless that step sets continueOnFailure. |
| FR-6 | Must | The system shall let an AI prompt step name a model provider and model, an optional thinking level, and an allowlist drawn from the selectable coding tools, and shall run the prompt with exactly that tool set. |
| FR-7 | Must | The system shall let a create-task step create a Fusion task carrying a title, a description, an optional target column, an optional model, and an optional thinking level, and shall attribute the new task to the originating schedule or routine. |
| FR-8 | Must | The system shall run an automation on demand and store the run result, including per-step results, in that automation's run history. |
| FR-9 | Must | The system shall let an operator enable or disable an automation in one call, and shall recompute the next run time when the cadence changes or a disabled automation is re-enabled. |
| FR-10 | Must | The system shall let an operator reorder the steps of a multi-step automation, and shall reject a reorder whose step IDs do not match the stored steps exactly. |
| FR-11 | Must | The system shall let operators create, read, update, and delete routines, each carrying a name, an optional description, an assigned agent, a trigger, either a command or a step list, a catch-up policy, an execution policy, an enabled flag, an optional timeout, and a global or project scope. |
| FR-12 | Must | The system shall support the four routine trigger types cron, webhook, api, and manual, and shall validate the cron expression of a cron trigger and the secret of a webhook trigger. |
| FR-13 | Must | The system shall apply the routine catch-up policy, which is run, skip, or run_one, to occurrences the routine missed while it was not running. |
| FR-14 | Must | The system shall apply the routine execution policy, which is parallel, queue, or reject, when a run is requested while another run of the same routine is in progress. |
| FR-15 | Must | The system shall run a routine on demand and expose that routine's run history. |
| FR-16 | Must | The system shall accept an HMAC-signed webhook call for a webhook-triggered routine, and shall refuse the call when the routine carries no secret, the signature header is missing, or the signature does not verify. |
| FR-17 | Must | The system shall execute due automations and due routines on a poll interval, and shall skip execution while the engine is paused or the project is globally paused. |
| FR-18 | Must | The system shall claim a due occurrence in storage before executing it, so that concurrent pollers, overlapping scopes, and separate engine processes do not run the same occurrence twice. |
| FR-19 | Should | The system shall stream live run output to the dashboard over server-sent events, including step boundaries, text deltas, tool activity, and the terminal result, and shall replay the buffered events to a client that attaches after the run started. |
| FR-20 | Should | The system shall keep automations and routines in a global lane and a project lane, and shall isolate reads and writes by the requested scope. |
| FR-21 | Should | The system shall record every automation and routine configuration change as a versioned revision, so an operator can restore an earlier definition of the same entity. |
| FR-22 | Should | The system shall show automations and routines in the dashboard Automations view, with editors for both, a scope control, run controls, and a run history list. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall require a webhook secret of at least 16 characters when a routine is created or updated with a webhook trigger, and shall refuse a webhook call that does not carry a valid signature. |
| NFR-2 | Must | Security | The system shall execute routine commands through a sandboxed backend rather than a bare shell, and shall record the sandbox prepare, run, and failure events in the run audit. |
| NFR-3 | Must | Security | The system shall not let a project-scoped request read or change a global-scoped automation or routine, and shall not let a global-scoped request read or change a project-scoped one. |
| NFR-4 | Must | Reliability | The system shall bound a run that hangs by a timeout, defaulting to 5 minutes, and shall allow a per-step timeout to override the schedule or routine timeout. |
| NFR-5 | Must | Reliability | The system shall treat a due occurrence as claimed before execution so that a second poller observes the claim loss and skips the occurrence. |
| NFR-6 | Must | Performance | The system shall cap the command output buffer at 1 MB and the stored run output at 10 KB, marking truncated output as such. |
| NFR-7 | Must | Performance | The system shall retain at most 50 run history entries per automation and at most 50 per routine, dropping the oldest entries first. |
| NFR-8 | Should | Availability | The system shall isolate failures so that one failing automation or routine does not stop the rest of the poll cycle. |
| NFR-9 | Should | Availability | The system shall keep a completed live run replayable for a bounded window, so a dashboard client that attaches late still receives the terminal result. |
| NFR-10 | Should | Performance | The system shall poll for due work no more often than every 10 seconds, and shall default to a 60 second interval. |
| NFR-11 | Should | Observability | The system shall log each scheduled execution, each lost claim, and each skip decision through the engine logger. |
| NFR-12 | Should | Observability | The system shall surface the durable outcome of a global routine in the backup settings surface, so an operator can distinguish a scheduled routine from a proven run. |

## Constraints

- Automations and routines live in PostgreSQL. The legacy SQLite read path is not available, and a configuration change is refused when the versioned configuration backend is absent.
- A project lane row is partitioned by project ID, so the same automation or routine ID can exist in two projects without either project addressing the other row.
- Global routines live in the central `global_routines` table, not in the project `routines` table.
- The global routine name is unique, so a shared-cluster routine cannot be duplicated.
- The dashboard mounts the automation and routine routes under `/api`.
- The scope is read from the `scope` query parameter or the `scope` body field, and an unrecognised value is a request error.
- A cron trigger is evaluated in UTC. The routine trigger also carries an optional timezone, which the persisted cron computation does not apply.
- The scheduler runs on the utility lane and does not consume the task-lane semaphore.

## Acceptance Criteria

- [ ] **FR-1**

```gherkin
@FR-1
Scenario: Create an automation
Given the dashboard API is running
When an operator posts an automation with a name, a schedule type, and a command
Then the response is 201 with the stored automation including its id, scope, and created timestamps
```

- [ ] **FR-2**

```gherkin
@FR-2
Scenario: Derive the cron expression from a preset
Given an operator creates an automation with schedule type "daily"
Then the stored automation carries the cron expression "0 0 * * *"
```

- [ ] **FR-3**

```gherkin
@FR-3
Scenario: Reject an automation with no work to do
Given an operator posts an automation with a name and no command and no steps
Then the response is 400 with a message that the command is required
```

- [ ] **FR-4**

```gherkin
@FR-4
Scenario: Compute the next run time
Given an operator creates an enabled automation with a valid cron expression
Then the stored automation carries a nextRunAt in the future
```

- [ ] **FR-5**

```gherkin
@FR-5
Scenario: Stop after a failed step
Given an automation has two command steps and the first step fails
When the automation runs
Then the second step does not run and the run result records one failed step
```

- [ ] **FR-6**

```gherkin
@FR-6
Scenario: Restrict the tools an AI prompt step may use
Given an AI prompt step names an allowlist of one selectable coding tool
When the step runs
Then the agent session receives exactly that tool allowlist
```

- [ ] **FR-7**

```gherkin
@FR-7
Scenario: Create a task from a create-task step
Given a create-task step carries a description and no target column
When the step runs
Then a Fusion task is created in the workflow intake column and its source records the schedule and step
```

- [ ] **FR-8**

```gherkin
@FR-8
Scenario: Record a manual run
Given an operator posts a manual run for an existing automation
Then the response carries the run result and the live run id, and the automation's run history holds the result
```

- [ ] **FR-9**

```gherkin
@FR-9
Scenario: Toggle an automation
Given an operator posts a toggle for a disabled automation
Then the returned automation is enabled and carries a recomputed nextRunAt
```

- [ ] **FR-10**

```gherkin
@FR-10
Scenario: Reject a reorder with the wrong step count
Given an automation has two steps
When an operator posts a reorder with one step id
Then the response is 400 with a step ID count mismatch message
```

- [ ] **FR-11**

```gherkin
@FR-11
Scenario: Create a routine
Given an operator posts a routine with a name, a cron trigger, and an agent id
Then the response is 201 with the stored routine including its catch-up and execution policies
```

- [ ] **FR-12**

```gherkin
@FR-12
Scenario: Reject an unknown trigger type
Given an operator posts a routine with trigger type "queue"
Then the response is 400 listing the supported trigger types
```

- [ ] **FR-13**

```gherkin
@FR-13
Scenario: Skip missed occurrences
Given a routine has catch-up policy "skip" and missed one cron occurrence
When the scheduler ticks
Then the routine runs once for the current occurrence and not once for the missed one
```

- [ ] **FR-14**

```gherkin
@FR-14
Scenario: Reject a concurrent run
Given a routine has execution policy "reject" and a run is already in progress
When a second run is requested
Then the second run returns a failed result stating that the routine was rejected
```

- [ ] **FR-15**

```gherkin
@FR-15
Scenario: Read a routine's run history
Given a routine has recorded runs
When an operator fetches the routine's runs
Then the response is the routine's run history array
```

- [ ] **FR-16**

```gherkin
@FR-16
Scenario: Refuse an unsigned webhook call
Given a webhook-triggered routine with a secret
When a caller posts to the routine's webhook without a signature header
Then the response is 401
```

- [ ] **FR-17**

```gherkin
@FR-17
Scenario: Skip execution while the engine is paused
Given an automation is due
When the engine settings report the engine as paused
Then the automation does not execute
```

- [ ] **FR-18**

```gherkin
@FR-18
Scenario: Run a due occurrence once across two pollers
Given a schedule is due
When two pollers claim the same due window concurrently
Then only one of them executes the schedule
```

- [ ] **FR-19**

```gherkin
@FR-19
Scenario: Stream a manual run
Given an operator starts a manual automation run
When a client opens the run stream for that automation
Then the client receives step, output, and terminal events for the run
```

- [ ] **FR-20**

```gherkin
@FR-20
Scenario: Keep the scopes apart
Given a global automation and a project automation exist
When an operator lists automations with scope "project"
Then only the project automation is returned
```

- [ ] **FR-21**

```gherkin
@FR-21
Scenario: Roll back a routine definition
Given a routine was renamed after it was created
When an operator restores the earlier configuration revision
Then the routine carries its earlier name again
```

- [ ] **FR-22**

```gherkin
@FR-22
Scenario: Show the Automations view
Given an operator opens Automations from the left sidebar
Then the view lists the automations and routines for the selected scope
```

- [ ] **NFR-1**

```gherkin
@NFR-1
Scenario: Refuse a webhook routine with a short secret
Given an operator posts a routine with a webhook trigger and a secret of 8 characters
Then the response is 400 explaining the 16 character minimum
```

- [ ] **NFR-2**

```gherkin
@NFR-2
Scenario: Audit a command routine
Given a routine runs a shell command
Then the run audit holds sandbox prepare and sandbox run rows for the routine
```

- [ ] **NFR-3**

```gherkin
@NFR-3
Scenario: Refuse a cross-scope read
Given a global automation exists
When a request reads that automation with scope "project"
Then the response is 404
```

- [ ] **NFR-4**

```gherkin
@NFR-4
Scenario: Time out a hanging run
Given an automation runs a command that does not finish
When the automation timeout elapses
Then the run result reports a failure naming the timeout
```

- [ ] **NFR-5**

```gherkin
@NFR-5
Scenario: Skip a lost claim
Given a poller loses the atomic claim for a due window
Then that poller skips the schedule and records no run
```

- [ ] **NFR-6**

```gherkin
@NFR-6
Scenario: Truncate oversized output
Given a run produces more output than the stored output cap
Then the stored output is truncated and marked as truncated
```

- [ ] **NFR-7**

```gherkin
@NFR-7
Scenario: Cap the run history
Given an automation has recorded more runs than the history cap
Then its run history holds only the most recent entries
```

- [ ] **NFR-8**

```gherkin
@NFR-8
Scenario: Isolate one failing routine
Given two routines are due and the first one throws during processing
Then the second routine still executes in the same poll cycle
```

- [ ] **NFR-9**

```gherkin
@NFR-9
Scenario: Replay a finished run
Given a manual run has already finished
When a client opens the run stream with that run id
Then the client receives the buffered events and the terminal result
```

- [ ] **NFR-10**

```gherkin
@NFR-10
Scenario: Enforce the minimum poll interval
Given the scheduler is constructed with a 1 second poll interval
Then the effective poll interval is 10 seconds
```

- [ ] **NFR-11**

```gherkin
@NFR-11
Scenario: Log a skipped schedule
Given a schedule is skipped because another poller holds its claim
Then the engine logger records the skip with the schedule name and id
```

- [ ] **NFR-12**

```gherkin
@NFR-12
Scenario: Show the global backup routine outcome
Given the shared backup routine has recorded a run
When an operator opens the backup settings
Then the surface shows the routine's last run result
```

## Conflicts

None identified yet.

## Open Questions

1. The routine trigger carries an optional timezone, but the persisted next-run computation always uses UTC. The code does not show whether the timezone is meant to shift the cron evaluation.
2. `catchUpLimit` is stored on the routine row with a default of 5, but the catch-up path in the routine runner bounds catch-up with a separate constant of 10 intervals. The code does not show which bound is authoritative.
3. The `api` routine trigger stores an endpoint on the routine, but no route in the dashboard serves that endpoint separately from the generic manual trigger route.
