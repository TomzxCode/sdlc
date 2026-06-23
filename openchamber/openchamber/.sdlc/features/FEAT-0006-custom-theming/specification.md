---
title: "Custom Theming System"
status: draft
---

# Specification: Custom Theming System

## Overview

The theme system is implemented in `packages/ui/src/lib/theme/` using CSS custom properties. Built-in themes are defined as TypeScript objects that generate CSS. Custom themes are loaded from JSON files, validated, and applied by overriding CSS custom properties. The Vite theme plugin (`vite-theme-plugin.ts`) handles theme compilation.

## Architecture

```
Built-in themes (packages/ui/src/lib/theme/)
    |
    +---> TypeScript theme definitions
    |
Custom themes (~/.config/openchamber/themes/*.json)
    |
    v
Theme loader (server reads JSON, client applies CSS vars)
    |
    v
CSS Custom Properties on :root
    |
    v
All UI components consume via theme tokens
```

## Data Models

### ThemeDefinition

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | Theme name |
| variant | enum | not null | light, dark |
| colors | object | not null | Color token mappings |
| typography | object | nullable | Font overrides |
| spacing | object | nullable | Spacing overrides |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Implementation | CSS custom properties | Native browser support; instant switching; no JS runtime cost |
| Hot reload | File watcher on themes directory | Detects changes and pushes new CSS without full reload |
| Built-in themes | TypeScript objects compiled at build time | Type-safe; caught at build time |
| Custom themes | JSON files validated at load time | User-friendly format; easy to create and share |

## Risks and Unknowns

1. Complex custom themes may override tokens in ways that break component layout
2. No theme validation beyond basic schema checking

## Out of Scope

- Theme marketplace or sharing platform
- Visual theme editor UI
