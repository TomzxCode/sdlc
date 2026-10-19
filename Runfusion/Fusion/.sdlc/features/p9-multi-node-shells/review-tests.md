---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Test cases that no longer match the code:

- TC-1 "Mesh task replication | task mutation | Replicated across nodes" asserts a capability that was deleted. Mesh task replication was removed at the PostgreSQL cutover (`packages/core/src/mesh/mesh-task-replication.ts:1` to `:8`), the replicated-create route was removed entirely (`packages/dashboard/src/routes/register-mesh-routes.ts:243` to `:250`), and the three replicated-create tests were deleted from the file the plan names (`packages/core/src/__tests__/mesh-task-replication.test.ts:1` to `:8`). The file now covers PROMPT.md seed builders and planning state only.
- TC-2 "Node route CRUD | node payload | Nodes created/updated" expects an update path. The named file covers only `GET /api/nodes` and `POST /api/nodes` (`packages/dashboard/src/routes/__tests__/register-node-routes.test.ts:69`, `:88`, `:131`). No test in the repository covers `PATCH /api/nodes/:id` (`packages/dashboard/src/routes/register-node-routes.ts:273`), `DELETE /api/nodes/:id` (`:409`), the health check (`:433`), metrics (`:451`), version (`:474`), plugin sync (`:497`), or compatibility (`:536`).
- TC-3 "Project CRUD | project payload | Projects managed" has no named file that covers it. `packages/dashboard/app/__tests__/api-projects.test.ts` is a general API-client suite for tasks, models, refine, and error handling, not project CRUD, and no file in the plan names the project registration route.
- TC-4 "Shell onboarding backcompat | legacy profile | Backcompat onboarding applied" points at the CLI autolaunch guard, which tests onboarding suppression rather than a legacy shell profile. `packages/cli/src/commands/__tests__/onboard-autolaunch-backcompat.test.ts:11` covers the skip reasons, and no test in the repository covers a legacy profile record in the mobile profile store (`packages/mobile/src/__tests__/connection-profiles.test.ts:20` to `:84`).
- TC-5 "ShellContext bridge | host type | Normalized shell host" points at a file that does not test host normalization. `packages/dashboard/app/__tests__/ShellContext.test.tsx:27` has one case, the open-connection-manager signal. Host normalization is covered in `packages/dashboard/app/__tests__/shell-host.test.ts:16` to `:60` and `packages/dashboard/app/__tests__/shell-native.test.ts:31`, neither of which is named in Key Test Files.
- TC-8 "Shell onboarding E2E | fresh device | Onboard via profile" is a gating test, not an end-to-end onboarding run. `packages/dashboard/app/__tests__/App.shell-onboarding.test.tsx:5` to `:55` asserts whether the onboarding modal is required, and no test drives the profile save and activation path through the modal.
- TC-9 "Node/project API integration | live server | Routes serve data" names two files that mock the fetch layer. `packages/dashboard/app/__tests__/api-node.test.ts:35` asserts the proxy helper arguments, and `packages/dashboard/app/__tests__/api-projects.test.ts:231` asserts JSON error handling, so neither starts a server. The live-server coverage for the project list is `packages/dashboard/src/__tests__/routes-tasks.test.ts:559`.

Named test files that do not exist:

- Key Test Files lists `packages/dashboard/src/routes/__tests__/api-node.test.ts`. No such file exists. The suite lives at `packages/dashboard/app/__tests__/api-node.test.ts`.
- Key Test Files lists `packages/dashboard/src/routes/__tests__/api-projects.test.ts`. No such file exists. The suite lives at `packages/dashboard/app/__tests__/api-projects.test.ts`.

Coverage matrix gaps:

- The Coverage Matrix has no row for FR-5, FR-6, NFR-2, or NFR-3, so four stated requirements are unverified by the plan.
- FR-4 is mapped only to TC-10, whose scope is "CLI serve/daemon/dashboard". The CLI project and node surfaces named in the requirement are covered by `packages/cli/src/commands/__tests__/project.test.ts:183` onward and `packages/cli/src/commands/__tests__/node.test.ts:237` onward, and the mesh status command is covered at `packages/cli/src/commands/__tests__/node.test.ts:580` to `:653`, but none of them is mapped.
- FR-2 is mapped to TC-1 and TC-6. TC-1 no longer exists as described, so the mesh protocol is verified only by the scheduler audit case, and the mesh HTTP surface has no mapped case.
- NFR-1 is mapped to TC-6 and TC-7, which cover the scheduler. The durable claim and lease tables (`packages/core/src/postgres/schema/central.ts:296`) and the unreachable-node policy (`packages/core/src/__tests__/unavailable-node-policy.test.ts:12`) are not mapped.

Significant test areas the plan does not cover:

- The mesh HTTP registrar suite is absent from Key Test Files: `packages/dashboard/src/__tests__/mesh-routes.test.ts:259` covers `POST /api/mesh/sync` including API key validation, peer merge, and new-peer computation, and `:737` covers the distributed task identifier routes.
- The Docker node subsystem is absent: `packages/core/src/__tests__/docker-client.test.ts`, `packages/core/src/__tests__/docker-provisioning.test.ts`, `packages/core/src/__tests__/mesh-config-generator.test.ts`, `packages/dashboard/src/routes/__tests__/register-docker-node-routes.test.ts`, `packages/dashboard/src/routes/__tests__/register-docker-provisioning-routes.test.ts`, `packages/dashboard/src/routes/__tests__/docker-node-routes.test.ts`, `packages/dashboard/src/routes/__tests__/docker-node-failure.test.ts`, and `packages/dashboard/src/routes/__tests__/docker-node-management-routes.test.ts`.
- The cloud-link pairing surface is absent: `packages/core/src/cloud-link/__tests__/client.test.ts`, `packages/core/src/cloud-link/__tests__/candidates.test.ts`, `packages/core/src/cloud-link/__tests__/store.test.ts`, and `packages/cli/src/commands/__tests__/cloud.test.ts:30` onward.
- The node discovery surface is absent: `packages/core/src/__tests__/node-discovery.test.ts:76` onward and `packages/core/src/__tests__/node-connection.test.ts`.
- The remote access surface is absent: `packages/dashboard/src/__tests__/remote-access-routes.test.ts:158` onward, `packages/dashboard/src/__tests__/routes-remote-access.test.ts`, and `packages/dashboard/src/__tests__/remote-login-handoff.test.ts`.
- The cross-node settings sync surface is absent: `packages/dashboard/src/routes/__tests__/settings-sync-attribution.test.ts:84` onward covers the pull, the receive, and the auth-receive attribution, and `packages/dashboard/src/__tests__/routes-system.test.ts:371` to `:375` covers the route inventory.
- The native shell package suites are absent: `packages/mobile/src/__tests__/native-shell.test.ts`, `packages/mobile/src/__tests__/qr-scanner.test.ts`, `packages/mobile/src/__tests__/shell-handoff.test.ts`, `packages/mobile/src/__tests__/connection-profiles.test.ts`, and `packages/desktop/src/__tests__/preload.test.ts` and `packages/desktop/src/__tests__/main-local-mode.test.ts`.
- The remaining shell surface suites are absent: `packages/dashboard/app/__tests__/shell-native.test.ts` and `packages/dashboard/app/__tests__/onboarding-overlay-layering.test.ts`.
