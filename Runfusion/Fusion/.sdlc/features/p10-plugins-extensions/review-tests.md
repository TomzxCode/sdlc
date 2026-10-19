---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Key test files

- The Key test files section names `packages/dashboard/app/__tests__/api-plugins`, which does not exist. The plugin API test is `packages/dashboard/app/api/__tests__/plugin-setup-api.test.ts`.

- The Key test files section names `packages/dashboard/src/routes/__tests__/register-approval-routes...` as a plugin route test. `packages/dashboard/src/routes/__tests__/register-approval-routes.test.ts` exists but covers approval routes, not plugins. The plugin route tests are `packages/dashboard/src/__tests__/plugin-routes.routes.test.ts` and `packages/dashboard/src/__tests__/plugin-routes-wiring.test.ts`, and there is no `packages/dashboard/src/routes/__tests__/register-plugins-automation.test.ts`.

### Test cases

- TC-6, TC-7 and TC-8 claim that a command is routed into the Claude CLI, the Droid CLI and Llama.cpp, but the named test files only assert extension path resolution and the settings toggle. `packages/cli/src/commands/__tests__/claude-cli-extension.test.ts:10-80`, `packages/cli/src/commands/__tests__/droid-cli-extension.test.ts:17-95` and `packages/cli/src/commands/__tests__/llama-cpp-extension.test.ts:7-40` cover `resolveClaudeCliExtension`, `resolveClaudeCliExtensionPaths`, `resolveDroidCliExtension`, `resolveDroidCliExtensionPaths`, `resolveLlamaCppExtension` and `resolveLlamaCppExtensionPaths` only. The routing behavior is tested in `packages/pi-claude-cli/src/__tests__/provider.test.ts` and `packages/droid-cli/src/__tests__/provider.test.ts`, which the plan never names. The Llama.cpp extension has no provider test of its own, only `packages/pi-llama-cpp/src/__tests__/index.test.ts` and `packages/pi-llama-cpp/src/__tests__/resolver.test.ts`.

### Coverage matrix

- The Coverage matrix maps no test case to FR-5, FR-6, FR-7, NFR-1 or NFR-3. The matrix at tests.md:44-50 lists only FR-1, FR-2, FR-3, FR-4 and NFR-2. FR-5 and NFR-2 are covered by the two drift checks, `scripts/check-plugin-interop-drift.mjs` and `scripts/check-pi-versions-pinned.mjs`, and NFR-2 has that one entry, but the other four requirements have no mapped case.

### Missing test areas

- The plugin SDK package has no test area. `packages/plugin-sdk/src/__tests__/index.test.ts` and `packages/plugin-sdk/src/__tests__/re-export-contract.test.ts` exist, and `packages/cli/src/__tests__/plugin-sdk-export.test.ts` and `packages/cli/src/__tests__/plugin-sdk-core-runtime-shim.test.ts` guard the published shape. FR-3 covers the SDK and the plan names no SDK test.

- The plugin authoring CLI has no test area. `packages/cli/src/__tests__/plugin-scaffold.test.ts`, `packages/cli/src/__tests__/plugin-scaffold-caret-fallback.test.ts`, `packages/cli/src/__tests__/plugin-dev.test.ts`, `packages/cli/src/__tests__/plugin-publish.test.ts` and `packages/cli/src/__tests__/plugin-pack-shape.test.ts` exist for `fn plugin create`, `fn plugin new`, `fn plugin dev` and `fn plugin publish`.

- The plugin permission and data surfaces have no test area. `packages/core/src/__tests__/plugin-task-store-gate.test.ts` covers the destructive TaskStore gate, `packages/core/src/__tests__/postgres/plugin-schema-hook.test.ts` covers the plugin schema-init hook, `packages/core/src/__tests__/plugin-hot-reload.test.ts` covers reload, `packages/core/src/__tests__/plugin-loader-lifecycle-scope.test.ts` covers the shared process lifecycle, and `packages/core/src/plugins/__tests__/bundled-plugin-install.test.ts` covers the bundled install and version refresh.

- The plugin extension surfaces have no test area. `packages/engine/src/__tests__/workflow-node-handler-extensions.test.ts` and `packages/engine/src/__tests__/workflow-verdict-provider-extensions.test.ts` cover the plugin-contributed node handlers and verdict providers, and `packages/core/src/__tests__/workflow-extension-registry.test.ts` covers the registry. The plan names no extension test, and FR-3 and FR-2 are the only requirements that touch this area.

- The dashboard plugin UI has no test area. `packages/dashboard/app/components/__tests__/PluginManager.test.tsx`, `PluginManager.toggle.test.tsx`, `PluginManager.install-browse.test.tsx`, `PluginManager.registry.test.tsx`, `PluginSlot.test.tsx`, `pluginNavIcon.test.ts` and `PiExtensionsManager.test.tsx` exist, and so do `packages/dashboard/app/plugins/__tests__/pluginViewRegistry.test.tsx`, `packages/dashboard/app/plugins/__tests__/registerBundledPluginViews.test.tsx`, `packages/dashboard/app/hooks/__tests__/usePluginUiSlots.test.ts`, `packages/dashboard/app/hooks/__tests__/usePluginUiContributions.test.ts` and `packages/dashboard/app/hooks/__tests__/usePluginDashboardViews.test.ts`. FR-6 names the PluginManager and the PiExtensionsManager, and the plan names only `PluginManager.test`.

- The pi extension discovery surface has no test area. `packages/core/src/__tests__/pi-extensions.test.ts`, `packages/core/src/__tests__/pi-extensions-format.test.ts` and `packages/core/src/__tests__/pi-extensions-write-path-durability.test.ts` cover the discovery, the source formatting and the durable write path for `packages/core/src/plugins/pi-extensions.ts`. FR-4 names the pi extensions but the plan names no discovery test.

- TC-3 names only the engine isolation test, while the same contract has two more tests. `packages/core/src/__tests__/plugin-mcp-servers-discovery-isolation.test.ts:51-105` covers the core provider and `packages/dashboard/src/__tests__/context-plugin-mcp-discovery-isolation.test.ts` covers the dashboard context.
