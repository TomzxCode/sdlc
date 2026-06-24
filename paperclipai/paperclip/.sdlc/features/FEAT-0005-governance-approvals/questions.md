# Open Questions: Governance & Approvals

## Sync drift (2026-06-24)

The following items were identified during codebase reconciliation and reflect functionality present in the code but not documented in the current requirements.md or specification.md.

1. **Authorization engine** — A fine-grained authorization/access control system exists at `server/src/services/authorization.ts` (1360 lines) that gates actions (create/read/update/delete/approve/etc.) on resources (company/agent/issue/etc.) per actor type. The governance feature does not describe how authorization interacts with approvals and board override.

2. **Principal permission grants** — Schema `principal_permission_grants` and related infrastructure provide fine-grained permission overrides beyond role-based defaults. Not documented.

3. **Execution policy subsystem** — `server/src/services/execution-policy-bootstrap.ts`, `execution-allowlist.ts`, `issue-execution-policy.ts` implement execution policies with review/approval stages and decision tracking. The spec mentions these in passing but does not describe the implementation.

4. **Issue execution decisions** — Schema `issue_execution_decisions` tracks execution policy decisions at the issue level. Not documented.

5. **Low-trust presets** — `server/src/services/low-trust-runtime-containment.ts`, `trust-preset-resolver.ts`, and doc `doc/LOW-TRUST-PRESETS.md` provide containment controls for hostile automated work. Not documented as part of governance.

6. **Source trust** — `server/src/services/source-trust.ts` manages trust levels for external sources. Not documented.

7. **Approvals on issues** — `server/src/services/issue-approvals.ts` and schema `issue_approvals` provide issue-level approval linking. The governance feature spec describes approvals broadly but misses issue-level approval details.
