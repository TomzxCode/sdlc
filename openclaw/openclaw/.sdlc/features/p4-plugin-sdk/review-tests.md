---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Plugin SDK and Extension System test plan

## Sync drift: 2026-10-19

### Blocking: `src/plugin-sdk/agent-core.test.ts` no longer exists

- Artifact says (tests.md:18): "| `src/plugin-sdk/agent-core.test.ts` | Agent core SDK exports |".
- Artifact relies on it for coverage (tests.md:47): "FR-1 (SDK types and interfaces) | `facade-runtime.test.ts`, `agent-core.test.ts`".
- Code: no `src/plugin-sdk/agent-core.test.ts` exists in the tree.
- Code: the module under test still exists as `src/plugin-sdk/agent-core.ts`, which now re-exports `runAgentLoop` from `packages/agent-core/src/index.js` (`src/plugin-sdk/agent-core.ts:28`).
- Code: the nearest remaining SDK-surface test is `src/plugin-sdk/core.test.ts`, and `src/plugin-sdk/provider-stream-shared.test.ts:1` is the only remaining file that imports `openclaw/plugin-sdk/agent-core`.
- Impact: FR-1's coverage points at a file that cannot be opened, so the matrix row is unresolvable.
- Classification: blocking.

### Blocking: the boundary-enforcement coverage row cites a file that does not exist at that path

- Artifact says (tests.md:52): "NFR-1 (Boundary enforcement) | `plugin-scope.test.ts`, `extension-import-boundaries.test.ts`".
- Code: no file named `extension-import-boundaries.test.ts` exists anywhere in the repo.
- Code: the real boundary suites are `test/plugin-extension-import-boundary.test.ts`, `test/test-helper-extension-import-boundary.test.ts`, and `test/scripts/extension-import-boundary-checker.test.ts`, all under the repo-level `test/` directory rather than next to the code they guard.
- Code: `src/plugins/loader-sdk-import-guardrails.test.ts:1-6` also guards SDK import usage inside the plugin loader fixtures.
- Impact: the NFR-1 row names a nonexistent suite and hides that boundary enforcement is covered by repo-level tests, not by a `src/` co-located file.
- Classification: blocking.

### Advisory: the import boundary check is an inventory report, not a failing test

- Artifact says (tests.md:31): "Plugin import from core internals | Import boundary check fails".
- Code: `scripts/check-plugin-extension-import-boundary.mts:1-2` describes itself as "Inventories core plugin imports that cross into bundled extension files", and it writes a report through `writeLine` from `scripts/lib/guard-inventory-utils.mjs`.
- Code: `src/plugins/loader-sdk-import-guardrails.test.ts:35-39` asserts that fixture imports stay off the SDK except for one allowlisted regression case.
- Impact: the scenario still holds for plugin-authored imports, but the enforcement mechanism is a report plus a narrower guardrail test, not a single boundary test.
- Classification: advisory.

### Advisory: notable test areas the artifact does not list

- Code: `src/plugin-sdk/api-baseline.test.ts` and `src/plugin-sdk/api-diff.ts` cover the public API baseline and drift detection that back `pnpm plugin-sdk:api:diff`.
- Code: `src/plugin-sdk/facade-loader.test.ts`, `src/plugin-sdk/facade-runtime.activation.test.ts`, `src/plugin-sdk/facade-runtime.cold.test.ts`, `src/plugin-sdk/facade-runtime.sync-failure.test.ts`, and `src/plugin-sdk/facade-activation-check.runtime.ts` cover facade loading and activation.
- Code: `src/plugin-sdk/channel-entry-contract.test.ts` and `src/plugin-sdk/channel-entry-contract.lifecycle.test.ts` cover the channel entry contract.
- Code: `src/plugin-sdk/provider-entry.test.ts` covers the provider entry contract.
- Code: `src/plugins/plugin-trust.ts` owns install provenance and trust, and `src/plugins/loader.trust-diagnostics.test.ts` and `src/plugins/loader.discovery-and-security.test-utils.ts` exercise it.
- Code: `src/plugins/install-managed-npm.ts` implements the managed npm install path, and `src/plugins/npm-package-traversal.test.ts` and `src/plugins/uninstall.test.ts` exercise it, while `src/plugins/git-install.test.ts` covers git installs.
- Code: `src/plugins/clawhub-archive-verification.ts` and `src/plugins/clawhub.registry-authority.test.ts` cover ClawHub install verification.
- Code: `src/plugins/manifest-registry.test.ts`, `src/plugins/manifest-registry-installed.test.ts`, and `src/plugins/bundled-manifest-contract-plugins.test.ts` cover manifest validation and the installed-plugin index.
- Code: `src/plugins/installed-plugin-index-store.test.ts` and `src/plugins/installed-plugin-index-store-write.test.ts` cover the SQLite-backed installed-plugin index.
- Code: `src/plugin-sdk/plugin-test-api.ts`, `src/plugin-sdk/plugin-test-runtime.ts`, and `src/plugin-sdk/plugin-test-contracts.ts` are the shipped plugin testing utilities behind FR-8, and they have no listed test file.
- Impact: the plan covers the original facade and registry surface but not the surface that now dominates the plugin system.
- Classification: advisory.
