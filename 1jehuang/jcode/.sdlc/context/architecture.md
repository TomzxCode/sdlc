# Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                           jcode (CLI client)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  TUI     │  │  REPL    │  │  run     │  │  api-bridge / acp    │  │
│  │ (ratatui)│  │          │  │ (json)   │  │  (harness API, SDKs) │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │
│                    │                 │                 │             │
│              ┌─────▼─────────────────▼─────────────────▼─────┐       │
│              │           jcode-protocol (NDJSON IPC)          │       │
│              │         Unix socket / Windows named pipe        │       │
│              └─────┬─────────────────┬─────────────────┬─────┘       │
└────────────────────┼─────────────────┼─────────────────┼─────────────┘
                     │                 │                 │
┌────────────────────▼─────────────────▼─────────────────▼─────────────┐
│               jcode server (long-lived daemon, `jcode serve`)         │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────────┐  │
│  │ session store  │  │ agent / turn   │  │ tools + agent runtime   │  │
│  │ + journal      │  │ loop           │  │ (30+ tools, bash gate)  │  │
│  └────────────────┘  └────────────────┘  └─────────────────────────┘  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────────┐  │
│  │ swarm          │  │ ambient        │  │ memory graph +          │  │
│  │ coordination   │  │ scheduler      │  │ embeddings (ONNX)       │  │
│  └────────────────┘  └────────────────┘  └─────────────────────────┘  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────────┐  │
│  │ reload/recovery│  │ telemetry      │  │ update check / restart  │  │
│  │                │  │ queue          │  │ snapshot                │  │
│  └────────────────┘  └────────────────┘  └─────────────────────────┘  │
└──────────────┬──────────────────────────────┬─────────────────────────┘
               │                              │
┌──────────────▼──────────────┐   ┌───────────▼──────────────────────────┐
│  LLM providers (40+)        │   │  Infrastructure                      │
│  Anthropic, OpenAI, Gemini, │   │  ~/.jcode/ (config, sessions, logs)  │
│  Copilot, Cursor, Bedrock,  │   │  telemetry.jcode.sh (Cloudflare W)   │
│  OpenRouter, OpenAI-compat  │   │  jcode.sh/install (GitHub Releases)  │
└─────────────────────────────┘   └──────────────────────────────────────┘
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| `jcode` CLI / client | Parse subcommands, spawn or connect to the server, present TUI/REPL/`run` output | Rust + clap, ratatui TUI |
| `jcode serve` daemon | Long-lived server owning sessions, agents, tools, swarm, memory, ambient mode | Rust, tokio, in `jcode-app-core` |
| `jcode-protocol` | Client-server wire protocol: `Request`/`ServerEvent`, NDJSON framing over Unix socket / named pipe | Rust, serde, NDJSON |
| `jcode-app-core` | Application core: server, agent/turn loops, tools, swarm, ambient, background tasks | Rust, `jcode-base` re-exported |
| `jcode-base` | Foundational downward-closed layer: provider, auth, config, session, message, memory, telemetry, transport | Rust |
| `jcode-tui` | Presentation layer: TUI widgets + offline video replay (`jcode replay`) | Rust, ratatui, crossterm |
| `jcode-provider-*` | Per-provider config, catalog, and runtime implementations | Rust (Anthropic, OpenAI, Gemini, Bedrock, Copilot, Cursor, OpenRouter, Antigravity, Claude CLI) |
| `jcode-harness-api` / `jcode-sdk` | Stable versioned client API for the harness; Rust SDK | Rust |
| `jcode-harness-api-server` | `jcode api-bridge`: bridges versioned API clients onto the internal protocol | Rust, Unix socket |
| `jcode-desktop2` | Greenfield desktop companion app | Rust, winit + wgpu + Vello + Parley |
| `ios/` (JCodeKit, JCodeMobile) | Native iOS companion app with gateway pairing | Swift, SwiftUI |
| `telemetry-worker/` | Server-side telemetry ingestion and analytics | Cloudflare Worker + D1 |
| Installers / launcher | Multi-platform install and self-update | Bash, PowerShell, npm launcher packages |

## Data Flow

A user starts a session: the client connects to the server over the protocol socket, subscribes to events, and sends a message.
The server runs the agent turn loop, which calls the selected provider's runtime (streaming deltas back as `ServerEvent`s), executes tool calls through the agent runtime, and appends every message to the session journal (`~/.jcode/sessions/<id>.json` snapshot plus `<id>.journal.jsonl` append log).
Compaction and memory injection happen inside the turn loop; memory embeddings are computed locally with an ONNX MiniLM model.
Swarm and ambient work run as background tasks on the same server, publishing progress events to subscribed clients.
Telemetry events are queued in the client and flushed to `telemetry.jcode.sh/v1/event` (opt-out via env var or file marker).
Auto-update checks GitHub releases and hot-reloads the server into a new binary without dropping sessions.

## Infrastructure

- CI: GitHub Actions (`.github/workflows/ci.yml` is the main gate: fmt, clippy `-D warnings`, budget ratchets, cross-platform build/test matrix for Linux/macOS/Windows, TypeScript SDK, iOS TestFlight, security scans). Release builds via `release.yml`.
- Distribution: GitHub Releases (tagged `v<version>`), `https://jcode.sh/install` for the install script, npm platform launcher packages, `RELEASING.md` documents quick (local) and CI release flows.
- Observability: telemetry pipeline (`TELEMETRY.md`, `telemetry-worker/` D1 schema + dashboards) plus file logging to `~/.jcode/logs` (not stderr).
- Storage: local-first under `~/.jcode/` (config.toml, sessions, auth, logs, durable state), sockets under the runtime dir.
- Release channels: stable and main update channels; immutable versioned binaries under `~/.jcode/builds/versions/<version>/`.

## Architecture Decisions

Key architectural decisions are documented in `docs/` (for example `SERVER_ARCHITECTURE.md`, `MODULAR_ARCHITECTURE_RFC.md`, `CRATE_OWNERSHIP_BOUNDARIES.md`, `HARNESS_API_AND_DESKTOP_REWRITE.md`) and the code comments in `Cargo.toml`.
Formal decision records, once captured, live under `.sdlc/knowledge/decisions/`.
