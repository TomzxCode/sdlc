<!-- session_link -->
# Project Overview

## Purpose

Pi is a minimal, self-extensible terminal coding agent harness.
The core is deliberately small (four built-in tools, no sub-agents, no plan mode, no MCP, no permission popups) and is designed to be aggressively extended via TypeScript extensions, skills, prompt templates, themes, and pi packages.
The monorepo ships a unified multi-provider LLM API (`pi-ai`), a stateful agent runtime (`pi-agent-core`), a custom terminal UI framework with differential rendering (`pi-tui`), the interactive coding agent CLI built on top of the others (`pi-coding-agent`), the foundations for remote sessions: a transport-neutral CBOR protocol (`pi-protocol`), a transport-neutral remote session client (`pi-client`), a session server (`pi-server`), a SQLite session storage backend (`pi-session-backend-sqlite-node`), and a model-backed evals harness (`pi-evals`), plus an app-composition runtime with facets, services, and replicated state (`chord`, standalone with no Pi dependencies), a durable conversation, task, and document runtime with in-memory storage (`pi-durable`), and vendor-neutral telemetry contracts and spans (`pi-telemetry`).

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Mario Zechner (badlogic) | Author / maintainer | Project direction, core minimalism, all packages |
| Earendil Works | Publishing org | Releases, supply-chain hardening, npm trusted publishing |
| pi extension authors | SDK consumers | Stable extension/skills API, provider coverage, documentation |
| End users (developers) | CLI users | Interactive coding workflow, model choice, reliability |
| Open-source contributors | Issue/PR submitters | Clear contribution gate, quality bar, what belongs in core vs extension |

## Scope

**In scope:**

- Twelve workspace packages: `pi-ai`, `pi-agent-core`, `pi-tui`, `pi-coding-agent`, `pi-protocol`, `pi-client`, `pi-server`, `pi-session-backend-sqlite-node`, `pi-evals`, `chord`, `pi-durable`, `pi-telemetry`.
- A terminal coding agent with read, bash, edit, and write tools plus session management.
- An extension platform (custom tools, commands, events, UI, providers) that keeps the core minimal.
- Multi-provider LLM access across 30+ providers with automatic auth resolution, token/cost tracking, tool-calling, and streaming.
- An embeddable SDK and multiple run modes (interactive TUI, print, JSON, RPC).
- Remote sessions: a CBOR wire protocol, a transport-neutral client, a token-authenticated session server, and a SQLite session backend.
- The legacy p1-orchestrator code formerly under `pi-server` (`server/src/legacy`) is removed and out of scope.
- Behavioral, model-backed evals for measuring end-to-end workflow behavior.
- App composition via `chord`: facets, services, and replicated state as a standalone runtime with no Pi dependencies.
- Durable execution via `pi-durable`: conversation, task, and document runtimes with MemoryStorage.
- Vendor-neutral telemetry contracts and spans via `pi-telemetry`.
- Supply-chain hardening: pinned deps, lockfile governance, generated npm shrinkwrap, release smoke tests.

**Out of scope:**

- Built-in MCP support, sub-agents, plan mode, and permission popups (extensions may provide these).
- Chat/Slack automation (lives in the separate `earendil-works/pi-chat` repo).
- An in-process sandbox or permission system (containerization is delegated to external sandboxes like Gondolin, Docker, or OpenShell).
- Backward compatibility not explicitly requested by the maintainer.

## Key Constraints

- Node `>=22.19.0`, ESM only (`"type": "module"`).
- Erasable TypeScript syntax only in code checked by the root config (no enums, namespaces, parameter properties, `import =`, `export =`).
- Lockstep versioning: all packages share one version and release together (`patch` for fixes+additions, `minor` for breaking changes, no major releases).
- Direct external dependencies pinned to exact versions; `package-lock.json` is the dependency ground truth.
- Lockfile commits are blocked by pre-commit unless `PI_ALLOW_LOCKFILE_CHANGE=1` is set.
- `models.generated.ts` and `*.models.ts` are generated; never edited by hand (`npm run generate-models`).
- Core must stay minimal; features that belong as extensions will be rejected from core.
