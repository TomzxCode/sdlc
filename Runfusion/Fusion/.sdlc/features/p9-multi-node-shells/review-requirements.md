---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Stale requirements:

- FR-6 says the system shall "stream node/project scoped events over the shared `/api/events` bus". The shared bus is project-scoped only. The route reads one `projectId` query parameter (`packages/dashboard/src/server.ts:1319` and `:1320`) and the SSE options type carries only `projectId` (`packages/dashboard/src/sse.ts:555` to `:558`). Node-scoped events travel on a separate proxy stream, `GET /api/proxy/:nodeId/events` (`packages/dashboard/src/routes/register-proxy-routes.ts:214` and `:242`), and `docs/dashboard-realtime.md` lists the two as separate channels.
- FR-4 lists the CLI surfaces "serve, daemon, dashboard, project, node, and mesh". The CLI also ships `fn cloud` (`packages/cli/src/bin.ts:1173`, `packages/cli/src/commands/cloud.ts`) and `fn desktop` (`packages/cli/src/bin.ts:961`, `packages/cli/src/commands/desktop.ts`), and both are documented in `docs/cli-reference.md:544` and `:860`.
- FR-4 says the system shall "expose CLI commands and TUI for serve, daemon, dashboard, project, node, and mesh". The terminal UI exists for `fn dashboard` only (`packages/cli/src/commands/dashboard.ts:165`, `docs/cli-reference.md:323`). `fn serve` and `fn daemon` have no TUI entry point.

Missing requirements (behavior the code implements that no FR or NFR covers):

- Docker-managed node provisioning is not covered. `DockerProvisioningService` creates, starts, stops, restarts, and deprovisions managed node containers (`packages/core/src/docker/docker-provisioning.ts:19` and `:27`), `MeshConfigGenerator` applies the mesh configuration by recreating the container and then registers the node in the mesh (`packages/core/src/mesh/mesh-config-generator.ts:33`), and the dashboard owns the routes `POST /api/docker/provision` (`packages/dashboard/src/routes/register-docker-provisioning-routes.ts:38`), `POST /api/docker-nodes` (`packages/dashboard/src/routes/register-docker-node-routes.ts:283`), and `POST /api/docker/nodes/:managedId/apply-mesh-config` (`:368`). The managed node record is persisted in `managed_docker_nodes` (`packages/core/src/postgres/schema/central.ts:176`). FR-1 covers node registration, not container lifecycle.
- Cloud-link pairing and presence are not covered. The client exposes `cloudPairStart`, `cloudPairComplete`, `cloudHeartbeat`, and `cloudRedeemTicket` (`packages/core/src/cloud-link/client.ts:100`, `:119`, `:139`, `:171`), the CLI exposes `fn cloud pair-start | pair-complete | heartbeat | status | unlink` (`packages/cli/src/commands/cloud.ts:38`, `packages/cli/src/bin.ts:1173`), and the engine keeps a Cloudflare Quick Tunnel alive while publishing the current URL (`packages/engine/src/cloud-link-presence.ts:1`). FR-5 covers remote access through tunnel providers and a tokenized login, which is a different path.
- Node discovery over the local network is not covered. `NodeDiscovery` broadcasts and listens for the Bonjour service type `_fusion._tcp` (`packages/core/src/mesh/node-discovery.ts:12` to `:17`), `node-connection.ts` holds the peer connection helper (`packages/core/src/mesh/node-connection.ts:1`), and the dashboard owns `GET /api/discovery/status`, `POST /api/discovery/start`, `POST /api/discovery/stop`, `GET /api/discovery/nodes`, and `POST /api/discovery/connect` (`packages/dashboard/src/routes/register-discovery-routes.ts:13`, `:36`, `:91`, `:113`, `:136`). No FR or NFR mentions discovery.
- Cross-node settings and credential sync is not covered. The dashboard owns `GET /api/nodes/:id/settings`, `POST /api/nodes/:id/settings/push`, `POST /api/nodes/:id/settings/pull`, `GET /api/nodes/:id/settings/sync-status`, and `POST /api/nodes/:id/auth/sync` (`packages/dashboard/src/routes/register-settings-sync-routes.ts:166`, `:200`, `:287`, `:422`, `:503`), with inbound endpoints `POST /api/settings/sync-receive`, `POST /api/settings/auth-receive`, and `GET /api/settings/auth-export` (`packages/dashboard/src/routes/register-settings-sync-inbound-routes.ts:82`, `:203`, `:307`). FR-2 names a shared mesh protocol but not a per-node push and pull surface.
- Node plugin version sync and version compatibility checks are not covered. `POST /api/nodes/:id/sync-plugins` compares plugin versions between the local node and a remote node (`packages/dashboard/src/routes/register-node-routes.ts:497`) and `GET /api/nodes/:id/compatibility` compares app versions (`:536`).
- The policy for work pinned to an unreachable node is not covered. `unavailableNodePolicy` chooses between `block` and `fallback-local` (`packages/core/src/config/settings-schema.ts:561`, `packages/engine/src/scheduler.ts:3237` to `:3256`) and `owningNodeHandoffPolicy` chooses between `block`, `reassign-to-local`, and `reassign-any-healthy` (`packages/core/src/types/merge/merge-policy.ts:249`, `packages/engine/src/scheduler.ts:3140`). NFR-1 states that work must not be lost but names no operator-visible policy switch.

Acceptance criteria gaps:

- The acceptance criteria list has no entry for FR-5, FR-6, NFR-2, or NFR-3, so four stated requirements are unverified.
- Every acceptance criterion checkbox is unchecked while the document frontmatter reads `status: done` (`requirements.md:46` to `:61`).
