---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Storage, Databases, and Backups specification

## Sync drift: 2026-11-16

### Data model schema versions are stale (blocking)

- Evidence: `src/state/openclaw-schema-versions.ts:17,55` exports agent version 42 and state version 40, and `package.json:18-21` mirrors those values.
- Artifact says: the shared state data model lists schema version 28 (specification.md:114) and the per-agent data model lists schema version 31 (specification.md:126).
- Code: both databases now publish state version 40 and agent version 42 in `PRAGMA user_version` and the primary `schema_meta` row.
- Blocking: the data model tables state the wrong published versions for both databases.

### The API Contracts table omits shipped database subcommands (advisory)

- Evidence: `src/cli/program/register.database.ts:95-410` registers `prepare-state`, `migration-capture`, `capabilities`, `create`, `restore`, and `restore-session-dependencies` under `openclaw database` in addition to the commands the spec lists.
- Artifact says: the CLI portion of the API Contracts table (specification.md:274-280) lists only `port`, `preflight`, `preflight-agent`, `verify-preservation`, `restore-migration-backup`, and the two `ownership` subcommands.
- Code: `openclaw database` also exposes six more subcommands that operate on the databases and migration captures this feature owns, including exact PostgreSQL state preparation and session dependency restore.
- Advisory: the summary table is incomplete, so a reader would not know these operator entry points exist.
