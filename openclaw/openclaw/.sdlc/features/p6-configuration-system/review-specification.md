---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Configuration System specification

## Sync drift: 2026-10-19

### Blocking: the top-level config data model lists 8 of 47 keys and names two of them wrong

- Artifact says (specification.md:30-41):

  | Field | Type | Description |
  |---|---|---|
  | agents | object | Agent-specific configuration |
  | channels | object | Channel plugin configuration |
  | models | object | Model provider configuration |
  | plugins | object | Plugin settings |
  | hooks | object | Hook scripts |
  | cron | object | Cron job definitions |
  | logs | object | Logging configuration |
  | sandbox | object | Tool sandbox policies |

- Code: `src/config/zod-schema.root-shape.ts:48` defines `export const OpenClawSchemaShape = {` with 47 top-level keys: `$schema`, `meta`, `env`, `wizard`, `diagnostics`, `logging`, `update`, `telemetry`, `browser`, `ui`, `secrets`, `auth`, `accessGroups`, `acp`, `models`, `nodeHost`, `agents`, `worktreeRoot`, `worktreeAcceleration`, `worktreeMaxCount`, `tools`, `security`, `bindings`, `broadcast`, `attachments`, `messages`, `tts`, `commands`, `approvals`, `session`, `cron`, `transcripts`, `hooks`, `channels`, `discovery`, `talk`, `gateway`, `cloudWorkers`, `database`, `storage`, `desktop`, `memory`, `mcp`, `skills`, `plugins`, `surfaces`, and `proxy`.
- Code: there is no top-level `logs` key; logging is `logging: LoggingConfigSchema` (`src/config/zod-schema.root-shape.ts:81`).
- Code: there is no top-level `sandbox` key; sandbox policy is expressed under `tools`, `security`, and per-agent settings, and the only `sandbox` string in the root shape is a Chrome flag help text at `src/config/zod-schema.root-shape.ts:114`.
- Impact: the table is the only description of the config shape, and 39 keys are missing while 2 listed keys do not exist, so a reader would mis-model the configuration file.
- Classification: blocking.

### Blocking: the overview says the schema "generates a JSON Schema for IDE support", but nothing is generated

- Artifact says (specification.md:10): "The schema is defined in TypeScript using zod and generates a JSON Schema for IDE support."
- Code: `scripts/generate-base-config-schema.ts:17-24` reports "runtime-computed; no generated file to write" and "no generated file to write" is the only outcome of both `--check` and `--write`.
- Code: `src/config/schema-base.ts:1-20` computes the JSON Schema at runtime through `computeBaseConfigSchemaResponse` from the zod schema, and `src/config/schema.base.generated.test.ts:18-22` asserts the computed shape.
- Code: the only committed `.schema.json` in the repo is `.github/crabbox/openclaw-performance-evidence.schema.json`, which is unrelated to config.
- Code: the JSON Schema reaches users through `openclaw config schema` (`src/cli/config-cli.ts:214`) and through the generated bundled-channel metadata at `src/config/bundled-channel-config-metadata.generated.ts`.
- Impact: a reader would look for a committed JSON Schema file to point an editor at, and would not know that the schema is served at runtime or that bundled channel config metadata is a generated artifact.
- Classification: blocking.

### Advisory: the config reload watcher lives under `src/gateway/`, not `src/config/`

- Artifact says (specification.md:48-52) that the config load flow is the whole story:

  ```
  Gateway Start → Config Loader: read openclaw.json
  Config Loader → File System: parse JSON
  Config Loader → Zod: validate against schema
  Config Loader → Runtime: if valid, apply config; if invalid, report errors
  ```

- Code: hot reload is implemented in `src/gateway/config-reload.ts` (with `config-reload-plan.ts`, `config-reload-status.types.ts`, `config-reload-recovery.ts`, and `config-reload.settings.ts`), not in `src/config/`.
- Code: `src/config/source-file.ts:34` provides the file watcher that feeds the reloader, and `src/gateway/config-reload.ts` owns the drain, apply, and rollback plan.
- Code: `src/config/io.invalid-config.ts` owns the invalid-config path, and `src/gateway/config-reload.invalid-config.test-support.ts:51` asserts "config reload skipped (invalid config)".
- Impact: the artifact's load flow is startup only, and a reader would not know where the reload path lives.
- Classification: advisory.

### Advisory: the "JSON does not support comments" risk is stale

- Artifact says (specification.md:68): "3. JSON format does not support comments, which can be a pain point for users".
- Code: `src/config/io.read-helpers.ts:143` parses config through `parseJsonWithJson5Fallback`, and `src/utils/parse-json-compat.ts:1-3` states "Strict JSON stays the fast path; JSON5 is only the authored/legacy fallback."
- Code: `src/config/includes.ts:1-10` documents `$include` with `.json5` examples.
- Impact: authored config files do accept comments, so the risk no longer applies.
- Classification: advisory.

### Advisory: the merge strategy is not a single custom merge-patch

- Artifact says (specification.md:60): "| Merge strategy | Custom merge-patch | Partial updates without overwriting unrelated keys |" and (specification.md:21) lists "Merge-Patch" as a config loader stage.
- Code: `src/config/merge-patch.ts` provides the merge-patch update used for config writes.
- Code: `src/config/includes.ts:19` uses a separate deep merge (`mergeDeep` from `src/infra/deep-merge.js`, applied at `src/config/includes.ts:208`) to combine included documents, and `src/config/includes-scan.ts` scans include roots.
- Code: `src/config/runtime-write-application.ts` and `src/config/config-journal-snapshot.ts` add a write-journal and snapshot layer on top of the patch.
- Impact: the spec presents one merge stage where the code has at least patch, deep merge, and journal/snapshot.
- Classification: advisory.
