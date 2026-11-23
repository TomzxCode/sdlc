---
title: "Process Daemon / PTY Service"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Test Plan: Process Daemon / PTY Service

## Scope

The Rust daemon and library under `packages/process-daemon`, the `@opencode/pty` wrapper, and the OpenCode integration that talks to the daemon.
Coverage includes framing and validation, ownership and handoff, terminal actors, pipe processes, transports, native callback ownership, CLI behavior, CI checks, and release packaging.

## Unit Tests

These tests live beside the Rust implementation and run with `cargo test --locked` from `packages/process-daemon`.

| File | Tests | Description |
|---|---|---|
| `packages/process-daemon/src/protocol.rs` | 7 | Protocol 9 version and features, request and response round trips, strict fields, unknown requests |
| `packages/process-daemon/src/ownership.rs` | 6 | Exclusive acquisition, acquisition timeout, non-renewing handoff, ticket consumption, generation fencing, expiry, deadlines |
| `packages/process-daemon/src/service.rs` | 26 | Terminal registry, actors, replay bounds, snapshots, rows, titles, foreground process, subscriptions, lifecycle |
| `packages/process-daemon/src/service/pipe.rs` | 1 | Newline counting on a partial output file write |
| `packages/process-daemon/src/service/pipe/windows.rs` | 8 | Windows pipe process spawn, job handling, signals, and output paths |
| `packages/process-daemon/src/daemon.rs` | 2 | Runtime root resolution and registration helpers |
| `packages/process-daemon/src/daemon/server.rs` | 19 | Request dispatch, token checks, owner gating, subscription delivery, and shutdown behavior |
| `packages/process-daemon/src/daemon/sweep.rs` | 3 | Stale runtime sweep decisions and liveness checks |
| `packages/process-daemon/src/daemon/unix.rs` | 8 | Socket paths, private directories, atomic registration, cleanup, and stale endpoint removal |
| `packages/process-daemon/src/daemon/windows.rs` | 2 | Windows runtime directory and registration behavior |
| `packages/process-daemon/src/transport/unix.rs` | 7 | Unix listener, wake, cancellation, and response completion |
| `packages/process-daemon/src/transport/windows.rs` | 7 | Named-pipe accept, connect, overlapped I/O, and retained final frames |
| `packages/process-daemon/src/transport/windows/security.rs` | 1 | Windows ACL and owner checks |
| `packages/process-daemon/src/ghostty/tests.rs` | 4 | Actor-local native terminal, callback ownership, formatted buffers, callback panics |
| `packages/process-daemon/src/client.rs` | 1 | Registration discovery and protocol mismatch rejection |
| `packages/process-daemon/src/musl.rs` | 1 | musl-specific behavior |

## Integration Tests

These tests spawn daemons, children, or the CLI and run with `cargo test --locked` from `packages/process-daemon`.

| File | Tests | Platform | Description |
|---|---|---|---|
| `packages/process-daemon/tests/service.rs` | 12 | Unix | Resize reports, controller takeover, independent terminals, bounded replay, titles, foreground process, slow observers |
| `packages/process-daemon/tests/ownership.rs` | 12 | Unix | Owner loss, final exit frames, handoff, single ticket winner, timeout, socket replacement, stop cleanup, pipe survival |
| `packages/process-daemon/tests/pipe.rs` | 23 | Unix | Pipe output order, signals, drain after exit, process groups, output files, environment, line counts, waiters, metadata |
| `packages/process-daemon/tests/runtime.rs` | 12 | Unix and Windows | Real child input and output, Unicode, cwd and environment, executable paths, console resize, terminal replies, replay, exits, termination |
| `packages/process-daemon/tests/playground.rs` | 3 | Unix | Authoritative query response, owner exit cleanup, observer replay through the CLI |
| `packages/process-daemon/tests/rows.rs` | 1 | Unix | `read_rows` round trip through the Rust daemon client |
| `packages/process-daemon/tests/ghostty-effects.rs` | 5 | All, plus Miri | Retained userdata across moves, owned callback bytes, null buffers, panics, teardown |
| `packages/process-daemon/tests/transport-retained.rs` | 1 | Miri | Retained native pointer across owner moves and repeated access |
| `packages/process-daemon/tests/pipe_windows.rs` | 18 | Windows | Pipe output and exits, environment, files, waiters, signals, job trees, command line, no window, concurrent file access |
| `packages/process-daemon/tests/windows-daemon.rs` | 7 | Windows | Real named-pipe ownership and handoff, registration locking, partial requests, blocked subscribers, ConPTY operations, exits |

Supporting fixtures and Miri manifests:

- `packages/process-daemon/tests/support/terminal_fixture.rs`
- `packages/process-daemon/tests/support/resize_fixture.rs`
- `packages/process-daemon/tests/ghostty-effects/Cargo.toml`
- `packages/process-daemon/tests/transport-retained/Cargo.toml`

## End-to-end Tests

These tests drive the daemon through the OpenCode server and SDK.

| File | Tests | Description |
|---|---|---|
| `packages/core/test/persistent-pty-daemon.test.ts` | 11 | Registration rotation, rediscovery, waits and cancellation, unreachable daemons, protocol mismatch, fresh starts, adopted daemon shutdown |
| `packages/core/test/persistent-pty-session.test.ts` | 8 | Session cleanup, rename and events, handoff lifetime, pipe process lifecycle, separation of pipes and terminals, request errors |
| `packages/server/test/persistent-pty.test.ts` | 1 | Live SDK read of a controlled terminal and rename without a feature check |
| `packages/app/e2e/utils/persistent-pty.ts` | utility | Shared helper for app end-to-end tests that use persistent PTYs |

CI adds checks that are not ordinary test functions.
`check-process-daemon.yml` runs formatting, Clippy, and the suites above on Linux and macOS, runs Miri under Stacked Borrows and Tree Borrows, and runs native Windows x64 and ARM64 builds and tests with a standalone library test executable to prove static Ghostty linking.
`release-process-daemon.yml` runs service and CLI integration checks, smoke tests each binary, and validates npm packages before publishing.

## Edge Cases and Failure Scenarios

- Unknown `op` values and bad request fields return errors instead of dropping the connection.
- A frame larger than 8 MiB fails before allocation.
- Ownership is exclusive, bounded by five seconds, and fenced by generation.
- A handoff ticket is non-renewing, expires after 120 seconds, and has only one winner.
- A superseded owner cannot prepare a handoff or stop the daemon.
- Owner loss stops terminals even while clients are blocked.
- A final exit frame reaches subscribers before the subscription closes.
- A blocked controller is woken by shutdown, and a blocked observer is disconnected when its queue stays full.
- Resize reports precede user input and are delivered once.
- Hidden terminal output stays bounded by the replay capacity.
- Alternate-screen reads do not expose primary-screen history, and zero rows is invalid.
- An OSC title hidden behind a user title publishes no change event.
- Pipe children get exactly the supplied environment and no ignored SIGPIPE.
- A descendant holding the pipe delays exit by at most one second.
- A failed pipe command stops background processes, and a surviving signal is escalated to SIGKILL.
- A rejected pipe request never creates or truncates the output file.
- A failing output file sets `output_error` while the process keeps running.
- Every waiter receives one exit, and terminate ends a pending wait with an error.
- Native callback state survives moves, repeated drains, null buffers, and panics under both Miri borrow models.
- Windows tests verify no console window, argument round trips, and output files that can be read and deleted while open.

## Coverage Matrix

| Requirement | Test coverage |
|---|---|
| FR-1 | `src/service.rs`, `tests/service.rs`, `tests/runtime.rs` |
| FR-2 | `tests/service.rs`, `tests/playground.rs`, `tests/runtime.rs` |
| FR-3 | `src/service.rs`, `tests/service.rs`, `tests/runtime.rs` |
| FR-4 | `src/ownership.rs`, `tests/ownership.rs`, `tests/windows-daemon.rs` |
| FR-5 | `src/ownership.rs`, `tests/ownership.rs`, `tests/windows-daemon.rs`, `persistent-pty-session.test.ts` |
| FR-6 | `src/daemon.rs`, `src/daemon/unix.rs`, `src/daemon/windows.rs`, `tests/ownership.rs`, `tests/windows-daemon.rs` |
| FR-7 | `src/protocol.rs`, `src/daemon/server.rs`, `tests/ownership.rs` |
| FR-8 | `src/protocol.rs`, `src/service.rs`, `tests/service.rs`, `tests/rows.rs`, `tests/runtime.rs` |
| FR-9 | `tests/service.rs`, `tests/ownership.rs`, `tests/windows-daemon.rs` |
| FR-10 | `tests/pipe.rs`, `tests/pipe_windows.rs`, `persistent-pty-session.test.ts` |
| FR-11 | `tests/pipe.rs`, `tests/pipe_windows.rs`, `persistent-pty-session.test.ts` |
| FR-12 | `src/daemon.rs`, `src/client.rs`, `tests/ownership.rs` |
| FR-13 | `src/daemon/sweep.rs`, `src/daemon/unix.rs`, `src/daemon/windows.rs`, `tests/ownership.rs` |
| FR-14 | CI npm validation in `release-process-daemon.yml`, `script/npm-packages.mjs` |
| FR-15 | `tests/playground.rs`, CLI smoke checks in both workflows |
| FR-16 | `.github/workflows/check-process-daemon.yml` |
| FR-17 | `.github/workflows/release-process-daemon.yml`, `script/npm-packages.mjs` |
| FR-18 | `persistent-pty-daemon.test.ts`, `persistent-pty-session.test.ts` |
| FR-19 | `tests/playground.rs` |
| NFR-1 | `src/daemon/unix.rs`, `src/transport/windows/security.rs`, `tests/windows-daemon.rs` |
| NFR-2 | `src/transport/windows/security.rs`, `tests/windows-daemon.rs` |
| NFR-3 | `tests/service.rs`, `tests/runtime.rs`, `tests/ownership.rs` |
| NFR-4 | `tests/service.rs`, `tests/ownership.rs`, `tests/runtime.rs` |
| NFR-5 | `src/protocol.rs`, `src/service.rs`, `tests/service.rs`, `tests/runtime.rs` |
| NFR-6 | Both GitHub workflows |
| NFR-7 | `src/protocol.rs`, `persistent-pty-daemon.test.ts` |
| NFR-8 | Both GitHub workflows, `build.rs` |
