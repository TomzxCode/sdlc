---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25897ffew6r70TkGexlr7Q
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The overview describes a record-only package; the shipped package is a full durable runtime
- **Evidence:** `packages/durable/src/index.ts:41` (`Harness`), `:126` (`createSession`), `:127` (`MemoryStorage`); `packages/durable/src/harness/scheduler.ts:253` (`TaskScheduler`, the 2507-line largest file); `packages/durable/src/harness/generation.ts` (`GenerationTask`), `src/harness/tool.ts:123` (`ToolTask`), `src/harness/compaction.ts` (`CompactionTask`); `packages/durable/src/storage/sqlite/storage.ts` (`SqliteStorage`), `src/storage/jsonl/storage.ts` (`JsonlStorage`); `packages/durable/src/env/index.ts:374` (`ExecutionEnv`); `packages/durable/src/tools/index.ts:31` (`createCodingTools`); `packages/durable/src/codemode/codemode.ts:248` (`createCodemodeExtension`); `packages/durable/src/images/index.ts:32` (`createPhotonImages`); `packages/durable/src/tool-search/tool-search.ts:11`; `packages/durable/src/harness/telemetry.ts:50` (`DURABLE_TELEMETRY_SCHEMA`); `packages/durable/src/testing/storage-conformance.ts:95` and `src/testing/env-conformance.ts:114` (the shared conformance suites).
- **Artifact says:** "The package currently ships the durable record contracts, the `Storage` persistence boundary, and the detached in-memory `MemoryStorage` reference implementation."
- **Required change:** Replace the overview with the shipped scope: the record contracts, the `Session` mutation line, the `Harness` and its scheduler, the three storage backends (memory, SQLite, JSONL), the `ExecutionEnv` abstraction, the built-in coding tools, code mode, image processing, deferred tool search, the telemetry schema, and the shared conformance suites. State that `packages/durable/docs/spec.md` (5612 lines) is the normative specification.
- **Severity:** blocking

### FR-4 states three task states; the model has six
- **Evidence:** `packages/durable/src/types.ts:599-643` (`TaskState<S, R>` = `pending` | `running` | `waiting` | `sleeping` | `completing` | `terminal`); `src/types.ts:614-621` (`waiting` carries `on: readonly TaskId[]` and `policy: JoinPolicy`), `src/types.ts:622-631` (`sleeping` carries `until: number`), `src/types.ts:632-637` (`completing` holds the outcome before `terminal`); `src/types.ts:368` (`JoinPolicy` = `failFast` | `allSettled`); `src/harness/scheduler.ts:67` (`LIVE_STATUSES` lists all five live states).
- **Artifact says:** "FR-4 ... The system shall model tasks as pending, running, and terminal states with completed, failed, aborted, orphaned, and faulted outcomes." The FR-4 acceptance criterion advances a task "from running and then terminal".
- **Required change:** List all six states and their extra fields. The outcome list (completed, failed, aborted, orphaned, faulted) is correct and stays.
- **Severity:** blocking

### FR-3 describes host inputs; the model is a submission with a type discriminator
- **Evidence:** `packages/durable/src/types.ts:476-537` (`SubmissionRecord` is `type: "input" | "write"`; the `input` variant has `queued` | `placed` | `done` | `unanswered`, the `write` variant has `queued` | `done` | `unanswered` with no `placed`); `src/types.ts:543-545` (`SubmissionSettlement`), `:548-552` (`SubmissionCreate`), `:798-803` (`SubmissionQuery`); `src/types.ts:953-968` (`tx.createSubmission`, `tx.settleSubmission`, `tx.placeSubmission`); `src/harness/submissions.ts` (`admitSubmission`).
- **Artifact says:** "FR-3 ... The system shall model host inputs through the queued, placed, done, and unanswered lifecycle states with conversation-scoped request ID deduplication." The acceptance criterion says "advance an input through its lifecycle".
- **Required change:** Rename the requirement to submissions, state the two types and the different state sets, and keep the conversation-scoped request-ID dedup rule (`requestId` on `SubmissionRecordBase`, `src/types.ts:471-472`).
- **Severity:** blocking

### FR-6 misstates the `Storage` boundary
- **Evidence:** `packages/durable/src/types.ts:1179-1273` (`Storage` interface): `commit`, `mintId`, `conversation`, `scanConversations`, `entry`, `findLatestHeadMarker`, `scanEntries`, `task`, `scanTasks`, `submission`, `scanSubmissions`, `submissionByRequest`, `findDocument`, `document`, `scanDocuments`, `close`.
- **Artifact says:** "FR-6 ... input lookup by ID and request key" and the `Storage` boundary has no submission-scan or document methods.
- **Required change:** Replace `input`/`inputByRequest` with `submission`/`submissionByRequest`, add `scanSubmissions`, and add the three document methods (`findDocument`, `document`, `scanDocuments`).
- **Severity:** blocking

### FR-5 understates the document model
- **Evidence:** `packages/durable/src/documents.ts:39-58` (`defineDoc`) and `:60-80` (`defineDocFamily`); `packages/durable/src/types.ts:57-61` (`DocumentSemantics`: scope session/conversation/task x history latest/rewindable x fork asOf/current/initial), `:82` (`DocDefinition`), `:85-89` (`DocFamilyDefinition`), `:78` (`checkpointWhen`), `:707-743` (`DocumentRecord`), `:746-750` (`DocumentCreate`), `:809-814` (`DocumentAddress`), `:824-833` (`DocumentContent` = `base` or `delta`), `:843-849` (`StoredDocument`).
- **Artifact says:** "FR-5 ... The system shall model document incarnations with session, conversation, and task scopes plus history and fork policies."
- **Required change:** Add the family concept, the base/delta content model with checkpointing, the retire/recreate lifecycle, and the scope/history/fork matrix as it is encoded in `DocumentSemantics`.
- **Severity:** blocking

### FR-10 calls `StorageWrite` a table-mutation union; it also carries document commands
- **Evidence:** `packages/durable/src/types.ts:852-868` (`StorageWrite` = `conversation` | `entry` | `task` | `submission` | `document.create` | `document.copy` | `document.change` | `document.retire`); `src/types.ts:893-898` (`TableCommitChange` is the table-only subset).
- **Artifact says:** "FR-10 ... the atomic `StorageWrite` table-mutation union."
- **Required change:** Describe `StorageWrite` as the table-and-document write union, and point at `TableCommitChange` for the table-only subset.
- **Severity:** blocking

### No requirement covers the commit line, the transaction surface, or the read-after-write rule
- **Evidence:** `packages/durable/src/types.ts:1074` (`Session.commit<T>(change: (tx: Tx) => T | Promise<T>, context: Context): Promise<T>`); `packages/durable/src/types.ts:910-1005` (`Tx` surface: `conversation`, `entry`, `task`, `scanEntries`, `appendEntry`, `createTask`, `createSubmission`, `settleSubmission`, `placeSubmission`, `doc`, `retireDoc`); `packages/durable/src/session/transaction.ts:199` (`Transaction implements Tx`), `:953` (`if (this.#hasTableWrite) throw new ReadAfterWrite(method)`); `packages/durable/src/errors.ts:17-22` (`ReadAfterWrite`).
- **Artifact says:** No requirement mentions `Session.commit`, `Tx`, or `ReadAfterWrite`.
- **Required change:** Add a requirement for the single mutation line: every write goes through `Session.commit((tx) => ..., context)`, reads inside the callback must go through `tx`, and a table read after the first table write raises `ReadAfterWrite`.
- **Severity:** blocking

### No requirement covers the scheduler, the task phase protocol, or recovery
- **Evidence:** `packages/durable/src/harness/scheduler.ts:253` (`TaskScheduler`), `:1466` (`#reserve`), `:1826-1831` (a phase that returns without durable progress is faulted: "Task ${current.kind} phase ${previous.checkpoint.phase} returned without durable progress"); `packages/durable/src/types.ts:324-330` (`runtime.sleepUntil(until, checkpoint, context)` ends the phase with a stored deadline); `packages/durable/src/harness/scheduler.ts:370-412` (on open, tasks left `running` go back to `pending`, the restart counter increments, and a task at the restart limit is parked and reported as `task_parked`); `packages/durable/src/harness/harness.ts:277-284` (`resume()` starts scheduling, `wake()` reports what the host must do); `packages/durable/src/harness/types.ts:665` (`Wake = { readonly active: boolean; readonly at?: number }`).
- **Artifact says:** Nothing covers task execution, scheduling, sleeping, or crash recovery.
- **Required change:** Add requirements for the scheduler, the fault rule, the sleep protocol, the recovery reconciliation, and the wake contract.
- **Severity:** blocking

### No requirement covers the built-in task kinds or document kinds
- **Evidence:** `packages/durable/src/harness/registry.ts:10` (`BUILTIN_TASKS = [GenerationTask, ToolTask, CompactionTask]`); task names `pi.generation`, `pi.tool`, `pi.compaction` (`packages/durable/src/harness/live.ts:130-132`, `src/harness/tool.ts:124`); document kinds `pi.agent` (`src/harness/agent.ts:44`, rewindable/asOf), `pi.inbox` (`src/harness/inbox.ts:22`), `pi.live` (`src/harness/live.ts:112`), `pi.provider` (`src/harness/provider.ts:13`), `pi.usage` (`src/harness/usage.ts:15`), `pi.tool.nested-call` (`src/harness/tool.ts:106-112`).
- **Artifact says:** No requirement names a task kind or a document kind.
- **Required change:** Add requirements for the three built-in tasks and the built-in document kinds, and for the `defineDoc`/`defineDocFamily` extension points.
- **Severity:** blocking

### No requirement covers the persistent backends
- **Evidence:** `packages/durable/src/storage/sqlite/node.ts:15` (`openNodeSqliteStorage(path, options)`), `src/storage/sqlite/cloudflare.ts:10` (`openDurableObjectSqliteStorage(ctx.storage)`), `src/storage/jsonl/node.ts:6` (`openNodeJsonlStorage(directory, context, options)`); `packages/durable/src/storage/sqlite/migrations.ts:113-121` (two migrations, `CURRENT_SQLITE_SCHEMA_VERSION = 2`), `:14-90` (the `durable_metadata`, `record_ids`, `conversations`, `entries`, `tasks`, `submissions`, `documents`, `document_revisions` tables); `packages/durable/src/storage/jsonl/storage.ts:29` (`FORMAT_VERSION = 1`), `:82-93` (`JsonlCorruptionError`, `JsonlStoragePoisonedError`).
- **Artifact says:** No requirement names a backend other than `MemoryStorage`; the constraints say "`MemoryStorage` is a conformance reference, not a persistent backend."
- **Required change:** Add requirements for the SQLite and JSONL backends, their open functions, the schema version, and the JSONL corruption contract.
- **Severity:** blocking

### No requirement covers the `ExecutionEnv` and the built-in tool surface
- **Evidence:** `packages/durable/src/env/index.ts:374` (`ExecutionEnv extends FileSystem, Shell`), `:209` (`FileSystem`), `:359` (`Shell`), `:45` (`FileError`), `:65` (`ExecutionError`), `:129` (`FileWatcher`), `:141` (`LineScan`), `:171` (`ListFilesOptions`); `packages/durable/src/env/node.ts:603` (`NodeExecutionEnv`), `src/env/node-watch.ts:139` (`NodeFileWatcher`), `src/env/line-scan.ts:16` (`LineScanner`); `packages/durable/src/tools/index.ts:31` (`createCodingTools` providing `read`, `write`, `edit`, `bash`), `:39` (`CodingTools`); `packages/durable/src/codemode/codemode.ts:248` (`createCodemodeExtension`), `:231` (`createCodemodeTool`), `:88` (`CODEMODE_TOOL_NAME = "codemode"`); `packages/durable/src/images/index.ts:32` (`createPhotonImages`), `src/images/node.ts`, `src/images/cloudflare.ts`; `packages/durable/src/tool-search/tool-search.ts:11` (`TOOL_SEARCH_TOOL_NAME = "tool_search"`).
- **Artifact says:** Nothing about an execution environment, coding tools, code mode, images, or tool search.
- **Required change:** Add requirements for the `ExecutionEnv` contract and its Node implementation, the built-in tools, the code-mode extension, the image processor, and the deferred tool-search tool.
- **Severity:** blocking

### No requirement covers the telemetry schema
- **Evidence:** `packages/durable/src/harness/telemetry.ts:50-139` (`DURABLE_TELEMETRY_SCHEMA`, version 1): spans `pi.durable.submit` and `pi.durable.phase`; events `pi.durable.entry`, `pi.durable.submission`, `pi.durable.report`, `pi.durable.checkpoint`, `pi.durable.replay`; metrics `pi.durable.reports`, `pi.durable.phase.duration`, `pi.durable.tasks.active`; `packages/durable/src/harness/types.ts:610` (`HarnessOptions.telemetry`); `packages/durable/src/types.ts:648-650` (`TaskRecord.trace` / `TaskRecord.links` carry the telemetry carrier).
- **Artifact says:** Nothing about telemetry.
- **Required change:** Add a requirement for the content-free telemetry vocabulary and the carrier propagation on tasks and submissions.
- **Severity:** blocking

### No requirement covers the shared conformance suites or the `testing` subpath
- **Evidence:** `packages/durable/src/testing/storage-conformance.ts:95` (`createStorageConformance`, 25 cases), `src/testing/env-conformance.ts:114` (`createEnvConformance`, 20 cases), `src/testing/runner.ts:13` (`registerStorageConformance`), `:28` (`registerEnvConformance`), `src/testing/storage-benchmark.ts:88` (`seedStorageBenchmark`), `:391` (`seedStorageWriteBenchmark`); `packages/durable/package.json` (`"./testing"` export).
- **Artifact says:** No requirement mentions a conformance suite; the constraints ask "Does the Session-level commit path need a published conformance suite shared by every backend?" as an open question.
- **Required change:** State that the storage and env conformance suites ship on the `./testing` subpath and that every backend is registered against them; close open question 3.
- **Severity:** blocking

### The "Pico" model name and the "input" vocabulary are gone
- **Evidence:** `packages/durable/src/storage/sqlite/storage.ts:151` is the only surviving "Pico" mention in the package ("Portable SQLite implementation of the Pico storage contract"); `packages/durable/src/types.ts` exports no `Input` type (the only `Input` identifiers left are tool-argument types such as `ReadToolInput` in `src/tools/read.ts:40`); the current vocabulary is Session, Harness, Storage, Document, Task, Submission.
- **Artifact says:** "It implements the Pico model in which a Session atomically commits immutable entries, full task records, and Chord-tracked documents." FR-3 says "host inputs". The Stakeholders table says "A stable record and storage contract for building the Pico Session mutation line."
- **Required change:** Drop the "Pico" name and the "input" vocabulary; use Session, Harness, Storage, Document, Task, and Submission.
- **Severity:** advisory

### The constraints describe a one-backend package
- **Evidence:** `packages/durable/src/storage/sqlite/storage.ts` and `src/storage/jsonl/storage.ts` are persistent backends; `packages/durable/src/errors.ts:29-33` (`StorageRequestError` fails only the read that asked for it, not the Session, unlike any other Storage error).
- **Artifact says:** "Constraints: `MemoryStorage` is a conformance reference, not a persistent backend. Storage trusts the owning Session for semantic validity of records, references, ancestry, and transitions."
- **Required change:** Keep the first constraint, and add that two persistent backends ship in the package and that `StorageRequestError` is the one Storage error that does not fail the Session.
- **Severity:** advisory

### The open questions are answered by the code
- **Evidence:** `packages/durable/src/storage/sqlite/node.ts:15` and `src/storage/jsonl/node.ts:6` (persistent backends exist); `packages/durable/src/storage/sqlite/migrations.ts:66-89` and `src/session/transaction.ts` (document deltas persist in-package as `document_revisions` with `DocumentContent` base/delta); `packages/durable/src/testing/storage-conformance.ts:95` and `src/testing/runner.ts:13` (the shared conformance suite ships on `./testing`).
- **Artifact says:** "Open Questions: 1. Which serialization-backed store becomes the first persistent `Storage` beyond `MemoryStorage`? 2. Should document deltas ship inside this package or stay in the Chord package with usage docs only? 3. Does the Session-level commit path need a published conformance suite shared by every backend?"
- **Required change:** Close all three: SQLite and JSONL both ship, document deltas persist in-package, and the conformance suite is published on the `./testing` subpath.
- **Severity:** advisory

## Open questions
- The requirements never state which surfaces of the package are public API and which are internal. The `package.json` `exports` map (18 entries) is the de facto public surface, but nothing in the code marks `src/search.ts`, `src/truncate.ts`, or `src/timers.ts` as internal or public, so the intended boundary cannot be recovered from the code.
