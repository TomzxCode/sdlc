---
title: "Docker / Self-Hosted Deployment"
status: done
---

# Specification: Docker / Self-Hosted Deployment

## Overview

The Docker setup uses a multi-stage `Dockerfile` (build stage with Bun, runtime stage with Bun + system deps). `docker-compose.yml` defines the service with volume mounts. `scripts/docker-entrypoint.sh` handles startup. `Caddyfile` provides reverse proxy config.

## Architecture

```
Dockerfile (multi-stage)
    Stage 1 (deps): Install dependencies
    Stage 2 (builder): Build web assets
    Stage 3 (runtime): Production image with Bun, Node, Git, SSH, cloudflared
    |
docker-compose.yml
    +---> Volume mounts (config, data, SSH, workspaces)
    +---> Environment variable configuration
    |
scripts/docker-entrypoint.sh
    +---> Start OpenCode server
    +---> Start OpenChamber
    |
Caddyfile (optional HTTPS termination)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Base image | oven/bun | Consistent with development toolchain |
| User | Non-root (openchamber, UID 1000) | Security best practice; matches volume ownership |
| OpenCode install | npm install -g opencode-ai | Ensures CLI is available inside container |

## Out of Scope

- Kubernetes Helm charts
- Docker Swarm configuration
- Automated container updates
