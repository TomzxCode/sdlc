---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

The plan covers `telemetry.test.ts` and `conformance.test.ts` accurately, but two of the five test files in the package are absent from it, and the one documented end-to-end case does not exist. The plan also predates the metrics, propagation, links, and capabilities requirements recorded in `review-requirements.md`, so its coverage matrix cannot reach them.

## Sync drift: 2026-10-19

### The plan omits test/metrics.test.ts
- **Evidence:** `packages/telemetry/test/metrics.test.ts:61-196` — five cases covering typed metric binding (names, kinds, metadata, exact attributes), required histogram attributes, detached measurement snapshots with exemplars and boundaries, rejection of malformed metadata, non-finite values, and unreadable attributes, and shared frozen no-op instruments.
- **Artifact says:** the Scope names "unit behavior in telemetry.test.ts and adapter conformance in conformance.test.ts", and no case covers metrics.
- **Required change:** add a metrics test section with one case per `it(...)` block in `test/metrics.test.ts`, and map them to the metrics requirement.

### The plan omits test/propagation.test.ts and its propagation-worker.ts helper
- **Evidence:** `packages/telemetry/test/propagation.test.ts:23-39` (continuing a parent in another Node process through `packages/telemetry/test/propagation-worker.ts:1-6`), `:41-76` (isolating crossed concurrent remote parents, linking shared roots), `:78-100` (detaching carrier and link snapshots, retaining settled target identities), `:102-122` (linking a new root to an extracted remote target), `:124-134` (rejecting malformed memory carriers, never inspecting no-op payloads).
- **Artifact says:** no case covers propagation or links.
- **Required change:** add a propagation and links test section with one case per `it(...)` block in `test/propagation.test.ts`, and state that the cross-process case shells out to a separate Node process.

### Four conformance groups have no case in the plan
- **Evidence:** `packages/telemetry/src/testing/conformance.ts` implements 17 cases in 9 groups: capabilities (`:74-100`), metrics (`:101-134`, `:135-162`), links (`:163-184`, `:185-203`), propagation (`:204-223`, `:224-244`, `:245-267`), callback lifecycle (`:268-288`, `:290-343`), status (`:345-385`), recording (`:387-407`, `:409-421`, `:423-447`), parentage (`:449-475`), passivity (`:477-502`, `:504-516`).
- **Artifact says:** TC-6..TC-13 map only to the callback lifecycle, status, recording, parentage, and passivity groups. The capabilities, metrics, links, and propagation groups are not represented.
- **Required change:** add cases for the four uncovered groups, and state the suite shape as 17 cases in 9 groups.

### TC-14 does not exist
- **Evidence:** no test in `packages/telemetry/test/` starts a span, adds an event, sets attributes, sets a status, resolves, and then asserts one settled snapshot with merged attributes, ordered events, and a final status. The closest real cases are the conformance `recording` case at `packages/telemetry/src/testing/conformance.ts:387-407`, which checks merged attributes and ordered events but leaves the status at the automatic `ok`, and the conformance `status` case at `:345-385`, which checks the final status but records no attributes or events. The only `setStatus` calls in the package's own test files are the no-op assertions at `packages/telemetry/test/telemetry.test.ts:200`.
- **Artifact says:** TC-14 is the single End-to-End Test: "Package-level span flow exercises start through settlement".
- **Required change:** either point TC-14 at the conformance `recording` and `status` cases, or add a real package-level flow test that exercises the whole sequence and asserts one settled snapshot.

### Advisory: the test infrastructure note omits the missing vitest config
- **Evidence:** `packages/telemetry/package.json:25` runs `vitest --run`, and `packages/telemetry` has no `vitest.config.ts`, unlike `packages/ai/vitest.config.ts` and `packages/agent/vitest.config.ts`. The package therefore runs on Vitest defaults and does not inherit the workspace aliases declared in `vitest.base.ts:35-36`; its tests import the source relatively, so they still work.
- **Artifact says:** "Vitest runs the telemetry package suite from the package directory."
- **Required change:** state that the package has no vitest config and runs on Vitest defaults, or add a config that extends the shared base.

### Advisory: the coverage matrix cannot reach the missing requirements
- **Evidence:** the Coverage Matrix maps FR-1..FR-9 and NFR-1..NFR-4, and the requirements define no FR for propagation, links, metrics, or the conformance suite.
- **Artifact says:** the matrix is complete for the stated requirements.
- **Required change:** extend the matrix after the requirements gain the four missing FRs recorded in `review-requirements.md`.

## Open questions

- None. The package's five test files were all read in full and every plan entry was matched against them.
