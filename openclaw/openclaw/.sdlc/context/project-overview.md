# Project Overview

## Purpose

OpenClaw is a personal AI assistant that runs on user-owned devices.
It answers users on the messaging channels they already use (WhatsApp, Telegram, Slack, Discord, iMessage, and 30+ others), can speak and listen on macOS/iOS/Android, and renders a live Canvas/Control UI for rich interaction.
The Gateway is the control plane — the product is the assistant itself, not just a gateway.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| End users | Individual operators | A fast, private, always-on AI assistant on their preferred channels |
| Plugin developers | Community contributors | A well-documented SDK to build and distribute extensions |
| Maintainers | Core team | Project stability, security, compatibility, and community health |
| Sponsors (OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, Convex) | Funding and infrastructure partners | Adoption and ecosystem growth |

## Scope

**In scope:**
- Multi-channel messaging integration for 30+ platforms
- AI agent execution with support for major model providers (OpenAI, Anthropic, Google, open-source, etc.)
- CLI for configuration, plugin management, and operations
- Web-based Control UI for chat and administration
- Plugin system with SDK for community extensions
- Companion apps for macOS, iOS, Android, Windows
- Agent tool system (bash, file I/O, web search, image generation, etc.)
- Configuration via `openclaw.json` with JSON schema validation
- Session management, conversation persistence, and context compaction

**Out of scope:**
- Multi-user/multi-tenant SaaS hosting (single-user, self-hosted design)
- Centralized cloud service (runs on user's own infrastructure)
- Formal enterprise SSO or RBAC
- Native desktop app beyond macOS (Linux/Windows via CLI only; Windows Hub companion app available)

## Key Constraints

- Node 22.22.3+ runtime (Node 24 recommended), with Bun compatibility
- Single-user architecture by design; no multi-tenant isolation
- Plugin isolation via explicit import boundaries and capability gating
- Configuration is single-source-of-truth via `openclaw.json`; no silent config compat
- SQLite-first for all runtime state; no JSON/JSONL sidecar files for state
- Security-first: no secrets in logs, explicit trust model, rate limiting on auth
- TypeScript ESM strict throughout; no `any` types, discriminated unions for routing
