---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25896ffeQpp5pBlvJ7Lg1u
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The plan understates the suite: 47 test files, not thirty
- **Evidence:** `packages/chord/test/` contains 47 `*.test.ts` files (`find test -name "*.test.ts" | wc -l` = 47), plus `test/delta-traversal.bench.ts`, the `test/delta-benchmark/`, `test/delta-tracker/`, `test/fixtures/` and `test/sqlite/` subtrees. The suite declares 492 `test()` / `it()` blocks, 10 of which are `.each` blocks expanding to 41 cases, so roughly 520 individual cases.
- **Artifact says:** "The suite covers thirty test files under packages/chord/test with roughly four hundred individual cases."
- **Required change:** Update the count to 47 test files and roughly 520 cases, and list the directories the suite spans.
- **Severity:** blocking

### TC-7, TC-9, TC-10 and TC-11 describe a service model the suite does not test
- **Evidence:** TC-7 expects "Singleton provide, consume, replacement, and disposal"; TC-9 expects "Facet host validates graphs and orders activation and disposal" over "Facets with chained dependencies"; TC-10 expects "Keyed services route through the host and stay local when marked local"; TC-11 expects "Loaders combine in order and dispose generations in reverse | Multiple facet loaders with resources". In the code, `Lifetime = "referenced" | "host"` is the only mode (`packages/chord/src/object.ts:76`), there is no singleton or keyed service, there is no facet dependency graph to validate, and `HostOptions.loader` is a single `FacetLoader` (`packages/chord/src/host.ts:146`), not a composable list. The loader suite is `packages/chord/test/loader.test.ts:7-20` (two cases: a child-process load-and-reload, and "needs a configured loader for modules").
- **Artifact says:** The four test cases above, and the coverage matrix rows "FR-3 | TC-7", "FR-4 | TC-10", "FR-5 | TC-9", "FR-9 | TC-11, TC-11E", "FR-10 | TC-15, TC-15E".
- **Required change:** Restate these cases against the real model: `packages/chord/test/host.test.ts` covers activation, lifetime, declarations and methods; `packages/chord/test/placement.test.ts` covers placement resolution (`hostNamed` / `hostFamily`); `packages/chord/test/host-objects-reload.test.ts` covers host-lifetime objects across a reload. FR-3, FR-4 and FR-5 as written have no test and no implementation.
- **Severity:** blocking

### Thirty-three test files are not covered by the plan
- **Evidence:** The plan names at most fourteen files (through TC-1 to TC-17). The following files exist in `packages/chord/test/` and materially cover the feature, but no test case in the plan refers to them: `awaiting.test.ts`, `bindings.test.ts`, `cluster.test.ts`, `contract.test.ts`, `flow.test.ts`, `flow-units.test.ts`, `generations.test.ts`, `host-objects-reload.test.ts`, `hydration.test.ts`, `links-review.test.ts`, `manager.test.ts`, `output.test.ts`, `output-skip.test.ts`, `placement.test.ts`, `principals.test.ts`, `provider-cost.test.ts`, `readiness.test.ts`, `reload.test.ts`, `replicated-state-delivery.test.ts`, `requests.test.ts`, `review.test.ts`, `sqlite/migrations.test.ts`, `sqlite/node.test.ts`, `sqlite/cloudflare.test.ts`, `state-diff.test.ts`, `state-draft.test.ts`, `state-fuzz.test.ts`, `state-init.test.ts`, `state-value.test.ts`, `tutorial.test.ts`, `types.test.ts`, `variants.test.ts`, `websocket.test.ts`.
- **Artifact says:** The Scope section says the suite exercises "facets, services, replicated state, delta tracking, the remote-service wire boundary, facet loading and reload, context, and strict-JSON validation", and the Coverage Matrix maps only FR-1 to FR-11 and NFR-1 to NFR-4.
- **Required change:** Add test cases for the uncovered areas, at minimum: contracts (`contract.test.ts`: fingerprints, reserved member names, coverage, `accepts` adapters), placement (`placement.test.ts`), principals (`principals.test.ts`), readiness (`readiness.test.ts`), flow control (`flow.test.ts`, `flow-units.test.ts`), shared bindings and linger (`bindings.test.ts`), variants and re-hold (`variants.test.ts`), generation GC (`generations.test.ts`), application requests (`requests.test.ts`), hot reload (`reload.test.ts`, `review.test.ts`, `host-objects-reload.test.ts`), cross-host reload (`cluster.test.ts`), the host manager and `processLock` (`manager.test.ts`), WebSocket links and packed payloads (`websocket.test.ts`), bounded output (`output.test.ts`, `output-skip.test.ts`), the SQLite facade (`sqlite/*.test.ts`), the tutorial examples (`tutorial.test.ts`) and the delta/state diff and draft suites (`state-diff.test.ts`, `state-draft.test.ts`, `state-fuzz.test.ts`, `state-init.test.ts`, `state-value.test.ts`, `delta-diff.test.ts`, `delta-tracker/tracker.test.ts`).
- **Severity:** blocking

### The plan does not mention the subsystems the requirements omit, so they have no coverage entry
- **Evidence:** The SQLite facade, the output module, the child-host manager, cluster reload and the telemetry-carrying `Context` are shipped (`packages/chord/src/sqlite/`, `packages/chord/src/output.ts`, `packages/chord/src/manager.ts`, `packages/chord/src/cluster.ts`, `packages/chord/src/context/index.ts`) and each has tests, but the plan's Scope does not name them and the Coverage Matrix has no row for them.
- **Artifact says:** "Out of scope is any real transport, Pi host integration, and performance benchmarking beyond the delta traversal bench."
- **Required change:** Add the SQLite, output, host-manager and cluster-reload areas to the plan scope and to the coverage matrix, and add the requirement rows that the same sync records as missing from `requirements.md` (see `review-requirements.md`).
- **Severity:** blocking

### The "Test Infrastructure" section understates the fixtures the suite uses
- **Evidence:** The suite also uses `packages/chord/test/fixtures/loader.ts` (the child-process facet loader fixture), `packages/chord/test/fixtures/counting.ts`, `packages/chord/test/fixtures/echo.ts`, `packages/chord/test/fixtures/worker.ts`, `packages/chord/test/delta-tracker/retention.worker.ts` (the GC-pressure worker), `packages/chord/test/sqlite/helpers.ts`, and the `test/delta-benchmark/` workers.
- **Artifact says:** "Vitest runs the suite from packages/chord with a loopback service transport helper. A dedicated retention worker exercises tracker proxies under garbage-collection pressure. Facet loader fixtures run in a child process through the Node loader with its reload query hook."
- **Required change:** List the fixture and worker files, and state that the SQLite suite runs against `node:sqlite` and a Durable Object stub.
- **Severity:** advisory

### The Coverage Matrix does not say which requirements the suite leaves uncovered
- **Evidence:** FR-2 (facet dependency-graph validation) has no test: no file under `packages/chord/test/` builds a graph of facets with a missing dependency, a duplicate provider or a cycle. FR-3 (singleton replacement) and FR-4 (keyed instances) have no test because neither concept exists in the code. NFR-3 (rehydration before new updates) is exercised indirectly by `packages/chord/test/replicated-state.test.ts` and `packages/chord/test/state.test.ts`, but no case names a disconnect and rehydrate sequence.
- **Artifact says:** The matrix maps FR-2 to "TC-9, TC-9E" and FR-3 to "TC-7", FR-4 to "TC-10".
- **Required change:** Mark FR-2, FR-3 and FR-4 as uncovered (they have no implementation either), and point NFR-3 at the state and replicated-state suites.
- **Severity:** advisory

## Open questions
- The plan does not state whether the suite is expected to run under `npm test` in `packages/chord` (`vitest --run`, `packages/chord/package.json:62`) or only through the repository-level `./test.sh`. The code supports both, and the choice is not answerable from the artifacts.
- The plan does not say whether `test/tutorial.test.ts` (which executes the examples in `packages/chord/docs/tutorial.md`) is a required gate or a documentation check. The code treats it as a normal test file.
