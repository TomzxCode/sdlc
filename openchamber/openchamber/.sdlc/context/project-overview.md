# Project Overview

## Purpose

OpenChamber is a multi-runtime GUI client for [OpenCode](https://opencode.ai), an AI-powered coding assistant CLI.
It provides desktop (Electron, macOS/Windows/Linux), web/PWA, VS Code extension, and native mobile (iOS/Android) interfaces so developers can interact with OpenCode sessions from any device.
The project solves the problem of OpenCode being terminal-only by adding rich visual workflows: branchable chat timelines, diff viewers, Git integration, integrated terminals, voice mode, session goals, multi-agent runs, and remote access via Cloudflare tunnels, ngrok, or a private E2EE relay.

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
- Electron desktop app (macOS, Windows, and Linux)
- Native mobile apps (iOS and Android) via Capacitor with push notifications and QR pairing
- Capacitor mobile app (iOS and Android) with native push notifications and QR pairing
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
- Private relay for E2EE remote access without open ports or third-party tunnels
- Session goals for autonomous AI-driven multi-turn execution with audit
- Streaming dictation (local sherpa-onnx or OpenAI-compatible Whisper endpoints)
- Docker deployment support
- Desktop SSH remote host management with port forwarding
- Startup service (systemd, launchd) integration
- Localization/i18n (multiple languages including Polish, Chinese)

**Out of scope:**

- The OpenCode server itself (separate project at opencode.ai)
- Tauri desktop app (legacy, maintenance-only for auto-update migration)
- Linear integration (on roadmap)
- Built-in browser for running dev apps (on roadmap, preview browser exists for local dev servers)

## Key Constraints

- OpenCode CLI must be installed as a prerequisite; OpenChamber is a UI layer, not an AI engine
- The Electron desktop boots the web server in-process; no sidecar subprocess
- Tauri desktop is legacy, receives no new features, and is kept for auto-update migration
- Private relay is the default remote-access method when available; no open ports or third-party tunnels required
- Shared UI code (`packages/ui`) must work across web, desktop (both shells), and VS Code webview
- Node.js >= 22 required; Bun 1.3 is the package manager and runtime for builds
- TypeScript strict mode enforced; no `any` without justification
- All UI colors must use theme tokens; no hardcoded color values or Tailwind color classes
- Icons must use the shared SVG sprite system; no direct `@remixicon/react` imports
- MIT licensed

