---
title: "Terminal and Browser Automation"
status: draft
---

# Specification: Terminal and Browser Automation

## Overview

Terminal execution uses a backend abstraction: each environment (local, Docker, SSH, Modal, Daytona, Singularity) implements the same interface for executing commands and transferring files. The browser tool uses Playwright to control a Chromium instance via CDP.

## Architecture

### Terminal
```
Terminal Tool (tools/terminal_tool.py)
    │
    ├── Environment ABC (tools/environments/)
    │   ├── LocalEnvironment
    │   ├── DockerEnvironment
    │   ├── SSHEnvironment
    │   ├── ModalEnvironment
    │   ├── DaytonaEnvironment
    │   └── SingularityEnvironment
    │
    ├── Security layer (tools/path_security.py, threat patterns)
    └── Background process watcher (notify_on_complete)
```

### Browser
```
Browser Tool (tools/browser_tool.py)
    │
    ├── Playwright controller
    ├── CDP agent (tools/browser_cdp_tool.py)
    ├── Dialog handler (tools/browser_dialog_tool.py)
    └── Supervisor (tools/browser_supervisor.py)
```

## Data Models

No custom data models. Terminal returns stdout/stderr strings. Browser returns page snapshots (screenshot + DOM state).

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Environment abstraction | ABC with register_backend pattern | New backends can be added without modifying the terminal tool |
| Browser engine | Playwright | Cross-browser, reliable, well-maintained, supports CDP |
| Browser connection | Live Chromium via CDP | Full browser environment with DevTools access |
| Background processes | Subprocess with watcher thread | Simple, reliable, platform-independent |
| Security | Multi-layer gating | Command allow/block lists, path validation, threat pattern detection, YOLO mode bypass |

## Sequences

### Command execution
```
Agent → terminal_tool(command) → environment.execute(cmd, timeout)
    → security check
    → spawn process
    → stream output
    → return output
```

### Browser navigation
```
Agent → browser_navigate(url)
    → Playwright navigation
    → snapshot (screenshot + DOM state)
    → return result with snapshot
```

## Risks and Unknowns

1. Remote backends (Modal, Daytona) introduce network dependency and latency
2. Browser automation is fragile — page layout changes, dynamic content, and anti-bot measures can break selectors
3. Background process watcher only works in gateway mode (needs asyncio event loop)

## Out of Scope

- Remote desktop/VNC access
- Mobile browser automation