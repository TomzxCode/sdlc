---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25887ffepNV1D64V1LVftJ
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The scope says the real-SSH coverage is not run in CI; CI runs it on Windows
- **Evidence:** `.github/workflows/env.yml:189-200` starts Windows' OpenSSH server with an ed25519 key and runs `npx vitest --run test/ssh-external.test.ts` twice, once with cmd.exe as the default shell and once with `PI_ENV_SSH_SHELL=powershell`, on the `windows-latest` runner. The same workflow also runs the Durable env tests (`:165-167`) and the pi-env suite against each shipped release daemon (`:75-126`, with `PI_ENV_DAEMON`).
- **Artifact says:** "| Scope | ... | Real-SSH coverage gated on `PI_ENV_SSH_HOST` documents the manual path and is not run in CI by default. |"
- **Required change:** State that `test/ssh-external.test.ts` runs in CI on the Windows runner against a locally started OpenSSH server, with cmd.exe and then PowerShell as the server's default shell, and that the same workflow runs the Durable env tests and the pi-env suite against the release daemon builds on six platforms.
- **Severity:** blocking

### TC-1 (ssh argument hardening) has no test
- **Evidence:** `sshArguments` (`packages/env/src/ssh.ts:77-120`) is never asserted in any test: `packages/env/test/` contains no reference to `sshArguments`, `BatchMode`, `ForwardAgent` or `ClearAllForwardings`. The hardening is only exercised indirectly by the SSH tests that connect.
- **Artifact says:** "| TC-1 | ssh argument hardening | Any SshTarget | BatchMode on, forwardings off, strict keys against the application file |" and the coverage matrix maps FR-3 and NFR-1 to it.
- **Required change:** Add a unit test that builds the argument list for a target and asserts `BatchMode=yes`, `ClearAllForwardings=yes`, `ForwardAgent=no`, `ForwardX11=no`, `ControlMaster=no`, `RemoteCommand=none`, `PermitLocalCommand=no`, `SendEnv=-*`, `StrictHostKeyChecking=yes`, `UserKnownHostsFile` pointing at the application file, `GlobalKnownHostsFile=none` and `HostKeyAlias`; also assert the rejection of a host that starts with a dash and of a port outside 1 to 65535 (`packages/env/src/ssh.ts:60-86`).
- **Severity:** blocking

### TC-4 (corrupt frame handling) has no test
- **Evidence:** The client tears the connection down on a corrupt frame at `packages/env/src/connection.ts:356-377` (length out of range, unparseable JSON) and the daemon rejects an out-of-range length at `packages/env/daemon/src/frame.rs:57-60`. No test in `packages/env/test/` sends a malformed frame; `grep -rn "corrupt" packages/env/test` returns nothing.
- **Artifact says:** "| TC-4 | corrupt frame handling | Overlong or unparseable frame | Connection torn down with a lost error |", mapped to FR-1 in the coverage matrix.
- **Required change:** Add a test that writes a frame with a length above 16 MiB or below 9 bytes, and one whose JSON does not parse, to a `Connection` over a pipe, and assert that the pending request fails with `{ code: "unknown", lost: true }` and that the next request starts a new daemon.
- **Severity:** blocking

### TC-6 (path resolution) has no test
- **Evidence:** The client resolves `~`, `file://` URLs, relative paths and Windows drive-relative paths at `packages/env/src/remote-env.ts:374-402`. The differential suite only uses relative names (`packages/env/test/differential.test.ts:63-92`, the `NAMES` list) and Durable's conformance suite does not cover `~` or `file://` either. No test asserts the resolved absolute path.
- **Artifact says:** "| TC-6 | path resolution | `~`, `file://`, relative, drive-relative paths | Absolute remote paths under remote path rules |".
- **Required change:** Add cases for `~`, `~/<name>`, a `file://` URL, a relative path resolved against `cwd`, and (on Windows) a drive-relative path resolved against the daemon's `=D:` working directory, comparing the resolved path with `NodeExecutionEnv`'s resolution of the same input.
- **Severity:** blocking

### TC-16 and TC-17 (deploy failure modes) have no test
- **Evidence:** The upload removes the temporary file and fails when the hash does not match (`packages/env/src/ssh.ts:443-458` for POSIX, `:417-441` for Windows), and a remote without `sha256sum`, `shasum` or `openssl` is refused with "has no sha256sum, shasum or openssl to verify pi-env" (`packages/env/src/ssh.ts:388-398` returns `nohash`, `:416` throws). No test injects a corrupt upload or a remote without hash tools. The nearest test, `packages/env/test/ssh.test.ts:155-169`, covers a tampered file that is already deployed, not a corrupt upload or a missing hash tool.
- **Artifact says:** "| TC-16 | Daemon upload corruption | Hash mismatch removes the temp file and fails the deploy |" and "| TC-17 | Remote without hash tools | Deploy refused with a no-verification error |".
- **Required change:** Add a case that corrupts the bytes in flight (or points `deployDaemon` at a binary that differs from the hash the remote computes) and asserts that the remote tool directory keeps no temporary file and that the deploy fails; add a case that runs the check on a host whose PATH has no hash tool and asserts the refusal.
- **Severity:** blocking

### TC-18 and TC-19 (banner tolerance and watch reconnect) have no test
- **Evidence:** The client discards everything before the `PI-ENV <token>` sync line and reports the noise through `onLog` (`packages/env/src/connection.ts:340-355`), and `RemoteWatcher` reopens the daemon's watcher after a lost connection and then reports `overflow` (`packages/env/src/watch.ts:133-157`). No test prints a banner before the sync line, and no test kills the daemon under a live watcher; Durable's conformance suite has watch cases but no reconnect case (`packages/durable/src/testing/env-conformance.ts:275-386`).
- **Artifact says:** "| TC-18 | Shell banner on stdout | Bytes before the `PI-ENV` sync line are discarded |" and "| TC-19 | Watch reconnect | Watcher reopens on the new daemon and reports `overflow` |".
- **Required change:** Add a test that starts a stand-in daemon which prints a banner before the sync line (the pattern `packages/env/test/old-daemon.ts:7` already shows) and asserts that the connection still works and that the banner reaches `onLog`; add a test that opens a watcher, kills the daemon, restarts it and asserts that the watcher reports `overflow` and keeps reporting changes afterwards.
- **Severity:** blocking

### The coverage matrix points FR-7 and NFR-4 at the wrong cases
- **Evidence:** FR-7 (the bounded listing with its `truncated` flag) is mapped to TC-10, which is the old-daemon fallback, not the listing bounds. The actual coverage is `packages/env/test/remote.test.ts:94-110` (10 100 entries listed, then `maxEntries: 5000` with `truncated: true`), `packages/env/test/ssh.test.ts:188-219` (the listing over SSH, equal to the local one), and Durable's conformance cases "listFiles stops at its bounds and reports truncated" (`packages/durable/src/testing/env-conformance.ts:544`) and "listFiles skips what git ignores in work trees, .git, and excluded names" (`:521`). NFR-4 (windowed, paced output) is mapped to TC-8, which runs random file-operation sequences, not command output; the actual coverage is `packages/env/test/remote.test.ts:28-57` and the conformance case "windowed exec keeps the exact tail and counts what it skips" (`packages/durable/src/testing/env-conformance.ts:438`).
- **Artifact says:** "| FR-7 | TC-10 |" and "| NFR-4 | TC-8 |" in the Coverage Matrix, and "TC-10 | old daemon fallback | ... `not_supported` error and caller-side walk" in the Integration Tests table.
- **Required change:** Give FR-7 and NFR-4 their own cases in the Integration Tests table (bounded listing with the `truncated` flag, and windowed output with exact skipped counts) and map them in the matrix. FR-7 and NFR-4 currently have no case of their own.
- **Severity:** blocking

### The plan does not mention the daemon's Rust unit tests
- **Evidence:** `cargo test --locked` runs 13 unit tests inside the daemon sources, and `.github/workflows/env.yml:154-159` runs them on every one of the five CI operating systems: `packages/env/daemon/src/frame.rs:101` (frame round trip), `decode.rs:46` (3 tests), `list.rs:170` (5 tests, including the gitignore rules and the bounds), `scan.rs:179` (1), `window.rs:206` (2) and `sys/windows.rs:648` (1). The plan's "Test files present" row names only the six TypeScript test files.
- **Artifact says:** "| Test files present | `conformance.test.ts`, `differential.test.ts`, `remote.test.ts`, `ssh.test.ts`, `terminal.test.ts`, `ssh-external.test.ts`. |"
- **Required change:** List the daemon's Rust unit tests as part of the plan, with the cases they cover: frame round trip and out-of-range length, the WHATWG UTF-8 decoder, the `listFiles` gitignore and exclude rules and its bounds, the line scanner, and the output window.
- **Severity:** blocking

### The plan does not record the release-build matrix the workflow runs
- **Evidence:** `.github/workflows/env.yml:75-126` runs the whole pi-env suite against each shipped release daemon (`PI_ENV_DAEMON`) for linux-x64, linux-arm64, darwin-arm64, darwin-x64, windows-x64 and windows-arm64, and `:59-72` checks the packed npm file list (the eight `bin/pi-env-<platform>-<arch>/pi-env` binaries and `docs/protocol.md`). The plan's Test Infrastructure section mentions only that `PI_ENV_DAEMON` overrides the binary under test, and the same workflow also runs Durable's env tests (`:165-167`).
- **Artifact says: | Test Infrastructure | ... `test/daemon.ts` spawns the daemon over a pipe; `PI_ENV_DAEMON` overrides the binary under test. |"
- **Required change:** State that the release builds are tested as shipped on six platforms, that the packed npm file list is checked, and which Durable env test files the workflow runs as the parity baseline.
- **Severity:** advisory

### `old-daemon.ts` is described as a pinned daemon; it is a stand-in
- **Evidence:** `packages/env/test/old-daemon.ts:1-5` is a Node script that answers `hello` without `features` and refuses every other operation as unknown. No released daemon is pinned or downloaded.
- **Artifact says:** "`test/old-daemon.ts` pins the pre-`listFiles` daemon for fallback coverage."
- **Required change:** Say that `test/old-daemon.ts` simulates a daemon released before `hello.features`, so the `not_supported` path is covered without an old binary.
- **Severity:** advisory

## Open questions
- The plan does not say whether the 30 second silence limit of the daemon (NFR-3) is meant to be covered by a test; such a test would take over 30 seconds. The code has no seam to shorten the limit, so this is a deliberate choice to make explicit.
