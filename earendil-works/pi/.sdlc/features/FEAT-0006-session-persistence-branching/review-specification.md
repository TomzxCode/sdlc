---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### Entry `type` enum values do not match the code
- **Evidence:** `packages/coding-agent/src/core/session-manager.ts:64-194` — the literal `type` values are `message`, `thinking_level_change`, `model_change`, `usage`, `compaction`, `branch_summary`, `custom`, `custom_message`, `context_edit`, `label`, `session_info`.
- **Artifact says:** "message, thinkingChange, modelChange, compaction, branchSummary, label, custom, sessionInfo".
- **Required change:** Use the snake_case literals and add the missing `usage`, `custom_message`, and `context_edit` types.
- **Blocking.**

### `SessionHeader` field names are wrong and incomplete
- **Evidence:** `packages/coding-agent/src/core/session-manager.ts:43-50` — `SessionHeader` is `{ type: "session"; version?: number; id: string; timestamp: string; cwd: string; parentSession?: string }`. The identifier field is `id`, not `sessionId`.
- **Artifact says:** fields `version`, `sessionId`, `cwd`.
- **Required change:** Use `id` for the identifier and add `type: "session"`, `timestamp`, and the optional `parentSession` pointer (set by `SessionManager.forkFrom` at `:1848-1855` and by `createBranchedSession` at `:1675-1682`).
- **Blocking.**

### The compaction entry model does not match `CompactionEntry`
- **Evidence:** `packages/coding-agent/src/core/session-manager.ts:91-104` — `CompactionEntry` carries `summary`, `firstKeptEntryId`, `tokensBefore`, `details?`, `usage?`, `fromHook?`, `systemMessage?`. The `reason` and `willRetry` values live on the events (`packages/coding-agent/src/core/extensions/types.ts:791-818`), not on the persisted entry. The valid reasons are `manual | threshold | overflow`; there is no `retry` reason.
- **Artifact says:** compaction entry fields `reason` (enum `manual`, `threshold`, `overflow`, `retry`), `willRetry`, `summary`, `cutPoint`.
- **Required change:** Describe the entry as `summary`, `firstKeptEntryId`, `tokensBefore`, `details?`, `usage?`, `fromHook?`, `systemMessage?`. Move `reason`/`willRetry` to the event contract and drop the `retry` reason.
- **Blocking.**

### `SessionManager.append(entry)` and `read()` do not exist
- **Evidence:** `packages/coding-agent/src/core/session-manager.ts:1204-1462` — appends are per-type: `appendMessage`, `appendThinkingLevelChange`, `appendModelChange`, `appendUsage`, `appendCompaction`, `appendCustomEntry`, `appendCustomMessageEntry`, `appendContextEdit`, `appendSessionInfo`, `appendLabelChange`. Reads are `getEntries()` (`:1520`), `getBranch()` (`:1469`), `getTree()` (`:1529`), `buildSessionProjection()` (`:1493`), `buildSessionContext()` (`:1497`).
- **Artifact says:** "### SessionManager.append(entry) / read()" and "Append appends a JSONL line; read loads and indexes the tree for traversal, listing, and migration."
- **Required change:** List the per-type append methods and the read/traversal methods with their real names.
- **Blocking.**

### The runtime API contract names a `navigate(direction)` method that does not exist
- **Evidence:** `packages/coding-agent/src/core/agent-session-runtime.ts:196-411` — the runtime exposes `switchSession(sessionPath, options)`, `newSession(options)`, `fork(entryId, options)`, `importFromJsonl(inputPath, cwdOverride)`, and `dispose()`. Tree navigation lives on `AgentSession.navigateTree(targetId, options)` (`packages/coding-agent/src/core/agent-session.ts:3994`).
- **Artifact says:** "### Runtime: fork() / switch(id) / navigate(direction)" and "Each tears down the current runtime, emits the corresponding `session_before_*` event, and recreates services bound to the target session/cwd."
- **Required change:** Correct the method names and signatures, and move tree navigation to `AgentSession`. Note that `fork` and `switchSession` tear down and recreate, while `navigateTree` does not.
- **Blocking.**

### The branching flow ends with events and calls that do not exist
- **Evidence:** `packages/coding-agent/src/core/agent-session-runtime.ts:262-350` — the fork path emits `session_before_fork` (`:150-165`), tears down with `session_shutdown` reason `"fork"`, creates the branched file via `SessionManager.createBranchedSession(targetLeafId)` (`packages/coding-agent/src/core/session-manager.ts:1632`), and then emits `session_start` with `reason: "fork"`. `createBranchedSession` writes the root-to-leaf path, re-creates label entries, and points `parentSession` at the source file. There is no `session_fork` event and the runtime is not re-entered through `switch()`.
- **Artifact says:** "/fork <message-id> -> session_before_fork event -> create new session file from entries up to message-id -> runtime.switch() to new session -> session_fork event".
- **Required change:** Replace `runtime.switch()` with the teardown/recreate path, replace `session_fork` with `session_start` (reason `"fork"`), and describe `createBranchedSession` (root-to-leaf path, labels re-created, `parentSession` pointer, original file untouched).
- **Blocking.**

### The architecture diagram puts the runtime hot-swap under tree navigation
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:3994-4186` — `navigateTree` changes the leaf and refreshes the finalized context in place; it does not recreate cwd-bound services.
- **Artifact says:** the diagram shows `AgentSessionRuntime` hot-swapping on "fork()/switch()/navigate()".
- **Required change:** State that the runtime hot-swaps on fork, session switch, new session, and JSONL import, and that tree navigation stays inside the current runtime.
- **Advisory.**

### The compaction flow omits the overflow trigger and the failure event
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:3046-3074` (overflow recovery path), `:3127-3266` (`_runAutoCompaction` emits `session_compact_failed` on failure or abort). The preparation step is `prepareCompaction` (`:2810`, `:3141`) with `findProjectedCutPoint`, not a bare `findCutPoint`.
- **Artifact says:** "threshold exceeded OR /compact" and the flow ends at `session_compact event (with reason, willRetry)`.
- **Required change:** List the three triggers (manual, threshold, overflow) and add the `session_compact_failed` event to the flow.
- **Advisory.**

## Open questions

- None. Every claim above was checked against `packages/coding-agent/src/core/session-manager.ts`, `src/core/agent-session.ts`, `src/core/agent-session-runtime.ts`, `src/core/compaction/`, and `src/core/extensions/types.ts`.
