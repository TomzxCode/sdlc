---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Tests (Cron Scheduling and Subagent Delegation)

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Integration Tests item "3-minute hard interrupt on runaway jobs" is stale.** The implemented guard is an inactivity watchdog with a 600s default and a `HERMES_CRON_TIMEOUT` override (`0` means unlimited), in `cron/scheduler.py::_run_agent_with_watchdog()`. The matching test is `tests/cron/test_cron_inactivity_timeout.py`.

2. **Edge case row "Runaway agent loop in cron | 3-minute hard interrupt" names the same removed behavior.** Expected behavior should name the configurable inactivity limit.

3. **Coverage matrix row "NFR-1 (3-minute hard interrupt) | test_scheduler.py" is stale.** It should reference the inactivity watchdog test and the configurable limit.

Resync `tests.md` to describe the inactivity watchdog, then re-review.
