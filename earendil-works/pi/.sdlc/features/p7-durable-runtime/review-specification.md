---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25897ffew6r70TkGexlr7Q
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The architecture section describes a five-file package; the code has ten source directories and 80 modules
- **Evidence:** `packages/durable/src/` contains the flat modules `documents.ts`, `entries.ts`, `tasks.ts`, `errors.ts`, `ids.ts`, `search.ts`, `truncate.ts`, `timers.ts` and the directories `harness/` (24 modules, `scheduler.ts` is 2507 lines), `session/` (`session.ts` 1123, `transaction.ts` 1071, `forks.ts`, `observation.ts`), `storage/` (`memory.ts`, `scan.ts`, `sqlite/`, `jsonl/`), `env/` (`index.ts` 377, `node.ts` 1226, `node-watch.ts` 522, `line-scan.ts` 145, `decode.ts`), `tools/` (10 modules), `codemode/` (5), `images/` (6), `tool-search/` (2), `testing/` (6).
- **Artifact says:** "`types.ts` owns all record contracts and the `Storage` interface. `storage/memory.ts` implements `Storage` with `Map` tables and sorted ID arrays. `storage/sqlite/` implements the persistent `SqliteStorage` over a portable `SqliteDatabase` facade (node and cloudflare adapters). `session/` owns the Session mutation line (`createSession`); `index.ts` re-exports the public surface."
- **Required change:** Replace the architecture section with the real layout: the record contracts in `types.ts`; the document model in `documents.ts`; the agent layer in `harness/` (Harness, TaskScheduler, GenerationTask, ToolTask, CompactionTask, registry, submissions, live/agent/inbox/provider/usage documents, telemetry schema, task graph, views, events); the mutation line in `session/` (Session, Transaction, forks, observation); the storage backends in `storage/`; the execution environment in `env/`; the built-in tools, code mode, image processing, and tool search; the shared conformance suites in `testing/`; and the flat helpers `entries.ts`, `tasks.ts`, `errors.ts`, `ids.ts`, `search.ts`, `truncate.ts`, `timers.ts`. State the 18-entry `package.json` `exports` map, which is the real public surface.
- **Severity:** blocking

### The API Contracts `Storage` boundary is missing seven methods and names two wrongly
- **Evidence:** `packages/durable/src/types.ts:1179-1273` (`Storage` interface): `commit`, `mintId`, `conversation`, `scanConversations`, `entry`, `findLatestHeadMarker`, `scanEntries`, `task`, `scanTasks`, `submission`, `scanSubmissions`, `submissionByRequest`, `findDocument`, `document`, `scanDocuments`, `close`.
- **Artifact says:** "The `Storage` boundary is: `commit`, `mintId`, `conversation`, `scanConversations`, `entry`, `findLatestHeadMarker`, `scanEntries`, `task`, `scanTasks`, `input`, `inputByRequest`, and `close`."
- **Required change:** Replace `input` with `submission` and `inputByRequest` with `submissionByRequest`, and add `scanSubmissions`, `findDocument`, `document`, `scanDocuments`.
- **Severity:** blocking

### The Task record data model is wrong in shape and missing eight fields
- **Evidence:** `packages/durable/src/types.ts:690-704` (`TaskRecord<I, S, R>` = `TaskRecordBase` intersected with a union of `{ state: pending | running | waiting | sleeping; memos? }` or `{ state: completing | terminal; memos?: never }`); `src/types.ts:599-643` (`TaskState`); `src/types.ts:618-620` (the wait list is `state.on` plus `state.policy`, not a top-level `after`); `src/types.ts:636` (the outcome lives inside `state`, not beside it); `src/types.ts:645-687` (`TaskRecordBase`: `trace`, `links`, `owner`, `abortReason`, `abandonOnRestart`, `startedAt`, `endedAt`, `restarts`).
- **Artifact says:** "state | TaskState | Pending, running, or terminal | Complete durable execution state." plus separate top-level rows `after | readonly Id[]` and `outcome | TaskOutcome | Terminal tasks only`. The table has no `owner`, `trace`, `links`, `abortReason`, `abandonOnRestart`, `startedAt`, `endedAt`, or `restarts`.
- **Required change:** Rebuild the task record table from `TaskRecordBase` and the `TaskState` union: state is one of six values; `memos` exists only for the four live states; the outcome is inside `state` and exists only for `completing` and `terminal`; `state.on` and `state.policy` describe a wait; `state.until` describes a sleep. Add the eight missing base fields.
- **Severity:** blocking

### The "Input record" data model is the submission model and is missing its type discriminator
- **Evidence:** `packages/durable/src/types.ts:476-537` (`SubmissionRecord` is `type: "input" | "write"`; the `input` variant has `queued` | `placed` | `done` | `unanswered`, the `write` variant has `queued` | `done` | `unanswered` with no `placed` and no `answer`); `src/types.ts:465-473` (`SubmissionRecordBase` with `trace`); `src/types.ts:543-545` (`SubmissionSettlement`); `src/types.ts:798-803` (`SubmissionQuery`).
- **Artifact says:** "### Input record ... status | queued, placed, done, or unanswered | Not null | Lifecycle state." and lists `entry`, `answer`, `reason`, `detail` as unconditional fields.
- **Required change:** Rename the model to Submission record, add the `type` discriminator and `trace`, and state that `placed` and `answer` exist only on the `input` variant.
- **Severity:** blocking

### The Document record section omits the family, the base/delta content model, and the address
- **Evidence:** `packages/durable/src/documents.ts:39-58` (`defineDoc`) and `:60-80` (`defineDocFamily`); `packages/durable/src/types.ts:78` (`checkpointWhen`), `:85-89` (`DocFamilyDefinition`), `:746-750` (`DocumentCreate`), `:809-814` (`DocumentAddress`), `:824-833` (`DocumentContent` = `base` or `delta`), `:843-849` (`StoredDocument` with `value` and `deltasSinceBase`); `packages/durable/src/storage/sqlite/migrations.ts:66-89` (the `documents` and `document_revisions` tables).
- **Artifact says:** The Document record table lists only `id`, `kind`, `key`, `createdAt`, `retiredAt`, `scope`, `history`, `fork`. Nothing about families, addresses, base/delta content, checkpointing, or the revision tables.
- **Required change:** Add the document model: `defineDoc` and `defineDocFamily`, the `DocumentAddress` (`kind` + `scope` + optional `key`), `DocumentContent` as `base` or `delta`, the `checkpointWhen` predicate that decides base versus delta, `DocumentCreate` and `StoredDocument`, and the `documents`/`document_revisions` storage tables.
- **Severity:** blocking

### The architecture diagram shows one storage implementation and no scheduler
- **Evidence:** `packages/durable/src/storage/memory.ts` (`MemoryStorage`), `src/storage/sqlite/storage.ts` (`SqliteStorage`), `src/storage/jsonl/storage.ts` (`JsonlStorage`); `packages/durable/src/harness/scheduler.ts:253` (`TaskScheduler`); `packages/durable/src/harness/harness.ts:525-547` (`Harness.open`).
- **Artifact says:** A flowchart with `Session --> Storage`, `Storage --> MemoryStorage`, `types --> MemoryStorage`, `types --> Session`.
- **Required change:** Redraw it: the Harness owns the TaskScheduler and drives the Session; the Session owns the Transaction; the Storage boundary has three implementations; the Transaction computes the write set and calls `Storage.commit(writes, context)`.
- **Severity:** blocking

### The Sequences section has no harness, scheduler, or document flow
- **Evidence:** `packages/durable/src/harness/harness.ts:525-547` (open, then `openTasks`); `packages/durable/src/harness/scheduler.ts:374-412` (recovery: `running` back to `pending`, restart counting, parking at the limit); `packages/durable/src/harness/scheduler.ts:1466` (`#reserve`); `packages/durable/src/harness/scheduler.ts:1881-1930` (the decision on the Session line, including the no-durable-progress fault at `:1826-1831`); `packages/durable/src/session/transaction.ts:199` (`Transaction implements Tx`); `packages/durable/src/harness/generation.ts` and `src/harness/tool.ts:123` (generation creates `pi.tool` tasks; `api.executeTool()` creates a nested `pi.tool` task recorded in `NestedCallDoc`, `src/harness/tool.ts:106-112`); `packages/durable/src/session/observation.ts:1-292` (`session.snapshot`, `session.snapshotAsOf`, `session.documentState`, `session.watchDoc`).
- **Artifact says:** Two sequences only: "Atomic mixed-table commit" and "Fork-aware entry scan", both drawn against `MemoryStorage` and the record tables.
- **Required change:** Add the open-and-recover flow, the reserve-run-decide flow with the fault rule, the generation-to-tool-to-nested-call flow, and the document materialization flow.
- **Severity:** blocking

### The specification never mentions the normative `docs/spec.md` or the conformance suites
- **Evidence:** `packages/durable/docs/spec.md` (5612 lines; sections 1 Terms, 2 Core records, 3 Documents, 4 Transactions and storage ownership, 5 Tasks, 6 Submissions and inbox, 7 Extensions/hooks/tools/system prompt, 8 Built-in tasks, 9 Document observation and Chord, 10 Storage contract, 11 Backends, 12 API footguns, 13 Non-goals at `:5598`); `packages/durable/test/spec-usage.test.ts:1-5` ("The usage examples of docs/spec.md, compile-checked"); `packages/durable/src/testing/storage-conformance.ts:95` (`createStorageConformance`, 25 cases); `packages/durable/src/testing/env-conformance.ts:114` (`createEnvConformance`, 20 cases); `packages/durable/src/testing/runner.ts:13` and `:28` (`registerStorageConformance`, `registerEnvConformance`).
- **Artifact says:** The specification never names `docs/spec.md`, never mentions a conformance suite, and never mentions the `testing` subpath export.
- **Required change:** State that `packages/durable/docs/spec.md` is the normative specification and that this artifact summarises it; state that the storage and env conformance suites ship on `@earendil-works/pi-durable/testing` and that every backend is registered against them; state that `test/spec-usage.test.ts` compile-checks the spec's usage examples.
- **Severity:** blocking

### The Technical Decisions table omits the decisions the code actually made
- **Evidence:** `packages/durable/src/session/transaction.ts:199` and `:953` (one mutation line, one transaction, read-after-write); `packages/durable/src/storage/sqlite/database.ts` and `src/storage/sqlite/schema.ts:54-63` (the portable `SqliteDatabase` facade and the prefixable identifier registry); `packages/durable/src/storage/sqlite/migrations.ts:91-112` (migration 2 rebuilds the tasks table to add `sleeping`, because SQLite cannot alter a CHECK constraint in place); `packages/durable/src/storage/jsonl/storage.ts` (the sidecar publication protocol with `main.jsonl` markers); `packages/durable/src/harness/telemetry.ts:50-139` (content-free telemetry with carriers stored on tasks and submissions); `packages/durable/src/testing/` (conformance as the contract for every backend).
- **Artifact says:** Five decisions: ID space, Detachment, Immutability enforcement, Fork history, Document scope split.
- **Required change:** Add the decisions the code encodes: the single commit line; base-plus-delta document storage with a caller-supplied checkpoint predicate; the runtime-neutral storage boundary over a portable SQLite facade and a `FileSystem`; conformance as the contract every backend is held to; content-free telemetry carriers stored on task and submission records; the `sleeping` status added by a table-rebuilding migration; and the JSONL marker-then-sidecar publication protocol.
- **Severity:** blocking

### The Out of Scope list excludes code that ships, and omits the real non-goals
- **Evidence:** `packages/durable/src/harness/` (the harness ships), `packages/durable/src/storage/jsonl/` (a second persistent backend ships), `packages/durable/src/env/`, `src/tools/`, `src/codemode/`, `src/images/`, `src/tool-search/`, `src/testing/` (all ship); `packages/durable/docs/spec.md:5598-5612` (the real non-goals: no whole-Session DOM, no visible-undurable publication, no Session-kernel semantic event journal, no session-scoped rewindable documents, no automatic checkpoint heuristic, no automatic third-party view mounting, no CRDT/offline multi-writer merge, no SQL translation of arbitrary Chord operations, no JSONL global compaction or automatic corruption repair, no compatibility layer for earlier harness prototypes, no forced termination of non-cooperative extension code).
- **Artifact says:** "- Harness scheduling policies beyond the Session mutation line (`src/session/`, `src/harness/`). - Persistent storage backends beyond the in-package `SqliteStorage` (`src/storage/sqlite/`, node and cloudflare adapters). - Chord document delta mechanics, covered by the Chord package. - HTTP endpoints and OpenAPI contracts."
- **Required change:** Replace the list with the non-goals the code states in `docs/spec.md` section 13, and keep only "HTTP endpoints and OpenAPI contracts" from the current list, which is still true (the package has no HTTP surface).
- **Severity:** blocking

### The Overview still calls the package a "Pico durable-record layer"
- **Evidence:** `packages/durable/src/storage/sqlite/storage.ts:151` ("Portable SQLite implementation of the Pico storage contract") is the only surviving "Pico" mention in the package; `packages/durable/src/index.ts:41` exports `Harness`, `:126` `createSession`.
- **Artifact says:** "The package implements the Pico durable-record layer as TypeScript contracts with `MemoryStorage` and `SqliteStorage` backends behind the `Storage` boundary, plus the Session mutation line and the `ExecutionEnv` interface."
- **Required change:** Drop the "Pico" name, drop "durable-record layer", and name the three shipped surfaces: the record contracts, the `Session` and `Harness` runtime, and the `Storage` boundary with its three backends.
- **Severity:** advisory

### The cursor continuation is described as `{ after }` only; it also carries the scan order
- **Evidence:** `packages/durable/src/storage/scan.ts:39-41` (`nextCursor(id, order)` returns `{ after, order }`); `packages/durable/src/storage/scan.ts:13-37` (`scanStart` rejects a cursor whose stored order differs from the requested order, and rejects a malformed cursor with `StorageRequestError`); `packages/durable/src/types.ts:758-762` (`Cursor` is an opaque record that "carries the scan's order").
- **Artifact says:** "Cursor pagination returns `{ items, next }` where `next` is an opaque `{ after }` continuation."
- **Required change:** State that the cursor carries both the last ID and the scan order, that a cursor continues the scan in the order it was created with, and that a query asking for a different order against that cursor is rejected.
- **Severity:** advisory

### The conversation owner edge is described as two independent fields
- **Evidence:** `packages/durable/src/types.ts:404-408` (`owner` is one object holding both `conversationId` and `taskId`); `packages/durable/src/session/transaction.ts:308-324` (an owner edge is created only for `ownership.kind === "task"`, and the conversation ID is derived from the owner task's conversation); `packages/durable/src/types.ts:394` (`ConversationOwnership` = `ownerless` | `{ kind: "task", taskId }`).
- **Artifact says:** "| owner.conversationId | Id | FK when present | Creator conversation for abort and idle waits. | owner.taskId | Id | FK when present | Creator task for abort and idle waits. |"
- **Required change:** State that the owner edge is present or absent as a whole, names an owning task, and carries that task's conversation ID with it.
- **Severity:** advisory

### The first risk is written about a future that has already happened
- **Evidence:** `packages/durable/src/storage/sqlite/storage.ts` and `src/storage/jsonl/storage.ts` are both persistent backends held to the same conformance suite (`packages/durable/test/sqlite-storage.test.ts:113`, `test/jsonl-storage.test.ts:123`).
- **Artifact says:** "1. A future persistent backend may interpret cursor shape or commit ordering differently than `MemoryStorage`."
- **Required change:** Replace it with a risk that is still open, for example the cost of prototype-safe cloning per record, or the query-plan and durability choices the SQLite backend makes (WAL checkpoint cadence, synchronous mode), which `docs/spec.md:5398-5400` leaves as backend choices validated by conformance and benchmarks.
- **Severity:** advisory

## Open questions
- The specification does not say which of the package's modules are public API and which are internal. The `package.json` `exports` map (18 entries) defines the public surface, but `src/search.ts` (BM25), `src/truncate.ts`, and `src/timers.ts` are reachable only through other packages' own copies, so the intended boundary cannot be recovered from the code.
