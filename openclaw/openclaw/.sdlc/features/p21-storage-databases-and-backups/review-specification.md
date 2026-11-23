---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-23

### Data model schema versions are stale again (blocking)

- Evidence: `src/state/openclaw-schema-versions.ts:19` exports agent version 43, `src/state/openclaw-schema-versions.ts:58` exports state version 41, and `package.json:19-22` mirrors both values.
- Artifact says: the shared state data model lists schema version 28 (`specification.md:114`) and the per-agent data model lists 31 (`specification.md:126`).
- Code: both databases publish the advanced versions, and the version constants still agree with package metadata.
- Blocking: the data model tables report the wrong published versions for both databases.

### The table catalog count is stale (advisory)

- Evidence: `.sdlc/context/schema.dbml:13-3300` contains 216 `Table` declarations, and its generated header is at line 1.
- Artifact says: the specification claims 206 tables in two places (`specification.md:105`, `specification.md:436`).
- Code: the generated catalog owns 216 tables.
- Advisory: the count is documentation only, and the catalog itself remains the source of truth.

### The API Contracts table still omits six shipped database subcommands (advisory)

- Evidence: `src/cli/program/register.database.ts:149,172,175,189,221,351` registers `prepare-state`, `migration-capture`, `capabilities`, `create`, `restore`, and `restore-session-dependencies`.
- Artifact says: the CLI rows at `specification.md:274-280` list only `port`, `preflight`, `preflight-agent`, `verify-preservation`, `restore-migration-backup`, and the two `ownership` subcommands.
- Code: the six additional subcommands are still present on this revision.
- Advisory: readers would not discover these operator entry points from the summary table.

### PostgreSQL status wording is stale (advisory)

- Evidence: `docs/reference/database-engines.md:11-12` documents PostgreSQL as a supported alternative on qualified 16 to 18 runtimes, and `docs/gateway/postgresql.md:49` reserves experimental status for other admitted majors.
- Artifact says: the technical decision calls PostgreSQL experimental (`specification.md:411`), and the risk entry repeats that label (`specification.md:424`).
- Advisory: the wording conflicts with current operator documentation, and the engine behavior itself is unchanged.
