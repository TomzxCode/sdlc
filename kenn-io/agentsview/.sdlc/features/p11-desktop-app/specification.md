---
title: "Desktop App"
status: done
---

# Specification: Desktop App

## Overview

The desktop app uses Tauri v2 to wrap the agentsview Go web server. The Go binary is built with the desktop build tag and embedded as a Tauri sidecar. The app provides a system tray icon, auto-start via platform-specific mechanisms, and auto-update via GitHub Releases.

## Architecture

```
Tauri Shell (Rust)
  → Sidecar: agentsview server (Go)
  → System Tray Icon
  → Auto-start (LaunchAgent / Registry)
  → Auto-update (GitHub Releases API)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Desktop framework | Tauri v2 | Lightweight, cross-platform, Rust-based |
| Server integration | Sidecar process | Keep Go server as single binary |
| Auto-update | GitHub Releases | Reuses existing release infrastructure |
| Build | CI workflows | Separate workflows for macOS and Windows |

## Build Configuration

- CI workflows: `.github/workflows/desktop-*.yml`
- Desktop source: `desktop/`
- Build artifacts: DMG (macOS), NSIS installer (Windows)
