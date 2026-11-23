---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Test plan review: Gateway Server

## Sync drift: 2026-10-19

Every test file the artifact lists still exists.
Two coverage-matrix rows point at files that do not cover the requirement they claim.
Several large areas of the gateway have no listed coverage.

### Blocking: FR-6 and NFR-1 are mapped to a file that tests neither shutdown nor crash recovery

- Classification: blocking.
- Artifact says (line 18): "| `src/gateway/gateway-stability.test.ts` | Stability and error recovery scenarios |"
- Artifact says (line 61): "| FR-6 (Graceful shutdown) | `gateway-stability.test.ts` |"
- Artifact says (line 62): "| NFR-1 (Crash recovery) | `gateway-stability.test.ts` |"
- Code says: `src/gateway/gateway-stability.test.ts:100` opens a single `describe("gateway stability lane")` and `:113` holds a single `it("keeps diagnostics bounded and queues drained under synthetic gateway churn")`.
- Code says: that file imports only `src/infra/diagnostic-events.ts` and `src/logging/diagnostic-stability.ts`, so it measures diagnostic memory bounds and never starts, drains, or restarts a gateway.
- Code says: the real coverage lives in `src/gateway/server-shutdown.test.ts`, `src/gateway/server-shutdown.runtime.test.ts`, `src/gateway/drain-active-sessions-for-shutdown.test.ts`, `src/gateway/active-sessions-shutdown-tracker.test.ts`, and `src/gateway/server-kernel.shutdown-budget.test.ts`.
- Code says: crash and restart recovery is covered in `src/gateway/server-run-shutdown.recovery.test.ts`, `src/gateway/session-recovery-service.ts`, and `src/gateway/server-startup-recovery-boundary.test.ts`.
- Impact: the artifact claims a requirement is covered by a test file that cannot fail for that requirement.

### Blocking: FR-5 is mapped to a file that never touches the HTTP probe routes

- Classification: blocking.
- Artifact says (line 60): "| FR-5 (Health check) | `gateway.test.ts` |"
- Code says: `src/gateway/gateway.test.ts:130`, `:254`, `:371`, and `:921` all exercise the `health` gateway RPC method, not the HTTP probe routes.
- Code says: the HTTP probe contract is covered in `src/gateway/server-http.probe.test.ts`, `src/gateway/server.health.test.ts`, `src/gateway/server.health.lifecycle.test.ts`, and `src/gateway/server.health-request-lifetime.test.ts`.
- Impact: the artifact points at a test that cannot catch a broken `/health`, `/readyz`, or `/startupz` route, which is the contract the specification documents.

### Advisory: the coverage matrix omits five functional requirements

- Classification: advisory.
- Artifact says (lines 55-63): the matrix covers FR-1, FR-2, FR-3, FR-5, FR-6, NFR-1, and NFR-2 only.
- Artifact says: FR-4, FR-7, FR-8, FR-9, and FR-10 have no row.
- Code says: FR-4 is covered in `src/gateway/server-reload-handlers.hot-reload-status.test.ts` and `src/gateway/server-reload-hot.cron-lazy.test.ts`.
- Code says: FR-7 is covered in `src/gateway/auth-rate-limit.test.ts` and `src/gateway/server-methods.control-plane-rate-limit.test.ts`.
- Code says: FR-8 is covered in `src/gateway/node-pairing-auto-approve.test.ts` and `src/gateway/node-registry-pairing.test.ts`.
- Code says: FR-9 is covered in `src/gateway/server-broadcast-live-text.test.ts` and `src/gateway/server-runtime-subscriptions.test.ts`.
- Code says: FR-10 is covered in `src/gateway/server/plugins-http.test.ts`.
- Impact: the map is incomplete rather than wrong.

### Advisory: the Test Infrastructure section describes a mocked transport

- Classification: advisory.
- Artifact says (line 49): "- Mock HTTP and WebSocket servers for gateway testing"
- Artifact says (line 50): "- SQLite in-memory database for session state tests"
- Code says: `src/gateway/server-http.ts:18-24` creates a real `node:http` or `node:https` server, and `src/gateway/server-runtime-state.ts:307` creates a real `ws` WebSocketServer.
- Code says: the session store is worker-backed and engine-selectable, per `src/infra/database-engine/registry.ts:24-33`.
- Impact: the infrastructure description no longer matches how the gateway is exercised.

### Advisory: large gateway areas have no listed coverage

- Classification: advisory.
- Artifact says (lines 12-35): the plan lists four unit files, one integration file, and five live files.
- Code says: `src/gateway/` holds over 2,600 files, of which more than 1,900 are test files.
- Code says: unlisted but notable areas include the RPC method dispatch and authorization suite in `src/gateway/server-methods.*.test.ts` and `src/gateway/methods/core-descriptors.since.test.ts`.
- Code says: unlisted but notable areas include the plugin reload and recovery suite in `src/gateway/server-plugin-reload*.test.ts`.
- Code says: unlisted but notable areas include the event broadcast and subscription suite in `src/gateway/server-runtime-subscriptions.*.test.ts` and `src/gateway/server-broadcast.*.test.ts`.
- Code says: unlisted but notable areas include the worker placement suite in `src/gateway/server.worker-placement.*.test.ts`.
- Code says: unlisted but notable areas include the plugin in-process dispatch suite in `src/gateway/server-plugin-in-process-dispatch.*.test.ts`.
- Impact: the plan under-represents the gateway by a wide margin, which matters for future coverage planning.

## Sync drift: 2026-11-16

Fresh analysis of the owned test paths confirms the 2026-10-19 drift is still unresolved. All ten test files listed in the artifact still exist, so no file has been removed. The coverage-map findings below still hold, and the code has advanced further. Paths refer to the current checkout at version 2026.11.4.

### Persisting: FR-6 and NFR-1 are still mapped to a file that tests neither shutdown nor crash recovery

- Classification: blocking.
- Artifact says (lines 18, 61, and 62): `src/gateway/gateway-stability.test.ts` covers graceful shutdown and crash recovery.
- Code says: that file has a single `it("keeps diagnostics bounded and queues drained under synthetic gateway churn")` at line 67 and imports only diagnostic helpers. It never starts, drains, or restarts a gateway. Real coverage still lives in `src/gateway/server-shutdown.test.ts`, `src/gateway/server-shutdown.runtime.test.ts`, `src/gateway/drain-active-sessions-for-shutdown.test.ts`, and the recovery tests.
- Impact: the mapped test still cannot fail for the requirements it claims to cover.

### Persisting: FR-5 is still mapped to a file that never touches the HTTP probe routes

- Classification: blocking.
- Artifact says (line 60): `src/gateway/gateway.test.ts` covers the health check.
- Code says: the `health` references at lines 130, 254, 371, and 921 all exercise the `health` gateway RPC method, not the HTTP probe routes. The HTTP probe contract is covered in `src/gateway/server-http.probe.test.ts`, which is present, and in the server health lifecycle tests.
- Impact: the mapped test still cannot catch a broken `/health`, `/readyz`, or `/startupz` route.

### Persisting: the coverage matrix still omits five functional requirements

- Classification: advisory.
- Artifact says (lines 55-63): FR-4, FR-7, FR-8, FR-9, and FR-10 have no row.
- Code says: their tests still exist, including `src/gateway/server-reload-handlers.hot-reload-status.test.ts` for FR-4, `src/gateway/auth-rate-limit.test.ts` for FR-7, and `src/gateway/node-registry-pairing.test.ts` for FR-8. New: one file named in the 2026-10-19 review, `src/gateway/server-broadcast-live-text.test.ts`, is no longer present, so the equivalent FR-9 coverage should be re-located before the matrix is updated.
- Impact: the map is still incomplete, and one previously cited file needs a fresh reference.

### Persisting: the Test Infrastructure section still describes a mocked transport

- Classification: advisory.
- Artifact says (lines 49-50): mock HTTP and WebSocket servers and an in-memory SQLite database.
- Code says: `src/gateway/server-http.ts:18-24` creates a real `node:http` or `node:https` server, `src/gateway/server-runtime-state.ts:312-313` creates a real WebSocket server, and the store is worker-backed and engine-selectable per `src/infra/database-engine/registry.ts`.
- Impact: the infrastructure description still does not match how the gateway is exercised.

### Persisting: large gateway areas remain unlisted

- Classification: advisory.
- Artifact says (lines 12-35): the plan lists four unit files, one integration file, and five live files.
- Code says: `src/gateway/` still holds thousands of test files. Unlisted areas still include RPC method dispatch and authorization, plugin reload and recovery, event broadcast and subscription, worker placement, and plugin in-process dispatch. New: version 2026.8 session goal methods at `src/gateway/methods/core-descriptors.ts:251-252` indicate another area with no listed coverage.
- Impact: the plan still under-represents the gateway, which matters for future coverage planning.

## Sync drift: 2026-11-23

Fresh analysis against the current checkout at version 2026.11.7 confirms the 2026-11-16 drift is still unresolved.
All ten test files listed in the artifact still exist, so no listed file has been removed.
Line numbers and file names below refer to the current checkout.

### Persisting: FR-6 and NFR-1 are still mapped to a file that tests neither shutdown nor crash recovery

- Classification: blocking.
- Artifact says (lines 18, 61, and 62): `src/gateway/gateway-stability.test.ts` covers graceful shutdown and crash recovery.
- Code says: `src/gateway/gateway-stability.test.ts:67` holds a single test named "keeps diagnostics bounded and queues drained under synthetic gateway churn", and its imports at `:2-3` are diagnostic helpers only.
- Code says: the mapped file never starts, drains, or restarts a gateway. Shutdown coverage now lives in `src/gateway/server-shutdown.test.ts:11` and `src/gateway/server-shutdown.runtime.test.ts:112`, and `src/gateway/drain-active-sessions-for-shutdown.test.ts` is present.
- Code says: two recovery files cited in the 2026-11-16 review are no longer present, `src/gateway/server-run-shutdown.recovery.test.ts` and `src/gateway/server-startup-recovery-boundary.test.ts`, so fresh recovery references must be located before the matrix is updated.
- Impact: the mapped test still cannot fail for the requirements it claims to cover.

### Persisting: FR-5 is still mapped to a file that never touches the HTTP probe routes

- Classification: blocking.
- Artifact says (line 60): `src/gateway/gateway.test.ts` covers the health check.
- Code says: `src/gateway/gateway.test.ts:130`, `:254`, `:371`, and `:921` all call the `health` gateway RPC method, not an HTTP probe route.
- Code says: `src/gateway/server-http.probe.test.ts:206` opens the "gateway probe endpoints" suite and `:231-233` asserts `/readyz` responses, while `:258-261` covers probe namespace variants.
- Impact: the mapped test still cannot catch a broken `/health`, `/readyz`, or `/startupz` route.

### Persisting: the coverage matrix still omits five functional requirements

- Classification: advisory.
- Artifact says (lines 55-63): FR-4, FR-7, FR-8, FR-9, and FR-10 have no row.
- Code says: `src/gateway/server-reload-handlers.hot-reload-status.test.ts`, `src/gateway/auth-rate-limit.test.ts`, `src/gateway/node-registry-pairing.test.ts`, and `src/gateway/server/plugins-http.test.ts` exist for FR-4, FR-7, FR-8, and FR-10.
- Code says: the FR-9 file named in the 2026-11-16 review is now `src/gateway/server-broadcast.live-text.test.ts`, while `src/gateway/server-broadcast-live-text.test.ts` is absent.
- Impact: the map is still incomplete, and the FR-9 reference needs the current file name.

### Persisting: the Test Infrastructure section still describes a mocked transport

- Classification: advisory.
- Artifact says (lines 49-50): mock HTTP and WebSocket servers and an in-memory SQLite database.
- Code says: `src/gateway/server-http.ts:1-2` creates a real `node:http` or `node:https` server, `src/gateway/server-runtime-state.ts:312-313` creates a real WebSocket server, and `src/infra/database-engine/registry.ts:24-33` selects among engine families.
- Impact: the infrastructure description still does not match how the gateway is exercised.

### Persisting: large gateway areas remain unlisted

- Classification: advisory.
- Artifact says (lines 12-35): the plan lists four unit files, one integration file, and five live files.
- Code says: `src/gateway/` still holds over 1,500 test files. Unlisted areas include RPC method dispatch and authorization, plugin reload and recovery, event broadcast and subscription, worker placement, and worker and MCP app HTTP routes.
- Code says: `src/gateway/methods/core-descriptors.ts:243-244` adds version 2026.8 session goal methods, and `src/gateway/worker-environments/artifact-transfer-http.test.ts` covers worker bootstrap transfer.
- Impact: the plan still under-represents the gateway, which matters for future coverage planning.
