---
title: "Notifications & Channel Bindings"
status: done
---

# Requirements: Notifications & Channel Bindings

## Overview

Loopany notifies owners about run outcomes (and deferred runs) over external channels (Slack, Telegram, Feishu). Channels are created from a webhook/token via the shared `ChannelAddForm`, verified with a live `testChannel` ping, and consumed by `gateway/notify.ts`. Only exec runs produce user-facing notifications, success or failure, with anti-spam streak logic, an offline deferred message, and a failure circuit breaker that auto-pauses a loop after a streak.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop owner | Get notified on run success/failure without watching the dashboard; silenceable via `notify: "never"`. |
| Product | Alerting that is calm and non-spammy: streak-based copy, deferred-run dedup, autopause with one subsuming note. |
| Security | Channels are webhook-shaped credentials; the webhook guard must prevent open SSRF and keep tokens out of list payloads. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | Channels shall be created via one shared `ChannelAddForm` (slack/telegram/feishu) used by both the notifications modal and the onboarding live step, with a live `testChannel` ping before saving. |
| FR-2 | Must | Notifications shall fire on run success and failure, but ONLY for exec runs; evolve/edit runs produce no user-facing notifications. |
| FR-3 | Must | Failure notifications shall be anti-spam: derived from persisted run rows, notifying at streak 1 then every 5th; a success resets the streak. |
| FR-4 | Must | `notify: "never"` shall silence everything, including the autopause note. |
| FR-5 | Must | A deferred exec run on an offline machine shall get exactly ONE calm `deferredMessage`, deduped by the deferred progress stamp. |
| FR-6 | Must | The failure circuit breaker shall auto-pause a loop (unschedule + `enabled=false`) at the configured streak, with one autopause note that SUBSUMES the failure alert. |
| FR-7 | Should | Channel credentials shall be validated by a webhook guard before any outbound request (SSRF containment). |
| FR-8 | Should | The gateway shall take an injectable notifier so tests observe pushes without network. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Channel tokens must never appear in channel-list payloads or logs. |
| NFR-2 | Must | Security | The webhook guard must reject private/internal targets and non-http(s) schemes before outbound delivery. |
| NFR-3 | Should | Reliability | Failure pushes must be de-alarmed and name sleep as the likely cause, distinguishing an interrupted run from a skipped scheduled one. |

## Constraints

- `runs` rows are the single source for streak/outcome; notifiers must not carry their own persisted state.
- Notifications are outbound only; there is no inbound reply handling.
- `notify` enum lives on the loop record (`default`/`never`), consumed at dispatch time.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** a channel form open in either the modal or the wizard
    - **When** a channel is added
    - **Then** a live `testChannel` ping runs before save and both surfaces share the form
- [ ] **FR-2**
    - **Given** an evolve or edit run completing
    - **When** it reports
    - **Then** no user-facing notification is pushed
- [ ] **FR-3**
    - **Given** a series of exec failures
    - **When** the streak reaches 1 and then every 5th
    - **Then** notifications fire only at those points; a success resets the streak
- [ ] **FR-4**
    - **Given** a loop with `notify: "never"`
    - **When** any failure or autopause occurs
    - **Then** nothing is pushed
- [ ] **FR-5**
    - **Given** a genuinely offline machine with a deferred exec run
    - **When** the deferral is recorded
    - **Then** exactly one calm `deferredMessage` is sent, deduped by the progress stamp
- [ ] **FR-6**
    - **Given** the failure streak reaching the autopause threshold
    - **When** the loop pauses
    - **Then** `enabled=false` + unschedule and ONE autopause note subsuming the failure alert
- [ ] **NFR-1**
    - **Given** a channel list call
    - **When** the payload renders
    - **Then** no token is present
- [ ] **NFR-2**
    - **Given** a channel webhook pointing at a private/internal host
    - **When** delivery is attempted
    - **Then** the guard rejects it before any outbound request

## Conflicts

None identified yet.

## Open Questions

1. None: behavior is fully determined by the code and its tests.
