---
title: "Tunnel & Remote Access"
status: draft
---

# Specification: Tunnel & Remote Access

## Overview

The tunnel system is implemented as a provider registry pattern in `packages/web/server/lib/tunnels/`. The Cloudflare provider spawns a `cloudflared` subprocess and manages its lifecycle. Tunnel state is tracked in server memory. The CLI (`packages/web/bin/cli.js`) provides tunnel subcommands.

## Architecture

```
CLI / API request
    |
    v
TunnelService (packages/web/server/lib/tunnels/)
    |
    v
TunnelProviderRegistry -> CloudflareTunnelProvider
    |
    v
cloudflared subprocess
    |
    v
Cloudflare edge network -> User's browser
```

## Data Models

### TunnelConfig

| Field | Type | Constraints | Description |
|---|---|---|---|
| provider | string | not null | Tunnel provider (e.g., "cloudflare") |
| mode | enum | not null | quick, managed-remote, managed-local |
| hostname | string | nullable | Required for managed-remote |
| token | string | nullable | Required for managed-remote |
| configPath | string | nullable | Optional for managed-local |

### TunnelProfile

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | Profile name |
| provider | string | not null | Provider identifier |
| mode | string | not null | Tunnel mode |
| hostname | string | nullable | Managed hostname |
| token | string | nullable | Auth token |

### TunnelState

| Field | Type | Constraints | Description |
|---|---|---|---|
| active | boolean | not null | Whether tunnel is running |
| url | string | nullable | Public tunnel URL |
| mode | string | not null | Current mode |
| connectToken | string | nullable | One-time connect token |

## API Contracts

### POST /api/tunnel/start

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| provider | string | yes | Tunnel provider |
| mode | string | yes | Tunnel mode |
| hostname | string | no | For managed-remote |
| token | string | no | For managed-remote |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| url | string | Public tunnel URL |
| connectToken | string | One-time connect token |

### POST /api/tunnel/stop

Stops the active tunnel. Returns 200 on success.

### GET /api/tunnel/status

Returns current tunnel state (active, url, mode).

## Sequences

### Quick tunnel with QR onboarding

```
User runs `openchamber tunnel start --provider cloudflare --mode quick --qr`
    |
    v
Server spawns cloudflared quick tunnel
    |
    v
Server generates one-time connect token
    |
    v
CLI renders QR code with tunnel URL + token in terminal
    |
    v
User scans QR on phone -> Phone browser opens OpenChamber UI
    |
    v
Connect token validated and consumed
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider pattern | Registry with pluggable providers | Extensible to future tunnel providers without modifying core |
| Subprocess | cloudflared as child process | Cloudflare's recommended approach; no native bindings needed |
| Connect tokens | In-memory, one-time, hash-based | Simple security model; no database dependency |
| Profile storage | File-based (YAML/JSON) | Simple to manage via CLI; no database required |

## Risks and Unknowns

1. cloudflared binary availability across platforms
2. Cloudflare free tier rate limits for quick tunnels

## Out of Scope

- WireGuard, Tailscale, or other VPN-based access
- Persistent (non-one-time) connect tokens
- Multi-provider active tunnels simultaneously
