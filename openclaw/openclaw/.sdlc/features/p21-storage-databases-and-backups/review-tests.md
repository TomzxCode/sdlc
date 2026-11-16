---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Storage, Databases, and Backups tests

## Sync drift: 2026-11-16

### Three referenced test files no longer exist (blocking)

- Evidence: none of these paths exist in the checkout and `git log --all` returns no history for any of them: `src/snapshot/local-repository-directory-identity.test.ts`, `src/state/openclaw-database-preflight.schema-only.test.ts`, `src/state/openclaw-state-db-schema-policy.test.ts`.
- Artifact says: the Test Files table lists all three (tests.md:30, tests.md:42, tests.md:61), and test cases TC-23 through TC-26, TC-82, and TC-119 plus the coverage matrix cite them.
- Code: the schema-only guidance case (TC-119) now lives in `src/state/openclaw-database-preflight.test.ts`. The snapshot directory identity case (TC-82) and the reader-admission schema-policy cases (TC-23 through TC-26) have no dedicated test file on this revision.
- Blocking: the test plan names files that cannot be run, so three groups of cases cannot be located from the plan.
