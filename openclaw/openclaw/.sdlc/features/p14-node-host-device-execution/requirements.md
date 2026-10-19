---
title: "Node Host and Device Execution"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Node Host and Device Execution

## Overview

Some work has to happen on a machine the Gateway does not own: a build agent in a server room, a phone, a laptop with the repository already checked out, a disposable cloud box. This feature provides the OpenClaw side of that relationship. A node host process runs on the remote machine, connects to the Gateway as a node, advertises the commands and capabilities it actually has, and executes only what the Gateway authorizes. The TypeScript node host in `src/node-host/` ships a foreground runner (`src/node-host/runner.ts`), a private JSONL entry point for the macOS companion app (`src/node-host/worker.ts`), a transport-independent runtime (`src/node-host/runtime.ts`) that both share, the `node.invoke` command surface including `system.run` with an approval plan and an allowlist, a supervisor that hosts agent sessions as worker children, workspace staging with git, quiescence, and retention, and an automatic runtime update path. The node keeps its own durable journal in the shared SQLite database so a restart does not lose track of a worker it launched.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Machine owner | Runs one command to start a node, gets a self-reconnecting host, and keeps the machine's own approval policy |
| Gateway operator | Sees the node's declared command surface, approves it, and can invoke commands on it |
| Agent runtime | Wants `system.run` to run on a named machine under a plan that was approved for that exact command, directory, and file |
| Security reviewer | Wants node-local exec approvals, a closed command surface, and no secret in the node's logs, journal, or launch arguments |
| Node operator running a service | Wants the node installed as a service that survives a reboot and updates itself without losing its pairing |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a foreground node host entry point (`openclaw node run`) and a private JSONL entry point for the macOS app, and both shall use the same transport-independent runtime so the command surface, the plugin registry, and the worker supervisor have one implementation. |
| FR-2 | Must | The system shall connect to the Gateway WebSocket in the node role with a declared protocol range, a client identity, the node's declared commands, and the node's capabilities, and shall reconnect with exponential backoff capped at 30 seconds while device approval is pending. |
| FR-3 | Must | The system shall resolve Gateway credentials from the paired device token, from the saved node configuration, or from the environment, and shall select the environment credentials explicitly when `--auth-from-env` is passed instead of the paired device token. |
| FR-4 | Must | The system shall keep the node's client instance id, display name, and Gateway connection metadata in the shared SQLite machine state, keep the signed device keypair in the device identity row, and keep the paired device auth tokens in the device auth token rows, and shall use the cryptographic device id for pairing and routing rather than the client instance id. |
| FR-5 | Must | The system shall advertise only the commands that are both available on the node and present in the node's command allowlist, together with the capabilities those commands require, and shall fail startup when no requested command is available. |
| FR-6 | Must | The system shall execute the commands the Gateway invokes on the node, including `system.run`, `system.which`, `system.run.prepare`, `system.execApprovals.get`, and `system.execApprovals.set`, and shall return stdout, stderr, and the exit code in the result payload. |
| FR-7 | Must | The system shall prepare an approval plan for an approval-backed `system.run` that binds the exact working directory and the exact executable path, shall revalidate that binding immediately before execution, and shall refuse the run when no stable executable path can be pinned. |
| FR-8 | Must | The system shall enforce node-local exec approvals with the security modes `deny`, `allowlist`, and `full` and the ask modes `off`, `on-miss`, and `always`, shall answer an unauthorized request with `SYSTEM_RUN_DENIED` rather than running it, and shall evaluate an allowlist command against the approved argv and the shell wrapper that will actually carry it, refusing a wrapper form that is not itself allowlisted. |
| FR-9 | Must | The system shall reject or strip unsafe environment overrides on a node run, including `PATH` overrides and interpreter or shell startup variables such as `NODE_OPTIONS`, `PYTHONPATH`, `BASH_ENV`, `DYLD_*`, and `LD_*`, and shall reduce shell-wrapper environment values to an explicit allowlist. |
| FR-10 | Must | The system shall host agent sessions as worker children through a supervisor that owns turn admission, cancellation, workspace custody, and capacity accounting, and shall refuse a launch whose bundle entry resolves outside its namespaced bundle. |
| FR-11 | Must | The system shall persist each worker launch in `node_worker_launches` and each worker turn in `node_worker_turns` with the plan hash, the supervisor pid and process start time, the worker pid and start time, and a terminal state, and shall reject a replayed launch whose plan hash differs from the recorded one. |
| FR-12 | Must | The system shall stage session workspaces under node-owned storage, apply a repository seed when one exists, require workspace quiescence before a capture, retain or delete workspace generations under an explicit retention policy, and enforce the node's existing-folder consent list so that a selected directory which is a file, a missing directory, a filesystem root, a directory overlapping the node's private worker storage, or a directory that escapes a configured root through a symlink is rejected. |
| FR-13 | Should | The system shall install the node host as a service on launchd, systemd, and the Windows task scheduler with `openclaw node install|status|start|restart|stop|uninstall`, and shall check for a node runtime update hourly, defer the update until the node has no local or worker work in flight, apply an update at most once every 12 hours, and honour `nodeHost.autoUpdate.enabled: false`, `update.checkOnStart: false`, and `OPENCLAW_NO_AUTO_UPDATE`. |
| FR-14 | Should | The system shall expose the Gateway-side node surface: pairing request list, approve, reject, and remove, node rename, node list, node describe, plugin surface refresh, plugin tool update, and skill update over the `node.*` RPC methods, shall accept node-originated events such as presence, host statistics, and desktop availability, and shall deliver queued node work to a node that drains a bounded batch, acknowledges the consumed ids, and reports whether more work remains. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The node shall never write a paired device token, a Gateway token, a password, or an approval secret into its log, its journal, its launch arguments, or its worker child environment, and shall scrub an encoded credential from worker diagnostics. |
| NFR-2 | Must | Security | The node's exec approvals and the Gateway's command policy shall be separate gates, and a command allowed by one shall still be subject to the other. The `nodes invoke` CLI path shall not expose `system.run` or `system.run.prepare`, which stay on the exec path. |
| NFR-3 | Must | Reliability | The node host shall wait for plugin availability watchers and active computer executions to finish cleanup during shutdown and shall report the failures from that cleanup instead of exiting silently. |
| NFR-4 | Must | Maintainability | The node runtime shall be transport-independent, so the foreground runner and the private app worker share one implementation and a transport change does not fork the command surface. |
| NFR-5 | Should | Availability | A terminal connect failure (a missing or mismatched token, an invalid bootstrap token, a missing or mismatched password, a missing identity header, or a client version mismatch) shall stop the foreground host with a visible reason, and a pending pairing shall keep the host retrying instead of stopping it. |
| NFR-6 | Should | Security | The node shall refuse to host sessions when its state directory or a resolved ancestor is group- or world-writable without sticky protection, and shall report the offending path and the remediation instead of changing the permissions itself. |

## Constraints

- The node host owns the machine it runs on. It does not decide session placement; the Gateway does. A node advertises what it can do and executes what the Gateway authorizes.
- The Gateway forwards the stored approval plan, not a caller-edited command, working directory, or session field, once an approval has been granted.
- Node-local exec approvals live in the node's own SQLite `exec_approvals_config` row. The Gateway's `gateway.nodes.commands.allow` policy is a separate gate that the node cannot widen.
- The command allowlist is durable node machine state. Omitting it on a later start keeps the saved list, and `--all-commands` removes it.
- The node host does not change ancestor filesystem permissions. A session-host staging failure is reported, not repaired.
- The node keeps its own launch and turn journal. The Gateway keeps the transcript and the session records.
- The `system.run` result carries stdout, stderr, and the exit code. Output is truncated with a visible marker rather than silently cut.
- An explicit command allowlist disables computer use, skill scanning and publication, plugin-tool publication, MCP servers, and worker hosting for that node.
- The Rust node host in `crates/` is a separate implementation tracked as FEAT-p11. This feature covers the TypeScript node host only.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: both entry points share one runtime
      Given the foreground runner and the private app worker
      When each prepares its runtime
      Then both resolve the same command surface, plugin registry, and worker supervisor implementation
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: node connects and retries while approval is pending
      Given a node whose device request is awaiting approval
      When the node connects
      Then it advertises its commands and capabilities and retries with exponential backoff capped at 30 seconds
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: environment auth is selected explicitly
      Given a node with a paired device token and OPENCLAW_GATEWAY_TOKEN set
      When the node starts with --auth-from-env
      Then the environment credentials are used instead of the paired token, and the choice is reported on stderr
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: identity and pairing are separate records
      Given a node with a stored client instance id, a signed device keypair, and a paired device token
      When the Gateway pairs and routes to the node
      Then the cryptographic device id is used for pairing and routing, and the client instance id is only connection metadata
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: the advertised surface is the intersection
      Given a node with a command allowlist naming one available command and one unavailable command
      When the node advertises its surface
      Then only the available allowlisted command is advertised, and startup fails when no requested command is available
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: system command results carry the process outcome
      Given an authorized system.which request
      When the node runs the command
      Then the result payload carries stdout, stderr, and the exit code
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: approval binds the working directory and executable
      Given an approval-backed system.run that omits the working directory
      When the node prepares the approval plan
      Then the plan captures the execution host working directory and pins the resolved executable path
      And the run is refused when no stable executable path can be pinned
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: local exec approvals gate the run
      Given node-local exec approvals with security deny
      When a system.run request arrives
      Then the run is refused with SYSTEM_RUN_DENIED and no process is started
      And an allowlist mode run whose shell wrapper is not itself allowlisted is refused as well
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: unsafe environment input is rejected
      Given a system.run request whose env map sets PATH or a shell startup variable
      When the node prepares the run
      Then the request is refused or the override is stripped, and a shell wrapper receives only the allowed environment values
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: the supervisor refuses an out-of-bundle entry
      Given a worker launch whose bundle entry resolves outside its namespaced bundle
      When the supervisor starts the launch
      Then the launch fails closed and no child process is started
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: a replayed launch with a different plan is rejected
      Given a recorded launch with a stored plan hash
      When the same launch id is claimed again with a different plan hash
      Then the claim is rejected
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: workspace capture waits for quiescence and honors consent
      Given a session workspace with a running process
      When a capture is requested
      Then the capture waits for the workspace quiescence lease and only then captures the manifest
      And a selected directory that escapes a configured root through a symlink is rejected
    ```

- [x] **FR-13**

    ```gherkin
    @FR-13
    Scenario: the node is installed as a service and updates when idle
      Given a supported platform with an available node runtime update
      When the operator runs openclaw node install and the update check runs
      Then the service definition is written for that platform's supervisor, the install reports the package version, the chosen runtime, and the service command, and the update is staged but not applied until the node is idle
    ```

- [x] **FR-14**

    ```gherkin
    @FR-14
    Scenario: pairing requests are approved explicitly and events are accepted
      Given a node that has submitted a command surface and queued node work
      When the operator approves the request, the node reports presence, and the node drains the queued work
      Then the approval binds the declared surface, a later expansion creates a new approval request, the presence event reaches the Gateway, and the node acknowledges only the ids it consumed
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: secrets never reach a log or a child
      Given a node with a paired device token and a worker launch
      When the node logs, journals, and starts the worker child
      Then no token, password, or approval secret appears in the log, the journal, the launch arguments, or the child environment
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: the two gates are independent
      Given a command allowed by the Gateway command policy but denied by node-local exec approvals
      When the command is invoked
      Then it is refused by the node's own approvals
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: shutdown waits for cleanup
      Given a node with a plugin availability watcher and an active computer execution
      When the node shuts down
      Then it waits for both to finish cleanup and reports a cleanup failure instead of exiting silently
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: the runtime is transport-independent
      Given a change to the transport used by the foreground runner
      When the private app worker is exercised
      Then it keeps the same command surface and supervisor behavior without a separate implementation
    ```

- [x] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: terminal connect errors stop the host
      Given the Gateway rejects the connect with a missing token or a client version mismatch
      When the node host handles the rejection
      Then it stops with a visible reason instead of retrying forever
    ```

- [x] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: unsafe workspace ancestors block session hosting
      Given a node whose state directory has a world-writable ancestor without sticky protection
      When session hosting is prepared
      Then hosting is refused, the node stays connected for other commands, and the offending path and the remediation are reported
    ```

## Conflicts

None identified yet.

## Open Questions

1. The command allowlist disables computer use, skill publication, plugin-tool publication, MCP servers, and worker hosting as a single switch. Should those be separable so a node can publish sessions without exposing execution, without an all-or-nothing allowlist?
2. Node-local exec approvals default to `full` with `ask: "off"`, which is broad for a freshly installed node. Should a node installed through a one-paste setup link default to a narrower mode, and how would an operator widen it later without reinstalling?
3. The automatic node update applies at most once every 12 hours and only when the node is idle. A permanently busy node therefore never updates. Should there be a maximum deferral after which the operator is warned?
