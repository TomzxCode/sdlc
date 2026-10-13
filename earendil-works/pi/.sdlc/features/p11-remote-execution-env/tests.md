---
title: "Remote Execution Env"
status: done
session_link: "none"
---

# Test Plan: Remote Execution Env

## Scope

The framed stdio protocol, the SSH detection and deployment flow, `RemoteExecutionEnv` parity with `NodeExecutionEnv`, `listFiles`, terminals, and watching are in scope.
Real-SSH coverage gated on `PI_ENV_SSH_HOST` documents the manual path and is not run in CI by default.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | ssh argument hardening | Any SshTarget | BatchMode on, forwardings off, strict keys against the application file |
| TC-2 | host-key line parsing | Scanned known-hosts lines | Plain alias lines accepted, markers and patterns rejected |
| TC-3 | frame codec round trip | Request, result, error, event, cancel, ping frames | Parsed id, JSON, and payload match what was written |
| TC-4 | corrupt frame handling | Overlong or unparseable frame | Connection torn down with a lost error |
| TC-5 | error code mapping | Daemon error codes | Client `FileError` codes match `NodeExecutionEnv` mapping |
| TC-6 | path resolution | `~`, `file://`, relative, drive-relative paths | Absolute remote paths under remote path rules |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | conformance suite over piped daemon | Debug daemon binary or `PI_ENV_DAEMON` | Durable env conformance suite passes against `RemoteExecutionEnv` |
| TC-8 | differential operation sequences | Same-machine daemon | Random sequences match `NodeExecutionEnv` except error messages |
| TC-9 | Durable tools comparison | Same-machine daemon | Tool results match `NodeExecutionEnv` |
| TC-10 | old daemon fallback | Daemon without `listFiles` feature | `not_supported` error and caller-side walk |
| TC-11 | terminal session | POSIX daemon | `terminal.test.ts` input, resize, and exit code behavior |
| TC-12 | reconnect semantics | Killed daemon mid-request | In-flight requests fail lost, next request starts a new daemon, stale handles fail |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-13 | SSH deploy and execute | `PI_ENV_SSH_HOST` set, trusted host key | Detect, deploy, connect, and run the suite over a real SSH server |
| TC-14 | lazy connection recovery | Unreachable target, then reachable | First op fails with its diagnostics, next op connects |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-15 | Changed host key | `HostKeyChangedError`, never auto-accepted |
| TC-16 | Daemon upload corruption | Hash mismatch removes the temp file and fails the deploy |
| TC-17 | Remote without hash tools | Deploy refused with a no-verification error |
| TC-18 | Shell banner on stdout | Bytes before the `PI-ENV` sync line are discarded |
| TC-19 | Watch reconnect | Watcher reopens on the new daemon and reports `overflow` |

## Test Infrastructure

- `test/daemon.ts` spawns the daemon over a pipe; `PI_ENV_DAEMON` overrides the binary under test.
- `test/old-daemon.ts` pins the pre-`listFiles` daemon for fallback coverage.
- `test/ssh-external.test.ts` runs the suite over a real SSH server when `PI_ENV_SSH_HOST` is set.
- Test files present: `conformance.test.ts`, `differential.test.ts`, `remote.test.ts`, `ssh.test.ts`, `terminal.test.ts`, `ssh-external.test.ts`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-4, TC-7 |
| FR-2 | TC-13 |
| FR-3 | TC-1 |
| FR-4 | TC-2, TC-15 |
| FR-5 | TC-12, TC-14 |
| FR-6 | TC-7, TC-8, TC-9 |
| FR-7 | TC-10 |
| FR-8 | TC-11 |
| FR-9 | TC-10 |
| FR-10 | TC-7 |
| NFR-1 | TC-1 |
| NFR-2 | TC-13 |
| NFR-3 | TC-12 |
| NFR-4 | TC-8 |
