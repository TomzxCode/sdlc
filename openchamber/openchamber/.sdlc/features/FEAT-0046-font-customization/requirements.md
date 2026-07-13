---
title: "Font Customization"
status: done
---

# Requirements: Font Customization

## Overview

Users can customize the font family and size used throughout the application via the settings UI, with the preference persisted and applied globally across all views (chat, code, terminal, settings).

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Adjust font for readability and comfort |
| Developers | Match editor font preference |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support changing the application font family. |
| FR-02 | Must | The system shall support changing the application font size. |
| FR-03 | Must | The system shall persist font preferences across sessions. |
| FR-04 | Must | The system shall apply font changes globally without restart. |
| FR-05 | Should | The system shall preview font changes in real time. |
| FR-06 | Should | The system shall provide a reset-to-default option. |
| FR-07 | Must | The system shall support separate configuration of monospace and proportional fonts, with a dedicated terminal font size. |
| FR-08 | Must | The system shall clamp main font size to 50%-200% and terminal font size to 9-52px. |

## Constraints

## Acceptance Criteria

- [ ] FR-01: Given the font settings, the user selects a different font family
- [ ] FR-02: Given the font settings, the user adjusts the font size
- [ ] FR-03: Given a font preference, it persists after app restart
- [ ] FR-04: Given a font change, all views update immediately
- [ ] FR-05: Given the font settings panel is open, adjusting the font size slider shows the text changing in real time
- [ ] FR-06: Given a modified font setting, clicking "Reset to defaults" restores original font family and size
- [ ] FR-07: Given the font settings, monospace and proportional fonts are configured separately with a dedicated terminal font size
- [ ] FR-08: Given font size input outside 50%-200% (main) or 9-52px (terminal), the value is clamped to the valid range
