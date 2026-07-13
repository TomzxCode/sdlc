---
title: "Cron Scheduling and Subagent Delegation"
status: done
---

# Test Plan: Cron Scheduling and Subagent Delegation

## Scope

Tests covering cron job store, scheduler tick loop, schedule parsing (duration, cron expression, every-phrase, ISO timestamp), per-job overrides, multi-platform delivery, delegation (single and batch), and subagent lifecycle.

## Test Files

- tests/cron/ — 28+ test files covering all cron subsystems
- tests/cron/test_jobs.py — Job store CRUD operations
- tests/cron/test_scheduler.py — Scheduler tick loop
- tests/cron/test_compute_next_run_last_run_at.py — Schedule computation
- tests/cron/test_cron_script.py — Pre-run data collection scripts
- tests/cron/test_cron_workdir.py — Per-job working directory
- tests/cron/test_cron_prompt_injection_skill.py — Skill loading per job
- tests/cron/test_cron_context_from.py — Job chaining
- tests/cron/test_cron_provider_pin.py — Provider overrides
- tests/tools/test_delegate.py — Subagent delegation
- tests/tools/test_delegate_*.py — Delegation edge cases
- tests/tools/test_cronjob_tools.py — Cronjob tool schema
- tests/tools/test_cronjob_run_immediate.py — Immediate job execution
- tests/hermes_cli/test_cron*.py — Cron CLI commands

## Unit Tests

- Schedule format parsing (duration, cron, every-phrase, ISO)
- Job CRUD (create, edit, list, pause, resume, remove)
- Tick loop state machine
- Delegate task argument validation
- Subagent role enforcement (leaf vs orchestrator)

## Integration Tests

- Full job lifecycle: create → schedule → fire → deliver
- Batch delegation with max_concurrent_children enforcement
- Background task completion notification
- File lock prevention of duplicate ticks
- 3-minute hard interrupt on runaway jobs
- Skill loading during cron execution

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Job fire time missed (catchup) | Catchup window clamped to 120s–2h |
| Runaway agent loop in cron | 3-minute hard interrupt |
| Duplicate tick across processes | File lock prevents duplicate |
| Delegate batch with failed subtasks | Other subtasks continue |
| Background delegation after restart | Lost (process-local, use cron instead) |
| Job with no_agent=True script failure | Script error reported, no agent invocation |

## Test Infrastructure

- In-memory job store for deterministic testing
- Mock scheduler tick for precise timing tests
- Temp filesystem for workdir tests
- Subprocess delegation testing

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (duration schedules) | test_compute_next_run_last_run_at.py |
| FR-2 (cron expressions) | test_compute_next_run_last_run_at.py |
| FR-3 (every-phrase schedules) | test_compute_next_run_last_run_at.py |
| FR-4 (ISO timestamps) | test_compute_next_run_last_run_at.py |
| FR-5 (per-job overrides) | test_cron_script.py, test_cron_workdir.py |
| FR-6 (multi-platform delivery) | Cron delivery tests |
| FR-7 (subagent delegation) | test_delegate.py |
| FR-8 (blocking + background) | test_delegate.py |
| FR-9 (concurrent batch) | test_delegate.py |
| NFR-1 (3-minute hard interrupt) | test_scheduler.py |
