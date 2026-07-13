---
title: "Internationalization"
status: done
---

# Requirements: Internationalization

## Overview

Hermes includes internationalization support with translation files in locales/ for multiple languages. The system provides localized strings for CLI output, error messages, and documentation. README translations exist in Spanish (README.es.md), Chinese (README.zh-CN.md), and Urdu (README.ur-pk.md).

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Non-English users | Use Hermes with CLI output and documentation in their preferred language |
| International contributors | Add and maintain translations for their language |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall support locale-based string loading from the locales/ directory |
| FR-2 | Should | CLI output shall respect the system locale setting |
| FR-3 | Should | Core documentation (README) shall be available in multiple languages |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Should | Maintainability | Adding a new locale shall require only a new translation file, no code changes |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the system locale is set to a supported language
    - **When** the CLI displays a localized string
    - **Then** the translated string is shown

## Conflicts

None identified yet.

## Open Questions

1. Should skill SKILL.md files also be localized?
