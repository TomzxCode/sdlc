---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
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
