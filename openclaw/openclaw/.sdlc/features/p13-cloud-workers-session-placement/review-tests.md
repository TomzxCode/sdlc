---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### The documented placement dispatch test file no longer exists

- Status: BLOCKING
- Evidence:
  - `tests.md` line 46, row TC-I-placement-dispatch, cites `src/gateway/worker-environments/placement-dispatch.test.ts`.
  - `tests.md` line 58, row TC-E-placement-flow, cites the same path together with `placement-dispatch-recovery.test.ts`.
  - `src/gateway/worker-environments/placement-dispatch.test.ts` does not exist in the repository.
  - The dispatch coverage was split into a family of suites in the same directory, including `placement-dispatch-coordinator.test.ts`, `placement-dispatch-continuity.test.ts`, `placement-dispatch-prepared.test.ts`, `placement-dispatch-staged-results.test.ts`, `placement-dispatch-shutdown.test.ts`, `placement-dispatch-reclaim.test.ts`, and `placement-dispatch-move-recovery.test.ts`.
  - `placement-dispatch-recovery.test.ts` still exists, so only the first path in TC-E-placement-flow is stale.
  - The replacement suites still cover the described behaviors. For example, `placement-dispatch-staged-results.test.ts` covers pending result recovery and conflict reporting, and `placement-dispatch-coordinator.test.ts` covers dispatch coalescing and queued moves.
- Artifact currently says: TC-I-placement-dispatch and TC-E-placement-flow point at `src/gateway/worker-environments/placement-dispatch.test.ts`.
- What the code actually does: dispatch, reclaim, continuity, staged result recovery, prepared dispatch, and shutdown coverage now live in separate `placement-dispatch-*.test.ts` files under `src/gateway/worker-environments/`, and the documented behaviors are still present across those suites.
- Needed change: repoint TC-I-placement-dispatch and TC-E-placement-flow at the surviving dispatch suites. The coverage matrix rows for FR-6, FR-11, FR-12, FR-13, and FR-14 reference TC-I-placement-dispatch by id and are fixed when that row is updated.

### Newer suites are not listed in the plan

- Status: ADVISORY
- Evidence:
  - The owned directories contain suites with no row in `tests.md`, including `device-placement-*.test.ts`, `desktop-*.test.ts`, `portal-node-carrier.test.ts`, `retained-owner-recovery.test.ts`, `prepared-pool-*.test.ts`, and many `local-workspace-*.test.ts` files.
  - The Scope section says every listed test file was confirmed to exist, which is still true, but the plan does not describe the expanded device placement, desktop, and retained-owner coverage.
- Artifact currently says: the plan documents a curated set of test files across the unit, integration, and end-to-end sections.
- What the code actually does: the subsystem has grown and now includes dedicated device placement, desktop and tunnel, portal carrier, and retained-owner suites beyond the documented set.
- Needed change: add rows for the new suites, or state that the plan is a curated subset rather than a complete inventory.
