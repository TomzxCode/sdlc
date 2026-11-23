<!-- session_link: full sync reconciliation, 2026-11-23 -->
# Telemetry

<!--
This file inventories the project's product analytics platform: the NeMo Relay shared-metrics
integration, its event conventions and taxonomy, identity model, privacy constraints, and funnels.
Operational monitoring (OTLP export, logging, tracing, alerting) lives in observability.md.
Update this file when the event contract, consent gate, identity model, or ingest path changes.
-->

## Platform

| Aspect | Detail |
|---|---|
| Product telemetry platform | NeMo Relay shared metrics, a first-party integration built into Hermes under `hermes_cli/observability/` (no observability plugin required) |
| Host runtime | `nemo-relay>=0.11,<0.12`, bounded subscriber `hermes.nemo_relay.shared_metrics` declared in `shared_metrics_contract.py`; unsupported native targets use an explicit no-op host |
| No third-party analytics SDK | No Amplitude, Mixpanel, PostHog, Google Analytics or Segment SDK is used in product code; `optional-mcps/amplitude` and `optional-mcps/mixpanel` are optional catalog entries and PostHog/SAM mentions are skill docs |
| Local store | `$HERMES_HOME/telemetry/shared_metrics/metrics.sqlite3` plus immutable delta packages under `outbox/*.json` |
| Ingest path | Hermes telemetry service at `https://telemetry.nousresearch.com/v1/telemetry` from `telemetry.shared_metrics.endpoint` config, deliberately not env-overridable; `202` means durably stored |
| Opt-in gate | Collection `telemetry.shared_metrics.enabled` and transmission `telemetry.shared_metrics.send`, both default false, both profile-owned, with send requiring enabled |
| Consent offer | Asked once per profile on `hermes setup`, interactive CLI/TUI, Desktop and dashboard; "Share with Nous" sets both true, "No thanks" sets both false, and managed installs are never offered |

Collection alone transmits nothing.
The sender runs only when `send` is also true and re-reads consent before every package.
Both keys are per-profile and cannot be set by a machine-managed configuration overlay.

## Event Conventions

| Convention | Detail |
|---|---|
| Producer chain | Turn, API, tool and approval hooks emit Relay scopes and marks; the bounded subscriber writes SQLite counters; counters become immutable JSON delta packages; the opt-in sender posts whole packages, never live spans |
| Contract | `hermes_cli/observability/shared_metrics_contract.py` is the authoritative allowlist for names, dimensions and enums; event schema `hermes.metrics.event.v4`, package schema v4 |
| Schema evolution | Additive-only changes keep older field sets valid; values a stable release shipped stay accepted as legacy so counters recorded before an upgrade still drain |
| Dimensions | Every dimension is a closed enum, a bucket, a shipped public name, or a bounded provider/model identifier from the model-route rules |
| Period and gating | One UTC day per period; a package is sent only when its whole period falls inside a recorded `send_consent_windows` interval, so the gate fails closed and never undercounts a split period |
| Retention | Exported packages and rows are kept locally 30 days, pending deltas are never pruned, and remote raw packages have no expiry in production but 30 days in staging |

Package resource fields carry only Hermes version, OS family, architecture and install method, with unrecognized values exported as `unknown`.
`hermes.client.active` and `hermes.install.snapshot` use a transactional 24-hour compare-and-set latch so each counts at most once per install per day.
Full definitions live in `website/docs/developer-guide/relay-shared-metrics.md`.

## Event Taxonomy

| Family | Representative metrics |
|---|---|
| Sessions and tasks | `hermes.session.count`, `hermes.client.active`, `hermes.task_run.started` / `finished` / `duration`, `hermes.task_cost.count`, `hermes.install.snapshot` |
| Models and cost | `hermes.model_route.count`, `hermes.model_tokens.sum`, `hermes.model_switch.count`, `hermes.fallback.count`, `hermes.model_tool_quality.count`, `hermes.model_friction.count`, `hermes.context_peak.count` |
| Tools and extensions | `hermes.tool_call.count` / `latency`, `hermes.tool.usage.count`, `hermes.tool_approval.count`, `hermes.tool_search.count`, `hermes.tool_batch.count`, `hermes.connector_chain.count`, `hermes.execution_backend.count`, `hermes.slash_command.count`, `hermes.extension.install.count` |
| Reliability | `hermes.process.exit`, `hermes.startup.latency`, `hermes.update.run` / `stage`, `hermes.compression.count`, `hermes.prepared_compaction.count`, `hermes.cron.run`, `hermes.platform.health` / `delivery`, `hermes.gateway.reply_latency`, `hermes.gateway.busy_arrival.count` |
| Agent harness and efficiency | `hermes.memory.op.count`, `hermes.curator.run.count`, `hermes.delegation.run.count`, `hermes.skill.lifecycle` / `load`, `hermes.file_edit.count`, `hermes.loop_guard.count`, `hermes.tool_recovery.count`, `hermes.terminal.outcome.count`, `hermes.model_reply_issue.count`, `hermes.cache_break.count`, `hermes.wasted_tokens.count`, `hermes.tool_overhead.count`, `hermes.tool_enabled_unused.count` |
| Engagement | `hermes.engagement.day.count`, `hermes.engagement.surface_day.count`, `hermes.model_switch_after.count` |
| Onboarding and signals | `hermes.setup.completed`, `hermes.provider_setup.count`, `hermes.feature_adoption.count`, `hermes.feature_disabled.count`, `hermes.tool_unavailable.count`, `hermes.install.milestone`, `hermes.install.run` |
| Desktop | `hermes.desktop.feature_use`, `action_use`, `mode_use`, `friction`, `long_frames.sum`, `dislike`, `onboarding` |

## Identity Resolution

| Aspect | Detail |
|---|---|
| `install_id` | Random UUID4 generated locally, persistent per `HERMES_HOME`, identifying a profile rather than a person and never derived from hardware, account, host, path or credential data |
| Transmission | Sent verbatim since the 2026-08-27 product decision; the earlier HMAC rotating-pseudonym design was removed before any consented user shipped |
| Linkability | Stable across packages and windows by design, so retention curves and longitudinal behaviour are computable; `sent_install_id` freezes the value used for byte-identical resends |
| Reset | Stopping Hermes and removing `$HERMES_HOME/telemetry/shared_metrics` regenerates the identity and clears aggregates and packages, but cannot unsend data already transmitted |
| Deletion | No remote delete API exists in the v1 ingest contract; `send: false` stops future transmission and closing the consent window excludes uncovered periods |

In multiplexed processes, each runtime's exit flush, export and send pass binds that runtime's own profile and its own consent state.
`send: false` stops transmission after the package currently in flight and does not stop local collection.

## Privacy Constraints

- Prompts, responses, commands, error text, tool arguments and results, session/task/request IDs, paths, hostnames, URLs and host names never enter events or packages.
- Provider and model identifiers pass only for shipped or public models; custom endpoints, local-server aliases and URL, path, IP or ARN model ids read `custom`.
- Tool names are exported only for built-ins and the Tool Search bridge; MCP tools read `mcp`, connector tools read `connector` without the slug, and plugin or custom tools read `plugin`.
- Skill names are exported only for skills Hermes ships, otherwise `custom`; memory text, old_text and error messages never enter `hermes.memory.op.count`.
- Local subscriber re-runs the model-route rules on every mark and drops rows it would rewrite to `custom` for an unapproved identifier.
- Fixed enum vocabularies are pattern-bounded in the JSON schema, with `shared_metrics_contract.py` as the authoritative allowlist.
- Agent monitoring egress uses `redact_for_egress` and never navigates a URL for telemetry.

## Funnels

| Funnel | Metrics |
|---|---|
| Install to first value | `hermes.install.run` records installer outcome and failure stage; `hermes.install.milestone` latches first success, gateway message, cron run, delegation, created skill and long session once per install |
| Consent and setup | `hermes.setup.completed` records surface and provider; `hermes.provider_setup.count` tracks started, completed, failed and abandoned flows per surface with a closed failure class |
| Adoption | `hermes.feature_adoption.count` reports days since install for each major feature's first real use; `hermes.feature_disabled.count` tracks what users turn off |
| Desktop first run | `hermes.desktop.onboarding` records step reached, completed and abandoned, with first-run events held in memory only until consent is answered |
| Retention and model switching | `hermes.engagement.day.count` for active days and next-day or next-week return, `hermes.model_switch_after.count` for turns before leaving a model |
| Friction | `hermes.model_friction.count`, `hermes.desktop.friction`, `hermes.desktop.dislike`, `hermes.wasted_tokens.count`, and the `retry` / `undo` slash-command signals |
