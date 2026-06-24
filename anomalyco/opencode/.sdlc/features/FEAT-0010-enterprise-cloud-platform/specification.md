---
title: "Enterprise & Cloud Platform"
status: draft
---

# Specification: Enterprise & Cloud Platform

## Architecture

```
SST (sst.config.ts) ──▶ infra/
  ├── app/          (cloud app service)
  ├── console/      (management console)
  ├── enterprise/   (self-hosted web app)
  ├── lake/         (data warehouse)
  ├── monitoring/   (OpenTelemetry, Sentry)
  ├── stats/        (analytics dashboard)
  └── identity/     (OpenAuth auth service)

packages/console/ ──▶ SST Console (app, core, function, mail, resource, support)
packages/stats/   ──▶ Stats dashboard (app, core, server)
packages/enterprise/ ──▶ Enterprise web app (SolidJS + Hono + SST)
```

The platform uses SST for infrastructure-as-code deployment, with separate packages for each service domain.

## Data Models

### team

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Team identity |
| name | text | not null | Display name |
| members | array | not null | Member references |

### deployment_stage

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | text | PK | Stage name (app, console, enterprise, etc.) |
| status | enum | not null | deploying, active, failed |

## API Contracts

Enterprise routes follow the same HTTP API pattern as the core server (see FEAT-0006) with added authentication middleware.

## Sequences

### Enterprise deployment

```
sst deploy --stage enterprise
infra definitions -> Cloudflare/Custom server
enterprise app initializes -> database, auth, teams
admin creates team -> invites members -> members access shared sessions
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| IaC | SST | Unified deployment for all services; polyglot stage definitions |
| Enterprise auth | OpenAuth | Open-source, standards-compliant auth service |
| Monitoring | OpenTelemetry + Sentry | Production-grade observability across services |

## Risks and Unknowns

1. Enterprise licensing and pricing model is not yet defined.
2. External identity provider integration (SAML, OIDC) is a likely future requirement.

## Out of Scope

- Core session runtime (see FEAT-0001).
- Plugin system (see FEAT-0007).
