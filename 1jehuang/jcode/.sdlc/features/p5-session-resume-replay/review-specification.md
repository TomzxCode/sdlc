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
| Architecture | the map omits `jcode-storage`, the replay builder, the restart snapshot, and the prewarm module | `crates/jcode-storage/` is the on-disk layer (`active_pids.rs`, `session_lease.rs`, plus the atomic-write and `.bak` recovery primitives in `src/lib.rs`). `crates/jcode-base/src/session/prewarm.rs` is not in the `session/` list. `crates/jcode-app-core/src/replay.rs`, `restart_snapshot.rs`, `session_active_pids.rs`, and `catchup.rs` are missing. `crates/jcode-message-types/` is not mentioned at all, and neither is `crates/jcode-tui-session-picker/`. | Extend the map with the missing stores and modules. |
| Data Models | the `StoredMessage` table with `id`, `role`, `content`, `token_usage`, `timestamp` (timestamp "not null") | `StoredMessage` (`crates/jcode-session-types/src/lib.rs:267-280`) has `timestamp: Option<DateTime<Utc>>` (nullable), and two fields are missing: `display_role: Option<StoredDisplayRole>` and `tool_duration_ms: Option<u64>`. `StoredTokenUsage` (`:289-301`) has `prompt_tokens`, `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`. | Replace the table and add the two missing fields. |
| Data Models | `SessionJournalMeta` described as capturing "parent id, title, status, compaction state, provider session id, model, reasoning effort, working dir, last pid, timestamps, and flags (canary, debug, saved)" | `crates/jcode-base/src/session/journal.rs:10-49` still has all of those, plus `custom_title`, `system_prompt`, the new `compaction_unchanged` flag, `model_usage_turn_id`, `provider_key`, `subagent_model`, `agent_model_overrides`, `improve_mode`, `autoreview_enabled`, `autojudge_enabled`, `testing_build`, `short_name`, and `save_label`. | Extend the description. |
| API Contracts | lists only `jcode replay [session]` and `jcode session rename` | The resume entry points are missing: the global `--resume` flag (`src/cli/args.rs:74-76`), the `jcode session rename` flags (`src/cli/args.rs:857-875`), and `jcode restart save/restore/status/clear` (`src/cli/args.rs:827-841`). `jcode replay` also accepts `--cols`, `--rows`, `--centered`, `--no-centered`. | Add the missing CLI sections and flags. |
| Sequences | "jcode --resume <name|id> → connect to server → load journal → replay events → client state rebuilt → stream continues from where it left off" | The current path loads a local stub first, advertises the held prefix, and applies only the returned tail, with a daemon-side prewarm supplying the full parse. | Replace with the corrected sequence. |
| Technical Decisions | four rows: snapshot+journal, journal replay events, import from external tools, memorable short names | Three more decisions are load-bearing and undocumented: prewarm at reload, delta history by fingerprint claim, and atomic write with `.bak` recovery plus single-write journal appends. | Append the three rows. |
| Out of Scope | "Cloud-backed session sync (a separate Jade cloud integration)." | Cloud session movement is implemented and touches the session store through the lease. | Reword to name the commands: "Cloud-backed session sync and cross-machine session movement (`jcode cloud move|return|where|attach`, and the `~/.jcode/session_leases` lease store) — a separate Jade cloud integration." |

## Missing Information

- The resume and history wire contract is undocumented: `Request::Subscribe` and `Request::ResumeSession` carry `client_has_local_history` and an optional `history_base`; the server answers with `ServerEvent::History` whose `messages_base_count` is set and whose `images_unchanged` is true; a fingerprint mismatch falls back to a full transcript (`crates/jcode-protocol/src/wire.rs:168-259`, `crates/jcode-protocol/src/wire/events.rs:558-572`).
- Three data models are missing: `StoredCompactionState` (`crates/jcode-session-types/src/lib.rs:303-311`), `SessionStatus` (`:154-167`), and `EnvSnapshot` (`:224`).
- The session lease and migration epoch, the active-session presence and streaming guard, the crash-recovery `.bak` pruner, and the session load burst attribution are not described.

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
