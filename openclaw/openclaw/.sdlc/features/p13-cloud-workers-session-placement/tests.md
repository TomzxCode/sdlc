---
title: "Cloud Workers and Session Placement"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Cloud Workers and Session Placement

## Scope

This plan covers the Gateway control plane in `src/gateway/worker-environments/`, the worker runtime in `src/worker/`, and the private worker-runtime package in `packages/worker-runtime/`. It covers environment lifecycle, provider provisioning and teardown, placement dispatch and recovery, worker admission, worker turn execution and RPC, workspace sync and reconciliation, credential brokering, node enrollment, bundle installation, worker-local inference, and the bounded task pool.

Out of scope: the provider plugins themselves (including the bundled Crabbox provider and its CLI), the Control UI screens, the GitHub publication broker, and the Rust node host in `crates/` (tracked separately as FEAT-p11).

Every test file listed below was confirmed to exist in the repository.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-U-admission | `src/gateway/worker-environments/admission.test.ts`: worker admission against the durable credential, build, and environment record | A connect envelope with a valid credential plus one mutated binding at a time | The matching admission reason (`invalid-credential`, `environment-mismatch`, `placement-mismatch`, `session-mismatch`, `credential-expired`, `environment-unavailable`, `bundle-mismatch`, `version-mismatch`, `owner-epoch-mismatch`, `rpc-set-mismatch`, `protocol-features-mismatch`) is returned, and a live connection is fenced after credential rotation |
| TC-U-store | `src/gateway/worker-environments/store.test.ts`: durable environment store transitions, owner epochs, fallback ports, and credential binding | Legal and illegal transition requests, ten ordered SSH fallback rows, SecretRef-only SSH keys | Legal transitions commit; illegal, stale, and lease-incomplete transitions are rejected; owner epochs are globally distinct across a session move; only SecretRef metadata is persisted for SSH keys |
| TC-U-credential-broker | `src/gateway/worker-environments/credential-broker.test.ts`: credential minting, renewal, and session binding | Attach, renew, and restart scenarios with a live or undelivered credential | Attach is refused before the current bootstrap; renewal stays on one owner epoch; an undelivered atomic session credential is recovered after restart without changing the owner |
| TC-U-launch-descriptor | `src/worker/launch-descriptor.test.ts`: launch descriptor validation | Malformed GitHub bindings, absent or partially populated exec authority, open connection endpoints, unbounded tool names, missing computer descriptors | Every malformed descriptor is rejected; only closed Unix or public WebSocket endpoints, bounded unique tool names, and complete authority pairs are accepted |
| TC-U-workspace-reconcile | `src/gateway/worker-environments/workspace-reconcile.test.ts`: reconciliation journal, staged result publication, and patch application | Changed, added, executable, binary, and symlink results; an oversized journal; a failed fence-row update | The accepted manifest is published before the journal advances; the journal is rejected above the inventory budget; raw bytes are preserved; the published result survives a failed fence-row update |
| TC-U-workspace-sync | `src/gateway/worker-environments/workspace-sync.test.ts`: bounded inbound workspace transfer over the SSH and node transports | Transfers with `never` and `idempotent` retry authority | A stale authority is rejected after preparation, and the bounded transfer fails rather than completing unbounded |
| TC-U-provider-destroy-timeout | `src/gateway/worker-environments/provider-destroy-timeout.test.ts`: provider teardown deadlines | A teardown that exceeds its deadline | The teardown stays queued, and a stale owner is rejected before any retry side effect runs |
| TC-U-bundle-installer | `src/gateway/worker-environments/node-worker-bundle-installer.test.ts`: node worker bundle installation | Concurrent installs sharing one environment | Install phases are published, byte notices and logs are throttled by the installer clock, and each sharing environment is reference counted until its callers settle |
| TC-U-inference-lifecycle | `src/gateway/worker-environments/inference-lifecycle.test.ts`: worker inference manager drain and cancellation | An exact Gateway stop, a revoked drain authority, a pending durable begin | The provider is cancelled idempotently; a stale drain never releases a newer accepted drain; a drain waits for an accepted start before shutdown persists its turn |
| TC-U-turn-execution | `src/gateway/worker-environments/worker-turn-execution.test.ts`: worker turn execution gates | Run authority closing during an await, and cancellation during result hydration | A passing gate is fenced when run authority closes, and the committed terminal result is settled when execution is cancelled during hydration |
| TC-U-worker-runtime | `src/worker/worker.runtime.test.ts`: worker-side runtime lifecycle | An empty model response, a real image above 64 KiB, a rejected admission, a rejected heartbeat, a stale mid-run transcript | Tool outcomes finalize, a large image settles through input and tool result, admission failure fails closed, a rejected heartbeat fences the worker, and a stale transcript base fails the run without duplicating or rebasing the paid tail |
| TC-U-worker-process | `src/worker/worker-process.test.ts`: restricted worker process startup | A worker process that receives a command before SQLite is admitted | The command is refused until the worker's own SQLite capability is admitted |
| TC-U-task-admission | `packages/worker-runtime/src/worker-task-admission.ts` and `packages/worker-runtime/src/worker-task-capacity.ts`, exercised through the pool tests: bounded admission | Task counts and input bytes at the configured limits | Admission refuses over-budget work instead of queueing without a bound, and a waiting pool is not overtaken by a newly submitting pool |
| TC-U-retained-operation | `packages/worker-runtime/src/retained-operation.test.ts`: retained operation combinators | A successor adoption and a source servicing throw | The successor is adopted once and serviced in the captured context without Promise reactions, and cleanup is joined after a synchronous source servicing throw |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-I-service-lifetime | `src/gateway/worker-environments/service-lifetime.test.ts`: service startup, periodic reconciliation, and shutdown drain | A running environment service with a scheduler and provider catalog | The catalog warms only for nonterminal profiles, failed maintenance retries on the next sweep, timed-out provider work is awaited during shutdown, a create queued before shutdown is rejected once its lock is acquired, and a destroy accepted before shutdown drains while it waits for the lock |
| TC-I-inventory-recovery | `src/gateway/worker-environments/service-inventory-recovery.test.ts`: read admission across a sealed database | A sealed database that later reopens | Reconciliation resumes after the reopen, while shutdown stays final |
| TC-I-prepare | `src/gateway/worker-environments/service-prepare.test.ts`: on-demand prepared worker admission | A HEAD request with no session, plus concurrent fresh builds | Admission authorizes setup and starts background preparation, the admitted profile's idle timeout survives a mid-flight configuration change, and concurrent builds deduplicate and fail closed at the global cap |
| TC-I-provider-provisioning | `src/gateway/worker-environments/provider-provisioning.test.ts`: provider allocation and profile handling | A provider profile with machines, operating systems, and a secret reference | Intent and the immutable profile settings are persisted before allocation, an explicit placement mode is required, an SSH lease is rejected for worker-turn placement, plaintext secret fields are rejected, and a permanent provider rejection is recorded as terminal |
| TC-I-provider-bootstrap | `src/gateway/worker-environments/provider-bootstrap.test.ts`: bundle installation and remote bootstrap | A provider whose install or SSH bootstrap fails or times out | An installation failure is recorded before a lease is allocated, a failed receipt persistence keeps the lease retryable, a timed-out SSH bootstrap aborts before the lease is torn down, and the failure detail is bounded in the session description |
| TC-I-provider-reconciliation | `src/gateway/worker-environments/provider-reconciliation.test.ts`: reconciliation against provider evidence | Persisted leases, a removed profile, and a stale bundle hash | A matching pre-credential row is adopted, a lease is inspected with its snapshot profile, a stale bundle hash re-enters bootstrapping, an unknown lease is fenced before stop, and the exact attached owner is preserved until remote stop is confirmed across a restart |
| TC-I-placement-dispatch | `src/gateway/worker-environments/placement-dispatch.test.ts`: dispatch, reclaim, and workspace reconciliation during a placement | A provider, an attached environment, and a completed turn | Startup transitions are reported without breaking dispatch, a completed turn's pending workspace result is recovered before stale-claim teardown, a workspace preflight failure is rejected before allocation and a corrected redispatch is allowed, a conflict keeps the worker draining, and an exact active environment is adopted after restart without reprovisioning |
| TC-I-placement-recovery | `src/gateway/worker-environments/placement-dispatch-recovery.test.ts`: restart recovery of a placement | A Gateway that restarted while a placement was in progress | An authoritative provisioning placement resumes through the canonical dispatch stages, a placement whose durable execution mode differs is fenced before attachment, a placement interrupted before its environment intent fails and permits redispatch, and a pending result is not recovered through a worker with the legacy launch dialect |
| TC-I-turn-launcher | `src/gateway/worker-environments/worker-turn-launcher.test.ts`: worker turn launch and local placement gating | A session with and without a placement, plus a compacted successor | A transcript target without a session incarnation is rejected, a target from another incarnation is rejected, a rebound session key is rejected, the exact local claim cleanup is kept across compaction successor acceptance, a stale local finally never releases a reclaimed run id, and local CLI execution is rejected after worker activation |
| TC-I-turn-rpc | `src/gateway/worker-environments/worker-turn-rpc.test.ts`: worker RPC admission, credentials, and inference over the worker channel | A preclaimed worker placement, a rotated credential, and an expired credential | Only a gateway-preclaimed placement is admitted, credential, build, owner-epoch, and successful admission gates are recorded, a late admission result is not attributed to a replacement with the same run id, exact-claim inference stays live past the credential TTL, an expired delivered credential is not rotated while its durable turn is active, and post-terminal mutations are fenced while sequenced replays are preserved |
| TC-I-node-enrollment | `src/gateway/worker-environments/node-enrollment.test.ts`: node enrollment and artifact transfer | A requested-state environment with artifacts to prepare | Artifacts are prepared without enrollment or transfer grants, grants are sized for the actual artifacts, both preparation archives are served over HTTP only while their exact owner is current, and an older pending enrollment never replaces a newer one |
| TC-I-task-server | `packages/worker-runtime/src/worker-task-server.test.ts`: the worker-side task server over a real message port | A parent and a task port with a startup message and a late resource-close receipt | The task server installs its listener on the startup port, serves a task, and joins the late resource-close receipt outside the execution promise it depends on |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-E-native-worker | `src/worker/native-worker.integration.test.ts`: a real worker with native (worker-local) inference | Start the worker with a private startup model and auth, run local tools, then commit the transcript | The worker executes local tools and durably commits their transcript; a pending native HTTP request is cancelled without submitting new transcript messages; an unselected sibling Gateway-proxied inference stays proxied when a local startup is provisioned |
| TC-E-placement-flow | `src/gateway/worker-environments/placement-dispatch.test.ts` and `src/gateway/worker-environments/placement-dispatch-recovery.test.ts` combined: dispatch, run, reconcile, reclaim, and recover | Provision an environment, dispatch a session, run a turn, let the worker die, then restart the Gateway | The transcript survives through durable commit batches, the accepted workspace result reconciles into the managed worktree, the reclaim completes, and the recovery pass re-derives the live placement, owner epoch, placement generation, and turn claim before any launch |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Credential presented by a different environment, or after rotation | Admission returns `environment-mismatch` or `invalid-credential`; a live connection is fenced with `credential-replaced` |
| TC-E2 | Worker bundle, OpenClaw version, RPC set version, or protocol features do not match the running Gateway | Admission refuses the connection with the matching reason and the session is redispatched |
| TC-E3 | Credential expired, or the environment moved to `draining` or `destroying` | Admission refuses with `credential-expired` or `environment-unavailable`; identity revalidation closes the socket on the next RPC |
| TC-E4 | Owner epoch changed after a session moved between environments | The stale worker is fenced with `owner-epoch-mismatch` and is never merged with the new owner |
| TC-E5 | Placement interrupted before its environment intent was persisted | Recovery fails the placement and permits a redispatch; it never adopts a partial environment |
| TC-E6 | Durable execution mode differs from the recovered placement | The placement is fenced before attachment rather than downgraded to a legacy dialect |
| TC-E7 | Worker with the legacy launch dialect attempts to recover a pending result | The pending result is not recovered through that worker |
| TC-E8 | Workspace changes on the remote side after the local result was accepted | The worker stays draining and the accepted local result is not silently replaced |
| TC-E9 | The quiescence lease expires or the accepted local result changes during reconciliation | The worker stays draining; the pending result stays fenced |
| TC-E10 | Workspace preflight fails before allocation | The dispatch is rejected before a machine is allocated, and a corrected redispatch is accepted |
| TC-E11 | Remote workspace inventory, manifest, or reconciled patch exceeds its limit | The operation fails with the limit named; no partial result is accepted |
| TC-E12 | Transcript commit presented with a base behind the current commit head | The run fails instead of duplicating or rebasing already-paid output |
| TC-E13 | Provider teardown exceeds its deadline | The teardown stays queued and a stale owner is rejected before retry side effects |
| TC-E14 | Provider returns a permanent profile rejection | The rejection is recorded as terminal and no retry loop is scheduled |
| TC-E15 | Plaintext secret fields in a provider profile | The profile is rejected before any intent is persisted |
| TC-E16 | A stale placement move completion arrives after a newer placement became active | The superseded source placement is not retired; the current placement stays active |
| TC-E17 | A worker tool invocation arrives after the placement generation changed | The invocation is refused, the effect does not run, and the denial is recorded as a runtime action decision |
| TC-E18 | A turn claim is missing, or its generation and owner epoch do not match | The turn is refused and no tool surface is granted |
| TC-E19 | Task pool reaches its admitted task count or admitted byte limit | The submission is rejected instead of queued without a bound |
| TC-E20 | A prepared pool sits at its configured maximum | The extra preparation is refused, and an unused preparation is released when it expires |

## Test Infrastructure

- Vitest is the test runner for the whole repository. The worker-environment suites use in-repo fakes for the provider, the SSH transport, the node supervisor, and the clock, plus `test/helpers/temp-dir.ts` for temporary directories.
- The Gateway suites exercise the real SQLite state schema in `src/state/openclaw-state-schema.sql`, so the table constraints described in the specification are enforced by the tests rather than mocked.
- The worker runtime suites in `src/worker/` run the real worker runtime against a real worker connection client, and `src/worker/native-worker.integration.test.ts` runs a real native inference startup.
- The `packages/worker-runtime` suites use real `node:worker_threads` message ports, so the startup handshake, the task channel, and the resource-close receipts are exercised across a real thread boundary.
- The node enrollment suite serves the real authenticated HTTP artifact routes, so the transfer authority and its expiry are covered end to end.
- No external cloud provider, network access, or real machine is required. The provider is always a test double.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-I-service-lifetime, TC-I-provider-reconciliation, TC-U-store |
| FR-2 | TC-I-provider-provisioning, TC-U-store |
| FR-3 | TC-I-prepare, TC-I-provider-provisioning |
| FR-4 | TC-U-admission, TC-U-credential-broker, TC-I-turn-rpc |
| FR-5 | TC-U-admission, TC-I-turn-rpc |
| FR-6 | TC-I-placement-dispatch, TC-I-placement-recovery |
| FR-7 | TC-I-turn-launcher, TC-I-turn-rpc, TC-U-launch-descriptor, TC-U-worker-process, TC-E18 |
| FR-8 | TC-E-native-worker, TC-U-inference-lifecycle |
| FR-9 | TC-I-turn-rpc, TC-E17 |
| FR-10 | TC-U-worker-runtime, TC-E12 |
| FR-11 | TC-U-workspace-reconcile, TC-I-placement-dispatch, TC-E11 |
| FR-12 | TC-I-placement-dispatch, TC-E16, TC-E20 |
| FR-13 | TC-I-prepare, TC-U-task-admission, TC-E19, TC-E20 |
| FR-14 | TC-I-placement-dispatch, TC-U-admission |
| NFR-1 | TC-E-native-worker, TC-I-provider-provisioning, TC-U-credential-broker, TC-E15 |
| NFR-2 | TC-U-admission, TC-I-turn-rpc |
| NFR-3 | TC-I-placement-recovery, TC-E5, TC-E6, TC-E7 |
| NFR-4 | TC-U-workspace-reconcile, TC-U-workspace-sync, TC-E11 |
| NFR-5 | TC-I-prepare, TC-E20 |
| NFR-6 | TC-I-service-lifetime, TC-I-inventory-recovery, TC-I-provider-reconciliation |
