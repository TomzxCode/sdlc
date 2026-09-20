# Telemetry

## Analytics Platform

| Property | Value |
|---|---|
| Platform | Paperclip first-party telemetry ingest, enabled by default and opt-out |
| SDK | `TelemetryClient` in `packages/shared/src/telemetry/client.ts` with typed helpers in `packages/shared/src/telemetry/events.ts` |
| Integration | Server-side (`server/src/telemetry.ts:12-26`) and CLI-side (`cli/src/telemetry.ts:19-48`) |
| API key location | No API key; per-install `installId` identifies the sender and `PAPERCLIP_TELEMETRY_ENDPOINT` overrides the ingest URL |

- Default ingest endpoints are `https://telemetry.paperclip.ing/ingest` with an AWS execute-api fallback (`packages/shared/src/telemetry/client.ts:14-17`).
- The client batches up to 50 events or 512 KiB per POST, flushes every 60 seconds, and retries transient failures with capped jittered backoff.

## Event Naming Conventions

- Event names use dotted snake_case entity-dot-action form such as `agent.created` and `interaction.resolved`.
- Dimension keys use snake_case such as `adapter_type` and `source_ref`.
- Dimension values must be `string`, `number`, or `boolean` primitives, and optional dimensions are omitted when absent.
- Emitters send raw observed values without lowercasing, alias mapping, or fallback mapping.
- The receiving layer owns canonicalization of legacy spellings, aliases, and future values.
- Sentinel values such as `other` or `unknown` cover required fields with no observed value and must not hide a concrete new value.
- New stable events must exist in the generated contract before normal client code emits them.
- Proposed events ahead of schema registration use `client.track()` with an `@ts-expect-error` proposal marker and are swallowed at runtime until registered (`doc/TELEMETRY_WORKFLOW.md:7-9`).

## Existing Event Taxonomy

| Event | Trigger | Key properties |
|---|---|---|
| `install.started` | CLI onboarding flow begins (`cli/src/commands/onboard.ts:553`) | none |
| `install.completed` | CLI onboarding finishes (`cli/src/commands/onboard.ts:730`) | `adapter_type` |
| `company.imported` | CLI company import (`cli/src/commands/client/company.ts:1869`) | `source_type`, `source_ref` (salted-hashed when private), `source_ref_hashed` |
| `project.created` | Project creation route (`server/src/routes/projects.ts:317-319`) | none |
| `routine.created` | Routine creation route (`server/src/routes/routines.ts:179-181`) | none |
| `routine.run` | Routine dispatch (`server/src/services/routines.ts:2039`) | `source`, `status` |
| `goal.created` | Goal creation route (`server/src/routes/goals.ts:43-45`) | `goal_level` |
| `agent.created` | Agent creation routes (`server/src/routes/agents.ts:4689-4691`) | `agent_role`, `agent_id` |
| `skill.imported` | Skill import route (`server/src/routes/company-skills.ts:1192-1195`) | `source_type`, `skill_ref` |
| `agent.first_heartbeat` | First agent heartbeat (`server/src/services/heartbeat.ts:17864`) | `agent_role`, `agent_id` |
| `agent.task_completed` | Issue-side task completion (`server/src/routes/issues.ts:14214-14222`) | `agent_role`, `agent_id`, `adapter_type`, `model`, hashed `task_id` |
| `agent.task_run` | Terminal run transition via `emitAgentTaskRun`, emitted once per run (`server/src/services/agent-task-run-telemetry.ts:55-125`) | `agent_id`, `state`, `adapter_type`, `agent_role`, `model`, duration and token counts, hashed `task_id` |
| `error.handler_crash` | HTTP error-handler crash (`server/src/middleware/error-handler.ts:89-90`) | `error_code` |
| `interaction.created` | Issue-thread interaction creation (`server/src/services/issue-thread-interactions.ts:1402`) | `interaction_kind`, `used_deprecated_resolver_policy_alias` |
| `interaction.resolved` | Issue-thread interaction resolution (`server/src/services/issue-thread-interactions.ts:1370`) | `interaction_kind`, `status`, `resolved_by_kind`, outcome counts, `legacy_inherited_restriction` |

- The generated contract at `packages/shared/src/telemetry/generated/paperclip-telemetry.ts` is the authority for names, dimensions, optionality, and enum domains.
- The event catalog is intentionally not copied into `packages/shared/src/telemetry/README.md` because copies drift as the contract changes.

## Identity Resolution

- Identity is per installation, not per user.
- First use creates `state.json` under the instance telemetry directory with a random `installId` UUID, a random salt, creation time, and first-seen version (`packages/shared/src/telemetry/state.ts:6-31`).
- Every envelope carries the `installId` and client version with a deterministic content-hash `batchId` for idempotent retry.
- Private references such as task ids and private source refs are salted-hashed with `hashPrivateRef` before emission, so raw values never leave the process.
- There is no anonymous-to-authenticated identity merge and no user identity in telemetry state.

## Privacy and Compliance

- Telemetry is enabled by default and is opt-out, not opt-in.
- It is disabled by `PAPERCLIP_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`, any detected CI environment, or `telemetry.enabled: false` in config (`packages/shared/src/telemetry/config.ts:66-86`).
- Emitters must not send PII, secrets, credentials, private paths, prompts, or model output through dimensions.
- Credential-bearing chat setup failures are replaced with a generic error before the crash-report path.
- Contract-first rule: the generated contract is updated before normal emitters use new events.
- Every telemetry change updates `packages/shared/src/telemetry/README.md` in the same pull request and requests a privacy review.
- Retention note: only `interaction.created`, `interaction.resolved`, and the external `codex.credential_health` event are assigned to the 90-day `operational_enum_count` class, and retention mapping for the remaining first-party events was not determined from the repo (`packages/shared/src/telemetry/retention.ts:46-50`).

## Funnels and Key Metrics

| Funnel | Steps | Defined in |
|---|---|---|
| None defined in repo | Not configured | Not configured |

- No funnel or key-metric definitions were found in the telemetry package.
- Status: Not configured.
