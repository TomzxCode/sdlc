---
issue: ""
title: "Scheduled Tasks"
status: draft
---

# Existing Solutions: Scheduled Tasks

## Overview

The scheduled tasks feature is fully implemented across the server and UI. The runtime (`packages/web/server/lib/scheduled-tasks/runtime.js`, ~774 lines) provides cron-based task scheduling with support for four schedule kinds (daily, weekly, once, cron), IANA timezone awareness via `luxon`, per-task enable/disable, global and per-project concurrency limits, missed task skipping (no catch-up), watchdog timeouts, one-time task auto-consumption, and integration with the desktop quit flow. Persistence is handled by `project-config.js` using atomic JSON writes. The UI provides `ScheduledTasksDialog.tsx` and `ScheduledTaskEditorDialog.tsx` for management. The feature works across web, desktop, and VS Code runtimes.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/scheduled-tasks/runtime.js`, `packages/web/server/lib/projects/project-config.js` (CRUD + schedule normalization), `packages/web/server/index.js` (createScheduledTasksRuntime), `packages/electron/main.mjs` (quit risk detection), `packages/ui/src/components/session/ScheduledTasksDialog.tsx`, `packages/web/server/lib/opencode/feature-routes-runtime.js` (route registration) |
| Open-source | Yes | `cron-parser` (already used v4.9.0), `luxon` (already used v3.5.0), `node-cron`, `cronstrue` |
| Commercial / SaaS | Yes | GitHub Actions scheduled workflows, Jenkins cron jobs, cron(8) system daemon |
| Standards / protocols | Yes | Cron expression format, IANA timezone database (TZDB) |
| Reference material | Yes | Cron format reference, luxon timezone docs, cron-parser API docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Internal scheduled-tasks runtime.js | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, FR-08 | FR-05 (cron visualization) |
| cron-parser (npm) | Library | MIT | Mature | FR-01, FR-03, FR-07 | N/A — already used |
| luxon (npm) | Library | MIT | Mature | FR-03 | N/A — already used |
| node-cron (npm) | Library | MIT | Mature | FR-01, FR-07 | Would replace custom timer logic — not needed |
| cronstrue (npm) | Library | MIT | Mature | FR-05 (human-readable cron) | Not yet adopted |

## Evaluation

### Internal scheduled-tasks runtime.js

- **Strengths:** Full implementation with production readiness.
  Supports daily (with multiple times), weekly (with weekday selection + multiple times), once (specific date+time), and cron (freeform 5-field) schedule kinds.
  IANA timezone support via `luxon` (`DateTime.fromMillis` with zone, `IANAZone.isValidZone`).
  Per-task enable/disable without deletion.
  Global and per-project concurrency limits with a queue-based execution model.
  Missed tasks are silently skipped — only fires while server is running (no catch-up).
  One-time tasks are auto-disabled after execution.
  Watchdog timeout per task run (30min default).
  Jitter on timer scheduling to prevent thundering herd.
  Desktop quit risk detection: `getStatus()` returns `hasRunningScheduledTasks` and `hasEnabledScheduledTasks` counts, used by Electron to warn on quit.
  Event emission (`openchamber:scheduled-task-ran`) for real-time UI updates.
  Manual "run now" capability independent of schedule.
  Task state tracking: lastRunAt, lastStatus, lastDurationMs, lastError, lastSessionId, nextRunAt.
- **Weaknesses:** No cron visualization in the task editor dialog (FR-05).
  No `cronstrue` integration for human-readable cron descriptions.
  Uses `setTimeout` for timer scheduling which has a maximum delay of ~24.8 days (`MAX_TIMER_DELAY_MS`), handled by re-scheduling but adds edge case complexity.
  Cron expression validation happens in `project-config.js` but errors could be surfaced better in the UI.
- **Integration effort:** Already done.
- **Cost:** Free.
- **Risks:** Low — code is in production use.

### cron-parser

- **Strengths:** Robust cron expression parsing with timezone support, DST handling, iterator capabilities.
  Used for both validation (`validateCronExpression` in `project-config.js`) and next-run computation (`computeNextRunAt` in `runtime.js`).
  v4.9.0 with MIT license, 3M+ weekly downloads.
- **Weaknesses:** Latest is v5.x, but v4.x is stable and sufficient.
- **Integration effort:** Already done.
- **Cost:** Free (MIT).
- **Risks:** None.

### luxon

- **Strengths:** IANA timezone support, DST handling, date math, formatting.
  Used for timezone-aware date calculations, weekday resolution, and time string parsing.
  v3.5.0 with MIT license.
- **Weaknesses:** N/A — well-maintained and already adopted.
- **Integration effort:** Already done.
- **Cost:** Free (MIT).
- **Risks:** None.

### cronstrue

- **Strengths:** Zero-dependency library converting cron expressions to human-readable text.
  Would enhance the task editor with descriptions like "At 9:00 AM, Monday through Friday".
  Supports 30+ locales matching OpenChamber's i18n languages.
  v3.14.0 (March 2026), MIT license, 375+ dependents, 2.7M weekly downloads.
- **Weaknesses:** Not yet adopted.
  Adds a dependency for a UI convenience feature.
- **Integration effort:** Low — single `cronstrue.toString(expression)` call in the React component.
- **Cost:** Free (MIT).
- **Risks:** Low.

## Recommendation

**Direction: Adopt**

The internal scheduled tasks runtime is fully functional and production-ready.
The existing stack (`cron-parser` for parsing, `luxon` for timezone handling, `project-config.js` for persistence) is the correct choice.
Two optional enhancements would improve the user experience: (1) adopt `cronstrue` for human-readable cron descriptions in the task editor, and (2) add a cron visualization component (custom or leveraging an existing React component).
No core changes to the runtime are needed.

## Sources of Information

- `packages/web/server/lib/scheduled-tasks/runtime.js`: Complete scheduled task runtime with timer scheduling, queue, concurrency limits, watchdog, state management, and desktop quit integration.
- `packages/web/server/lib/projects/project-config.js`: Task CRUD, normalization, validation, and atomic JSON persistence.
- `packages/web/server/index.js`: Runtime creation with dependency injection (`projectConfigRuntime`, `buildOpenCodeUrl`, etc.).
- `packages/electron/main.mjs`: Quit risk detection using `getStatus()` for running/enabled scheduled task counts.
- `packages/ui/src/components/session/ScheduledTasksDialog.tsx`: UI dialog for listing and managing scheduled tasks.
- `packages/ui/src/lib/i18n/messages/en.ts`: i18n strings for scheduled tasks UI.
- `cron-parser` v4.9.0: MIT, standard cron expression parser, already in `packages/web/package.json`.
- `luxon` v3.5.0: MIT, IANA timezone-aware datetime library, already in `packages/web/package.json`.
- `cronstrue` v3.14.0: MIT, zero-dependency cron-to-human-readable library, not yet adopted.

## Open Questions

1. Should `cronstrue` be added to provide human-readable descriptions in the scheduled task editor dialog?
2. Is the setTimeout-based scheduling with MAX_TIMER_DELAY_MS workaround stable enough for long-running server instances (weeks+), or should a tick-based approach be considered?
3. Should the cron visualization (FR-05) be a custom component or leverage an existing library?
