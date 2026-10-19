---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25887ffepNV1D64V1LVftJ
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### File watching is not a requirement at all
- **Evidence:** `packages/env/src/remote-env.ts:827-850` implements `ExecutionEnv.watch` over the daemon's `watch` op; `packages/env/src/watch.ts:23-157` is `RemoteWatcher`, a reconnecting watcher that reports `overflow` after a lost connection (`packages/env/src/watch.ts:133-157`); `packages/env/daemon/src/watch.rs` (778 lines) is a port of Durable's `NodeFileWatcher` that runs next to the files; `packages/env/src/index.ts:32` exports `RemoteWatcher` and `RemoteWatchOptions`. Durable's env conformance suite exercises the watch contract against `RemoteExecutionEnv` (`packages/durable/src/testing/env-conformance.ts:275-386`, registered by `packages/env/test/conformance.test.ts:17-31`).
- **Artifact says:** FR-1 to FR-10 cover the daemon, SSH hardening, host-key trust, lazy start, parity, `listFiles`, terminals, old-daemon fallback and `LocalExecutionEnv`. None of them mentions watching, and neither do the NFRs or the acceptance criteria.
- **Required change:** Add a requirement for the watch contract (Should): the daemon runs Durable's `NodeFileWatcher` next to the files, native events only trigger a rescan, the client reconnects the watcher on a new daemon and reports `overflow`, and the daemon-side `watch` op streams `ready`, `change` and `error` events. Add the matching acceptance criterion and cover it in the coverage matrix.
- **Severity:** blocking

### FR-8 omits the terminal's foreground job reporting
- **Evidence:** `packages/env/src/terminal.ts:77-82` (`RemoteTerminal.foreground()`) asks the daemon for the terminal's foreground process group; the daemon answers with the `ptyForeground` op (`packages/env/daemon/src/main.rs:411-425`, `packages/env/daemon/src/pty.rs:125-142`); the client type is `TerminalForeground` (`packages/env/src/terminal.ts:21-23`) and is exported at `packages/env/src/index.ts:31`. The wire contract is `packages/env/docs/protocol.md:148-151`.
- **Artifact says:** "| FR-8 | Should | The system shall run interactive programs in a daemon pseudo-terminal (`openTerminal`), reporting raw output, input, resize, and exit code. |"
- **Required change:** Extend FR-8 to state that the terminal also reports the job in the foreground (its process group id and the leader's name, absent while the program itself is in front), and that the call fails with `EBADF` once the terminal has ended. Add the acceptance criterion for it.
- **Severity:** blocking

### NFR-4 does not state the output spill
- **Evidence:** `packages/env/src/remote-env.ts:898` sends the `spill` option and `:926`/`:941` carry `spillPath` back; the daemon writes the complete raw output to `pi-output-<uuid>.log` in a fresh `tmp-` directory once the output crosses `spill.afterBytes` or `spill.afterLines` (`packages/env/daemon/src/exec.rs:129-189`); `packages/env/docs/semantics.md:59-60` states the rule.
- **Artifact says:** "| NFR-4 | Should | Performance | The system shall bound frames at 16 MiB, pace command output through windows, and answer control frames ahead of bulk data. |" Spill is not mentioned.
- **Required change:** State the spill behaviour in NFR-4 (or a new Should requirement): the complete raw output is preserved to a file once the thresholds are crossed, and the path is reported with the result and with a timeout or abort failure.
- **Severity:** advisory

### Every acceptance criterion is unchecked while the feature is marked done
- **Evidence:** `packages/env/requirements.md` has `status: done` in its frontmatter, and all fourteen acceptance criteria under FR-1 to NFR-4 are `- [ ]`. The same repository's `packages/durable`-derived features (`p7-durable-runtime`, `p8-chord-composition-runtime`, `p9-telemetry-contracts`) tick theirs.
- **Artifact says:** The acceptance criteria list is unticked while the frontmatter says the feature is done.
- **Required change:** Tick the criteria that the test suite and the implementation now satisfy, and leave the untested ones (see `review-tests.md`) unticked, or state which criterion proves each one.
- **Severity:** advisory

## Open questions
- The Open Questions section still asks "Which remote systems beyond Linux, macOS, Android Termux, and Windows must be supported before this feature is declared complete" while the artifact is `status: done` and the supported set is fixed by the release build matrix (`.github/workflows/env-daemons.yml:22-31`: linux, android, darwin, windows on x64 and arm64). The code cannot answer whether further systems are planned.
