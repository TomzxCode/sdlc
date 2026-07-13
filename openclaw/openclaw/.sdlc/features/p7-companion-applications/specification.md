---
title: "Companion Applications"
status: done
---

# Specification: Companion Applications

## Overview

Companion apps are platform-native applications that connect to the gateway over a secure WebSocket connection using the Gateway Protocol. They communicate with the gateway for chat, voice I/O, device pairing, and status monitoring.

## Architecture

```
Companion App (macOS/iOS/Android/Windows)
     │
     ▼  Gateway Protocol (WebSocket + RPC)
     │
Gateway Server → Agent Runtime
```

### Platform Stacks

| Platform | Language/Framework | Build System |
|---|---|---|
| macOS | Swift + SwiftUI | Xcode, xcworkspace |
| iOS | Swift + SwiftUI | Xcode, xcworkspace |
| Android | Kotlin | Gradle |
| Windows | C# (Windows Hub) | .NET |

## Data Models

### DevicePairing

| Field | Type | Constraints | Description |
|---|---|---|---|
| deviceId | string | PK | Unique device identifier |
| userId | string | not null | Associated user |
| publicKey | string | not null | Device public key for auth |
| pairedAt | timestamp | not null | Pairing timestamp |
| lastSeen | timestamp | nullable | Last activity time |

## Sequences

### Device Pairing Flow

```
App → Gateway: request pairing code
Gateway → User: display pairing code (CLI/Control UI)
User → App: enter pairing code
App → Gateway: submit signed pairing request
Gateway → App: confirm pairing, issue device token
App → Gateway: authenticated WebSocket connection
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Communication protocol | Gateway Protocol over WebSocket | Consistent with other gateway clients |
| Voice on iOS | AVSpeechSynthesizer (TTS) | Native, no external dependencies |
| Voice on Android | TextToSpeech API | Native Android API |
| Device pairing | Code-based handshake | Simple UX, works on all platforms |

## Risks and Unknowns

1. Apple platform restrictions (notarization, App Store review) can delay releases
2. Voice I/O quality varies significantly across platforms and devices
3. Windows Hub is in early stages; capabilities may change

## Out of Scope

- Linux desktop app (Linux users use CLI and channels)
- Web app (use Control UI instead)
- Cross-platform shared UI toolkit (each app is natively built)
