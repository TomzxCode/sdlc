# sdlc

A central workspace that holds the SDLC (Software Development Lifecycle) artifacts, context, and feature specifications for several open-source AI projects, organized under `{organization}/{repository}/.sdlc/`.

## What

This repository contains no application code. It is a documentation workspace that tracks the requirements, specifications, architecture, and knowledge records for a set of upstream open-source projects in one place. Each project lives under its own `{org}/{repo}/` directory, which mirrors its GitHub path, and holds a `.sdlc/` tree of markdown artifacts produced by the SDLC skill pipeline (needs, requirements, specifications, plans, tests, decisions, assumptions, learnings).

## Why

Keeping the specification work for multiple projects in a single workspace makes it easy to cross-reference architecture, share conventions, and run the same SDLC pipeline (review, sync, backpropagation) consistently across projects. The upstream code repositories stay focused on code, while this workspace holds the durable planning and design artifacts that precede and guide implementation.

## Included

**Tracked projects:**

| Directory | Project | Description |
|---|---|---|
| [`1jehuang/jcode`](1jehuang/jcode/.sdlc) | [J-Code](https://github.com/1jehuang/jcode) | Terminal AI coding agent harness (fork of sst/opencode) with an always-on daemon, RAM-efficient TUI, multi-provider auth, and agent memory |
| [`anomalyco/opencode`](anomalyco/opencode/.sdlc) | [OpenCode](https://github.com/anomalyco/opencode) | Open source AI coding agent with a durable session runtime, terminal/web/desktop UIs, and a headless API |
| [`earendil-works/pi`](earendil-works/pi/.sdlc) | [Pi](https://github.com/earendil-works/pi) | Minimal, self-extensible terminal coding agent harness (`pi-ai`, `pi-agent-core`, `pi-tui`, `pi-coding-agent`) |
| [`kenn-io/agentsview`](kenn-io/agentsview/.sdlc) | [agentsview](https://github.com/kenn-io/agentsview) | Local web viewer for AI agent sessions with FTS5 search, cost tracking, analytics, and live SSE updates |
| [`NousResearch/hermes-agent`](NousResearch/hermes-agent/.sdlc) | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Persistent, self-improving personal AI agent running one core across CLI, TUI, messaging gateways, desktop, and API |
| [`openchamber/openchamber`](openchamber/openchamber/.sdlc) | [OpenChamber](https://github.com/openchamber/openchamber) | Multi-runtime GUI client for OpenCode (Electron, web/PWA, VS Code) |
| [`openclaw/openclaw`](openclaw/openclaw/.sdlc) | [OpenClaw](https://github.com/openclaw/openclaw) | Personal AI assistant on user-owned devices across 30+ messaging channels with a Control UI and plugin SDK |
| [`paperclipai/paperclip`](paperclipai/paperclip/.sdlc) | [Paperclip](https://github.com/paperclipai/paperclip) | Open-source control plane for autonomous AI-agent companies |
| [`Runfusion/Fusion`](Runfusion/Fusion/.sdlc) | [Fusion](https://github.com/Runfusion/Fusion) | Model-agnostic multi-agent orchestrator that drives a task board through plan/build/review/merge behind a human approval gate |
| [`superdesigndev/loopany-platform`](superdesigndev/loopany-platform/.sdlc) | [Loopany](https://github.com/superdesigndev/loopany-platform) | Multi-user scheduled-loop manager where a zero-exec server schedules and notifies, with bring-your-own-agent execution on each user's machine |

## Getting Started

This workspace is consumed by the [SDLC skill](https://github.com/tomzx/agents/tree/main/skills/sdlc). To work on a project's artifacts:

1. Browse to `{org}/{repo}/.sdlc/context/project-overview.md` to understand the project's purpose and scope.
2. Read the relevant `features/FEAT-NNNN-*/` artifacts (requirements then specification) to see what a feature must do and how it is designed.
3. Run SDLC skills against a project directory, e.g. `sync-sdlc`, `sdlc-status`, `backpropagate-sdlc`, or the full `sdlc` pipeline.

## License

This workspace aggregates specifications for upstream open-source projects, each licensed under the terms stated in its own repository (see the links above). No application code is hosted here.
