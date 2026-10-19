# Project Overview

## Purpose

jcode (J-Code) is a terminal-based AI coding agent harness written in Rust.
It runs a long-lived local server (daemon) that manages AI coding sessions and streams agent responses into a fast, memory-efficient terminal UI.
The project targets developers who want an always-on coding agent that can use their existing LLM subscriptions (Claude Max, ChatGPT Pro, and 30+ other providers) instead of a dedicated API key.
It is an independent project that benchmarks against OpenCode, Codex CLI, pi, and Claude Code, and can import credentials from several of them.
Distinguishing features are RAM efficiency, multi-model support, multi-agent ("swarm") coordination, an agent memory system with local storage and Jev-based relevance recall, session resume and replay, ambient background operation, and companion clients.
The desktop app drives jcode through the Rust SDK; the iOS app is a thin client over the server's WebSocket gateway (`/health`, `/pair`, `/ws`).
The versioned harness API and its Rust and TypeScript SDKs are the separate surface for embedding the agent runtime in other programs.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Individual developers | End users | Blazing-fast TUI, low RAM usage, multi-model support, reliable session persistence, low-friction login with their existing LLM subscriptions |
| Maintainer (1jehuang) | Maintainer | Shaping the product roadmap, release cadence, telemetry-informed decisions, and keeping the roadmap ahead of the tools it benchmarks against (OpenCode, Codex CLI, pi, Claude Code) |
| OpenClaw-style personal-agent users | End users | Ambient mode, memory, garden/scout work cycles, iOS/desktop companions, pairing with the mobile app |
| LLM provider operators | External partners | Auth integration coverage, sponsored discovery placement, provider catalog accuracy |
| Open source contributors | Community | Clear contribution and release process, quality-guardrail CI, issue-driven PR workflow |

## Scope

**In scope:**
- Terminal agent harness: TUI, REPL, single-shot `run`, session resume/replay/import
- Always-on local server/daemon with Unix socket (or named pipe) IPC, hot reload, and multi-client support
- Multi-provider authentication and routing (OAuth, API keys, external credentials)
- Agent memory system (local memory graph under `~/.jcode/memory`, Jev Decisions recall, memory injection, and ambient consolidation) and session search
- Multi-agent swarm coordination with plan DAG and comm channels
- Ambient background mode, background tasks, and overnight processing
- Context compaction, hooks, permissioning, and shell-command safety gates
- Telemetry collection and an opt-out model
- Auto-update, installers, and multi-platform release tooling
- Harness API bridge with Rust and TypeScript SDKs
- Companion iOS app (ios/) and desktop panels via the model-facing panel tool
- Account, billing, and metered hosted-model routing (`jcode account`, `/hosted`)
- Cloud session handoff (`jcode cloud move` and `jcode cloud return`)

**Out of scope:**
- A fully managed per-user cloud agent host (planned in `docs/JCODE_CLOUD_AWS.md` but not deployed; the local daemon remains the runtime for self-hosted use)
- Model training or fine-tuning
- Non-terminal UI as the primary interface (desktop/iOS are companions)
- Vendoring or re-implementing provider APIs beyond the connectors the codebase ships

## Key Constraints

- Rust workspace, edition 2024, with strict quality budgets enforced in CI (`clippy -D warnings`, warning/panic/code-size/test-size/swallowed-error/wildcard-reexport/dependency-boundary budgets, module-declaration check, and an unused-dependency gate).
- Single-server, multi-client daemon architecture: first `jcode` run spawns the server, later runs connect over a Unix socket.
- Terminal-first with an emphasis on low RAM and fast first frame; selected dependency stacks are pinned to `opt-level = 3` in dev profiles.
- Providers are reached through the user's existing subscriptions where possible; auth must support Claude Max OAuth, OpenAI/Codex OAuth, Gemini OAuth, GitHub Copilot device flow, Azure Entra ID, and OpenAI-compatible API keys.
- Local-first storage: sessions, config, auth, and memory live under `~/.jcode/`; provider API-key env files live in the platform config dir (`~/.config/jcode/`), and the daemon socket lives in the runtime dir (for example `/run/user/<uid>/jcode.sock`).
- Privacy-conscious telemetry with explicit opt-out (`JCODE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, or a file marker); collection is documented in `TELEMETRY.md`, including the one identifiable path (provider OAuth account email) that the opt-out also covers.
- Cross-platform: Linux (x86_64/aarch64), macOS (aarch64, x86_64), Windows (x86_64/aarch64), with FreeBSD smoke coverage.
