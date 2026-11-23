---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Storage, Databases, and Backups tests

## Sync drift: 2026-11-16

### Three referenced test files no longer exist (blocking)

- Evidence: none of these paths exist in the checkout and `git log --all` returns no history for any of them: `src/snapshot/local-repository-directory-identity.test.ts`, `src/state/openclaw-database-preflight.schema-only.test.ts`, `src/state/openclaw-state-db-schema-policy.test.ts`.
- Artifact says: the Test Files table lists all three (tests.md:30, tests.md:42, tests.md:61), and test cases TC-23 through TC-26, TC-82, and TC-119 plus the coverage matrix cite them.
- Code: the schema-only guidance case (TC-119) now lives in `src/state/openclaw-database-preflight.test.ts`. The snapshot directory identity case (TC-82) and the reader-admission schema-policy cases (TC-23 through TC-26) have no dedicated test file on this revision.
- Blocking: the test plan names files that cannot be run, so three groups of cases cannot be located from the plan.

## Sync drift: 2026-11-23

### Three referenced test files are still absent (blocking)

- Evidence: `src/state/openclaw-state-db-schema-policy.test.ts`, `src/state/openclaw-database-preflight.schema-only.test.ts`, and `src/snapshot/local-repository-directory-identity.test.ts` are absent from the checkout.
- Artifact says: the Test Files table lists all three (`tests.md:30`, `tests.md:42`, `tests.md:61`), and cases TC-23 through TC-26 (`tests.md:111-114`), TC-82 (`tests.md:170`), and TC-119 (`tests.md:208`) plus the coverage matrix cite them.
- Code: the retry and restore guidance case now lives at `src/state/openclaw-database-preflight.test.ts:480`, while no dedicated file carries the schema-policy or directory-identity cases.
- Blocking: the test plan names files that cannot be run, so those cases cannot be located from the plan.
- Note: this is the same blocking gap recorded on 2026-11-16, still present on this revision.
