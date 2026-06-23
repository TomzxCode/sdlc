---
title: "Internationalization (i18n)"
status: draft
---

# Specification: Internationalization (i18n)

## Overview

i18n is implemented in `packages/ui/src/lib/i18n/` with `store.ts` for locale state, `useI18n.ts` for the hook, `context.tsx` for the provider, and `messages/` for translation dictionaries (14 files, lazy-loaded).

## Architecture

```
I18n Provider (packages/ui/src/lib/i18n/context.tsx)
    +---> Wraps app, provides translation function
    |
store.ts (locale preference, current locale)
useI18n.ts (hook for components)
    |
messages/ (lazy-loaded dictionaries)
    +---> en.ts, zh-CN.ts, es.ts, pt-BR.ts, uk.ts, ko.ts, pl.ts
    +---> Per-section translations (settings pages, etc.)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Loading | Lazy-loaded per locale | Reduces initial bundle size; only loads needed locale |
| Detection | navigator.language | Standard browser API; covers most detection scenarios |
| Fallback | English for missing keys | Graceful degradation; no broken UI |

## Out of Scope

- Right-to-left (RTL) layout support
- Translation management UI
- Community translation platform
