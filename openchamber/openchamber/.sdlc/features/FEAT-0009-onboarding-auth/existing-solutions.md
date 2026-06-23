---
issue: ""
title: "Onboarding & Auth"
status: draft
---

# Existing Solutions: Onboarding & Auth

## Overview

OpenChamber already has a full onboarding flow and authentication system. The onboarding consists of a chooser screen (local vs remote), local setup screen (OpenCode CLI detection and installation guidance), remote connection form (host URL and credential entry), desktop connection recovery (handles local unavailable, remote unreachable, incompatible server), and recovery routing logic. Authentication uses `@simplewebauthn/server` v13.3.0 and `@simplewebauthn/browser` v13.3.0 for passkey-based WebAuthn authentication plus UI password protection via `--ui-password` CLI flag. The existing system covers FR-01 through FR-07 and FR-09. One-scan onboarding via tunnel QR (FR-08) and Windows/Linux desktop recovery are not yet implemented.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/onboarding/`, `packages/web/server/lib/opencode/core-routes.js` (passkey routes), `packages/web/server/lib/opencode/auth.js`, `packages/web/package.json` (@simplewebauthn deps) |
| Open-source | Yes | `@simplewebauthn/server` v13.3.0, `@simplewebauthn/browser` v13.3.0, WebAuthn API, react-stepflow, flowsterix, wizzard-packages |
| Commercial / SaaS | No | Auth0, Clerk, WorkOS exist but self-hosted nature makes them unsuitable |
| Standards / protocols | Yes | FIDO2 WebAuthn (W3C), passkeys (Apple/Google/Microsoft), QR code login patterns |
| Reference material | Yes | SimpleWebAuthn docs, WebAuthn spec, passkeys.dev |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber built-in onboarding + auth | Internal | MIT | Mature | FR-01 to FR-07, FR-09, NFR-01, NFR-02 | FR-08 (tunnel QR one-scan), Windows desktop recovery partial |
| `@simplewebauthn/server` v13.3.0 | Library | MIT | Mature | WebAuthn registration, authentication, passkey support, credential management | Backend only, requires browser counterpart |
| `@simplewebauthn/browser` v13.3.0 | Library | MIT | Mature | Browser-side WebAuthn ceremonies, conditional UI, autofill | Frontend only, requires server counterpart |
| React stepflow / wizzard-packages | Library | MIT | Active | Multi-step wizard state machine | UI pattern only, not an onboarding system |
| flowsterix | Library | MIT | Active | Guided tours with shadcn components | Tour overlay, not setup wizard |

## Evaluation

### OpenChamber built-in onboarding + auth

- **Strengths:** Complete onboarding flow with chooser (local vs remote), CLI detection and installation guidance for macOS, remote connection form with probe/error handling, desktop connection recovery with four scenarios (local unavailable, no default connection, remote unreachable, incompatible server), recovery routing with config-based scenario definitions. Authentication uses SimpleWebAuthn for full WebAuthn passkey support plus UI password protection. Passkey routes cover status, authentication options/verify, registration options/verify, listing, and revocation with tunnel scope restrictions.
- **Weaknesses:** One-scan onboarding via tunnel QR code (FR-08) is not implemented. Windows desktop recovery is not fully covered (the recovery config has limited Windows-specific scenarios). The onboarding UI uses custom components rather than a generalized wizard framework which makes adding steps more work.
- **Integration effort:** Low (already integrated).
- **Cost:** None.
- **Risks:** None.

### SimpleWebAuthn

- **Strengths:** 1.6M weekly downloads, MIT license, 100% TypeScript, supports Node LTS 20+ and Deno, covers all WebAuthn attestation formats (Android Key, Apple, FIDO U2F, TPM, Packed, None), built-in passkey support with conditional UI and autofill.
- **Weaknesses:** Requires careful challenge management and credential persistence. Stale challenges must be cleaned up.
- **Integration effort:** Low (already integrated).
- **Cost:** None (MIT).
- **Risks:** None. Market-leading WebAuthn library.

### React wizard libraries (stepflow, wizzard-packages, flowsterix)

- **Strengths:** Provide state machine-based wizard patterns, validation, conditional steps, and persistence.
- **Weaknesses:** Over-engineered for OpenChamber's needs. The existing onboarding has only 3-4 screens with simple linear flow.
- **Integration effort:** Medium (would require replacing existing custom wizard).
- **Cost:** None (MIT).
- **Risks:** Additional dependency with marginal benefit.

## Recommendation

**Direction: Adopt and extend**

The existing onboarding and auth system is mature and well-integrated. Extend with:
- One-scan onboarding via tunnel QR code (FR-08) using the existing Cloudflare tunnel infrastructure and QR code generation.
- Complete desktop recovery coverage for Windows using WSL detection and configuration.
- Continue using `@simplewebauthn` for all passkey operations; it is the de facto standard WebAuthn library for Node.js.

## Sources of Information

- `core-routes.js` at `packages/web/server/lib/opencode/core-routes.js` (lines 312-390) - passkey route definitions
- `OnboardingScreen.tsx` at `packages/ui/src/components/onboarding/OnboardingScreen.tsx` - main onboarding orchestrator
- `desktopRecoveryConfig.ts` at `packages/ui/src/components/onboarding/desktopRecoveryConfig.ts` - recovery scenario configurations
- `ChooserScreen.tsx` at `packages/ui/src/components/onboarding/ChooserScreen.tsx` - local/remote chooser
- `LocalSetupScreen.tsx` at `packages/ui/src/components/onboarding/LocalSetupScreen.tsx` - CLI detection and install guidance
- `RemoteConnectionForm.tsx` at `packages/ui/src/components/onboarding/RemoteConnectionForm.tsx` - remote host connection
- SimpleWebAuthn docs at `simplewebauthn.dev`
- passkeys.dev - WebAuthn passkey implementation guide

## Open Questions

1. Should the one-scan tunnel QR flow (FR-08) generate a QR code on the server or client side?
2. Does the onboarding need a skip option for power users who already know the setup?
3. Should passkey registration be offered as part of the onboarding flow or only through settings post-setup?
