---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
The v0.99.0 headline "reload and resume large sessions much faster" shipped a substantial mechanism that no requirement covers.

## Completeness

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-10 | The system shall restore a large session without re-sending the whole transcript: the client shall show its locally persisted transcript immediately, shall advertise the transcript prefix it already holds, and the server shall return only the missing history tail. Sessions above a size threshold shall be pre-parsed in the background after a server reload so a resume does not pay the parse cost. | Prewarm: `crates/jcode-base/src/session/prewarm.rs` (`MIN_PREWARM_BYTES = 2 MiB`, `MAX_PREWARM_SESSIONS = 64`, `PREWARM_WORKERS = 2`, `ENTRY_TTL = 30 s`, wired into `Session::load_for_resume` at `crates/jcode-base/src/session/persistence.rs:503-513`). Paint-first: `Session::load_startup_stub` (`:520-534`) and `Session::load_for_remote_startup` (`:536+`). Delta wire: `HistoryBase` (`crates/jcode-protocol/src/lib.rs:84-93`), `history_prefix_fingerprint` (`:116-124`), `Request::Subscribe.history_base` (`crates/jcode-protocol/src/wire.rs:173`), `Request::ResumeSession.client_has_local_history` (`:250`), `ServerEvent::History.messages_base_count` and `images_unchanged` (`crates/jcode-protocol/src/wire/events.rs:558-572`). |

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-2 | "The system shall resume a session by id or memorable short name (`--resume`, session picker)." | The picker now opens immediately with the cached list and refreshes in the background (v0.98.0). | "The system shall resume a session by id or memorable short name (`--resume`, session picker). The session picker shall open immediately with the cached list and refresh from a background scan without blocking the UI." |
| FR-9 | "The system shall support session search across persisted sessions." | Search is a first-class agent tool backed by a persistent incremental index, not a one-off query (`crates/jcode-app-core/src/tool/session_search.rs`, `session_search_index.rs` with a Bloom filter over hashed tokens, `crates/jcode-session-types/src/lib.rs:351-953`). | "The system shall support session search across persisted sessions and external agent transcripts, backed by a persistent incremental index that reuses unchanged entries so a large store stays searchable without re-reading every file." |

## Non-functional requirements

NFR-2 reads "Session files can grow large; persistence and search must not degrade the agent loop."
Extend it: "Large sessions shall be pre-parsed in the background at reload, resumed with a delta history transfer, and searched through a persistent incremental index."

## Constraints

The constraints section names the snapshot and journal paths but omits three other on-disk stores:

- Add: "Restart state: `~/.jcode/restart-snapshot.json`."
- Add: "Cross-machine migration leases: `~/.jcode/session_leases/<id>.json`."
- Reword the first bullet to: "Storage layout: `~/.jcode/sessions/<id>.json` snapshot plus `<id>.journal.jsonl`; a crash-recovery copy `<id>.bak` sits next to the snapshot."

## Open questions

Open Question 1 asks for the journal compaction and truncation policy.
The journal now omits unchanged compaction state through a `compaction_unchanged` flag to avoid overflowing the cap (`crates/jcode-base/src/session/journal.rs:19-25`).
Replace it with: "What is the exact journal size cap and the checkpoint-rewrite threshold? The journal now omits unchanged compaction state (`compaction_unchanged`) to avoid overflowing the cap, but the numeric cap is still not documented."

## Testability

FR-10 needs at least one Gherkin acceptance criterion, for example: "Given a persisted session larger than the prewarm threshold after a server reload / When the client resumes it / Then the local transcript is displayed before the server round trip completes, and the server sends only the history messages after the advertised prefix (verified by matching fingerprint, otherwise a full transcript is sent)".

## Feasibility

No issues found.
