---
title: "Notifications & Channel Bindings"
status: done
---

# Specification: Notifications & Channel Bindings

## Overview

Channels are webhook-shaped credentials (slack/telegram/feishu) created through the shared `ChannelAddForm` (extracted from `NotificationsModal`, reused by the onboarding live step), each verified by a live `testChannel` ping. `gateway/notify.ts` consumes them at run finalization: only exec runs notify, the failure streak derives from persisted run rows (notify at streak 1 then every 5th, success resets), deferred offline runs get ONE calm message, and the circuit breaker auto-pauses at the configured streak with one subsuming note. `webhookGuard.ts` SSRF-contains outbound delivery. The notifier is injected into the gateway so tests observe pushes without network.

## Architecture

```
ChannelAddForm (shared: NotificationsModal + onboarding live step)
  createChannel(teamId, {kind, token}) → store.channels
  testChannel(channel) → live ping (ok/error)

gateway/notify.ts  (injectable notifier into MachineGateway)
  notifyRunSuccess / notifyRunFailure
  failureMessage: de-alarmed, names sleep as likely cause
  deferredMessage: one per offline deferred exec run (dedup via DEFERRED_LABEL stamp)

gateway/circuitBreaker (via notifyRunFailure)
  streak >= LOOPANY_FAILURE_AUTOPAUSE_STREAK → enabled=false + unschedule + ONE note

webhookGuard.ts
  scheme/SSRF validation before outbound delivery
```

Channel routes: `createChannel`, `listChannels`, `testChannel`, `deleteChannel` (session-authed, team-scoped). `notify: "never"` silences every push.

## Data Models

- `channels` table: per-team rows carrying `kind` + an encrypted/webhook credential; list payloads never include the token.
- `loops.notify`: enum (`default`/`never`) consumed at dispatch time.
- Streak: derived from `runs` rows (phase `error` only; `skipped` is transparent to the streak).

## API Contracts

### Channel CRUD (session-authed, team-scoped)

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/teams/<teamId>/channels` | `createChannel` with live `testChannel` ping |
| GET | `/api/teams/<teamId>/channels` | `listChannels` (no tokens) |
| POST | `/api/teams/<teamId>/channels/test` | `testChannel` |
| DELETE | `/api/teams/<teamId>/channels/<id>` | `deleteChannel` |

### Webhook guard

Rejects before any outbound request: non-http(s) schemes and private/internal targets (loopback, link-local, metadata, private ranges).

## Sequences

### Failure with autopause

```
report() !ok (exec run)
  streak = count consecutive phase=error rows
  if notify:"never" → stop
  notify at streak 1, then every 5th (persisted rows, deploy-safe)
  if streak >= LOOPANY_FAILURE_AUTOPAUSE_STREAK (default 10, 0=off)
    → store.updateLoop enabled=false + unschedule
    → ONE autopause note that SUBSUMES the failure alert
    → silent under notify:"never"; plain pause, re-enable resumes
```

### Deferred offline run

```
pending exec run on an unreachable machine
  sweep holds it; alarm policy mirrors presence
  asleep (<6h) → fully silent
  genuinely offline → ONE calm deferredMessage per run
  dedup = DEFERRED_LABEL progress stamp (doubles as the UI "waiting" hint)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Shared form | `ChannelAddForm` extracted from `NotificationsModal` | Two binding surfaces can't drift |
| Persisted streak | Derived from run rows, not notifier state | Exact, deploy-safe |
| Autopause | `enabled=false` + unschedule + one subsuming note | Circuit breaker without spam; a plain pause, re-enable resumes |
| SSRF containment | `webhookGuard` before outbound delivery | Webhooks are attacker-adjacent credentials |
| Injectable notifier | Inject into MachineGateway | Tests observe pushes without network |
| De-alarmed copy | Names sleep as likely cause | Distinguishes an interrupted run from a skipped scheduled one |

## Risks and Unknowns

1. `skipped` runs must stay transparent to the streak (excluded, quiet gray in the UI) — the count keys off phase `error` only.
2. The autopause threshold is env-tunable (`LOOPANY_FAILURE_AUTOPAUSE_STREAK`), `0 = off`.
3. Deferred dedup relies on the DEFERRED_LABEL progress stamp; an asleep machine is fully silent.

## Out of Scope

- Inbound replies or webhook callbacks from channels.
- The onboarding live step's binding surface (onboarding feature owns the wizard; the form itself is shared here).
