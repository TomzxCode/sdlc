---
title: "Remote Execution Env"
status: done
session_link: "none"
---

# Requirements: Remote Execution Env

## Overview

Agents need their tools to run on a remote machine, usually reached over SSH, while the Durable worker, its storage, and its credentials stay local.
This feature provides a Rust daemon that runs on the remote machine plus a Durable `ExecutionEnv` client (`RemoteExecutionEnv`) that talks to it through a lazily started `Connection`.
`LocalExecutionEnv` reuses the same daemon on the local machine so local and remote file listings share one implementation.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agent runtime (Durable) | Runs tools against any `ExecutionEnv` without knowing whether it is local or remote |
| Machine owner | Accepts host keys out of band and deploys a verified daemon to their remote machines |
| Daemon operator | Debugs remote failures from daemon diagnostics and client error codes |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall run a daemon on the remote machine that performs file operations and commands there over a framed protocol on stdin and stdout (`docs/protocol.md`). |
| FR-2 | Must | The system shall detect the remote system (Linux, macOS, Android Termux, Windows on x86-64 and arm64), deploy the matching daemon binary when missing or changed, and verify it by SHA-256 before every start. |
| FR-3 | Must | The system shall connect over the system `ssh` with strict host-key checking against the application's own known-hosts file under a fixed alias, with no forwarding, no shared connections, and no locale forwarding. |
| FR-4 | Must | The system shall require explicit host-key trust: `scanHostKey` shows fingerprints for out-of-band comparison, `acceptHostKey` records them, and a changed key is never accepted automatically. |
| FR-5 | Must | The system shall start the connection lazily on the first operation and retry the next operation after a failure; a lost connection fails in-flight requests and a new daemon starts on the next request. |
| FR-6 | Must | The system shall make `RemoteExecutionEnv` results match `NodeExecutionEnv` running on the remote machine, with only error messages allowed to differ (`docs/semantics.md`). |
| FR-7 | Must | The system shall list the file tree below a directory in the daemon (`listFiles`, bounded by `maxEntries`, `maxBytes`, `timeoutMs` with a `truncated` flag), skipping `.git`, excluded names, and git-ignored entries without following symbolic links. |
| FR-8 | Should | The system shall run interactive programs in a daemon pseudo-terminal (`openTerminal`), reporting raw output, input, resize, and exit code. |
| FR-9 | Should | The system shall report older daemons that lack `listFiles` as `not_supported` via `hello.features` so callers fall back to their own walk. |
| FR-10 | May | The system shall provide `LocalExecutionEnv` (`NodeExecutionEnv` plus daemon-backed `listFiles` on the same machine) for local sessions. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall never forward agents, X11, or local commands, never run `ssh` with prompts (`BatchMode`), and never start a daemon whose hash was not verified. |
| NFR-2 | Must | Compatibility | The system shall support Linux, macOS, Android (Termux), and Windows on x86-64 and arm64, including Windows string commands through Git Bash. |
| NFR-3 | Should | Reliability | The system shall kill every remote process group it started and exit the daemon after 30 seconds without receiving bytes or when stdin ends. |
| NFR-4 | Should | Performance | The system shall bound frames at 16 MiB, pace command output through windows, and answer control frames ahead of bulk data. |

## Constraints

- The daemon is a Rust program shipped per supported remote system in `bin/`.
- There is no HTTP surface; the only wire contract is the framed stdio protocol in `docs/protocol.md`.
- Windows terminals are not supported yet.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: daemon serves file operations over stdio
      Given a built daemon binary started with serve and a token
      When the client sends framed hello and lstat requests
      Then the daemon answers with its info and file metadata
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: missing daemon is deployed and verified
      Given an SSH target whose remote tool directory lacks the current daemon
      When connectSsh runs detection and deployment
      Then the daemon at the SHA-256 named path matches the shipped binary before it starts
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: ssh runs hardened
      Given any SshTarget
      When sshArguments builds the command line
      Then BatchMode is on, all forwardings are off, and host keys resolve only against the application known-hosts file
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: unknown host key blocks connection until accepted
      Given a target whose key is not in the known-hosts file
      When the client connects
      Then it fails with HostKeyUnknownError and succeeds only after scanHostKey fingerprints are accepted
    ```

    ```gherkin
    @FR-4
    Scenario: changed host key is refused
      Given a target whose presented key differs from the trusted key of the same type
      When acceptHostKey is called with the new lines
      Then it rejects with HostKeyChangedError until forgetHostKey removes the old keys
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: lazy connection retries after failure
      Given an sshConnection with no network on first use
      When the first operation fails and the network returns
      Then the next operation detects, deploys, and connects without recreating the env
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: remote results match NodeExecutionEnv
      Given the same operation sequence against RemoteExecutionEnv and NodeExecutionEnv
      When the differential suite compares them
      Then results match except error message text
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: bounded listing with truncation flag
      Given a directory tree larger than maxEntries
      When listFiles runs with a small maxEntries limit
      Then it returns the first entries with truncated true
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: interactive terminal echoes and exits
      Given a connection to a POSIX daemon
      When openTerminal runs the login shell and sends input
      Then raw output streams back and the exit code is reported on completion
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: old daemon falls back
      Given a daemon whose hello features lack listFiles
      When listFiles is called
      Then it fails with not_supported so the caller walks the tree itself
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: local env lists through local daemon
      Given a LocalExecutionEnv with a connection to localDaemon
      When listFiles runs on a local directory
      Then entries match the daemon implementation used by remote envs
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: no forwarding or prompts in ssh invocation
      Given the ssh argument builder
      When any connection command is produced
      Then ForwardAgent, ForwardX11, and PermitLocalCommand are disabled and BatchMode is enabled
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: platform matrix detected
      Given reachable Linux, macOS, Android, and Windows targets in both architectures
      When detectPlatform probes each
      Then each reports its platform, arch, and home correctly
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: dropped connection stops remote commands
      Given running remote commands with their output
      When the client stops sending bytes for 30 seconds
      Then the daemon kills every process group it started and exits
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: large output is paced not lost
      Given a command producing output beyond the window
      When it runs with a window configured
      Then coalesced output arrives with skipped accounting and control replies are not starved
    ```

## Conflicts

None identified yet.

## Open Questions

1. Which remote systems beyond Linux, macOS, Android Termux, and Windows must be supported before this feature is declared complete.
2. Whether Windows pseudo-terminal support has a required delivery date or stays out of scope indefinitely.
