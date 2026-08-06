---
title: "Loopany Daemon & CLI"
status: done
---

# Requirements: Loopany Daemon & CLI

## Overview

The daemon (`@crewlet/loopany`) is the machine-side half of Loopany: one binary with two roles. As a poll-loop daemon it connects to a server, polls for due runs, and executes them with the user's local coding agent (Claude Code, Codex, or Grok). As the in-run `loopany` callback it lets the agent report results, adjust the loop's schedule/dashboard, and finish closed loops. It also owns the user-facing CLI (up/status/down/log/new/edit/show/home/skill/setup/update), the loop-folder watcher, transient-failure resume, the cwd jail, the PATH shim, and the best-effort install of the public skill and SessionStart hooks.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop operator | Low-friction install and connect, a content-first home, and honest status; credentials and files stay local. |
| Agent session | The in-run callback is reachable with the exact verbs the server advertises; help never has side effects. |
| Server operator | The daemon forwards whatever credential its env carries; old servers degrade gracefully (TOON text vs `SERVER_TOO_OLD`). |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The daemon shall classify every invocation in a pure router and map the route to its handler, with `--help`/`-h` short-circuiting to per-verb usage before any side effect. |
| FR-2 | Must | The daemon shall run as a poll loop (detached via `up`, foreground via `up --foreground`), polling with an opt-in long-poll when idle. |
| FR-3 | Must | The in-run callback (when `LOOPANY_RUN_TOKEN` is set) shall win over every other route, including bare `loopany` (which posts `home` on the run credential). |
| FR-4 | Must | The daemon shall spawn the loop's coding agent based on `loops.agent` (claude-code / codex / grok) with the correct CLI flags and env forwarding. |
| FR-5 | Must | A transient coding-agent crash shall resume the session (`--resume`) with a short continuation prompt, up to `LOOPANY_TRANSIENT_RETRIES` attempts. |
| FR-6 | Must | The daemon shall report runs through the run credential and print the server's TOON `text` + `exitCode` for every server verb. |
| FR-7 | Must | The daemon shall enforce a cwd jail (`LOOPANY_ROOTS`) and an allowlisted child environment. |
| FR-8 | Must | The daemon shall install the public skill for every known coding agent on `up`/`new`, best-effort and never blocking. |
| FR-9 | Should | The daemon shall install SessionStart hooks for Claude Code, Codex, and Grok via shared JSON merge logic, gated on a durable on-PATH `loopany`. |
| FR-10 | Should | The daemon shall maintain a pidfile `<pid>:<startTime>` so a reused pid never reads as the live daemon. |
| FR-11 | Should | The daemon shall write a version-consistent PATH shim (or use a durable PATH global) and report it as `bin:`. |
| FR-12 | Should | The daemon shall forward out-of-run `report`/`finish`/`complete` so the server's crafted run-only 403 reaches the agent. |
| FR-13 | Should | The daemon shall report loop-creation milestones via `loopany progress <step> --connect-key <key>` (best-effort). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The device token passes to the child via env, never argv (ps-visible). |
| NFR-2 | Must | Reliability | A run whose server has gone text-less (too old) surfaces a definitive `SERVER_TOO_OLD` error, never blank output. |
| NFR-3 | Must | Security | `ensureBinShim`/`refreshHooks` must never clobber a foreign `loopany` or write the real home when running under tests. |
| NFR-4 | Should | Operability | All external touches (process/network/fs) are injectable seams so tests never need a real process or network. |
| NFR-5 | Should | Performance | An idle poll should re-poll quickly after a server hold and sleep out the poll interval after a fast answer. |
| NFR-6 | Should | Reliability | The SessionStart home fetch must be bounded so a hung server degrades to a definitive home, never stalling session start. |

## Constraints

- The daemon spawns a coding agent that runs with the user's credentials; it is the highest-permission surface and is continuously hardened.
- The workflow subprocess runs bare node; the MCP bridge is plain ESM on purpose.
- `report`/`finish` reject an invalid `--status` with a 400 `VALIDATION_ERROR` (fail loud).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** `loopany up --foreground --help`
    - **When** it is parsed
    - **Then** the per-verb help prints and the poll loop never launches
- [ ] **FR-2**
    - **Given** `loopany up` on a fresh machine
    - **When** it runs
    - **Then** a detached daemon polls the server and an idle poll opts into `wait:true`
- [ ] **FR-3**
    - **Given** a run with `LOOPANY_RUN_TOKEN` set
    - **When** the agent types bare `loopany`
    - **Then** the callback posts `home` on the run credential
- [ ] **FR-4**
    - **Given** a loop bound to `codex`
    - **When** the run starts
    - **Then** the daemon spawns `codex exec` with the correct flags and env
- [ ] **FR-5**
    - **Given** a claude crash classified transient
    - **When** the run retries
    - **Then** it resumes the prior session and spend is summed across attempts
- [ ] **FR-6**
    - **Given** any server verb
    - **When** the server returns
    - **Then** the daemon prints `body.text` and exits with `body.exitCode`
- [ ] **FR-7**
    - **Given** a server-sent root outside `LOOPANY_ROOTS`
    - **When** the daemon resolves it
    - **Then** the cwd jail narrows, never widens
- [ ] **FR-8**
    - **Given** `loopany up`
    - **When** the skill install runs
    - **Then** the skill lands at user scope for every `SKILL_TARGET_AGENTS`, best-effort
- [ ] **NFR-1**
    - **Given** a spawned agent process
    - **When** the command is built
    - **Then** the device token appears only in env, never in argv
- [ ] **NFR-2**
    - **Given** a pre-0.12 server returning no `text`
    - **When** a device verb is invoked
    - **Then** `SERVER_TOO_OLD` is printed to stdout, exit 1

## Conflicts

None identified yet.

## Open Questions

1. None: the daemon behavior is fully determined by the code and its tests.
