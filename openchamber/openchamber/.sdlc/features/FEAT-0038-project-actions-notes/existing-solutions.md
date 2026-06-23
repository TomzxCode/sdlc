---
issue: ""
title: "Project Actions & Notes"
status: draft
---

# Existing Solutions: Project Actions & Notes

## Overview

The codebase already has substantial implementation for project actions, notes, and todos. Project config (`packages/web/server/lib/projects/project-config.js`) handles persistence of notes, todos, project actions, and scheduled tasks. The UI has `ProjectNotesTodoPanel.tsx` with markdown notes editing, draggable todo items (using `@dnd-kit` for sorting), todo-to-session/worktree send dialog, and project action detection and execution. Dev server URL detection and preview URL opening are also implemented. The main gap is cron-based scheduled tasks (FR-05) and worktree creation from todos (FR-06), which are partially covered and may need refinement.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/projects/project-config.js`, `packages/ui/src/components/session/ProjectNotesTodoPanel.tsx`, `packages/ui/src/components/session/TodoSendDialog.tsx`, `packages/ui/src/stores/useTerminalStore.ts` (projectActionRuns), `packages/ui/src/lib/openchamberConfig.ts`, `packages/web/server/lib/opencode/settings-runtime.js` |
| Open-source | Yes | `@dnd-kit` (already used), `cron-parser` (already used), `luxon` (already used), `cronstrue` (cron human-readable) |
| Commercial / SaaS | Yes | Linear, Notion, GitHub Projects (project management integrations) |
| Standards / protocols | Yes | Markdown (notes format), cron expression standard |
| Reference material | Yes | Cron expression format, IANA timezone database |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Internal project-config.js + ProjectNotesTodoPanel | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-07, FR-08 | FR-05, FR-06 |
| @dnd-kit (sortable) | Library | MIT | Mature | FR-03 | N/A — already used |
| cron-parser | Library | MIT | Mature | FR-09, NFR-01 | N/A — already used |
| luxon | Library | MIT | Mature | FR-09 (timezone) | N/A — already used |
| cronstrue | Library | MIT | Mature | FR-09 (cron visualization) | Not yet adopted, would help human-readable display |
| Dnd-kit sortable | Library | MIT | Mature | FR-03 | N/A — already used in ProjectNotesTodoPanel |

## Evaluation

### Internal project-config.js + ProjectNotesTodoPanel

- **Strengths:** Fully implemented project config persistence layer with CRUD for scheduled tasks, notes, todos, and actions.
  `ProjectNotesTodoPanel` provides a rich UI with markdown notes editing, draggable todos with expand/complete/send operations.
  Todo send dialog supports sending to a session or creating a worktree (FR-06 bridge exists but actual worktree creation from todos needs verification).
  Project actions include dev server detection, SSH port forwarding, URL preview opening.
  Terminal store tracks `projectActionRuns` for running action state.
  Auto-detection of dev server URLs from npm scripts or project config is in place.
  Timezone-aware scheduling with `luxon` and `cron-parser` supports daily/weekly/once/cron schedule kinds.
- **Weaknesses:** Scheduled tasks (FR-05) is listed as a should-have and may have gaps in reliability or UI integration.
  Worktree creation from todos (FR-06) needs verification of actual implementation completeness.
  Per-project custom icons (FR-08) not detected in the codebase scan (may need implementation).
  Context panel size persistence (NFR-02) needs verification.
- **Integration effort:** Low — substantial parts already done.
- **Cost:** Free.
- **Risks:** Low — core is production-ready.

### @dnd-kit

- **Strengths:** Already in use across multiple components for drag-to-reorder (todos, model picker, sidebar projects, draft presets).
  Provides sortable context, array move, keyboard support, and CSS transforms.
  Version 6.x (core) and 10.x (sortable) are well-maintained.
- **Weaknesses:** N/A — already adopted and working.
- **Integration effort:** Already done.
- **Cost:** Free (MIT).
- **Risks:** None.

### cron-parser + luxon

- **Strengths:** `cron-parser` provides robust cron expression parsing with timezone support, iterator capabilities.
  `luxon` provides IANA timezone support, DST handling, and date math.
  Both are already dependencies in `packages/web/package.json`.
- **Weaknesses:** `cron-parser` v4.x is used (latest is v5.x), but no known breaking issues.
- **Integration effort:** Already done.
- **Cost:** Free (MIT).
- **Risks:** None.

### cronstrue

- **Strengths:** Zero-dependency library that converts cron expressions to human-readable descriptions in 30+ languages.
  Would enhance the task editor dialog with descriptive labels like "Every day at 9:00 AM" alongside the raw cron expression.
  MIT license, well-maintained (3.14.0, March 2026).
- **Weaknesses:** Not yet adopted in the codebase.
  Adds a dependency for a convenience feature.
- **Integration effort:** Low — single function call in the UI component.
- **Cost:** Free (MIT).
- **Risks:** Low.

## Recommendation

**Direction: Adopt and extend**

The project actions, notes, and todos implementation is already largely complete and production-ready.
The existing stack (`@dnd-kit` for drag-to-reorder, `cron-parser` + `luxon` for scheduling, `project-config.js` for persistence) is the right foundation.
The main extensions needed are: (1) finish scheduled tasks UI integration, (2) verify and complete worktree-from-todo flow, (3) optionally adopt `cronstrue` for human-readable cron display in the task editor.
No new libraries are strictly required.

## Sources of Information

- `packages/web/server/lib/projects/project-config.js`: CRUD for scheduled tasks, notes, todos, actions with full validation and atomic writes.
- `packages/ui/src/components/session/ProjectNotesTodoPanel.tsx`: Full project notes (markdown) and draggable todos UI with send-to-session/worktree dialog.
- `packages/ui/src/components/session/TodoSendDialog.tsx`: Modal for selecting target session variant, agent, model when sending a todo.
- `packages/ui/src/stores/useTerminalStore.ts`: `projectActionRuns` state tracking for running project actions.
- `packages/ui/src/lib/openchamberConfig.ts`: OpenChamber project config types and serialization.
- `@dnd-kit`: MIT, drag-to-reorder library already in use across the codebase for todos, model picker, and sidebar.
- `cron-parser` v4.9.0: MIT, standard cron expression parsing library already in use.
- `luxon` v3.5.0: MIT, IANA timezone-aware date library already in use.
- `cronstrue` v3.14.0: MIT, zero-dependency cron-to-human-readable conversion, not yet adopted.

## Open Questions

1. Is the worktree-from-todo flow (FR-06) fully implemented or does it need additional development?
2. Should `cronstrue` be adopted for the scheduled task editor to show human-readable cron descriptions?
3. Are per-project custom icons (FR-08) needed, or can they be deferred?
