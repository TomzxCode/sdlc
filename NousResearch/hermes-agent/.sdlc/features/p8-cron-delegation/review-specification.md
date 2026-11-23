---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-23
---

# Review: Specification (Cron Scheduling and Subagent Delegation)

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Architecture tree labels `lifecycle_guard.py` as the "3-minute hard interrupt".** `cron/lifecycle_guard.py` contains no timeout logic. It blocks gateway lifecycle commands such as `hermes gateway restart`, `launchctl`/`systemctl` operations on the gateway, and process kills aimed at the host interpreter. The hard interrupt actually lives in `cron/scheduler.py::_run_agent_with_watchdog()`.

2. **Technical decision row "Hard interrupt | 3-minute timeout" is stale.** The implemented limit is an idle-time watchdog: `_cron_inactivity_seconds()` defaults to 600s, honors `HERMES_CRON_TIMEOUT`, and treats `0` as unlimited. Attached scripts are bounded separately by a 3600s script timeout.

3. **Risks item 3 ("The 3-minute hard interrupt may be too short for complex batch tasks") rests on the removed fixed timeout.** With a 600s idle default and `0` meaning unlimited, this risk no longer describes the code.

4. **Data model table omits most authored job fields.** `cron/job_definition.py::JOB_DEFINITION_FIELDS` includes `name`, `provider`, `base_url`, `skill`, `no_agent`, `monitor_script`, `monitor_url`, `schedule_display`, `deliver`, `origin`, `enabled_toolsets`, `attach_to_session`, `reasoning_effort`, `failure_deliver`, `timezone`, `grace_minutes`, `catch_up`, and `wrap_response` in addition to the documented fields. FR-5 requires a provider override, but `provider` is absent from the table. `timezone` and `grace_minutes` are also active scheduler knobs documented in `cron/AGENTS.md`.

Resync `specification.md` to the implemented architecture, timeout, and job schema, then re-review.

## Sync drift: 2026-11-23

New drift detected during `/sync-sdlc` reconciliation beyond the 2026-11-16 entries:

1. **Technical decision row "Delegation | Subprocess with shared budget" is stale.** `tools/delegate_tool.py::_build_child_agent()` constructs an in-process `AIAgent` at `tools/delegate_tool.py:319`. It passes `iteration_budget=None` with the comment "fresh budget per subagent" at `tools/delegate_tool.py:334`. `max_iterations` comes from `delegation.max_iterations` config, default 250, and caller-supplied values are ignored (`tools/delegate_tool.py:660-668`). There is no subprocess, and children do not inherit the parent's remaining iteration budget. Replace the row with the in-process child agent and the config-owned iteration budget, then re-review.
