---
issue: ""
title: "Docker / Self-Hosted Deployment"
status: draft
---

# Existing Solutions: Docker / Self-Hosted Deployment

## Overview

The codebase already has a working Dockerfile (multi-stage build with Bun), docker-compose.yml with persistent volumes and environment variable configuration, a Caddyfile for HTTPS reverse proxy, cloudflared inside the container via the official image, and OpenCode CLI auto-installed via npm. The Docker setup is documented in the README and already used in production by self-hosters. The main gaps are polish: entrypoint script hardening, better environment variable documentation, and optional optimizations like non-root user hardening and health checks.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `Dockerfile`, `docker-compose.yml`, `Caddyfile`, `packages/web/server/lib/opencode/openchamber-routes.js` (Docker detection), `packages/web/server/lib/opencode/tunnel-auth.js` (host.docker.internal), `scripts/docker-entrypoint.sh`, `CHANGELOG.md` |
| Open-source | Yes | Docker multi-stage build patterns, docker-compose best practices, cloudflared Docker integration |
| Commercial / SaaS | No | N/A — self-hosted deployment only |
| Standards / protocols | Yes | Dockerfile reference, docker-compose spec, OCI container standards |
| Reference material | Yes | Docker docs, Caddy docs, cloudflared docs, Open WebUI deployment patterns |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing OpenChamber Dockerfile + docker-compose.yml | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-05, FR-08 | FR-06 (Caddy config exists but is dev-focused) |
| Docker multi-stage build pattern | Standard | N/A | Mature | FR-01 | N/A |
| cloudflared Docker image (official) | Product | MIT | Mature | FR-04 | N/A |
| Caddy reverse proxy | Product | Apache 2.0 | Mature | FR-06 | Existing Caddyfile is dev-only, needs production template |
| Open WebUI Docker deployment | Reference | MIT | Mature | Reference for env-var-based Docker config | Not applicable to OpenChamber directly |
| Langfuse Docker deployment | Reference | MIT | Mature | Reference for multi-service docker-compose + env config | Not applicable to OpenChamber directly |

## Evaluation

### Existing OpenChamber Dockerfile + docker-compose.yml

- **Strengths:** Already production-used by community.
  Multi-stage build keeps image size down (build deps in builder stage, runtime only in final).
  Includes cloudflared from official image, OpenCode CLI auto-installed via npm, git/openssh/python3 for agent tooling.
  docker-compose.yml provides persistent volume mounts for config, state, SSH keys, and workspaces.
  Environment variables cover port, password, tunnel provider/mode/hostname/token, external OpenCode host.
  Docker detection logic already exists in the server (`/.dockerenv`, `process.env.container`).
  `host.docker.internal` is added for external OpenCode access.
- **Weaknesses:** Caddyfile exists but targets a dev scenario (self-signed TLS on port 3443 proxying to 3001), not a production HTTPS setup.
  Entrypoint script (`scripts/docker-entrypoint.sh`) not reviewed in this survey but referenced.
  No health check in docker-compose.yml.
  No Docker image publishing (by design per FR-08).
  No dockerignore file found.
  No CPU/memory limits in docker-compose.yml.
- **Integration effort:** Low — the solution already exists.
- **Cost:** Free.
- **Risks:** Low — well-established pattern.

### Docker multi-stage build

- **Strengths:** Standard best practice for Node.js/Bun images.
  Reduces final image size significantly.
  Well-documented by Docker.
- **Weaknesses:** N/A — already implemented.
- **Integration effort:** Already done.
- **Cost:** Free.
- **Risks:** None.

### cloudflared Docker integration

- **Strengths:** Official Cloudflare image with pinned digest for reproducibility.
  Supports quick/managed-remote/managed-local tunnel modes.
- **Weaknesses:** Requires Cloudflare account for managed tunnels.
- **Integration effort:** Already done — binary copied into final image.
- **Cost:** Cloudflare tunnel is free for basic use.
- **Risks:** Pinned digest needs updating manually when upgrading cloudflared.

### Caddy reverse proxy

- **Strengths:** Automatic HTTPS via Let's Encrypt.
  Simple configuration syntax.
  Well-maintained and widely used for self-hosted deployments.
- **Weaknesses:** Existing Caddyfile is development-only, not suitable for production deployment.
- **Integration effort:** Low — would add a `Caddyfile.production` or update the existing one.
- **Cost:** Free.
- **Risks:** None.

## Recommendation

**Direction: Adopt**

The existing Dockerfile and docker-compose.yml are production-ready and already used by the community.
The focus should be on hardening the Caddyfile for production use, adding health checks, ensuring the entrypoint script handles all edge cases (signal handling, graceful shutdown), and providing better documentation for the environment variables.
No external library or tool is needed beyond what is already in use.

## Sources of Information

- Existing `Dockerfile` at repository root: multi-stage build with Bun runtime, apt system deps, cloudflared, and OpenCode CLI.
- Existing `docker-compose.yml`: services definition with volumes, environment variables, and host.docker.internal.
- Existing `Caddyfile`: dev reverse proxy config for port 3443.
- Open WebUI Docker deployment docs: good reference for env-var-driven Docker configuration of an AI web app.
- Langfuse Docker deployment: reference for multi-service docker-compose with env configuration.

## Open Questions

1. Should the entrypoint script handle graceful shutdown via SIGTERM/SIGINT forwarding to the Node process?
2. Should a production Caddyfile be provided alongside the dev one, or should the existing one be upgraded?
3. Should docker-compose.yml include resource limits and health checks?
