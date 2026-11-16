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
| Platform | First-party daily update check, identifier-free installation counting, update-outcome reporting, and opt-in anonymous feature statistics, served by the public `openclaw/telemetry` worker at `telemetry.openclaw.ai` |
| SDK | None (plain HTTPS `GET`/`POST`/`HEAD` from `src/infra/telemetry.ts`, `src/infra/telemetry-installation-count.ts`, and `src/infra/update-result-telemetry.ts`, no third-party analytics SDK in manifests) |
| Integration | Server-side (Gateway) and CLI (`openclaw telemetry show\|on\|off` in `src/cli/telemetry-cli.ts`) |
| API key location | No key; override the complete endpoint URL via `OPENCLAW_TELEMETRY_ENDPOINT` env var |
| Local persistence | The accepted update result is cached in the shared state database under the `telemetry.updateCheck` config-machine-state key, the last claimed receiver day for counting is stored under an endpoint-hashed `telemetry.installationCount.*` key, the update-outcome claim is stored in a bounded machine-state record, and the session count is read from the local `session_state_events` table (src/infra/telemetry-store.worker.ts, src/infra/telemetry-installation-count.ts, src/infra/telemetry-worker-contract.ts) |
| Secondary service | ClawHub install reporting is a separate path (src/infra/clawhub-telemetry.ts) that posts operator-initiated install events to the ClawHub API with a ClawHub token, and is disabled by `CLAWHUB_DISABLE_TELEMETRY` or `CLAWDHUB_DISABLE_TELEMETRY` |

## Event Naming Conventions

- There is a fixed set of narrow requests, not an open event stream: an update-only `GET /api/latest-version`, an optional statistics `POST` with a versioned JSON body (`schema: 1`), an optional payload-free counting `POST`, and an optional update-outcome `POST` with a versioned JSON body (`schema: 2`).
- Payload fields use camelCase (`providerFamilies`, `pluginsEnabled`, `sessionsLast24h`); the request surface is the literal `gateway` or `cli`.
- The CLI preview in `openclaw telemetry show` reports the `gateway` surface, and the preview is a local build of the payload rather than a retrieved one.
- No per-action or per-invocation events exist: the system never records plugin invocations, messages, model requests, or active users.
- The counting POST has no body and sends only the `OpenClaw-Installation-Count` header, with a fixed `User-Agent: openclaw-installation-count/1`; the receiver advertises its day via a response header on a successful update answer.
- The update-outcome POST uses a fixed `User-Agent: openclaw-update-result/1`, an `event` discriminator of `update_result`, and a `schema` of `2`; it is preceded by a payload-free capability `HEAD` that must return `204` with `OpenClaw-Update-Results: 2`.
- The ClawHub install report uses a different convention: its own authenticated endpoint, an `event` discriminator of `install` or `plugin_install`, and no `schema` version.

## Existing Event Taxonomy

| Event | Trigger | Key properties |
|---|---|---|
| Daily update check (`GET /api/latest-version`) | Gateway startup (cached 24h, rechecked during maintenance with jitter) unless disabled | `User-Agent` only: OpenClaw version, OS, Node version, CPU arch, surface; no body, no identifiers |
| Anonymous feature statistics (`POST`, opt-in) | Same daily check when `telemetry.enabled: true` and `DO_NOT_TRACK` unset and not in CI | `schema`, `version`, `platform`, `node`, `surface`, `features.channels`, `features.providerFamilies`, `features.plugins`, `features.pluginsEnabled`, `features.sessionsLast24h` |
| Identifier-free installation count (`POST`, no body) | Follows a successful uncached daily check when the receiver advertises an `OpenClaw-Installation-Count` response header with protocol version `1` and an authoritative UTC day | `OpenClaw-Installation-Count` header with protocol version, advertised receiver day, and days since the last locally claimed day capped at 31; fixed counting `User-Agent`; no version, platform, feature inventory, or identifier |
| Update-outcome report (`POST`, on by default) | A settled update run succeeds, fails, or rolls back, after a capability `HEAD` returns `204` with `OpenClaw-Update-Results: 2` | `schema: 2`, `event: update_result`, `outcome`, public `fromVersion`/`targetVersion`/`resultingVersion`/`runningVersion`, `platform`, `arch`, `installMethod`, `channel`, coarse `duration`, `postCheck`, `failedStage`, `errorCategory`, `errorCode`, `rollback`, `recovery` |
| ClawHub install report (`POST /api/cli/telemetry/install`) | Operator installs a ClawHub skill or plugin | `event` (`install` or `plugin_install`), skill `slug`, optional `ownerHandle`, `reference`, `trustState`, and `version`, or plugin `packageName` and `version`; sent only with a ClawHub token |

- Full field semantics live in `docs/gateway/telemetry.md`.
- Named channels, providers, and plugins are filtered to public/bundled/cataloged identities; private plugin identities are never named.
- Public aggregates are published at `telemetry.openclaw.ai`.
- `features.sessionsLast24h` counts local session-creation events in the preceding 24 hours, not active sessions, messages, or all sessions that existed.
- Counting is allowed before feature consent, and `telemetry.enabled: false`, a recorded decline, or `DO_NOT_TRACK` suppresses it without disabling the update-only GET.
- Counting is at most one POST per successful uncached daily check, never follows redirects, and is never retried for the same receiver day after a lost response or crash.
- Update-outcome reporting is on by default, is controlled by the automatic update-request policy rather than `telemetry.enabled`, and is suppressed in CI even with a custom endpoint.
- Update-outcome values are closed allowlists with unknown fallbacks; no prereleases, build metadata, refs, or Git SHAs are sent.
- The ClawHub install report belongs to a different service with its own auth and opt-out, so it is not part of the daily update check.

## Identity Resolution

- No user, account, install, device, or machine identifier is created or sent (no UUID, no tracking id).
- The local cache in the shared state database holds only the accepted latest version, an optional operator-facing note, and the timestamp of the last successful check, so the worker-backed store introduces no identifier either.
- The count header carries only an endpoint-hashed local state key that is identical for everyone using that endpoint and never leaves the host; the receiver keeps aggregate day totals, not per-install histories.
- Repeated reports cannot be linked into per-install history; they are not counts of unique installations or users.
- Approximate geography (country, region, city, timezone) is derived server-side by Cloudflare and retained 3 months; no raw IPs or coordinates are stored in analytics.

## Privacy and Compliance

- Anonymous feature statistics are off by default; interactive setup offers opt-in with "No thanks" preselected, and non-interactive installs never opt in automatically.
- Installation counting and update-outcome reporting are on by default and are not gated by `telemetry.enabled`.
- `DO_NOT_TRACK=1` or `DO_NOT_TRACK=true` forces statistics and installation counting off even when `telemetry.enabled` is true (the update-only `GET` and update outcomes still send).
- `telemetry.enabled: false` or a recorded decline also suppresses installation counting without disabling the update-only `GET`.
- `update.checkOnStart: false`, `OPENCLAW_NO_AUTO_UPDATE=1`, or `OPENCLAW_NIX_MODE=1` disables every automatic request including update outcomes; explicit `openclaw telemetry` and update commands still work.
- CI environments (`CI` truthy) send nothing; a custom `OPENCLAW_TELEMETRY_ENDPOINT` permits daily checks against a test receiver in CI but not update outcomes.
- ClawHub install reporting is disabled separately by `CLAWHUB_DISABLE_TELEMETRY` or `CLAWDHUB_DISABLE_TELEMETRY`.
- Never collected: message content, prompts, model names, API keys, credentials, secret references, file paths, hostnames, exact client timestamps, or account/user, install, device, and machine identifiers.

## Funnels and Key Metrics

| Funnel | Steps | Defined in |
|---|---|---|
| None defined | No funnels exist; only daily version/platform counts and opt-in feature aggregates | `https://telemetry.openclaw.ai` (public aggregates) |

- The maturity scorecard tracks this surface as the Telemetry Export category of the observability domain (qa/maturity-scores.yaml, taxonomy.yaml). The domain is rated beta (M3) and the category is scored Beta for quality and completeness with LTS support marked unsupported; it scores feature completeness, not funnel performance.
