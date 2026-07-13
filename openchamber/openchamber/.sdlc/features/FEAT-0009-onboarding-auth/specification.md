---
title: "Onboarding & Auth"
status: done
---

# Specification: Onboarding & Auth

## Overview

The onboarding flow is a series of screens in `packages/ui/src/components/onboarding/`. Authentication uses WebAuthn for passkeys (`packages/web/server/lib/ui-auth/`, `packages/ui/src/components/auth/`). UI password protection is enforced by Express middleware before serving static assets.

## Architecture

```
OnboardingFlow (packages/ui/src/components/onboarding/)
    +---> OnboardingScreen (entry point)
    +---> ChooserScreen (local vs remote)
    +---> LocalSetupScreen (detect OpenCode, configure)
    +---> RemoteConnectionForm (host, credentials)
    +---> RecoveryScreen (connection failure recovery)
    +---> DesktopConnectionRecovery (Electron-specific)

Auth (packages/ui/src/components/auth/)
    +---> Passkey registration/login via @simplewebauthn/browser

Server Auth (packages/web/server/lib/ui-auth/)
    +---> ui-auth.js (WebAuthn challenge/verification)
    +---> Express middleware (password check before SPA)
```

## Sequences

### First-run local setup

```
App starts -> No saved config detected
    |
    v
OnboardingScreen -> ChooserScreen
    |
    v  User selects "Local"
LocalSetupScreen -> Check for OpenCode binary
    |
    v  Found
Server starts OpenCode -> UI loads chat
```

### Passkey registration

```
User opens settings -> Security -> Register passkey
    |
    v
Server generates WebAuthn challenge -> Browser prompts biometric
    |
    v
Client sends attestation -> Server verifies and stores credential
    |
    v
Future logins use passkey for passwordless auth
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Passkey | WebAuthn via @simplewebauthn | Industry standard; no custom crypto |
| UI password | Express middleware (gate all routes) | Simple; enforced before any client code runs |
| Onboarding | Multi-screen wizard | Guides users through required steps without overwhelming |

## Risks and Unknowns

1. WebAuthn support varies across browsers and devices
2. Passkey credentials tied to device; no cross-device sync without platform support

## Out of Scope

- SSO/SAML integration
- Multi-factor authentication beyond passkeys
- User management (single-user model)
