---
title: "Telemetry"
status: done
---

# Requirements: Telemetry

## Overview

jcode collects opt-out telemetry to understand product health: installation and upgrade funnels, auth success, onboarding progress, session start/end/crash, and turn-end usage. Events are queued client-side in `jcode-telemetry-core`, sent to `https://telemetry.jcode.sh/v1/event`, and ingested by a Cloudflare Worker into D1 for dashboards and analysis. The full disclosure and opt-out model is documented in `TELEMETRY.md`. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Maintainer | Product-health metrics (DAU, install funnel, token value) without violating user trust |
| End users | Clear disclosure of what is and is not collected, and an easy opt-out |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall emit structured telemetry events for install, upgrade, auth success, onboarding step, feedback, sponsored discovery, session lifecycle, and turn end. |
| FR-2 | Must | The system shall queue and flush events asynchronously without blocking the agent. |
| FR-3 | Must | The system shall respect opt-out via `JCODE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, or a file marker. |
| FR-4 | Must | The system shall never collect message content, prompts, or responses. |
| FR-5 | Must | The system shall ingest events server-side into a Cloudflare Worker backed by D1. |
| FR-6 | Should | The system shall provide analytics views (DAU, install conversion funnel, token value, geography). |
| FR-7 | Should | The system shall support schema versioning for events so changes are trackable. |
| FR-8 | Should | The system shall capture session end reasons (including crashes) for reliability analysis. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Privacy | Event payloads must not contain session content or identifying message text. |
| NFR-2 | Should | Reliability | Failed telemetry sends must not fail the client workflow. |
| NFR-3 | Should | Performance | The background queue must be bounded and non-blocking. |
| NFR-4 | Should | Availability | Server-side ingestion must tolerate bursts (bounded D1 usage). |

## Constraints

- Opt-out must be discoverable and documented (`TELEMETRY.md`).
- Schema and D1 size must be controlled (migrations, size self-defense).

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** an install and a session start
    - **When** events fire
    - **Then** install, session_start, and turn_end events are produced with the documented shape
- [ ] **FR-2**
    - **Given** an active session
    - **When** the agent is running
    - **Then** telemetry sending does not block the turn loop
- [ ] **FR-3**
    - **Given** `JCODE_NO_TELEMETRY=1` set
    - **When** jcode runs
    - **Then** no telemetry events are emitted
- [ ] **FR-4**
    - **Given** an active session with message content
    - **When** events are produced
    - **Then** no message content or prompt text is included
- [ ] **FR-5**
    - **Given** emitted events
    - **When** they reach the ingestion endpoint
    - **Then** they are stored in D1 with the schema applied
- [ ] **FR-6**
    - **Given** ingested data
    - **When** dashboards run
    - **Then** DAU, install funnel, and token-value views render
- [ ] **FR-7**
    - **Given** a new event shape
    - **When** it is emitted
    - **Then** the schema version is bumped and tracked
- [ ] **FR-8**
    - **Given** a crashed session
    - **When** the session ends
    - **Then** the end reason (crash) is captured in the event
- [ ] **NFR-1**
    - **Given** any telemetry payload
    - **When** inspected
    - **Then** it contains no session content or message text
- [ ] **NFR-2**
    - **Given** a failing telemetry endpoint
    - **When** the client continues
    - **Then** the client workflow is unaffected
- [ ] **NFR-3**
    - **Given** high event volume
    - **When** the queue fills
    - **Then** the queue stays bounded (capacity 2048) and does not grow unbounded
- [ ] **NFR-4**
    - **Given** an event burst
    - **When** the worker ingests it
    - **Then** D1 usage stays within the self-defense limits

## Conflicts

None identified yet.

## Open Questions

1. What is the retention window for D1 data and when are aggregates rolled up? Not documented beyond the dashboards.
