---
title: "Telemetry"
status: done
---

# Specification: Telemetry

## Overview

Client-side telemetry lives in `crates/jcode-telemetry-core` (async queue, lifecycle/onboarding trace, state support) with event structs in `crates/jcode-usage-types` (Install, Upgrade, Auth, SessionStart, TurnEnd, SessionLifecycle with end reasons, ErrorCounts). Server-side ingestion is a Cloudflare Worker in `telemetry-worker/` (worker.js, D1 schema, 24 migrations). This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
client (jcode-telemetry-core, bounded queue cap 2048)
   │  HTTPS POST /v1/event
   ▼
telemetry.jcode.sh (Cloudflare Worker)
   │  validation + schema
   ▼
D1 database (schema.sql + migrations/0001..0024)
   │
   ▼
dashboards (DAU, install funnel, token value, geo, health, users, discovery)
```

## Data Models

### Event Types (`jcode-usage-types`)

| Event | Fields | Description |
|---|---|---|
| InstallEvent | platform, version | Install funnel event. |
| UpgradeEvent | from_version, to_version | Upgrade funnel event. |
| AuthEvent | provider, method | Auth success/failure. |
| OnboardingStepEvent | step | Onboarding progress. |
| SessionLifecycleEvent | reason | Includes `SessionEndReason` (e.g. crash). |
| TurnEndEvent | usage | Turn-level token usage. |
| ErrorCounts | category | Error aggregates. |

Events are schema-versioned (schema version 6 in `jcode-telemetry-core`).

## API Contracts

### Client -> Worker: `POST https://telemetry.jcode.sh/v1/event`

**Body**: JSON event object with shared metadata (version, platform, session id, coarse geography added server-side).

## Sequences

### Event emission

```
Trigger (install/session start/turn end/...) → build event → push to bounded queue
Background task flushes queue → POST /v1/event → worker validates → D1 insert
Opt-out env var set → queue disabled → no events emitted
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Bounded background queue | `BACKGROUND_QUEUE_CAPACITY: 2048` | Non-blocking, bounded memory (NFR-3). |
| Cloudflare Worker + D1 | `telemetry-worker/` | Cheap serverless ingestion with SQL analytics. |
| Explicit opt-out | env vars or file marker | Trust and compliance (FR-3). |
| No content collection | event structs exclude messages | Privacy boundary (NFR-1). |
| D1 size self-defense | migrations + size controls | Keeps cost and availability bounded. |

## Risks and Unknowns

1. Server-side dashboards depend on D1 data quality and retention; retention is not documented.
2. Opt-out coverage must be re-checked as new event sites are added.

## Out of Scope

- Individual-session profiling or user tracking beyond aggregate product metrics.
- Collection of prompts, responses, or message content by design.
