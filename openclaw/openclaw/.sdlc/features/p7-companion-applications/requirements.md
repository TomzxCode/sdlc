---
title: "Companion Applications"
status: draft
---

# Requirements: Companion Applications

## Overview

Companion applications extend OpenClaw to native platforms: macOS desktop app, iOS app, Android app, and Windows companion. They provide platform-specific features like voice I/O, system tray integration, notifications, and native chat experiences.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Native OS integration, voice input/output, smooth experience |
| Operators | Consistent behavior across platforms |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The macOS app shall provide system tray integration with quick access to gateway controls |
| FR-2 | Must | The iOS app shall provide push notifications for new assistant messages |
| FR-3 | Must | The Android app shall support voice input and text-to-speech output |
| FR-4 | Must | Companion apps shall connect to the gateway over the local network or Tailscale |
| FR-5 | Must | The macOS app shall support text-to-speech using system voices |
| FR-6 | Should | Companion apps shall display session history |
| FR-7 | Should | Companion apps shall support device pairing for secure gateway connection |
| FR-8 | May | The Windows companion app shall support setup, tray status, chat, node mode, and local MCP mode |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Companion apps shall authenticate with the gateway using secure pairing |
| NFR-2 | Should | Performance | Voice I/O shall have latency under 2 seconds for real-time interaction |

## Constraints

- iOS app requires Apple Developer Program membership for distribution
- macOS app requires notarization for distribution outside the Mac App Store
- Android app targets modern Android versions (API 26+)
- Companion apps are optional; core functionality works via CLI and channels

## Acceptance Criteria

- [ ] **FR-1**: Given the macOS app running, when the user clicks the tray icon, then gateway controls are accessible
- [ ] **FR-2**: Given the iOS app with push enabled, when the gateway sends a message, then a push notification appears
- [ ] **FR-7**: Given a companion app, when it connects to the gateway for the first time, then the device pairing flow completes successfully
- [ ] **NFR-1**: Given a companion app connection request without valid credentials, when it reaches the gateway, then it is rejected

## Conflicts

None identified yet.

## Open Questions

1. Should the companion apps offer full chat functionality or be thin clients?
2. What is the minimum supported OS version for each platform?
