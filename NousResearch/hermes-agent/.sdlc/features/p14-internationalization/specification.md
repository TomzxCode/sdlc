---
title: "Internationalization"
status: done
---

# Specification: Internationalization

## Architecture

```
Internationalization (locales/)
    │
    ├── en/ — English (default)
    ├── es/ — Spanish
    ├── zh-CN/ — Chinese (Simplified)
    └── <locale>/ — Future locales
```

## Data Models

### Locale file format

| Field | Type | Description |
|---|---|---|
| key | string | Translation key (dot-notation) |
| value | string | Translated string |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | Directory-based locale files | Simple, no dependencies, easy to add new locales |
| Default | English | Always fall back to English for untranslated keys |
| CLI locale detection | System locale or config setting | Respects user's environment |

## Risks and Unknowns

1. Maintainability of translations across rapid development — new strings may not be translated promptly
2. Not all CLI output is currently internationalized (incremental adoption)

## Out of Scope

- Runtime language switching (requires agent restart)
- Machine translation of missing strings
