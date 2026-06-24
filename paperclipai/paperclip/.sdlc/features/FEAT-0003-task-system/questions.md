# Open Questions: Task System (Issues)

## Sync drift (2026-06-24)

The following items were identified during codebase reconciliation and reflect functionality present in the code but not documented in the current requirements.md or specification.md.

1. **Board Chat / Conference Room** — An experimental board-level chat assistant exists at `server/src/routes/board-chat.ts` and `ui/src/pages/BoardChat.tsx`. It spawns a Claude subprocess with the board skills prompt and streams results via SSE to a "Board Operations" issue. This contradicts the spec's "tasks + comments only (no separate chat system)" V1 decision. Needs explicit documentation as an experimental feature.

2. **Issue thread interactions** — The codebase supports interaction types `request_confirmation`, `ask_user_questions`, `suggest_tasks`, `request_checkbox_confirmation`, and `signal_board_attention` via `issue_thread_interactions` table and service (`server/src/services/issue-thread-interactions.ts`). The feature spec does not mention these.

3. **Task watchdogs** — A scoped task watchdog system exists (`server/src/services/task-watchdogs.ts`, `task-watchdog-scope.ts`, schema `issue_watchdogs`) that allows authorized agents to restore live task paths within a watched issue subtree. The spec mentions `doc/execution-semantics.md` but does not describe the watchdog implementation.

4. **Issue tree control** — `server/src/services/issue-tree-control.ts` and route `issue-tree-control.ts` provide tree-level operations (hold, release, block). Not documented in the feature spec.

5. **Issue recovery actions** — Recovery action tracking exists at `server/src/services/issue-recovery-actions.ts` and schema `issue_recovery_actions`. Not documented.

6. **Issue plan decompositions** — Schema `issue_plan_decompositions` exists. Not documented.

7. **External objects integration** — External objects (`external_objects`, `external_object_mentions`) are linked to issues. Not documented.

8. **Work products** — `server/src/services/work-products.ts` provides artifact-backed and workspace-file reference work products. The spec mentions them briefly but the implementation details are not captured.
