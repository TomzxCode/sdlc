---
title: "Onboarding & First-Run Experience"
status: done
---

# Specification: Onboarding & First-Run Experience

## Overview

The onboarding wizard (`routes/onboarding.tsx` → `components/OnboardingWizard.tsx`) mirrors how a loop is really born, reusing the production machinery: `createMachine`/`machineStatus` for the machine step, `mintClaim`/`claimStatus` + the Housekeeper template for the create step, and a pure branch-table first-run poll for the live step. Milestone reporting flows through `POST /api/claim/progress` into a bounded TTL'd in-memory map, and a dev-only sim writes the same store rows a real daemon would.

## Architecture

```
/t?team=<id> → DashboardView → OnboardingEntry
   └─ empty workspace (no loops + no machines) → auto-start wizard once
      └─ /onboarding?team=<id> → OnboardingWizard
           Step: Meet Housekeeper (cinematic) → Machine (createMachine/.online)
           → Create (mintClaim/claimStatus + Housekeeper description + CreationChecklist)
           → Live (firstRunStatus + ChannelAddForm binding)
```

State persists per team via `lib/onboardingState.ts` (pure, unit-tested). Milestones report via `loopany progress <step> --connect-key <key>` → `POST /api/claim/progress` → `tokens.ts` `recordClaimProgress` (TTL'd map keyed by claim token).

## Data Models

The wizard writes the SAME store rows a real daemon would:

- `machines` (via `simulateMachineConnect`/`createMachine` → `updateMachine` online).
- `loops` (via `gateway.createLoop` with the claim, `createLoop` fires `scheduler.runNow`).
- `runs` (the first run's row; `firstRunStatus` reads it, never triggers it).
- Claim progress: in-memory TTL'd map keyed by the claim token (`recordClaimProgress`/`readClaimProgress`).

## API Contracts

### POST /api/claim/progress

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| claim | string | yes | `dk_`-shaped claim token |
| step | string | yes | Enum from `CREATION_STEPS` (re-validated at storage) |

**Response (200 OK)**

Records the milestone. The per-IP `machineRouteLimit` runs BEFORE the capped body read; the per-claim bucket rides the token tier only.

### Sim endpoints (dev only)

`server/onboardingSim.ts` `simulateMachineConnect` / `simulateLoopCreated` / `simulateFirstRun` / `simulateNotifyBind` — refuse when `onboardingSimEnabled()` is false (production build or `LOOPANY_ONBOARDING_SIM` unset).

## Sequences

### First-run status branch table (`lib/firstRun.ts` `firstRunStateFrom`)

```
poll firstRunStatus(loopId)
  done → payoff (CTA to /loops/$loopId/runs/$runId)
  error → failed hand-off (honest non-success copy)
  running → live (keep polling)
  pending+offline / canceled → scheduled hand-off,
     terminal only after SCHEDULED_SETTLE_POLLS consecutive scheduled reads
```

### Creation milestone reporting (round 8 emit path)

```
agent runs loopany progress <step> --connect-key <key> per milestone
  → progress-cli.ts runProgress → POST /api/claim/progress (resolves claim from snippet)
  → wizard polls claimProgress alongside claimStatus (checklist NEVER gates)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Own route | `/onboarding`, never a homepage overlay | Never restructures the dashboard |
| Detection-driven | Steps advance only on `.online`/`.done` | Never a claimed Next; mirrors real creation |
| State persistence | `lib/onboardingState.ts` pure per-team | Mid-flow reload resumes; Back can't re-trigger auto-start |
| Cinematic | Spring-physics CSS/SVG/JS, one elapsed-ms clock | No framer-motion; vitest fake timers drive it; reduced-motion stills |
| Milestone enum | `lib/creationSteps.ts` deriveStepStates tolerant of junk | Keys off the highest reported index |
| Emit path | The creation SKILL, not a curl in the pasted prompt | `references/create.md` teaches `loopany progress`; the snippet stays lean |
| Shared surface | One `CreationChecklist` for wizard AND compose modal | The two can't drift |
| Sim gate | `onboardingSimEnabled()` on both affordance and effect | A prod build can reach neither |

## Risks and Unknowns

1. The wizard polls claimStatus and firstRunStatus on timers; backend restarts drop the in-memory claim-progress map (the checklist is never gating, so this only dims milestones).
2. `simulateFirstRun` seeds a finished run so the Loop page shows content; it must never run against prod.

## Out of Scope

- The notification channel internals (shared `ChannelAddForm` is owned by the notifications feature).
- The onboarding template content itself (templates feature owns the Housekeeper card).
