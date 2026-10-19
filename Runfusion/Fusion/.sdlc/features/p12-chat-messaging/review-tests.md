---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

- TC-1 does not match the file it names. `packages/core/src/chat/__tests__/chat-memory-focus.test.ts:1-12` tests persistence of the per-conversation memory focus on `chat_sessions.memory_focus` for RUFU-068, not a rule that selects focused messages in a room. No test in the repository covers the described behavior.
- TC-2 has no test. The traversal check lives in the unexported `resolveRoomAttachmentPath` at `packages/dashboard/src/routes/register-chat-room-routes.ts:31-42`, and no test file asserts the `Invalid attachment path` rejection, so nothing proves that a crafted filename is refused or that no write lands outside the room directory.
- TC-3 does not cover the requirement it is mapped to. `packages/core/src/chat/__tests__/chat-message-tie-pagination.pg.test.ts:1-30` exercises the `chat_messages` table for the Stash backfill route, while the room query orders by `created_at` alone at `packages/core/src/async-stores/async-chat-store.ts:712-731` and has no id tiebreak, so room message pagination has no tie-stability test.
- TC-4 has no test. The four room test files named in `docs/architecture.md:1045` (`packages/core/src/__tests__/chat-store.rooms.test.ts`, `packages/dashboard/src/__tests__/chat.rooms.test.ts`, `packages/dashboard/src/__tests__/chat-routes.rooms.test.ts`, `packages/dashboard/app/components/__tests__/ChatView.rooms.test.tsx`) do not exist. The only test that calls a room endpoint is `packages/dashboard/src/__tests__/large-text-body-parser-integration.test.ts:114`, which posts one message and asserts the body size limit.
- TC-5 has no test. No test drives a room send through a rendered surface, and the dashboard no longer renders rooms. `packages/dashboard/app/components/ChatView.tsx:846-850` states that ChatView no longer subscribes to or renders persistent Rooms. Room reply behavior is covered only at the manager level, in `packages/dashboard/src/__tests__/chat-manager.test.ts:4487`, `:4554`, `:4664`, `:4711`, and `:4770`.
- Coverage Matrix drift: FR-6 has no test case, so the saved-script endpoints at `packages/dashboard/src/routes/register-messaging-scripts.ts:19-170` are untested in the plan.
- Coverage Matrix drift: NFR-2 is mapped to TC-4, which does not exist, so no test covers the rate-limit split between read and mutation room routes. `packages/dashboard/src/routes/register-chat-room-routes.ts:127` and `:148` show the two limits in use.
- Coverage Matrix drift: the plan has no row for the mailbox messaging endpoints at `packages/dashboard/src/routes/register-messaging-scripts.ts:232-608`, for the CLI commands at `packages/cli/src/commands/chat.ts` and `packages/cli/src/commands/message.ts`, or for the `fn_post_room_message` tool at `packages/engine/src/agent-tools.ts:6602`.
- Significant new test area not covered: room transcript compaction. `packages/dashboard/src/__tests__/chat-room-compaction.test.ts` tests `buildCompactedRoomTranscript`, and the compaction rules are described in `docs/architecture.md:364`.
- Significant new test area not covered: the room client hook. `packages/dashboard/app/hooks/__tests__/useChatRooms.test.ts`, `packages/dashboard/app/hooks/__tests__/useChatRooms.cache.test.ts`, and `packages/dashboard/app/hooks/__tests__/useChatRooms.resume-instrumentation.test.ts` cover room selection, optimistic sends, deduplication, SSE handling, and caching.
- Significant new test area not covered: the room API client. `packages/dashboard/app/api/__tests__/chat-rooms-api.test.ts` covers the room request builders and the large room log serialization.
- Significant new test area not covered: room attachment content reading. `packages/dashboard/src/__tests__/chat-attachment-content.test.ts:127-240` covers basename resolution and text inlining for the `chat-room-attachments` root.
- Significant new test area not covered: the room creation modal. `packages/dashboard/app/components/__tests__/CreateRoomModal.test.tsx` covers the dialog that no production component renders.
- Significant new test area not covered: the mailbox archive routes. `packages/dashboard/src/routes/__tests__/messaging-archive-routes.test.ts` covers the `/api/messages/:id/archive` and `/unarchive` routes from `packages/dashboard/src/routes/register-messaging-scripts.ts:525-545`.
