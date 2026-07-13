---
title: "Scheduled Tasks"
status: done
---

# Specification: Scheduled Tasks

## Overview

Scheduled tasks use a server-side runtime (`packages/web/server/lib/scheduled-tasks/runtime.js`) with `cron-parser` for cron expression evaluation. The UI uses `ScheduledTasksDialog.tsx` and `ScheduledTaskEditorDialog.tsx` for management.

## Architecture

```
ScheduledTasksDialog / ScheduledTaskEditorDialog (packages/ui/src/components/session/)
    +---> Task CRUD with cron expression editor
    +---> Locale-aware weekday/timezone display
    |
Server (packages/web/server/lib/scheduled-tasks/runtime.js)
    +---> cron-parser for expression evaluation
    +---> Task execution (triggers OpenCode prompt)
    +---> Coordinate with desktop quit flow
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Cron engine | cron-parser | Standard cron expression library with locale support |
| Execution | Server-side | Tasks must run even if no client is connected |

## Out of Scope

- Task chaining or dependencies
- Calendar view for schedules
