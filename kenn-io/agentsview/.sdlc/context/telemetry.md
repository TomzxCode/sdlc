# Telemetry

## Analytics platform

| Property | Value |
|---|---|
| Platform | PostHog |
| SDK | go.kenn.io/kit/telemetry PostHogReporter (server-side, wrapped by internal/telemetry) |
| Integration | Server-side only, emitted by the daemon process |
| API key location | Embedded constant postHogAPIKey in internal/telemetry/telemetry.go |

## Event naming conventions

- Event names use snake_case.
- Only explicitly allowlisted events may be sent.
- The allowlist is enforced in code via kittelemetry.WithAllowedEvent.
- Any non-allowlisted event is rejected through EventAllowed and SanitizeProperties.
- No per-feature event naming scheme exists beyond the single current event.

## Existing event taxonomy

| Event | Trigger | Key properties |
|---|---|---|
| daemon_active | Server startup and every 24 hours while the daemon runs | application=agentsview, version, commit, OS, CPU architecture, source=daemon, installation ID as DistinctId |

- The ping runs in the background and never blocks startup or operation.
- Person-profile processing is disabled with $process_person_profile=false.
- GeoIP lookup is disabled with $geoip_disable=true.

## Identity resolution

- Identity is a stable random 32-hex installation ID.
- The ID is stored in the telemetry-install-id file inside the data directory.
- A fresh data directory mints a new ID while copying the directory preserves it.
- PostHog consumes the same ID as the event DistinctId.
- The ID also attributes local sessions to the machine independently of telemetry.
- Disabling telemetry does not delete or rotate the installation ID.

## Privacy and compliance

- Telemetry is anonymous and contains no session data, prompts, project names, file paths, account information, hostnames, or machine identity.
- Set AGENTSVIEW_TELEMETRY_ENABLED=0 to disable outbound telemetry.
- The generic TELEMETRY_ENABLED=0 fallback is also honored via the kit helper.
- Telemetry is hard-disabled inside Go test binaries regardless of environment variables.
- The installation identity file remains in use for local attribution after opt-out.

## Funnels and key metrics

| Funnel | Steps | Defined in |
|---|---|---|
| None defined | No funnels exist, only the daemon_active liveness ping | N/A |
