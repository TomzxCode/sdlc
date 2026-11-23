---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-11-16

### TC-16 cites a dreaming test file that does not exist

- Status: BLOCKING
- Evidence:
  - TC-16 in the Integration Tests table names `extensions/memory-core/src/dreaming.test.ts` as the test for dreaming service reconciliation.
  - That file does not exist in the repository at code_ref `0eae4c0423cdf46fc94059ce1435ec96a0c37d15`, and no file by that name exists anywhere in git history.
  - No current test covers the four cases described in TC-16: the managed dreaming job created for the system agent and reconciled without an ambient owner, a replaced service updating the job and stopping the old reconciliation timer, scheduler maintenance staying out of user, heartbeat, and cron reply hooks, and managed dreaming firing only while the queued cron event is still pending.
  - The related suites now in the tree cover different behavior: `extensions/memory-core/src/dreaming-startup-lifecycle.test.ts` covers generation ordering and cleanup admission, `extensions/memory-core/src/dreaming-startup-cleanup.test.ts` covers stale phase reclamation after a gateway restart, `extensions/memory-core/src/dreaming.system-event-ownership.test.ts` covers the managed dreaming token on heartbeat and cron triggers, and `extensions/memory-core/src/dreaming-phases.test.ts` covers phase behavior.
- Artifact currently says: the dreaming service reconciliation cases are tested in `extensions/memory-core/src/dreaming.test.ts`.
- What the code actually does: no such test file exists and the described reconciliation, timer replacement, and pending-event cases have no matching test.
- Needed change: restore or locate the intended test, then repoint TC-16 at the real file, or rewrite TC-16 to describe the cases the surviving dreaming suites actually cover.

### TC-19 cites an Active Memory end-to-end proof that does not exist

- Status: BLOCKING
- Evidence:
  - TC-19 in the End-to-End Tests table names `test/e2e/qa-lab/runtime/active-memory-trigger-stall.product-proof.e2e.test.ts` as the proof for the index generation lock stall.
  - That file does not exist in the repository and no file matching `active-memory-trigger-stall` exists anywhere in git history.
  - No source, test, or config file defines the `OPENCLAW_ACTIVE_MEMORY_TRIGGER_STALL_PROOF` gate that TC-19 and the Test Infrastructure section say controls the suite.
  - The runtime product-proof directory contains suites for codex, gateway, managed worktrees, and session transcript flows, but none for Active Memory recall.
  - Active Memory recall behavior is currently covered by unit tests such as `extensions/active-memory/trigger-recall.test.ts`, not by an end-to-end product proof.
- Artifact currently says: an opt-in end-to-end proof verifies that a stalled index generation lock does not block the turn.
- What the code actually does: neither the proof file nor its opt-in gate exists.
- Needed change: add the end-to-end proof, or remove TC-19 and the matching Test Infrastructure bullet and reclassify the covered behavior under the Active Memory unit tests.

### Coverage matrix rows point at the two missing cases

- Status: ADVISORY
- Evidence:
  - The Coverage Matrix maps FR-6 and FR-7 partly to TC-16, and FR-5, FR-11, and NFR-2 partly to TC-19.
  - Both TC-16 and TC-19 are missing, so those matrix cells currently reference nonexistent proof.
- Artifact currently says: the listed requirements are covered by TC-16 and TC-19.
- What the code actually does: those requirements have other coverage in the tree, but not through the two cited cases.
- Needed change: after resolving the two blocking items, re-point the affected matrix cells at the tests that actually provide the coverage.

## Sync drift: 2026-11-23

Re-verified against current `main` at `78d2f2e70`; the previous `code_ref` is absent from this checkout. The 2026-11-16 blocking findings still hold, and the rest of the plan still matches the tree. The verdict stays `changes-requested`.

### TC-16 still cites a nonexistent dreaming test file

- Status: BLOCKING
- Evidence:
  - `tests.md:53` names `extensions/memory-core/src/dreaming.test.ts` in the TC-16 cell.
  - No file named `dreaming.test.ts` exists in `extensions/memory-core/src/` at `78d2f2e70`. The directory holds `dreaming.ts` and the suites `dreaming-command.test.ts`, `dreaming-consolidation.test.ts`, `dreaming-dreams-file.test.ts`, `dreaming-phases.test.ts`, `dreaming-repair.test.ts`, `dreaming-shared.test.ts`, `dreaming-snippet-dedupe.test.ts`, `dreaming-startup-cleanup.test.ts`, `dreaming-startup-lifecycle.test.ts`, `dreaming-state.test.ts`, `dreaming-sweep-narrative.test.ts`, and `dreaming.system-event-ownership.test.ts`.
  - The four TC-16 behaviors are spread across those suites rather than one file, for example `dreaming.system-event-ownership.test.ts:51` covers heartbeat and cron trigger ownership and `dreaming-phases.test.ts:146` marks owner turns with `senderIsOwner`.
- Artifact currently says: the reconciliation, timer replacement, reply-hook exclusion, and pending-event cases live in `extensions/memory-core/src/dreaming.test.ts`.
- What the code actually does: no such file exists at the current head.
- Needed change: repoint TC-16 at the suites that carry those cases or rewrite TC-16 to their actual coverage.

### TC-19 still cites a nonexistent end-to-end proof and gate

- Status: BLOCKING
- Evidence:
  - `tests.md:62` names `test/e2e/qa-lab/runtime/active-memory-trigger-stall.product-proof.e2e.test.ts` in the TC-19 cell.
  - `tests.md:62` and `tests.md:85` both name the `OPENCLAW_ACTIVE_MEMORY_TRIGGER_STALL_PROOF` gate.
  - Neither the proof path nor the gate string appears anywhere in the tree at `78d2f2e70`, confirmed by a repository-wide search for `active-memory-trigger-stall` and `OPENCLAW_ACTIVE_MEMORY_TRIGGER_STALL_PROOF`.
  - `extensions/active-memory/trigger-recall.test.ts` exists and exercises recall triggering, and the circuit breaker is configured in `extensions/active-memory/config.ts:236`; neither is the gated end-to-end product proof TC-19 describes.
- Artifact currently says: an opt-in end-to-end proof covers the stalled index generation lock.
- What the code actually does: no proof file and no gate exist at the current head.
- Needed change: add the proof and gate, or remove TC-19 and the matching Test Infrastructure bullet and reclassify the behavior under the Active Memory unit tests.

### All other cited test paths resolve

- Status: ADVISORY
- Evidence:
  - Every other cited file exists at `78d2f2e70`, including `src/memory/root-memory-files.test.ts`, `src/memory/memory-artifact-provenance.test.ts`, `src/memory-host-sdk/dreaming.test.ts`, the `packages/memory-host-sdk/src/host/` suites, `extensions/memory-core/src/cli.test.ts`, `extensions/memory-core/src/doctor-health.test.ts`, the four `src/gateway/server-methods/` memory suites, and `extensions/memory-core/src/session-search-visibility.cross-agent.test.ts`.
- Artifact currently says: those files back TC-1 through TC-15, TC-17, TC-18, and TC-20 through TC-29.
- What the code actually does: the cited paths are present.
- Needed change: none for these cases.
