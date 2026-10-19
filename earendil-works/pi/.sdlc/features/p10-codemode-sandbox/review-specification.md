---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### `CodemodeRunOptions` omits `signal` and `timeoutMs`, and a `start()` run has no default deadline
- **Evidence:** `packages/codemode/src/types.ts:214` (`signal?: AbortSignal`) and `packages/codemode/src/types.ts:216` (`timeoutMs?: number`, "Default: none (not the sandbox's default)"); `packages/codemode/src/runtime/execution.ts:549` (`timeoutMs: options.timeoutMs ?? Number.POSITIVE_INFINITY`).
- **Artifact says:** the `CodemodeRunOptions` table lists only `startedAt`, `seed`, `tools`, `globals`, `store`, `onStarted`, `onCall`, `onIdle`; the 300000 ms default is stated only for `CodemodeExecuteOptions`.
- **Required change:** add `signal` and `timeoutMs` to the `CodemodeRunOptions` table and state that a `start()` run has no deadline unless `timeoutMs` is given.

### `CodemodeOutcome` is used but never modeled
- **Evidence:** `packages/codemode/src/types.ts:196-198` (`{ ok: true; value }` or `{ ok: false; message: string; properties?: Record<string, unknown> }`); `packages/codemode/src/runtime/execution.ts:269-282` (the `properties` object is validated and serialized with the answer).
- **Artifact says:** the `onCall` row says "Host answers each call via `run.deliver(seq, now, id, outcome)`", but no data model defines `outcome`.
- **Required change:** add a `CodemodeOutcome` model, including that a rejection carries a `properties` object whose own properties are attached to the script's `Error` except `name`, `message` and `stack`.

### The API contract table omits part of the public surface
- **Evidence:** `packages/codemode/src/runtime/execution.ts:479-486` (`registerTool`, `unregisterTool`), `packages/codemode/src/types.ts:150-162` (`acquireWorker`, `onWorkerStarted`), `packages/codemode/src/cloudflare.ts:32` (`DEFAULT_REMOTE_MEMORY_LIMIT_BYTES`), `packages/codemode/src/cloudflare.ts:35` (`cloudflareQuickJSWasm`), `packages/codemode/src/cloudflare.ts:62-65` (the `maxInterruptBudget` and `maxMemoryLimitBytes` subclass hooks), `packages/codemode/src/source.ts:11` (`CODEMODE_OPTIONS_PREFIX`), `packages/codemode/src/source.ts:45` (`CodemodeSourceError`), `packages/codemode/src/runtime/inline.ts:39` (`DEFAULT_INTERRUPT_BUDGET`), `packages/codemode/src/runtime/inline.ts:42` (`INLINE_MAX_STACK_SIZE`), `packages/codemode/src/runtime/prelude-source.ts:34-43` (`MAX_STORE_VALUE_CHARS`, `MAX_STORE_TOTAL_CHARS`, `MAX_OUTPUT_CHARS`, `MAX_OUTPUT_ITEMS`), `packages/codemode/src/declarations.ts:10` (`DEFAULT_INPUT_SCHEMA_MAX_CHARS`).
- **Artifact says:** the table lists one or two exports per entry and no limits.
- **Required change:** list the exported limits, the tool-table methods, the worker-admission options and the Durable Object subclass hooks in the API contract table.

### The return shape of `parseCodemodeSource` is not modeled
- **Evidence:** `packages/codemode/src/source.ts:39-43` (`ParsedCodemodeSource` is `{ code, options }`, and `code` is "the script with the options line replaced by an empty line, so line numbers are unchanged"), `packages/codemode/src/source.ts:108-124` (an options line on any line but the first is rejected, and an options line without code is rejected).
- **Artifact says:** the `./source` row says only "Splits the `// @options:` line from code"; the `CodemodeSourceOptions` model has no counterpart for the returned code.
- **Required change:** add a `ParsedCodemodeSource` model and state that the options line must be the first line and that the returned code keeps its line count.

### Advisory: the error table's "Code" column is not a field of `CodemodeError`
- **Evidence:** `packages/codemode/src/types.ts:75-80` (`CodemodeError` has `kind`, `name?`, `message`, `stack?`).
- **Artifact says:** the table has a `Code` column that repeats the kind.
- **Required change:** rename the column to `kind` or drop it.

### Advisory: the "durable host" behind the deterministic runs is not identified
- **Evidence:** `packages/durable/src/codemode/codemode.ts:46` imports the portable entry, `packages/durable/src/codemode/codemode.ts:86` defines `CODEMODE_MODULE_VERSION = 2`, `packages/durable/src/codemode/codemode.ts:444-447` refuses to resume a script that started under another version.
- **Artifact says:** the decisions table says "a durable host can resume a run after restart and get identical calls and output"; the specification never names the consumer, and this feature's artifacts do not cover `packages/durable/src/codemode/`.
- **Required change:** name the consumer, or state that the durable integration belongs to the durable feature.

## Open questions
- Is `packages/durable/src/codemode/` in scope for this feature (see the requirements review)? The specification's rationale for `start()` depends on it, but the durable feature (`p7-durable-runtime`) may already own that integration.
