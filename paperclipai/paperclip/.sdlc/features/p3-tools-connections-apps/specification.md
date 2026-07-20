---
title: "Tools, Connections & Apps"
status: done
---

# Specification: Tools, Connections & Apps

## Architecture

The tools subsystem is organized around several service modules that handle connection lifecycle, policy evaluation, gateway proxying, and runtime management. The app gallery provides a discovery layer on top of MCP-based tool integrations.

```
App Gallery ──► Tool Profile ──► Tool Access Policy ──► Tool Gateway ──► External Service
                      │                                        │
                      ▼                                        ▼
              Profile Binding                          Content Guards
              Precedence                               Runtime Supervision
                                                       Usage Metrics
```

## Data Models

### tool_access (schema)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Access record identifier |
| company_id | uuid | FK to companies, not null | Owning company |
| target_type | text | not null | Connection, profile, or policy target type |
| target_id | uuid | not null | Target entity identifier |
| principal_type | text | not null | User or agent |
| principal_id | text | not null | Principal identifier |
| permission | text | not null | Granted permission level |
| created_at | timestamptz | not null, default now | Creation timestamp |

## API Contracts

### GET /api/tool-access

List tool access records for a company.

### POST /api/tool-access

Create a new tool access record.

### Tool Gateway endpoints

HTTP-based tool gateway for proxying calls to external services with auth injection, content guards, and policy enforcement.

## Key Sequence Flows

### Tool Call Flow

```
Agent → Tool Gateway → Policy Check → Content Guard Scan → Auth Injection
   → External Service → Response → Usage Logging → Agent
```

### Connection Setup

```
Operator → Initiate OAuth → Browser redirect → User authorizes → Callback received
   → Store encrypted tokens → Connection active in app gallery
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Gateway protocol | MCP/SSE with HTTP fallback | Supports both streaming and request-response tool patterns |
| Policy model | Per-company, principal-based grants | Consistent with existing authz system design |
| Credential storage | Reuses secrets system encryption | No separate credential vault needed; encrypted at rest |

## Risks and Unknowns

1. Tool call latency depends on external service responsiveness; timeout and retry configuration needs tuning.
2. Content guards may produce false positives for legitimate tool invocations; guard rules need careful calibration.
3. App gallery installation and update lifecycle is not yet defined.

## Out of Scope

- Public app store/marketplace for community tool integrations (deferred)
- Custom tool authoring SDK (agents use existing MCP tools)
- Tool usage billing or cost allocation (deferred to budget system)
