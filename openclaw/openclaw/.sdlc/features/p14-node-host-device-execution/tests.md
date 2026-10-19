---
title: "Node Host and Device Execution"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Node Host and Device Execution

## Scope

This plan covers the TypeScript node host in `src/node-host/`: the foreground runner, the private app worker, the transport-independent runtime, the `node.invoke` command surface including `system.run` and its approval plan and allowlist, the worker supervisor, the launch and turn journal, workspace staging, and the automatic runtime update. It also covers the Gateway-side node surface the node depends on, through the node handler suites in `src/gateway/server-methods/`.

Out of scope: the Rust node host in `crates/` (tracked separately as FEAT-p11), the macOS companion application's UI, the node registry's internal storage, and the cloud worker control plane (tracked as FEAT-p13).

Every test file listed below was confirmed to exist in the repository.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-U-runner | `src/node-host/runner.test.ts`: foreground host startup, credential resolution, and reconnect handling | An external signal closing the runtime, a companion stdin close, a pairing candidate, and expired fallback setup codes | Managed state admission is retained while the signal closes the runtime, the source runtime is joined when the companion stdin closes, the pairing candidate that completes the handshake is persisted, remote credentials are stripped before local node-host auth is resolved, a saved token is only offered for resume when a paired node credential exists, shared auth is never used as a fallback when the saved token disappears, explicitly requested environment auth replaces the paired token, remote-mode credentials survive a Gateway switch, MCP clients close before a terminal reconnect pause exits, and a pairing reconnect pause stays visible without stopping the foreground host |
| TC-U-runtime | `src/node-host/runtime.test.ts`: runtime lifecycle, skill-bin cache, invocation cancellation, and invoke input dispatch | A retired connection, a superseded invocation, a failed plugin cleanup, a framed plugin message listener failure, and a pre-spawn input overflow | A queued invocation is not admitted after its connection is retired, a superseded invocation is cancelled without orphaning its replacement, a failed plugin cleanup is retried on explicit close, invoke admission stays closed after a failed idle-worker cleanup until reconnect, MCP startup aborts without waiting while supervisor retirement runs independently, buffered and live input are delivered in sequence without replaying duplicates, and an overflowing pre-spawn buffer aborts without delivering partial input |
| TC-U-runtime-supervisor | `src/node-host/runtime.worker-supervisor.test.ts`: worker supervisor lifetime across the runtime | A claimed worker, a cancelled invoke, and a reconnect | The claimed worker stays alive until the runtime closes, so a cancel or a reconnect does not release a live worker |
| TC-U-invoke | `src/node-host/invoke.test.ts`: the `node.invoke` command surface | Plugin node commands, a redelivered plugin invocation, a terminal upload, and exec approval writes with a stale base hash, a lost CAS race, a lock timeout, a filesystem failure, and a malformed payload | The owning agent session is passed to plugin node commands, only the replacement result is published for a redelivered invocation, terminal uploads are staged, an exec approval update with a stale base hash or a lost CAS race is rejected, a lock timeout is classified as `TIMEOUT`, filesystem and update failures are classified as `UNAVAILABLE`, a malformed payload is classified as `INVALID_REQUEST`, and the effective exec policy is included in a `system.run.prepare` response |
| TC-U-system-run | `src/node-host/invoke-system-run.test.ts`: the `system.run` execution path | A companion relay that cannot preserve the execution context, an unreachable companion, a cancelled command, an approval miss without a plan, a transparent and a semantic env wrapper, and an approval-backed script operand | Execution context is refused when the companion cannot preserve it, a native cwd refusal is not labelled approval-required, an unreachable companion is reported without a local replay, a companion deadline is classified as a timeout, a cancelled command is neither spawned nor published, an approval miss without a plan is not auto-reviewed, env wrappers are handled in allowlist mode, an approved script operand is revalidated after the authorization commit, a runtime script operand binding is validated at dispatch, an unsafe environment input is rejected before execution, and a shell wrapper receives only the allowed environment values |
| TC-U-system-run-plan | `src/node-host/invoke-system-run-plan.test.ts`: the approval plan and its bindings | An approval request that omits the cwd, a mutable runtime operand, a mutable shell script operand, a symlinked binary with a writable target, and a rewritten `pnpm dlx` operand | The execution host working directory is captured, mutable operands are captured in the plan, a relative or writable native binary keeps the fail-closed behavior, a symlinked binary with a writable target is refused, a rewritten script operand is detected, and the real shell script operand is captured after a value-taking shell flag |
| TC-U-system-run-allowlist | `src/node-host/invoke-system-run-allowlist.test.ts`: allowlist argv resolution | A Windows shell execution, a bare wildcard authorization, and an opaque Windows shell transport | Windows shell execution is pinned to the resolved allowlisted executable, an unresolved Windows shell argv authorized by a bare wildcard is preserved, and an opaque Windows shell transport or a blocked execution plan fails closed |
| TC-U-launch-store | `src/node-host/node-worker-launch-store.test.ts`: the durable launch journal | An initialized schema, a warm launch join, a rolled-back transaction, an expired terminal receipt, and a container identity | A launch is claimed and started without revoking schema authority, admitted facts are shared across warm joins without freshness probes, lazy companion facts are refreshed after a rollback, only the oldest expired terminal receipts are pruned in bounded batches, the exact replay fence is kept while unrelated receipts are pruned, and a cleanup binding is not broadened when the ambient external mode changes |
| TC-U-turn-store | `src/node-host/node-worker-turn-store.test.ts`: the durable turn journal | A turn claim, a finish, a conflicting retry, a stale result writer, and an immutable identity mismatch | Durable claim and finish receipts are returned to one turn and owner read, receipts are replayed after supervisor shutdown without restarting recovery, completed receipts stay independent of the physical slot, the exact supervisor and worker are required even when the placement matches, conflicting retries are rejected, stale result writers are rejected, and old receipts are pruned without releasing the warm owner |
| TC-U-workspace | `src/node-host/node-worker-workspace.test.ts`: workspace seeds, admission, and retention | A snapshot without a source workspace, a fresh seed inside and outside its freshness window, an excess seed, and two competing stores of the same repository | A store without an existing source workspace is rejected, a fresh seed is kept and replaced only after its freshness window, old and excess seeds are pruned while recent temporary copies are preserved, a snapshot is stored outside the state directory and replaces the whole workspace on apply, and competing stores of the same repository are serialized across sessions |
| TC-U-auto-update | `src/node-host/auto-update.test.ts`: the automatic node runtime update | An available update, a busy node, a committed runtime pointer, and a Bun registry read in flight | The check runs immediately and hourly without repeatedly staging the installed release, the committed runtime pointer time is used and activation is allowed at exactly twelve hours, the update is staged once while busy and waits for the parent acknowledgement before requesting shutdown, and an in-flight registry read is cancelled when the node stops |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-I-supervisor | `src/node-host/node-worker-supervisor.test.ts`: worker supervision with the durable journal | A node with worker capacity, a worker bundle, and a workspace | A launch is idempotent and only bounded non-secret facts are persisted, two durable launches are admitted and one physical slot is released at a time, saturated admission is aborted when the supervisor closes, the worker is spawned with only the supplied runtime essentials, worker result text is preserved while failure diagnostics are bounded and scrubbed, an encoded credential is redacted across the stderr cutoff, credential scrubbing rotates and prior-turn diagnostics are dropped when a worker is reused, a blocked cancellation write is bounded and stops only its physical owner, a running worker is never signalled for a mismatched immutable cancel identity, an accepted cancellation is preserved when a rejected terminal event needs a journal retry, an out-of-bundle entry fails closed, and each child's admission re-arm reason is replayed after a supervisor restart |
| TC-I-nodes-invoke | `src/gateway/server-methods/nodes.invoke-abort.test.ts` and `src/gateway/server-methods/nodes.invoke-wake.test.ts`: Gateway-side invocation routing, abort, and wake | A paired node, a queued invocation, a cancelled caller, and a sleeping node | The invocation is routed to the node with the timeout and idempotency key, a caller cancellation aborts the invocation, and a queued invocation wakes a sleeping node |
| TC-I-nodes-read | `src/gateway/server-methods/nodes.read.test.ts`: node listing, description, and event handling | A registry with paired and pending nodes | A paired node is listed and described with its capabilities and command surface, and a node event is accepted and projected into the registry |
| TC-I-nodes-event | `src/gateway/server-methods/nodes.event.test.ts`: node-originated event handling | A node event carrying host statistics | The event is accepted, the registry is updated, and the result reports whether the event was handled |
| TC-I-nodes-pending | `src/gateway/server-methods/nodes.pending-work.test.ts`: queued node work | A node with queued work items | The work is drained in a bounded batch, `hasMore` reflects the remaining work, and only the consumed ids are acknowledged |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-E-node-flow | `src/node-host/runner.test.ts` and `src/node-host/invoke.test.ts` combined: connect, pair, invoke, and report | Start the foreground host, approve the pending node request on the Gateway, invoke a command, and let the node report the result | The node advertises only the allowlisted commands, the approval binds the declared surface, the command runs under the node-local policy, and the result reaches the Gateway with stdout, stderr, and the exit code |
| TC-E-worker-hosted-session | `src/node-host/node-worker-supervisor.test.ts` and `src/node-host/node-worker-turn-store.test.ts` combined: host a session, restart, and recover | Launch a worker, run a turn, stop the supervisor, and start it again | The launch and turn receipts are replayed from the journal, the physical slot is preserved for the predecessor, the worker is not launched twice, and the workspace generation is released under the retention policy |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Node-local exec approvals are set to `deny` | The run is refused with `SYSTEM_RUN_DENIED` and no process starts |
| TC-E2 | A Windows `cmd.exe /c` wrapper in allowlist mode | The run is refused and the operator is told to approve the wrapper form |
| TC-E3 | The request environment sets `PATH`, `NODE_OPTIONS`, `PYTHONPATH`, `BASH_ENV`, `DYLD_*`, or `LD_*` | The override is rejected or stripped, and a shell wrapper receives only the allowed environment values |
| TC-E4 | An approval-backed run that cannot pin a stable executable path | The run is refused instead of running an unpinned command |
| TC-E5 | The approved working directory changes between approval and execution | The run is refused and the drift is reported |
| TC-E6 | The approved file operand changes between approval and execution | The run is refused and the drift is reported |
| TC-E7 | The Gateway rejects the connect with a missing token, a mismatched token, an invalid bootstrap token, a missing password, a missing identity header, or a client version mismatch | The foreground host stops with a visible reason instead of retrying forever |
| TC-E8 | The device approval is still pending | The node keeps retrying with exponential backoff capped at 30 seconds and does not stop |
| TC-E9 | A command allowlist names a command that is not available on the node | Startup fails and the node reports which requested command was unavailable |
| TC-E10 | A worker bundle entry resolves outside its namespaced bundle | The launch fails closed and no child process starts |
| TC-E11 | A launch is replayed with a different plan hash | The claim is rejected and the recorded plan is not overwritten |
| TC-E12 | A turn result arrives from a stale writer or a mismatched immutable identity | The write is rejected and the journal keeps the original receipt |
| TC-E13 | The node's worker slots are all in use | The launch waits for a slot and then reports capacity exhaustion rather than exceeding the advertised count |
| TC-E14 | The supervisor closes while an admission is waiting | The waiting admission is aborted and the physical capacity claim is released |
| TC-E15 | A cancellation targets a worker whose immutable identity does not match | The running worker is not signalled |
| TC-E16 | A session requests a directory that is a file, a missing directory, a filesystem root, a directory overlapping the node's private worker storage, or one that escapes a configured root through a symlink | The request is rejected |
| TC-E17 | The node's state directory or a resolved ancestor is group- or world-writable without sticky protection | Session hosting is refused, the node stays connected for its other commands, and the offending path and the remediation are reported |
| TC-E18 | The node is permanently busy when an update is available | The update is staged but not applied, and the node keeps its current runtime |
| TC-E19 | The node is closed while an MCP client or a plugin cleanup is still running | The close waits for the cleanup and reports the failure instead of exiting silently |
| TC-E20 | An encoded credential appears in worker stderr | The credential is scrubbed across the stderr cutoff, and the scrubbing rotates when the worker is reused |

## Test Infrastructure

- Vitest is the test runner for the whole repository. The node-host suites use in-repo fakes for the Gateway connection, the supervisor, the clock, and the filesystem, plus `test/helpers/temp-dir.ts` for temporary directories.
- The launch and turn suites exercise the real SQLite schema from `src/state/openclaw-state-schema.sql`, so the table constraints described in the specification are enforced by the tests rather than mocked.
- The supervisor suite spawns a real worker child process with a test bundle, so the launch, the cancellation, and the credential-scrubbing paths run against a real process.
- The workspace suite uses real Git repositories in a temporary directory, so the seed, the freshness window, and the competing-store serialization are exercised against a real Git implementation.
- The Gateway node suites in `src/gateway/server-methods/` use the shared Gateway test harness with an authenticated context and a connected node.
- No external machine, network access, or real device is required. The Gateway connection is always a test double.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-U-runtime, TC-U-runner, TC-U-runtime-supervisor |
| FR-2 | TC-U-runner, TC-E7, TC-E8 |
| FR-3 | TC-U-runner |
| FR-4 | TC-U-runner, TC-E-node-flow |
| FR-5 | TC-U-runtime, TC-E9, TC-I-nodes-read |
| FR-6 | TC-U-invoke, TC-E-node-flow |
| FR-7 | TC-U-system-run-plan, TC-E4, TC-E5 |
| FR-8 | TC-U-system-run, TC-U-system-run-allowlist, TC-E1, TC-E2 |
| FR-9 | TC-U-system-run, TC-E3 |
| FR-10 | TC-I-supervisor, TC-E10, TC-E13, TC-E14 |
| FR-11 | TC-U-launch-store, TC-U-turn-store, TC-E11, TC-E12 |
| FR-12 | TC-U-workspace, TC-I-supervisor, TC-E16 |
| FR-13 | TC-U-runner, TC-U-auto-update, TC-E18 |
| FR-14 | TC-I-nodes-read, TC-I-nodes-event, TC-I-nodes-pending, TC-E-node-flow |
| NFR-1 | TC-I-supervisor, TC-E20 |
| NFR-2 | TC-U-invoke, TC-E1, TC-E2 |
| NFR-3 | TC-U-runtime, TC-E19 |
| NFR-4 | TC-U-runtime, TC-U-runner |
| NFR-5 | TC-U-runner, TC-E7, TC-E8 |
| NFR-6 | TC-U-workspace, TC-E17 |
