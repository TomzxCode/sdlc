# Project Overview

## Purpose

jcode (J-Code) is a terminal-based AI coding agent harness, a fork and evolution of sst/opencode.
It runs a long-lived local server (daemon) that manages AI coding sessions and streams agent responses into a fast, memory-efficient terminal UI.
The project targets developers who want an always-on coding agent that can use their existing LLM subscriptions (Claude Max, ChatGPT Pro, and 30+ other providers) instead of a dedicated API key.
Distinguishing features are RAM efficiency, multi-model support, multi-agent ("swarm") coordination, an agent memory system with local embeddings, session resume and replay, ambient background operation, and companion iOS/desktop clients reached through a harness API and SDKs.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Individual developers | End users | Blazing-fast TUI, low RAM usage, multi-model support, reliable session persistence, low-friction login with their existing LLM subscriptions |
| Fork owner / maintainer (1jehuang) | Maintainer | Shaping the product roadmap, release cadence, telemetry-informed decisions, and keeping the fork ahead of upstream opencode |
| OpenClaw-style personal-agent users | End users | Ambient mode, memory, garden/scout work cycles, iOS/desktop companions, pairing with the mobile app |
| LLM provider operators | External partners | Auth integration coverage, sponsored discovery placement, provider catalog accuracy |
| Open source contributors | Community | Clear contribution and release process, quality-guardrail CI, conventional commits, issue-driven PR workflow |

## Scope

**In scope:**
- Terminal agent harness: TUI, REPL, single-shot `run`, session resume/replay/import
- Always-on local server/daemon with Unix socket (or named pipe) IPC, hot reload, and multi-client support
- Multi-provider authentication and routing (OAuth, API keys, external credentials)
- Agent memory system (local ONNX embeddings, recall/injection/consolidation) and session search
- Multi-agent swarm coordination with plan DAG and comm channels
- Ambient background mode, background tasks, and overnight processing
- Context compaction, hooks, permissioning, and shell-command safety gates
- Telemetry collection and an opt-out model
- Auto-update, installers, and multi-platform release tooling
- Harness API bridge with Rust and TypeScript SDKs
- Companion iOS app and greenfield desktop app (desktop2)

**Out of scope:**
- A hosted/managed cloud agent service (the local daemon is the product)
- Model training or fine-tuning
- Non-terminal UI as the primary interface (desktop/iOS are companions)
- Vendoring or re-implementing provider APIs beyond the connectors the codebase ships

## Key Constraints

- Rust workspace, edition 2024, with strict quality budgets enforced in CI (`clippy -D warnings`, warning/panic/code-size/swallowed-error/wildcard-reexport/dependency-boundary budgets).
- Single-server, multi-client daemon architecture: first `jcode` run spawns the server, later runs connect over a Unix socket.
- Terminal-first with an emphasis on low RAM and fast first frame; heavy dependency stacks are pinned to `opt-level = 3` in dev profiles.
- Providers are reached through the user's existing subscriptions where possible; auth must support Claude Max OAuth, OpenAI/Codex OAuth, Gemini OAuth, Azure Entra ID, and OpenAI-compatible API keys.
- Local-first storage: sessions, config, auth, and memory live under `~/.jcode/`.
- Privacy-conscious telemetry with explicit opt-out (`JCODE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, or a file marker); collection is documented in `TELEMETRY.md`.
- Cross-platform: Linux (x86_64/aarch64), macOS (aarch64, x86_64), Windows (x86_64/aarch64), with FreeBSD smoke coverage.
