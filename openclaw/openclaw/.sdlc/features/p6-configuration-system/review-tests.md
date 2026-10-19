---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Configuration System test plan

## Sync drift: 2026-10-19

### Blocking: two listed test files no longer exist

- Artifact says (tests.md:17): "| `src/config/validation.test.ts` | Config validation logic |".
- Artifact says (tests.md:20): "| `src/config/io.parse.test.ts` | Config file parsing |".
- Code: no `src/config/validation.test.ts` and no `src/config/io.parse.test.ts` exist in the tree.
- Code: validation logic now lives in `src/config/validation.ts` with its own suites `src/config/validation.policy.test.ts`, `src/config/validation.async.test.ts`, `src/config/validation.allowed-values.test.ts`, `src/config/validation.channel-schema-errors.test.ts`, `src/config/validation.channel-metadata.test.ts`, `src/config/validation.dm-policy.test.ts`, `src/config/validation.sandbox-container-env.test.ts`, `src/config/validation.cold-imports.test.ts`, `src/config/validation-plugin-config.identity.test.ts`, and `src/config/validation-plugin-config.native-catalog.test.ts`.
- Code: config file parsing now lives in `src/config/io.load.ts`, `src/config/io.read-helpers.ts`, and `src/config/io.factory.ts`, with suites `src/config/io.load-async.test.ts`, `src/config/io.load-read-error.test.ts`, `src/config/io.load-env-restore.test.ts`, `src/config/io.read-helpers.test.ts`, `src/config/io.factory.test.ts`, and `src/config/io.invalid-config.test.ts`.
- Code: `src/config/schema.test.ts:8` already imports `validateConfigObjectRaw` from `./validation.js`, so schema-level validation is covered by the schema suite.
- Impact: two rows of the unit test table point at files that cannot be opened, and the replacement suites are not listed.
- Classification: blocking.

### Blocking: the env-var substitution coverage row names the wrong suite

- Artifact says (tests.md:48): "FR-3 (Env var substitution) | `config.env-vars.test.ts`".
- Artifact also lists (tests.md:24): "| `src/config/config.env-vars.test.ts` | Environment variable substitution |".
- Code: `src/config/config.env-vars.test.ts:1-30` covers runtime environment publication and ownership, and its test names are about publishing, staging, restoring, and precedence (for example "blocks config-owned host controls and startup env vars", "publishes only captured dotenv after failed loading and preserves prior ownership").
- Code: the actual substitution contract is implemented in `src/config/env-substitution.ts` and covered by `src/config/env-substitution.test.ts`, which asserts `${FOO}`, `${FOO:-fallback}`, and `$${LITERAL}` escape behavior.
- Code: `src/config/config.env-vars.test.ts:278-281` calls `resolveConfigEnvVars` only as an aside inside the dotenv reload case.
- Impact: FR-3's dedicated suite is missing from the plan and the named suite covers a different concern.
- Classification: blocking.

### Blocking: the redaction coverage row names no test file

- Artifact says (tests.md:52): "FR-9 (Secret redaction) | Covered by general redaction tests".
- Code: the dedicated redaction suites are `src/config/redact-snapshot.test.ts`, `src/config/redact-snapshot.secret-ref.ts`, `src/config/redact-snapshot.raw.ts`, `src/config/redact-snapshot.test-helpers.ts`, `src/plugin-sdk/migration-sensitive-redaction.test.ts`, and `src/secrets/store/secret-store.redaction.test.ts`.
- Code: `src/config/schema.test.ts:1` also states it covers "canonical config schema defaults, validation, and sensitive redaction".
- Code: `src/config/config-journal-snapshot.test.ts` covers the journal snapshot path, and `src/config/io.audit.test.ts` covers the config audit record path.
- Impact: the row names no artifact, so a reviewer cannot verify NFR-1 or FR-9 from the plan.
- Classification: blocking.

### Advisory: notable test areas the artifact does not list

- Code: `src/secrets/resolve.test.ts`, `src/secrets/resolve.mixed-failures.test.ts`, `src/secrets/resolve.manifest-registry.test.ts`, `src/secrets/ref-contract.test.ts`, `src/secrets/audit.test.ts`, `src/secrets/configure.test.ts`, `src/secrets/apply.test.ts`, and `src/secrets/plan.test.ts` cover the SecretRef resolution, audit, configure, apply, and plan surfaces that the requirements do not cover either.
- Code: `src/flows/bundled-health-checks.test.ts`, `src/flows/doctor-config-validation-check.ts`, `src/flows/doctor-core-checks.test.ts`, and `src/flows/doctor-lint-flow.ts` cover the Doctor health-check and lint layer that FR-6 depends on.
- Code: `src/config/schema.base.generated.test.ts` covers the computed base config schema, and `src/config/channel-config-metadata.test.ts` plus `src/config/bundled-channel-config-metadata.generated.ts` cover the generated bundled channel metadata.
- Code: `src/config/env-substitution.test.ts` covers the FR-3 substitution grammar, and `src/config/env-preserve.test.ts` covers environment preservation across reload.
- Code: `src/config/io.write-journal.test.ts`, `src/config/config-journal-snapshot.test.ts`, and `src/config/io.snapshot.test.ts` cover the write journal and snapshot layers.
- Code: `src/config/includes.top-level-key.test.ts` and `src/config/include-write-boundary.test.ts` cover include resolution and the include write boundary.
- Code: `src/config/deferred-plugin-migration-config.ts` and `src/config/io.deferred-plugin-migrations.test.ts` cover the deferred plugin migration path that Doctor drives.
- Code: `src/config/future-version-guard.test.ts` covers the forward-compatibility guard, and `src/config/config.schema-regressions.test.ts` covers schema regression snapshots.
- Code: `scripts/check-env-var-count.mts` and `config/env-var-count-budget.txt` implement the `pnpm check:env-var-count` ratchet over `OPENCLAW_*` names in `src`, `packages`, and `extensions`; no test file in the plan covers it.
- Impact: the plan covers the original load, validate, patch, and substitute surface but not the snapshot, journal, secrets, Doctor, or schema-generation surfaces the system now owns.
- Classification: advisory.
