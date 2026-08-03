---
title: "Kanban Multi-Agent Work Queue"
status: done
---

# Test Plan: Kanban Multi-Agent Work Queue

## Scope

Tests covering the kanban CLI, the SQLite board store, the worker/orchestrator toolset, dispatcher behavior (claim/reclaim/promotion/spawn), board isolation, attachments, comment injection, model overrides, and dashboard integration.

## Test Files

- tests/tools/test_kanban_tools.py — Worker/orchestrator `kanban_*` toolset
- tests/tools/test_kanban_redaction.py — Sensitive-data redaction in kanban tool output
- tests/tools/test_delegate_kanban_isolation.py — Subagent/worker board isolation
- tests/tools/test_kanban_comment_injection.py — Comment injection from worker environment
- tests/plugins/test_kanban_worker_runs.py — Worker run lifecycle through the dispatcher
- tests/plugins/test_kanban_board_project_api.py — Board and project APIs
- tests/plugins/test_kanban_dashboard_plugin.py — Dashboard plugin wiring
- tests/plugins/test_kanban_attachments.py — File attachment lifecycle
- tests/plugins/test_kanban_estimate.py — Task effort estimation
- tests/plugins/test_kanban_model_override.py — Per-task model override propagation

## Unit Tests

- Board creation, listing, switching, renaming, archiving, and deletion
- Task create (including dedup-key idempotency), show, edit, assign, block, complete, archive
- Dependency link/unlink behavior
- Attachment add/list/remove

## Integration Tests

- Worker spawned for board A cannot see board B (isolation via pinned env)
- Comment injection from the worker environment into a task
- Model override reaching the spawned worker
- Dashboard plugin loading against a real board store

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| EC-1 | Duplicate create with same dedup key | Returns existing task id, no duplicate row |
| EC-2 | Task exceeding failure limit | Dispatcher auto-blocks it to prevent a spin loop |
| EC-3 | Worker heartbeat expires (stale claim) | Dispatcher reclaims and re-promotes the task |
| EC-4 | Runaway worker on reclaim | SIGTERM then SIGKILL frees the task |
| EC-5 | Board hard-deleted with attachments | Board directory removed; no recovery (documented) |
| EC-6 | Sensitive data in tool output | Redacted before returning to the agent |

## Test Infrastructure

- Per-board SQLite fixtures in temp directories
- Mock gateway/dispatcher state for tick-driven tests
- Isolated `HERMES_HOME` per test (no writes to `~/.hermes/`)

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (kanban CLI) | test_kanban_board_project_api.py |
| FR-3 (board lifecycle) | test_kanban_board_project_api.py |
| FR-4 (task lifecycle + dedup) | test_kanban_tools.py, test_kanban_board_project_api.py |
| FR-6 (attachments) | test_kanban_attachments.py |
| FR-7 (comments) | test_kanban_comment_injection.py |
| FR-8 (kanban_* toolset) | test_kanban_tools.py |
| FR-9/FR-10 (dispatcher) | test_kanban_worker_runs.py |
| FR-11 (board isolation) | test_delegate_kanban_isolation.py |
| FR-12 (auto-block) | test_kanban_worker_runs.py |
| FR-14 (dashboard) | test_kanban_dashboard_plugin.py |
| NFR-1 (isolation) | test_delegate_kanban_isolation.py |
| NFR-3 (atomic claims) | test_kanban_worker_runs.py |
