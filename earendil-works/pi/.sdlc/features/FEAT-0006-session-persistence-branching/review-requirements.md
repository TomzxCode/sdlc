---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### FR-02 omits three implemented session entry types
- **Evidence:** `packages/coding-agent/src/core/session-manager.ts:183-194` — the `SessionEntry` union has 11 members. `UsageEntry` (`:80-89`, written by `appendUsage` at `:1244`), `CustomEntry` (`:128-132`, extension state, excluded from LLM context), and `ContextEditEntry` (`:175-180`, append-only replacement/omission of an earlier entry's context content) are not in FR-02's list.
- **Artifact says:** FR-02 lists "messages, thinking-level changes, model changes, compaction summaries, branch summaries, labels, custom messages, and session info."
- **Required change:** Add `usage` entries (model-attributed token usage, not in LLM context), `custom` entries (extension state, not in LLM context), and `context_edit` entries to FR-02.
- **Blocking.**

### FR-08 requires the removed `session_fork` and `session_switch` events
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:754-860` defines the session event union: `session_start`, `session_info_changed`, `session_before_switch`, `session_before_fork`, `session_before_compact`, `session_compact`, `session_compact_failed`, `session_shutdown`, `session_before_tree`, `session_tree`. There is no `session_fork` and no `session_switch`. `packages/coding-agent/CHANGELOG.md:2836` records "Removed extension post-transition events `session_switch` and `session_fork`. Use `session_start` with `event.reason`."
- **Artifact says:** FR-08 requires `session_before_compact/compact`, `session_before_fork/fork`, `session_before_switch/switch`, `session_before_tree/tree`.
- **Required change:** Replace the `fork` and `switch` pairs with the events the code emits: `session_before_fork` followed by `session_start` (reason `"fork"`), and `session_before_switch` followed by `session_start` (reason `"new"` or `"resume"`). Also list `session_start`, `session_info_changed`, `session_shutdown`, and `session_compact_failed`.
- **Blocking.**

### FR-07 acceptance criterion names `/tree` as a runtime hot-swap trigger
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:3994-4186` — `AgentSession.navigateTree` moves the leaf pointer inside the same `SessionManager` and never touches `AgentSessionRuntime`. The runtime is replaced only by `switchSession` (`packages/coding-agent/src/core/agent-session-runtime.ts:196`), `newSession` (`:226`), `fork` (`:262`), and `importFromJsonl` (`:359`).
- **Artifact says:** AC FR-07: "Given an interactive session / When the user runs `/tree` and switches branches / Then the runtime tears down cwd-bound services and recreates them for the target branch without leaking state."
- **Required change:** Scope the criterion to `/new`, `/resume`, `/fork`, and cross-cwd session replacement. Describe `/tree` as a leaf move within the same runtime that emits `session_before_tree` and `session_tree`.
- **Blocking.**

### FR-10 mentions only HTML export
- **Evidence:** `packages/coding-agent/src/core/session-export.ts:9-45` provides `serializeSessionBranch` and `exportSessionToJsonl`; `/export` accepts a `.jsonl` output path (`packages/coding-agent/src/modes/interactive/interactive-mode.ts:3229`, `:6539`).
- **Artifact says:** FR-10: "The system shall support session export to HTML."
- **Required change:** State that export produces HTML (`src/core/export-html/`) or JSONL (`src/core/session-export.ts`).
- **Advisory.**

### Acceptance criteria are missing for most requirements
- **Evidence:** `requirements.md:59-82` states "Every FR and NFR shall have at least one acceptance criterion" but lists criteria only for FR-01, FR-05, FR-06, FR-07, and NFR-01. FR-02, FR-03, FR-04, FR-08 through FR-12, NFR-02, NFR-03, and NFR-04 have none.
- **Artifact says:** "Every FR and NFR shall have at least one acceptance criterion."
- **Required change:** Add the missing criteria or relax the statement so the artifact matches its own contents.
- **Advisory.**

## Open questions

- The "Conflicts" and "Open Questions" sections are still placeholders ("None identified yet."). The remote/session-sync question is still unanswered by the code: sessions remain local JSONL files under `~/.pi/agent/sessions/`, with no remote store in the repository.
