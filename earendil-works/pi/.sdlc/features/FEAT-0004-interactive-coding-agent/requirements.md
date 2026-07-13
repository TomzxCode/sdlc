---
title: "Interactive Coding Agent"
status: done
---

# Requirements: Interactive Coding Agent

## Overview

`pi-coding-agent` is the CLI product: a minimal terminal coding harness built around four core tools (read, bash, edit, write), designed to be extended.
It wires `pi-ai`, `pi-agent-core`, and `pi-tui` into an `AgentSession` that drives prompts, manages models and thinking levels, executes built-in tools, and renders an interactive TUI.
It also exposes print, JSON, and RPC modes plus an embeddable SDK.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users (developers) | A reliable interactive coding workflow with model choice and responsive UI |
| Extension / SDK authors | A stable SDK surface and clear extension boundaries |
| Maintainers | A minimal core that stays small; features belong in extensions when possible |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `pi` CLI with an interactive TUI as the default mode. |
| FR-02 | Must | The system shall provide four default built-in tools: `read`, `bash`, `edit`, `write`, and a read-only tool set (`read`, `grep`, `find`, `ls`). |
| FR-03 | Must | The system shall provide an `AgentSession` core that drives the prompt loop, manages model and thinking level, runs compaction, executes bash, and exports HTML. |
| FR-04 | Must | The system shall resolve model selection via `provider/id:thinking` patterns, scoped model cycling, and in-TUI `/model` and `/scoped-models` commands. |
| FR-05 | Must | The system shall provide built-in slash commands (`settings`, `model`, `export`, `fork`, `tree`, `login`, `logout`, `new`, `compact`, `resume`, `reload`, `quit`, and others). |
| FR-06 | Must | The system shall support run modes: interactive (default), print (`-p`), JSON (`--mode json`), RPC (`--mode rpc`), and SDK. |
| FR-07 | Must | The system shall provide global and project settings (`~/.pi/agent/settings.json`, `.pi/settings.json`) with file locking and deep merge, plus keybindings. |
| FR-08 | Must | The system shall gate project resources (settings, extensions, context files) behind a project-trust decision. |
| FR-09 | Must | The system shall discover and load resources (extensions, skills, prompt templates, themes, AGENTS.md/CLAUDE.md) from global, project, and package sources. |
| FR-10 | Must | The system shall build the system prompt from base prompt, project context, skills, date, and cwd. |
| FR-11 | Should | The system shall support theme loading (JSON themes, light/dark auto, hot-reload). |
| FR-12 | Should | The system shall provide update-check and install-telemetry endpoints, disable-able via env flags or `--offline`. |
| FR-13 | Should | The system shall support first-time setup flow (theme + analytics opt-in) behind an experimental flag. |
| FR-14 | May | The system shall provide a `pi install/remove/update/list/config` package manager for pi packages (npm/git). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | The package shall target Node `>=22.19.0` and use erasable TypeScript syntax only. |
| NFR-02 | Must | Reliability | A hot-swap runtime shall tear down and recreate cwd-bound services when switching sessions or cwds. |
| NFR-03 | Must | Security | The system shall not include an in-process sandbox; containerization is delegated to external sandboxes (documented). |
| NFR-04 | Should | Performance | Startup shall defer non-essential network operations when `--offline` / `PI_OFFLINE=1` is set. |
| NFR-05 | Should | Maintainability | The published CLI shall include a generated npm shrinkwrap pinning transitive deps. |

## Constraints

- Core is minimal: no built-in MCP, sub-agents, plan mode, or permission popups (extensions provide these).
- Direct dependencies pinned to exact versions; lockfile is ground truth.
- New issues/PRs from new contributors are auto-closed by default (maintainer gate).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-02**
    - **Given** a default agent session
    - **When** tools are registered
    - **Then** `read`, `bash`, `edit`, `write` are available, and the read-only set restricts to `read`, `grep`, `find`, `ls`.
- [ ] **FR-03**
    - **Given** a user prompt
    - **When** submitted to `AgentSession.prompt()`
    - **Then** it expands commands/templates, emits lifecycle events, streams the response, executes tools, handles retries/compaction, and persists entries to the session file.
- [ ] **FR-06**
    - **Given** the CLI invoked with `-p`, `--mode json`, `--mode rpc`, or no flag
    - **When** it starts
    - **Then** it runs in print, JSON, RPC, or interactive mode respectively.
- [ ] **FR-08**
    - **Given** an untrusted project
    - **When** the agent starts
    - **Then** project resources are not loaded until a trust decision is recorded (or `--approve` is passed non-interactively).
- [ ] **NFR-02**
    - **Given** an active interactive session
    - **When** the user switches sessions or cwd via `/fork` or `/tree`
    - **Then** the runtime tears down and recreates cwd-bound services without leaking state.

## Conflicts

None identified yet.

## Open Questions

1. Should the experimental first-time setup flow graduate to default behavior, and on what timeline?
2. What is the policy for promoting a widely-used extension into a built-in tool or command?
