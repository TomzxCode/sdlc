---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Requirements review: Gateway Server

## Sync drift: 2026-10-19

The requirements were reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: the Node.js runtime constraint is contradicted by the package manifest

- Classification: blocking.
- Artifact says (line 46): "- Must run on Node.js 22.19+ (Node 24 recommended)"
- Code says: `package.json:2474-2476` sets `"engines": { "node": ">=24.16.0 <25 || >=26.1.0" }`.
- Code says: Node 22 is not in the supported range, and Node 26 is now supported.
- Impact: a reader would believe Node 22 is a supported deployment target, and the package manager refuses to install on it.

### Blocking: FR-2 names only three of the eight supported authentication methods

- Classification: blocking.
- Artifact says (line 25): "| FR-2 | Must | The gateway shall authenticate requests using bearer tokens, device pairing, or pre-auth tokens |"
- Code says: `src/gateway/auth.ts:38-46` reports the resolved method as one of `none`, `token`, `password`, `tailscale`, `device-token`, `bootstrap-token`, `trusted-proxy`, or `remote-ingress`.
- Code says: `src/gateway/auth-mode-policy.ts:1-30` makes `gateway.auth.mode` a required disambiguator when both a token and a password are configured.
- Code says: `src/gateway/auth.ts:44-45` attaches a verified Tailscale identity, and `src/gateway/ingress-attribution.ts` provides the remote-ingress attribution path.
- Impact: a reader would not plan for password mode, Tailscale identity, or identity-aware reverse proxy deployment, which are the three most common production configurations.

### Blocking: no requirement covers the pluggable database storage engine

- Classification: blocking.
- Artifact says (lines 22-33): the functional requirement table covers HTTP and WebSocket serving, auth, session management, config hot-reload, health, graceful shutdown, rate limiting, node pairing, broadcast, and plugin HTTP endpoints. No requirement mentions storage engines.
- Artifact says (line 45): "- Single-user architecture: no multi-tenant isolation required"
- Code says: `package.json:6` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`.
- Code says: `package.json:11` sets `openclaw.postgresFamilies` to `["state", "agent", "workboard", "logbook", "team-reports"]`.
- Code says: `src/infra/database-engine/registry.ts:24-33` marks five families as PostgreSQL-capable, and `src/infra/database-engine/registry.ts:39-56` resolves a per-family engine override.
- Code says: `docs/reference/database-engines.md` and `docs/gateway/postgresql.md` document the operator-facing behavior, including mixed-engine limits.
- Impact: NFR-1 says the gateway "shall recover from crashes with minimal session data loss", but the artifact never states that the session store can live outside a local SQLite file, so a reader would size backup and migration plans incorrectly.

### Advisory: FR-5 describes one health endpoint where the code exposes three probe classes

- Classification: advisory.
- Artifact says (line 28): "| FR-5 | Must | The gateway shall expose a health check endpoint |"
- Code says: `src/gateway/gateway-http-route-contracts.ts:1-8` exposes six routes across three classes: live, ready, and startup.
- Code says: `docs/gateway/health.md:102-104` documents that only `/readyz` and `/startupz` reflect agent database admission and channel account readiness.
- Impact: the requirement is satisfied as written. It should name the three classes so a reader knows that a supervisor must watch readiness, not liveness.

### Advisory: FR-4 does not name the four config reload modes

- Classification: advisory.
- Artifact says (line 27): "| FR-4 | Must | The gateway shall support hot-reload of configuration without full restart |"
- Code says: `src/config/types.gateway.ts:88-89` defines `GatewayReloadMode` as `off`, `restart`, `hot`, or `hybrid`.
- Code says: `src/gateway/server-reload-hot.ts` and `src/gateway/server-reload-restart.ts` implement the two live paths.
- Impact: the requirement holds. It should mention that reload strategy is operator-selectable.

### Advisory: the acceptance criteria are all unchecked

- Classification: advisory.
- Artifact says (lines 51-58): every acceptance criterion is prefixed with `- [ ]`.
- Code says: the same behaviors are demonstrably implemented and covered by tests, for example `src/gateway/gateway.test.ts:254` asserts the hot-reload status and `src/gateway/auth.test.ts` covers the auth rejections.
- Impact: the checklist state does not reflect the code, which is misleading to a reader who treats unchecked boxes as unimplemented work.
