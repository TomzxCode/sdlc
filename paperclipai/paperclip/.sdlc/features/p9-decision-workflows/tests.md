---
title: "Decision Workflows"
status: done
---

# Test Plan: Decision Workflows

## Scope

Tests cover decision validation, signing, idempotency, effect execution, staleness, expiry, continuations, queues, triage, retention, decision models, fast responses, training examples, receipt history, and the decision UI.
Out of scope are approval decisions tracked in FEAT-0005, release smoke coverage, and unrelated auth merge decision tests in adapter packages.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Decision validators accept all six effect variants and reject malformed or unknown effects | Effect objects for comment, create, status, assign, cancel tree, and blocker cases plus invalid variants | Valid effects parse and invalid effects throw (`packages/shared/src/decision.test.ts`) |
| TC-2 | Decision validators enforce option, input, and effect limits and duplicate ids | Overlong option and input collections plus duplicate ids and a cancel tree without destructive style | Validation throws for each invalid case (`packages/shared/src/decision.test.ts`) |
| TC-3 | Decision signing preserves signatures after key storage moves and never invents a missing legacy key | Signed spec with a key moved into environment storage and a missing legacy volume | Signature remains valid and missing key is not replaced (`server/src/services/decision-signing.test.ts`) |
| TC-4 | Decision provider contract keeps usage on refusals and validation failures | Charged refusal, invalid answer, OpenRouter refusal, missing usage, and subscription routing | Usage is retained, no answer is invented, and unsupported routing is rejected (`server/src/__tests__/decision-model-provider.test.ts`) |
| TC-5 | Fast response provider bounds context and retains charges on rejected output | Copied JSON output, long output, multibyte metadata, OpenRouter, Google, and Bedrock fixtures | Bounded prompt survives, long or copied output fails, and charges remain (`server/src/__tests__/fast-response-provider.test.ts`) |
| TC-6 | Fast response model choices respect routed connections and direct Anthropic configuration | Routed connection and direct Anthropic connection fixtures | Only configured or direct model ids are returned (`server/src/__tests__/fast-response-models.test.ts`) |
| TC-7 | Decision queue migrations preserve queue schema constraints | Current queue migration fixtures | Queue tables and constraints remain valid (`packages/db/src/decision-queue-migrations.test.ts`) |
| TC-8 | Decision receipt navigation preserves origin and exact document revision | Mixed document owner and external href payloads | Origin interaction stays and exact plan revision is used (`ui/src/lib/decision-receipt-navigation.test.ts`) |

Files: `packages/shared/src/decision.test.ts`, `server/src/services/decision-signing.test.ts`, `server/src/__tests__/decision-model-provider.test.ts`, `server/src/__tests__/fast-response-provider.test.ts`, `server/src/__tests__/fast-response-models.test.ts`, `packages/db/src/decision-queue-migrations.test.ts`, `ui/src/lib/decision-receipt-navigation.test.ts`.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Concurrent idempotent creates and double decides produce one winner | Embedded Postgres with an agent run and a decision | Existing decision is returned and the losing decide is rejected (`server/src/__tests__/decisions-service.test.ts`) |
| TC-10 | Effects execute once and stored outcomes replay with executor audit attributed to the decider | Decision with a chosen effect and a client idempotency key | One effect execution, replayed outcome, and activity attributed to the board user (`server/src/__tests__/decisions-service.test.ts`) |
| TC-11 | Bulk archive acceptance binds to the exact signed versioned manifest | Aging attention items with retention versions | Manifest hash and snapshots match and completion serializes (`server/src/__tests__/decisions-service.test.ts`) |
| TC-12 | Stale strict targets, secondary targets, intersection denial, and lost mutation authority fail closed | Signed strict and lenient decisions with changed target state | Strict effects are skipped, lenient authority is rechecked, and unsafe mutation is rejected (`server/src/__tests__/decisions-service.test.ts`) |
| TC-13 | Claimed effects and stale running decisions recover exactly once and continuations retry | Decided decision with a claimed execution and interrupted continuation | Effect settles once and continuation is delivered without replay (`server/src/__tests__/decisions-service.test.ts`, `server/src/__tests__/decision-effect-recovery-work.test.ts`) |
| TC-14 | Expiry happens at the saved deadline, respects batch size, and rolls back with activity failures | Open decisions with deadlines and target invalidations | Decisions expire atomically, workers stay bounded, and origin agents wake (`server/src/__tests__/decisions-service.test.ts`, `server/src/__tests__/decision-expiry-work.test.ts`) |
| TC-15 | Statistics group by rule key and separate dismissals from expiry | Decisions with accepted, dismissed, expired, and cancelled outcomes | Proposed, accepted, rejected, and expired counts and chosen options match (`server/src/__tests__/decisions-service.test.ts`) |
| TC-16 | Decision model settings, availability, manager-only test, and history enforce company isolation | Configured decision model and board actors | Settings, choices, fixed sample, and content-free history are returned (`server/src/__tests__/decision-models.test.ts`) |
| TC-17 | Decision model settlement records charges, budget holds, revocation, and concurrent admissions | Managed connection, grant, and budget policy fixtures | Charges and invocations settle once and revoked or denied work is blocked (`server/src/__tests__/decision-models.test.ts`) |
| TC-18 | Queues create idempotently, patch, list by update time, and audit mutations | Seeded company and board actor | One queue exists and all mutations are logged (`server/src/__tests__/decision-queues-routes.test.ts`) |
| TC-19 | Queue items cover three source kinds and starter queues materialize from plan, question, and PR signals | Attention sources with matching signals | Items are added once and board-only sources stay hidden from agents (`server/src/__tests__/decision-queues-routes.test.ts`) |
| TC-20 | Triage records agent decide-by values, preserves override history, and serializes partial updates | One triage row with a decide-by value and no snooze | Concurrent updates keep both fields and advance the version once (`server/src/__tests__/decision-queues-routes.test.ts`) |
| TC-21 | Retention auto-archives, exempts keep rows, revives sources, and rejects stale manifests | Retention rows with expected versions and archive notifications | Archive and revive settle correctly and a changed version fails the whole manifest (`server/src/__tests__/decision-retention-service.test.ts`) |
| TC-22 | Retention materialization cannot pre-archive unseen agent recovery or force new sources | Recovery, review, and blocker attention fixtures | Existing manual controls are preserved and unseen sources require ordinary materialization (`server/src/__tests__/decision-retention-materialization-security.test.ts`) |
| TC-23 | Training examples respect the cutoff, scrub deleted content, enforce author ownership, and export JSONL | Interaction with comments and runs around the decision cutoff | Snapshot excludes later content, updates require the author, and export contains state and labels (`server/src/__tests__/decision-training.test.ts`) |
| TC-24 | Decision history preserves receipt verdicts, pins document revisions, paginates, and isolates companies | Mixed review, document, approval, and task receipts | History entries keep recorded outcomes and exact links without leaking private tasks (`server/src/__tests__/decision-history.test.ts`) |
| TC-25 | Fast responses deduplicate turns, honor the experimental gate, suppress real replies, and respect budgets | Accepted chat turns with agent work, linked users, and reservations | Acknowledgement settles once or is skipped with no provider work when owned elsewhere (`server/src/__tests__/fast-responses.test.ts`) |
| TC-26 | Company and project decision owners save and clear through their routes | Board user with management access | Only the intended owner field changes and server rejection is surfaced (`server/src/__tests__/company-default-decision-owner-route.test.ts`, `server/src/__tests__/project-decision-owner-route.test.ts`) |
| TC-27 | Recorded decision idle and stalled review routes react to decision events | Issues with recorded decisions and stalled review state | Routes keep idle and stalled state consistent with decision outcomes (`server/src/__tests__/issue-recovery-recorded-decision-idle.test.ts`, `server/src/__tests__/issue-stalled-review-decision-routes.test.ts`) |
| TC-28 | Decision wakeup uses the heartbeat runtime only when enabled | Continuation request with enabled and disabled runtime fixtures | Wake is enqueued on enabled runtime and stays quiet otherwise (`server/src/__tests__/decision-wakeup.test.ts`) |
| TC-29 | Queue routes reject task-bridge JWTs and return the same not found for missing and unauthorized sources | Route harness with actor variants | Access failures are indistinguishable to callers (`server/src/__tests__/decision-queues-routes.test.ts`) |

Files: `server/src/__tests__/decisions-service.test.ts`, `server/src/__tests__/decision-models.test.ts`, `server/src/__tests__/decision-model-provider.test.ts`, `server/src/__tests__/decision-expiry-work.test.ts`, `server/src/__tests__/decision-target-work.test.ts`, `server/src/__tests__/decision-wakeup.test.ts`, `server/src/__tests__/decision-effect-recovery-work.test.ts`, `server/src/__tests__/decision-queues-routes.test.ts`, `server/src/__tests__/decision-retention-service.test.ts`, `server/src/__tests__/decision-retention-materialization-security.test.ts`, `server/src/__tests__/decision-training.test.ts`, `server/src/__tests__/decision-history.test.ts`, `server/src/__tests__/fast-responses.test.ts`, `server/src/__tests__/company-default-decision-owner-route.test.ts`, `server/src/__tests__/project-decision-owner-route.test.ts`, `server/src/__tests__/issue-recovery-recorded-decision-idle.test.ts`, `server/src/__tests__/issue-stalled-review-decision-routes.test.ts`.

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-30 | DecisionCard renders provenance, target links, effects, stale warnings, and terminal states | Render pending, decided, expired, dismissed, and partial decisions | Links, warnings, and result rows match the signed decision (`ui/src/components/DecisionCard.test.tsx`) |
| TC-31 | DecisionCard requires typed confirmation for cancel tree options | Select a destructive cancel tree option | Submit stays disabled until the typed confirmation matches (`ui/src/components/DecisionCard.test.tsx`) |
| TC-32 | DecisionResolver loads all targets and refreshes resolved status | Mount compact and full views with changed issue query | Cancel previews derive from signed scope and stale cache is replaced (`ui/src/components/DecisionResolver.test.tsx`) |
| TC-33 | TaskDecisionRecord opens the full named record and hides cached text after access loss | Open compact receipt, change viewer, and invalidate decisions | Full record shows recorded inputs and results and cached text is removed (`ui/src/components/TaskDecisionRecord.test.tsx`) |
| TC-34 | Company settings Decisions section labels owner selects and saves only the changed owner | Render settings and change or clear the owner field | Accessible labels are present and the request carries only the intended field (`ui/src/pages/CompanySettingsDecisions.test.tsx`) |
| TC-35 | ProjectProperties decision owner lists members and saves a new owner | Open the owner field and select a member or company default | Saved owner round-trips through the field update (`ui/src/components/ProjectProperties.decision-owner.test.tsx`) |
| TC-36 | DecisionModelSettings handles added connections, refetch changes, and load failures | Add a connection, change config elsewhere, fail and retry a refetch | Drafts and test feedback clear or persist as specified and errors show retry copy (`ui/src/components/decision-models/DecisionModelSettings.test.tsx`) |
| TC-37 | DecisionHistory renders setup links for model history | Mount history with invocation fixtures | Setup links are present (`ui/src/components/decision-models/DecisionHistory.test.tsx`) |
| TC-38 | FastResponseSettings saves API settings and keeps drafts across unchanged refetches | Save settings, refetch, and create a new connection | Saved settings persist and the recommended model is selected (`ui/src/components/fast-responses/FastResponseSettings.test.tsx`) |
| TC-39 | Runner story decisions match the user story before a click | Apply decisions to tool and connection interaction fixtures | Matching decision is accepted and mismatched story decisions throw (`tests/runner-e2e/everyday-decisions.test.ts`) |

Files: `ui/src/components/DecisionCard.test.tsx`, `ui/src/components/DecisionResolver.test.tsx`, `ui/src/components/TaskDecisionRecord.test.tsx`, `ui/src/components/ProjectProperties.decision-owner.test.tsx`, `ui/src/pages/CompanySettingsDecisions.test.tsx`, `ui/src/components/decision-models/DecisionModelSettings.test.tsx`, `ui/src/components/decision-models/DecisionHistory.test.tsx`, `ui/src/components/fast-responses/FastResponseSettings.test.tsx`, `tests/runner-e2e/everyday-decisions.test.ts`.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-40 | Signed spec is tampered with before a direct dismissal | Dismissal is refused with a signature error (`server/src/__tests__/decisions-service.test.ts`) |
| TC-41 | Signing secret is removed after a decision is proposed | Decision fails closed and no replacement key is invented (`server/src/__tests__/decisions-service.test.ts`, `server/src/services/decision-signing.test.ts`) |
| TC-42 | Decision deadline passes before effect execution | Decision expires instead of executing after the deadline (`server/src/__tests__/decisions-service.test.ts`) |
| TC-43 | Issue graph contains cycles during snapshot or cancel tree work | Traversal is bounded (`server/src/__tests__/decisions-service.test.ts`) |
| TC-44 | Lenient cancel tree targets change after proposal | Cancellation does not expand beyond the signed descendant scope (`server/src/__tests__/decisions-service.test.ts`) |
| TC-45 | Two actors create the same queue key concurrently | One queue row exists and both callers receive it (`server/src/__tests__/decision-queues-routes.test.ts`) |
| TC-46 | One expected retention version changes in a reviewed manifest | The whole archive action fails and no row is archived (`server/src/__tests__/decision-retention-service.test.ts`) |
| TC-47 | An agent attempts training writes or exports | The route refuses with a human user error (`server/src/__tests__/decision-training.test.ts`) |
| TC-48 | Training example id is malformed | Route returns not found (`server/src/__tests__/decision-training.test.ts`) |
| TC-49 | Fast response backlog expires before dispatch | Request expires with no inference attempt (`server/src/__tests__/fast-responses.test.ts`) |
| TC-50 | Provider work is interrupted with an unknown charge | Charge stays reserved and no regenerated attempt is billed (`server/src/__tests__/fast-responses.test.ts`) |
| TC-51 | Provider emits long or copied acknowledgement output | Output is rejected while the provider charge is retained (`server/src/__tests__/fast-response-provider.test.ts`) |
| TC-52 | Session replay captures decision UI | Agent option labels, recorded inputs, and receipt text are excluded (`ui/src/components/DecisionCard.test.tsx`, `ui/src/components/TaskDecisionRecord.test.tsx`, `ui/src/components/DecisionResolver.test.tsx`) |

## Test Infrastructure

- Embedded Postgres test databases supply real transactions, advisory locks, and constraint checks.
- Supertest route harnesses supply actor variants and mock provider or budget seams.
- Provider tests use mocked SDK calls with usage receipts and routing fixtures.
- UI tests use jsdom with mocked API hooks, router, query client, and company contexts.
- Runner story fixtures supply interaction payloads for matching decisions.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-9, TC-15, TC-30 |
| FR-2 | TC-3, TC-12, TC-40, TC-41 |
| FR-3 | TC-10, TC-12, TC-13, TC-30, TC-32 |
| FR-4 | TC-9, TC-10 |
| FR-5 | TC-14, TC-28, TC-42 |
| FR-6 | TC-14, TC-15 |
| FR-7 | TC-11, TC-46 |
| FR-8 | TC-15 |
| FR-9 | TC-18, TC-19, TC-29 |
| FR-10 | TC-19 |
| FR-11 | TC-20 |
| FR-12 | TC-21, TC-22, TC-46 |
| FR-13 | TC-4, TC-16, TC-17, TC-36 |
| FR-14 | TC-5, TC-6, TC-25, TC-38 |
| FR-15 | TC-25, TC-38, TC-49, TC-50, TC-51 |
| FR-16 | TC-23, TC-47, TC-48 |
| FR-17 | TC-30, TC-31, TC-32, TC-34, TC-52 |
| NFR-1 | TC-16, TC-18, TC-22, TC-29, TC-47 |
| NFR-2 | TC-2, TC-3, TC-12, TC-20, TC-21, TC-45 |
| NFR-3 | TC-2, TC-5, TC-12, TC-14, TC-25, TC-43 |
| NFR-4 | TC-16, TC-17, TC-23, TC-24 |
| NFR-5 | TC-13, TC-14, TC-21, TC-25, TC-28, TC-50 |
