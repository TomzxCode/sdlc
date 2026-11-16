---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Requirements (Cron Scheduling and Subagent Delegation)

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **NFR-1 "Cron jobs shall have a 3-minute hard interrupt to prevent runaway sessions" is stale.** The implemented guard is an inactivity watchdog, not a fixed 3-minute wall-clock interrupt. `cron/scheduler.py::_cron_inactivity_seconds()` defaults to 600s idle, reads `HERMES_CRON_TIMEOUT` as an override, and accepts `0` for unlimited. `_run_agent_with_watchdog()` hard-interrupts only a stalled session, so a long but active job is never cut off. `cron/lifecycle_guard.py` is a gateway lifecycle command guard, not a timeout. No 180s cron job interrupt exists in `cron/`. Reword NFR-1 to describe the configurable idle watchdog.

Resync `requirements.md` to describe the implemented watchdog, then re-review.
