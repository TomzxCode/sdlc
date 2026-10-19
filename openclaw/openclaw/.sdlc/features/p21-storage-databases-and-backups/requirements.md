---
title: "Storage, Databases, and Backups"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Storage, Databases, and Backups

## Overview

OpenClaw keeps its durable data in two kinds of database and moves copies of that data to named external destinations.
The shared control-plane database at `~/.openclaw/state/openclaw.sqlite` holds configuration state, registries, approvals, plugin state, and shared runtime state.
Each agent owns a separate data-plane database at `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` that holds sessions, transcripts, memory indexes, auth state, and conversation state.
Both databases record their published schema in `PRAGMA user_version` and in a primary `schema_meta` row, apply forward-only migrations when an older supported database is opened, and refuse a database that a newer build wrote.
The Gateway process is the single owner of every OpenClaw database, so the CLI, Doctor, cron, and plugin child processes either route their mutations through the Gateway or take exclusive ownership while it is stopped.
A pluggable engine abstraction lets the shared state, agent, workboard, logbook, and team-reports families run on SQLite or on the experimental PostgreSQL adapter, and an offline port command moves existing stores between the two.
Named storage destinations give backups a place to land outside the machine, each one guarded by an explicit initialization marker and an optional per-location encryption key.
Portable backups and restores, in the form of local archives, verified SQLite snapshots, Git-backed dumps, and cold-storage session archives, let an operator recover state after a failed update, a lost disk, or a replaced host.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Gateway operator | Know where each database lives, which build can open it, and how to recover it |
| Update and migration owner | Move a database forward without losing rows, and know when a rollback needs the pre-upgrade backup |
| Backup operator | Produce verifiable copies, schedule them, and restore them onto a fresh target |
| Storage operator | Configure named destinations with encryption at rest and an explicit initialization step |
| Plugin and extension author | Use the engine abstraction, the storage provider contract, and the snapshot provider without a private path |
| Security reviewer | Confirm that database files, backup archives, and storage keys are protected and that key material is never written in plaintext |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall keep shared control-plane state in the shared database at `~/.openclaw/state/openclaw.sqlite` and each agent's data-plane state in `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`, with the canonical DDL for both owned by `src/state/openclaw-state-schema.sql` and `src/state/openclaw-agent-schema.sql` |
| FR-2 | Must | The system shall publish each database's schema version in two places, the SQLite `PRAGMA user_version` and the primary `schema_meta` row that records `role`, `agent_id`, `schema_version`, and `app_version` |
| FR-3 | Must | The system shall apply forward-only migrations when it opens an older supported database, and shall refuse to open a database whose published schema version is newer than the running build |
| FR-4 | Must | The system shall keep the code-side schema version constants in `src/state/openclaw-schema-versions.ts` in lockstep with the `openclaw.schemaVersions` block in `package.json`, so that both report state version 28 and agent version 31 |
| FR-5 | Must | The system shall treat the Gateway process as the single owner of every OpenClaw database and its state, and shall require the CLI, Doctor, cron, and plugin child processes to route mutations through the Gateway or to hold exclusive ownership while the Gateway is stopped |
| FR-6 | Must | The system shall record a durable external ownership claim for the shared state database in the `config_machine_state` row `gateway.supervision`, and shall refuse shared-state writes from an unsupervised process while that claim is held |
| FR-7 | Must | The system shall serialize cross-process work with host-owned leases recorded in the `state_leases` table, keyed by scope and lease key, carrying an owner token, an expiry, a heartbeat, and a renewal inside the caller's write transaction |
| FR-8 | Must | The system shall verify a database before admitting it and classify the result as `exact`, `startup-repairable`, `migration-required`, `incompatible`, or `indeterminate`, and shall expose the same classification through `openclaw database preflight` and `openclaw database preflight-agent` |
| FR-9 | Must | The system shall run SQLite format, schema, required index, and integrity checks once per physical database per process load, shall reuse a clean-close seal for that database, and shall keep a durable refusal in the quarantine store at `state/openclaw-quarantine.sqlite` when a database fails |
| FR-10 | Must | The system shall reach every database through one engine abstraction with a SQLite adapter and a PostgreSQL adapter, shall keep SQLite as the default, shall mark PostgreSQL as experimental, and shall treat the generated PostgreSQL DDL under `src/state/postgres-schema.generated/` as generated output that is not hand-edited |
| FR-11 | Must | The system shall port existing stores offline between engines with `openclaw database port`, scoped by the `state`, `agent`, `workboard`, `logbook`, or `team-reports` family, and shall write a manifest that supports both `--resume` and `--rollback` of an interrupted port |
| FR-12 | Must | The system shall expose named storage destinations under `storage.locations`, each with a provider, provider-owned settings, an explicit encryption choice, an initialization marker at the destination root that holds the location identity, and portable object keys, and shall refuse to publish an object over an existing key |
| FR-13 | Must | The system shall encrypt stored objects with a chunked AES-256-GCM envelope under a per-location master key derived from the configured passphrase with scrypt, and shall verify the passphrase against the location marker before any object is read or written |
| FR-14 | Must | The system shall produce portable backups as local archives, verified per-database SQLite snapshots, and Git-backed table dumps, shall restore them only onto a fresh target path, and shall record each run outcome in the shared `backup_runs` table that the `backup.status` Gateway method reports |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall keep database files, backup archives, and storage objects private to the host user, and shall never write a storage master key, a passphrase, or a decrypted object body into a marker file, a manifest, a log, or a Gateway response |
| NFR-2 | Must | Reliability | The system shall not repeat per-request database admission checks, and shall not probe a foreign commit with `PRAGMA data_version`, a version observation, or a foreign-observation scope, so that one physical database is validated once per process load and its facts are shared with every handle and worker |
| NFR-3 | Must | Availability | The system shall exit with status 78 when the Gateway finds a database schema newer than the running build, so that the generated service unit does not restart it in a loop, and shall name the compatible build in the refusal |
| NFR-4 | Must | Performance | The system shall bound every database wait with a 5 second SQLite busy timeout, shall stream storage objects in 1 MiB encrypted segments, and shall keep a snapshot or backup from holding an open read transaction across a yield |
| NFR-5 | Should | Maintainability | The system shall give each responsibility exactly one owner, so that the shared database, the per-agent database, the engine abstraction, the storage locations, and the backup artifacts each have a single module that decides and a separate module that performs the work |
| NFR-6 | Should | Portability | The system shall make stored copies verifiable from their own contents, so that a snapshot carries a manifest with a SHA-256 artifact digest, a Git dump carries a per-table row count and digest, and a storage object key stays within a portable character set |

## Constraints

- The Gateway process owns every OpenClaw database and its state.
- A CLI, Doctor, cron, or plugin child process either routes its mutations through the Gateway or holds exclusive ownership while the Gateway is stopped.
- Schema migrations run forward only, and an older build refuses a newer schema.
- A schema version marker is never lowered by hand, and rollback restores the verified pre-upgrade backup with its matching build.
- The shared state database stays the control plane, and the per-agent database stays the agent data plane.
- SQLite stays the default engine, and PostgreSQL stays experimental.
- The generated PostgreSQL DDL tree is output, so a hand edit there is discarded on the next generation run.
- A storage destination is initialized explicitly, and runtime writes never create the initialization marker.
- A backup archive or snapshot is restored only onto a fresh target path, and an existing file or sidecar at that path is refused.
- The full table catalog for the two databases is documented in `.sdlc/context/schema.dbml`, not in this feature directory.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Resolve the two default database locations
      Given a default state directory of ~/.openclaw
      When the shared database path and an agent database path are resolved
      Then the shared database path is ~/.openclaw/state/openclaw.sqlite
      And the agent database path is ~/.openclaw/agents/main/agent/openclaw-agent.sqlite
    ```

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Keep the canonical DDL in the two SQL files
      Given the shared state schema file and the agent schema file
      When each file is read
      Then the shared file declares the shared control-plane tables
      And the agent file declares the session, transcript, and memory tables
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Publish the schema version in both markers
      Given a freshly created shared state database
      When its schema version is read
      Then the SQLite user_version equals the published shared state version
      And the primary schema_meta row records role global, the schema version, and the app version
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Refuse a database whose metadata disagrees with the header
      Given a shared state database whose schema_meta version was edited to a lower value
      When the database is opened for maintenance
      Then the open is refused with a metadata schema version mismatch
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Migrate an older supported database forward
      Given a shared state database at a supported older version
      When it is opened by the current build
      Then the forward migration runs and the published version advances to the current version
      And the retained rows are preserved
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Refuse a database written by a newer build
      Given a shared state database whose user_version is one above the supported version
      When it is opened by the current build
      Then the open is refused with a newer schema version error naming the found and supported versions
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Keep the code constants and the package metadata aligned
      Given the openclaw schemaVersions block in package.json
      When it is compared with the exported schema version constants
      Then the package block reports state 28 and agent 31
      And the exported constants report the same two values
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Refuse an outside writer while the Gateway owns the state
      Given a running Gateway that owns the shared state database
      When an unsupervised outside process attempts a shared state write
      Then the write is refused with a state ownership error
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Admit a supervised writer that holds exclusive ownership
      Given a stopped Gateway and a process running under an external supervisor
      When that process opens the shared state database for writing
      Then the open is admitted and the write path proceeds
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Record and report a durable ownership claim
      Given a stopped Gateway and an externally supervised process
      When that process claims shared state ownership with a manager identifier
      Then the config_machine_state row gateway.supervision holds the version 1 external ownership record
      And a later ownership status read reports the same manager identifier
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Refuse a second manager from replacing a claim
      Given a shared state database already claimed by manager alpha
      When manager beta attempts an ownership claim
      Then the claim is refused and manager alpha keeps the durable ownership
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Acquire, renew, and release a state lease
      Given an empty state_leases table
      When a lease is acquired for a scope and key with a lease duration
      Then a lease row exists with the owner token and an expiry
      And the lease is renewed inside a write transaction and then released
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Report a held lease to a second acquirer
      Given a live lease held for a scope and key
      When a second acquirer requests the same scope and key
      Then the acquisition reports the lease as held with the current holder owner
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Classify a copied shared state database
      Given a consolidated copy of a shared state database at the current version
      When openclaw database preflight runs on that copy
      Then the reported status is exact and the target version equals the supported shared state version
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Report a copied database that needs migration
      Given a consolidated copy of a shared state database at an older supported version
      When openclaw database preflight runs on that copy
      Then the reported status is migration-required and the copy is not modified
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Refuse a preflight on a database with SQLite sidecars
      Given a copied state database that still has a WAL and shared memory sidecar
      When openclaw database preflight runs on it
      Then the result is indeterminate and names the sidecars
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Validate a physical database once per process load
      Given one shared state database opened by several handles and workers
      When the admission facts are inspected
      Then the format, schema, required index, and integrity checks run once for that physical file
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Keep a durable refusal for a failed database
      Given a shared state database that failed its integrity check
      When the failure is recorded and the database is opened again
      Then the quarantine store at state/openclaw-quarantine.sqlite holds the refusal
      And the database is refused again without a repair
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Report the supported engines and families
      Given the openclaw package metadata
      When the engine and family lists are read
      Then the engine list is sqlite and postgres
      And the PostgreSQL family list is state, agent, workboard, logbook, and team-reports
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Keep the generated PostgreSQL DDL as generated output
      Given the generated PostgreSQL schema tree
      When a change is needed in the PostgreSQL DDL
      Then the change is made in the generator or in the SQLite source
      And the generated tree is regenerated rather than hand-edited
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Port one family to another engine
      Given a stopped Gateway and a shared state database on SQLite
      When openclaw database port runs with the state family and a destination engine
      Then the port writes a manifest under the state directory recovery path
      And the original capture is retained so the port can be rolled back
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Refuse a port that names neither a destination nor a recovery mode
      Given a stopped Gateway
      When openclaw database port runs without a destination, a resume, or a rollback
      Then the command is refused with the three required options named
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Initialize a storage destination and hold its identity
      Given a configured filesystem storage location with an existing directory
      When openclaw storage init runs for that location
      Then the openclaw-storage.json marker at the destination root holds a version 1 record with a location identifier
      And running init again with the same settings verifies the existing marker
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Refuse to use a destination without a marker
      Given a configured storage location that was never initialized
      When a runtime operation opens that location
      Then the operation is refused with an unavailable state that names the init command
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Refuse a non-portable object key
      Given an initialized storage location
      When an object is published under a key that contains a path traversal segment
      Then the publication is refused before the provider is called
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Round-trip an encrypted object
      Given an initialized storage location with a passphrase
      When an object is written and read back
      Then the stored bytes differ from the plaintext
      And the read-back bytes match the written bytes exactly
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Refuse the wrong passphrase
      Given an initialized storage location with a passphrase
      When the location is opened with a different passphrase
      Then the open is refused with a wrong-key state
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Create and verify a per-database snapshot
      Given a shared state database on disk
      When openclaw backup sqlite create runs with the global source and a repository
      Then a snapshot directory holds a manifest and the database artifact
      And the manifest artifact digest matches the stored bytes
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Refuse a restore onto an occupied target
      Given a verified snapshot and a target path that already holds a file
      When openclaw backup sqlite restore runs against that target
      Then the restore is refused and the existing file is left untouched
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Report the recorded backup outcomes
      Given a recorded backup run in the shared backup_runs table
      When the backup.status Gateway method is called
      Then the response reports the run target, the latest run, and the configured storage locations
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Keep key material out of the marker and out of responses
      Given an initialized encrypted storage location
      When the marker file and a Gateway storage response are inspected
      Then the marker holds only the scrypt parameters, the salt, and the key check
      And no response body carries the passphrase or a plaintext object body
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Share one admission across handles and workers
      Given one shared state database opened by the main thread and by a worker
      When both handles run their first read
      Then the admission check runs once for that physical file
      And no data_version probe is issued on either path
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Stop the Gateway instead of restarting it against a newer schema
      Given a shared state database whose schema version is newer than the running build
      When the Gateway starts
      Then the process exits with status 78 and the refusal names the newer schema version
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Bound the database wait and the storage segment size
      Given a locked shared state database
      When a write waits for the lock
      Then the wait is bounded by a 5 second busy timeout
      And an encrypted storage object is produced in 1 MiB segments
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Keep one deciding owner per responsibility
      Given the state, storage, snapshot, and engine modules
      When each responsibility is mapped to its owner
      Then the shared database owner, the storage location owner, the snapshot owner, and the engine adapter are each a single module
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Verify a stored copy from its own contents
      Given a snapshot directory and a Git backup commit
      When each is verified
      Then the snapshot manifest carries an artifact SHA-256 and size
      And the Git manifest carries a row count and digest per table
    ```

## Conflicts

None identified yet.

## Open Questions

1. The shared state database and the per-agent databases are documented as SQLite paths, and the PostgreSQL adapter is experimental. Whether the PostgreSQL families should become the default for new installations is not decided.
2. The storage marker keeps a scrypt key check so a wrong passphrase can be reported, but it does not recover a lost passphrase. Whether a key-rotation path should be added to the storage contract is not decided.
3. The backup run ledger keeps a bounded window of runs, but the retention policy for the underlying archive files on a storage destination is configured per backup job rather than by a shared owner. Whether one shared retention owner should replace the per-job setting is not decided.
