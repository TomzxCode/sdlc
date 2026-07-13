# Project Overview

## Purpose

Hermes Agent is a persistent, self-improving personal AI agent built by Nous Research.
It runs the same agent core across five surfaces (CLI, TUI, messaging gateway, Electron desktop, and an API server) while maintaining memory, skills, and a deepening user model across sessions.
The agent autonomously creates and improves skills from its own experience, persists knowledge across conversations, and is reachable from wherever the user is — Telegram, Discord, Slack, Signal, WhatsApp, email, Matrix, Mattermost, Google Chat, IRC, Teams, Line, and a dozen more platforms — all from a single install that can run on infrastructure as cheap as a $5 VPS or serverless backends that hibernate when idle.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Individual power users | End users | A persistent AI assistant available across all devices and platforms with real terminal and browser access |
| Developers and researchers | Contributors | An agent with real terminal/browser automation, batch trajectory generation for training tool-calling models, and a plugin/skill extension system |
| Teams using messaging platforms | Operators | Automated workflows, scheduled reports, and multi-agent task boards via Telegram, Discord, Slack, etc. |
| Self-hosting enthusiasts | Operators | Run their own AI agent on their own infrastructure without vendor lock-in, using any LLM provider |
| Plugin and skill developers | Contributors | Extend the agent through plugins, skills, MCP servers, and platform adapters without modifying core files |

## Scope

**In scope:**
- Multi-platform personal AI agent (CLI, messaging, TUI, desktop, web dashboard)
- Persistent conversation store with full-text search and cross-session recall
- Autonomous skill creation and self-improvement from experience
- Real terminal and browser automation with multiple backend options
- Scheduled cron jobs that deliver results to any messaging platform
- Isolated subagent delegation for parallel work
- Plugin system for extensions (tools, memory providers, model providers, platform adapters)
- Model Context Protocol (MCP) client for external tool servers
- Multi-profile support for fully isolated agent instances
- Data-driven skin/theme system for CLI customization
- Multi-turn conversation with tool-calling LLMs (any OpenAI-compatible provider)

**Out of scope:**
- Outbound telemetry or usage attribution without explicit user opt-in
- New `HERMES_*` environment variables for non-secret configuration (behavioral settings go in `config.yaml`)
- New core model tools when the capability can be expressed as a CLI command + skill, service-gated tool, plugin, or MCP server
- Third-party product plugins integrated into the core tree (observability backends, vendor SaaS, analytics dashboards must ship as standalone plugin repos)
- New in-tree memory providers (the set of built-in providers under `plugins/memory/` is closed; new ones must ship as standalone repos)

## Key Constraints

- **Python 3.11 through 3.13** (capped below 3.14 for wheel compatibility)
- **Dependencies pinned with upper bounds** for supply-chain attack surface reduction (post-litellm compromise policy)
- **Per-conversation prompt caching is sacred:** system prompt must be byte-stable for the life of a conversation; mid-conversation context mutation is forbidden
- **The core is a narrow waist:** every model tool is sent on every API call, so new core tools are the last resort — capability lives at the edges via CLI + skill, service-gated tools, plugins, and MCP servers
- **All behavioral settings go in `config.yaml`;** `.env` is for secrets only (API keys, tokens, passwords)
- **Supported platforms:** Linux, macOS, native Windows (via PowerShell + portable MinGit), Windows via WSL2, Android via Termux