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
| Zero panics/crashes in the agent loop for basic usage | 100% test pass rate | CI test suite | — | On track |
| Session JSONL format remains stable with migration path | Format version documented | Version constant check | — | On track |

### Provider Coverage

**Owner:** Maintainers
**Statement:** Maintain broad LLM provider coverage with automatic model discovery.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| 30+ providers supported | 30 | Model catalog | 30+ | On track |
| Model catalog auto-generated daily | 100% uptime of generation | CI scheduled job | — | On track |

### Extension Ecosystem

**Owner:** Community
**Statement:** Grow the extension ecosystem with a stable API surface.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Extension API documented and versioned | Documentation published | docs/ completeness | — | At risk |

## Strategic Pillars

- Minimalism: core stays small; features belong in extensions
- Reliability: no silent failures, no data loss
- Extensibility: well-designed API surface for the community
- Supply chain security: pinned deps, trusted publishing, lockfile governance

## Non-Goals

- Becoming a full IDE or replacing VS Code/Cursor
- Built-in MCP, sub-agents, plan mode, or permission popups
- Chat/Slack automation (lives in pi-chat)

## Alignment

| Feature / Initiative | Objective | Notes |
|---|---|---|
| FEAT-0001 (LLM Provider Abstraction) | Provider Coverage | Core provider infrastructure |
| FEAT-0002 (Agent Runtime) | Core Stability | Agent loop reliability |
| FEAT-0003 (Terminal UI Framework) | Core Stability | TUI rendering stability |
| FEAT-0004 (Interactive Coding Agent) | Core Stability | CLI product |
| FEAT-0005 (Extension Platform) | Extension Ecosystem | Extension API |
| FEAT-0006 (Session Persistence) | Core Stability | Session format stability |

## Review Cadence

- **Review frequency:** quarterly
- **Last reviewed:** 2026-07-20
- **Next review:** 2026-10-01

## Open Questions

1. What is the timeline for stabilizing the ExtensionAPI as a versioned contract?
