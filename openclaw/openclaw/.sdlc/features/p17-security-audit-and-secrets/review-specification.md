---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-23
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-11-23

### Documented error code set does not match the gateway's closed error code set

- Status: ADVISORY
- Evidence:
  - `specification.md:287` documents `INVALID_AUDIT_FILTERS` as the code for an unsupported audit filter combination. The `audit.activity.list` handler returns `INVALID_REQUEST` for exactly that case at `src/gateway/server-methods/audit.ts:158-166`, with the detail message built at line 158 and passed to `errorShape(ErrorCodes.INVALID_REQUEST, ...)` at line 165.
  - The closed code set in `packages/gateway-protocol/src/gateway-error-codes.ts:6-17` has no `INVALID_AUDIT_FILTERS` member.
  - `specification.md:289` documents `INTERNAL` for Gateway failures. The same closed set has no `INTERNAL` member; transient service failures use `UNAVAILABLE`, for example `src/gateway/session-observer-rpc.ts:23`.
  - `api.yaml` is consistent with the code: its only documented example code is `INVALID_REQUEST` at `api.yaml:83`.
- Artifact currently says: the shared error table lists four codes, including `INVALID_AUDIT_FILTERS` and `INTERNAL`.
- What the code actually does: audit filter conflicts, bad ranges, and malformed cursors all return `INVALID_REQUEST`. The gateway emits a closed set that has neither `INVALID_AUDIT_FILTERS` nor `INTERNAL`.
- Needed change: in the next specification revision, describe filter conflicts as `INVALID_REQUEST` with a detail message, and replace `INTERNAL` with the actual failure code the Gateway can emit. No code change is required.
