---
title: "Internationalization (i18n)"
status: done
---

# Requirements: Internationalization (i18n)

## Overview

Full localization system supporting 7 locales (English, Simplified Chinese, Spanish, Portuguese-BR, Ukrainian, Korean, Polish) with lazy-loaded dictionaries, browser language detection, and persistent locale preference. Settings pages have dedicated locale-specific translation files.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Non-English-speaking users | Use the app in their native language |
| Translators | Contribute and maintain translations |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support 7+ locales with lazy-loaded translation dictionaries. |
| FR-02 | Must | The system shall auto-detect browser language on first use. |
| FR-03 | Must | The system shall persist the user's locale preference. |
| FR-04 | Must | The system shall support runtime locale switching without restart. |
| FR-05 | Should | The system shall retry failed locale loads. |
| FR-06 | Should | The system shall default to English for missing translations. |
| FR-07 | Should | The system shall accept new translations by editing TypeScript locale files without a formal contribution process or translation management UI. |
| FR-08 | Must | The system shall fall back to English for missing translation keys. |

## Constraints

## Acceptance Criteria

- [ ] FR-01: Given 7 locales, the user can switch between them in settings
- [ ] FR-02: Given a browser set to Korean, the app defaults to Korean on first use
- [ ] FR-03: Given a locale preference, it persists after app restart
- [ ] FR-04: Given a locale switch, the UI updates without page reload
- [ ] FR-05: Given a failed locale load due to network error, the system retries loading automatically
- [ ] FR-06: Given a locale file that fails to load entirely, the system defaults to English
- [ ] FR-07: Given a new TypeScript locale file registered in store.ts, the locale appears without a formal contribution process
- [ ] FR-08: Given a locale with missing keys, the system displays English text for those keys
