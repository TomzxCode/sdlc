---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Test Plan

## Sync drift: 2026-11-16

Five test file paths in tests.md no longer exist in the codebase.
The test cases themselves still exist, but they were moved into other files.

- TC-4 lists `src/context-engine/host-param-projection.test.ts`, which does not exist. The host parameter projection cases now live in `src/context-engine/registry.host-params.test.ts`, a file that tests.md does not list.
- TC-5 lists `src/context-engine/quarantine-health.test.ts`, which does not exist. The quarantine health cases now live under the "quarantine health" block in `src/context-engine/registry.selection.test.ts`. The specific case "an empty warm turn does not dispatch health cleanup again" no longer appears; the current cases are "does not create or adopt absent/native-only state during health cleanup", "keeps accepted registration when its health cleanup is superseded", and "joins worker-backed activation health cleanup".
- TC-9 lists `src/context-engine/registry.factory-admission.test.ts`, which does not exist. The factory admission case now lives under the "foreground admission" block in `src/context-engine/registry.selection.test.ts`.
- TC-10 lists `src/context-engine/registry.copied-view-resources.test.ts`, which does not exist. The copied view case now lives under the "registry adoption" block in `src/context-engine/registry.logical-turn-resources.test.ts`.
- TC-11 lists `src/context-engine/registry.fallback-resources.test.ts`, which does not exist. The fallback resources cases now live under the "lazy fallback native resources" block in `src/context-engine/registry.logical-turn-resources.test.ts`.

All other test paths in tests.md exist, and the documented cases are still present after the consolidation.

## Sync drift: 2026-11-23

Re-verified against the current checkout. The five stale test paths from 2026-11-16 remain in tests.md and still do not exist on disk. Verdict stays changes-requested with the following file:line evidence.

- TC-4 in tests.md:37 still lists `src/context-engine/host-param-projection.test.ts`, which is absent. The cases now live in `src/context-engine/registry.host-params.test.ts`: the "host parameter projection" block at line 19, "does not retry validator-shaped engine failures" at line 236, and "preserves raw call identity despite process quarantine" at line 287.
- TC-5 in tests.md:38 still lists `src/context-engine/quarantine-health.test.ts`, which is absent. The cases now live under "quarantine health" in `src/context-engine/registry.selection.test.ts:474`: "warns when persisted quarantine inventory cannot be read" at line 515, "invalidates empty health receipts after worker and native registrations" at line 527, "does not create or adopt absent/native-only state during health cleanup" at line 544, and "keeps accepted registration when its health cleanup is superseded" at line 572. The documented case "an empty warm turn does not dispatch health cleanup again" is absent; the nearest current case is "joins worker-backed activation health cleanup" at line 686.
- TC-9 in tests.md:42 still lists `src/context-engine/registry.factory-admission.test.ts`, which is absent. The case now lives under "foreground admission" in `src/context-engine/registry.selection.test.ts:286`, with "propagates host admission failure without quarantining an uncalled factory (%s)" at line 294.
- TC-10 in tests.md:43 still lists `src/context-engine/registry.copied-view-resources.test.ts`, which is absent. The case now lives under "registry adoption" at `src/context-engine/registry.logical-turn-resources.test.ts:609`, with the assertion at line 610.
- TC-11 in tests.md:44 still lists `src/context-engine/registry.fallback-resources.test.ts`, which is absent. The cases now live under "lazy fallback native resources" at `src/context-engine/registry.logical-turn-resources.test.ts:387`, with the modes rejected-factory, primary-failure, and shared at line 388.

Requirements and specification were re-checked against the code paths and are in sync, so no review-requirements or review-specification regression was needed.
