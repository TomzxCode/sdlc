---
title: "Task System (Issues)"
status: done
session_link: "—"
---

# Test Plan: Task System (Issues)

## Scope

Issue lifecycle, atomic checkout, release/force-release, comments, documents, attachments, work products, labels, blockers, thread interactions, liveness, and execution policy are covered by route and service tests.
Out of scope: project/issue-level privacy ACLs.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Issue prefix/counter generation | Company context | Per-company human ids (`server/src/services/issue-prefix.test.ts`) |
| TC-2 | Issue liveness rule | Agent-owned non-terminal issues | Live/waiting/recovery path enforced (`server/src/__tests__/issue-liveness.test.ts`) |
| TC-3 | Execution policy evaluation | Issue + policy state | Correct policy verdicts (`server/src/__tests__/issue-execution-policy.test.ts`) |
| TC-4 | Thread interaction resolution | Interaction payloads | Correct resolution (`server/src/services/issue-thread-interactions.test.ts`, `server/src/services/issue-thread-interaction-resolution.test.ts`) |
| TC-5 | Dependency wakeups | Blocker graph changes | Dependents re-woken (`server/src/services/issue-dependency-wakeups.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Checkout wakeup flow | `todo` issue, claiming agent | Assignee + `in_progress` + locks set (`server/src/__tests__/issues-checkout-wakeup.test.ts`) |
| TC-7 | Auto-checkout via heartbeat | Heartbeat context on claimable issue | Exactly-once claim (`server/src/__tests__/heartbeat-auto-checkout.test.ts`) |
| TC-8 | Attachment routes (upload/serve/range) | File upload, video range request | Allowlist enforced, `206` ranges (`server/src/__tests__/issue-attachment-routes.test.ts`) |
| TC-9 | Comment routes and attribution | Agent/user comments | Persisted with audit (`server/src/__tests__/issue-comment-attribution-audit-routes.test.ts`, `server/src/__tests__/issue-queued-comments-routes.test.ts`) |
| TC-10 | Document restore routes | Document revisions | Restore works (`server/src/__tests__/issue-document-restore-routes.test.ts`) |
| TC-11 | Execution policy routes/persistence | Policy payloads | Persisted and enforced (`server/src/__tests__/issue-execution-policy-routes.test.ts`, `server/src/__tests__/issue-execution-policy-persistence.test.ts`) |
| TC-12 | Recovery actions and stale-lock sweep | Stuck/execution locks | Recovery + sweep (`server/src/__tests__/issue-recovery-actions.test.ts`, `server/src/__tests__/recovery-stale-issue-lock-sweep.test.ts`) |
| TC-13 | Blocker diagnostics and attention | Blocker relations | Diagnostics surfaced (`server/src/__tests__/issue-blocker-diagnostics-routes.test.ts`, `server/src/__tests__/issue-blocker-attention.test.ts`) |
| TC-14 | Thread interaction routes | Interaction payloads | Route behavior (`server/src/__tests__/issue-thread-interaction-routes.test.ts`) |
| TC-15 | Review policy and attention | `in_review` issues | Review gating (`server/src/__tests__/issue-review-policy.test.ts`, `server/src/__tests__/issue-review-attention.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-16 | Concurrent checkout race | Two concurrent checkouts on one `todo` issue | Exactly one succeeds, other gets `409` |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-17 | `in_progress` without assignee | Rejected `422` rule violation |
| TC-18 | Force-release by non-board actor | Rejected; board-only with audit entry |

## Test Infrastructure

- Vitest suite; run-dispatch and wake-queue module tests also exercise checkout paths.
- `doc/TASKS.md` and `doc/execution-semantics.md` document semantics.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-6 |
| FR-02 | TC-17 |
| FR-03 | TC-6, TC-7, TC-16 |
| FR-04 | TC-1 (related: goal fallback `server/src/__tests__/issue-goal-fallback.test.ts`) |
| FR-05 | TC-9 |
| FR-06 | TC-8 |
| FR-07 | TC-10 |
| FR-08 | TC-13, TC-14 (plus work-product/label coverage in related route tests) |
| FR-09 | TC-2, TC-12 |
| FR-10 | TC-3, TC-11 |
| NFR-01 | TC-16 |
| NFR-02 | Activity-log assertions in issue route tests |
