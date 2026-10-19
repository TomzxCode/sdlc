---
title: "Database & Memory Backup and Restore"
status: done
---

# Specification: Database & Memory Backup and Restore

## Overview

Database backup and restore live in `@fusion/core`. `BackupManager` owns the operator-facing contract and delegates every dump and restore to `PgBackupManager`, which shells out to `pg_dump` and `pg_restore` with the connection components passed through libpq environment variables. A backup is a stem of up to three dump files: the `project` and `archive` schemas, the `central` schema, and the `public.fusion_schema_migrations` bookkeeping table. A restore validates the sources, captures a retained pre-restore stem, restores the groups in order, and then reconciles the migration ledger so the restored schema matches the running code. Memory backup and restore are a separate concern: `MemoryBackupManager` copies the project and agent memory directories into timestamped snapshot directories and restores them file by file. The operator reaches both through the `fn backup` and `fn memory-backup` commands, the dashboard settings sections, and two dashboard API routes.

## Architecture

```
                 ┌───────────────────────────────────────────────────────────────┐
                 │  Operator surfaces                                            │
                 │                                                               │
                 │  fn backup --create|--list|--restore|--cleanup                 │
                 │  fn memory-backup --create|--list|--restore                    │
                 │  Settings > Database Backups  (global)                         │
                 │  Settings > Memory Backups    (project)                       │
                 │  GET /api/backups   POST /api/backups                          │
                 └───────────────────────────┬───────────────────────────────────┘
                                             │
                 ┌───────────────────────────▼───────────────────────────────────┐
                 │  @fusion/core                                                 │
                 │                                                               │
                 │  backup/backup.ts                    BackupManager            │
                 │  backup/backup-settings-migration.ts  settings migration      │
                 │  postgres/pg-backup.ts              PgBackupManager           │
                 │  postgres/restore-migration-reconcile.ts  ledger reconcile   │
                 │  memory/memory-backup.ts            MemoryBackupManager       │
                 │  automation/global-routine-store.ts  "Database Backup"         │
                 │  automation/routine-store.ts         "Memory Backup"           │
                 └──────┬────────────────────────────────┬────────────────────────┘
                        │                                │
        pg_dump / pg_restore                filesystem copy / rename
        (libpq PG* env vars)                (.fusion/memory, .fusion/agent-memory)
                        │                                │
   ┌────────────────────▼──────────────────┐  ┌──────────▼─────────────────────┐
   │  PostgreSQL cluster                   │  │  Project memory files          │
   │  schema project  (dump 1)             │  │  Agent memory files            │
   │  schema archive  (dump 1)             │  │  Snapshot directories          │
   │  schema central  (dump 2)             │  └────────────────────────────────┘
   │  public.fusion_schema_migrations      │
   │                                     (dump 3)                                │
   └────────────────────────────────────────┘

   Engine cron runner
   (packages/engine/src/scheduling/cron-runner.ts)
     "fn backup --create"        -> runBackupCommand in-process
     "fn memory-backup --create" -> runMemoryBackupCommand in-process
```

## Data Models

### Backup stem (PgBackupPair)

| Field | Type | Constraints | Description |
|---|---|---|---|
| timestamp | string | not null, `YYYYMMDD-HHMMSS` with an optional `-N` counter, prefixed `pre-restore-` for a pre-restore stem | Stem shared by the project, central, and migration dump files of one backup |
| project | PgDumpResult | optional | Dump of the `project` and `archive` schemas |
| central | PgDumpResult or `{ skipped: "disabled" \| "missing" }` | optional | Dump of the `central` schema, or the reason it was skipped |
| migrations | PgDumpResult or `{ skipped: "missing" }` | optional | Dump of `public.fusion_schema_migrations`, or the reason it is absent |

### Dump file (PgDumpResult)

| Field | Type | Constraints | Description |
|---|---|---|---|
| filename | string | not null, matches `fusion-` plus an optional `central-` or `migrations-`, plus an optional `pre-restore-`, plus `pg-`, plus the stem, plus `.dump` | Published file name |
| path | string | not null | Absolute path of the published file |
| sizeBytes | number | not null, 0 or greater | File size in bytes |
| createdAt | string | not null, ISO 8601 | Publication time |

### Backup selection (PgBackupSelection)

| Field | Type | Constraints | Description |
|---|---|---|---|
| family | string | not null, `regular` or `pre-restore` | Which family the selected file belongs to |
| stem | string | not null | Shared stem of the selected file |
| selectedKind | string | not null, `project` or `central` | Which file the operator selected |
| selectedPath | string | not null | Resolved path of the selected file |
| projectPath | string | not null | Sibling project dump path |
| centralPath | string | not null | Sibling central dump path |
| migrationsPath | string | not null | Sibling migration bookkeeping dump path |

### Restore result (BackupRestoreResult)

| Field | Type | Constraints | Description |
|---|---|---|---|
| restored | array of `project` and `central` | not null | Groups that were restored |
| preRestoreBackup | BackupPairInfo | optional | The retained rollback stem |
| projectRollback | string | optional, `succeeded` | Project rollback outcome |
| centralRollback | string | optional, `succeeded` | Central rollback outcome |
| migrationBookkeepingRollback | string | optional, `succeeded` | Bookkeeping rollback outcome |
| migrationBookkeeping | string | not null, `restored`, `unavailable`, or `skipped-central-only` | Bookkeeping outcome |

### Memory snapshot (MemoryBackupInfo)

| Field | Type | Constraints | Description |
|---|---|---|---|
| filename | string | not null, matches `memory-YYYY-MM-DD-HHMMSS` with an optional `-N` counter | Snapshot directory name |
| createdAt | string | not null, ISO 8601 | Snapshot creation time |
| size | number | not null, 0 or greater | Total bytes of the snapshot files |
| path | string | not null | Absolute path of the snapshot directory |
| scope | string | not null, `project`, `agents`, or `all` | Which memory roots the snapshot holds |
| entryCount | number | not null, 0 or greater | Number of files in the snapshot |

### Schedule status (BackupScheduleStatus)

| Field | Type | Constraints | Description |
|---|---|---|---|
| enabled | boolean | not null | Whether automatic backups are turned on |
| cronExpression | string | not null, defaults to `0 2 * * *` | The configured cron expression |
| routineRegistered | boolean | not null | Whether the backup routine exists |
| nextRunAt | string | optional | Next scheduled run time |
| lastRunAt | string | optional | Last run time |
| lastRunSucceeded | boolean | optional | Outcome of the last run |
| lastRunOutput | string | optional, truncated to 500 characters | Output of the last run |
| runCount | number | optional | How many times the routine has run |

### Database backup settings (global)

| Field | Type | Constraints | Description |
|---|---|---|---|
| autoBackupEnabled | boolean | not null, default `false` | Turns on the scheduled database backup |
| autoBackupSchedule | string | not null, default `0 2 * * *` | Cron expression for the database backup |
| autoBackupRetention | number | not null, default `7`, 1 to 100 | Number of backup stems to keep |
| autoBackupDir | string | not null, default `.fusion/backups`, relative to the global Fusion directory | Where the dump files are written |

### Memory backup settings (project)

| Field | Type | Constraints | Description |
|---|---|---|---|
| memoryBackupEnabled | boolean | not null, default `false` | Turns on the scheduled memory backup |
| memoryBackupSchedule | string | not null, default `0 3 * * *` | Cron expression for the memory backup |
| memoryBackupRetention | number | not null, default `14`, 1 to 100 | Number of memory snapshots to keep |
| memoryBackupDir | string | not null, default `.fusion/backups/memory`, relative to the project root | Where the snapshot directories are written |
| memoryBackupScope | string | not null, default `all`, one of `project`, `agents`, `all` | Which memory roots a snapshot holds |

### Migration rewind sentinel (RestoredSchemaRelationSentinel)

| Field | Type | Constraints | Description |
|---|---|---|---|
| version | string | not null | Migration version this sentinel guards |
| relations | string list | optional | Relations that must exist at that version |
| columns | relation and column pairs | optional | Columns that must exist at that version |
| primaryKeys | relation and ordered column list | optional | Primary key column list that must match, compared in order |
| columnTypes | relation, column, and data type | optional | Column data type that must match |
| triggers | relation and trigger name | optional | Trigger that must exist |
| policies | relation and policy name | optional | Row-level security policy that must exist |
| indexes | relation and index name | optional | Index that must exist |
| absentColumns | relation and column pairs | optional | Column that must not exist |
| forcedRowLevelSecurity | string list | optional | Relations that must have row-level security forced |

## API Contracts

The normative contract is in [`api.yaml`](api.yaml) (OpenAPI 3.1).
The table below is a summary; request and response schemas, error response bodies, and auth requirements are in `api.yaml`.

| Method | Path | Purpose |
|---|---|---|
| GET | /api/backups | List the stored database backup dumps and the automatic backup schedule evidence |
| POST | /api/backups | Create a database backup immediately and apply the retention count |

Error codes shared across endpoints:

| Status | Code | Description |
|---|---|---|
| 500 | BACKUP_FAILED | The backup command reported a failure, or the schedule could not be loaded |

A listing failure is not an error status. `GET /api/backups` returns 200 with an empty inventory, a `listError` string, and the schedule evidence.

### Command surface

| Command | Purpose |
|---|---|
| `fn backup --create` | Create a database backup stem and apply retention |
| `fn backup --list` | List the stored database backup stems, newest first |
| `fn backup --restore` with a file argument | Restore from a selected project or central dump |
| `fn backup --cleanup` | Delete the stems beyond the retention count |
| `fn memory-backup --create` with an optional `--scope` of `project`, `agents`, or `all` | Create a memory snapshot |
| `fn memory-backup --list` | List the memory snapshots, newest first |
| `fn memory-backup --restore` with a directory argument | Restore memory from a snapshot directory |

## Key Sequences

### Create a database backup

```
Operator            BackupManager        PgBackupManager      pg_dump       Filesystem
   |                     |                      |                |              |
   |-- fn backup --create|                      |                |              |
   |                     |-- createBackup() --->|                |              |
   |                     |                      |-- mkdir backup dir ------------>|
   |                     |                      |-- claim stem (marker) --------->|
   |                     |                      |                |              |
   |                     |                      |-- dump project+archive ------->|
   |                     |                      |                |-- .part file ->|
   |                     |                      |-- publish .part -> final ------>|
   |                     |                      |                |              |
   |                     |                      |-- dump central ---------------->|
   |                     |                      |-- publish .part -> final ------>|
   |                     |                      |                |              |
   |                     |                      |-- dump migration bookkeeping ->|
   |                     |                      |-- publish .part -> final ------>|
   |                     |                      |                |              |
   |                     |                      |-- release marker -------------->|
   |                     |                      |-- cleanup old stems ---------->|
   |                     |<-- PgBackupPair -----|                |              |
   |<-- output ---------|                      |                |              |
```

### Restore a database backup

```
Operator          BackupManager         PgBackupManager      pg_restore    Ledger
   |                   |                      |                |             |
   |-- fn backup --restore FILE          |                |             |
   |                   |-- resolve selection->|                |             |
   |                   |   (project or central; a bookkeeping dump alone is refused)
   |                   |                      |                |             |
   |                   |-- validate sources ->|                |             |
   |                   |                      |-- pg_restore --list ->         |
   |                   |                      |                |             |
   |                   |-- capture pre-restore stem              |             |
   |                   |                      |-- dump project+central+migrations|
   |                   |                      |                |             |
   |                   |-- restore project --->|                |             |
   |                   |                      |-- pg_restore (single transaction)|
   |                   |-- restore central --->|                |             |
   |                   |-- restore bookkeeping ->               |             |
   |                   |                      |                |             |
   |                   |-- reconcile ledger ---------------------->|             |
   |                   |   (rewind from earliest missing sentinel, replay baseline)
   |                   |                      |                |             |
   |<-- success ------ |                      |                |             |
   |                   |                                                             
   |   on failure after the project group committed:
   |                   |-- roll back project, central, bookkeeping from the retained stem
   |<-- failure with the retained dump names -----
```

### Create and restore a memory snapshot

```
Operator         MemoryBackupManager        Filesystem
   |                    |                       |
   |-- fn memory-backup --create                |
   |                    |-- mkdir snapshot tmp  |
   |                    |-- copy .fusion/memory -> snapshot/project
   |                    |-- copy .fusion/agent-memory -> snapshot/agents
   |                    |-- rename tmp -> final  |
   |<-- snapshot info --|                       |
   |                                                             
   |-- fn memory-backup --restore DIR           |
   |                    |-- read snapshot files |
   |                    |-- write each file to a temporary path
   |                    |-- rename each into place
   |                    |   (a changed destination file is refused without overwrite)
   |<-- success --------|                       |
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Backup format | `pg_dump --format=custom` logical dumps | Standard PostgreSQL format, supports parallel and selective restore through `pg_restore` |
| Schema coverage | Dump the `project`, `archive`, and `central` schemas rather than the whole cluster | The cluster can hold unrelated databases, so a whole-cluster dump would capture more than Fusion owns |
| Bookkeeping dump | A separate `fusion-migrations-pg-*` file for `public.fusion_schema_migrations` | `pg_dump` ignores `--schema` once `--table` is supplied, so the bookkeeping table needs its own archive |
| Credential transport | libpq `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` environment variables | Keeps the password out of the process argument list and points the client at the embedded cluster's random port; the non-functional `PG_CONNECTION_STRING` variable is not used |
| Publication | Dump to a private `.part` path, then rename after the stem claim is rechecked | A truncated archive is never restorable and never listed |
| Stem claim | An exclusively created `.reserved` marker holding an owner nonce | A filename existence check is a cross-process race, so a single atomic claim covers both halves of a stem |
| Retention | Count stems, keep the newest N, never prune a pre-restore stem or a live claim | The rollback pair promised by a restore must survive retention |
| Restore ordering | Project and archive, then central, then bookkeeping, then ledger reconciliation | The central schema holds the node and project registry, so it is restored after the project data it references |
| Rollback | Restore the retained pre-restore stem for every group already committed | A partial restore is worse than no restore, and the operator keeps the recovery evidence |
| Migration reconciliation | Rewind the ledger from the earliest missing schema sentinel, then replay the baseline in one transaction | Restoring an older dump drops later relations while the ledger still claims them, so the next startup would skip those migrations |
| Restore transaction | `pg_restore --single-transaction` | A failed restore must not leave the target schemas half replaced |
| Client timeout | 120 seconds per native client invocation, configurable | A hung native client must not block the caller indefinitely |
| Backup root | The global Fusion directory for database dumps, the project root for memory snapshots | One PostgreSQL cluster serves every project, while the memory files are project-owned |
| Settings scope | Database backup policy in global settings, memory backup policy in project settings | Follows the ownership of the data each policy protects |
| Scheduled execution | The engine runs the canonical `fn backup --create` form in-process | Shelling out would launch a possibly older binary from `PATH`; a command with shell metacharacters is not intercepted because its side effects cannot be mirrored |
| Memory restore write | Write to a temporary file, then rename | A failed restore must not leave a truncated memory file |
| Memory snapshot scope | `project`, `agents`, or `all` | The operator can snapshot one memory root or both |

## Risks and Unknowns

1. `pg_dump` and `pg_restore` are not bundled with `embedded-postgres`. A host without the PostgreSQL client tools cannot run a backup or restore, and the failure only appears when the command runs.
2. The native backup commands take no cross-process lock and do not quiesce other writers. A restore while the engine is writing can capture a torn state.
3. A `pg_dump` major version that differs from the server major version can produce a dump that warns about format incompatibility.
4. The migration reconciliation catalog is a hand-maintained list of sentinels. A new migration that is not in the catalog can be skipped by a restore of an older dump.
5. The pre-restore stems accumulate because retention never prunes them.
6. The dashboard inventory lists one row per dump file, so a complete three-file stem appears as three rows.
7. The CLI always restores memory with overwrite enabled, so the library guard against overwriting a changed memory file is unreachable from the operator surface.
8. `fn backup --restore` cannot restore the project schemas without also restoring the central schema, because the CLI does not expose the `skipCentral` option.

## Out of Scope

- Copying or moving a live database file (the SQLite file-copy backup path was removed with the PostgreSQL cutover)
- Backing up the Git worktrees, the git history, or the task worktree contents
- Backing up the dashboard configuration, the plugin directory, or the local model cache
- Encrypting the dump files at rest
- Uploading the dumps to object storage or any remote destination
- Cross-process locking or cluster-wide quiescence around the native backup commands
- The `fn db migrate` pre-migration SQLite copy, which belongs to the PostgreSQL cutover
