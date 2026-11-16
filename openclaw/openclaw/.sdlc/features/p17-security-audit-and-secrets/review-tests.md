---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### Four test-plan source paths no longer exist, though their behaviors are still covered

- Status: ADVISORY
- Evidence:
  - TC-31 names `src/audit/execution-owner-lifecycle-receipts.test.ts`. That file does not exist. The behavior lives in `src/audit/execution-identity-context.test.ts` under the describe block "owner-native execution lifecycle receipts" at line 440, including "uses admitted absence without catalog probes or allocating opt-in storage" at line 441, "keeps unbound cron storage opt-in on reopen" at line 474, and "keeps cron cursors stable and rejects mismatched or reused execution bindings" at line 500. The production owner `src/audit/execution-owner-lifecycle-receipts.ts` still exists.
  - TC-47, TC-48, TC-63, TC-64, and TC-65 name `src/pairing/pairing-store.test.ts`. That file does not exist. The behavior lives in `src/pairing/pairing-store.worker.test.ts`, which covers skipping malformed persisted requests (line 61), approving and dismissing account-scoped requests by opaque id (line 85), colliding codes and exhaustion without leaking codes (line 108), the prune and expired-request path (lines 228 and 329), and the `CHANNEL_PAIRING_PENDING_MAX` cap in `src/pairing/pairing-store-model.ts`.
  - TC-14 names `src/security/audit-gateway-auth-selection.test.ts`. That file does not exist. The behavior lives in `src/security/audit-gateway-exposure.test.ts` under the describe block "security audit gateway auth selection" at line 692, including "adds warning finding when probe auth SecretRef is unavailable" at line 693.
  - TC-11 names `src/security/audit-trust-model.test.ts`. That file does not exist. The behavior lives in `src/security/audit-gateway-exposure.test.ts` under the describe block "security audit trust model findings" at line 255, with related trust-model checks in `src/security/audit-cross-agent-session-access.test.ts` and `src/security/audit-exec-surface.test.ts`.
- Artifact currently says: the Unit Tests, Integration Tests, and Edge Cases tables attribute these cases to the four file paths above.
- What the code actually does: every referenced path has been renamed or folded into another suite. The behaviors are still tested, so coverage is intact, but four rows point readers at files that do not exist.
- Needed change: repoint TC-31, TC-47, TC-48, TC-63, TC-64, TC-65, TC-14, and TC-11 at the surviving test files listed above. No new tests are required.
