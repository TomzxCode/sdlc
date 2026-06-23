---
title: "Onboarding & Auth"
status: draft
---

# Requirements: Onboarding & Auth

## Overview

OpenChamber provides a first-run onboarding flow that guides users through choosing local or remote setup, configuring connections, and recovering from connection issues. Authentication supports passkey-based login for remote access and UI password protection.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| New users | Guided setup experience without reading docs |
| Remote users | Secure authentication for remote access |
| Self-hosters | Password protection for shared instances |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a first-run onboarding screen with local/remote setup options. |
| FR-02 | Must | The system shall support local setup: detect OpenCode installation and guide configuration. |
| FR-03 | Must | The system shall support remote connection setup: enter host URL and credentials. |
| FR-04 | Must | The system shall support passkey-based authentication for remote access. |
| FR-05 | Must | The system shall support UI password protection for the web server. |
| FR-06 | Should | The system shall provide a recovery screen for handling connection failures gracefully. |
| FR-07 | Should | The system shall provide a desktop connection recovery flow for Electron users. |
| FR-08 | May | The system shall support one-scan onboarding via tunnel QR code. |
| FR-09 | Must | The system shall store passkey credentials locally per device; users shall register a new passkey on each device. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Passkeys shall use WebAuthn standard; no passwords stored on server. |
| NFR-02 | Must | Security | UI password shall be validated server-side before serving the SPA. |

## Constraints

- Passkey auth uses `@simplewebauthn/server` and `@simplewebauthn/browser`
- UI password is set via CLI flag `--ui-password` or environment variable
- Onboarding state is persisted so returning users skip the flow

## Acceptance Criteria

- [ ] FR-01: Given a fresh install, the onboarding screen shows local and remote options
- [ ] FR-02: Given local setup chosen, the system checks for OpenCode and guides installation if missing
- [ ] FR-03: Given remote setup chosen, the user enters a host URL and authenticates
- [ ] FR-04: Given passkey auth, the user can register and log in with a biometric or hardware key
- [ ] FR-05: Given a UI password is set, unauthenticated requests are rejected
- [ ] FR-06: Given a connection failure during onboarding, the recovery screen offers retry options
- [ ] FR-09: Given a user on a new device, when authenticating, they must register a new passkey; credentials from other devices are not available
- [ ] FR-07: Given an Electron desktop with a failed remote connection, the recovery flow guides the user through re-authentication
- [ ] FR-08: Given a tunnel connection, the onboarding screen displays a QR code that a mobile device can scan to connect
- [ ] NFR-01: Given passkey registration, the system uses WebAuthn with public key cryptography; no password is transmitted or stored on the server
- [ ] NFR-02: Given a UI password is configured, the server validates the password before serving the SPA; unauthenticated requests receive HTTP 401
