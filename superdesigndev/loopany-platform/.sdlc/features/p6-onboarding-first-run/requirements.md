---
title: "Onboarding & First-Run Experience"
status: done
---

# Requirements: Onboarding & First-Run Experience

## Overview

The onboarding experience guides a brand-new user from an empty workspace to their first loop's first run. It is its own route (`/onboarding`), never a homepage overlay, and advances only on detected reality: the machine step reuses the real `createMachine`/`machineStatus`, the create step reuses the real `mintClaim`/`claimStatus` with the Housekeeper template, and a final `live` step folds the celebration, first-run wait, and notification binding. The live creation checklist shows agent-reported milestones lighting up, and a dev-only simulation lets the whole flow be clicked locally without a second machine.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| New user | A guided, skippable walk from sign-in to a real running loop, with honest states (never a spinner-trap). |
| Product | One onboarding surface that mirrors how a loop is really born, reusing production machinery so it never drifts. |
| Developer | A dev-only simulation gate so the flow is clickable locally without a second machine or GitHub OAuth. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | Onboarding shall be its own route, entered once for a fully empty workspace (no loops and no machines) and re-openable as a quiet banner while the user has no loops. |
| FR-2 | Must | The route shall carry the dashboard's team as `?team=<id>` and validate it with the same `canViewTeam` gate as `/t/$teamId`. |
| FR-3 | Must | The machine step shall reuse `createMachine`/`machineStatus` and gate Continue on `.online`. |
| FR-4 | Must | The create step shall reuse `mintClaim`/`claimStatus` with the Housekeeper template `description`, auto-advancing on `.done`. |
| FR-5 | Must | The wizard shall persist step + minted tokens per team via a pure state module so a mid-flow reload resumes. |
| FR-6 | Must | The "Meet Housekeeper" step shall play a four-act spring-physics storyboard driven by one elapsed-ms clock, with hover pause and a reduced-motion stills path. |
| FR-7 | Must | The creation checklist shall show agent-reported milestones lighting up, derived from a fixed enum tolerant of skipped/repeated/out-of-order/absent/junk reports. |
| FR-8 | Must | The `live` step shall poll `firstRunStatus` (done → payoff, error → honest failed hand-off, running → live, pending+offline/canceled → scheduled hand-off) and settle only after consecutive scheduled reads. |
| FR-9 | Must | The `live` step shall offer notification binding via the shared `ChannelAddForm`, fully optional with dashboard/see-result always available. |
| FR-10 | Should | A dev-only sim (production build never exposes it) shall simulate machine connect and loop creation through the same store rows a real daemon would write. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | The checklist's claim-progress endpoint shall be enum-only with a body cap and IP flood guard before the body read. |
| NFR-2 | Must | Accessibility | `prefers-reduced-motion` renders a separate 4-frame static-stills path; the storyboard is decorative and never gates Continue. |
| NFR-3 | Should | Performance | The milestone progress map shall be bounded/TTL'd in memory, keyed by the claim token. |
| NFR-4 | Should | Reliability | The first-run poll shall never trigger a run; it only reads run rows. |

## Constraints

- The wizard must not claim a Next without detected reality.
- The checklist is a single shared surface used by both the wizard and the dashboard's compose modal.
- Dev-sim is gated by ONE flag (`LOOPANY_ONBOARDING_SIM` truthy AND not a production build) enforced on both affordance and effect.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** an empty workspace
    - **When** the dashboard loads
    - **Then** the wizard auto-starts once and a back navigation cannot re-trigger it
- [ ] **FR-2**
    - **Given** a bookmarked `/t/<B>` deep link
    - **When** onboarding starts
    - **Then** the machine+claim mint into team B, never the last-used cookie team
- [ ] **FR-3**
    - **Given** the machine step with the daemon not yet connected
    - **When** Continue is attempted
    - **Then** it stays gated until `.online` is detected
- [ ] **FR-4**
    - **Given** a pasted connect snippet
    - **When** the claim resolves `.done`
    - **Then** the wizard auto-advances to the live step
- [ ] **FR-5**
    - **Given** a mid-flow reload
    - **When** the wizard reopens
    - **Then** it resumes at the persisted step and tokens
- [ ] **FR-6**
    - **Given** the cinematic playing
    - **When** hovered or reduced-motion is set
    - **Then** it pauses or renders the static stills; `data-act`/`hk-score`/`hk-day` hooks reflect the state
- [ ] **FR-7**
    - **Given** agent milestone reports
    - **When** the checklist derives state
    - **Then** milestones light up from the highest reported index, tolerant of junk
- [ ] **FR-8**
    - **Given** a pending+offline first run
    - **When** the live step polls
    - **Then** it settles into the queued hand-off only after consecutive scheduled reads
- [ ] **FR-9**
    - **Given** the live step
    - **When** a channel is bound
    - **Then** it reuses the shared `ChannelAddForm` with a live `testChannel` ping; binding is optional
- [ ] **NFR-1**
    - **Given** an oversized or forged claim-progress request
    - **When** it hits the endpoint
    - **Then** the IP flood guard + body cap run before the body is read
- [ ] **NFR-3**
    - **Given** a production build
    - **When** the sim endpoints are hit
    - **Then** both the affordance and the effect refuse

## Conflicts

None identified yet.

## Open Questions

1. None: behavior is fully determined by the code and its tests.
