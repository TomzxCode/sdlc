---
title: "Process Daemon / PTY Service"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Specification: Process Daemon / PTY Service

## Overview

The implementation is a Rust library and binary under `packages/process-daemon`.
The library exposes `client`, `daemon`, `protocol`, and `service` modules, plus private `ghostty`, `ownership`, `transport`, and `musl` modules.
The binary dispatches to `client::run_cli`, which starts and observes daemons and provides an interactive playground.
The npm wrapper lives in `packages/process-daemon/npm` and publishes as `@opencode/pty`.
CI and release automation live in `.github/workflows/check-process-daemon.yml` and `.github/workflows/release-process-daemon.yml`.

## Architecture

```text
opencode-pty process
├── service lock and atomic private registration
├── authenticated framed IPC over Unix socket or Windows named pipe
├── ownership state machine with handoff tickets
├── terminal registry
├── terminal 1
│   ├── blocking reader thread
│   ├── actor and libghostty thread
│   ├── blocking writer thread
│   └── child-wait thread
└── terminal 2
    ├── blocking reader thread
    ├── actor and libghostty thread
    ├── blocking writer thread
    └── child-wait thread
```

The actor owns the portable-pty master, the libghostty terminal, the bounded replay, parsed screen state, lifecycle, and snapshots.
Output flows from the reader through a bounded actor queue, into replay and the parser, then through a bounded writer queue for terminal replies.
User input enters the same actor queue and uses the same writer queue.
No borrowed libghostty value or native handle leaves the actor thread.
The daemon loop waits in `poll(2)` on the listener and a wake socket pair on Unix, and polls every 25 ms on Windows.
Handler threads own connection reads and writes, and shutdown cancellation wakes partial requests and blocked subscription writes before joining.

## Data Models

### Registration

Stored as `service.json` in `DIR/NAME` with `service.lock` beside it.

| Field | Type | Description |
|---|---|---|
| instance_id | string | Random per-daemon identity |
| pid | u32 | Daemon process ID |
| protocol | u32 | `PROTOCOL_VERSION`, currently 9 |
| socket | path | Opaque local endpoint, a Unix socket path or Windows pipe name |
| token | string | Random credential required on every request |
| features | string array | Additive capabilities, empty in protocol 9 |

### ProcessInfo

| Field | Type | Description |
|---|---|---|
| id | u64 | Terminal identifier |
| mode | enum | `pty` or `pipe` |
| pid | u32 or null | Child process ID, historical metadata after exit |
| command | string array | Program and arguments |
| cwd | path | Child working directory |
| group_id | string | Opaque client-supplied grouping key |
| lifecycle | enum | `running`, `exited` with optional code and signal, or `failed` with a message |
| output_head / output_tail | u64 | Absolute byte offsets |
| started_at / exited_at | u64 / u64 or null | Milliseconds since the Unix epoch |
| pty | object or absent | `title`, `user_title`, `foreground_process`, `cols`, `rows` |
| pipe | object or absent | `output_path`, `output_lines`, `output_error`, `metadata` |

Exactly one of `pty` and `pipe` is present and it matches `mode`.
A PTY title is the user title, else the latest non-empty OSC title, else the creation title.
`output_error` is omitted when no file write failed.

### Protocol Frames

Control frames are bounded UTF-8 JSON with a four-byte big-endian length prefix and an `8 * 1024 * 1024` byte cap.
Envelopes carry `token` and `request`, where `request` has an `op` tag.
Output frames use tag byte zero followed by an eight-byte start offset, an eight-byte end offset, and the raw bytes.
An unparseable request is answered with `Error` after the token is checked, so clients can probe for support.

### Stream Events

Subscriptions carry ordered `Output`, `Resized`, `Exited`, `ControllerChanged`, `TitleChanged`, and `ForegroundProcessChanged` events.
Each subscription has an attachment ID, a controller or observer role, a generation, and a replay that starts at a requested offset.
Controller delivery applies backpressure, while observers tolerate bounded bursts and are disconnected when their 1024-slot queue stays full.

## API Contracts

The daemon surface is a local framed byte stream, not an HTTP API, so an OpenAPI `api.yaml` does not apply.
The HTTP endpoints that OpenCode exposes for persistent PTYs are defined in `packages/protocol/src/groups/persistent-pty.ts` and are outside this package.

| Request op | Response type | Notes |
|---|---|---|
| `ping` | `pong` | Instance ID, PID, protocol, features |
| `own` | `owned` or `error` | Optional handoff ticket, exclusive owner |
| `prepare_handoff` | `handoff` or `error` | Ticket and Unix millisecond expiry, owner only |
| `create_pty` | `created` | Program, args, cwd, env, group, title, cols, rows |
| `create_pipe` | `created` | Program, args, cwd, env, group, output path, metadata |
| `list` | `processes` | Mode is required |
| `get` | `process` | Either mode |
| `wait` | `exited` or `error` | Pipe only, held until exit |
| `signal` | `ok` | Pipe only, SIGTERM, SIGINT or SIGKILL |
| `set_metadata` | `ok` | Pipe only, replaces metadata |
| `write` | `ok` | Base64 input bytes, optional attachment ID |
| `resize` | `ok` | PTY and parser resize in one actor command |
| `control` | `resized` | Atomic interaction promotion with resize and checkpoint |
| `input` | `ok` | Promotes controller, carries resize and input |
| `snapshot` | `snapshot` | Parsed text, VT checkpoint, cursor |
| `read_rows` | `rows` | Physical rows from the active buffer |
| `rename` | `ok` | Sets or clears the user title |
| `replay` | `replay` | Absolute offsets and truncation flag |
| `subscribe` | `attached` then stream events | Replay to live |
| `terminate` | `ok` | Kills and removes one process |
| `shutdown` | closed | Stops the daemon |

## Sequences

### Startup and ownership

```text
integration starts opencode-pty daemon --name NAME
daemon creates DIR/NAME, locks service.lock, binds endpoint
daemon writes service.json with instance_id, pid, protocol, socket, token, features
integration reads service.json and sends own request within five seconds
daemon answers owned and keeps that connection as the sole owner
integration sends ordinary requests and subscriptions on separate connections
```

### Handoff

```text
owner sends prepare_handoff on its own connection
daemon returns ticket and expires_at, the same ticket on repeated preparation
successor sends own with the ticket, even while the old owner is connected
daemon increments generation, consumes the ticket, and returns owned
old owner can no longer prepare handoffs or shut down
old owner disconnect does not stop the daemon
unclaimed ticket expiry cancels the handoff and stops a disconnected daemon
```

### PTY output

```text
child writes to PTY
reader sends bytes to the bounded actor queue
actor appends raw bytes to replay and calls libghostty vt_write
actor queues parser replies to the bounded writer queue
writer sends replies to the child
actor fans out coalesced output frames to subscribers
```

### Pipe process

```text
integration sends create_pipe with an absolute output path
daemon opens and truncates the file, then spawns the child with exact env
reader writes every output byte to the file before sending it to the actor
actor keeps no replay and counts newlines with output_tail
wait holds its connection until child exit and output end are both known
daemon publishes Exited with exit code or signal, offsets, lines and errors
```

### Release

```text
maintainer bumps Cargo.toml, Cargo.lock and npm/package.json to X.Y.Z
maintainer merges to dev and pushes process-daemon-vX.Y.Z
checks job validates the tag against protocol and package versions
build jobs compile eight targets and run service and CLI integration checks
package job writes SHA256SUMS, release-manifest.json and nine npm packages
release job publishes the GitHub release and npm packages with trusted publishing
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Terminal parsing | Direct libghostty C API with generated subset bindings | Keeps native state actor-local and avoids a third-party Rust crate |
| Framing | Four-byte big-endian length with tagged raw frames | Allows binary output to bypass JSON without losing JSON request ergonomics |
| Ownership | One owner connection with generation and handoff tickets | Fences a superseded server without persisting ownership state |
| Transport | Unix sockets and Windows named pipes behind one module | Keeps framing, dispatch, and subscriptions shared across platforms |
| Pipe storage | Output file is the only copy | Avoids unbounded replay for commands without a terminal |
| Registration | Atomic replace under a private lock | Prevents two daemons using one runtime directory |
| Native build | Pinned Ghostty revision built by Zig, `links = "ghostty-vt"` | Reproducible builds and rejection of competing native owners |
| npm dispatch | Thin ESM wrapper plus platform optional dependencies | One stable import for eight platform binaries |

## Risks and Unknowns

1. A Linux child that exits with a large queued PTY write can leave the master write blocked and prevent the writer thread from joining.
2. Child process-tree cleanup goes only as far as portable-pty's root killer, so descendants can survive.
3. ConPTY can consume application terminal queries itself on Windows.
4. Registration replacement on Windows requires local NTFS and Windows 10 1709 or later.
5. Cold-client checkpoint transport is not implemented.
6. Platform signing is not implemented.
7. Protocol 8 daemon replacement on upgrade ends running commands and terminals.

## Out of Scope

- OpenTUI integration for persistent terminals and ordered groups.
- A Windows interactive `TerminalClient` and playground.
- Descriptor passing or live replacement of a crashed daemon.
- Hardening portable-pty's Windows ConPTY backend.
- Persisted ownership or handoff state.
