---
title: "Database & Memory Backup and Restore"
status: done
---

# Requirements: Database & Memory Backup and Restore

## Overview

Fusion keeps its durable state in one PostgreSQL cluster and keeps project and agent memory in files under the project root.
An operator can capture that state on demand or on a schedule, list what has been captured, restore it after a failure or a wrong change, and prune old copies.
A database backup is a set of PostgreSQL logical dumps covering the `project`, `archive`, and `central` schemas plus the migration bookkeeping table, so a restored database can be brought back in line with the code that is running.
A memory backup is a separate snapshot of the project and agent memory directories, captured and restored on its own schedule and its own retention count.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Needs a recoverable copy of the database and of memory before a risky change, and needs to see what is captured and when |
| Fleet maintainer | Needs the automatic backup schedule to run unattended and to report its last outcome |
| Database administrator | Needs a restored database to match the schema the running code expects |
| Maintainer / contributor | Needs the backup, restore, and prune commands to behave predictably from the CLI and the dashboard |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall create a database backup that dumps the `project` and `archive` schemas into a `fusion-pg-` dump file, the `central` schema into a `fusion-central-pg-` dump file, and the `public.fusion_schema_migrations` bookkeeping table into a `fusion-migrations-pg-` dump file, where each name ends with the shared timestamp stem and the `.dump` extension |
| FR-2 | Must | The system shall publish each dump by writing to a private in-progress artifact and renaming it into place only after the dump completed and the stem claim is still owned, so a partial dump is never listed and never restorable |
| FR-3 | Must | The system shall claim a backup stem exclusively with a per-stem reservation marker so two processes cannot capture the same stem |
| FR-4 | Must | The system shall list backup stems newest first, grouping the project, central, and migration files of one stem into a single entry, and shall report a stem whose central or migration file is missing as incomplete instead of presenting it as a full backup |
| FR-5 | Must | The system shall restore a selected stem by validating every source archive first, capturing a retained pre-restore stem, and then restoring the project and archive schemas, the central schema, and the migration bookkeeping in that order |
| FR-6 | Must | The system shall refuse to restore migration bookkeeping when the pre-restore capture is disabled, because that capture is the rollback source |
| FR-7 | Must | The system shall roll back every restore group it already committed from the retained pre-restore stem when a later group or the migration reconciliation fails, and shall report both the original failure and any rollback failure |
| FR-8 | Must | The system shall reconcile `public.fusion_schema_migrations` after a project restore by rewinding the ledger from the earliest missing schema sentinel and replaying the schema baseline, so an older dump cannot skip later schema upgrades |
| FR-9 | Must | The system shall treat a selected `fusion-central-pg-*` dump as a central-only restore that leaves the migration bookkeeping untouched, and shall reject contradictory restore options |
| FR-10 | Must | The system shall delete backups beyond the configured retention count, oldest first, and shall never delete a pre-restore stem or a stem that holds a live reservation |
| FR-11 | Must | The system shall provide the `fn backup --create`, `fn backup --list`, `fn backup --restore` with a file argument, and `fn backup --cleanup` commands |
| FR-12 | Must | The system shall run an automatic database backup on a cron expression as a global routine named "Database Backup" that runs `fn backup --create` |
| FR-13 | Must | The system shall expose the database backup inventory at `GET /api/backups` and an immediate backup creation at `POST /api/backups`, and shall show the inventory together with the schedule evidence in the global Database Backups settings section |
| FR-14 | Must | The system shall create a memory backup that snapshots the project memory directory `.fusion/memory` and the agent memory directory `.fusion/agent-memory` into a timestamped directory, honoring the configured scope |
| FR-15 | Must | The system shall list memory backups with their scope, file count, size, and creation time, and shall delete memory backups beyond the configured retention count, oldest first |
| FR-16 | Must | The system shall restore memory from a snapshot directory, and shall refuse to overwrite an existing memory file whose content differs from the snapshot unless the caller asks for overwrite |
| FR-17 | Must | The system shall provide the `fn memory-backup --create` command with an optional `--scope` argument of `project`, `agents`, or `all`, plus the `fn memory-backup --list` command and the `fn memory-backup --restore` command with a directory argument |
| FR-18 | Must | The system shall run an automatic memory backup on a cron expression as a project routine named "Memory Backup" that runs `fn memory-backup --create` |
| FR-19 | Must | The system shall store the database backup policy (`autoBackupEnabled`, `autoBackupSchedule`, `autoBackupRetention`, `autoBackupDir`) in global settings, and the memory backup policy (`memoryBackupEnabled`, `memoryBackupSchedule`, `memoryBackupRetention`, `memoryBackupDir`, `memoryBackupScope`) in project settings |
| FR-20 | Must | The system shall migrate the database backup settings from project scope to global scope once, adopting a single configured value, keeping any existing global value, and recording a conflict for the operator to resolve when projects disagree |
| FR-21 | Should | The system shall run the automatic backup inside the engine process when the scheduled command is the canonical `fn backup --create` or `fn memory-backup --create` form, and shall decline that interception when the command embeds a shell continuation, redirection, or substitution |
| FR-22 | Should | The system shall sweep abandoned in-progress artifacts and their reservation markers, and shall not sweep a live claim |
| FR-23 | Should | The system shall keep the next-run time of an existing backup routine when the desired routine fields are unchanged, so a settings save does not postpone a due backup |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall pass PostgreSQL connection components to `pg_dump` and `pg_restore` only through the libpq `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, and `PGDATABASE` environment variables, never as process arguments, and shall redact the connection-string password from any client error message |
| NFR-2 | Must | Data integrity | The system shall validate every source dump with `pg_restore --list` before any destructive restore, so a corrupt archive is refused before the target schemas are touched |
| NFR-3 | Must | Data integrity | The system shall run each restore in a single transaction, so a failed restore does not leave the target schemas half replaced |
| NFR-4 | Must | Availability | The system shall bound every `pg_dump` and `pg_restore` invocation with a client timeout of 120 seconds by default, so a hung native client cannot block the caller |
| NFR-5 | Must | Data integrity | The system shall apply the ledger rewind and the baseline replay in one transaction, so a failed replay cannot leave a rewound ledger against restored schemas |
| NFR-6 | Must | Security | The system shall reject a backup directory that is absolute, that contains a parent-directory segment, or that starts with a drive letter, for both the database and the memory backup directory |
| NFR-7 | Must | Security | The system shall require certificate verification when reconciling migrations against a remote PostgreSQL host, and shall keep TLS off for loopback and embedded clusters that have no TLS |
| NFR-8 | Must | Operability | The system shall report the schedule evidence (enabled state, cron expression, next run, last run, last outcome, run count) alongside the backup inventory, so an empty inventory cannot hide a schedule failure |
| NFR-9 | Must | Compatibility | The system shall order its `pg_dump` and `pg_restore` install-location search with the server major version, which is 15 for the embedded cluster, ahead of the later major versions, to avoid dump-format incompatibility |
| NFR-10 | Should | Operability | The system shall resolve `pg_dump` and `pg_restore` from `PATH` first and then from common install locations, and shall surface a missing binary as a named native client failure |
| NFR-11 | Should | Compatibility | The system shall keep a legacy two-member backup stem restorable, shall report its migration bookkeeping as unavailable, and shall still rewind and replay the ledger for it |
| NFR-12 | Should | Observability | The system shall record the run count, the last run time, and the last run outcome of the backup routine, so an operator can see whether the schedule works |
| NFR-13 | Should | Operability | The system shall warn the operator when automatic backups are enabled but no routine is registered, naming the two actions that reconcile it |
| NFR-14 | Should | Data integrity | The system shall write each restored memory file to a temporary file and rename it into place, so a failed restore does not leave a truncated memory file |

## Constraints

- Restore dumps are local recovery artifacts and must never be committed to git. The `.gitignore` patterns `fusion-pg-*.dump` and `fusion-pg-*.sql` guard that naming pattern (`FNXC:RecoveryArtifacts`).
- `pg_dump` and `pg_restore` are not bundled with `embedded-postgres`, which ships only `initdb`, `pg_ctl`, and the server binary. The operator must install the PostgreSQL client tools or configure the binary paths.
- The native backup commands take no cross-process lock and do not quiesce other writers. The operator must stop other Fusion writers and competing backup commands before a list, create, cleanup, or especially a restore.
- The database backup directory setting is relative to the global Fusion directory, and the memory backup directory setting is relative to the project root.
- The database backup policy is global because one PostgreSQL cluster holds every project. The memory backup policy stays project-scoped because the memory files are project-owned.
- A restore replaces the contents of the target schemas. It is destructive by design.
- The `fn backup` and `fn memory-backup` commands are operator surfaces. Agents have no backup or restore tool.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Create a database backup
      Given a running Fusion PostgreSQL cluster
      When the operator runs "fn backup --create"
      Then a "fusion-pg-" dump file holds the project and archive schemas
      And a "fusion-central-pg-" dump file holds the central schema
      And a "fusion-migrations-pg-" dump file holds public.fusion_schema_migrations
      And all three file names end with the same timestamp stem
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Partial dump is never published
      Given a dump that fails midway
      When the backup runs
      Then no final dump file exists for that stem
      And the listing does not offer the stem
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Two processes claim one stem
      Given two processes start a backup in the same second
      When both allocate a stem
      Then only one of them owns the stem
      And the other uses the next counter value
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: List stems newest first
      Given three stored backup stems
      When the operator runs "fn backup --list"
      Then the newest stem is listed first
      And one stem with a missing central file is shown as incomplete
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Restore a project stem
      Given a stored project stem
      When the operator runs "fn backup --restore" with a dump file name
      Then every source archive is validated first
      And a pre-restore stem is retained
      And the project and archive schemas are restored
      And the central schema is restored
      And the migration bookkeeping is restored
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Bookkeeping restore without a rollback source
      Given a caller that disables the pre-restore capture
      When the caller restores a stem that contains migration bookkeeping
      Then the request is refused
      And no dump client is invoked
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Central restore fails after the project restore committed
      Given a stem that restores the project schemas and then fails on central
      When the restore runs
      Then the project and archive schemas are rolled back from the retained pre-restore stem
      And the failure names the retained dumps
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Restore an older dump
      Given a restored schema that is missing a relation the ledger claims
      When the reconciliation runs
      Then the ledger is rewound from the earliest missing sentinel
      And the schema baseline is replayed
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Central-only restore
      Given a stored "fusion-central-pg-" dump file
      When the operator restores it
      Then only the central schema is restored
      And the migration bookkeeping is left unchanged
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Retention prunes the oldest stems
      Given a retention count of 2 and four stored stems
      When the cleanup runs
      Then the two oldest stems are deleted
      And every file of a pruned stem is deleted
      And a pre-restore stem is kept
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Backup command surface
      Given the "fn" CLI
      When the operator runs "fn backup" with no flag
      Then the command prints the usage line and exits with status 1
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Automatic database backup
      Given automatic database backups are enabled with a valid cron expression
      When the settings are saved
      Then a global routine named "Database Backup" runs "fn backup --create" on that cron expression
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Dashboard backup inventory
      Given the dashboard API is serving
      When the operator opens the Database Backups settings section
      Then "GET /api/backups" returns the stored dumps with the schedule evidence
      And "POST /api/backups" creates a backup immediately
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Create a memory backup
      Given a project with memory files and agent memory files
      When the operator runs "fn memory-backup --create"
      Then a timestamped snapshot directory holds a copy of ".fusion/memory" and a copy of ".fusion/agent-memory"
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: List and prune memory backups
      Given a memory retention count of 1 and three stored snapshots
      When a new snapshot is created
      Then the listing shows the scope, file count, size, and creation time
      And the two oldest snapshots are deleted
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Restore memory that would overwrite a changed file
      Given a memory file that differs from the snapshot
      When a restore runs without overwrite
      Then the restore is refused and names the file
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Memory backup command surface
      Given the "fn" CLI
      When the operator runs "fn memory-backup --create --scope agents"
      Then only the agent memory directory is snapshotted
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Automatic memory backup
      Given automatic memory backups are enabled with a valid cron expression
      When the settings are saved
      Then a project routine named "Memory Backup" runs "fn memory-backup --create" on that cron expression
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Settings scope
      Given a project and a global configuration
      When the operator writes the backup settings
      Then the database backup policy is stored globally
      And the memory backup policy is stored on the project
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Migrate the database backup settings once
      Given two projects with different backup settings and no global value
      When the migration runs
      Then the global value is adopted from the single configured project value
      And the conflict is recorded for the operator to resolve
      And a second run changes nothing
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Scheduled backup runs in-process
      Given a scheduled command of "fn backup --create"
      When the cron runner executes it
      Then the backup runs inside the engine process
      And a command of "fn backup --create && notify-send done" is not intercepted
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Sweep abandoned artifacts
      Given an abandoned reservation marker and a partial dump
      When the cleanup runs
      Then the marker and the partial dump are removed
      And a live reservation marker is kept
    ```

- [ ] **FR-23**

    ```gherkin
    @FR-23
    Scenario: Save unchanged backup settings
      Given a registered backup routine with a next-run time
      When the operator saves the same backup settings
      Then the routine keeps its next-run time
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Credentials stay out of the process list
      Given a PostgreSQL connection string with a password
      When a dump runs
      Then the password is passed only through the PGPASSWORD environment variable
      And it appears in no process argument
      And it is absent from the error message when the client fails
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Corrupt archive is refused before the restore
      Given a corrupt source dump
      When a restore runs
      Then the archive listing fails
      And no restore command is issued against the target schemas
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Restore runs as one transaction
      Given a valid source dump
      When the restore runs
      Then the restore client is called with a single-transaction flag
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Native client timeout
      Given a native client that never settles
      When a dump is requested
      Then the call is abandoned at the client timeout
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Baseline replay fails after the rewind
      Given a schema baseline that fails to apply
      When the reconciliation runs
      Then the ledger keeps its original versions
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Reject an unsafe backup directory
      Given a backup directory of "../escape"
      When the backup settings are applied
      Then the directory is rejected
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: TLS policy for migration reconciliation
      Given a connection string for a loopback host
      And a connection string for a remote host
      When the reconciliation connection is built
      Then the loopback connection has TLS off
      And the remote connection requires certificate verification
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Listing fails but schedule evidence survives
      Given the backup listing fails
      When "GET /api/backups" runs
      Then the response still carries the schedule evidence
      And it carries the listing error
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: Client binary search order
      Given the dump client is not on PATH
      When the client binary is resolved
      Then the install location for major version 15 is searched before the locations for major versions 16 and 17
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: Client binary is missing
      Given no "pg_dump" binary is on PATH or in a known install location
      When a backup runs
      Then the backup fails and the error names the pg_dump spawn failure
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: Restore a legacy two-member stem
      Given a stored stem with a project dump and a central dump and no bookkeeping dump
      When the operator restores the project dump
      Then the restore succeeds
      And the bookkeeping is reported as unavailable
      And the ledger is still rewound and replayed
    ```

- [ ] **NFR-12**

    ```gherkin
    @NFR-12
    Scenario: Schedule evidence carries the last outcome
      Given a backup routine that has run
      When the schedule status is built
      Then it carries the run count, the last run time, and the last outcome
    ```

- [ ] **NFR-13**

    ```gherkin
    @NFR-13
    Scenario: Enabled policy with no registered routine
      Given automatic backups are enabled and no routine is registered
      When the Database Backups settings section renders
      Then a warning names restarting Fusion and saving the settings again
    ```

- [ ] **NFR-14**

    ```gherkin
    @NFR-14
    Scenario: Memory restore writes through a temporary file
      Given a memory snapshot to restore
      When the restore runs
      Then each file is written to a temporary path and renamed into place
    ```

## Conflicts

None identified yet.

## Open Questions

1. The dashboard inventory lists one row per dump file, so a complete three-file stem appears as three rows. Should the inventory group by stem instead?
2. The CLI has no flag to restore the project schemas without also restoring the central schema. Is a project-only restore a required operator action?
3. Pre-restore stems are retained indefinitely and the retention count never prunes them. What is the intended way to reclaim that disk space once a restore is confirmed?
4. The CLI always restores memory with overwrite enabled, so the library guard against overwriting a changed memory file is unreachable from the operator surface. Should the CLI expose that choice?
