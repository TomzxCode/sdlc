<!-- session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA -->
# Telemetry

<!--
This file captures the project's product analytics infrastructure: the analytics platform,
event conventions, existing event taxonomy, and privacy constraints. It gives create-telemetry
the context it needs to define new events consistently with the existing taxonomy.
System health monitoring (metrics, logs, traces) lives in observability.md.
Update this file when the analytics platform or event conventions change.
-->

## Analytics Platform

| Property | Value |
|---|---|
| Platform | First-party daily update check plus opt-in anonymous feature statistics, served by the public `openclaw/telemetry` worker at `telemetry.openclaw.ai` |
| SDK | None (plain HTTPS `GET`/`POST` from `src/infra/telemetry.ts`, no third-party analytics SDK in manifests) |
| Integration | Server-side (Gateway) and CLI (`openclaw telemetry show\|on\|off` in `src/cli/telemetry-cli.ts`) |
| API key location | No key; override endpoint via `OPENCLAW_TELEMETRY_ENDPOINT` env var |
| Local persistence | The accepted update result is cached in the shared state database under the `telemetry.updateCheck` config-machine-state key, and the session count is read from the local `session_state_events` table (src/infra/telemetry-store.kernel.ts, src/infra/telemetry-store.worker.ts, src/infra/telemetry-worker-contract.ts) |
| Secondary service | ClawHub install reporting is a separate path (src/infra/clawhub-telemetry.ts) that posts operator-initiated install events to the ClawHub API with a ClawHub token, and is disabled by `CLAWHUB_DISABLE_TELEMETRY` or `CLAWDHUB_DISABLE_TELEMETRY` |

## Event Naming Conventions

- There is a fixed two-tier request model, not an open event stream: an update-only `GET /api/latest-version` and, when opted in, a statistics `POST` with a versioned JSON body (`schema: 1`).
- Payload fields use camelCase (`providerFamilies`, `pluginsEnabled`, `sessionsLast24h`); the request surface is the literal `gateway` or `cli`.
- The CLI preview in `openclaw telemetry show` reports the `gateway` surface, and the preview is a local build of the payload rather than a retrieved one.
- No per-action or per-invocation events exist: the system never records plugin invocations, messages, model requests, or active users.
- The ClawHub install report uses a different convention: its own authenticated endpoint, an `event` discriminator of `install` or `plugin_install`, and no `schema` version.

## Existing Event Taxonomy

| Event | Trigger | Key properties |
|---|---|---|
| Daily update check (`GET /api/latest-version`) | Gateway startup (cached 24h, rechecked during maintenance with jitter) unless disabled | `User-Agent` only: OpenClaw version, OS, Node version, CPU arch, surface; no body, no identifiers |
| Anonymous feature statistics (`POST`, opt-in) | Same daily check when `telemetry.enabled: true` and `DO_NOT_TRACK` unset and not in CI | `schema`, `version`, `platform`, `node`, `surface`, `features.channels`, `features.providerFamilies`, `features.plugins`, `features.pluginsEnabled`, `features.sessionsLast24h` |
| ClawHub install report (`POST /api/cli/telemetry/install`) | Operator installs a ClawHub skill or plugin | `event` (`install` or `plugin_install`), skill `slug`, optional `ownerHandle`, `reference`, `trustState`, and `version`, or plugin `packageName` and `version`; sent only with a ClawHub token |

- Full field semantics live in `docs/gateway/telemetry.md`.
- Named channels, providers, and plugins are filtered to public/bundled/catalogued identities; private plugin identities are never named.
- Public aggregates are published at `telemetry.openclaw.ai`.
- `features.sessionsLast24h` counts local session-creation events in the preceding 24 hours, not active sessions, messages, or all sessions that existed.
- The ClawHub install report belongs to a different service with its own auth and opt-out, so it is not part of the daily update check.

## Identity Resolution

- No user, account, install, device, or machine identifier is created or sent (no UUID, no tracking id).
- The local cache in the shared state database holds only the accepted latest version, an optional operator-facing note, and the timestamp of the last successful check, so the worker-backed store introduces no identifier either.
- Repeated reports cannot be linked into per-install history; they are not counts of unique installations or users.
- Approximate geography (country, region, city, timezone) is derived server-side by Cloudflare and retained 3 months; no raw IPs or coordinates are stored in analytics.

## Privacy and Compliance

- Anonymous feature statistics are off by default; interactive setup offers opt-in with "No thanks" preselected, and non-interactive installs never opt in automatically.
- `DO_NOT_TRACK=1` or `DO_NOT_TRACK=true` forces statistics off even when `telemetry.enabled` is true (the update-only `GET` still sends).
- `update.checkOnStart: false`, `OPENCLAW_NO_AUTO_UPDATE=1`, or `OPENCLAW_NIX_MODE=1` disables every automatic request; explicit `openclaw telemetry` and update commands still work.
- CI environments (`CI` truthy) send nothing unless `OPENCLAW_TELEMETRY_ENDPOINT` is set.
- ClawHub install reporting is disabled separately by `CLAWHUB_DISABLE_TELEMETRY` or `CLAWDHUB_DISABLE_TELEMETRY`.
- Never collected: message content, prompts, model names, API keys, credentials, secret references, file paths, hostnames, or account/user identifiers.

## Funnels and Key Metrics

| Funnel | Steps | Defined in |
|---|---|---|
| None defined | No funnels exist; only daily version/platform counts and opt-in feature aggregates | `https://telemetry.openclaw.ai` (public aggregates) |

- The maturity scorecard tracks this surface as the Telemetry Export category of the observability domain (qa/maturity-scores.yaml, taxonomy.yaml). The domain is rated beta (M3) and the category is scored Beta for quality and completeness with LTS support marked unsupported; it scores feature completeness, not funnel performance.
