---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Storage, Databases, and Backups requirements

## Sync drift: 2026-11-16

### FR-4 pins schema versions that the code has advanced past (blocking)

- Evidence: `src/state/openclaw-schema-versions.ts:17,55` exports `OPENCLAW_AGENT_SCHEMA_VERSION = 42` and `OPENCLAW_STATE_SCHEMA_VERSION = 40`, and `package.json:18-21` declares `openclaw.schemaVersions` as state 40 and agent 42.
- Artifact says: FR-4 requires both sources to "report state version 28 and agent version 31" (requirements.md:40), and the FR-4 acceptance criterion repeats "the package block reports state 28 and agent 31" (requirements.md:153).
- Code: the code-side constants and the package metadata still agree, which is the invariant FR-4 protects, but both now report state 40 and agent 42.
- Blocking: an implementer or an acceptance check that uses the stated versions would assert the wrong values.

## Sync drift: 2026-11-23

### FR-4 pins schema versions that advanced again (blocking)

- Evidence: `src/state/openclaw-schema-versions.ts:19` exports agent version 43, `src/state/openclaw-schema-versions.ts:58` exports state version 41, and `package.json:19-22` mirrors those values.
- Artifact says: FR-4 requires state 28 and agent 31 (`requirements.md:40`), and its acceptance criterion repeats those values (`requirements.md:153`).
- Code: the lockstep invariant still holds, but both published versions advanced since the 2026-11-16 entry recorded 40 and 42.
- Blocking: an implementer or an acceptance check using 28 and 31 asserts the wrong versions.

### FR-10 and the constraints still label PostgreSQL experimental (advisory)

- Evidence: `docs/reference/database-engines.md:11-12` documents PostgreSQL as a supported alternative on qualified 16 to 18 runtimes, and `docs/gateway/postgresql.md:49` limits experimental status to other admitted majors.
- Artifact says: FR-10 requires PostgreSQL to be marked experimental (`requirements.md:46`), and the constraint repeats that rule (`requirements.md:72`).
- Code: `package.json:8-10` still lists sqlite and postgres, and the operator docs no longer apply blanket experimental status to the engine.
- Advisory: the wording no longer matches current operator documentation, but the shipped engine contract is unchanged.
