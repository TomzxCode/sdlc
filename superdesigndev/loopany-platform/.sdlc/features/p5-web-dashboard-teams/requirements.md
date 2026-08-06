---
title: "Web Dashboard, Teams & Run UI"
status: done
---

# Requirements: Web Dashboard, Teams & Run UI

## Overview

The web dashboard is the team surface for Loopany: a TanStack Start application where users see their loops, machines, runs, and timeline, manage teams, and drill into loop and run detail. The team lives in the URL (`/t/$teamId`) with membership-validated scoping, so tabs on different teams can be open at once. Loop detail supports editing (dispatch a run or copy an agent-neutral prompt), run detail shows transcripts, costs, artifacts, and a live activity card, and the cross-loop timeline projects future fires. This feature also covers the shared compose modal and team/machine management surfaces.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop owner | A dashboard where loops, runs, artifacts, and notifications are visible and actionable. |
| Team members | See a shared team surface (loops, timeline, machines, channels) without operating machines. |
| Team owner | Manage membership, roles, invites, and team deletion with safe guards (delete blocked while the team owns loops). |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The dashboard's team shall live in the URL (`/t/$teamId`), with list server fns taking an explicit validated `teamId` (route param wins over the cookie). |
| FR-2 | Must | Bare `/` in gated mode shall redirect to the last-used or personal team; a non-member `/t/<x>` is a generic not-found (enumeration-safe). |
| FR-3 | Must | The dashboard shall list jobs, machines, and teams with a fetch-then-set poll refresh that keeps stale data on a transient blip. |
| FR-4 | Must | Loop detail shall render the loop's generative dashboard, runs list, files panel, and controls (enable/pause, run now, evolve, edit, delete). |
| FR-5 | Must | Run detail shall show transcript, metrics, cost, artifacts, diff, status, and a live activity card while running. |
| FR-6 | Must | Loop editing shall offer two paths: Dispatch (one agent pass on the owner's machine) and Copy prompt (agent-neutral, built by a pure helper). |
| FR-7 | Must | The cross-loop timeline shall be one form at every zoom (row = loop, x = time), with future fires projected from the loop's cron. |
| FR-8 | Must | Team management shall be owner-only for membership changes and support rename, add-by-email, single-use invite links, role changes, leave, and delete. |
| FR-9 | Must | Delete shall be blocked while a team owns loops, and the last-owner guard shall be enforced transactionally. |
| FR-10 | Should | The compose modal shall handle all three shapes (blank, template, bundle) sharing one connect-key machinery. |
| FR-11 | Should | No page shall have horizontal scroll; wide content scrolls inside its own pane. |
| FR-12 | Should | The files panel shall show the task file exactly once with type/title chips from front matter. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Every team fn shall take an explicit teamId and authorize by membership + role, never the active-team cookie. |
| NFR-2 | Must | Security | The last-owner guard shall be transactional so concurrent self-removals cannot strand a memberless team. |
| NFR-3 | Must | Accessibility | Prefers-reduced-motion disables decorative animation; Recharts animation is off including tooltips. |
| NFR-4 | Should | Performance | Recharts stays out of the base client bundle (loop detail lazy-loads the chunk). |
| NFR-5 | Should | Reliability | Source-reading test guards must keep the path in a variable (vite rewrites the literal `new URL` form). |

## Constraints

- Loop detail and run detail are pages, not modals; Base UI Dialog parts require a `Dialog.Root` ancestor.
- The dashboard's team comes from the URL param; the cookie is only the bare-`/` redirect hint, never an auth key.
- Generic operation copy is agent-neutral, never "Claude Code", because Loopany runs multiple agents.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** a signed-in member on `/t/A` and `/t/B`
    - **When** tabs load
    - **Then** each shows its own team's loops and a team switch re-seeds the poll state
- [ ] **FR-2**
    - **Given** a signed-out visitor on a non-member `/t/<x>`
    - **When** the route loads
    - **Then** it throws the same generic not-found as a missing loop
- [ ] **FR-3**
    - **Given** a transient poll blip
    - **When** the dashboard refreshes
    - **Then** stale data is kept, never an invalidate-throw
- [ ] **FR-4**
    - **Given** a loop with a dashboard, files, and runs
    - **When** its detail page loads
    - **Then** all surfaces render and controls are available
- [ ] **FR-5**
    - **Given** a running run
    - **When** its detail page is open
    - **Then** the live activity card shows the pulsing step line and a ticking elapsed clock
- [ ] **FR-6**
    - **Given** the loop edit composer
    - **When** "Copy prompt" is chosen
    - **Then** a pure, agent-neutral prompt is copied with the loop's on-disk dir named when derivable
- [ ] **FR-7**
    - **Given** a loop with a daily cron
    - **When** the timeline renders
    - **Then** future fires project as dashed ghosts past the now-line
- [ ] **FR-8**
    - **Given** an owner managing a team
    - **When** they mint an invite link
    - **Then** a single-use, 7-day link is redeemable by any signed-in user
- [ ] **FR-9**
    - **Given** a team that owns loops
    - **When** delete is attempted
    - **Then** it is blocked with a disabled state, never cascaded
- [ ] **NFR-1**
    - **Given** a member browsing team A
    - **When** they manage team B
    - **Then** authorization checks the explicit teamId, never the cookie
- [ ] **NFR-2**
    - **Given** two concurrent self-removals of the last two owners
    - **When** both commit
    - **Then** exactly one wins; the team never ends up memberless

## Conflicts

None identified yet.

## Open Questions

1. None: behavior is fully determined by the code and its tests.
