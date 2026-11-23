---
title: "Onboarding"
status: done
---

# Test Plan: Onboarding

## Scope

This plan records tests that already cover the implemented onboarding wizard, Cloud seed receiver, onboarding chat, greeting delivery, first-task compatibility path, and adjacent setup entry points.
The primary scope is the server, UI, browser, canary, and runner-e2e suites.
CLI bootstrap and smoke scripts are listed as adjacent setup coverage and are not normative for the first-run product wizard.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Cloud seed route and service coverage in `server/src/__tests__/onboarding-seed-route.test.ts` (16 cases) | Seed payloads, actors, retries, failures | Idempotent application, mission split, bounded fields, audit once, access denial, retry after content transaction failure |
| TC-2 | Onboarding chat route coverage in `server/src/__tests__/onboarding-chat-route.test.ts` (5 cases) | Chat and greeting requests | One owner-bound chat, no task number, signup context, one greeting run, suggestion stays as context until acceptance |
| TC-3 | Greeting rendering coverage in `server/src/services/onboarding-greeting.test.ts` (3 cases) | Agent names including blank and whitespace | Agent name is used or dropped without leaving a gap |
| TC-4 | First-task asset coverage in `server/src/services/onboarding-first-task-assets.test.ts` (11 cases) | Templates, placeholders, proposal modes, child handoff recipes | Filled greeting, two-option card, valid brief modes, native child handoff rules, AGENTS.md bundle |
| TC-5 | First-task admission coverage in `server/src/__tests__/onboarding-first-task-admission.test.ts` (19 cases) | Agent runs, proposals, decisions, blockers, plan revisions | Native child creation requires trusted human acceptance and valid blockers |
| TC-6 | Issue first-task route coverage in `server/src/__tests__/issue-onboarding-first-task-routes.test.ts` (9 cases) | First-task create requests and concurrent creates | Origin stamped once, greeting and opening card seeded, skill brief server owned, no assignment wake |
| TC-7 | Approval producer and consumer contract in `server/src/__tests__/onboarding-approval-history.test.ts` | Table-driven native, REST issue, REST child, and decomposition paths under `skipIf` | Persisted approval survives the supported paths |
| TC-8 | Invitation onboarding text coverage in `server/src/__tests__/invite-onboarding-text.test.ts` (4 cases) | Invite text with host and inviter variants | Plain-text doc includes endpoints, diagnostics, inviter message, and LAN candidates |
| TC-9 | Dot OAuth onboarding coverage in `server/src/__tests__/dot-oauth-onboarding.test.ts` (7 cases) | Pairing, token refresh, browser origin, capability requests | Setup invalidation, safe refresh, pinned ingress, no public personal endpoint |
| TC-10 | Wizard core coverage in `ui/src/components/OnboardingWizard.test.tsx` (97 cases) | Drafts, adapters, providers, model choices, double submits, environment results | One company and one hire, duplicate adoption, blocked hires, Back behavior, restored configuration |
| TC-11 | Wizard step and launcher coverage in `ui/src/components/OnboardingWizard.step.test.tsx` (13 cases) and `ui/src/App.onboarding-launcher.test.tsx` (3 cases) | Cloud and self-hosted companies, routes, goals, reopened dialogs | Correct entry step, stable open wizard, route takeover, company withdrawal |
| TC-12 | Adapter recovery coverage in `ui/src/components/OnboardingWizard.adapters.test.tsx` (5 cases) | Disabled defaults, saved Codex and Paperclip Runner drafts, pending registry | Saved drafts normalized without losing model or runner choices |
| TC-13 | Wizard variant coverage in `ui/src/components/OnboardingWizardVariant.test.tsx` (3 cases) | Task open, dialog request, route dismissal | Wizard dependency tree stays unmounted until requested and route state resets safely |
| TC-14 | Onboarding library coverage in `ui/src/lib/onboarding-route.test.ts` (30 cases), `onboarding-state.test.ts` (5 cases), `onboarding-chat.test.ts` (2 cases), `onboarding-launch.test.ts` (2 cases), `onboarding-auto-open.test.ts` (7 cases), `onboarding-motion-tokens.test.ts` (2 cases), `onboarding-connection-test.test.ts` (2 cases), and `onboarding-agent-role.test.ts` (6 cases) | Routes, saved drafts, visibility, goals, offers, reduced motion, timeouts, role labels | Owned drafts only, one offer per company, visible paint gate, bounded checks, correct default goal and role naming |
| TC-15 | Analytics coverage in `ui/src/lib/analytics/onboarding-analytics.test.tsx` (11 cases) | Consent changes, user changes, step transitions, dismissal and reopen | Consent-gated capture, held events with original time, one event per transition, new session on reopen |
| TC-16 | Visual primitive coverage in `ui/src/components/onboarding/Stepper.test.ts` (7 cases), `onboarding-character.test.ts` (6 cases), and `OnboardingCharacter.test.tsx` (4 cases) | Wizard steps, character sequences, canvas failures | Arc numbering stays within three segments and failed canvas work releases resources |
| TC-17 | Chat page coverage in `ui/src/pages/AgentChat.test.tsx` (6 cases) and `ui/src/pages/BoardChat.test.tsx` (6 cases) | Disabled Agent Chat, stale navigation, other accounts, hidden tabs, wizard overlay, existing comments | Greeting waits for paint and visibility, errors are retryable, staged reveal and typing hold behave correctly |
| TC-18 | Storybook draft fixture coverage in `ui/storybook/fixtures/onboardingDraft.test.ts` (6 cases) | Owned and malformed draft values | Fixtures stay within the wizard arc and clear without residue |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-19 | Browser onboarding coverage in `tests/e2e/onboarding.spec.ts` (7 cases) | Running app with mocked login and environment signals | Naming creates no goal, login resumes, failed probes block hire, saved advanced adapter survives setup |
| TC-20 | Canary coverage in `tests/canary-onboarding/canary-onboarding.spec.ts` (1 case) | Published canary package | Exact published canary installs and reaches Connect a model |
| TC-21 | Release smoke coverage in `tests/release-smoke/docker-auth-onboarding.spec.ts` (2 cases) | Authenticated Docker deployment | Login and onboarding complete and hire the lead agent |
| TC-22 | Runner product journey coverage in `tests/runner-e2e/product-journeys/onboarding-first-task.test.ts` (20 cases), `onboarding-pre-acceptance.test.ts` (2 cases), `onboarding-connect.test.ts` (10 cases), and `cloud-onboarding.test.ts` (5 cases) | Runner harness with guarded product journeys | Pre-acceptance authority, plan revision checks, capability caps, connect deadlines, and accepted task readback are verified |
| TC-23 | CLI onboarding coverage in `cli/src/__tests__/onboard.test.ts` (9 cases) and `onboard-service.test.ts` (20 cases) | Temporary config homes and flag combinations | Existing config preserved, invalid bytes backed up, service installer follows opt-in and safety checks |
| TC-24 | Smoke script coverage in `scripts/docker-onboard-smoke.test.mjs` (8 cases) and `scripts/service-onboard-smoke.test.mjs` (4 cases) | Smoke harness and workflow files | Container names, cleanup logs, and release workflow routing stay intact |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-19 | Browser wizard walk | Open onboarding, name organization, connect provider, handle login, connect agent, finish | Company and agent exist, chat opens, no goal is invented during naming |
| TC-20 | Canary install walk | Install exact published canary, open wizard, reach model step | Published artifact supports the onboarding entry point |
| TC-21 | Docker authenticated walk | Start authenticated Docker stack, log in, run wizard | Lead agent is hired through the release artifact |
| TC-22 | Runner guarded journeys | Drive native and REST first-task flows with adversarial snapshots | No execution work is admitted without trusted acceptance and valid evidence |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-1 | Seed revision replay | Response reports `changed: false` and no second agent, goal, task, or audit entry is created |
| TC-1 | Changed seed revision | Existing goal and agent are updated in place and the old first-task back-reference is preserved |
| TC-1 | Missing or out-of-bound seed field | Request fails validation before service writes |
| TC-1 | Seed content transaction failure | Seed row and audit entry roll back and Cloud can retry |
| TC-2 | Repeated or concurrent chat opens | One owner-bound conversation is returned |
| TC-2 | Agent Chat disabled or agent ambiguous | Request returns 404 and no conversation is created |
| TC-14 | Hidden tab or unmount during welcome delay | Greeting request waits for visibility or is cancelled |
| TC-17 | Failed greeting wake | Page shows a retry action and a later admission can succeed |
| TC-5 | Native child before persisted acceptance | Creation is rejected with `onboarding_first_task_acceptance_required` |
| TC-5 | Stale plan revision or agent-only approval | Execution is rejected because the human decision does not match the latest plan |
| TC-6 | Concurrent first-task create | Partial unique index allows one onboarding first task and the loser degrades to an ordinary issue |
| TC-10 | Duplicate agent name and harness | Existing agent is adopted instead of hiring a numbered duplicate |
| TC-12 | Disabled default adapter or incomplete registry load | Saved draft is normalized without losing the user's model or runner |
| TC-14 | Draft names a company the user does not own | Draft is discarded before any company scoped request uses it |
| TC-15 | Consent withdrawn while analytics is loading | Held events are dropped |

## Test Infrastructure

- Vitest suites in `server/src`, `ui/src`, `cli/src`, and `scripts` use project fixtures and mocked external adapters.
- Server route tests use the database test harness, `routeApp`, actor setup, and Cloud seed payload builders.
- UI tests mock API clients, adapter discovery, analytics consent, and browser storage.
- Browser and canary suites use Playwright with app or published artifact targets.
- Runner-e2e journeys use the runner harness with snapshots for native, REST, connect, and acceptance evidence.
- Greeting UI tests require a visible document and two painted frames before the greeting call.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-10, TC-11, TC-19 |
| FR-02 | TC-10, TC-11 |
| FR-03 | TC-10, TC-12, TC-22 |
| FR-04 | TC-10, TC-11, TC-21, TC-22 |
| FR-05 | TC-2, TC-10, TC-19, TC-21 |
| FR-06 | TC-1 |
| FR-07 | TC-1 |
| FR-08 | TC-1 |
| FR-09 | TC-1 |
| FR-10 | TC-1, TC-2 |
| FR-11 | TC-1 |
| FR-12 | TC-2, TC-17 |
| FR-13 | TC-2, TC-14, TC-17, TC-19 |
| FR-14 | TC-2, TC-17 |
| FR-15 | TC-2, TC-5, TC-6, TC-22 |
| FR-16 | TC-4, TC-6, TC-7, TC-22 |
| FR-17 | TC-5, TC-7, TC-22 |
| FR-18 | TC-11, TC-14 |
| FR-19 | TC-15 |
| NFR-01 | TC-1, TC-2, TC-17 |
| NFR-02 | TC-1 |
| NFR-03 | TC-1, TC-2, TC-6 |
| NFR-04 | TC-2, TC-19, TC-22 |
| NFR-05 | TC-1, TC-2 |
| NFR-06 | TC-10, TC-14, TC-17 |
