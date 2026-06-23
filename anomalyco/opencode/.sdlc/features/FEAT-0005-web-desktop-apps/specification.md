---
title: "Web & Desktop Apps"
status: draft
---

# Specification: Web & Desktop Apps

## Overview

`packages/app` provides the shared SolidJS web UI consumed by both the browser experience and the Electron desktop shell.
`packages/desktop` wraps that UI, bundles a local server, and produces cross-platform installers via its build/package scripts.

## Architecture

```
Browser ──▶ web app (packages/app, SolidJS + Vite + Tailwind)
                 │ shared components (packages/ui)
Electron shell (packages/desktop) ── wraps ──▶ web app
                 │
                 ▼
          local OpenCode server
```

## Data Models

The apps consume server-projected `Message`/`Part` and config shapes; they hold no durable model beyond local UI/session view state.

## API Contracts

The apps consume the HTTP API (see FEAT-0006).

## Sequences

### Desktop launch

```
Electron main -> start local server (default port 4096)
Electron -> load web app (bundled or dev server)
web app -> connect to local server -> render sessions
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Shared UI | `packages/app` + `packages/ui` | Single component library across web and desktop |
| Desktop shell | Electron | Cross-platform native packaging with a web UI |
| Dev workflow | Web dev server hot-reloads independent of core server | Faster UI iteration |

## Risks and Unknowns

1. Auto-update cadence and mechanism across macOS, Windows, and Linux are not fully specified here.
2. Parity between graphical and TUI capabilities must be maintained as features land.

## Out of Scope

- Terminal UI (see FEAT-0004).
- Server implementation (see FEAT-0006).
