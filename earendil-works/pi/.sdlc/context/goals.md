<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Goals and Objectives

## Purpose

Pi is a minimal, self-extensible terminal coding agent harness designed to be the smallest viable core that can be aggressively extended via TypeScript extensions, skills, prompt templates, themes, and pi packages. The project solves the problem of an opinionated, production-ready coding assistant that stays small while supporting a rich ecosystem of extensions.

## Vision

Pi becomes the go-to open-source terminal coding agent for developers who want a minimal, fast, and extensible tool that respects their terminal and workflow.

## Time Horizon

- **Current period:** 2026 H2
- **Period type:** half

## Objectives

### Core Stability and Reliability

**Owner:** Maintainers
**Statement:** Ensure the core agent loop, session persistence, and TUI are reliable and performant.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Zero panics/crashes in the agent loop for basic usage | 100% test pass rate | CI test suite (`npm test` in the CI workflow) | — | On track |
| Session JSONL format remains stable with migration path | Format version documented | Version constant check (`CURRENT_SESSION_VERSION`) | v3, with v1 and v2 auto-migrated on load | On track |

### Provider Coverage

**Owner:** Maintainers
**Statement:** Maintain broad LLM provider coverage with automatic model discovery.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| 30+ providers supported | 30 | Model catalog | 42 built-in providers | On track |
| Model catalog regenerated on every CI run to `main` and published on a weekday schedule | Published on every scheduled run | CI scheduled job (`publish-model-catalog`), which has no uptime instrumentation | Weekday cron (Mon-Fri), publishing at 10:17, 12:17, and 14:17 Europe/Vienna | On track |

### Extension Ecosystem

**Owner:** Community
**Statement:** Grow the extension ecosystem with a stable API surface.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Extension API documented and versioned | Documentation published | docs/ completeness | Documented in `packages/coding-agent/docs/extensions.md`, with no API version constant | At risk |

## Strategic Pillars

- Minimalism: core stays small; features belong in extensions
- Reliability: no silent failures, no data loss
- Extensibility: well-designed API surface for the community
- Supply chain security: pinned deps, trusted publishing, lockfile governance

## Non-Goals

- Becoming a full IDE or replacing VS Code/Cursor
- Built-in sub-agents, plan mode, or a built-in permission system
- MCP implementation inside the core agent (it ships as the `mcp` coding-agent extension backed by `@earendil-works/pi-mcp`)
- Chat/Slack automation (lives in the separate `earendil-works/pi-chat` repo)

## Alignment

| Feature / Initiative | Objective | Notes |
|---|---|---|
| FEAT-0001 (LLM Provider Abstraction) | Provider Coverage | Core provider infrastructure |
| FEAT-0002 (Agent Runtime) | Core Stability | Agent loop reliability |
| FEAT-0003 (Terminal UI Framework) | Core Stability | TUI rendering stability |
| FEAT-0004 (Interactive Coding Agent) | Core Stability | CLI product |
| FEAT-0005 (Extension and Skills Platform) | Extension Ecosystem | Extension API |
| FEAT-0006 (Session Persistence and Branching) | Core Stability | Session format stability |

The p-prefixed features (p1 to p12) are shipped and cover remote sessions, SQLite session storage, evals, the durable runtime, chord, telemetry, codemode, the remote execution env, and the MCP client.
They are not mapped to an objective yet.

## Review Cadence

- **Review frequency:** quarterly
- **Last reviewed:** 2026-10-19
- **Next review:** 2027-01-19

## Open Questions

1. What is the timeline for stabilizing the ExtensionAPI as a versioned contract?
