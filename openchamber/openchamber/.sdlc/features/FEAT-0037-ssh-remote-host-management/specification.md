---
title: "SSH Remote Host Management"
status: draft
---

# Specification: SSH Remote Host Management

## Overview

The SSH manager is a dedicated Electron module (`packages/electron/ssh-manager.mjs`, 1249 lines) that manages SSH tunnels and remote connections. The UI uses `useDesktopSshStore.ts`, `DesktopHostSwitcher.tsx`, and `RemoteInstancesPage.tsx`.

## Architecture

```
RemoteInstancesPage (packages/ui/src/components/sections/remote-instances/)
    +---> Instance CRUD (host, port, key, password)
    +---> Connection lifecycle (connect, disconnect, retry)
    |
DesktopHostSwitcher (packages/ui/src/components/desktop/)
    +---> Local/remote host switching
    |
useDesktopSshStore.ts (connection state)
    |
Electron SSH Manager (packages/electron/ssh-manager.mjs)
    +---> SSH tunnel management
    +---> Port forwarding (local, remote, dynamic)
    +---> Auto-install on remote hosts
    +---> Connection health monitoring
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Location | Electron main process (not renderer) | SSH requires native system access; cannot run in webview |
| Install | Automated via SSH commands | Reduces setup friction for new remote instances |

## Out of Scope

- SSH key generation
- SSH agent forwarding
- Multi-hop SSH tunnels
