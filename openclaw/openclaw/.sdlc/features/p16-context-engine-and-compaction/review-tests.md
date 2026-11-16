---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
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
