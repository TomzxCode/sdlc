---
issue: ""
title: "SSH Remote Host Management"
status: draft
---

# Existing Solutions: SSH Remote Host Management

## Overview

The Electron desktop app already has a fully functional SSH manager (`packages/electron/ssh-manager.mjs`, ~1250 lines) that wraps the system `ssh` command (via `child_process.spawn`) and provides connect/disconnect/retry lifecycle, local/remote/dynamic port forwarding, SSH config file import (`Include` directives, globs, `~/.ssh/config` globbing), multi-instance management with independent connections, connection health monitoring with polling, structured logging per instance, and integration with the desktop host switcher UI. No external npm SSH library is used — the manager spawns the system SSH binary directly. The settings UI for remote instances is fully internationalized across 8 languages. The main gap is auto-installation of OpenChamber on remote hosts (FR-05) and agent forwarding support (FR-08).

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/electron/ssh-manager.mjs`, `packages/electron/main.mjs`, `packages/ui/src/components/desktop/DesktopHostSwitcher.tsx`, `packages/ui/src/lib/settings/metadata.ts`, i18n files (en, zh-CN, zh-TW, uk, pt-BR, ko, pl, es) |
| Open-source | Yes | `ssh2` (npm), `node-ssh` (npm), `ssh2-sftp-client` (npm) |
| Commercial / SaaS | Yes | VS Code Remote-SSH, JetBrains Gateway, Termius |
| Standards / protocols | Yes | SSH protocol (RFC 4251), OpenSSH config format, SSH agent forwarding |
| Reference material | Yes | OpenSSH man pages, SSH config file documentation |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Internal ElectronSshManager (system ssh spawn) | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, FR-09 | FR-05, FR-08 |
| ssh2 (npm) | Library | MIT | Mature | FR-01, FR-02, FR-04, FR-08, FR-09 | FR-05, FR-06, FR-07 |
| node-ssh (npm) | Library | MIT | Mature | FR-01, FR-02, FR-04, FR-09 | FR-05, FR-06, FR-07, FR-08 |
| VS Code Remote-SSH | Product | Proprietary | Mature | FR-01, FR-02, FR-05, FR-06, FR-07, FR-08, FR-09 | Not embeddable, proprietary |
| JetBrains Gateway | Product | Proprietary | Mature | FR-01, FR-02, FR-05, FR-08, FR-09 | Not embeddable, proprietary |

## Evaluation

### Internal ElectronSshManager (system ssh spawn)

- **Strengths:** Already implemented and used in production.
  Uses the system SSH binary which respects user's `~/.ssh/config`, known_hosts, and SSH agent automatically.
  Supports SSH config file import with `Include` directive expansion, glob wildcards, and `~` expansion.
  Manages multiple simultaneous SSH instances independently with full lifecycle (connect, disconnect, retry).
  Supports local (`-L`), remote (`-R`), and dynamic/SOCKS5 (`-D`) port forwarding.
  Has connection health monitoring with adjustable polling intervals and stabilization ticks.
  Structured per-instance log buffer with configurable line limits.
  Exposes status via IPC to the renderer for the desktop host switcher UI.
  Graceful shutdown of all connections on app quit.
  Pick-random-port fallback for port conflicts.
- **Weaknesses:** Does not support SSH agent forwarding (`-A` flag) in the current code (FR-08 gap — needs to be added to the spawn args).
  Does not support auto-installing OpenChamber on remote hosts (FR-05 gap — needs detection + scp/curl deployment logic).
  Uses raw string parsing for SSH config file import which can be brittle.
  No integrated password-based auth UI flow (relies on SSH agent or key-based auth).
- **Integration effort:** Low — the solution already exists.
- **Cost:** Free.
- **Risks:** Low. The system SSH binary approach is simpler and more robust than embedding a JS SSH library for the Electron desktop use case.

### ssh2 (npm)

- **Strengths:** Pure JavaScript SSH2 implementation.
  Full client and server capabilities.
  Supports exec, shell, SFTP, port forwarding, agent forwarding.
  Very widely used (2000+ dependents).
  TypeScript types available via `@types/ssh2`.
- **Weaknesses:** Would require significant rewrite of the existing SSH manager.
  Cannot automatically use user's `~/.ssh/config` or SSH agent without additional code.
  Being a JS implementation, it may have edge cases with newer SSH algorithms.
  Requires managing SSH key parsing and known_hosts verification manually.
  The existing system SSH approach handles config file parsing and agent integration for free.
- **Integration effort:** High — would replace the entire existing working SSH manager.
- **Cost:** Free (MIT).
- **Risks:** Medium — changing from system SSH to a JS implementation could break edge cases that the system SSH handles (key types, config options, agent forwarding).

### node-ssh (npm)

- **Strengths:** Promise-based wrapper around ssh2.
  Simpler API than raw ssh2 for common operations (exec, shell).
  715 dependents, MIT license.
- **Weaknesses:** Same downsides as ssh2.
  Adds an additional abstraction layer.
  Fewer features than raw ssh2 (e.g., port forwarding requires raw ssh2 access).
  Potential maintenance risk with slower update cadence.
- **Integration effort:** High — same as ssh2.
- **Cost:** Free (MIT).
- **Risks:** Medium — same as ssh2 plus dependency on an intermediary wrapper.

## Recommendation

**Direction: Adopt and extend**

The existing `ElectronSshManager` in `packages/electron/ssh-manager.mjs` is the right solution — it uses the system SSH binary which provides free compatibility with all OpenSSH features, user config, and agent integration. Two extensions are needed: (1) add `-A` flag support for agent forwarding (FR-08) by appending it to the spawn arguments, and (2) add remote OpenChamber auto-installation (FR-05) using SSH exec to detect the remote OS/arch, download or scp the matching OpenChamber release, and start it.

No external SSH library is needed — the system `ssh` command approach is the standard for desktop SSH tools (VS Code Remote-SSH, Termius all use the system SSH or bundle OpenSSH).

## Sources of Information

- `packages/electron/ssh-manager.mjs`: Full SSH connection manager with spawn-based SSH, config file import, port forwarding, health monitoring, logging, and multi-instance management.
- `packages/ui/src/lib/i18n/messages/en.ts`: i18n keys for `desktopHostSwitcher.ssh.*` showing the SSH lifecycle phases.
- `packages/ui/src/lib/i18n/messages/en.ts` settings: `settings.remoteInstances.*` i18n showing full settings UI for remote instances.
- `ssh2` npm package: Pure JS SSH2 implementation, MIT, 2000+ dependents.
- `node-ssh` npm package: Promise-based wrapper around ssh2, 715 dependents.
- VS Code Remote-SSH extension: Uses a similar system-SSH-spawn approach for remote development.

## Open Questions

1. For auto-install (FR-05), should we detect the remote OS/arch and download the matching release from GitHub, or scp a bundled binary?
2. Should password-based SSH auth be supported in the UI, or should we rely on SSH agent/key-based auth only?
3. Does the existing `ssc` (ssh config) parser handle all edge cases of OpenSSH config format (Match blocks, hostname expansion, ProxyJump)?
