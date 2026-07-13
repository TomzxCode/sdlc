---
title: "Font Customization"
status: done
---

# Specification: Font Customization

## Overview

Font customization is managed via `packages/ui/src/stores/useCustomizationStore.ts` with the font settings persisted. Typography utilities in `packages/ui/src/lib/typography.ts` apply the chosen font family and size as CSS custom properties on the root element.

## Architecture

```
Settings > Appearance (font controls)
    |
useCustomizationStore.ts (fontFamily, fontSize, persisted)
    |
typography.ts (applies CSS custom properties)
    +---> Sets --font-family, --font-size on :root
    |
All components consume CSS variables
    (chat messages, code blocks, terminal, settings)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Mechanism | CSS custom properties | Single source of truth; all components inherit automatically |
| Persistence | Zustand persist middleware | Consistent with other customization settings |

## Out of Scope

- Per-view font settings
- Custom font file upload
- Font ligature configuration
