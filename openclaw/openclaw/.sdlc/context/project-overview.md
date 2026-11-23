<!-- session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3 -->
# Project Overview

## Purpose

OpenClaw is a personal AI assistant that runs on user-owned devices.
It answers users on the messaging channels they already use (Discord, iMessage, Slack, Teams, Telegram, WhatsApp, and many more), can speak and listen on macOS/iOS/Android, and renders a live Canvas/Control UI for rich interaction.
One Gateway runs as a personal assistant on a laptop or as a shared team deployment; configuration is the only difference.
The Gateway is the control plane; the product is the assistant itself, not just a gateway.
It remembers past conversations, can hand long work to a paired device or a leased cloud machine, and can learn repeatable procedures as skills.
Anonymous feature statistics are opt-in and off by default; update checks and bounded terminal update-outcome reports are on by default, and `update.checkOnStart: false` or `OPENCLAW_NO_AUTO_UPDATE=1` disables those update requests.

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
- Shared team deployment as configuration of the same Gateway (one trust domain; see `docs/start/multiplayer.md`)
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
- A centralized cloud service or hosted OpenClaw fleet run by the project (self-hosting is the default, and hosted services stay optional)
- A first-party enterprise SSO or RBAC product (named operator roles and reverse-proxy SSO integration are supported instead)
- A paid tier, hosted service, or token from the OpenClaw Foundation
- A core-repo native desktop app for Windows (Windows Hub lives in `openclaw/openclaw-windows-node`, and a Tauri desktop app is the backup)

## Key Constraints

- Node `>=24.16.0 <25 || >=26.1.0` runtime (Node 26 recommended), with opt-in Bun compatibility
- Single trust-domain architecture by design; team use shares one control plane, not multi-tenant isolation
- Plugin isolation via explicit import boundaries and capability gating; plugins import core only through `openclaw/plugin-sdk/*`
- Configuration is single-source-of-truth via `openclaw.json`; no silent config compat
- SQLite-first for all runtime state; no JSON/JSONL sidecar files for state
- PostgreSQL is a supported alternative engine (schema versions state 41, agent 43)
- Security-first: no secrets in logs, explicit trust model, rate limiting on auth
- TypeScript ESM strict throughout; no `any` outside test support files, discriminated unions for routing
- The Gateway process is the single owner of every OpenClaw database and its state; other processes route mutations through it
