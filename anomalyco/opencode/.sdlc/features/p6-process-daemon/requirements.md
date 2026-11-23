---
title: "Process Daemon / PTY Service"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Requirements: Process Daemon / PTY Service

## Overview

The process daemon is a persistent Rust service named `opencode-pty` that owns terminal child processes for OpenCode.
It uses `portable-pty` to run children and `libghostty-vt` to keep authoritative terminal state and answer terminal protocol queries.
Each terminal has isolated reader, actor, writer, and child-wait threads, so one terminal cannot block the service or another terminal.
The service speaks protocol 9 over a private authenticated local byte stream, a Unix socket or a Windows named pipe.
One connection owns the daemon, and ordinary requests and subscriptions use separate connections.

The package lives at `packages/process-daemon` in the OpenCode monorepo.
It moved from `anomalyco/opencode-pty` at commit `443945a`, version `0.3.1`, and is currently version `0.6.0`.
The npm wrapper `@opencode/pty` selects a platform-specific native binary and exposes its path as `binaryPath`.
OpenCode's core, protocol, and server layers provide a lazy backend proxy and experimental HTTP endpoints on top of the daemon.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Persistent terminals survive server restarts and terminal queries are answered correctly |
| Server team | A small authenticated local transport with explicit ownership and handoff |
| Client team | A typed npm wrapper and a binary path that works on every supported platform |
| Release engineers | Reproducible cross-platform binaries and npm packages with provenance |
| Core team | Thread isolation that keeps one slow terminal from blocking another |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The daemon shall own multiple PTY child processes with one reader, one actor, one writer, and one child-wait thread per terminal. |
| FR-2 | Must | The actor shall be the only owner of libghostty state, and terminal-generated responses shall go through the same serialized writer path as user input. |
| FR-3 | Must | The daemon shall keep bounded replay with absolute output offsets and explicit truncation. |
| FR-4 | Must | The daemon shall accept one owner connection within five seconds of startup and stop when that connection is lost unless a handoff was prepared. |
| FR-5 | Must | A prepared handoff ticket shall be valid for 120 seconds, be consumable only once, and replace a connected owner atomically. |
| FR-6 | Must | The daemon shall publish an atomic private registration containing an instance ID, PID, protocol version, features, endpoint, and token. |
| FR-7 | Must | Protocol 9 shall use four-byte big-endian frames with bounded UTF-8 JSON control frames and tagged raw binary output frames. |
| FR-8 | Must | The daemon shall support create, list, get, write, resize, control, input, snapshot, read_rows, rename, replay, subscribe, terminate, and shutdown for PTYs. |
| FR-9 | Must | A terminal shall have at most one controller, with observers promoted by explicit takeover and demotion of the previous controller. |
| FR-10 | Must | The daemon shall support pipe processes with no terminal, stdin closed, stdout and stderr merged, and all output written to an absolute path. |
| FR-11 | Must | Pipe processes shall support wait, signal with SIGTERM, SIGINT or SIGKILL, and replacement of an opaque metadata object. |
| FR-12 | Must | Every command shall accept `--name NAME` and an optional `--runtime-dir DIR`, with names restricted to one path component of letters, digits, `.`, `_`, or `-`. |
| FR-13 | Should | The daemon shall remove its own registration and socket on exit and sweep abandoned sibling runtime directories older than ten minutes. |
| FR-14 | Must | The npm package shall select the native binary for the current platform and expose `binaryPath` or `undefined` for unsupported platforms. |
| FR-15 | Must | The CLI shim shall spawn the selected binary with inherited stdio and forward its exit status or signal. |
| FR-16 | Must | CI shall check formatting, Clippy, and tests for Linux, macOS, Windows x64 and ARM64, plus Miri callback ownership tests. |
| FR-17 | Must | A `process-daemon-vX.Y.Z` tag shall publish nine npm packages and binaries for eight platform targets with checksums, a manifest, and provenance. |
| FR-18 | Should | OpenCode shall start one daemon lazily per server runtime directory and reuse the previous directory only through an explicit handoff descriptor. |
| FR-19 | Should | The playground shall start and own a daemon and expose commands for creating terminals, running commands, inspecting state, and stopping the daemon. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The registration file and runtime directory shall be private, and the token shall be required on every request. |
| NFR-2 | Must | Security | Windows clients shall verify the registration owner, ACL, and named pipe server PID before sending the token. |
| NFR-3 | Must | Reliability | The daemon shall not block the control path on terminal I/O. |
| NFR-4 | Must | Reliability | One terminal exit shall not stop the service or another terminal. |
| NFR-5 | Must | Performance | Actor and writer queues shall be bounded, output shall be coalesced at 8 KiB or after 1 ms, and frames shall be capped at 8 MiB. |
| NFR-6 | Must | Portability | The daemon shall build on Linux GNU, Linux musl, macOS, and Windows MSVC for x64 and ARM64. |
| NFR-7 | Should | Compatibility | Additive capabilities shall use a required `features` list, and breaking changes shall bump the protocol version. |
| NFR-8 | Must | Build | Normal builds shall not need bindgen or libclang, and the native Ghostty revision shall be pinned in `ghostty-revision`. |

## Constraints

- The package version, every npm version, and the release tag must agree.
- The package declares `links = "ghostty-vt"` so Cargo rejects a second native Ghostty owner.
- This repository does not use Changesets.
- The default branch is `dev`, and releases are tagged from it.
- Rust 1.90.0 and Zig 0.16.0 are the pinned toolchains.
- The Windows Rust `TerminalClient` and interactive CLI are not ported.

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a daemon with two PTY terminals
    - **When** one child stops reading its output
    - **Then** the other terminal and the control path continue to work
- [ ] **FR-2**
    - **Given** a program that sends a terminal query
    - **When** libghostty produces a response
    - **Then** the response reaches the child through the same writer queue as user input
- [ ] **FR-4**
    - **Given** a newly started daemon with no owner
    - **When** no owner claims it within five seconds
    - **Then** the daemon stops
- [ ] **FR-5**
    - **Given** a prepared handoff ticket
    - **When** two successors try to claim it
    - **Then** only one succeeds and the superseded connection loses owner privileges
- [ ] **FR-7**
    - **Given** a request frame larger than 8 MiB
    - **When** the daemon reads it
    - **Then** the connection fails with a frame limit error
- [ ] **FR-9**
    - **Given** an active controller and an observer
    - **When** the observer takes over control
    - **Then** the former controller stays subscribed and receives a controller change event
- [ ] **FR-10**
    - **Given** a pipe process request with an absolute output path
    - **When** the child writes to stdout and stderr
    - **Then** both byte streams are written to the file in order
- [ ] **FR-14**
    - **Given** `@opencode/pty` installed on a supported platform
    - **When** `binaryPath` is read
    - **Then** it points to the platform-specific native executable
- [ ] **NFR-1**
    - **Given** a registration file and a runtime directory
    - **When** another local user inspects them
    - **Then** the permissions deny access

## Conflicts

The package-level `AGENTS.md` describes an earlier scope without OpenCode IPC, descriptor passing, or a Windows backend.
The README, SPEC, and current source describe the implemented behavior and take precedence here.

## Open Questions

1. What drove the choice of five seconds for acquisition and 120 seconds for handoff expiry?
2. When will platform signing be added to releases?
3. What is the design for cold-client checkpoint transport?
4. Will the Windows Rust `TerminalClient` and playground be ported?
5. Which approach will harden process-tree termination beyond portable-pty's root killer?
6. How will persistent terminals and ordered groups be integrated into OpenTUI?
7. How often should `ghostty-revision` be advanced relative to upstream changes?
