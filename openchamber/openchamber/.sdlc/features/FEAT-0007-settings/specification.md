---
title: "Settings"
status: done
---

# Specification: Settings

## Overview

Settings are organized as a shell (`SettingsView.tsx`) with sidebar navigation and per-page content components. Each section lives in `packages/ui/src/components/sections/`. Settings are read from and written to the OpenCode server via API calls. A windowed variant (`SettingsWindow.tsx`) is available for desktop.

## Architecture

```
SettingsView (packages/ui/src/components/views/SettingsView.tsx)
    |
    +---> Sidebar navigation (collapsible groups)
    +---> Page content area
    |       |
    |       +---> sections/appearance/
    |       +---> sections/chat/
    |       +---> sections/notifications/
    |       +---> sections/sessions/
    |       +---> sections/shortcuts/
    |       +---> sections/git-identities/
    |       +---> sections/magic-prompts/
    |       +---> sections/projects/
    |       +---> sections/remote-instances/
    |       +---> sections/agents/
    |       +---> sections/behavior/
    |       +---> sections/commands/
    |       +---> sections/mcp/
    |       +---> sections/providers/
    |       +---> sections/usage/
    |       +---> sections/skills/
    |       +---> sections/voice/ (inline)
    |       +---> sections/tunnel/ (inline)
    |
    +---> Shared primitives (sections/shared/)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Layout | Sidebar + content page pattern | Familiar settings UX; scales to many pages |
| Shared primitives | Reusable form components in sections/shared/ | Consistent styling and behavior across all settings pages |
| Persistence | Server-side via OpenCode config API | Single source of truth; survives client refresh |

## Risks and Unknowns

1. Adding new settings pages increases the settings bundle size
2. Some settings require server restart to take effect

## Out of Scope

- Cloud sync of settings
- Settings profiles/presets
