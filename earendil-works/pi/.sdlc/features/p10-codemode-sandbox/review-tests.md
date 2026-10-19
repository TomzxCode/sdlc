---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### `packages/codemode/test/worker-lifetime.test.ts` is not covered by the plan
- **Evidence:** `packages/codemode/test/worker-lifetime.test.ts` (5 `it` blocks plus a `describe.each` over runtimes) is the only coverage of the worker admission contract (`packages/codemode/src/runtime/host.ts:30-38` calls `acquireWorker` before creating the worker and releases it on worker exit) and of `onWorkerStarted` exit timing (`packages/codemode/src/types.ts:156-162`); it uses the fixture `packages/codemode/test/fixtures/worker-process-exit.ts` at `packages/codemode/test/worker-lifetime.test.ts:216`.
- **Artifact says:** the Scope names the suites `sandbox.test.ts`, `deterministic.test.ts`, `declarations.test.ts`, `portable.test.ts` and `source.test.ts`; the worker-lifetime suite appears nowhere, and no test case covers admission or worker exit.
- **Required change:** add the suite and its cases to the plan and map them to the worker-lifetime contract.

### TC-26 has no test in the repo
- **Evidence:** no file under `packages/codemode/test/` or elsewhere in the repo references `examples/cloudflare`; the only files that mention it are the example itself (`packages/codemode/examples/cloudflare/README.md`, `packages/codemode/examples/cloudflare/agent/src/index.ts`, `packages/codemode/examples/cloudflare/sandbox/src/index.ts`).
- **Artifact says:** TC-26 "Cloudflare example wiring ... Scripts execute in the sandbox Worker and tool calls resolve in the agent Worker" is an end-to-end test case.
- **Required change:** either drop TC-26 or turn it into a documentation check, since the example is not exercised by any suite.

### The plan excludes the coding-agent side, which is in the feature's scope
- **Evidence:** `packages/coding-agent/test/suite/agent-session-codemode.test.ts` (25 `it` blocks) covers FR-10 end to end: nested calls through the agent loop with only the script result reaching the model (`:206-246`), nested calls routed through the `tool_call` and `tool_result` hooks (`:248-296`), the `codemode.mode` presentation (`:141-185`), the options line and the memory limit (`:484-521`), the output token budget and the spill file (`:523-552`), `store()` persistence (`:600-624`) and the `models.*` API (`:664-1031`). Also `packages/coding-agent/test/codemode-renderer.test.ts` (5 blocks), `packages/coding-agent/test/codemode-worker-admission.test.ts` (2 blocks, 5 cases, regression #10748), `packages/coding-agent/test/codemode-worker-config.test.ts` (3 blocks, regression #10204) and the "codemode description catalog" block in `packages/coding-agent/test/tool-search.test.ts:67-125` (5 blocks).
- **Artifact says:** the Scope says "It excludes the coding-agent `codemode` tool behavior, which belongs to the consumer package", while the feature covers `packages/coding-agent/src/extensions/codemode/`.
- **Required change:** include the coding-agent suites in the plan and map them to FR-10, NFR-1, NFR-3 and NFR-4; the exclusion sentence contradicts the feature scope.

### Advisory: the suite counts do not match the files
- **Evidence:** `packages/codemode/test/deterministic.test.ts` holds 16 `it` blocks, 14 of them inside the loop over the two backends (`worker` and `remote`, `packages/codemode/test/deterministic.test.ts:43-46` and `:106-107`), so the file runs 30 cases, not the 24 the plan states. `packages/codemode/test/sandbox.test.ts` holds 52 `it` blocks plus one `it.each` with 7 cases (`:854-862`), and the 47 blocks inside `describe.each(Object.keys(BACKENDS))` (`:73`, three backends at `:24-40`) run 3 times each, so the file runs about 153 cases, not 54.
- **Artifact says:** "Suite counts at sync time: `sandbox.test.ts` 54 tests, `deterministic.test.ts` 24, `declarations.test.ts` 17, `portable.test.ts` 7, `source.test.ts` 5."
- **Required change:** restate the counts as blocks and executions, or drop them. The counts could not be confirmed by running the suites in this environment, where `node_modules` is absent, so they are derived from the test sources.

### Advisory: TC-24 names the wrong fixture, and one fixture is not mentioned
- **Evidence:** the "embedded sources parse as JavaScript" case parses `PRELUDE_SOURCE` with `node:vm` (`packages/codemode/test/sandbox.test.ts:67-70`); `packages/codemode/test/fixtures/raw-worker.ts` is a fake worker that posts raw host messages and is used as a `workerUrl` at `packages/codemode/test/sandbox.test.ts:840` and `:863`; `packages/codemode/test/fixtures/worker-process-exit.ts` is used at `packages/codemode/test/worker-lifetime.test.ts:216`.
- **Artifact says:** TC-24 uses the `raw-worker.ts` fixture, and the Test Infrastructure section calls it "the embedded worker source parse test".
- **Required change:** point TC-24 at `PRELUDE_SOURCE` and describe the two fixtures for what they are.

### Advisory: NFR-5 has no proof inside the suite
- **Evidence:** `packages/codemode/test/portable.test.ts` runs in Node, so it cannot show that the entry imports no `node:*` built-in; the guard is the repo-level entry-graph check `scripts/check-entry-graphs.mjs:46-59`, which forbids `codemode/src/index.ts`, `runtime/host.ts`, `runtime/worker.ts` and `codemode/src/wasm.ts` from the `./portable` and `./cloudflare` entries.
- **Artifact says:** NFR-5's acceptance criterion is "Given a runtime without `node:*` built-ins ... the import succeeds and both portable sandboxes construct", and the coverage matrix maps NFR-5 to TC-9 and TC-21.
- **Required change:** say that NFR-5 is proven by the entry-graph check rather than by TC-9 and TC-21, or add a bundling test for the portable entry.

### Advisory: the durable consumer's suites are not mentioned
- **Evidence:** `packages/durable/test/codemode.test.ts`, `packages/durable/test/codemode-describe.test.ts`, `packages/durable/test/codemode-models.test.ts` and `packages/durable/test/tool-search.test.ts` exercise the sandbox through `packages/durable/src/codemode/`.
- **Artifact says:** the plan covers `packages/codemode/test/` only.
- **Required change:** decide whether the durable integration belongs to this feature (see the open question) and either add the suites or state that they belong to the durable feature.

## Open questions
- Is the durable integration (`packages/durable/src/codemode/`) part of this feature? If not, the plan should say that the durable suites are covered by the durable feature.
