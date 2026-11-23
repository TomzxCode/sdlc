<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->

# Project Overview

## Purpose

OpenCode is an open source AI coding agent that runs locally and assists with software engineering tasks.
It exposes a durable session runtime that preserves conversational history while assembling the system context an agent needs to act correctly in its current environment.
Users interact with it through a terminal UI, a web and desktop app, a headless HTTP API, or editor integrations such as the VSCode extension.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| OpenCode core team | Maintainers | Architecture integrity, review gates, release cadence |
| Contributors | External developers | Clear contribution path, style guide, good first issues |
| End users (developers) | CLI / desktop / web users | Reliable agent sessions, provider choice, low latency |
| Plugin / SDK authors | Integrators | Stable plugin API, generated SDK, MCP compatibility |
| Operators | Self-hosters | Headless server, authentication, policy, and multi-project support |

## Scope

**In scope:**
- A durable, replayable session runtime with prompt admission, model calls, compaction, and instruction deltas.
- Multiple frontends: terminal UI (TUI), web app, and Electron desktop app.
- A headless HTTP API server exposing project, session, message, config, and event routes.
- An LLM provider layer with a model catalog, provider adapters in `packages/ai`, and a Claude Agent provider built into `packages/core`.
- Policy evaluation for providers, tools, integrations, MCP servers, skills, plugins, and web search, with organization-managed statements delivered by OpenCode Console.
- An agent and tool system with built-in tools, permissions, and skills.
- A plugin system with namespaced hooks, plus a generated TypeScript client, an embeddable SDK, and a VSCode extension.
- A CodeMode engine for confined, schema-described code execution over explicit tools.
- An Agent Client Protocol (ACP) implementation for use from ACP-compatible editors.
- Independently deployed services for the website and docs, data, public files, release metadata, and legacy endpoints.

**Out of scope:**
- Hosting or managing the user's code repositories (OpenCode operates on local directories only).
- Training or fine-tuning models (it consumes existing providers).
- General-purpose chat outside a coding/project context.
- The retired OpenCode GitHub Action, which is no longer published.

## Key Constraints

- Runtime is Bun 1.4.4 or newer on TypeScript, and Bun workspaces cover `packages/*`, `packages/plugins/*`, `services/*`, and `packages/data/*`.
- Provider support is data-driven via models.dev, so new providers should require little or no code change.
- The AI package (`packages/ai`) is a standalone Effect-first abstraction that can be consumed independently of the rest of OpenCode.
- V2 session core separates durable prompt admission from model execution and keeps execution process-local until clustering is implemented.
- Runtime dependencies flow from Schema to Core and Protocol, then to Server.
- Client runtime code may depend on Schema and Protocol but never Core or Server, and SDK composes Client, Core, and Server.
- Changing the public Protocol or Server `HttpApi` requires running `bun run generate` from `packages/client`, and generated client files are never edited directly.
- This repository does not use Changesets, and releases follow the existing release workflow.
- New user-visible behavior, risky core changes, and work not ready to release require a feature flag in `packages/schema/src/config/flag.ts`.
- UI and core product features require design review before implementation.
- Bug fixes, chores, and tests must reference an existing issue, while documentation, refactor, and feature PRs are exempt from the automated linked-issue check.
- The default branch is `dev`, and branches and PRs target `dev`.
