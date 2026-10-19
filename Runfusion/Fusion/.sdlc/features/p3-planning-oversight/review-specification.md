---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Architecture

- **`register-planning-chat` is listed as a dashboard API registrar but it is an empty scaffold and is not mounted.** The whole file is `export function registerPlanningChatRoutes(_ctx: ApiRoutesContext): void { /* Step scaffold: route extraction lands in subsequent steps. */ }` (`packages/dashboard/src/routes/register-planning-chat.ts:1-5`). `packages/dashboard/src/routes.ts` mounts `registerTaskWorkflowRoutes` (`:987`) and `registerPlanningSubtaskRoutes` (`:1001`) but never `registerPlanningChatRoutes`, and `packages/dashboard/src/routes/create-api-routes-mount-sequence.ts:9-10` does not list it.

- **`tasks-overseer-controls` and `tasks-planner-overseer-state` are test file names, not route registrars.** The routes they cover live in `packages/dashboard/src/routes/register-task-workflow-routes.ts`: `POST /tasks/:id/overseer/nudge` (`:5138`), `POST /tasks/:id/overseer/stop` (`:5155`), `GET /tasks/:id/overseer/explain` (`:5172`) and `GET /tasks/:id/overseer/interventions` (`:5198`). The board and detail `plannerOverseerState` enrichment is in the same file at `:1426` and `:5055`. The names in the Architecture box are `packages/dashboard/src/routes/__tests__/tasks-overseer-controls.test.ts` and `packages/dashboard/src/routes/__tests__/tasks-planner-overseer-state.test.ts`.

- **The core planner module list omits the spec-lock and drift-report modules, which are part of the public `@fusion/core` surface.** `packages/core/src/planner/spec-lock.ts` and `packages/core/src/planner/drift-report.ts` are exported from `packages/core/src/index.ts:131-134` and `packages/core/src/index.gate.ts:101-104`. They are also not in the `packages/core/src/planner/index.ts` barrel (`:5-12`), so the Architecture box should list the package entry point rather than the barrel.

- **The engine module list omits the planning reset fence and the advisor, veto, session-delta and watchdog overseer modules.** `packages/engine/src/planning-reset-fence.ts` implements `PlanningResetFence` and `isPlanningResetHoldClearingUpdate`. `packages/engine/src/overseer/` also contains `overseer-advise-tool.ts`, `overseer-advisor-runtime.ts`, `overseer-advisor-service.ts`, `overseer-noop-finalize-veto.ts`, `overseer-session-delta.ts` and `overseer-watchdog.ts`, none of which the box mentions.

### Data models

- **The "Planner Oversight State" table does not correspond to any type in the code.** The shipped types are `PlannerOverseerRuntimeSnapshot` (`packages/core/src/planner/planner-overseer-state.ts:27-62`, fields `state`, `oversightLevel`, `watchedStage`, `signal`, `attemptCount`, `attemptLimit`, `pendingConfirmation`, `observedAt`, `reason`, `lastAction`, `advisorActive`, `advisorBacklog`, `lastAdviceSeverity`), `PlannerInterventionEntry` (`packages/core/src/planner/planner-intervention.ts:190-207`), `PlannerConfirmationRequest` (`packages/core/src/planner/planner-confirmation.ts:45-58`), `SpecLock` and `CurrentPlanEvidence` (`packages/core/src/planner/spec-lock.ts:44-71`) and `DriftReport` (`packages/core/src/planner/drift-report.ts:15-32`). The `perTaskOverride` row is a task column (`packages/core/src/postgres/schema/project.ts:212`, `planner_oversight_level`), not part of an oversight state object, and the `confirmation` and `interventions` rows are separate records with their own shapes.

### API contracts

- **`GET /api/tasks/:id/overseer-state` does not exist.** No route with that path is registered anywhere under `packages/dashboard/src/routes/`. The actual surfaces are `GET /tasks/:id/overseer/explain`, `GET /tasks/:id/overseer/interventions`, `POST /tasks/:id/overseer/nudge`, `POST /tasks/:id/overseer/stop` (`packages/dashboard/src/routes/register-task-workflow-routes.ts:5138`, `:5155`, `:5172`, `:5198`), `GET /tasks/:id/spec-lock` (`:5005`), and the transient `plannerOverseerState` field added to `GET /tasks` and `GET /tasks/:id` (`:1426` and `:5055`). The transient snapshot is never persisted (`packages/core/src/planner/planner-overseer-state.ts:24-26`).

### Sequences

- **The oversight sequence names a run-audit event that the code does not emit.** The sequence says `task:oversight-withheld-human-control`, but the emitted type is `overseer:oversight-withheld-human-control` (`packages/engine/src/project-engine.ts:2732` and the type union at `packages/engine/src/util/run-audit.ts:1030`).

- **The oversight sequence omits the approval-blocked withhold reason.** The sequence says "if user-paused/auto-merge-off", but the guard also withholds on an approval hold (`packages/engine/src/overseer/overseer-human-control-policy.ts:59` and `:93-95`).

- **The oversight sequence's confirm step is unreachable in the live path.** The sequence says the overseer may "withhold/steer/confirm", but the confirm branch is never entered at runtime: `packages/core/src/planner/planner-recovery.ts:240-253` suppresses the merger and pull-request confirmation when `autoMergeWillProceed === true`, and `packages/engine/src/overseer/planner-recovery-controller.ts:251-265` withholds the task whenever `allowsAutoMergeProcessing` is false, so `autoMergeWillProceed` is always true on the path that reaches the decision. `resolveConfirmation` has no production caller.

### Technical decisions

- **The "Oversight levels" row rests on a human gate that the live path never reaches.** The rationale says the levels escalate "with a human gate at the top", and the default level is `autonomous` (`packages/core/src/types/ui/execution-and-ui.ts:41`, `DEFAULT_PLANNER_OVERSIGHT_LEVEL = "autonomous"`). The gate itself is the unreachable branch described above, so the row needs to say what actually happens at the top level: bounded autonomous recovery of three attempts per task and watched stage, with the merge and pull-request checkpoint suppressed as advisory.

### Risks and unknowns

- **The claim that confirmation state is "tracked by engine tests" no longer holds.** The pending confirmation registry is an in-memory map (`packages/engine/src/overseer/planner-recovery-controller.ts:200`), so it does not survive an engine restart, and the only engine suite that exercised the confirmation lifecycle is skipped (`packages/engine/src/__tests__/planner-recovery-controller-confirmation.test.ts:39-43`).
