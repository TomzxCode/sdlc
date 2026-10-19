---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Architecture:

- The diagram has no CLI layer. The Overview says the `fn` CLI drives serve, daemon, dashboard, project, node, and mesh (`specification.md:10`), but the top box of the diagram is only "Desktop (Electron) / Mobile (Capacitor)" (`specification.md:15`). The CLI surface lives in `packages/cli/src/commands/` and is registered in `packages/cli/src/bin.ts:854` onward.
- The diagram omits the cloud-link control plane and the managed Docker host. The CLI pairs a node to a cloud control plane (`packages/core/src/cloud-link/client.ts:100`) and the engine keeps a tunnel alive for it (`packages/engine/src/cloud-link-presence.ts:1`), and managed node containers run on a separate Docker host (`packages/core/src/docker/docker-client.ts`).
- The diagram does not name the registrar mount-order contract. `CREATE_API_ROUTES_REGISTRAR_MOUNT_SEQUENCE` (`packages/dashboard/src/routes/create-api-routes-mount-sequence.ts:8`) is the tested contract that fixes the order of the registrars the diagram lists.
- The diagram names "register-docker-*" but the registrar pair is split: `registerDockerProvisioningRoutes` owns container lifecycle endpoints and `registerDockerNodeRoutes` owns managed-node metadata and mesh configuration (`packages/dashboard/src/routes/create-api-routes-mount-sequence.ts:19`).

Data Models:

- `url | string | not null | Node endpoint` is wrong. The column is a nullable text (`packages/core/src/postgres/schema/central.ts:59`).
- `status | enum | not null | online/offline` is wrong. The column is a text with default `offline` (`packages/core/src/postgres/schema/central.ts:61`), the mesh state payload accepts `online`, `offline`, `connecting`, and `error` (`packages/dashboard/src/routes/register-mesh-routes.ts:68`), and peer rows default to `unknown` (`packages/core/src/postgres/schema/central.ts:150`).
- The `claims/leases | json` row names a field that does not exist on the node row. Claims live in the `task_claims` table keyed by `(projectId, taskId)` with `ownerNodeId`, `ownerAgentId`, `ownerRunId`, `leaseEpoch`, and `leaseRenewedAt` (`packages/core/src/postgres/schema/central.ts:296` to `:309`).
- The Node table omits the fields the code persists: `name` (not null, unique, `:57`), `type` (not null, checked against `local` and `remote`, `:58` and `:72`), `apiKey` (`:60`), `capabilities` (`:62`), `systemMetrics` (`:63`), `knownPeers` (`:64`), `versionInfo` (`:65`), `pluginVersions` (`:66`), `dockerConfig` (`:67`), `maxConcurrent` (`:68`), `createdAt`, and `updatedAt` (`:69` and `:70`).
- The section has no model for the other central tables the feature depends on: `projects` (`packages/core/src/postgres/schema/central.ts:38`), `project_node_path_mappings` (`:78`), `peer_nodes` (`:144`), `managed_docker_nodes` (`:176`), `mesh_shared_snapshots` (`:235`), and `mesh_write_queue` (`:252`).

API Contracts:

- The request table says `name` is required and `nodeUrl` is optional. The route requires `name` and `path`, and `path` must be an absolute path (`packages/dashboard/src/routes/register-project-routes.ts:273` to `:302`). There is no `nodeUrl` field. The route also accepts `isolationMode`, `nodeId`, `cloneUrl`, `gitSetupMode`, `workspaceMode`, and `taskPrefix` (`:273`).
- The response table says 200 OK with a `project` field. The route answers 201 with the project object spread at the top level, plus `outcome` and `_meta` (`packages/dashboard/src/routes/register-project-routes.ts:573` to `:577`).
- The section documents one endpoint. The project registrar exposes 17 routes (`packages/dashboard/src/routes/register-project-routes.ts:70` to `:1131`), the node registrar exposes 16 (`packages/dashboard/src/routes/register-node-routes.ts:92` to `:536`), the mesh registrar exposes 6 (`packages/dashboard/src/routes/register-mesh-routes.ts:49` to `:252`), the discovery registrar exposes 5 (`packages/dashboard/src/routes/register-discovery-routes.ts:13` to `:136`), the Docker node registrar exposes 13 (`packages/dashboard/src/routes/register-docker-node-routes.ts:96` to `:490`), and the Docker provisioning registrar exposes 7 (`packages/dashboard/src/routes/register-docker-provisioning-routes.ts:38` to `:349`).
- No error contract is specified. The node routes answer 400 for a missing url, 404 for an unknown node, and 409 for a duplicate name (`packages/dashboard/src/routes/register-node-routes.ts:122`, `:255`, `:155` to `:160`), and the discovery route answers 502 for a malformed remote payload and 504 for a timeout (`:200` to `:216`).
- The mesh auth contract is not specified. A sender whose node row carries an `apiKey` must present it as `Authorization: Bearer <key>`, otherwise the route answers 401 (`packages/dashboard/src/routes/register-mesh-routes.ts:26` to `:41` and `:280` to `:289`).

Sequences:

- "register → discover → onboard (QR/manual/tokenized link) → mesh membership" does not match the node path. `fn node connect` registers the node and runs a health check in one step (`packages/cli/src/commands/node.ts:271` to `:338`), and there is no node QR or tokenized-link step. QR and manual entry belong to the native shell onboarding flow (`docs/native-shell.md`), and the tokenized link belongs to the remote access login URL (`packages/dashboard/src/routes/register-settings-memory-routes.ts:1190` and `:1222`).
- The sequence omits the membership exchange that actually happens over HTTP. `POST /api/mesh/sync` merges the sender's peers, marks the sender online, and exchanges auth material (`packages/dashboard/src/routes/register-mesh-routes.ts:252` to `:452`), and `GET /api/mesh/state` fans out to remote nodes and merges their snapshots (`packages/dashboard/src/routes/register-mesh-routes.ts:49` to `:157`).
- The sequence omits the distributed task identifier allocation that keeps identifiers unique across nodes: `POST /api/mesh/task-ids/reserve`, `POST /api/mesh/task-ids/commit`, `POST /api/mesh/task-ids/abort`, and `GET /api/mesh/task-ids/state` (`packages/dashboard/src/routes/register-mesh-routes.ts:166`, `:188`, `:208`, `:229`).

Technical Decisions:

- The "Shared backend" row states the outcome but omits the constraint that decides whether the topology is possible. Embedded PostgreSQL is per-machine only, so a shared board needs an external `DATABASE_URL` (`docs/shared-mesh-protocol.md`, `docs/multi-project.md:24` to `:29`).
- The decision table omits the port convention for managed node containers. They default to `4041` because `4040` is reserved for the production dashboard (`packages/core/src/mesh/mesh-config-generator.ts:13`, `docs/architecture.md:570`).
- The decision table omits the node auth rule that the mesh routes enforce, described under API Contracts above.
