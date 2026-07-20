---
title: "Analytics & Cost Tracking"
status: done
---

# Requirements: Analytics & Cost Tracking

## Overview

The analytics and cost tracking feature provides dashboards and reports on session activity, tool usage, token consumption, and associated costs. It includes activity heatmaps, velocity metrics, per-model cost breakdowns, session health signals, and AI-generated insights.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Understand personal productivity patterns and AI agent costs |
| Engineering manager | Team-wide usage visibility via PostgreSQL sync and analytics queries |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall compute and display activity heatmaps over configurable time ranges |
| FR-2 | Must | The system shall track token usage per session and per model |
| FR-3 | Must | The system shall compute cost estimates using a pricing catalog |
| FR-4 | Must | The system shall provide daily cost summaries with per-model breakdowns |
| FR-5 | Must | The system shall compute session health signals (outcome, tool health, context pressure) |
| FR-6 | Must | The system shall provide a session stats endpoint with distribution metrics |
| FR-7 | Must | The system shall support timezone-aware date bucketing |
| FR-8 | Should | The system shall provide AI-generated insights from session data |
| FR-9 | Should | The system shall support automated session classification (human vs automated) |
| FR-10 | Should | The system shall compute velocity metrics (sessions/day, messages/session) |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Analytics queries should complete in under 2 seconds |
| NFR-2 | Should | Accuracy | Cost tracking prices are within 5% of actual provider billing |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** session data exists
    - **When** the analytics page is loaded
    - **Then** activity heatmaps are displayed for the configured time range
- [ ] **FR-4**
    - **Given** sessions have token usage data
    - **When** `agentsview usage daily` is run
    - **Then** a cost summary with model breakdown is printed

## Open Questions

1. How should prompt caching costs be modeled for accurate pricing?
