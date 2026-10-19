---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-6 | "The system shall support overnight processing for long-running consolidation jobs." | Overnight is a separate, user-initiated supervised coordinator run, not an ambient capability. It is reached through `/overnight start|status|log|review|cancel` (`crates/jcode-overnight-core/src/lib.rs:14-24,290`; `crates/jcode-app-core/src/server/runtime_special_commands.rs:311-380`). There is no reference to `overnight` anywhere under `crates/jcode-app-core/src/ambient/`, and there is no overnight window trigger. | Remove FR-6 from ambient mode and record the overnight run as a separate feature. If it must stay, reword to: "The system shall expose a separate supervised overnight run (`/overnight start|status|log|review|cancel`) for long-running consolidation; overnight is not driven by the ambient scheduler." |
| FR-2 | "The system shall execute directives (ambient instructions) and run tasks such as garden/scout activities." | Directives are `UserDirective`s arriving as email replies to ambient notifications (`crates/jcode-app-core/src/ambient/directives.rs:12-25`, wired to the IMAP reply poller at `ambient/runner.rs:565-576`), not config-style instructions. Garden and scout are prompt-level task categories (`ambient/prompt.rs:481-506`), not discrete task types. The actual task source is the scheduled queue. | "The system shall execute scheduled queue items, user directives received by email reply, and prompt-defined garden (memory-graph maintenance) and scout (proactive work) activities." |
| FR-3 | "The system shall persist ambient state (status, log, directives) so it survives reloads." | The state is per-user on disk under `~/.jcode/ambient/`, written by the ambient runner process, and is not part of the server's durable-state reload snapshot. "Log" means per-cycle transcript files, of which `jcode ambient log` surfaces only the newest 20 (`ambient/runner.rs:344`). | "The system shall persist ambient state (status and cycle counters in `~/.jcode/ambient/state.json`, the scheduled queue in `queue.json`, directives in `directives.json`, and per-cycle transcripts under `transcripts/`) so ambient survives a server restart." |
| FR-5 | "The system shall expose ambient status and control via the CLI (`jcode ambient status`, `trigger`, `stop`, `log`)." | The control surface is wider: the debug-socket commands `ambient:start`, `ambient:queue`, `ambient:permissions`, `ambient:approve:<id>`, `ambient:deny:<id>` (`crates/jcode-app-core/src/server/debug_ambient.rs:25-171`) and the `jcode permissions` review command (`src/cli/args.rs:370-371`). | "The system shall expose ambient status and control via the CLI (`jcode ambient status`, `log`, `trigger`, `stop`, plus the hidden `run-visible`) and via the server debug socket (`ambient:start`, `ambient:queue`, `ambient:permissions`, `ambient:approve:<id>`, `ambient:deny:<id>`), with pending ambient permission requests reviewable via `jcode permissions`." |

## Non-functional requirements

NFR-1 reads "Ambient actions shall be subject to the same permission/safety gates as interactive actions."
Partially true.
The ambient agent uses the same `SafetySystem` and the same command-risk gate, but the permission path is ambient-specific: `request_permission` is restricted to registered ambient sessions (`crates/jcode-app-core/src/tool/ambient.rs:73-102`) and ambient requests are answered out of band through the debug socket or `jcode permissions`, not by the interactive turn's prompt.
Reword to: "Ambient actions shall be subject to the same safety system and command-risk gates as interactive actions, but ambient permission requests follow their own request and approval flow."

## Constraints

"Ambient runs inside the same server process (not a separate daemon)." is incomplete.
The runner is created and its loop spawned inside the server (`crates/jcode-app-core/src/server.rs:833-834,1526-1534`), but it is initialized even when `[ambient].enabled = false` so scheduled session-targeted tasks still work, and a visible cycle runs as a separate process (`jcode ambient run-visible`).
Reword to: "Ambient runs inside the server process (not a separate daemon). The runner is always present so scheduled session-targeted tasks work even with `[ambient].enabled = false`; a visible cycle is the one exception and is launched as a separate `jcode ambient run-visible` process."

## Open questions

Open Question 1 asks for the default work-cycle cadence and task budget.
The defaults are now stated: `min_interval_minutes = 5`, `max_interval_minutes = 120`, `pause_on_active_session = true`, `proactive_work = true`, `allow_api_keys = false`, `api_daily_budget = None` (`crates/jcode-config-types/src/lib.rs:1367-1382`).
Replace it with: "Resolved: cycles are scheduled adaptively between `min_interval_minutes` (5) and `max_interval_minutes` (120) based on rate-limit headroom, and pause while an interactive session is active. Open: the per-cycle token budget is not configurable, only the daily API-key budget (`api_daily_budget`)."

## Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall deliver scheduled items to their target (ambient, session, or spawn) and spawn a session for a spawn-target item. | `ScheduleTarget::{Ambient, Session, Spawn}` (`crates/jcode-app-core/src/ambient.rs:96-110`), `take_ready_direct_items` (`ambient/persistence.rs:118-146`), `deliver_scheduled_direct_item` and `spawn_session_for_scheduled_item` (`ambient/runner.rs:388-553`). |
| FR-10 | The system shall adapt cycle intervals to rate-limit headroom and track a rolling 24 hour usage log. | `crates/jcode-app-core/src/ambient/scheduler.rs:21-24,48-53,133-136` (`UsageLog`, 24 hour pruning, `AdaptiveScheduler`). |
| FR-11 | The system shall hold a single-instance lock so two ambient runners do not run at once. | `crates/jcode-app-core/src/ambient/persistence.rs:169-207` (`AmbientLock` at `~/.jcode/ambient/ambient.lock`). |

## Testability

No issues found beyond the corrections above.

## Feasibility

No issues found.
