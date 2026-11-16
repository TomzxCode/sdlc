---
artifact: tests.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

Drift found by `/sync-sdlc` comparing this artifact against the current code. Not yet reconciled.

- **Test Files entry and Coverage Matrix point at a nonexistent test.** `tests/plugins/test_kanban_worker_runs.py` is listed under "Test Files" and is the only mapped test for FR-9/FR-10 (dispatcher) and FR-12 (auto-block) in the Coverage Matrix, but no such file exists in the repository. The dispatcher and auto-block behavior documented here is not covered by the named test.
