---
title: "Tools, Connections & Apps"
status: done
---

# Requirements: Tools, Connections & Apps

## Overview

The tools, connections, and apps subsystem provides a third-party integration framework that lets agents use external services (GitHub, Slack, file systems, etc.) through a managed tool gateway. It handles OAuth-based connection lifecycle, tool access policies with runtime enforcement, MCP/SSE gateway proxying, tool runtime profiles with capacity management, and an app gallery for discovering and installing pre-built integrations. Every tool call is governed by content guards, access policies, and runtime supervision to prevent data leaks and runaway executions.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Configure tool connections, set access policies, review usage metrics, manage the app gallery |
| Agent | Discover available tools, invoke them through the gateway with appropriate auth and policy enforcement |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating OAuth-based connections to third-party services with configurable scopes. |
| FR-02 | Must | The system shall support tool access policies that define which agents can use which tools under what conditions. |
| FR-03 | Must | The system shall proxy tool calls through an MCP/SSE gateway that enriches requests with connection auth and applies content guards. |
| FR-04 | Must | The system shall support tool runtime profiles with capacity limits, timeout configuration, and concurrency management. |
| FR-05 | Must | The system shall record tool usage metrics per agent, per tool, per company for observability and audit. |
| FR-06 | Must | The system shall support content guards that prevent sensitive data from being transmitted through tool calls. |
| FR-07 | Should | The system shall support an app gallery for browsing, installing, and configuring pre-built tool integrations. |
| FR-08 | Should | The system shall support tool profile binding precedence for resolving which profile applies to an agent-project combination. |
| FR-09 | Should | The system shall support runtime slot leasing for managing concurrent tool process execution capacity. |
| FR-10 | Should | The system shall support a local service supervisor for managing locally-running tool-related services. |
| FR-11 | May | The system shall provide a tools MCP server package for external access to Paperclip tool resources. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Tool access must enforce company boundaries and principal permission grants. |
| NFR-02 | Must | Security | Connection credentials must be stored encrypted at rest (via the secrets system). |
| NFR-03 | Must | Observability | Every tool call must be logged with agent identity, tool name, duration, and outcome. |
| NFR-04 | Should | Performance | Tool call proxying must complete within the configured timeout with a p99 latency under 5 seconds for standard tools. |

## Constraints

- Tool access policies are company-scoped and evaluated per-invocation.
- Connections are scoped to a company and may be shared across agents within that company.
- Content guard rules are evaluated before the tool call is proxied to the external service.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** A board operator with company access
    - **When** They initiate an OAuth connection flow for a supported service
    - **Then** The connection is created with the requested scopes and stored encrypted
- [ ] **FR-02**
    - **Given** A tool access policy exists for company A
    - **When** An agent from company B attempts to use the tool
    - **Then** Access is denied
- [ ] **FR-03**
    - **Given** An agent with tool access
    - **When** They invoke a tool through the gateway
    - **Then** The request is enriched with auth credentials and proxied; content guards are applied
- [ ] **FR-05**
    - **Given** An agent invokes a tool
    - **When** The call completes
    - **Then** A usage metric record is created with agent, tool, duration, and outcome

## Conflicts

None identified yet.

## Open Questions

1. How does tool access policy interact with the existing auth/permission system's principal permission grants?
2. Are app gallery installations per-company or per-instance?
3. How are MCP server capabilities discovered and registered for the tool gateway?
