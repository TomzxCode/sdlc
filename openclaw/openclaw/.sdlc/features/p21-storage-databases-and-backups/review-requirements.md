---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Storage, Databases, and Backups requirements

## Sync drift: 2026-11-16

### FR-4 pins schema versions that the code has advanced past (blocking)

- Evidence: `src/state/openclaw-schema-versions.ts:17,55` exports `OPENCLAW_AGENT_SCHEMA_VERSION = 42` and `OPENCLAW_STATE_SCHEMA_VERSION = 40`, and `package.json:18-21` declares `openclaw.schemaVersions` as state 40 and agent 42.
- Artifact says: FR-4 requires both sources to "report state version 28 and agent version 31" (requirements.md:40), and the FR-4 acceptance criterion repeats "the package block reports state 28 and agent 31" (requirements.md:153).
- Code: the code-side constants and the package metadata still agree, which is the invariant FR-4 protects, but both now report state 40 and agent 42.
- Blocking: an implementer or an acceptance check that uses the stated versions would assert the wrong values.
