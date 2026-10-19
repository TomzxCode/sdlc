---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.
The plan DAG itself survived; what changed is the deep task-graph mode, the report-validation story, and the module and vocabulary references.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Architecture | "typed comm channels (comm_graph, comm_plan, comm_session, comm_control, comm_sync, comm_await)" | `crates/jcode-app-core/src/server/comm_graph.rs` does not exist. Present: `comm_await.rs`, `comm_control.rs`, `comm_plan.rs`, `comm_session.rs`, `comm_sync.rs`, plus `client_comm.rs`, `client_comm_channels.rs`, `client_comm_context.rs`, `client_comm_message.rs`, `client_comm_swarms.rs`. | Reword to "typed comm channels (comm_plan, comm_session, comm_control, comm_sync, comm_await, client_comm*)". |
| Data Models | `PlanItem.status` typed as "enum \| pending/in-progress/done/failed" | `PlanItem.status` is a `String` (`crates/jcode-plan/src/lib.rs:21`). The real vocabulary, from the status predicates at `crates/jcode-plan/src/lib.rs:217-240` and `SwarmLifecycleStatus` (`crates/jcode-swarm-core/src/lib.rs:124-139`): queued, ready, pending, todo, running, running_stale, completed, done, failed, stopped, crashed, blocked, spawned. | Reword the type to string and list the real vocabulary. |
| Data Models | the table lists only `item`, `version`, `status` | `PlanItem` also has `content`, `priority`, `id`, `subsystem`, `file_scope`, `blocked_by`, `assigned_to` (`crates/jcode-plan/src/lib.rs:18-31`); `VersionedPlan` has `items`, `version`, `participants`, `task_progress` (`:106-113`); `SwarmTaskProgress` adds `assigned_session_id`, `assigned_at_unix_ms`, `started_at_unix_ms`, `last_heartbeat_unix_ms`, `last_detail`, `last_checkpoint_unix_ms`, `checkpoint_summary`, `completed_at_unix_ms`, `stale_since_unix_ms`, `heartbeat_count`, `checkpoint_count`, `dead_assignee_reclaims` (`:35-67`). | Add the missing rows. |
| Data Models | "item \| PlanItem \| bounded by MAX_PLAN_ITEMS = 1024" | The bound is not a struct field. It is enforced at plan approval and merge time (`crates/jcode-app-core/src/server/comm_plan.rs:407`, `debug_swarm_write.rs:402`). | Reword as "items \| list of PlanItem \| merged plan rejected when the count exceeds MAX_PLAN_ITEMS = 1024 (enforced at approve/merge time)". |
| API Contracts | "ServerEvent swarm variants — `swarm_status`, `swarm_plan`, member status snapshots." | A third swarm event exists: `swarm_plan_proposal` (`crates/jcode-protocol/src/wire/events.rs:328-337`). | Add `swarm_plan_proposal`. |
| Sequences | "Worker runs task → completion report (tldr + marker) / Server validates report (jcode-swarm-core) → sends Comm message to coordinator" | The marker is added to the assignment prompt, and the server normalizes and records rather than validating and rejecting. | Replace with the corrected sequence: the assignment prompt carries the completion marker, the worker reports through the swarm tool, the server normalizes the report and records it on the member, and the coordinator is notified. |
| Technical Decisions | "Report validation \| tldr rule + completion marker \| Prevents malformed member output from corrupting the plan." | There is no rejection path. | Reword to "Report normalization \| tldr derivation + 4000-character cap + prompt-level completion marker \| Keeps the coordinator's inbox readable without ever blocking a worker's report." |
| Technical Decisions | "Typed comm channels \| `comm_*.rs` modules with graph/plan/session/control separation" | There is no graph module. | Reword to "plan/session/control/sync/await separation". |
| Technical Decisions | "Persistence \| swarm state in durable server state" | The concrete path is `~/.jcode/state/swarm/<swarm_id>.json` (`crates/jcode-app-core/src/server/swarm_persistence.rs:12,148`), with a legacy runtime-dir location migrated on load (`:14,168-200`). | Name the path and the migration. |
| Risks and Unknowns | "Scheduling and parallelism heuristics are not fully documented in the code; inferred from module structure." | They are documented in `docs/SWARM_ARCHITECTURE.md` and implemented as affinity-based assignment (`crates/jcode-plan/src/lib.rs:713-770`), a bounded `run_plan` driver, and the live-worker cap `agents.swarm_max_concurrent_agents` (`crates/jcode-app-core/src/server/comm_session.rs:1416-1426`). | Reword: the heuristics are documented and implemented; the remaining unknown is how to tune the affinity weights as swarm size grows. |

## Missing Information

- The v0.99.0 removal of the deep task-graph mode is not recorded: the `task_graph`, `expand_node`, `complete_node`, and `inject_gap` actions and the `node_id`, `gate_id`, `nodes`, and `artifact` schema fields are gone, and `/effort swarm-deep` no longer exists.
- The swarm root effort default (`agents.swarm_root_effort` = `low`, new in v0.99.0) is not documented (`crates/jcode-config-types/src/lib.rs:577-579,724-735`).
- The idempotent swarm mutation replay state (`crates/jcode-app-core/src/server/swarm_mutation_state.rs`, 30 second final-state TTL, 30 minute pending TTL) is not documented.
- The inline gallery and strip configuration (`agents.swarm_gallery_max_pct`, `agents.swarm_strip_layout`) is not documented.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.
