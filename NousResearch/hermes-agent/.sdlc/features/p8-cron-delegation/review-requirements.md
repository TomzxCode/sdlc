---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-23
---

# Review: Requirements (Cron Scheduling and Subagent Delegation)

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **NFR-1 "Cron jobs shall have a 3-minute hard interrupt to prevent runaway sessions" is stale.** The implemented guard is an inactivity watchdog, not a fixed 3-minute wall-clock interrupt. `cron/scheduler.py::_cron_inactivity_seconds()` defaults to 600s idle, reads `HERMES_CRON_TIMEOUT` as an override, and accepts `0` for unlimited. `_run_agent_with_watchdog()` hard-interrupts only a stalled session, so a long but active job is never cut off. `cron/lifecycle_guard.py` is a gateway lifecycle command guard, not a timeout. No 180s cron job interrupt exists in `cron/`. Reword NFR-1 to describe the configurable idle watchdog.

Resync `requirements.md` to describe the implemented watchdog, then re-review.

## Sync drift: 2026-11-23

New drift detected during `/sync-sdlc` reconciliation beyond the 2026-11-16 entry:

1. **NFR-3 says delegation concurrency is capped with a default of 3.** The current default is 10. `tools/delegate_tool_config.py::_DEFAULT_MAX_CONCURRENT_CHILDREN = 10` and `hermes_cli/config_defaults.py` sets `delegation.max_concurrent_children: 10`. `hermes_cli/config_migrations.py` records a deliberate migration from 3 to 10. The cap is configurable with a floor of 1 and no ceiling. Update NFR-3 to the default of 10, then re-review.
