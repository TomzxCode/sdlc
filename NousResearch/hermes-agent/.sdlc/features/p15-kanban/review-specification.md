---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

Drift found by `/sync-sdlc` comparing this artifact against the current code. Not yet reconciled.

- **Task status enum is wrong (Data Models > Task).** Documented as `todo/in_progress/blocked/done/archived`. `hermes_cli/kanban_workflow.py::DEFAULT_STATUSES` is `{triage, todo, scheduled, ready, running, blocked, review, done, archived}`. There is no `in_progress`; the code adds `triage`, `scheduled`, `ready`, `running`, `review`.
- **Task field names are wrong (Data Models > Task).** Documented `description`, `dedup_key` (unique), `failure_count`. The `Task` dataclass and `SCHEMA_SQL` in `hermes_cli/kanban_db.py` use `body`, `idempotency_key`, `consecutive_failures` (plus a `max_retries` breaker). `idempotency_key` is not a UNIQUE column; dedup is a SELECT-then-insert in `create_task`.
- **API contract tool table omits registered tools.** `kanban_schedule`, `kanban_request_review`, `kanban_request_changes` are registered in `tools/kanban_tools.py` `_TOOLS` but are absent from the "kanban_* toolset" contract table.
