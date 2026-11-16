---
artifact: tests.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: tests.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **`tests/run_agent/` does not exist.** The Test Files, Unit Tests and End-to-End Tests sections all point at `tests/run_agent/`, described as holding "115+ test files". No such directory exists in the tree. The named files (`test_run_agent.py`, `test_streaming.py`, `test_tool_call_guardrail_runtime.py`, `test_iteration_budget_race.py`) live under `tests/agent/`.
- **The `tests/agent/` file count is wrong.** Test Files claims "226 test files"; the directory currently holds 1197 `test_*.py` files (1204 files total).
- **Two named test files do not exist anywhere under `tests/`.** `test_interactive_interrupt.py` (Test Files, Coverage Matrix FR-4) and `test_jsondecodeerror_retryable.py` (Coverage Matrix NFR-2) have no file in the tree. No file matching `*json*decode*` exists at all. Interrupt coverage lives under other names in `tests/agent/` (for example `test_exit_cleanup_interrupt.py`, `test_concurrent_interrupt.py`).
- **The "Budget sharing with subagents" integration test cannot exist.** Subagents receive a fresh `IterationBudget` (`tools/delegate_tool.py:317`), so there is no shared parent/child budget to exercise. Coverage Matrix FR-3 points at `test_iteration_budget_race.py`, which tests the `IterationBudget` primitive in isolation, not parent/child sharing.

Resync the Test Files list, file counts, and coverage matrix to the tests that exist.
