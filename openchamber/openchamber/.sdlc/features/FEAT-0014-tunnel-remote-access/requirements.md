---
title: "Tunnel & Remote Access"
status: done
---

# Requirements: Tunnel & Remote Access

## Overview

OpenChamber supports Cloudflare tunnels for remote access, enabling users to connect to their local OpenCode instance from any device. The system supports quick, managed-remote, and managed-local tunnel modes, with QR code onboarding and one-time connect tokens for secure access.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Remote workers | Access their dev machine's AI assistant from a tablet or phone |
| Teams | Share development sessions across devices via managed tunnels |
| Self-hosters | Persistent remote access via Docker or systemd |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support Cloudflare tunnels in quick, managed-remote, and managed-local modes. |
| FR-02 | Must | The system shall generate QR codes for quick tunnel onboarding. |
| FR-03 | Must | The system shall support one-time connect tokens that are revoked after use. |
| FR-04 | Must | The system shall support tunnel lifecycle management (start, stop, status) via CLI and API. |
| FR-05 | Must | The system shall support multiple tunnel profiles with distinct configurations. |
| FR-06 | Should | The system shall enforce UI password protection for remote access. |
| FR-07 | Should | The system shall support at most one active tunnel per running instance. |
| FR-08 | May | The system shall support additional tunnel providers beyond Cloudflare. |
| FR-09 | Must | The system shall support tunnel providers via a provider registry, with Cloudflare (quick, managed-remote, managed-local) and ngrok (beta, quick tunnel) as implemented providers. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Connect links shall be one-time tokens; generating a new link revokes the previous unused link. |
| NFR-02 | Must | Security | Replacing or stopping a tunnel shall revoke existing connect links and invalidate remote sessions. |
| NFR-03 | Should | Reliability | Tunnel processes shall be monitored and restarted on failure. |

## Constraints

- `cloudflared` binary must be available on the host or in the Docker image
- Tunnel tokens and connect links are stored in server memory (not persisted across restarts)

## Acceptance Criteria

- [ ] FR-01: Given a running instance, the user can start a tunnel in quick mode and access the UI remotely
- [ ] FR-02: Given a quick tunnel, a QR code is generated that contains the tunnel URL
- [ ] FR-03: Given a connect link, after one use, the link is invalidated
- [ ] FR-04: Given an active tunnel, the user can stop it via CLI or API
- [ ] FR-05: Given a managed-remote profile, the user can start a tunnel with a specific hostname and token
- [ ] FR-06: Given a remote access URL, the system prompts for a UI password before granting access
- [ ] FR-07: Given an active tunnel, starting a second tunnel is rejected; at most one tunnel is active per instance
- [ ] FR-08: Given a provider registry, an additional tunnel provider can be registered and used for tunnel creation
- [ ] FR-09: Given a configured provider (Cloudflare or ngrok), the system creates a tunnel using the provider registry with the appropriate mode
- [ ] NFR-01: Given a one-time connect link, after first use the link is revoked; generating a new link revokes the previous unused one
- [ ] NFR-02: Given an active tunnel, replacing or stopping it revokes existing connect links and invalidates remote sessions
- [ ] NFR-03: Given a running tunnel process, if it crashes the system detects the failure and restarts it automatically
