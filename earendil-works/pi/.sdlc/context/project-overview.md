<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Project Overview

## Purpose

Pi is a minimal, self-extensible terminal coding agent harness.
The core is deliberately small: four built-in tools are active by default (read, bash, edit, write), while grep, find, ls, and powershell exist but stay off by default.
The core has no sub-agents, no plan mode, and no built-in permission system.
Everything else is expected to arrive as TypeScript extensions, skills, prompt templates, themes, or Pi packages.
The monorepo ships a unified multi-provider LLM API with 42 built-in providers (`pi-ai`), a stateful agent runtime (`pi-agent-core`), a custom terminal UI framework with differential rendering (`pi-tui`), the interactive coding agent CLI built on top of the others (`pi-coding-agent`), a sandboxed script runtime where model-written JavaScript calls injected tools (`pi-codemode`), a standalone Model Context Protocol client (`pi-mcp`), remote execution environments for Durable over SSH (`pi-env`), a private model-backed evals harness (`pi-evals`), a typed host runtime with facets, services, and replicated state (`chord`), a durable conversation, task, and document runtime with in-memory, JSONL, and SQLite storage (`pi-durable`), and vendor-neutral telemetry contracts and spans (`pi-telemetry`).

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Mario Zechner (badlogic) | Author / maintainer | Project direction, core minimalism, all packages |
| Earendil Works | Publishing org | Releases, supply-chain hardening, npm trusted publishing |
| pi extension authors | SDK consumers | Stable extension/skills API, provider coverage, documentation |
| End users (developers) | CLI users | Interactive coding workflow, model choice, reliability |
| Open-source contributors | Issue/PR submitters | Clear contribution gate, quality bar, what belongs in core vs extension |

The maintainer name comes from the `author` field in `packages/ai/package.json` (and in the agent, coding-agent, telemetry, and tui packages).
The repository names no other maintainer roster, so the set of people with merge rights is not visible from the code.
"badlogic" is the legacy GitHub org named in changelog issue links and in `badlogic/pi-skills` and `badlogic/pi-share-hf` references, and it is the GitHub user that the issue triage workflow assigns `durable`-labelled issues to.

## Scope

**In scope:**

- Eleven workspace packages, ten published and `pi-evals` private: `pi-ai`, `pi-agent-core`, `pi-tui`, `pi-coding-agent`, `pi-codemode`, `pi-mcp`, `pi-env`, `pi-evals`, `chord`, `pi-durable`, `pi-telemetry`.
- A terminal coding agent with read, bash, edit, and write active by default, plus JSONL session management.
- An extension platform (custom tools, commands, events, UI, providers) that keeps the core minimal.
- Multi-provider LLM access across 42 built-in providers with automatic auth resolution, token/cost tracking, tool-calling, and streaming.
- An embeddable SDK and multiple run modes (interactive TUI, print, JSON, RPC).
- Built-in MCP integration via the `mcp` coding-agent extension backed by the standalone `pi-mcp` client (stdio, Streamable HTTP, and in-memory transports), with per-server and per-tool exposure modes and `/mcp` management.
- Sandboxed model-written scripting via the `codemode` coding-agent extension backed by `pi-codemode` (QuickJS VM compiled to WebAssembly, worker-thread execution on Node/Bun).
- Remote execution for Durable via `pi-env`: a small Rust daemon deployed over SSH plus a `RemoteExecutionEnv` client whose results match local execution.
- Durable execution via `pi-durable`: conversation, task, and document runtimes with MemoryStorage, JSONL, and SQLite (`src/storage/sqlite/`) backends.
- Behavioral, model-backed evals (`pi-evals`, private) that compare a with-docs and a without-docs agent variant and report the lift.
- App composition via `chord`: facets, services, contracts, and replicated state as a typed host runtime whose only monorepo dependency is `pi-telemetry`.
- Vendor-neutral telemetry contracts and spans via `pi-telemetry`.
- Supply-chain hardening: pinned deps, lockfile governance, generated npm shrinkwrap, release smoke tests.

**Out of scope:**

- Built-in sub-agents, plan mode, and a built-in permission system (extensions may provide these).
- Chat/Slack automation (lives in the separate `earendil-works/pi-chat` repo).
- An in-process sandbox or permission system (containerization is delegated to external sandboxes like Gondolin, Docker, or OpenShell).
- Backward compatibility not explicitly requested by the maintainer.

## Key Constraints

- Node `>=22.19.0`, ESM only (`"type": "module"`).
- Erasable TypeScript syntax only in code checked by the root config (no enums, namespaces, parameter properties, `import =`, `export =`).
- `npm run check` (Biome, pinned-dep and runtime-dep checks, import and entry-graph checks, install-lock check, `tsc --noEmit`, browser smoke) gates commits through the husky pre-commit hook.
- Contributors must run `npm run check` and `./test.sh` before a pull request, and must not edit `CHANGELOG.md` (maintainers add entries).
- Lockstep versioning: all packages share one version and release together (`patch` for fixes+additions, `minor` for breaking changes, no major releases).
- Direct external dependencies pinned to exact versions; `package-lock.json` is the dependency ground truth.
- `.npmrc` sets `save-exact=true` and `min-release-age=2`.
- Lockfile commits are blocked by pre-commit unless `PI_ALLOW_LOCKFILE_CHANGE=1` is set.
- GitHub Actions are pinned to commit SHAs, and CI installs with `npm ci --ignore-scripts`.
- `models.generated.ts` and `*.models.ts` are generated; never edit them by hand (`npm run generate:models`).
- Core must stay minimal; features that belong as extensions will be rejected from core.
