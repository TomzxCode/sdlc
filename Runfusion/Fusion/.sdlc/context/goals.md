# Goals and Objectives

## Purpose

Fusion exists to solve fragmentation in AI agent work: agents are spread across many products, each locking a developer into its own models, workflows, and surfaces. Fusion is the model- and surface-agnostic orchestration layer that lets a developer drive every agent across machines and surfaces without dropping threads or losing track of what runs where.

## Vision

Fusion becomes the neutral orchestration layer for software delivery: a software factory where rough ideas are planned, built, reviewed, and shipped by a fleet of agents, controllable from any surface and machine, adaptable to any model or workflow.

## Time Horizon

- **Current period:** 2026 H2
- **Period type:** half

## Objectives

### Drive multi-node orchestration to production utility

**Owner:** Core platform team
**Statement:** Make driving agents across machines and surfaces in a scalable, multi-node way the default, reliable experience rather than a single-box tool.

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Active nodes running agents per week | Growing weekly | Count of nodes executing agent work in the week | Unknown at sync | At risk |

**KPIs (ongoing):**

| KPI | Target | Window | Source |
|---|---|---|---|
| Active nodes | — | Weekly | Node/mesh telemetry |
| Concurrent agent sessions | — | Daily | Dashboard usage/credits |

### Widen surface coverage

**Owner:** Dashboard & shells team
**Statement:** Meet the developer wherever they are: dashboard/kanban, mobile, desktop, and terminal, all driving and observing the same agents.

**KPIs (ongoing):**

| KPI | Target | Window | Source |
|---|---|---|---|
| Mobile/desktop active users | — | Weekly | Shell onboarding data |

### Grow the ecosystem and adaptability

**Owner:** Plugin & models team
**Statement:** Keep the product neutral by evolving with models and workflows via the plugin system, missions, goals, and agent companies.

**KPIs (ongoing):**

| KPI | Target | Window | Source |
|---|---|---|---|
| Unique models + plugins active per user | — | Monthly | Settings/usage data |

### Keep the outcome signal strong

**Owner:** Whole team
**Statement:** Prioritize shipped, working code over activity.

**KPIs (ongoing):**

| KPI | Target | Window | Source |
|---|---|---|---|
| Task completion rate | — | Weekly | Task store |
| LOC shipped via Fusion | — | Weekly | Merge/commit stats |

## Strategic Pillars

- **Multi-node orchestration** — work must scale out beyond a single box
- **Surface coverage** — no surface is the "real" one; every surface can drive and observe agents
- **Ecosystem & adaptability** — neutrality lives in the plugin system and model/workflow swapping
- **Pluggable multi-user** — open, pluggable extension points for access, roles, and deployment models

## Non-Goals

- Locking the product to any single model, provider, or workflow vendor
- A hardcoded multi-user permission model before the pluggable extension points exist
- Publishing the private `@fusion/*` packages as independently versioned artifacts

## Alignment

| Feature / Initiative | Objective | Notes |
|---|---|---|
| FEAT-p9 (Multi-node operator surfaces & shells) | Multi-node orchestration / Surface coverage | Mesh, nodes, projects, desktop, mobile |
| FEAT-p4 (Agent execution engine) | Multi-node orchestration | Durable agents, heartbeat, scheduler |
| FEAT-p10 (Plugins & extensions) | Ecosystem & adaptability | Plugin SDK, pi extensions |
| FEAT-p1 (Task board & lifecycle) | Outcome signal | The board that tracks completion |
| FEAT-p5 (Automated review, merge & PR) | Outcome signal | Shipment of code via Fusion |

## Review Cadence

- **Review frequency:** monthly
- **Last reviewed:** 2026-06-02 (STRATEGY.md)
- **Next review:** monthly cadence TBD

## Open Questions

1. KPI targets and measurement sources are not all instrumented; this file should be reconciled against actual dashboard metrics during the next goals review.
2. "Agent companies" (from STRATEGY.md) is not yet implemented in the codebase; confirm whether it is a roadmap concept or a shipped feature.
