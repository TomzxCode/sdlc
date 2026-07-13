---
title: "Interactive Coding Agent"
status: done
---

# Specification: Interactive Coding Agent

## Overview

`pi-coding-agent` composes the three libraries into a CLI product.
`main()` parses args, resolves project trust, builds a `SessionManager` and `AgentSessionRuntime`, then dispatches to a run mode.
The `AgentSession` is the central class shared by all modes; `InteractiveMode` renders events via `pi-tui`.

## Architecture

```
cli.ts -> main() -------------------------------+
  args parse, migrations, trust resolve         |
  createSessionManager, createAgentSessionRuntime|
        |                                       |
        v                                       |
+-------------------+   owns session +          |
| AgentSession      |   cwd-bound services      |
| Runtime           |   (hot-swap on            |
+---------+---------+   fork/switch/tree)       |
          |                                   |
          v                                   |
+-------------------+   delegates to           |
| AgentSession      |----> pi-agent-core Agent |
| (prompt loop,     |----> ModelRegistry (auth)|
|  compaction, bash,|----> pi-ai streamSimple  |
|  tools, export)   |                          |
+---------+---------+                          |
          | events                             |
          v                                   |
   +------+------+------+                     |
   |             |      |                     |
   v             v      v                     |
Interactive   Print   RPC  <-- modes dispatch-+
Mode (pi-tui) (text/json)
```

## Data Models

### Settings (excerpt)

| Field | Type | Description |
|---|---|---|
| defaultModel | string | `provider/id:thinking` |
| transport | enum | `sse` / `websocket` / `auto` |
| compaction | object | Thresholds and behavior |
| extensions/skills/prompts/themes | string[] | Enabled resource globs |
| telemetry/analytics | object | Opt-in/out flags |
| projectTrust | object | Trust defaults |

### ResourceLoader sources

| Source | Path | Trust-gated |
|---|---|---|
| Global user | `~/.pi/agent/`, `~/.agents/` | No |
| Project | `.pi/`, `.agents/`, `AGENTS.md`, `CLAUDE.md` | Yes |
| Package | installed pi packages | Per-source |

### Tool sets

| Set | Tools |
|---|---|
| Default (4) | `read`, `bash`, `edit`, `write` |
| Read-only | `read`, `grep`, `find`, `ls` |

## API Contracts

### SDK: createAgentSession()

Factory building an `AgentSession` wired with a resource loader, model registry, settings, and extension runner.
Exposes `prompt`, `subscribe`, `state`, `abort`, `setModel`, `setThinkingLevel`, `compact`, `fork`.

### CLI flags (excerpt)

| Flag | Effect |
|---|---|
| `-p` / `--prompt` | Print mode (single-shot) |
| `--mode json` / `--mode rpc` | JSON event stream / RPC protocol |
| `-c` / `-r` / `--fork` / `--session` | Continue / resume / fork / specific session |
| `-t` / `-xt` / `-nbt` / `-nt` | Tool allowlist / exclude / no-builtin / none |
| `--model` / `--models` | Model / scoped cycling set |
| `--approve` / `--no-approve` | Non-interactive project trust |
| `--offline` | Disable startup network ops |

## Sequences

### Interactive prompt

```
user input -> AgentSession.prompt()
  -> slash command? extension command or builtin
  -> emit input event (extensions may transform/intercept)
  -> expand skill/template
  -> streaming? queue steer/follow-up
  -> validate model + auth
  -> check pre-prompt compaction
  -> before_agent_start (extensions modify system prompt / inject messages)
  -> Agent.prompt() -> agentLoop -> streamFn -> pi-ai
  -> stream deltas, execute tools, emit events
  -> _handlePostAgentRun: retry/compact/queued messages loop
  -> append entries to SessionManager JSONL
InteractiveMode renders events incrementally via pi-tui
```

### Run mode dispatch

```
main() -> resolveAppMode(args)
  interactive -> AgentSessionRuntime + InteractiveMode (TUI)
  print       -> runPrintMode (text or json)
  rpc         -> runRpcMode (JSONL stdin/stdout)
  (SDK)       -> createAgentSession() used programmatically
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Central class | `AgentSession` shared by all modes | One code path for prompt lifecycle across modes |
| Runtime hot-swap | `AgentSessionRuntime` recreates services | Clean state on fork/switch/tree without leaking cwd-bound resources |
| Core tools | Four only | Minimal core; more tools via extensions |
| No in-process sandbox | Delegate to external sandboxes | Core stays small; security boundary is the OS/container |
| Resource discovery | Global + project + package, trust-gated | User controls what project code executes |
| Modes | Interactive default; print/json/rpc alternatives | One binary serves TUI users, scripts, and embeddings |

## Risks and Unknowns

1. `InteractiveMode` is a very large module (~193KB); changes there are high-churn and hard to review.
2. Project trust is a security-critical path; regressions could execute untrusted code.
3. The package manager and resource discovery span many source locations; collision and precedence rules must stay consistent.

## Out of Scope

- Provider abstraction internals (FEAT-0001).
- Agent loop internals (FEAT-0002).
- TUI rendering internals (FEAT-0003).
- Extension/skills API surface (FEAT-0005).
- Session format and branching internals (FEAT-0006).
