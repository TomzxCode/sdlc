---
title: "Installation and Auto-Update"
status: done
---

# Specification: Installation and Auto-Update

## Overview

Installers live in `scripts/` (`install.sh`, `install.ps1`, `install_release.sh`, `uninstall.*`), release automation in `.github/workflows/release.yml` and `scripts/quick-release.sh`, and the update engine in `crates/jcode-update-core` (download from GitHub Releases, git-pull handling, divergence detection). Hot-reload on update execs the server into a new binary, reusing the same PID and socket. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
User machine
├── launcher: ~/.local/bin/jcode (symlink into builds/current or builds/stable)
├── builds/versions/<version>/jcode  (immutable binaries)
├── builds/stable/jcode              (stable channel)
├── builds/current/jcode             (self-dev channel)
└── scripts/install.sh / install.ps1 / install_release.sh / uninstall.*

Release pipeline
├── .github/workflows/release.yml (Linux/macOS/Windows builds, signing)
├── scripts/quick-release.sh      (local ~2.5-min release)
├── scripts/generate_release_notes.sh
└── scripts/post_discord_release.py
```

## Data Models

### Version layout

| Path | Role |
|---|---|
| `~/.jcode/builds/versions/<version>/jcode` | Immutable versioned binary. |
| `~/.jcode/builds/stable/jcode` | Stable channel pointer. |
| `~/.jcode/builds/current/jcode` | Self-dev/source-build channel pointer. |
| `~/.jcode/builds/shared-server/jcode` | Symlink into a version, used by the shared daemon. |

## API Contracts

### Update check (`jcode-update-core`)

- Queries GitHub Releases for the configured channel (`stable`/`main`).
- Downloads, extracts, and stages the new binary into a versioned directory.
- Handles `git pull`-based source updates with divergence detection.

## Sequences

### Auto-update hot reload

```
jcode update → check releases → download + extract → stage into builds/versions/<v>
→ server reload → exec new binary (same PID, same socket) → clients reconnect
→ launcher repointed to new version
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Immutable versioned binaries | `builds/versions/<version>/` | Atomic installs and clean rollback. |
| Exec-based hot reload | reload into new binary | Preserves sessions and socket (NFR-2). |
| Separate update crate | `jcode-update-core` | Isolates download/pull/divergence logic. |
| Install-script funnel | `scripts/install.sh` + telemetry install events | Measures conversion and reach. |
| Quick vs CI release | `quick-release.sh` vs `release.yml` | Fast local iteration vs reproducible artifacts. |

## Risks and Unknowns

1. Binary signing coverage outside Windows is not fully documented.
2. Divergence handling for git-pull updates depends on local clone state.

## Out of Scope

- A system package manager integration (Homebrew exists for macOS; others inferred).
- Containerized distribution of the agent runtime.
