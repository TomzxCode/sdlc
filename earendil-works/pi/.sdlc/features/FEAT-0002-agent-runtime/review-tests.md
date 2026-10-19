---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83563ffeRejJwzXWhPYVQK
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The coverage matrix points four requirements at a package that does not test this one
- **Severity:** blocking
- **Evidence:** `packages/agent/package.json:25-28` — `pi-agent-core` does not depend on `@earendil-works/pi-durable`, and `packages/agent/CHANGELOG.md:31` records that the durable runtime, compaction, and skills were removed from this package in 1.0.0.
- **Artifact says:** `tests.md:41` (FR-09), `tests.md:44` (FR-12), `tests.md:45` (FR-13), and `tests.md:46` (FR-14) list "covered in its test suite" in the `pi-durable` package, and `tests.md:11` makes the same claim in the scope statement.
- **Required change:** remove the `pi-durable` rows and the scope claim, and replace them with the behaviours this package actually implements (the same drift is recorded against the requirements themselves in `review-requirements.md`).

### FR-05, FR-07, and FR-10 are mapped to the wrong test file
- **Severity:** blocking
- **Evidence:** `packages/agent/test/agent.test.ts` contains no `beforeToolCall` or `afterToolCall` test; those live in `packages/agent/test/agent-loop.test.ts:528`, `packages/agent/test/agent-loop.test.ts:1732`, `packages/agent/test/agent-loop.test.ts:1964`, `packages/agent/test/agent-loop.test.ts:2167`, and `packages/agent/test/agent-loop.test.ts:2214`.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:199` ("should handle custom message types via `convertToLlm`") is the custom-message coverage; `packages/agent/test/agent.test.ts` has no custom-message or `convertToLlm` test.
- **Evidence:** `packages/agent/test/e2e.test.ts:208` ("handles abort during streaming") is abort coverage that the matrix does not list.
- **Artifact says:** `tests.md:37` (FR-05) and `tests.md:42` (FR-10) point at `agent.test.ts`, and `tests.md:39` (FR-07) lists only `agent.test.ts`.
- **Required change:** point FR-05 and FR-10 at `agent-loop.test.ts`, and add `e2e.test.ts` to the FR-07 row.

### The matrix has no row for behaviours the repo already tests
- **Severity:** blocking
- **Evidence:** `packages/agent/test/agent.test.ts:361` and `packages/agent/test/agent.test.ts:399` cover NFR-03, which has no matrix row.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:1732`, `packages/agent/test/agent-loop.test.ts:1783`, `packages/agent/test/agent-loop.test.ts:1841`, `packages/agent/test/agent-loop.test.ts:1899`, and `packages/agent/test/agent-loop.test.ts:1964` cover the batch termination rule, which no requirement states.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:456` covers the refusal to execute tool calls from a length-truncated message, which no requirement states.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:2133` covers `runToolCall`, which no requirement states.
- **Evidence:** `packages/agent/test/agent.test.ts:163`, `packages/agent/test/agent.test.ts:211`, and `packages/agent/test/agent.test.ts:246` cover the tool loadout declaration, which no requirement states.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:589` covers the `prepareArguments` shim, which no requirement states.
- **Evidence:** `packages/agent/test/agent-loop.test.ts:1108` through `packages/agent/test/agent-loop.test.ts:1633` cover `finishTurn`, `prepareRequest`, and `prepareNextTurn`, which no requirement states.
- **Artifact says:** `tests.md:29-49` maps 15 of the 19 requirements and FR-01, FR-03, FR-08, FR-11, NFR-03, NFR-04, and NFR-05 are either missing or untested.
- **Required change:** add matrix rows for the termination rule, the length-truncation guard, `runToolCall`, the tool loadout declaration, the `prepareArguments` shim, the request and turn hooks, and NFR-03.

### The plan has no test-case identifiers, so the matrix cannot be traced to cases
- **Severity:** advisory
- **Evidence:** the artifact template at `skills/sdlc/templates/features/tests.md` defines a `TC-N` test-case table and a `| Requirement | Test Cases |` matrix, while `tests.md:29-49` has a `| Requirement | Test Files |` matrix and no test-case table.
- **Artifact says:** `tests.md:13-22` describes the suites at file granularity only.
- **Required change:** either add the `TC-N` table with the test names from the four suites, or state that the Vitest suites in `packages/agent/test/` are the source of truth and map each requirement to the covering test name.

## Open questions
- Should the `examples/mcp-codemode` package be exercised by an automated test, given that it is the only in-repo consumer of `runToolCall` (`packages/agent/examples/mcp-codemode/tools.ts:91`)?
