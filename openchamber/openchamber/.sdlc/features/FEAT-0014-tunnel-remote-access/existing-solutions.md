---
issue: ""
title: "Tunnel & Remote Access"
status: draft
---

# Existing Solutions: Tunnel & Remote Access

## Overview

The codebase already has a mature tunnel and remote access implementation with a provider registry pattern supporting Cloudflare (quick, managed-remote, managed-local modes) and ngrok (beta quick tunnel). Features include QR code generation, one-time connect tokens, tunnel lifecycle management (start, stop, status), multiple tunnel profiles, UI password protection, and bus-based tunnel state dispatch. The recommendation is to adopt the existing provider-registry architecture and extend rather than build a new system or adopt alternative tunnel providers.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/tunnels/`, `packages/web/server/lib/opencode/core-routes.js`, CLI tunnel commands |
| Open-source | Yes | cloudflared, ngrok, node-cloudflared npm, bore, localtunnel, pagekite, frp |
| Commercial / SaaS | Yes | Cloudflare Tunnel, ngrok, Tailscale Funnel, serveo |
| Standards / protocols | Yes | Cloudflare Tunnel API, ngrok Agent API |
| Reference material | Yes | Cloudflare Tunnel docs, ngrok docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing tunnel provider registry + providers | Internal | MIT | Mature | FR-01 through FR-09, NFR-01, NFR-02, NFR-03 | ngrok is beta only |
| node-cloudflared (npm) | Library | MIT | Mature | FR-01 | Node.js wrapper; binary management |
| cloudflared binary | CLI | Apache 2.0 | Mature | FR-01, FR-04 | All tunnel modes |
| ngrok agent | CLI | Proprietary | Mature | FR-08, FR-09 | Beta support only |
| bore / localtunnel | CLI / Library | MIT | Stale | FR-01 | No auth; no managed modes; unreliable |

## Evaluation

### Existing Tunnel Provider Registry + Implemented Providers

- **Strengths:** Provider registry pattern (`packages/web/server/lib/tunnels/registry.js`) is extensible by design — new providers implement `start`, `stop`, `checkAvailability`, `resolvePublicUrl`. Cloudflare provider supports all three modes (quick, managed-remote, managed-local). QR code generation via CLI `--qr` flag. One-time connect tokens with revocation on reuse. Tunnel lifecycle management via CLI and API. Multiple tunnel profiles for managed-remote. UI password protection for tunnel sessions. Bus-based state dispatch for tunnel events. Provider health checks. At-most-one-active-tunnel enforcement. Constants, normalization, and validation in `types.js`. Managed config persistence in `managed-config.js`. Documentation in `DOCUMENTATION.md`.
- **Weaknesses:** ngrok provider is beta (quick mode only). No test suite for tunnel providers. Tunnel process monitoring/restart (NFR-03) is implicit via process manager, not explicit in code.
- **Integration effort:** Low. Already integrated with CLI, server, and auth layers.
- **Cost:** Free (MIT). Cloudflare tunnel has free tier with usage limits. ngrok free tier is limited.
- **Risks:** Low. `cloudflared` binary dependency must be available on host. This is documented as a constraint.

### node-cloudflared (npm)

- **Strengths:** Automatically manages cloudflared binary installation. Typed API for tunnel creation. Cross-platform (macOS, Linux, Windows).
- **Weaknesses:** Higher-level abstraction may not expose all cloudflared features. Still depends on cloudflared binary.
- **Integration effort:** Medium. Would need to replace the current subprocess spawning approach.
- **Cost:** Free (MIT).
- **Risks:** Low. But the current approach uses cloudflared directly, which provides full access to all cloudflared features.

### bore / localtunnel / serveo

- **Strengths:** Simple, no auth required. Good for quick prototyping.
- **Weaknesses:** No persistent tunnels, no managed modes, no auth, unreliable uptime. Not suitable for production remote access.
- **Integration effort:** Low. Simple subprocess spawn.
- **Cost:** Free.
- **Risks:** High. Unreliable, no security model. Not viable for the use cases in the requirements (remote workers, teams, self-hosters).

## Recommendation

**Direction:** Adopt

The existing tunnel implementation with its provider registry is the right architecture. It already supports Cloudflare (all three modes) and ngrok (beta). The provider registry pattern allows adding new providers without changing the orchestration layer. The main improvements are stabilizing the ngrok provider and adding explicit process monitoring/restart for NFR-03.

## Sources of Information

- `packages/web/server/lib/tunnels/`: Full tunnel module with registry, types, providers, routes, and docs.
- `packages/web/server/lib/tunnels/registry.js`: Provider registry with registration, lookup, and capability listing.
- `packages/web/server/lib/tunnels/types.js`: Tunnel constants, normalization, validation, and error types.
- `packages/web/server/lib/tunnels/DOCUMENTATION.md`: Module documentation.
- `packages/web/server/lib/tunnels/providers/cloudflare.js`: Cloudflare tunnel provider implementation.
- `packages/web/server/lib/tunnels/providers/ngrok.js`: Ngrok tunnel provider (beta).
- `packages/web/server/lib/opencode/core-routes.js:272-410`: Tunnel auth controller integration.
- `cloudflared`: Cloudflare's official tunnel client at `github.com/cloudflare/cloudflared`.
- `node-cloudflared`: npm package at `github.com/JacobLinCool/node-cloudflared`.

## Open Questions

1. Should the ngrok provider be moved from beta to stable, or should additional providers (Tailscale Funnel, frp) be added first?
2. Should tunnel process monitoring/restart (NFR-03) use a process manager (PM2/node-pm2) or a custom polling loop?
