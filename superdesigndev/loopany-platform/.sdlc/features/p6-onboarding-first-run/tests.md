---
title: "Onboarding & First-Run Experience"
status: done
---

# Test Plan: Onboarding & First-Run Experience

## Scope

Testing the onboarding wizard state machine, the Housekeeper cinematic, the creation checklist, the claim-progress endpoint guards, the first-run branch table, the dev-only sim gate, and the onboarding-state persistence. Out of scope: dashboard list surfaces and notification binding internals.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Wizard auto-starts once for an empty workspace | No loops + no machines | Wizard starts; `markOnboardingDismissed` set BEFORE redirect so Back can't re-trigger |
| TC-2 | Onboarding entry prefers the URL team over the cookie | `?team=<B>` bookmarked | Machine+claim mint into team B |
| TC-3 | Machine step gates Continue on `.online` | `machineStatus` offline | Continue disabled until detected online |
| TC-4 | Create step auto-advances on `.done` | `claimStatus` done | Wizard advances without a claimed Next |
| TC-5 | Onboarding state persists per team across reloads | Mid-flow reload | Resumes at the persisted step + tokens |
| TC-6 | Creation checklist derives milestone states | Skipped/repeated/out-of-order/absent/junk reports | Highest reported index lights up; junk tolerated |
| TC-7 | First-run branch table returns each hand-off | done / error / running / pending+offline / canceled | done→payoff, error→failed (honest copy), running→live, others→scheduled |
| TC-8 | Scheduled hand-off settles only after consecutive reads | Transient pending reads then settled | `SCHEDULED_SETTLE_POLLS` consecutive reads before terminal |
| TC-9 | Sim gate refuses in production builds | `onboardingSimEnabled()` false | Sim endpoints refuse; affordance hidden |
| TC-10 | Claim-progress is enum-only and re-validated at storage | Junk step value | Rejected; bounded TTL'd map keyed by claim token |
| TC-11 | Cinematic advances from one elapsed-ms clock | Hover pause, replay, finished flag | Pure function of `elapsed`; interval stops once finished |
| TC-12 | Cinematic reduced-motion path | `prefers-reduced-motion` | Separate 4-frame static-stills path; `data-act="stills"` |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | First run errors | Honest non-success hand-off, never "First run complete" |
| TC-14 | Claim-progress flood/oversize | IP flood guard + body cap run before the body read |
| TC-15 | Checklist quiet period | Elapsed-aware reassurance after 25s quiet, never gating |
| TC-16 | Cinematic with the ticker guard | Reads a `finished` boolean, not `elapsed`, so it stops once finished |
| TC-17 | React synthesized enter/leave | Tests dispatch delegated mouseover/mouseout, not raw enter/leave |

## Test Infrastructure

- vitest with jsdom and fake timers driving the elapsed-ms clock and poll loops.
- Dev-sim exercised through the same store rows a real daemon writes (pglite integration).
- `data-act`/`data-testid=hk-score`/`hk-day` are the cinematic test hooks.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-2 |
| FR-3 | TC-3 |
| FR-4 | TC-4 |
| FR-5 | TC-5 |
| FR-6 | TC-11, TC-12, TC-16 |
| FR-7 | TC-6 |
| FR-8 | TC-7, TC-8 |
| FR-9 | live-step binding shared surface (covered by `ChannelAddForm` integration) |
| FR-10 | TC-9 |
| NFR-1 | TC-10, TC-14 |
| NFR-2 | TC-12 |
| NFR-3 | TC-10 |
| NFR-4 | TC-7 (read-only poll) |
