---
title: "Project Actions & Notes"
status: done
---

# Requirements: Project Actions & Notes

## Overview

OpenChamber provides project-level productivity tools: project actions for running dev servers and detecting preview URLs, persistent project notes, draggable todo items, and scheduled tasks. Users can organize work per-project and trigger common actions without leaving the app.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Run dev servers, manage notes and todos alongside coding |
| Project leads | Track project-level tasks and schedules |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support project actions: detect and run dev servers, configure SSH port forwarding, open remote URLs locally. |
| FR-02 | Must | The system shall support persistent project notes (markdown) that survive session switches. |
| FR-03 | Must | The system shall support draggable todo items per project with reorder capability. |
| FR-04 | Must | The system shall support sending todo items to the chat session as prompts. |
| FR-05 | Should | The system shall support scheduled tasks (cron-based) that trigger prompts automatically. |
| FR-06 | Should | The system shall support creating worktrees from todo items. |
| FR-07 | Should | The system shall support auto-detection of dev server URLs from npm scripts or project configuration. |
| FR-08 | May | The system shall support per-project custom icons with upload and automatic favicon discovery. |
| FR-09 | Must | The system shall support standard 5-field cron expressions with timezone-aware scheduling (IANA timezone strings) and schedule kinds: daily, weekly, once, and cron. |
| FR-10 | Must | The system shall allow scheduled tasks to target specific agents, models, providers, and variants. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Scheduled tasks shall execute reliably with cron parsing and error handling. |
| NFR-02 | Should | Performance | Context panel sizes for notes/todos shall be remembered across sessions. |

## Constraints

- Project actions are defined in project config or auto-detected
- Notes and todos are persisted via server-side storage
- Scheduled tasks use cron expressions parsed by `cron-parser`
- Scheduled tasks runtime lives in `packages/web/server/lib/scheduled-tasks/`


## Acceptance Criteria

- [ ] FR-01: Given a project with a dev server action, clicking it starts the server
- [ ] FR-02: Given project notes, they persist after closing and reopening the project
- [ ] FR-03: Given todo items, the user can drag to reorder them
- [ ] FR-04: Given a todo item, clicking "Send to session" creates a prompt from it
- [ ] FR-05: Given a scheduled task with a cron expression, it fires at the specified times
- [ ] FR-06: Given a todo item, the user can create a worktree from it
- [ ] FR-07: Given a project with npm scripts or project configuration, dev server URLs are auto-detected
- [ ] FR-08: Given a project, the user can set a custom icon via upload or automatic favicon discovery
- [ ] FR-09: Given a cron expression with a timezone, scheduling respects the IANA timezone and supports daily, weekly, once, and cron kinds
- [ ] FR-10: Given a scheduled task, the user can target a specific agent, model, provider, and variant
- [ ] NFR-01: Given a scheduled task with a cron expression, it executes reliably with proper error handling
- [ ] NFR-02: Given resized context panels for notes and todos, panel sizes are remembered across sessions

