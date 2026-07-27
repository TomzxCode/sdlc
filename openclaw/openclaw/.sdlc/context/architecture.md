# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Channels                            │
│  WhatsApp  Telegram  Discord  Slack  iMessage  IRC  Signal ... │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Gateway Server (HTTP/WS)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │   Auth   │ │ Sessions │ │ Channels │ │  Control UI (Web)  │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────────────┐   │
│  │   CLI    │ │  Config  │ │  Plugin Registry & Lifecycle  │   │
│  └──────────┘ └──────────┘ └──────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Runtime                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │ Models   │ │  Tools   │ │ Compaction│ │  Subagents         │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                       │
│  │ Prompts  │ │ Memory   │ │ Trajectory│                       │
│  └──────────┘ └──────────┘ └──────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| Gateway Server | HTTP/WebSocket server, auth, session lifecycle, API endpoints | TypeScript, Hono, Node.js |
| Agent Runtime | AI conversation engine, model provider integration, tool execution | TypeScript, provider-specific SDKs |
| Channel System | Message transport abstraction, channel-specific rendering, deliverability | TypeScript, per-channel native SDKs |
| Plugin System | Extension registry, lifecycle management, import boundary enforcement | TypeScript, facade-runtime pattern |
| CLI | Command-line interface for configuration, plugins, channels, operations | TypeScript, yargs |
| Config System | JSON schema validation, file I/O, env var substitution, merge-patch | TypeScript, zod |
| Control UI | Web dashboard for chat and administration | TypeScript, Lit web components |
| Mobile/Desktop Apps | Companion applications for macOS, iOS, Android, Windows | Swift (iOS/macOS), Kotlin (Android), C# (Windows) |

## Data Flow

1. User sends a message on a channel (WhatsApp, Telegram, etc.)
2. Channel plugin receives the message, normalizes it into an internal envelope
3. Gateway server authenticates the request, resolves the session, and dispatches to the agent runtime
4. Agent runtime constructs a prompt with conversation history, system prompt, and available tools
5. Model provider (OpenAI, Anthropic, etc.) generates a response, possibly invoking tools
6. Tools execute (bash, file I/O, web search, etc.) and return results
7. Agent runtime compacts context as needed and streams the response back
8. Channel plugin renders the response in the native channel format and delivers it
9. Session state and transcript are persisted to SQLite

## Infrastructure

| Area | Technology |
|---|---|
| Runtime | Node.js 22.22.3+, 24.15+, or 25.9+ (26 recommended), Bun compatible |
| State storage | SQLite via Kysely query builder |
| Configuration | JSON files with zod schema validation |
| CI/CD | GitHub Actions, Blacksmith Testbox |
| Package manager | pnpm (workspace monorepo) |
| Build | tsdown (TypeScript bundler) |
| Linting | oxlint |
| Formatting | oxfmt |
| Testing | Vitest |
| Protocol | Gateway Protocol (custom WebSocket/HTTP RPC) |
| Hosting | Self-hosted (user's machine, VPS, Docker, fly.io) |

## Architecture Decisions

Key decisions are recorded in `.sdlc/knowledge/decisions/`. Notable patterns include:
- Single-user architecture: no multi-tenancy, simplified auth and state management
- SQLite-first: all runtime state in SQLite, no JSON sidecar files
- Plugin facade pattern: plugins import core only via `openclaw/plugin-sdk/*`
- No silent config compat: runtime reads canonical config only; migrations handled by `openclaw doctor --fix`
- Bundled vs external plugins: bundled plugins ship in core dist; external official plugins use registry-aware facade-runtime
