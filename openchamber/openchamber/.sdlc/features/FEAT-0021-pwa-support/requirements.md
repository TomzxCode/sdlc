---
title: "PWA Support"
status: draft
---

# Requirements: PWA Support

## Overview

Installable Progressive Web App with service worker for push notifications and offline handling, install prompt with dismissible toast, display mode detection, dynamic manifest sync for recent session shortcuts, and window controls overlay layout adaptation.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Mobile/tablet users | Install as app-like experience on home screen |
| Desktop PWA users | Run in its own window outside the browser |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall be installable as a PWA with service worker. |
| FR-02 | Must | The system shall handle push notifications via the service worker when the app is not visible. |
| FR-03 | Must | The system shall show an install prompt toast that can be dismissed without reappearing. |
| FR-04 | Must | The system shall detect display mode (standalone, fullscreen, window-controls-overlay). |
| FR-05 | Should | The system shall sync the PWA manifest with recent session shortcuts. |
| FR-06 | Should | The system shall adapt layout for window controls overlay mode. |
| FR-07 | Should | The system shall support configurable install orientation. |
| FR-08 | Must | The system shall support cached-shell offline mode only; full offline mode is out of scope. |

## Acceptance Criteria

- [ ] FR-01: Given a supported browser, the user can install OpenChamber as a PWA
- [ ] FR-02: Given the PWA is closed, push notifications still appear
- [ ] FR-03: Given the install prompt, dismissing it prevents repeated prompts
- [ ] FR-04: Given the PWA is in standalone mode, the UI adapts (no browser chrome)
- [ ] FR-05: Given a session is active, the PWA manifest includes a shortcut for that session
- [ ] FR-06: Given the PWA is in window-controls-overlay mode, the layout adapts to avoid the overlay region
- [ ] FR-07: Given the PWA install prompt, the user can configure the install orientation before installation
- [ ] FR-08: Given the PWA is offline, only the cached shell is available; full functionality requires a server connection

## Constraints
