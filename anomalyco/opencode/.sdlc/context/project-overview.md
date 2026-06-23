# Project Overview

## Purpose

OpenCode is an open source AI coding agent that runs locally and assists with software engineering tasks.
It exposes a durable session runtime that preserves conversational history while assembling the system context an agent needs to act correctly in its current environment.
Users interact with it through a terminal UI, a web/desktop app, a headless HTTP API, or editor integrations such as the VSCode extension.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| OpenCode core team | Maintainers | Architecture integrity, review gates, release cadence |
| Contributors | External developers | Clear contribution path, style guide, good first issues |
| End users (developers) | CLI / desktop / web users | Reliable agent sessions, provider choice, low latency |
| Plugin / SDK authors | Integrators | Stable plugin API, generated SDK, MCP compatibility |
| Operators | Self-hosters / enterprise | Headless server, observability, auth, multi-project support |

## Scope

**In scope:**
- A durable, replayable session runtime with provider turns, compaction, and a system context algebra.
- Multiple frontends: terminal UI (TUI), web app, Electron desktop app.
- A headless HTTP API server exposing project, session, message, and config routes.
- An LLM provider layer with a model catalog and provider adapters.
- An agent and tool system with built-in tools, permissions, and skills.
- A plugin system with namespaced hooks, plus a generated TypeScript SDK and editor integrations.

**Out of scope:**
- Hosting or managing the user's code repositories (OpenCode operates on local directories only).
- Training or fine-tuning models (it consumes existing providers).
- General-purpose chat outside a coding/project context.

## Key Constraints

- Runtime is Bun 1.3+ on TypeScript; packages are distributed as a Bun workspace monorepo.
- Provider support is data-driven via models.dev, so new providers should require little or no code change.
- V2 session core separates durable prompt admission from model execution and keeps execution process-local until clustering is implemented.
- UI/core product features require design review with the core team before implementation.
- All PRs must reference an existing issue; issue-first policy is enforced.
- The project uses a vouch/denounce trust system for contributor governance.
