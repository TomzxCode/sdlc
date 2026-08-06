---
title: "Web Dashboard, Teams & Run UI"
status: done
---

# Specification: Web Dashboard, Teams & Run UI

## Overview

The web app is a TanStack Start application (React 19, Tailwind v4, Base UI, Recharts, CodeMirror). Server functions (`src/server/loopApi.ts`) drive the dashboard; team logic lives in framework-free `src/server/teamAdmin.ts` with a thin `teamFns.ts` RPC wrapper. Routes render the dashboard under `/t/$teamId` (plus open-mode `/`), loop detail under `/loops/$loopId`, run detail under `/loops/$loopId/runs/$runId`, and the cross-loop timeline under `/t/$teamId/timeline`.

## Architecture

```
/t/$teamId → DashboardView (mounts with key=teamId → fetch-then-set poll)
  ├─ listJobs / listMachines / listMyTeams (explicit teamId, requestScope)
  ├─ BundleCarousel → ComposeModal (blank | template | bundle)
  └─ TeamsModal / MachinesModal / NotificationsModal
/loops/$loopId → LoopDetailView (LoopView dashboard chunk lazy-loaded)
/loops/$loopId/runs/$runId → RunView (LiveActivity while run.running)
/t/$teamId/timeline → LoopTimeline (projectFires + run query, row=loop, x=time)
```

Team authorization: every fn takes an explicit `teamId` and checks membership + role via `assertOwner` (single chokepoint); non-members get the enumeration-safe generic not-found.

## Data Models

The UI consumes Drizzle rows through `adapters.ts` (Loop/Run → JobSummary/JobDetail):

- `teams` + `team_members` (roles `owner`/`member`) + `team_invites` (single-use, 7-day, role-baked).
- `machines` (presence via `lib/machinePresence.ts`: online <30s, asleep <6h, else offline).
- `loops` (via `loopApi` adapters incl. the derived `nextFire`/`classification`/`runs`).
- `runs` (via run detail adapters: transcript, usage, cost, artifacts, progress).

## API Contracts

The UI consumes server functions, not REST: `listJobs(teamId)`, `listMachines(teamId)`, `listMyTeams()`, `listTimeline(teamId, range)`, `mintClaim`, `claimStatus`, `createChannel`, `testChannel`, `requestEdit`, `copyEditPrompt` (pure client helper), `getJobDetail`, `getArtifact`, and `firstRunStatus`. Team management RPCs (`createTeam`, `renameTeam`, `addMemberByEmail`, `createInvite`, `redeemTeamInvite`, `setMemberRole`, `removeMember`, `leaveTeam`, `deleteTeam`) route through `teamFns.ts` → `teamAdmin.ts`.

## Sequences

### Team invite redeem

```
owner: TeamsModal → createInvite → POST (token, role baked) → share /invite/<token>
recipient (signed-in) → GET /invite/<token> → redeemTeamInvite
  ├─ invalid / already-used (redeemedAt stamped) / expired → error
  ├─ already-member → success (link burned, no double-add)
  └─ fresh join at the invite's role
signed-out visitor → gated SignIn with callbackURL back to the invite
```

### Loop edit dispatch

```
LoopDetailView editVia:
  (1) Dispatch → requestEdit({id, instruction}) → scheduler.requestEdit → next tick runs an edit run
  (2) Copy prompt → buildEditPrompt (pure) → clipboards a self-contained prompt
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Team in the URL | `/t/$teamId` param, cookie is last-used hint only | Different teams in different tabs; route param wins over cookie |
| Poll refresh | Fetch-then-set, never `router.invalidate` | The loader re-run throws on a transient blip; keep stale data |
| Team logic layer | `teamAdmin.ts` framework-free, `teamFns.ts` thin RPC | Every rule testable against real pglite without mocking the Start runtime |
| Delete safety | Blocked while the team owns loops; last-owner transactional | Never strand a memberless team or orphan loops |
| Timeline | Row = loop, x = time, zoom changes only the window; future fires projected | A run is a point event, so Gantt bars have no length; lanes line up vertically on contention |
| Agent-neutral copy | "your coding agent", not "Claude Code" | Loopany runs claude-code, codex, and grok |
| No page-level h-scroll | `min-w-0` on grid/flex children; panes scroll internally | Pinned by `*.regression.test.ts` guards |

## Risks and Unknowns

1. Dashboard header still overflows below ~690px (pre-existing, not the content grid).
2. The timeline projection is capped per loop and the run query is capped, surfaced as `truncated` when exceeded.

## Out of Scope

- The onboarding wizard and first-run flow (separate feature).
- The template market pages (separate feature).
- Notification channel binding UI internals (notifications feature owns the shared `ChannelAddForm`).
