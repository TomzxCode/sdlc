---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Specification review: Gateway Server

## Sync drift: 2026-10-19

The specification was reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: the Gateway is no longer built on Hono

- Classification: blocking.
- Artifact says (line 10): "The Gateway Server is built on Hono (a lightweight HTTP framework) with WebSocket support."
- Artifact says (line 80): "| HTTP framework | Hono | Lightweight, fast, good WebSocket support, TypeScript-native |"
- Artifact says (line 15): "HTTP/WS Clients → Hono Router → Auth Middleware → Method Dispatch"
- Code says: `src/gateway/server-http.ts:1` imports `createServer` from `node:http` and `createServer` from `node:https`.
- Code says: `src/gateway/server-runtime-state.ts:307` creates the WebSocket server with `new NpmWebSocketServer({ noServer: true, ... })` from `packages/gateway-client/src/websocket.js`.
- Code says: `package.json` has no `hono` dependency and no file under `src/` imports `hono`.
- Code says: there is no router or middleware layer.
- Code says: `src/gateway/server-http-request.ts` dispatches by classifying the request path.
- Impact: every architecture, sequence, and technical-decision statement in the artifact that names Hono is wrong.

### Blocking: the Session data model no longer matches the session store

- Classification: blocking.
- Artifact says (lines 27-36): a `Session` table with `sessionId` as PK, `agentId`, `createdAt`, `updatedAt`, `metadata` JSON, and `state`.
- Code says: `src/state/openclaw-agent-schema.sql:16` defines `session_nodes` keyed by `session_key` (not `sessionId`), with `current_session_id`, `entry_json`, `status` constrained to `running|done|failed|killed|timeout`, `created_via`, `created_actor_type`, `owner_actor_type`, `owner_actor_id`, `project_id`, `parent_session_key`, `fork_source_session_key`, `label`, `display_name`, `category`, `pinned_at`, `archived_at`, `last_read_at`, `last_interaction_at`, `last_activity_at`.
- Code says: `src/state/openclaw-agent-schema.sql:53` adds `session_entry_snapshots`, `:120` adds `session_participants`, `:131` adds `session_key_contract`, `:140` adds `session_windows`, `:192` adds `conversations`, `:257` adds `session_conversations`, `:288` adds `session_members`, and `:437` adds `transcript_events`.
- Code says: there is no `metadata` column and no free-form `state` column on the session row.
- Impact: a reader would look for a single flat session table and a `state` enum that the code does not have.

### Blocking: session state is not SQLite-only, and the Out of Scope list is contradicted

- Classification: blocking.
- Artifact says (line 10): "Session state is persisted to SQLite via Kysely."
- Artifact says (line 82): "| State storage | SQLite via Kysely | Durable, no external DB dependency, good query capabilities |"
- Artifact says (line 94, under Out of Scope): "External database support (PostgreSQL, etc.)"
- Code says: `package.json:6` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`.
- Code says: `package.json:11` sets `openclaw.postgresFamilies` to `["state", "agent", "workboard", "logbook", "team-reports"]`.
- Code says: `src/infra/database-engine/registry.ts:24-33` marks the `state`, `agent`, `workboard`, `logbook`, and `team-reports` families as `postgres: true`.
- Code says: `src/infra/database-engine/registry.ts:39-56` resolves a per-family engine override, so the `agent` family that holds `session_nodes` and `transcript_events` can run on PostgreSQL.
- Code says: `docs/reference/database-engines.md` documents the experimental PostgreSQL adapter, and `docs/gateway/postgresql.md` is the operator guide.
- Impact: the artifact states as out of scope a capability the product ships today, and a reader would believe SQLite is the only supported store.

### Blocking: the `POST /api/sessions` REST contract does not exist

- Classification: blocking.
- Artifact says (lines 40-54): "`POST /api/sessions`" with `agentId` and `channelId` request fields and a `sessionId` plus `token` response.
- Artifact says (lines 69-74): the Session Creation Flow starts with "Client → Gateway: POST /api/sessions { agentId, channelId }".
- Code says: there is no `/api/sessions` route.
- Code says: session creation is the `sessions.create` RPC method, declared at `src/gateway/methods/core-descriptors.ts:253`.
- Code says: the HTTP surface is limited to probe routes, Control UI routes, plugin HTTP routes, and the node watch routes, classified in `src/gateway/gateway-http-route-contracts.ts:1-71` and `src/gateway/remote-control-ui-http-routing.ts`.
- Code says: the transport is a WebSocket JSON-RPC protocol, documented in `docs/gateway/protocol.md`.
- Impact: a reader would build against a REST endpoint that is not there, and would expect a session access token that the RPC path does not return.

### Blocking: the `GET /health` response contract is wrong and incomplete

- Classification: blocking.
- Artifact says (lines 56-63): "`GET /health`" returns `status` of `ok` or `degraded` plus `uptime` in seconds.
- Code says: `src/gateway/server-http-probes.ts:121-124` returns `JSON.stringify({ ok: true, status })` for the live class, so the body is `{"ok":true,"status":"live"}` and there is no `uptime` field.
- Code says: `src/gateway/gateway-http-route-contracts.ts:1-8` defines six probe routes across three classes: `/health` and `/healthz` are `live`, `/ready` and `/readyz` are `ready`, `/startup` and `/startupz` are `startup`.
- Code says: `src/gateway/server-http-probes.ts:88-120` returns `200` or `503` for the ready and startup classes, and `405` for non-GET and non-HEAD methods.
- Code says: `docs/gateway/health.md:102-104` and `docs/gateway/health.md:287` document the same contract.
- Impact: an operator or a supervisor reading the artifact would monitor the wrong route and parse the wrong body.

### Blocking: the auth model is understated

- Classification: blocking.
- Artifact says (line 10): "Auth uses bearer tokens, device-pairing handshake, or pre-configured bootstrap tokens."
- Artifact says (line 81): "| Auth model | Bearer token + device pairing | Simple for single-user, extends to node pairing |"
- Code says: `src/gateway/auth.ts:38-46` lists eight authentication methods: `none`, `token`, `password`, `tailscale`, `device-token`, `bootstrap-token`, `trusted-proxy`, and `remote-ingress`.
- Code says: `src/gateway/auth-mode-policy.ts:1-30` rejects an ambiguous config that sets both `gateway.auth.token` and `gateway.auth.password` without an explicit `gateway.auth.mode`.
- Code says: `src/gateway/auth.ts:44-45` carries a fully verified Tailscale identity, not just a boolean.
- Impact: the artifact omits password mode, Tailscale identity, and trusted-proxy identity, so a reader would mis-plan a deployment behind a reverse proxy.

### Blocking: plugin method dispatch is a scoped, entitlement-gated registry, not a middleware pipeline

- Classification: blocking.
- Artifact says (line 10): "It uses a plugin-based architecture for method handlers and middleware."
- Code says: `src/gateway/methods/core-descriptors.ts:20` holds the canonical core method policy table, and the file declares 526 core methods.
- Code says: `src/gateway/methods/registry.ts:25-60` normalizes each descriptor, forces plugin-owned methods through `normalizePluginGatewayMethodScope`, and rejects session-scoped methods that are not `operator.write` with a required profile.
- Code says: `src/plugin-sdk/gateway-method-runtime.ts:33-38` reserves gateway method dispatch for plugins that declare `contracts.gatewayMethodDispatch: ["authenticated-request"]`.
- Code says: `src/gateway/methods/descriptor.ts` defines the scope, lifetime, `controlPlaneWrite`, `profileAccess`, and `sessionAccess` axes that the artifact never mentions.
- Code says: `src/gateway/server-methods/request-authorization.ts` and `src/gateway/server-methods.ts:260-584` implement pre-dispatch authorization, control-plane write budgets, and mutation guards.
- Impact: the artifact describes a middleware chain that does not exist and omits the scope and entitlement model that now governs every call.

### Advisory: the config reload decision names only one of four modes

- Classification: advisory.
- Artifact says (line 83): "| Config reload | File watcher + hot-reload | Zero-downtime config updates without process restart |"
- Code says: `src/config/types.gateway.ts:88-89` defines `GatewayReloadMode` as `off`, `restart`, `hot`, or `hybrid`.
- Impact: wording and granularity only. The requirement that reload exists still holds.

### Advisory: the architecture diagram omits the probe routes, the method registry, and the session-row projection

- Classification: advisory.
- Artifact says (lines 14-23): the diagram shows "HTTP/WS Clients → Hono Router → Auth Middleware → Method Dispatch" branching to "Session Methods" and "Plugin Methods" over a "SQLite Store".
- Code says: the diagram also omits the probe routes, which `src/gateway/gateway-http-route-contracts.ts:1-71` classifies separately from Control UI and plugin routes, and the method descriptor model, which `src/gateway/methods/descriptor.ts` defines with scope, lifetime, and access axes.
- Impact: the diagram is a simplification, not a contradiction, once the Hono naming is fixed.

### Advisory: the Risks and Unknowns list is out of date

- Classification: advisory.
- Artifact says (lines 86-88): "WebSocket scaling with many concurrent connections needs benchmarking" and "Plugin-provided HTTP endpoints may have security implications for auth enforcement".
- Code says: `src/gateway/server/event-loop-health.ts`, `src/gateway/server/health-state.ts`, and `src/gateway/server/readiness.ts` now cover event-loop and readiness health, and `src/gateway/server/plugins-http/route-auth.ts` plus `src/gateway/security-path.ts` now own plugin route auth.
- Impact: the risks have been addressed in code, so the list no longer points at live uncertainty.
