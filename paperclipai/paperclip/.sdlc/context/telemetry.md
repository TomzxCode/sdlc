# Telemetry

## Analytics Platform

| Property | Value |
|---|---|
| Platform | Paperclip first-party telemetry ingest, enabled by default and opt-out, with PostHog delivery added on Paperclip Cloud |
| SDK | `TelemetryClient` in `packages/shared/src/telemetry/client.ts` with typed helpers in `packages/shared/src/telemetry/events.ts`, plus `posthog-node` 5.38.2 pinned in `server/package.json:118` and `posthog-js` loaded as a script in the browser |
| Integration | Server-side (`server/src/telemetry.ts:12-26`) and CLI-side (`cli/src/telemetry.ts:19-48`), plus the Cloud direct path (`server/src/services/posthog-direct/index.ts`) and Cloud browser path (`server/src/routes/posthog-proxy.ts`) |
| API key location | No API key for first-party ingest; per-install `installId` identifies the sender and `PAPERCLIP_TELEMETRY_ENDPOINT` overrides the ingest URL; Cloud PostHog uses `PAPERCLIP_POSTHOG_PROJECT_TOKEN` |

- Default ingest endpoints are `https://telemetry.paperclip.ing/ingest` with an AWS execute-api fallback (`packages/shared/src/telemetry/client.ts:14-17`).
- The client batches up to 50 events or 512 KiB per POST, flushes every 60 seconds, and retries transient failures with capped jittered backoff.
- `resolveCloudPostHogConfig` returns `null` on self-hosted installs and gates direct delivery and browser analytics on Cloud-managed config with a project token and stack id (`server/src/services/cloud-posthog-config.ts:25-43`).
- Direct delivery also requires `PAPERCLIP_POSTHOG_DIRECT` to be enabled and an explicit environment, otherwise the process keeps using the collector (`server/src/services/cloud-posthog-config.ts:45-53`, `server/src/telemetry.ts:31-62`).
- Browser analytics runs only when `PAPERCLIP_POSTHOG_BROWSER_ENABLED=1`, and the board sends events to the same-origin `/_ph` proxy (`server/src/services/cloud-posthog-browser.ts:54-77`, `server/src/routes/posthog-proxy.ts:1-15`).
- Browser PostHog is not an npm dependency of the UI, and `posthog-js` loads as `/static/array.js` through the proxy (`ui/src/lib/analytics/product-analytics.ts:1-23`).
- No Segment, Amplitude, Mixpanel or Google Analytics SDK exists in the repo, and those names appear only in app catalog data.

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
| `agent.created` | Agent creation routes (`server/src/routes/agents.ts:4479,4662`) | `agent_role`, `agent_id` |
| `agent.first_heartbeat` | First agent heartbeat (`server/src/services/heartbeat.ts:1591-1598`) | `agent_role`, `agent_id` |
| `agent.task_completed` | Issue-side task completion (`server/src/routes/issues.ts:15091-15098`) | `agent_role`, `agent_id`, `adapter_type`, `model`, hashed `task_id` |
| `agent.task_run` | Terminal run transition via `emitAgentTaskRun`, emitted once per run (`server/src/services/agent-task-run-telemetry.ts:55-125`) | `agent_id`, `state`, `adapter_type`, `agent_role`, `model`, duration and token counts, hashed `task_id` |
| `artifact.created` | Artifact creation after commit (`server/src/services/product-telemetry.ts:186-205`) | `artifact_type`, `provider`, `creation_flow` |
| `company.imported` | CLI company import (`cli/src/commands/client/company.ts:1869`) | `source_type`, `source_ref` (salted-hashed when private), `source_ref_hashed` |
| `connection.app_linked` | Aggregator app newly connected in a committed sync (`server/src/services/connector-telemetry.ts:349-373`) | `provider`, `app` |
| `connection.app_requested` | Person or agent asks an aggregator to add an app (`server/src/services/connector-telemetry.ts:375-404`) | `provider`, `app`, `origin`, `outcome` |
| `connection.created` | Tool-purpose connection row committed (`server/src/services/connector-telemetry.ts:166-194`) | `connector_key`, `transport`, `auth_kind`, `setup_flow`, `status`, `enabled`, `server_domain` for custom connectors |
| `connection.invoked` | Tool invocation reaches a terminal status (`server/src/services/connector-telemetry.ts:236-312`) | `connector_key`, `transport`, `status`, `origin`, `duration_seconds`, `server_domain` for custom connectors |
| `connection.updated` | Tool-purpose connection `status` or `enabled` changes (`server/src/services/connector-telemetry.ts:196-234`) | `connector_key`, `transport`, `auth_kind`, `change_source`, `previous_status`, `status`, `previous_enabled`, `enabled`, `server_domain` for custom connectors |
| `error.handler_crash` | HTTP error-handler crash (`server/src/middleware/error-handler.ts:92`) | `error_code` |
| `goal.created` | Goal creation route (`server/src/routes/goals.ts:43-45`) | `goal_level` |
| `install.completed` | CLI onboarding finishes (`cli/src/commands/onboard.ts:730`) | `adapter_type` |
| `install.started` | CLI onboarding flow begins (`cli/src/commands/onboard.ts:553`) | none |
| `interaction.created` | Issue-thread interaction creation (`server/src/services/issue-thread-interactions.ts:1417`) | `interaction_kind`, `used_deprecated_resolver_policy_alias` |
| `interaction.resolved` | Issue-thread interaction resolution (`server/src/services/issue-thread-interactions.ts:1385`) | `interaction_kind`, `status`, `resolved_by_kind`, outcome counts, `legacy_inherited_restriction` |
| `model.connected` | Model connection setup after commit (`server/src/services/product-telemetry.ts:207-224`) | `provider`, `connection_method`, `ownership`, `routing_kind`, `first_for_company` |
| `plan.approved` | Plan approval after commit (`server/src/services/product-telemetry.ts:164-178`) | `approved_by_kind`, `starts_execution` |
| `plan.created` | Plan creation after commit (`server/src/services/product-telemetry.ts:147-162`) | `created_by_kind`, `at_task_creation` |
| `project.created` | Project creation route (`server/src/routes/projects.ts:431-434`) | none |
| `routine.created` | Routine creation route (`server/src/routes/routines.ts:179-181`) | none |
| `routine.run` | Routine dispatch (`server/src/services/routines.ts:2049-2055`) | `source`, `status` |
| `server.started` | Telemetry client initialization at server start (`server/src/telemetry.ts:64-90`) | `os_platform` |
| `skill.imported` | Skill import route (`server/src/routes/company-skills.ts:1367-1375`) | `source_type`, `skill_ref` |
| `task.blocked` | Task status transition to blocked (`server/src/services/product-telemetry.ts:82-115`) | `blocked_reason`, `blocked_by_kind` |
| `task.completed` | Task status transition to done (`server/src/services/product-telemetry.ts:82-105`) | `completed_by_kind`, `is_subtask` |
| `task.created` | Issue creation after commit (`server/src/services/product-telemetry.ts:48-66`) | `created_by_kind`, `is_subtask` |

- The generated contract at `packages/shared/src/telemetry/generated/paperclip-telemetry.ts` is the authority for names, dimensions, optionality, and enum domains.
- The generated contract defines these 28 events in `PAPERCLIP_EVENTS` and `EventDimensionsMap` (`packages/shared/src/telemetry/generated/paperclip-telemetry.ts:219-279`).
- The event catalog is intentionally not copied into `packages/shared/src/telemetry/README.md` because copies drift as the contract changes.

## Identity Resolution

- First-party identity is per installation, not per user.
- First use creates `state.json` under the instance telemetry directory with a random `installId` UUID, a random salt, creation time, and first-seen version (`packages/shared/src/telemetry/state.ts:6-31`).
- Every envelope carries the `installId` and client version with a deterministic content-hash `batchId` for idempotent retry.
- First-party private references such as task ids and private source refs are salted-hashed with `hashPrivateRef` before emission, so raw values never leave the process.
- There is no anonymous-to-authenticated identity merge and no user identity in telemetry state.
- Cloud PostHog identifies the signed-in user, and the browser uses the authenticated user id as `distinct_id` so browser and server events land on the same PostHog person (`ui/src/components/ProductAnalyticsGate.tsx:35-41`).
- Cloud direct events use the acting user id as `distinct_id` when known, otherwise `workspace:<stackId>`, and carry `stack_id`, `company_id`, `user_id`, `environment`, the `workspace` group and session ids (`server/src/services/posthog-direct/event-shape.ts:140-192`).
- The direct path intentionally carries unhashed user, agent, company, stack and private-ref identifiers, unlike the first-party collector path (`server/src/services/posthog-direct/event-shape.ts:12-21`).

## Privacy and Compliance

- First-party telemetry is enabled by default and is opt-out, not opt-in.
- It is disabled by `PAPERCLIP_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`, any detected CI environment, or `telemetry.enabled: false` in config (`packages/shared/src/telemetry/config.ts:67-86`).
- First-party emitters must not send PII, secrets, credentials, private paths, prompts, or model output through dimensions.
- Cloud direct delivery intentionally sends unhashed user, agent, company, stack and private-ref identifiers to PostHog (`server/src/services/posthog-direct/event-shape.ts:12-21`).
- Credential-bearing chat setup failures are replaced with a generic error before the crash-report path.
- Contract-first rule: the generated contract is updated before normal emitters use new events.
- Every telemetry change updates `packages/shared/src/telemetry/README.md` in the same pull request and requests a privacy review.
- Browser analytics asks for consent where required, with timezone rules and a `PAPERCLIP_POSTHOG_COUNTRY_HEADER` override (`ui/src/lib/analytics/consent.ts:17-26`, `server/src/services/cloud-posthog-browser.ts:23-28`).
- Browser analytics is denied when Global Privacy Control or Do Not Track is set and consent is required (`ui/src/lib/analytics/consent.ts:22-25,58-67`).
- Choices are stored in `localStorage` under `paperclip.analyticsConsent`, and declining stops capture and session recording (`ui/src/lib/analytics/consent.ts:28-52`, `ui/src/lib/analytics/product-analytics.ts:264-276,366-376`).
- Retention note: `EVENT_RETENTION_CLASS` maps 13 events to the 90-day `operational_enum_count` class (`packages/shared/src/telemetry/retention.ts:46-59`).
- The first-party entries are `interaction.created`, `interaction.resolved`, `server.started`, `model.connected`, `task.created`, `task.completed`, `task.blocked`, `plan.created`, `plan.approved`, `artifact.created`, `connection.app_linked` and `connection.app_requested`, and the remaining entry is the external `codex.credential_health` event.

## Funnels and Key Metrics

| Funnel | Steps | Defined in |
|---|---|---|
| None defined in repo | Not configured | Not configured |

- No funnel or key-metric definitions were found in the telemetry package.
- Status: Not configured.
