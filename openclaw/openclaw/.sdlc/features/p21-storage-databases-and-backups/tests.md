---
title: "Storage, Databases, and Backups"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Storage, Databases, and Backups

## Scope

This plan covers the shared state database, the per-agent database, schema versioning and migration, database preflight and integrity, single-owner admission and leases, the database engine abstraction and the offline port, the named storage locations with their marker and encryption envelope, the snapshot and Git backup artifacts, and the backup outcome ledger.

It lists the existing test files that prove each requirement, so the coverage matrix maps a requirement onto the files that already exercise it. Every test case row names the file that carries it.

Out of scope:

- The table catalog itself, which is verified by the schema sources and the generated catalogs rather than by a test per table.
- The business behavior of the domain repositories that read and write through the persistence layer, including the user profile merge rules, the personal model account rules, and the GitHub publication lifecycle. Only the repository-level storage behavior is covered here.
- The session, transcript, memory, and channel behavior stored in the per-agent database.
- The plugin-defined database families and their own schemas.
- The Control UI surfaces that display backup and storage state.
- The `openclaw update` flow, except where it intersects with database preflight, migration, and backup coverage.

## Test Files

| File | Category | What it covers |
|---|---|---|
| `src/state/openclaw-state-db.test.ts` | Integration | Shared state database open, forward migrations, Doctor repairs and rollbacks, WAL reads, and refusal of an unrecognized registry schema |
| `src/state/openclaw-state-db-checkonce.test.ts` | Integration | Per-physical-file admission, clean-close seals, replacement file validation, and the refusal of corrupt current-version state on restart |
| `src/state/openclaw-state-db-schema-policy.test.ts` | Integration | Shared state reader admission policy, cold schema fact reuse, and the refusal of a rolled-back schema transaction |
| `src/state/openclaw-state-db-schema-version.test.ts` | Integration | Shared state content version facts and the schema publication worker |
| `src/state/openclaw-state-db-schema-migration-required.test.ts` | Integration | Deferred schema publication and its legacy update ledger deadlines |
| `src/state/openclaw-agent-db.test.ts` | Integration | Per-agent database open, registry, lease, deletion fencing, and agent schema migrations |
| `src/state/openclaw-agent-db.postgres.test.ts` | Integration | PostgreSQL agent store bootstrap, index and trigger migration, worker reads, and search |
| `src/state/openclaw-state-db.postgres.test.ts` | Integration | PostgreSQL shared state bootstrap, authority metadata migration, and anchor-preserving reads |
| `src/state/openclaw-database-preflight.test.ts` | Integration | Preflight classification, the package schema metadata alignment, and the registered-owner gate |
| `src/state/openclaw-database-preflight.explicit-file.test.ts` | Integration | Preflight of an explicit copied file, including the sidecar refusal |
| `src/state/openclaw-database-preflight.agent.test.ts` | Integration | Agent database preflight refusal paths |
| `src/state/openclaw-database-preflight.lifecycle.test.ts` | Integration | Preflight cancellation and failure handling |
| `src/state/openclaw-database-preflight.startup-integrity.test.ts` | Integration | Startup integrity, the clean-close seal reuse, and the newer-schema refusal priority |
| `src/state/openclaw-database-preflight.startup-prepared.test.ts` | Integration | Startup admission against reserved, unowned, and unreadable stores |
| `src/state/openclaw-database-preflight.schema-only.test.ts` | Integration | Schema-only preflight, retry guidance, and deferred agent upgrades |
| `src/state/openclaw-database-preflight.artifacts.test.ts` | Integration | Inspection under a live writer and the reader lock tolerance |
| `src/state/openclaw-database-preflight-agent-scheduler.test.ts` | Integration | Bounded parallel agent inspection and the strict foreground admission |
| `src/state/openclaw-state-ownership.test.ts` | Integration | External shared-state ownership inspection, the durable claim, and the write fence |
| `src/state/openclaw-state-lease.test.ts` | Integration | State lease renewal inside the caller's write transaction and exit cleanup |
| `src/state/openclaw-state-read-worker.test.ts` | Integration | Shared state read worker routing, pool retention, and cleanup |
| `src/state/openclaw-state-worker-registry.test.ts` | Integration | Write worker registry registration and dispatch |
| `src/state/openclaw-state-read-operation-registry.test.ts` | Integration | Read operation registry wiring |
| `src/state/openclaw-quarantine-store.test.ts` | Integration | Quarantine store decisions, version handling, and the clean-close seal |
| `src/state/agent-database-admission.test.ts` | Integration | Agent database admission refusals and the isolated secondary handling |
| `src/state/user-profiles.test.ts` | Integration | Durable user profile storage, merge, and rename behavior |
| `src/infra/database-engine/config.test.ts` | Unit | Per-family engine selection and the unused PostgreSQL connection |
| `src/infra/database-engine/admission-scope.test.ts` | Unit | The engine admission scope and the main-thread refusal |
| `src/infra/database-engine/port-command.test.ts` | Integration | The port command inspection path and the foreign-key failure mapping |
| `src/infra/database-engine/port-command.integration.test.ts` | Integration | The offline port, its dry run, its resume, and its rollback |
| `src/commands/doctor-database-port.test.ts` | Integration | Port engine-selection admission and the mixed-install family requirement |
| `src/snapshot/database-backup.test.ts` | Integration | The offline database backup admission and the invalid recovery config refusal |
| `src/snapshot/local-repository.test.ts` | Integration | The local snapshot repository, the pending-marker recovery, and the manifest parser |
| `src/snapshot/local-repository-directory-identity.test.ts` | Integration | Snapshot directory identity and its policy |
| `src/snapshot/git-backup.test.ts` | Integration | The Git backup repository, the scope selection, and the redacted diagnostics |
| `src/snapshot/git-backup-codec.test.ts` | Integration | The Git dump codec, the version manifest refusal, and the cell fidelity |
| `src/snapshot/git-backup-ownership.test.ts` | Integration | The Git backup artifact ownership and pruning |
| `src/snapshot/session-cold-storage-backup.test.ts` | End-to-end | The session cold archive across a full archive capture, a SQLite snapshot, and a Git backup |
| `src/snapshot/export-envelope.test.ts` | Unit | The PostgreSQL export envelope shape |
| `src/storage/encryption.test.ts` | Unit | The OCSTOR1 encryption envelope, its sizes, and its tamper refusals |
| `src/storage/filesystem.test.ts` | Integration | The filesystem provider publish, listing, root, and symlink rules |
| `src/storage/locations.test.ts` | Integration | The storage location identity, the marker, the passphrase, and the key rules |
| `src/commands/backup-sqlite.test.ts` | Integration | The SQLite snapshot create, list, verify, and restore commands |
| `src/commands/backup-restore.test.ts` | Integration | The archive restore, the fresh target rule, and the capacity check |
| `src/commands/backup-git.test.ts` | Integration | The Git backup command scope selection and the artifact verify and restore for an unconfigured agent |
| `src/commands/backup-schedule.test.ts` | Integration | The scheduled backup job creation and its redaction policy |
| `src/commands/backup-verify.test.ts` | Integration | The archive verification and its refusals |
| `src/commands/backup-verify-completeness.test.ts` | Integration | The completeness of the captured database set in the archive |
| `src/commands/backup-outcome.test.ts` | Integration | The recorded backup outcome, the exclusive custody, and the absent-database case |
| `src/commands/backup.create-verify.test.ts` | Integration | The archive create with immediate verification and its outcome settlement |
| `src/gateway/server-methods/storage.test.ts` | Integration | The `storage.locations.list` and `storage.locations.probe` Gateway methods |
| `test/storage-locations-r2.test.ts` | End-to-end | The object-store multipart publication and its authority fence |

## Unit Tests

| ID | Description | Input | Expected Output | Source |
|---|---|---|---|---|
| TC-1 | Storage encryption envelope computes the stored size from the plaintext size alone | Plaintext sizes of 0, 1, one segment, one segment plus one byte, and three segments plus 17 bytes | Each stored size is accepted and round-trips to the same plaintext size | `src/storage/encryption.test.ts` |
| TC-2 | Storage encryption envelope rejects impossible stored sizes | A negative size and a size beyond the segment limit | Both are refused with a size error | `src/storage/encryption.test.ts` |
| TC-3 | Storage encryption envelope rejects tampering | A truncated stream, a reordered segment, a modified header, trailing bytes, and the wrong key | Each case is refused and no plaintext is emitted | `src/storage/encryption.test.ts` |
| TC-4 | Storage encryption envelope bounds each yield and closes the source on cancellation | A cancelled encryption stream | Each yielded chunk stays within the segment bound and the source iterator is closed | `src/storage/encryption.test.ts` |
| TC-5 | Storage key and prefix validation refuses a non-portable key | A key with a `..` segment, an empty segment, a disallowed character, and an over-length key | Each is refused before the provider is called | `src/storage/locations.test.ts` |
| TC-6 | Storage marker derives the master key and verifies the key check | A marker with a scrypt descriptor and the correct passphrase | The key check matches; a wrong passphrase is refused with a wrong-key state | `src/storage/locations.test.ts` |
| TC-7 | Storage marker and its identity are stable across reopens | The same location opened twice with the same passphrase | Both opens report the same location identity and the same encrypted flag | `src/storage/locations.test.ts` |
| TC-8 | Shared state content version facts are read directly | A mutated content marker, a rolled-back transaction, a malformed marker, and a replaced database | The reader reports the committed fact in each case and never infers a version from table shape | `src/state/openclaw-state-db-schema-version.test.ts` |
| TC-9 | Shared state schema publication runs through the worker and refreshes the retained facts | A publication after an in-process updater write | The published version advances and the retained admission facts are refreshed | `src/state/openclaw-state-db-schema-version.test.ts` |
| TC-10 | A missing state database and its parent directory stay uncreated | A publication attempt against an absent database | Neither the database nor the parent directory is created | `src/state/openclaw-state-db-schema-version.test.ts` |
| TC-11 | State lease re-checks exact ownership inside the caller's write transaction | A lease whose owner token was replaced before the renewal | The renewal is refused with a lease-lost error | `src/state/openclaw-state-lease.test.ts` |
| TC-12 | State lease exit-cleanup diagnostics stay off standard output | A lease released during process exit | The machine-readable output on standard output is unchanged | `src/state/openclaw-state-lease.test.ts` |
| TC-13 | Per-family engine selection honors the family overrides and the default | A config with a default engine and a family override | Each family reports its effective engine and an unused PostgreSQL connection is not resolved | `src/infra/database-engine/config.test.ts` |
| TC-14 | Engine admission refuses main-thread use outside an admitted scope | A PostgreSQL statement issued on the main thread outside an admitted scope | The statement is refused and an admitted synchronous scope still succeeds | `src/infra/database-engine/admission-scope.test.ts` |
| TC-15 | The PostgreSQL export envelope refuses an anchor that belongs to another store | A correctly hashed anchor from a different store | The export is refused | `src/snapshot/export-envelope.test.ts` |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome | Source |
|---|---|---|---|---|
| TC-16 | Shared state database migrates a supported older version forward | A shared state database at an older supported schema version | The forward migration runs, the published version advances, and the retained rows survive | `src/state/openclaw-state-db.test.ts` |
| TC-17 | Shared state database rolls a failed Doctor repair back | A readability repair attempted against a foreign schema role | The transaction rolls back and the database is left as it was | `src/state/openclaw-state-db.test.ts` |
| TC-18 | Shared state database refuses an unrecognized agent registry schema | A shared state database whose agent registry schema is not recognized | The open is refused and no repair is attempted | `src/state/openclaw-state-db.test.ts` |
| TC-19 | Shared state database reads committed live WAL rows without changing the source | A shared state database in WAL mode with uncheckpointed commits | The committed rows are visible and the source files are unchanged | `src/state/openclaw-state-db.test.ts` |
| TC-20 | Shared state admission validates a physical file once per process load | A restarted current-schema database | The full verification is preserved across the restart and the repeated version probes are skipped | `src/state/openclaw-state-db-checkonce.test.ts` |
| TC-21 | A corrupt current-version database is refused on restart without a clean receipt | A database with a broken file and no clean-close seal | The database is refused and no repair is applied | `src/state/openclaw-state-db-checkonce.test.ts` |
| TC-22 | A replaced file is validated before the shared-state pathname is reused | A database file replaced under the same path | The replacement is validated rather than reusing the old facts | `src/state/openclaw-state-db-checkonce.test.ts` |
| TC-23 | Shared state reader admission reuses cold schema facts | A reader admitted after the schema facts are already known | The format and schema checks do not run again and no warm freshness probe is added | `src/state/openclaw-state-db-schema-policy.test.ts` |
| TC-24 | Shared state reader admission observes a migration committed during the first admission | A migration committed while the first reader admission is in flight | The reader picks up the committed facts and does not reuse the pre-migration ones | `src/state/openclaw-state-db-schema-policy.test.ts` |
| TC-25 | Shared state reader admission does not reuse a rolled-back schema transaction | A schema transaction that rolls back after validation | The rolled-back validation is not reused | `src/state/openclaw-state-db-schema-policy.test.ts` |
| TC-26 | Shared state reader admission does not create a missing database | A reader opened against an absent path | The database and its parent directory stay absent | `src/state/openclaw-state-db-schema-policy.test.ts` |
| TC-27 | Deferred schema publication waits for the legacy update ledger deadlines | A terminal update row and a running update row | The publication is deferred until every affected row clears its own deadline | `src/state/openclaw-state-db-schema-migration-required.test.ts` |
| TC-28 | Per-agent database opens the agent store and its shared registry under the default state owner | A configured agent with its own database file | Both the agent database and the shared registry open under one owner | `src/state/openclaw-agent-db.test.ts` |
| TC-29 | Per-agent database distinguishes an absent, an unowned, and an unsupported read-only database | Three agent database paths in those three states | Each is reported in its own state and none is repaired in place | `src/state/openclaw-agent-db.test.ts` |
| TC-30 | Per-agent database fences registration and lease claims beneath a pending deletion | A deletion journal entry for another agent | The registration and the lease claim are refused | `src/state/openclaw-agent-db.test.ts` |
| TC-31 | Per-agent database refuses a database path shared by two agent ids | One explicit path configured for two agents | The second agent is refused | `src/state/openclaw-agent-db.test.ts` |
| TC-32 | PostgreSQL shared state bootstraps, migrates the authority metadata, and reuses the admission | A PostgreSQL state store opened twice | The schema is bootstrapped, the lazy fragments are retained, and the second open reuses the admission | `src/state/openclaw-state-db.postgres.test.ts` |
| TC-33 | PostgreSQL shared state reads an existing store while another connection reserves its SQLite anchor | A store with a reserved anchor | The store is read and the anchor is not disturbed | `src/state/openclaw-state-db.postgres.test.ts` |
| TC-34 | PostgreSQL agent store migrates the version 27 indexes and revision triggers while retaining rows | An agent store at the previous version | The indexes and triggers are migrated and the retained rows and search index survive | `src/state/openclaw-agent-db.postgres.test.ts` |
| TC-35 | Database preflight keeps the package schema metadata aligned with the code constants | The `openclaw.schemaVersions` block in `package.json` and the exported constants | The two report the same state and agent versions | `src/state/openclaw-database-preflight.test.ts` |
| TC-36 | Database preflight refuses released legacy audit state before changing any artifact | A shared state database at a released legacy audit schema | The preflight is refused and no persistent artifact is modified | `src/state/openclaw-database-preflight.test.ts` |
| TC-37 | Database preflight refuses a legacy agent database without mutating its WAL | A configured agent database at a legacy schema | The preflight is refused and the WAL is untouched | `src/state/openclaw-database-preflight.test.ts` |
| TC-38 | Database preflight rejects a configured agent path owned by another agent | A configured path whose recorded owner is a different agent | The preflight is refused before any write | `src/state/openclaw-database-preflight.test.ts` |
| TC-39 | Database preflight admits a supported forward state migration after the Doctor-owned repair | A shared state database whose only blocker is the Doctor-owned audit repair | The preflight reports the migration as admissible | `src/state/openclaw-database-preflight.test.ts` |
| TC-40 | Database preflight checks every registered owner before a Gateway restart | A registry with several agent entries | Every registered owner is checked and the restart is refused on any failure | `src/state/openclaw-database-preflight.test.ts` |
| TC-41 | Database preflight reports a failed agent registry query as indeterminate | A registry query that fails | The result is indeterminate with the reason and not a false refusal | `src/state/openclaw-database-preflight.test.ts` |
| TC-42 | Preflight of an explicit copied file refuses a database with SQLite sidecars | A copied state database that still has a WAL and shared memory sidecar | The result is indeterminate and names the sidecars, and the copy is not modified | `src/state/openclaw-database-preflight.explicit-file.test.ts` |
| TC-43 | Preflight of an explicit copied file separates genuine drift from a legacy additive column | A copied database with an added nullable column and one with real drift | The additive column is admitted and the real drift is refused without a write | `src/state/openclaw-database-preflight.explicit-file.test.ts` |
| TC-44 | Startup integrity prefers the newer-schema refusal over a missing same-version column | A database that is both newer and missing a column | The newer-schema refusal is reported | `src/state/openclaw-database-preflight.startup-integrity.test.ts` |
| TC-45 | Startup cold-loads a compatible storage seal without validation SQL or snapshots | A database with a valid clean-close seal | The seal is reused and no validation SQL or snapshot runs | `src/state/openclaw-database-preflight.startup-integrity.test.ts` |
| TC-46 | Startup isolates a corrupt foreign secondary before reporting its integrity failure | A healthy primary with a corrupt secondary store | The secondary is isolated and the primary still starts | `src/state/openclaw-database-preflight.startup-integrity.test.ts` |
| TC-47 | Startup admission keeps an unowned non-reserved database strict | An unowned custom store at startup | The store stays in strict foreground admission | `src/state/openclaw-database-preflight.startup-prepared.test.ts` |
| TC-48 | Preflight inspection runs under a live writer without ending its transactions | A writer that keeps committing during the inspection | The inspection completes and the uncommitted writer versions are ignored | `src/state/openclaw-database-preflight.artifacts.test.ts` |
| TC-49 | Agent preflight inspection is bounded and keeps the strict foreground admission | A fleet of agent stores with one slow store | The inspections are bounded by the host CPU count and the strict store still prevents handoff | `src/state/openclaw-database-preflight-agent-scheduler.test.ts` |
| TC-50 | External shared-state ownership inspection does not create a state tree | A missing database path | The result is unowned and no directory is created | `src/state/openclaw-state-ownership.test.ts` |
| TC-51 | External shared-state ownership inspection reads a WAL when the shared memory index is absent | A database with a WAL and no shared memory file | The ownership row is read and the database family is not modified | `src/state/openclaw-state-ownership.test.ts` |
| TC-52 | External shared-state ownership does not expose a rolled-back ownership row | A rollback journal race during inspection | The rolled-back ownership is not reported | `src/state/openclaw-state-ownership.test.ts` |
| TC-53 | External shared-state ownership claim is idempotent for one manager and refuses a second | A database claimed by manager alpha | A repeat claim by alpha succeeds and a claim by beta is refused | `src/state/openclaw-state-ownership.test.ts` |
| TC-54 | External shared-state ownership refuses an unmarked writable open before changing the family | A writable open against an unmarked database | The open is refused and the database family is unchanged | `src/state/openclaw-state-ownership.test.ts` |
| TC-55 | External shared-state ownership fences a claim made immediately before a repair | A claim and a repair racing on the same database | The repair is fenced by the claim | `src/state/openclaw-state-ownership.test.ts` |
| TC-56 | External shared-state ownership keeps a snapshot stable when a WAL appears after capture | A snapshot captured before a WAL appears | The snapshot stays stable and the ownership read is not corrupted | `src/state/openclaw-state-ownership.test.ts` |
| TC-57 | Shared state read worker captures the queued read routing and schema facts | A read issued with a scoped environment | The routing and the schema facts are captured without reading unrelated environment values | `src/state/openclaw-state-read-worker.test.ts` |
| TC-58 | Shared state read worker retains the shared pool after a resource drain failure | A drain that fails | The pool is retained for the canonical retry and the error is preserved | `src/state/openclaw-state-read-worker.test.ts` |
| TC-59 | Shared state read worker reads externally created state after an absent read | A database created by another process after a read found none | The next read sees the externally created state without allocating a worker first | `src/state/openclaw-state-read-worker.test.ts` |
| TC-60 | Shared state write worker registry registers and dispatches its operations | A registered write operation | The operation is dispatched through its worker and the result is returned | `src/state/openclaw-state-worker-registry.test.ts` |
| TC-61 | Quarantine store keeps its decisions scoped to the recorded pathname | A hard-linked alias of a quarantined database | The alias is not quarantined and the original decision is preserved | `src/state/openclaw-quarantine-store.test.ts` |
| TC-62 | Quarantine store reports a newer schema version instead of reading its rows | A quarantine store written by a newer format | The refusal names the newer schema version | `src/state/openclaw-quarantine-store.test.ts` |
| TC-63 | Quarantine store validates a replaced store once while a sibling stays open | A replaced quarantine store with an open sibling handle | The replacement is validated once and the sibling stays open | `src/state/openclaw-quarantine-store.test.ts` |
| TC-64 | Agent database admission keeps a malformed secondary isolated while the required agents start | A required agent and a secondary with malformed ownership | The required agent starts and the secondary is isolated | `src/state/agent-database-admission.test.ts` |
| TC-65 | Durable user profile storage survives a rename, a merge, and a reused identity | A profile whose provider login is renamed and reused | The immutable owner stays isolated and the surviving merge head keeps the persisted names | `src/state/user-profiles.test.ts` |
| TC-66 | Filesystem storage provider publishes without clobbering existing bytes | An existing object at the target key | The publish is refused, the existing bytes survive, and the staging files are removed | `src/storage/filesystem.test.ts` |
| TC-67 | Filesystem storage provider lists by lexical prefix and reports metadata | Nested objects under a prefix | The listing returns the nested objects with their size and modification time, and delete is idempotent | `src/storage/filesystem.test.ts` |
| TC-68 | Filesystem storage provider requires an existing absolute directory | A missing root and a relative path | Both are refused and the root is never created | `src/storage/filesystem.test.ts` |
| TC-69 | Filesystem storage provider rejects a replaced root during a streamed put | A root swapped while the stream is running | The put fails and the replacement root is not filled | `src/storage/filesystem.test.ts` |
| TC-70 | Filesystem storage provider refuses symlink escapes | A symlinked object inside the root | The symlink is refused and excluded from the listing | `src/storage/filesystem.test.ts` |
| TC-71 | Storage location round-trips scoped encrypted streams without extra object reads | A scoped location with an encrypted object | The read-back bytes match and the listing and stat calls issue no object read | `src/storage/locations.test.ts` |
| TC-72 | Storage location initialization is idempotent with the same key and reports a wrong passphrase | An initialized location opened twice, then with a wrong passphrase | The second init verifies the existing marker and the wrong passphrase is refused | `src/storage/locations.test.ts` |
| TC-73 | Storage location refuses a missing marker with the recovery options | A location with no marker | The refusal is unavailable and names the init command and the display target | `src/storage/locations.test.ts` |
| TC-74 | Storage location skips foreign keys inside the requested prefix | A prefix that contains an unrelated object | The foreign object is skipped and the in-prefix objects are returned | `src/storage/locations.test.ts` |
| TC-75 | Storage location validates the namespace and the key before calling the provider | An invalid key and an invalid namespace | Both are refused before the provider call | `src/storage/locations.test.ts` |
| TC-76 | Local snapshot repository sorts snapshots newest first and ignores incomplete staging directories | A repository with committed snapshots and a partial staging directory | The listing is newest first and the partial directory is ignored | `src/snapshot/local-repository.test.ts` |
| TC-77 | Local snapshot repository recovers a complete pending snapshot | A pending marker with a complete snapshot | The snapshot is recovered through verify and restore and concurrent callers recover the same one | `src/snapshot/local-repository.test.ts` |
| TC-78 | Local snapshot repository rejects a markerless partial snapshot directory | A directory with a manifest but no commit marker | The directory is refused | `src/snapshot/local-repository.test.ts` |
| TC-79 | Local snapshot repository rejects an artifact that changed after the commit marker | An artifact modified after the snapshot was committed | The verification is refused and the changed artifact is not published | `src/snapshot/local-repository.test.ts` |
| TC-80 | Local snapshot repository refuses a restore when the final directory sync fails | A restore whose directory sync fails | The restore fails and the failure is reported | `src/snapshot/local-repository.test.ts` |
| TC-81 | Snapshot manifest parser refuses a manifest with unexpected fields | A manifest with an extra key, an unsupported schema version, a mismatched snapshot id, a non-canonical timestamp, a traversal path, a prefixed digest, an invalid agent id, a traversal basename, an out-of-range user version, and a zero size | Each is refused with a manifest error | `src/snapshot/local-repository.test.ts` |
| TC-82 | Snapshot directory identity is retained exactly through the repository, validation, and restore operations | A snapshot repository on a directory with a large device and inode identity | The exact directory identity is retained through every operation | `src/snapshot/local-repository-directory-identity.test.ts` |
| TC-83 | Offline database backup admission refuses an invalid recovery config before dispatch | A config that names a PostgreSQL connection that cannot be resolved | The backup is refused with the invalid-config error and no artifact is written | `src/snapshot/database-backup.test.ts` |
| TC-84 | Archive create verifies the archive and settles the outcome recording before it reports completion | A created archive and a failing outcome recording | The verification runs first and the completion report reflects the settled outcome | `src/commands/backup.create-verify.test.ts` |
| TC-85 | Archive capture keeps the configured, registered, and discovered databases complete | An archive missing one captured database | Each omission is refused by the completeness check | `src/commands/backup-verify-completeness.test.ts` |
| TC-86 | Git backup rejects a repository that overlaps the state directory | A Git repository inside the state directory and the reverse overlap | Both overlaps are refused | `src/snapshot/git-backup.test.ts` |
| TC-87 | Git backup dumps a configured external agent database for the explicit and the all scope | A configured agent database outside the default location | The agent database appears in both the explicit and the all scope | `src/snapshot/git-backup.test.ts` |
| TC-88 | Git backup reports Windows ACL remediation instead of a POSIX command | A Windows-style permission failure | The remediation names the ACL step and not a POSIX command | `src/snapshot/git-backup.test.ts` |
| TC-89 | Git backup redacts and durably preserves credential-bearing push diagnostics | A push that fails with a credential in the message | The diagnostic is redacted, the redaction is durable, and the raw secret never appears | `src/snapshot/git-backup.test.ts` |
| TC-90 | Git backup returns bounded redacted diagnostics from both failed history streams | A repository whose history cannot be read | The diagnostics are bounded and redacted | `src/snapshot/git-backup.test.ts` |
| TC-91 | Git dump codec restores historical agent data and refuses an incompatible version manifest | A Git dump and a manifest with a mismatched version | The historical data is restored and the mismatched manifest is refused | `src/snapshot/git-backup-codec.test.ts` |
| TC-92 | Git dump codec preserves the cell types, key order, quoted DDL, and triggers | A dump with quoted identifiers, case triggers, and mixed storage classes | The restored rows and schema match the source exactly | `src/snapshot/git-backup-codec.test.ts` |
| TC-93 | Git backup artifact ownership prunes only the declared artifacts | A repository with declared and extra files | The declared artifacts are refreshed and pruned while the extras stay | `src/snapshot/git-backup-ownership.test.ts` |
| TC-94 | SQLite backup command creates, lists, verifies, and restores the global database | A shared state database with committed rows and an empty repository | The snapshot, listing, verification, and fresh restore all succeed and the restored rows match | `src/commands/backup-sqlite.test.ts` |
| TC-95 | SQLite backup command requires exactly one named source and the required paths | A create with no source, a create with both sources, and a create with no repository | Each is refused with the named requirement | `src/commands/backup-sqlite.test.ts` |
| TC-96 | SQLite backup command reports a missing snapshot path for verify and restore | A verify and a restore against a missing path | Both report the missing path | `src/commands/backup-sqlite.test.ts` |
| TC-97 | SQLite backup command refuses a generic provider artifact before verify or restore | A snapshot directory produced by a different provider | The verify and the restore are refused | `src/commands/backup-sqlite.test.ts` |
| TC-98 | SQLite backup command does not claim completion when a corrupt database also rejects the outcome recording | A corrupt database during a snapshot create | The command fails and does not report a successful snapshot | `src/commands/backup-sqlite.test.ts` |
| TC-99 | Archive restore round-trips an archive into a fresh target with readable databases | A created archive and an empty target directory | The inventory matches, the databases are readable, and the target is populated | `src/commands/backup-restore.test.ts` |
| TC-100 | Archive restore refuses a non-empty target and accepts an empty one | A target with a file and an empty target | The non-empty target is refused and the empty one is accepted | `src/commands/backup-restore.test.ts` |
| TC-101 | Archive restore refuses insufficient target capacity before extraction | A target smaller than the archive | The restore is refused before any extraction and the hardlink data is counted once | `src/commands/backup-restore.test.ts` |
| TC-102 | Archive restore verifies a corrupt archive before touching an empty target | A corrupt archive and an empty target | The archive is refused and the target is left untouched | `src/commands/backup-restore.test.ts` |
| TC-103 | Archive restore cleans an incomplete target and preserves the extraction error | An extraction that fails, with and without a failing cleanup | The incomplete target is cleaned and the extraction error is preserved | `src/commands/backup-restore.test.ts` |
| TC-104 | Archive restore rejects a staging target inside a live agent directory | A target inside a configured external agent directory | The restore is refused | `src/commands/backup-restore.test.ts` |
| TC-105 | Git backup command resolves every agent root for an all-scope backup and keeps the scope conflict ahead of agent validation | A config with several agents and a conflicting scope selection | Every agent and its configured root resolve, and the scope conflict is reported first | `src/commands/backup-git.test.ts` |
| TC-106 | Scheduled backup adds one isolated command job with the selected Git backup arguments | A scheduled Git backup | One cron job is added with the selected arguments | `src/commands/backup-schedule.test.ts` |
| TC-107 | Scheduled backup redacts pushed schedules by default and warns only on full fidelity | A pushed schedule without and with the include-secrets flag | The default schedule is redacted and the full-fidelity schedule warns | `src/commands/backup-schedule.test.ts` |
| TC-108 | Scheduled backup refuses a pushed schedule when the repository has no origin | A repository without an origin remote | The schedule is refused | `src/commands/backup-schedule.test.ts` |
| TC-109 | Scheduled backup rejects a non-local Gateway before touching local paths | A schedule issued through a remote Gateway | The schedule is refused and no local path is touched | `src/commands/backup-schedule.test.ts` |
| TC-110 | Archive verification refuses a malformed SQLite snapshot, a missing asset payload, and a malformed manifest | An archive with a structurally valid but malformed snapshot, a manifest naming a missing payload, and a manifest with invalid JSON | Each is refused, and the malformed manifest does not leak the parser internals | `src/commands/backup-verify.test.ts` |
| TC-111 | A recorded backup outcome is written under exclusive custody and leaves an absent database absent | A host with no shared state database | The recording is skipped and no blank database is created | `src/commands/backup-outcome.test.ts` |
| TC-112 | The storage location Gateway methods list and probe without opening roots or activating providers | A configured filesystem location, an unloaded provider, and a location without a marker | The list reports the sanitized destinations, the probe reports the marker state, and no root is created | `src/gateway/server-methods/storage.test.ts` |
| TC-113 | The port command inspects without writing and refuses changed canonical SQLite data | A source database changed between the inspection and the write | The port is refused and the source is unchanged | `src/infra/database-engine/port-command.test.ts` |
| TC-114 | The port command takes no persistent action for a dry run | A dry-run port over a mixed install | No store and no config is written | `src/infra/database-engine/port-command.integration.test.ts` |
| TC-115 | The port command rolls back a preparing manifest before any target is verified | An interrupted port with a preparing manifest | The manifest is rolled back and no target is left behind | `src/infra/database-engine/port-command.integration.test.ts` |
| TC-116 | The port command resumes an interrupted migration from its retained manifest | An interrupted port with an active manifest | The port resumes from the retained manifest and the stores are archived rather than replaced | `src/infra/database-engine/port-command.integration.test.ts` |
| TC-117 | Port engine selection requires a family for a mixed install before touching stores | A config with one family on a different engine | The port is refused with the family requirement and the stores and config are unchanged | `src/commands/doctor-database-port.test.ts` |
| TC-118 | A homogeneous port is a no-op | A config whose families all share one engine | The port reports no stores and the config is unchanged | `src/commands/doctor-database-port.test.ts` |

| TC-119 | Preflight schema-only inspection keeps its retry and restore guidance with the affected agent databases | A shared state store whose agent databases need a migration | The inspection reports the affected agent databases together with their retry and restore guidance | `src/state/openclaw-database-preflight.schema-only.test.ts` |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome | Source |
|---|---|---|---|---|
| TC-120 | A snapshot and a restore round-trip through the CLI into a fresh database | Create a snapshot of the shared database, verify it, then restore it onto a fresh path | The restored database opens and reports the same schema version as the source | `src/commands/backup-sqlite.test.ts` |
| TC-121 | A session cold archive survives a full archive capture, a SQLite snapshot, and a Git backup | Back up an agent with cold transcript history by each of the three paths, delete the source archive, then restore | The restored events match the original and the restored database passes its integrity and foreign key checks | `src/snapshot/session-cold-storage-backup.test.ts` |
| TC-122 | An object-store multipart publication is fenced when the authority is lost mid-stream | Publish a large object while the backup namespace changes owner, with and without a failing cleanup | The publication is refused, the multipart upload is aborted, and the failure names the owner change without leaking the provider error | `test/storage-locations-r2.test.ts` |
| TC-123 | A corrupt cold archive is refused by every backup path | Corrupt the authoritative cold archive, then back up by each of the three paths | Every path fails with a verification error and no restored database is produced | `src/snapshot/session-cold-storage-backup.test.ts` |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior | Source |
|---|---|---|---|
| TC-124 | A database is opened by a build that supports an older schema | The open is refused with a newer schema version error naming the found and the supported version | `src/state/openclaw-state-db-checkonce.test.ts` |
| TC-125 | A shared state database is opened while a WAL appears between the snapshot and the read | The read stays on the captured snapshot and the ownership read is not corrupted | `src/state/openclaw-state-ownership.test.ts` |
| TC-126 | A shared state database carries a malformed ownership record | The read is refused with the typed metadata error rather than being reported as unowned | `src/state/openclaw-state-ownership.test.ts` |
| TC-127 | An ownership claim is attempted while a Doctor repair is in flight | The repair is fenced and the claim is applied to the current committed state | `src/state/openclaw-state-ownership.test.ts` |
| TC-128 | A lease is held by a process that then dies | The lease stays held until its expiry, and a later acquirer takes it after the expiry | `src/state/openclaw-state-lease.test.ts` |
| TC-129 | A lease is requested for a scope and key that another holder owns | The acquisition reports the lease as held with the current holder owner and expiry | `src/state/openclaw-state-lease.test.ts` |
| TC-130 | A database passes its integrity check but its `schema_meta` version disagrees with the header | The open is refused with a metadata schema version mismatch | `src/state/openclaw-state-db.test.ts` |
| TC-131 | A copied database still carries a WAL or shared memory sidecar | The preflight is indeterminate and names the sidecars, and the copy is not modified | `src/state/openclaw-database-preflight.explicit-file.test.ts` |
| TC-132 | A copied database is at a version newer than the running build | The preflight is incompatible and the copy is not modified | `src/state/openclaw-database-preflight.startup-integrity.test.ts` |
| TC-133 | An agent database is configured on a path that another agent already owns | The preflight is refused before any write and the other agent's database is untouched | `src/state/openclaw-database-preflight.test.ts` |
| TC-134 | An agent database is held for deletion recovery at an older schema | The runtime refuses the store and directs the operator to Doctor, without migrating the held file | `src/state/openclaw-database-preflight.test.ts` |
| TC-135 | A storage location is opened with a passphrase and the location was initialized without encryption | The open is refused with a wrong-key state that names the original configuration | `src/storage/locations.test.ts` |
| TC-136 | A storage location is initialized twice with different passphrases | The second init verifies the existing marker and reports a wrong passphrase | `src/storage/locations.test.ts` |
| TC-137 | A storage object is published with a declared size that does not match the body | The publication is refused and the object is not stored | `src/storage/locations.test.ts` |
| TC-138 | A storage object is published while the location marker changed after the location was opened | The publication is refused with an identity-changed message | `src/storage/locations.test.ts` |
| TC-139 | A storage listing returns an object outside the requested prefix | The listing fails instead of returning the foreign object | `src/storage/locations.test.ts` |
| TC-140 | A snapshot restore target already holds a file or a sidecar | The restore is refused and the existing file is left untouched | `src/snapshot/local-repository.test.ts` |
| TC-141 | A snapshot manifest names a snapshot id that does not match its directory | The manifest is refused | `src/snapshot/local-repository.test.ts` |
| TC-142 | A Git backup repository overlaps the state directory | The backup is refused in both overlap directions | `src/snapshot/git-backup.test.ts` |
| TC-143 | A Git backup push fails with a credential in the diagnostic text | The diagnostic is redacted and the raw credential is never persisted | `src/snapshot/git-backup.test.ts` |
| TC-144 | A backup archive is corrupt and the target directory is empty | The archive is refused before extraction and the empty target is left as it was | `src/commands/backup-restore.test.ts` |
| TC-145 | A restore target is inside a live agent directory | The restore is refused and the live directory is untouched | `src/commands/backup-restore.test.ts` |
| TC-146 | A backup run outcome is recorded on a host with no shared state database | The recording is skipped and no blank database is created | `src/commands/backup-outcome.test.ts` |
| TC-147 | A backup outcome write is refused because the local state owner changed | The outcome is not recorded and the caller is told to read `backup.status` | `src/commands/backup-outcome.test.ts` |
| TC-148 | A storage location points at a directory that was replaced by a mount point | The put fails and the replacement directory is not filled | `src/storage/filesystem.test.ts` |
| TC-149 | A port run is attempted while another process already hosts the owner | The port is refused before the config or the stores are touched | `src/infra/database-engine/port-command.integration.test.ts` |
| TC-150 | A port run is attempted with insufficient local capacity | The port is refused before the capture | `src/infra/database-engine/port-command.integration.test.ts` |
| TC-151 | A port run is attempted with aliased source paths | The port is refused without exposing the database payloads | `src/infra/database-engine/port-command.integration.test.ts` |

## Test Infrastructure

- Vitest is the test runner for every file listed here, and the suites live next to the code they cover.
- The state and agent database suites use real SQLite files through the state and agent database helpers, so the `STRICT` table constraints in the two SQL files are exercised directly.
- The preflight suites build real copies of the databases and manipulate `PRAGMA user_version` to stage the version states.
- The ownership suites stage WAL, shared memory, and rollback journal families to exercise the inspection paths without mutating the source files.
- The storage suites use a temporary directory tree as the filesystem backend, and the encryption suite drives the streaming envelope directly.
- The snapshot and Git backup suites shell out to real `git` and use real private snapshot directories, so the pending-marker and directory-durability paths are exercised against the filesystem.
- The PostgreSQL suites run against a real PostgreSQL server and are skipped when no server is configured.
- `test/storage-locations-r2.test.ts` mocks the S3 client of the bundled Cloudflare plugin, so the multipart publication path is exercised without a network call.
- The Doctor and port suites use the Doctor test helpers, which own a private state directory per case.
- `src/test-utils/openclaw-test-state.ts` provides the shared private state directory used by the command-level suites.

## Coverage Matrix

| Requirement | Test Files | Test Cases |
|---|---|---|
| FR-1 | `src/state/openclaw-state-db.test.ts`, `src/state/openclaw-agent-db.test.ts`, `src/state/openclaw-database-preflight.test.ts`, `src/state/openclaw-state-db.postgres.test.ts`, `src/state/openclaw-agent-db.postgres.test.ts` | TC-16, TC-28, TC-29, TC-31, TC-32, TC-34, TC-35, TC-36, TC-37, TC-38 |
| FR-2 | `src/state/openclaw-state-db-schema-version.test.ts`, `src/state/openclaw-state-db.test.ts` | TC-8, TC-9, TC-16, TC-130 |
| FR-3 | `src/state/openclaw-state-db.test.ts`, `src/state/openclaw-database-preflight.test.ts`, `src/state/openclaw-database-preflight.startup-integrity.test.ts` | TC-16, TC-17, TC-18, TC-35, TC-36, TC-44, TC-124, TC-132 |
| FR-4 | `src/state/openclaw-database-preflight.test.ts`, `src/state/openclaw-state-db-schema-version.test.ts` | TC-9, TC-35 |
| FR-5 | `src/state/openclaw-state-ownership.test.ts`, `src/state/openclaw-state-lease.test.ts`, `src/commands/backup-outcome.test.ts` | TC-50, TC-54, TC-55, TC-147 |
| FR-6 | `src/state/openclaw-state-ownership.test.ts` | TC-50, TC-51, TC-52, TC-53, TC-54, TC-55, TC-56, TC-126, TC-127 |
| FR-7 | `src/state/openclaw-state-lease.test.ts` | TC-11, TC-12, TC-128, TC-129 |
| FR-8 | `src/state/openclaw-database-preflight.test.ts`, `src/state/openclaw-database-preflight.explicit-file.test.ts`, `src/state/openclaw-database-preflight.startup-integrity.test.ts`, `src/state/openclaw-database-preflight.startup-prepared.test.ts`, `src/state/openclaw-database-preflight.schema-only.test.ts` | TC-35, TC-36, TC-37, TC-38, TC-39, TC-40, TC-41, TC-42, TC-43, TC-44, TC-47, TC-119, TC-131, TC-132, TC-133, TC-134 |
| FR-9 | `src/state/openclaw-state-db-checkonce.test.ts`, `src/state/openclaw-state-db-schema-policy.test.ts`, `src/state/openclaw-quarantine-store.test.ts`, `src/state/openclaw-state-read-worker.test.ts` | TC-20, TC-21, TC-22, TC-23, TC-24, TC-25, TC-26, TC-45, TC-46, TC-61, TC-62, TC-63 |
| FR-10 | `src/infra/database-engine/config.test.ts`, `src/infra/database-engine/admission-scope.test.ts`, `src/infra/database-engine/port-command.test.ts`, `src/infra/database-engine/port-command.integration.test.ts`, `src/commands/doctor-database-port.test.ts`, `src/snapshot/export-envelope.test.ts`, `src/state/openclaw-state-db.postgres.test.ts`, `src/state/openclaw-agent-db.postgres.test.ts` | TC-13, TC-14, TC-15, TC-32, TC-33, TC-34, TC-113, TC-114, TC-115, TC-116, TC-117, TC-118 |
| FR-11 | `src/commands/doctor-database-port.test.ts`, `src/infra/database-engine/port-command.integration.test.ts` | TC-114, TC-115, TC-116, TC-117, TC-118, TC-142, TC-149, TC-150, TC-151 |
| FR-12 | `src/storage/filesystem.test.ts`, `src/storage/locations.test.ts` | TC-5, TC-6, TC-7, TC-66, TC-67, TC-68, TC-69, TC-70, TC-71, TC-72, TC-73, TC-74, TC-75, TC-135, TC-136, TC-137, TC-138, TC-139, TC-148 |
| FR-13 | `src/storage/encryption.test.ts`, `src/storage/locations.test.ts` | TC-1, TC-2, TC-3, TC-4, TC-6, TC-7, TC-71, TC-72, TC-135, TC-136 |
| FR-14 | `src/commands/backup-sqlite.test.ts`, `src/commands/backup-restore.test.ts`, `src/commands/backup-git.test.ts`, `src/commands/backup-schedule.test.ts`, `src/commands/backup-verify.test.ts`, `src/commands/backup-verify-completeness.test.ts`, `src/commands/backup.create-verify.test.ts`, `src/commands/backup-outcome.test.ts`, `src/snapshot/local-repository.test.ts`, `src/snapshot/git-backup.test.ts`, `src/snapshot/git-backup-codec.test.ts`, `src/snapshot/git-backup-ownership.test.ts`, `src/snapshot/session-cold-storage-backup.test.ts`, `src/gateway/server-methods/storage.test.ts` | TC-81, TC-83, TC-84, TC-85, TC-86, TC-87, TC-88, TC-89, TC-90, TC-91, TC-92, TC-93, TC-94, TC-95, TC-96, TC-97, TC-98, TC-99, TC-100, TC-101, TC-102, TC-103, TC-104, TC-105, TC-106, TC-107, TC-108, TC-109, TC-110, TC-111, TC-112, TC-120, TC-121, TC-123, TC-140, TC-141, TC-142, TC-143, TC-144, TC-145, TC-146, TC-147 |
| NFR-1 | `src/storage/encryption.test.ts`, `src/storage/locations.test.ts`, `src/snapshot/git-backup.test.ts`, `test/storage-locations-r2.test.ts` | TC-1, TC-3, TC-6, TC-72, TC-89, TC-122, TC-135, TC-136, TC-143 |
| NFR-2 | `src/state/openclaw-state-db-checkonce.test.ts`, `src/state/openclaw-state-db-schema-policy.test.ts`, `src/state/openclaw-state-read-worker.test.ts` | TC-20, TC-21, TC-22, TC-23, TC-24, TC-25, TC-26, TC-57, TC-58, TC-59, TC-125 |
| NFR-3 | `src/state/openclaw-state-db-checkonce.test.ts`, `src/state/openclaw-database-preflight.startup-integrity.test.ts` | TC-44, TC-124, TC-132 |
| NFR-4 | `src/storage/encryption.test.ts`, `src/snapshot/local-repository.test.ts`, `src/commands/backup-restore.test.ts` | TC-1, TC-4, TC-80, TC-101 |
| NFR-5 | `src/state/openclaw-state-db.test.ts`, `src/state/openclaw-agent-db.test.ts`, `src/infra/database-engine/config.test.ts`, `src/commands/backup-sqlite.test.ts`, `src/snapshot/git-backup-codec.test.ts` | TC-13, TC-16, TC-28, TC-35, TC-91, TC-94, TC-120 |
| NFR-6 | `src/snapshot/local-repository.test.ts`, `src/snapshot/git-backup-codec.test.ts`, `src/snapshot/git-backup.test.ts`, `src/commands/backup-sqlite.test.ts` | TC-81, TC-86, TC-91, TC-92, TC-94, TC-120, TC-121 |
