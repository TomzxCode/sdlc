---
title: "Project Actions & Notes"
status: done
---

# Specification: Project Actions & Notes

## Overview

Project actions are configured via project config files and auto-detection. Notes and todos live in the context panel's context tab. Scheduled tasks are managed server-side with cron-based execution.

## Architecture

```
ProjectActionsButton (packages/ui/src/components/layout/ProjectActionsButton.tsx)
    |  Detects dev servers, npm scripts, custom actions
    v  REST calls
Server (project actions via project config)

ProjectNotesTodoPanel (packages/ui/src/components/session/ProjectNotesTodoPanel.tsx)
    +---> Markdown notes editor
    +---> Draggable todo list (@dnd-kit)
    +---> Send-to-session action
    +---> Create-worktree-from-todo action

Scheduled Tasks (packages/web/server/lib/scheduled-tasks/runtime.js)
    +---> Cron expression parsing (cron-parser)
    +---> Task execution (triggers OpenCode prompts)
    +---> UI: ScheduledTasksDialog, ScheduledTaskEditorDialog
```

## Data Models

### ProjectAction

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Action identifier |
| name | string | not null | Display name |
| type | enum | not null | dev-server, ssh-forward, open-url, custom |
| command | string | not null | Shell command or URL |
| autoDetect | boolean | not null | Whether to auto-detect from project |

### ProjectNote

| Field | Type | Constraints | Description |
|---|---|---|---|
| projectId | string | PK | Project identifier |
| content | string | not null | Markdown content |

### TodoItem

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Item identifier |
| projectId | string | FK | Project identifier |
| text | string | not null | Todo text |
| order | number | not null | Sort position |
| completed | boolean | not null | Completion state |

### ScheduledTask

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Task identifier |
| cron | string | not null | Cron expression |
| prompt | string | not null | Prompt to execute |
| enabled | boolean | not null | Active state |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Drag and drop | @dnd-kit | Modern, accessible DnD library with sortable support |
| Cron parsing | cron-parser | Standard cron expression library |
| Task persistence | Server-side storage | Tasks must survive client disconnects |

## Risks and Unknowns

1. Dev server detection heuristics may produce false positives
2. Scheduled tasks may accumulate if the server is offline during scheduled times

## Out of Scope

- Task dependencies or workflows
- Calendar integration
- Task assignment to specific agents
