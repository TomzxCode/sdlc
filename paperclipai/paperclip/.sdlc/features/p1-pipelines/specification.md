---
title: "Pipelines"
status: draft
---

# Specification: Pipelines

## Overview

The pipeline system provides structured stage-based workflow management for tracking work items. It defines pipelines with ordered stages and allowed transitions, and cases that flow through those stages. Automated agents can claim, transition, and execute work on cases. The system records every state change as a typed event for full auditability.

## Architecture

The pipeline system lives in `server/src/services/pipelines.ts` (5158 lines) with aggregation support in `pipelines-aggregation.ts` and conversation context in `pipeline-conversation-context.ts`. UI pages at `ui/src/pages/Pipelines.tsx` and `PipelineSettings.tsx`. Route file at `server/src/routes/pipelines.ts` (2913 lines). The system uses Drizzle for DB access and integrates with the heartbeat/issue assignment wakeup system for automation.

## Data Models

### pipelines

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Pipeline identifier |
| company_id | uuid | FK to companies, not null | Owning company |
| project_id | uuid | FK to projects, nullable | Associated project |
| key | text | not null, unique per company | Unique pipeline key |
| name | text | not null | Display name |
| description | text | nullable | Optional description |
| enforce_transitions | boolean | not null, default false | Whether to enforce allowed transitions |
| created_by_user_id | text | nullable | Creating user |
| created_by_agent_id | uuid | FK to agents, nullable | Creating agent |
| archived_at | timestamp | nullable | Soft-delete timestamp |

### pipeline_stages

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Stage identifier |
| pipeline_id | uuid | FK to pipelines, not null | Parent pipeline |
| key | text | not null, unique per pipeline | Stage key |
| name | text | not null | Display name |
| kind | text | not null, check (working, review, done, cancelled) | Stage classification |
| position | integer | not null | Display order |
| config | jsonb | not null, default {} | Stage-specific configuration |

### pipeline_transitions

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Transition identifier |
| pipeline_id | uuid | FK to pipelines, not null | Parent pipeline |
| from_stage_id | uuid | FK to pipeline_stages, not null | Source stage |
| to_stage_id | uuid | FK to pipeline_stages, not null | Target stage |
| label | text | nullable | Display label |

### pipeline_cases

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Case identifier |
| company_id | uuid | FK to companies, not null | Owning company |
| pipeline_id | uuid | FK to pipelines, not null | Parent pipeline |
| stage_id | uuid | FK to pipeline_stages, not null | Current stage |
| case_key | text | not null | Unique case key |
| title | text | not null | Case title |
| summary | text | nullable | Optional summary |
| fields | jsonb | not null, default {} | Structured case fields |
| workspace_ref | jsonb | nullable | Reference to execution workspace |
| parent_case_id | uuid | FK self, nullable | Parent case in hierarchy |
| version | integer | not null, default 1 | Case version for concurrency |

### pipeline_case_events

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Event identifier |
| company_id | uuid | FK to companies, not null | Owning company |
| case_id | uuid | FK to pipeline_cases, not null | Parent case |
| type | text | not null (ingested, transitioned, claimed, etc.) | Event type |
| actor_type | text | not null | User, agent, or system |
| payload | jsonb | not null, default {} | Event-specific data |

## API Contracts

### GET /api/pipelines

Returns pipelines for a company.

### POST /api/pipelines

Create a new pipeline.

### GET /api/pipelines/:id/cases

List cases in a pipeline with optional stage filter.

### POST /api/pipelines/:id/cases

Create a new case in a pipeline.

### POST /api/pipelines/cases/:id/transition

Transition a case to a new stage.

### POST /api/pipelines/cases/:id/claim

Claim a case with lease-based ownership.

## Sequences

### Case Lifecycle

```
Agent → POST claim → Server checks lease availability → DB assigns lease → Returns lease token
Agent → POST transition → Server validates transition allowed → DB updates stage → Records event
System → Automation trigger → Server executes automation logic → DB updates case → Records event
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Case ownership | Lease-based with expiry | Prevents abandoned cases blocking progress |
| Stage kinds | Fixed set (working, review, done, cancelled) | Simple workflow model for the initial implementation |
| Event sourcing | Typed event log on pipeline_cases | Full audit trail without complex event sourcing infrastructure |
| Automation | Integration with heartbeat/run system | Reuses existing agent invocation infrastructure |

## Risks and Unknowns

1. Pipeline automation may have complex retry and error recovery requirements not yet fully understood.
2. Integration between pipeline cases and the issue/task system needs clearer semantics.
3. Performance of case event queries at scale (many events per case) is untested.

## Out of Scope

- Drag-and-drop pipeline builder UI (deferred)
- Complex branching workflows beyond linear stage progression
- Pipeline templates or sharing across companies
