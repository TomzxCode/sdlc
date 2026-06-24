# Project Overview

## Purpose

OpenChamber is a multi-runtime GUI client for [OpenCode](https://opencode.ai), an AI-powered coding assistant CLI.
It provides desktop (Electron, macOS), web/PWA, and VS Code extension interfaces so developers can interact with OpenCode sessions from any device.
The project solves the problem of OpenCode being terminal-only by adding rich visual workflows: branchable chat timelines, diff viewers, Git integration, integrated terminals, voice mode, multi-agent runs, and remote access via Cloudflare tunnels.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Bohdan Triapitsyn | Author and maintainer | Project direction, architecture, releases |
| OpenChamber contributors | Community developers | Contributing code, reporting bugs, feature requests |
| OpenCode users (developers) | End users | Rich GUI for AI-assisted coding across devices |
| Mobile/tablet users | End users | PWA access to remote OpenCode instances |
| VS Code users | End users | In-editor AI assistance via extension |

## Scope

**In scope:**

- Web/PWA frontend and Express server for hosting OpenCode sessions
- Electron desktop app (macOS; Windows and Linux planned)
- Tauri desktop app (legacy, maintenance-only for auto-update)
- VS Code extension with sidebar webview
- Shared UI component library (`@openchamber/ui`)
- CLI for starting, stopping, configuring, and tunneling the web server
- Cloudflare tunnel integration for remote access
- Git/GitHub workflows (commits, PRs, branch management, worktrees)
- Integrated terminal (ghostty-web, bun-pty/node-pty)
- Voice input (local Whisper) and text-to-speech output
- Multi-agent/multi-run sessions with isolated worktrees
- Skills catalog and local skill management
- Custom theming system with 18+ built-in themes
- Usage quota tracking across multiple AI providers
- Docker deployment support
- Localization/i18n (multiple languages including Polish, Chinese)

**Out of scope:**

- The OpenCode server itself (separate project at opencode.ai)
- Windows and Linux desktop apps (on roadmap, not yet implemented)
- Mobile native app (on roadmap)
- Linear integration (on roadmap)
- Built-in browser for running dev apps (on roadmap)

## Key Constraints

- OpenCode CLI must be installed as a prerequisite; OpenChamber is a UI layer, not an AI engine
- The Electron desktop boots the web server in-process; no sidecar subprocess
- Tauri desktop is legacy and receives no new features; kept only for auto-update migration
- Shared UI code (`packages/ui`) must work across web, desktop (both shells), and VS Code webview
- Node.js >= 22 required; Bun is the package manager and runtime for builds
- TypeScript strict mode enforced; no `any` without justification
- All UI colors must use theme tokens; no hardcoded color values or Tailwind color classes
- Icons must use the shared SVG sprite system; no direct `@remixicon/react` imports
- MIT licensed

