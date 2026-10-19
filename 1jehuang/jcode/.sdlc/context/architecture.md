# Architecture

## System overview

```mermaid
flowchart TB
    subgraph Client["jcode CLI client"]
        TUI["TUI (ratatui)"]
        REPL["REPL"]
        Run["run (json)"]
        Bridge["api-bridge / acp (harness API, SDKs)"]
    end
    Protocol["jcode-protocol (NDJSON IPC)<br/>Unix socket / named pipe"]
    Client --> Protocol
    subgraph Server["jcode server (long-lived daemon, jcode serve)"]
        direction TB
        SessionStore["session store + journal"]
        TurnLoop["agent / turn loop"]
        Tools["tools + agent runtime (30+ tools, bash gate)"]
        Swarm["swarm coordination"]
        Ambient["ambient scheduler"]
        Memory["memory graph + recall (Jev) + embeddings (ONNX, opt-in)"]
        Reload["reload / recovery"]
        TelemetryQ["telemetry queue"]
        Update["update check / restart snapshot"]
    end
    Protocol --> Server
    Server --> Providers["LLM providers (40+)<br/>Anthropic, OpenAI, Gemini, Copilot, Cursor, Bedrock, OpenRouter, OpenAI-compat"]
    Server --> Infra["Infrastructure<br/>~/.jcode/ (config, sessions, logs)<br/>telemetry.jcode.sh (Cloudflare Worker)<br/>jcode.sh/install (GitHub Releases)"]
```

## Entity relationship diagram

```mermaid
erDiagram
    SESSION ||--o{ MESSAGE : contains
    SESSION ||--o{ TURN : runs
    SESSION ||--o{ SWARM_PLAN : plans
    SESSION ||--o{ TELEMETRY_EVENT : emits
    TURN ||--o{ MESSAGE : produces
    TURN ||--o{ TOOL_CALL : executes
    MESSAGE ||--o{ TOOL_CALL : requests
    SESSION ||--o{ MEMORY_NODE : recalls
    SWARM_PLAN ||--o{ SWARM_TASK : decomposes
    PROVIDER_AUTH ||--o{ TURN : serves
    SESSION {
        string id
        string title
        string status
        string journal_path
    }
    MESSAGE {
        string id
        string role
        string content_blocks
    }
    TURN {
        string turn_index
        string turn_end_reason
    }
    TOOL_CALL {
        string id
        string name
        string input
    }
    MEMORY_ENTRY {
        string id
        string content
        string embedding
    }
    SWARM_PLAN {
        string version
        string participants
        string items
    }
    SWARM_TASK_STATE {
        string task_id
        string status
        string assigned_to
    }
    PROVIDER_AUTH {
        string state
        boolean has_oauth
        boolean has_api_key
    }
    TELEMETRY_RECORD {
        string event
        string id
        string session_id
    }
    GOAL {
        string id
        string status
    }
    TODO_ITEM {
        string id
        string status
    }
```

- Relationships are inferred from the session, turn loop, tool runtime, swarm, memory, provider, and telemetry code.
- Turn state is implicit in the agent turn loop, so `TURN` carries the observable turn index and stop reason rather than a stored record.
- Telemetry is recorded through flat `record_*` calls in `jcode-telemetry-core`, so `TELEMETRY_RECORD` is a logical entity rather than a Rust type.
- The session model is file-based (JSON snapshot plus JSONL journal) under `~/.jcode/sessions/`; `schema.dbml` records the telemetry database schema.

## Key components

| Component | Responsibility | Technology |
|---|---|---|
| `jcode` CLI / client | Parse subcommands, spawn or connect to the server, present TUI/REPL/`run` output | Rust + clap, ratatui TUI |
| `jcode serve` daemon | Long-lived server owning sessions, agents, tools, swarm, memory, ambient mode | Rust, tokio, in `jcode-app-core` |
| `jcode-protocol` | Client-server wire protocol: `Request`/`ServerEvent`, NDJSON framing over Unix socket / named pipe | Rust, serde, NDJSON |
| `jcode-app-core` | Application core: server, agent/turn loops, tools, swarm, ambient, background tasks | Rust, `jcode-base` re-exported |
| `jcode-base` | Foundational downward-closed layer: provider, auth, config, session, message, memory, telemetry, transport | Rust |
| `jcode-tui` | Presentation layer: TUI widgets + offline video replay (`jcode replay`) | Rust, ratatui, crossterm |
| `jcode-provider-*` | Per-provider config, catalog, and runtime implementations | Rust (Anthropic, OpenAI, Gemini, Bedrock, Copilot, Cursor, OpenRouter, Antigravity, Grok Build, plus 42 OpenAI-compatible profiles) |
| `jcode-harness-api` / `jcode-sdk` | Stable versioned client API for the harness; Rust SDK | Rust |
| `jcode-harness-api-server` | `jcode api-bridge`: bridges versioned API clients onto the internal protocol | Rust, Unix socket |
| `jcode-companion` / `jcode-voice` | Per-login desktop companion for open, terminals, lid override, and voice input | Rust |
| `jcode-command-risk` | Deterministic blast-radius classification for shell and file-mutation tools | Rust |
| `jcode-codemode` | Embedded QuickJS sandbox where the model orchestrates tool calls from JavaScript | Rust, rquickjs |
| `ios/` (JCodeKit, JCodeMobile) | Native iOS companion app with gateway pairing | Swift, SwiftUI |
| `telemetry-worker/` | Server-side telemetry ingestion and analytics | Cloudflare Worker + D1 |
| Installers / launcher | Multi-platform install and self-update | Bash, PowerShell, npm launcher packages |

Jcode Desktop lives in a separate repository and is not part of this workspace.

## Data flow

- A user starts a session: the client connects to the server over the protocol socket, subscribes to events, and sends a message.
- The server runs the agent turn loop, which calls the selected provider runtime (streaming deltas back as `ServerEvent`s), executes tool calls through the agent runtime, and appends every message to the session journal (`~/.jcode/sessions/<id>.json` snapshot plus `<id>.journal.jsonl` append log).
- Compaction and memory injection happen inside the turn loop.
- Memory recall runs through Jev Decisions by default; local ONNX MiniLM embeddings are opt-in behind the `embeddings` feature, and a remote OpenAI-compatible embedding backend is pluggable.
- Swarm and ambient work run as background tasks on the same server, publishing progress events to subscribed clients.
- Telemetry events are queued in `jcode-telemetry-core` (shared by client and server) and flushed to `telemetry.jcode.sh/v1/event` (opt-out via env var or file marker).
- Auto-update checks GitHub releases; an explicit reload request hot-reloads the server into a new binary, and a restart snapshot re-launches the prior sessions afterwards.

## Infrastructure

- Hosting and deployment topology is summarized below.
- Detailed technology stack, development tooling, CI/CD pipelines, environments, deployment procedures, and rollback live in `infrastructure.md`.
- Monitoring stack, alerting, and dashboards live in `observability.md`.
- CI: GitHub Actions (`.github/workflows/ci.yml` is the main gate: fmt, clippy `-D warnings`, budget ratchets, cross-platform build/test matrix for Linux/macOS/Windows, TypeScript SDK, security scans). iOS TestFlight runs separately in `ios-testflight.yml`, and FreeBSD smoke in `freebsd-smoke.yml`.
- Release builds run via `release.yml`.
- Distribution: GitHub Releases (tagged `v<version>`), `https://jcode.sh/install` for the install script, npm platform launcher packages, `RELEASING.md` documents quick (local) and CI release flows.
- Observability: telemetry pipeline (`TELEMETRY.md`, `telemetry-worker/` D1 schema + dashboards) plus file logging to `~/.jcode/logs` (not stderr).
- Storage: local-first under `~/.jcode/` (config.toml, sessions, auth, logs, durable state), sockets under the runtime dir.
- Release channels: stable and main update channels.
- Immutable versioned binaries live under `~/.jcode/builds/versions/<version>/`.

## Architecture decisions

- Key architectural decisions are documented in `docs/` (for example `SERVER_ARCHITECTURE.md`, `MODULAR_ARCHITECTURE_RFC.md`, `CRATE_OWNERSHIP_BOUNDARIES.md`) and the code comments in `Cargo.toml`.
- Formal decision records live under `.sdlc/knowledge/`, one file per record, using the `decision.md` template.
