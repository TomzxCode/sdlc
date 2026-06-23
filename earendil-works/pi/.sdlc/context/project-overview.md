# Project Overview

## Purpose

Pi is a minimal, self-extensible terminal coding agent harness.
The core is deliberately small (four built-in tools, no sub-agents, no plan mode, no MCP, no permission popups) and is designed to be aggressively extended via TypeScript extensions, skills, prompt templates, themes, and pi packages.
The monorepo ships four libraries: a unified multi-provider LLM API (`pi-ai`), a stateful agent runtime (`pi-agent-core`), a custom terminal UI framework with differential rendering (`pi-tui`), and the interactive coding agent CLI built on top of all three (`pi-coding-agent`).

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

- Four workspace packages: `pi-ai`, `pi-agent-core`, `pi-tui`, `pi-coding-agent`.
- A terminal coding agent with read, bash, edit, and write tools plus session management.
- An extension platform (custom tools, commands, events, UI, providers) that keeps the core minimal.
- Multi-provider LLM access across 30+ providers with automatic auth resolution, token/cost tracking, tool-calling, and streaming.
- An embeddable SDK and multiple run modes (interactive TUI, print, JSON, RPC).
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
