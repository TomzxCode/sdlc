# Service Levels

## Overview

OpenChamber is a self-hosted GUI client for OpenCode. The primary "service" is the Express web server that serves the UI and proxies AI requests. Formal SLOs are not yet defined for this project; this file is a placeholder until service-level targets are established.

## Scope

**Services in scope:**
- OpenChamber Express server (web UI, API, SSE events)
- OpenChamber Electron desktop app
- OpenChamber VS Code extension
- Private relay infrastructure (remote access)

**Out of scope:**
- OpenCode CLI (external dependency)
- AI model provider APIs (external dependency)
- Cloudflare tunnel / ngrok infrastructure (third-party)

## Open Questions

1. Formal SLOs, SLIs, and error budgets have not been defined for any OpenChamber service. These should be established as the project matures toward production use.
2. What are the acceptable latency targets for SSE streaming (chat response perception)?
3. What uptime targets apply to self-hosted deployments (user-dependent)?
