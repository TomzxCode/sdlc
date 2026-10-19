---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25897ffew6r70TkGexlr7Q
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The scope excludes the Session mutation line, the Harness, and the document model, but 54 test files cover them
- **Evidence:** `packages/durable/test/` holds 69 `.test.ts` files. The plan names three of them (`test/memory-storage.test.ts`, `test/types.test.ts`, and the shared suite at `src/testing/storage-conformance.ts`). The unmentioned material: 37 `harness-*.test.ts` files (generation, compaction, inbox, ownership, nested tools, recovery, sleep, telemetry, reports, view, task graph, registry, events, context, prompt, live deltas, and more), 8 `session-*.test.ts` files (`session-checkpoints-migrations`, `session-definitions`, `session-document-retention`, `session-documents`, `session-forks`, `session-states`, `session-tables`, `session-watches`), `test/sqlite-storage.test.ts`, `test/sqlite-migrations.test.ts`, `test/sqlite-facade.test.ts`, `test/sqlite-cloudflare.test.ts`, `test/jsonl-storage.test.ts`, `test/storage-runtime-boundary.test.ts`, `test/tools.test.ts`, `test/tools-read-differential.test.ts`, `test/tools-images.test.ts`, `test/tool-search.test.ts`, `test/codemode.test.ts`, `test/codemode-describe.test.ts`, `test/codemode-models.test.ts`, `test/env-node.test.ts`, `test/env-node-spill.test.ts`, `test/env-node-conformance.test.ts`, `test/env-line-scan.test.ts`, `test/env-truncate.test.ts`, `test/images-wasm-module.test.ts`, `test/spec-usage.test.ts`, `test/provider-session-cache-e2e.test.ts`, `test/system-order-cache-e2e.test.ts`, and `test-workers/storage.test.ts` plus `test-workers/wake.test.ts`.
- **Artifact says:** "This plan covers the Pico record contracts and `Storage` behavior in `packages/durable`. It is derived from the shared storage conformance suite (`src/testing/storage-conformance.ts`, registered for the memory, SQLite, and JSONL backends), `test/memory-storage.test.ts` (retained-state case), and `test/types.test.ts` (three compile-time discriminator cases). Out of scope are the Session mutation line, the Harness agent loop, and Chord delta mechanics."
- **Required change:** Widen the scope to the whole package: the record contracts, the `Storage` contract and its three backends, the `Session` mutation line and document model, the `Harness` and scheduler, the built-in tasks, the `ExecutionEnv` and its conformance suite, the built-in tools and code mode, the telemetry schema, and the specification usage test. The exclusions must go: the Session mutation line, the Harness, and the document model are all covered by tests that exist today.
- **Severity:** blocking

### The storage conformance suite has 25 cases; the plan represents 12 of them
- **Evidence:** `packages/durable/src/testing/storage-conformance.ts:95` (`createStorageConformance`) defines 25 cases. The plan's TC-1..TC-12 cover cases 1-7, 9, 10, 11, 14, 24, and 25. No plan case represents case 8 ("filters and pages conversations by durable owner edges"), 12 ("stores owners and scans waiting and completing tasks by status"), 13 ("stores and scans sleeping tasks by status"), 15 ("stores passive write submissions without input-only lifecycle states", `src/testing/storage-conformance.ts:763`), 16 ("reconstructs rewindable documents and preserves half-open incarnations"), 17 ("streams long document tails across root replacement deltas"), 18 ("copies stored document bases independently and rejects ambiguous sources"), 19 ("uses bases for version transitions and rejects historical reads of current-only documents"), 20 ("indexes logical addresses and exact-scope scans independently"), 21 ("keeps document lifecycle failures atomic and gives create-plus-retire an empty lifetime"), 22 ("rolls back record tables and secondary indexes when a document command fails"), or 23 ("keeps indexed string identities lossless").
- **Artifact says:** The Unit Tests table ends at TC-13 and the Integration Tests table at TC-16, with no case for owner edges, waiting/completing/sleeping task scans, passive write submissions, or any document behaviour.
- **Required change:** Add plan cases for the thirteen uncovered conformance cases, and extend the Coverage Matrix so the document, submission-write, task-status, and owner-edge behaviour each map to a requirement.
- **Severity:** blocking

### The env conformance suite, the workerd project, the runnable examples, and the spec usage test are not in the plan
- **Evidence:** `packages/durable/src/testing/env-conformance.ts:114` (`createEnvConformance`, 20 cases: binary reader ranges, line scanning, rename durability, directory reader paging, argv exec, windowed exec, timeout versus abort, `listFiles` with gitignore, symlinks); `packages/durable/test/env-node-conformance.test.ts:33` and `:48` (two `registerEnvConformance` registrations); `packages/durable/test-workers/vitest.config.ts` (a separate Vitest project running in `workerd` through `@cloudflare/vitest-plugin`); `packages/durable/test-workers/storage.test.ts:13` (the storage conformance suite against Durable Object SQLite in workerd) and `test-workers/wake.test.ts`; `packages/durable/test/examples/00-conversation.ts` through `31-reload-and-restart.ts` (32 runnable examples, one per documented pattern); `packages/durable/test/spec-usage.test.ts:1-5` ("The usage examples of docs/spec.md, compile-checked").
- **Artifact says:** The plan names none of these. Its Test Infrastructure section lists only the Vitest suite in `packages/durable/test/`, the storage conformance suite, and the type-level assertions.
- **Required change:** Add the env conformance suite and its 20 cases, the workerd project and its two test files, the 32 runnable examples, and the specification usage compile check to the plan and to the Coverage Matrix.
- **Severity:** blocking

### The plan's test command and infrastructure section describe a single Vitest pass
- **Evidence:** `packages/durable/package.json` `"test": "vitest --run && PI_DURABLE_DOCUMENT_RETENTION_MS=0 vitest --run && npm run test:workers"`, `"test:workers": "vitest --run --config test-workers/vitest.config.ts"`, `"bench:storage": "vitest bench --config vitest.benchmark.config.ts"`, plus eight `bench:*` scripts for the standalone benchmark files; `packages/durable/vitest.config.ts` (excludes `test-workers/**`, setup file `./test/setup-document-retention.ts`); `packages/durable/src/testing/storage-benchmark.ts:88` (`seedStorageBenchmark`), `:391` (`seedStorageWriteBenchmark`), `:284` (`STORAGE_READ_BENCHMARKS`), `:409` (`STORAGE_WRITE_BENCHMARKS`); `packages/durable/test/storage.bench.ts` and the eight `*-bench.ts` scripts under `test/`.
- **Artifact says:** "TC-17 | Package check passes for sources and tests | Run the root check | No erasable-TypeScript or import-hygiene violations for the package." and "Test Infrastructure - Vitest suite in `packages/durable/test/` using `BACKGROUND_CONTEXT` as the storage context. ... Targeted runs avoid the full suite (from `packages/durable`): `npx vitest --run test/memory-storage.test.ts`."
- **Required change:** State the three-phase package test command (the plain pass, the retention-disabled pass, and the workerd project), the benchmark config and the eight standalone benchmark scripts, and keep the root `npm run check` as a separate static check rather than the only verification.
- **Severity:** blocking

### The plan describes `test/types.test.ts` as three compile-time discriminator cases; it now covers submissions, waits, compaction, and extension erasure
- **Evidence:** `packages/durable/test/types.test.ts:49` ("brands numeric IDs by record kind and carries task result types"), `:72` ("encodes discriminator-dependent fields"), `:256` ("types submissions, task waits, compaction, and tasks erased into extensions"); `:257-258` (`SubmissionDraft` discriminators), `:319-344` (the `SubmissionDraft`, hook, and task-input compile-time failures). The file is 346 lines and carries 29 `@ts-expect-error` markers, so the "twenty-nine invalid shapes" count still holds.
- **Artifact says:** "Scope ... `test/types.test.ts` (three compile-time discriminator cases)."
- **Required change:** Keep the count of three cases and the twenty-nine invalid shapes, and describe what the third case now covers: `SubmissionDraft` type discriminators, `TaskOwnership`, `CompactionResult`, hook typing by the task's own hooks, and the extension-erasure boundary.
- **Severity:** advisory

### The plan still uses the retired "input" vocabulary for submissions
- **Evidence:** `packages/durable/src/testing/storage-conformance.ts:116-129` builds a `SubmissionRecord` with `type: "input"`; case 15 (`:687`-area) exercises `type: "write"`; `packages/durable/src/types.ts:476-537` (the `SubmissionRecord` union).
- **Artifact says:** TC-1, TC-3, TC-10, TC-18, and TC-19 all speak of an "input" record, and the Scope paragraph says "the Pico record contracts".
- **Required change:** Use the submission vocabulary and the `type: "input" | "write"` discriminator; drop "Pico".
- **Severity:** advisory

### TC-16 does not name the error type the code throws
- **Evidence:** `packages/durable/src/storage/memory.ts:498` and `src/storage/sqlite/storage.ts:302`, `:327`, `:356`, `:393` throw `new StorageRequestError(\`Unknown conversation: ${conversationId}\`)`; `packages/durable/src/errors.ts:29-33` (`StorageRequestError` fails only that read, not the Session, unlike any other Storage error).
- **Artifact says:** "TC-16 | Unknown conversations fail fast on history reads | No conversation with the queried ID | Entry scan and head-marker search throw `Unknown conversation`."
- **Required change:** Name `StorageRequestError` and state that it is the one Storage error that fails only the read and not the Session.
- **Severity:** advisory

## Open questions
- The plan does not say whether the 32 files under `packages/durable/test/examples/` are executed by CI or only runnable by hand. `packages/durable/package.json` has no script that runs them, and `packages/durable/vitest.config.ts` includes only `*.test.ts` by default, so their status is not recoverable from the code.
