---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
The v0.99.0 "simplify swarm mode" release removed the deep task-graph mode, so the artifacts need to record that removal and the behavior that replaced it.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-7 | "The system shall validate member reports (including a tldr rule and completion-report marker) before accepting them." | Nothing is rejected. `validate_swarm_tldr` normalizes a caller-supplied tldr or derives a truncated preview when the body exceeds 240 characters, and its doc comment states "Missing or overlong summaries must never block delivery" (`crates/jcode-swarm-core/src/lib.rs:24-44`). The completion marker is a prompt instruction appended to assignments (`crates/jcode-swarm-core/src/lib.rs:343-363`), not a server-side gate. `Request::CommReport` is accepted unconditionally (`crates/jcode-app-core/src/server/client_lightweight_control.rs:756-800`). | "The system shall normalize member completion reports (trim, cap at 4000 characters via `MAX_SWARM_COMPLETION_REPORT_CHARS`, derive a tldr preview when the body exceeds 240 characters) and record them for the coordinator; a missing or overlong tldr must not block delivery." |
| FR-5 | "The system shall show member status and progress in the session." | Still accurate, but the v0.99.0 pinned-todo collapse and the overall progress display are separate session-todo work and are not part of this feature. | No wording change; add an Out of Scope note that the pinned todo band and the todo policy are owned by FEAT-p15. |

## Non-functional requirements

NFR-1 reads "Swarm state must be durable across server reloads and restarts."
The code is durable but with two documented losses: idle headless workers are not restored after a restart (`IDLE_WORKER_NOT_RESTORED_NOTE`, `crates/jcode-app-core/src/server/swarm_persistence.rs:101-102,356`), and dormant plans are pruned after the retention window (default 7 days, `:18,60-90`).
Reword to: "Swarm state must be durable across server reloads and restarts. Durable snapshots are pruned only when a plan is dormant (no items, or every item unassigned and not active) and untouched for the retention window (default 7 days); idle headless workers are not resumed after a restart and are reported as such."

## Constraints

The constraint "Swarm behavior is configured under the `[agents]` config section (spawn mode, swarm model)." understates the surface.
`[agents]` also carries `swarm_effort`, `swarm_root_effort` (new in v0.99.0, default `low`), `swarm_max_concurrent_agents`, `swarm_stall_after_secs`, `swarm_stall_nudge`, `swarm_gallery_max_pct`, and `swarm_strip_layout` (`crates/jcode-config-types/src/lib.rs:564-655`).
Reword accordingly.

## Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall drive a plan to completion through a `run_plan` coordinator that dispatches ready tasks, waits, retries, and reports utilization and terminal summaries under a concurrency budget. | `crates/jcode-app-core/src/tool/communicate.rs:426,892,1110-1301,2857`, tests in `crates/jcode-app-core/src/tool/communicate_tests.rs:46-520`. |
| FR-10 | The system shall support task control actions (start, start_task, wake, resume, retry, reassign, replace, salvage). | `TaskControlAction` (`crates/jcode-plan/src/lib.rs:243-278`), `crates/jcode-app-core/src/server/comm_control_tests/task_control.rs`. |
| FR-11 | The system shall track per-task progress through heartbeats and checkpoints, detect stale workers, and reclaim assignments from dead assignees. | `crates/jcode-plan/src/lib.rs:35-67,573-629` (`SwarmTaskProgress`, `MAX_DEAD_ASSIGNEE_RECLAIMS`). |
| FR-12 | The system shall detect and nudge stalled workers after a configurable stall interval, at most once per stall episode. | `crates/jcode-app-core/src/server/swarm_watchdog.rs` (`agents.swarm_stall_after_secs`, `agents.swarm_stall_nudge`). |
| FR-13 | The system shall label swarms and route direct messages across swarms, persisting labels under `~/.jcode/state/swarm-labels.json`. | `docs/SWARM_ARCHITECTURE.md:206-218`. |
| FR-14 | The system shall restrict spawning to the swarm root, scope broadcasts to a subtree, and reparent orphans. | `docs/SWARM_ARCHITECTURE.md:26-56`, `crates/jcode-app-core/src/server/swarm_cascade_tests.rs`. |
| FR-15 | The system shall not offer the deep task-graph mode, which was removed in v0.99.0. | The `task_graph`, `expand_node`, `complete_node`, and `inject_gap` actions and the `node_id`, `gate_id`, `nodes`, and `artifact` fields are gone (`crates/jcode-app-core/src/tool/communicate_tests.rs:1085-1091`); `/effort swarm-deep` no longer exists (`crates/jcode-tui/src/tui/app/input_help.rs:110`). |

## Open questions

Open Question 1 asks for the default worker limit and balancing algorithm.
Both are now documented.
Replace it with: "Resolved: live workers are capped by `agents.swarm_max_concurrent_agents` (default 32) with a hard ceiling of 1000 members; tasks are balanced by assignment affinity (current load, dependency carryover, subsystem and file-scope overlap) with a cap of 3 automatic reclaims per node."

## Testability

The acceptance criterion for FR-7 reads "Then the report is rejected or flagged for the coordinator".
It must be inverted: "Then the report is normalized, recorded on the member, and delivered to the coordinator without being rejected".

## Feasibility

No issues found.
