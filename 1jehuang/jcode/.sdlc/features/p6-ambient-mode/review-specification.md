---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "Ambient mode is implemented in `crates/jcode-app-core/src/` (`ambient.rs`, `ambient_runner.rs`, `ambient_scheduler.rs`, and the `ambient/` module) with shared types in `crates/jcode-ambient-types`." | `ambient_runner.rs` and `ambient_scheduler.rs` are now 3-line re-export shims (`ambient_runner.rs:3`, `ambient_scheduler.rs:1-3`). The implementations live in `crates/jcode-app-core/src/ambient/{runner,scheduler,directives,manager,paths,persistence,prompt}.rs`. `crates/jcode-ambient-types` holds only `UsageRecord`, `UsageSource`, and `RateLimitInfo`. | Reword to name the `ambient/` module and the shims, and to say that token-accounting types live in `jcode-ambient-types`. |
| Architecture | "├── [ambient] config (directives, schedules)" | `[ambient]` has no directive or schedule keys. The real keys are `enabled`, `provider`, `model`, `allow_api_keys`, `api_daily_budget`, `min_interval_minutes` (5), `max_interval_minutes` (120), `pause_on_active_session` (true), `proactive_work` (true), `work_branch_prefix` ("ambient/"), `visible` (true) (`crates/jcode-config-types/src/lib.rs:1342-1382`). | Reword to list the real keys and to mention the runtime queue and directives under `~/.jcode/ambient/`. |
| Data Models | heading "Ambient State (`jcode-ambient-types`)" | `AmbientState`, `AmbientStatus`, `AmbientCycleResult`, `CycleStatus`, `ScheduleRequest`, `ScheduledItem`, `Priority`, and `ScheduleTarget` all live in `crates/jcode-app-core/src/ambient.rs:70-189`. | Reword the heading to `crates/jcode-app-core/src/ambient.rs`. |
| Data Models | "status \| enum \| not null \| Running / idle / stopped." | `AmbientStatus` is `Idle`, `Running { detail }`, `Scheduled { next_wake }`, `Paused { reason }`, `Disabled` (`crates/jcode-app-core/src/ambient.rs:70-83`). There is no "stopped"; `jcode ambient stop` sets `Disabled` (`ambient/runner.rs:153-159`). | Replace with the real variants. |
| Data Models | the `directives`, `log`, and `schedule` rows | None of these are fields of `AmbientState` (`ambient.rs:137-144` holds status, last_run, last_summary, last_compactions, last_memories_modified, total_cycles). The real on-disk layout is `ambient/paths.rs`: `state.json`, `queue.json`, `directives.json`, `transcripts/*.json`, `usage.json`, `ambient.lock`, plus the visible-cycle handoff files. | Replace the three rows with the seven real files and their roles. |
| Sequences | "Results logged → state persisted → status events published to UI" | There is no ambient server event; `crates/jcode-protocol/src/wire/events.rs` has no `Ambient` variant. The TUI widget reads persisted state from disk behind a TTL cache (`crates/jcode-tui/src/tui/app/helpers.rs:1406-1469,1332-1404`). | Reword: "Results logged to `~/.jcode/ambient/transcripts` → state persisted to `~/.jcode/ambient/state.json` → the TUI ambient widget reads the persisted state (TTL-cached) to render status." |
| Technical Decisions | "Overnight hook \| overnight processing module \| Long-running consolidation fits idle windows." | There is no overnight hook. | Delete the row. |
| Technical Decisions | "Same-process scheduler \| `ambient_scheduler.rs` in app-core" | The implementation is `crates/jcode-app-core/src/ambient/scheduler.rs`, re-exported by `ambient_scheduler.rs`. | Reword to name both. |
| Technical Decisions | "Durable ambient state \| persisted status/log" | The real paths are `~/.jcode/ambient/{state,queue,directives}.json` plus `transcripts/*.json`. | Reword, and say "survives restarts" rather than "reloads". |

## Missing Information

- The ambient tool surface is not in API Contracts: `end_ambient_cycle`, `schedule_ambient`, `request_permission`, `send_message` (`crates/jcode-app-core/src/tool/ambient.rs`).
- The visible-cycle mode (`jcode ambient run-visible` and the `VisibleCycleContext` handoff files) is not described.
- The reply ingestion path (the IMAP reply poller and the message-channel reply loops that create `UserDirective`s) is not described.
- The ambient permission review flow (pending requests, `expire_dead_session_requests`, approve and deny) is not described.

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
