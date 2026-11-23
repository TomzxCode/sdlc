# Project Overview

## Purpose

OpenChamber is a multi-runtime GUI workspace for running and reviewing AI coding work, built around [OpenCode](https://opencode.ai).
It provides desktop (Electron, macOS/Windows/Linux), web/PWA, VS Code extension, and mobile (iOS and Android via Capacitor) interfaces so developers can work with OpenCode sessions from any device.
It solves the problem of OpenCode being terminal-only by adding visual workflows: branchable chat timelines, diff viewers, source control integration, integrated terminals, voice mode, session goals, multi-agent runs, AI-guided changes walkthroughs, diagram editing, and remote access via Cloudflare tunnels, ngrok, SSH, Tailscale Serve/Funnel, or a private E2EE relay.

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
- Capacitor mobile apps (iOS and Android) with native push notifications and QR pairing
- VS Code extension with sidebar webview
- Shared UI component library (`@openchamber/ui`)
- CLI for starting, stopping, configuring, and tunneling the web server
- Cloudflare tunnel integration for remote access
- Git/GitHub workflows (commits, PRs, branch management, worktrees)
- Linear integration (OAuth, issue lookup, team-to-project mapping, status updates, session status comments)
- Integrated terminal (ghostty-web, bun-pty/node-pty)
- Voice input (streaming dictation, local sherpa-onnx or OpenAI-compatible Whisper endpoints) and text-to-speech output
- Multi-agent/multi-run sessions with isolated worktrees
- Skills catalog and local skill management
- AI-guided changes walkthrough that turns a diff into an ordered tour of stops and chapters
- DrawIO-based diagram editor for editing `.drawio`/`.xml` diagram files
- Agent manager for organizing agent groups and launching multi-runs from them
- Control plane (`openchamber control` CLI) and the managed `openchamber` agent tool for scripting agent runs
- Custom theming system with 18+ built-in themes
- Usage quota tracking across multiple AI providers
- Private relay for E2EE remote access without open ports or third-party tunnels
- Session goals for autonomous AI-driven multi-turn execution with audit
- Docker deployment support
- Desktop SSH remote host management with port forwarding
- Startup service (systemd, launchd) integration
- Localization/i18n (12 locales including German, French, Japanese, Korean, Polish, Chinese simplified and traditional)
- Isolated spaces backend (Docker place and space manager, stage 1a, unwired: no routes, settings, or UI yet)
- `@openchamber/sdk` guest contract and app-owned extensions (`packages/sdk`, `packages/extensions`)
- Multi-provider source control for GitHub, GitLab, Gitea, Gerrit, and Forgejo with provider-neutral change requests and repository bindings
- Provider-neutral issue trackers with live tracked items
- Agent workflows and session leads
- Session work, todos, drafts, and warming
- Shared render pages with local image grants
- Tailscale Serve and Funnel remote access
- Permission auto-accept policy
- Diagnostics timeline
- Enterprise admin policy
- Canary nightly release channel
- Nix packages for the server and desktop
- Signed Windows installers
- Linux `.deb`, `.rpm`, and AppImage packages with an R2 release mirror
- Behavior-net nightly verification

**Out of scope:**

- The OpenCode server itself (separate project at opencode.ai); desktop and CLI/web bundle a matching build
- A full built-in browser for running dev apps (on roadmap; a preview browser for local dev servers and a desktop built-in browser for arbitrary web pages exist)
- A persistent database, analytics, or observability platform

## Key Constraints

- Desktop and CLI/web bundle a matching OpenCode CLI/server build, so a separate OpenCode installation is not required; the VS Code extension still uses the user's installed OpenCode CLI
- The Electron desktop boots the web server in-process; no sidecar subprocess
- Private relay is the default remote-access method when available; no open ports or third-party tunnels required
- Shared UI code (`packages/ui`) must work across web, desktop (Electron), and VS Code webview
- Node.js >= 24.14 required (`.nvmrc` is `lts/krypton`); Bun 1.4.5 is the package manager; TypeScript ~7.0.2; Electron 45
- TypeScript strict mode enforced; no `any` without justification
- All UI colors must use theme tokens; no hardcoded color values or Tailwind color classes
- Icons must use the shared SVG sprite system; no direct `@remixicon/react` imports
- MIT licensed
