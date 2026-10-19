<!-- session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA -->
# Project Overview

## Purpose

OpenClaw is a personal AI assistant that runs on user-owned devices.
It answers users on the messaging channels they already use (Discord, iMessage, Slack, Teams, Telegram, WhatsApp, and many more), can speak and listen on macOS/iOS/Android, and renders a live Canvas/Control UI for rich interaction.
One Gateway runs as a personal assistant on a laptop or as a shared team deployment; configuration is the only difference.
The Gateway is the control plane; the product is the assistant itself, not just a gateway.
It remembers past conversations, can hand long work to a paired device or a leased cloud machine, and can learn repeatable procedures as skills.
Anonymous feature statistics are opt-in and off by default; `update.checkOnStart: false` disables the daily version check and statistics together.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| End users | Individual operators | A fast, private, always-on AI assistant on their preferred channels |
| Plugin developers | Community contributors | A well-documented SDK to build and distribute extensions and skills |
| Maintainers | Core team | Project stability, security, compatibility, and community health |
| Sponsors and donors (Amazon, Lobster Computer Company, Offline Holdings, OpenAI, Red Hat, University of Michigan; infrastructure from Blacksmith, Convex, GitHub, NVIDIA, Vercel) | Funding and infrastructure partners | Adoption and ecosystem growth |
| OpenClaw Foundation (independent 501(c)(3)) | Stewardship, employs core team, signs releases | Project stability, security, compatibility, and community health |

## Scope

**In scope:**
- Multi-channel messaging integration for roughly 30 platforms beyond the named channels, most of them official plugins
- Shared team deployment as configuration of the same Gateway (one trust domain; see `docs/start/teams.md`)
- AI agent execution with support for major model providers (OpenAI, Anthropic, Google, open-source, etc.)
- Durable memory and session recall (curated memory files, episodic notes, standing intents, hybrid search)
- Remote and cloud execution of session work (paired device node hosts, leased cloud workers, worker-local inference)
- CLI and setup wizard for configuration, plugin management, and operations
- Terminal UI for interactive chat
- Web-based Control UI for chat and administration
- Plugin system with SDK for community extensions, plus a skill system with a personal library and a Workshop loop
- Companion apps for macOS, iOS, Android, Windows, and Linux
- Agent tool system (bash, file I/O, web search, image generation, etc.)
- Configuration via `openclaw.json` with JSON schema validation
- Session management, conversation persistence, and context compaction
- Local security audit, a content-free runtime activity ledger, and SecretRef-based credential handling
- Session dashboards, a project registry, and shared boards for tracking work

**Out of scope:**
- Multi-tenant SaaS hosting for mutually untrusted parties (run one Gateway per tenant instead)
- Centralized cloud service or hosted OpenClaw fleet (runs on user's own infrastructure)
- Formal enterprise SSO or RBAC
- No paid tier, hosted service, or token (stewarded by the OpenClaw Foundation)
- Native desktop app beyond macOS and Linux (Windows via CLI only; Windows Hub companion app available)

## Key Constraints

- Node `>=24.16.0 <25 || >=26.1.0` runtime (Node 26 recommended), with opt-in Bun compatibility
- Single trust-domain architecture by design; team use shares one control plane, not multi-tenant isolation
- Plugin isolation via explicit import boundaries and capability gating; plugins import core only through `openclaw/plugin-sdk/*`
- Configuration is single-source-of-truth via `openclaw.json`; no silent config compat
- SQLite-first for all runtime state; no JSON/JSONL sidecar files for state. PostgreSQL is supported as an experimental second engine (schema versions state 28, agent 31)
- Security-first: no secrets in logs, explicit trust model, rate limiting on auth
- TypeScript ESM strict throughout; no `any` types, discriminated unions for routing
- The Gateway process is the single owner of every OpenClaw database and its state; other processes route mutations through it
