---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25887ffepNV1D64V1LVftJ
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### "Remote path includes full SHA-256" is wrong: only the first 32 hex characters are used
- **Evidence:** `packages/env/src/ssh.ts:379-384` builds the remote path as `pi-env-${sha256.slice(0, 32)}`, that is the first 32 hex characters (128 bits) of the digest, not the full 64-character SHA-256. `packages/env/src/ssh.ts:410-413` computes the full digest and passes it to that function, and the deployed name is asserted in `packages/env/test/ssh.test.ts:35` (`createHash("sha256")...digest("hex").slice(0, 32)`).
- **Artifact says:** Technical Decisions: "| Daemon naming | Remote path includes full SHA-256 | Versions never collide and verification precedes every start |", and the API Contracts row "`deployDaemon` | Upload the matching binary to its SHA-256 named path and verify it".
- **Required change:** State that the remote path carries the first 32 hex characters of the daemon's SHA-256 (128 bits of the digest), while the whole file is verified against the full digest before every start. The same wording fix applies to the `deployDaemon` row.
- **Severity:** blocking

### The TypeScript surface table lists 13 of the 34 exported names
- **Evidence:** `packages/env/src/index.ts:1-32` exports 34 names. The specification's API Contracts table lists 13 (`RemoteExecutionEnv`, `LocalExecutionEnv`, `Connection`, `connectSsh`, `sshConnection`, `scanHostKey`, `acceptHostKey`, `forgetHostKey`, `detectPlatform`, `deployDaemon`, `openTerminal`, `nodePlatform`, `localDaemon`). The 21 missing are `ConnectionOptions`, `RequestOptions`, `Reply`, `RemoteInfo`, `isConnectionLost`, `RemoteError`, `LocalExecutionEnvOptions`, `RemoteExecutionEnvOptions`, `SshTarget`, `SshConnectOptions`, `RemotePlatform`, `SshError`, `HostKeyUnknownError`, `HostKeyChangedError`, `sshArguments`, `packagedDaemon`, `RemoteTerminal`, `TerminalForeground`, `TerminalOptions`, `RemoteWatcher` and `RemoteWatchOptions`. `SshTarget` and `RemotePlatform` have data-model rows in the specification, but the option and result types, the four error classes, `sshArguments` (which FR-3's acceptance criterion depends on) and the whole terminal and watcher surface do not appear anywhere in the artifact.
- **Artifact says:** "The TypeScript surface is:" followed by the 13-row table.
- **Required change:** Extend the table with the missing exports, or state that it is a partial list of the entry points and point at `packages/env/src/index.ts` for the full surface. If it stays partial, add at least the error classes (`RemoteError`, `HostKeyUnknownError`, `HostKeyChangedError`, `SshError`), the transport types (`ConnectionOptions`, `RequestOptions`, `Reply`, `RemoteInfo`, `isConnectionLost`) and the terminal and watcher types, since the acceptance criteria in `requirements.md` depend on them.
- **Severity:** blocking

### The `loginShell` option is not in the contract
- **Evidence:** `packages/env/src/ssh.ts:464-472` defines `SshConnectOptions.loginShell`; `packages/env/src/ssh.ts:475-484` (`launchCommand`) starts the daemon through the remote user's login shell (`exec "$SHELL" -lc 'exec "$0" "$@"'`) when it is set, and `packages/env/src/ssh.ts:482` uses the plain path otherwise. `packages/env/test/ssh.test.ts:221-244` tests both. The specification's "Detect, deploy, connect, execute" sequence and its API table say only "start daemon over ssh".
- **Artifact says:** The sequence has "C->>S: start daemon over ssh" and the API table has no row for the SSH connect options.
- **Required change:** State that the daemon can be started through the remote user's login shell on request, so commands see the environment of `~/.profile` and similar files, and that it is off by default.
- **Severity:** advisory

### The client-side liveness limits are not in the liveness contract
- **Evidence:** `packages/env/src/connection.ts:17` sets `START_TIMEOUT_MS = 60_000` and `:286-289` fails a start that has not answered within it; `packages/env/src/connection.ts:13-15` pings every 5 s and treats 30 s of silence from the daemon as a lost connection (`:301-306`). The daemon's own limits are `PING_INTERVAL` 5 s and `SILENCE_LIMIT_MS` 30_000 (`packages/env/daemon/src/main.rs:37-38`).
- **Artifact says:** The "Cancellation and liveness" sequence only covers the daemon's ping and its 30 s silence exit; the client is not mentioned.
- **Required change:** Add the client's limits to the liveness section: it pings every 5 s, gives up on a silent daemon after 30 s, and abandons a start that has not answered within 60 s, failing the waiting requests with `{ code: "unknown", lost: true }`.
- **Severity:** advisory

## Open questions
- The specification names `packages/env/docs/protocol.md` as the normative wire contract and does not enumerate the operations, so the `ptyForeground` op and the `listFiles` result shape are only documented there. The code cannot say whether the specification is meant to carry a second, partial copy of the operation list.
