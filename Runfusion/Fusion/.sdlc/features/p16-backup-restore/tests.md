---
title: "Database & Memory Backup and Restore"
status: done
---

# Test Plan: Database & Memory Backup and Restore

## Scope

Covers the PostgreSQL dump creation, listing, retention, and restore path, the migration ledger reconciliation after a restore, the backup settings scope and migration, the automatic backup schedule, the `fn backup` and `fn memory-backup` command surfaces, the in-process scheduled backup interception, and the dashboard `GET` and `POST /api/backups` routes.

Out of scope: the PostgreSQL cutover (`fn db migrate`) and its pre-migration SQLite copy, the memory backend itself, and any end-to-end test that restores a live production cluster.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `pg_dump` produces the project, central, and bookkeeping dump files | A `PgBackupManager` with an injected client exec | Three published files that share one stem |
| TC-2 | The central dump is skipped when it is turned off | `includeCentral: false` | No central file, and the pair records the skip |
| TC-3 | Connection components travel through the libpq environment variables | A connection string with a password | The exec env carries `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`, and the argv carries none of them |
| TC-4 | The same libpq environment reaches `pg_restore` | A restore call | The restore exec env matches the dump exec env |
| TC-5 | A failed central dump removes the orphaned project dump | The central dump throws | No file from that stem remains |
| TC-6 | The project dump covers the `project` and `archive` schemas, the central dump covers only `central` | A recorded `pg_dump` argv | The schema flags match the two groups |
| TC-7 | The listing is empty when the backup directory is absent | No directory | An empty list |
| TC-8 | The listing reports project and central orphans and skips malformed files | A directory with orphan and malformed names | Orphans reported, malformed names ignored |
| TC-9 | One stem is shared by both halves | Two dumps in the same second | The same stem, and a counter suffix on collision |
| TC-10 | The listing returns pairs newest first | Several stored stems | Newest first |
| TC-11 | Retention keeps the configured count of stems | A retention count of 2 | The two oldest stems deleted, with every file of each stem |
| TC-12 | A source archive is listed before a destructive restore | A valid dump | The restore is called with the list-only flag first |
| TC-13 | A corrupt archive fails validation before the restore | A corrupt dump | The validation throws and no restore runs |
| TC-14 | The native client timeout stays bounded and the error is credential-safe | An injected client that never settles | The call is abandoned at the timeout, with no password in the message |
| TC-15 | A restore spawn failure redacts the password | A client that throws with a URL | The password is replaced by a mask |
| TC-16 | A missing dump file fails the restore | A path that does not exist | The restore throws |
| TC-17 | The stem claim is exclusive, publication is a rename, and no residue is left | Two concurrent claims | One owner, a rename-based publication, and no leftover files |
| TC-18 | Retention leaves pre-restore stems and live claims alone | A pre-restore stem and a live marker | Both survive the cleanup |
| TC-19 | Only abandoned reservations and their partial dumps are swept | A stale marker and a live marker | The stale one is removed and the live one is kept |
| TC-20 | The connection string parser handles both shapes | A URL form and a libpq keyword/value form | The expected host, port, user, password, and database |
| TC-21 | The migration rewind floor is the earliest missing sentinel | A catalog that misses an early relation | The floor is that relation's version, and the ledger is rewound from it |
| TC-22 | A later sentinel does not hide an earlier missing version | A catalog that misses `0011` while `0012` is present | The rewind starts at `0011` |
| TC-23 | A present column with the wrong primary key still rewinds | A catalog where the column exists but the key is single-column | The rewind starts at the key repair version |
| TC-24 | A present trigger with a missing policy or unforced RLS still rewinds | A catalog missing the trigger, the policy, or the forced RLS | The rewind starts at the partition repair version |
| TC-25 | A wrong column data type still rewinds | A catalog where the counter column is `integer` | The rewind starts at the bigint counter version |
| TC-26 | A failed baseline replay keeps the ledger versions | A baseline that throws | The ledger is unchanged |
| TC-27 | The reconciliation TLS policy separates loopback from remote hosts | A loopback URL and a remote URL | TLS off for loopback, certificate verification for remote |
| TC-28 | The backup root resolves to the global settings directory | A store that reports a global settings directory | The manager is built on that directory |
| TC-29 | An external connection string wins over the embedded registry | Both configured | The external string is used |
| TC-30 | The schedule status carries the run count, last run, and last outcome | A routine with a last run result | The evidence fields are populated and the output is bounded |
| TC-31 | An unchanged routine keeps its cadence | A routine that matches the desired fields | The sync plan is a no-op |
| TC-32 | The settings migration adopts a single configured project value | One project with a value | The global value is that value |
| TC-33 | The settings migration records a conflict when projects disagree | Two projects with different values | The conflict is recorded and the global value is not overwritten |
| TC-34 | The settings scope keeps the database policy global and the memory policy project-scoped | A global and a project configuration | The database keys land in global settings and the memory keys in project settings |
| TC-35 | The in-process backup command matcher accepts the canonical forms | `fn backup --create`, `npx -y runfusion.ai backup --create`, and case variants | All intercepted |
| TC-36 | The in-process backup command matcher refuses other forms | `fn backup --list`, a command with a shell continuation, and a trailing positional argument | None intercepted |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-37 | The backup inventory route returns the newest dumps and the schedule evidence | A registered backup routine | The response carries the backups, the count, the total size, and the schedule |
| TC-38 | A failed backup creation surfaces as a route error | A backup command that reports a failure | The route returns the failure instead of a success body |
| TC-39 | A failed listing still returns the schedule evidence | A manager that cannot list | An empty inventory, the listing error, and the schedule evidence |
| TC-40 | A paired restore validates, retains a pre-restore stem, then restores project before central | A fake `PgBackupManager` | The call order is validation, pre-restore capture, project restore, central restore |
| TC-41 | A bookkeeping restore is refused without a pre-restore rollback source | A stem that contains bookkeeping | The restore is refused before any client call |
| TC-42 | A central restore failure rolls the project group back from the retained stem | A fake manager that fails on central | The project rollback is recorded and the failure names the retained dumps |
| TC-43 | A reconciliation failure rolls the project group back | A reconcile seam that throws | The project rollback is recorded |
| TC-44 | A central-only restore leaves the bookkeeping untouched | A selected central dump | The bookkeeping is reported as skipped for a central-only restore |
| TC-45 | The `fn backup` commands resolve the project store and close it | A resolved project | Each command uses the resolved store and the store is closed |
| TC-46 | The `fn backup` commands retry a transient lock and fail cleanly when the lock persists | A store that reports a lock error | The command retries, then fails with a clear error and closes the store |
| TC-47 | The `fn memory-backup` commands create, list, and restore | A resolved project | Each command calls the matching core function |
| TC-48 | The `fn memory-backup` commands retry a transient lock and close the store | A store that reports a lock error | The command retries, then fails with a clear error and closes the store |
| TC-49 | The CLI routes the backup and memory-backup flags | The argument parser | Each flag reaches its command, and a missing flag prints the usage line and exits 1 |
| TC-50 | The scheduled backup runs in-process and resolves the shared cluster root | A schedule whose command is `fn backup --create` | The core backup command is called with the global settings directory |
| TC-51 | A manual automation run intercepts the in-process backup | A manual run of a `fn backup --create` schedule | The run is intercepted instead of shelling out |
| TC-52 | The settings section styles use the design tokens | The backup section stylesheet | The selectors exist and use the token variables |
| TC-53 | A live PostgreSQL cluster separates the bookkeeping dump from the project dump | An embedded or shared PostgreSQL test harness | The bookkeeping listing names the bookkeeping table and the project listing does not |
| TC-54 | A live restore returns the ledger to the captured version set | A captured backup and a drifted ledger | The ledger matches the captured set and the drift marker is gone |
| TC-55 | A live legacy pair leaves the bookkeeping untouched | A stem whose bookkeeping file is removed | The bookkeeping is reported as unavailable and the ledger is unchanged |
| TC-56 | A live central-only restore leaves the bookkeeping untouched | A central dump | The bookkeeping is reported as skipped and the ledger is unchanged |
| TC-57 | A live bookkeeping restore without a pre-restore stem is refused before any mutation | A live task row in the project schema | The call is refused and the task rows and the ledger are unchanged |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-58 | The dashboard operator creates a backup and sees it in the inventory | Open the Database Backups settings section, press Backup Now, then reload the inventory | The creation succeeds and the new dump appears in the list |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-59 | The `pg_dump` binary is missing | The backup fails with an error that explains the PostgreSQL client tools must be installed |
| TC-60 | The connection string cannot be parsed | The client receives no `PG*` values and the error is a clear connect failure |
| TC-61 | A selected file name is not a canonical dump name | The selection is refused with a message that names the expected pattern |
| TC-62 | A bookkeeping dump is selected for restore | The selection is refused because bookkeeping dumps cannot be restored alone |
| TC-63 | `skipCentral` and `centralOnly` are both requested | The restore is refused as contradictory |
| TC-64 | The pre-restore capture did not produce a complete stem | The restore is refused before any target mutation |
| TC-65 | The rollback of a committed group also fails | Both the original failure and the rollback failure are reported |
| TC-66 | The backup directory is absolute, contains a parent-directory segment, or starts with a drive letter | The directory is rejected |
| TC-67 | The cron expression is invalid | The backup run is refused with the invalid expression named |
| TC-68 | The retention count is outside 1 to 100 | The retention value is rejected |
| TC-69 | A memory snapshot would overwrite a changed memory file | The restore is refused and names the file, unless overwrite was requested |
| TC-70 | The memory snapshot holds neither memory root | The backup fails and names the scope it looked for |
| TC-71 | The memory backup directory escapes the project root | The directory is rejected |
| TC-72 | A memory snapshot name already exists | A counter suffix is added so the new snapshot does not overwrite the old one |

## Test Infrastructure

- Vitest across the `core`, `engine`, `dashboard`, and `cli` packages.
- `PgBackupManager` takes an injected client exec, so the dump and restore contract is proven without a live cluster and without wall-clock fixtures.
- The shared PostgreSQL harness (`packages/core/src/__test-utils__/pg-test-harness.ts`) provides the live cluster for the bookkeeping cases, and those cases skip when `pg_dump` and `pg_restore` are not on `PATH`.
- The dashboard route tests mount the registrar against a fake store.
- The CLI tests mock `@fusion/core` and the project context, and assert on the store close on every exit path.
- The memory snapshot file operations are exercised only through the CLI tests, which mock the core manager.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-6, TC-53 |
| FR-2 | TC-5, TC-17 |
| FR-3 | TC-9, TC-17 |
| FR-4 | TC-7, TC-8, TC-10, TC-61 |
| FR-5 | TC-12, TC-16, TC-40, TC-53 |
| FR-6 | TC-41, TC-57 |
| FR-7 | TC-42, TC-43, TC-64, TC-65 |
| FR-8 | TC-21, TC-22, TC-23, TC-24, TC-25, TC-26, TC-54 |
| FR-9 | TC-44, TC-56, TC-62, TC-63 |
| FR-10 | TC-11, TC-18, TC-19, TC-68 |
| FR-11 | TC-45, TC-46, TC-49 |
| FR-12 | TC-30, TC-31, TC-50, TC-67 |
| FR-13 | TC-28, TC-37, TC-38, TC-39, TC-52, TC-58 |
| FR-14 | TC-70, TC-72 |
| FR-15 | TC-47, TC-72 |
| FR-16 | TC-47, TC-69 |
| FR-17 | TC-47, TC-48, TC-49 |
| FR-18 | TC-30, TC-31, TC-48 |
| FR-19 | TC-34 |
| FR-20 | TC-32, TC-33 |
| FR-21 | TC-35, TC-36, TC-50, TC-51 |
| FR-22 | TC-19 |
| FR-23 | TC-31 |
| NFR-1 | TC-3, TC-4, TC-15, TC-20, TC-29, TC-60 |
| NFR-2 | TC-12, TC-13 |
| NFR-3 | TC-40 |
| NFR-4 | TC-14 |
| NFR-5 | TC-26 |
| NFR-6 | TC-66, TC-71 |
| NFR-7 | TC-27 |
| NFR-8 | TC-30, TC-39 |
| NFR-9 | TC-10 |
| NFR-10 | TC-59 |
| NFR-11 | TC-55 |
| NFR-12 | TC-30 |
| NFR-13 | TC-39 |
| NFR-14 | TC-69 |

## Key Test Files

- `packages/core/src/__tests__/postgres/pg-backup.test.ts`
- `packages/core/src/__tests__/backup.test.ts`
- `packages/core/src/__tests__/postgres/pg-backup-migration-bookkeeping.pg.test.ts`
- `packages/core/src/__tests__/backup-schedule-status.test.ts`
- `packages/core/src/__tests__/backup-settings-migration.test.ts`
- `packages/core/src/__tests__/backup-settings-scope.test.ts`
- `packages/cli/src/commands/__tests__/backup.test.ts`
- `packages/cli/src/commands/__tests__/backup-lock-retry.test.ts`
- `packages/cli/src/commands/__tests__/memory-backup.test.ts`
- `packages/cli/src/commands/__tests__/memory-backup-lock-retry.test.ts`
- `packages/cli/src/__tests__/bin.test.ts`
- `packages/engine/src/__tests__/cron-runner.test.ts`
- `packages/dashboard/src/routes/__tests__/register-system-maintenance-routes.test.ts`
- `packages/dashboard/src/__tests__/routes-automation.test.ts`
- `packages/dashboard/app/components/__tests__/SettingsModal.backup.css.test.ts`
