---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Missing requirements

- Plugin-contributed workflow traits and workflow extensions have no requirement. FR-3 lists only manifest, SDK, routes, tools, dashboard UI and runtime contributions. The code registers plugin traits into the workflow trait registry at `packages/engine/src/plugins/plugin-trait-adapter.ts:145` (`registerPluginTraits`) and `packages/engine/src/plugins/plugin-runner.ts:485` (`syncPluginTraits`), and registers plugin workflow extensions at `packages/engine/src/plugins/plugin-workflow-extension-adapter.ts:7` (`registerPluginWorkflowExtensions`) and `packages/engine/src/plugins/plugin-runner.ts:532` (`syncPluginWorkflowExtensions`). The registry lives at `packages/core/src/workflows/workflow-extension-registry.ts:36` and its move-policy extensions decide task transitions at `packages/core/src/task-store/project-store-ops.ts:570`. The extension kinds include column metadata, move policies, work engines, node handlers, task verdict providers and auto-merge fact providers, all listed in `packages/plugin-sdk/src/index.ts:88-116`.

- Plugin-contributed step parsers have no requirement. `packages/engine/src/plugins/plugin-parser-adapter.ts:123` (`registerPluginStepParsers`) registers each parser under a `plugin:<pluginId>:<parserId>` key with a five second budget (`packages/engine/src/plugins/plugin-parser-adapter.ts:36`), and `packages/engine/src/plugins/plugin-runner.ts:611` (`syncPluginStepParsers`) keeps them in sync with plugin state.

- The plugin gate verdict contract has no requirement. `packages/core/src/plugins/plugin-gate-verdict.ts:65` (`resolveColumnPluginGates`) finds plugin gate traits on a target column, the engine records the verdict before the move, and `packages/core/src/task-store/moves.ts:768-784` re-checks it inside the task lock and fails closed when a blocking gate has no recorded allow verdict. The recording and consumption helpers are at `packages/core/src/task-store/workflow-definitions.ts:489` and `packages/core/src/task-store/workflow-definitions.ts:506`.

- The opt-in AI security scan has no requirement. `packages/core/src/plugins/plugin-loader.ts:447-457` runs `scanPluginSecurity` before the plugin module is imported when `aiScanOnLoad` is set, and a `blocked`, `error` or `unavailable` verdict stops the load and puts the plugin in the `error` state. The scanner itself is `packages/core/src/plugins/plugin-security-scan.ts:19`. The CLI refuses to continue on the same verdicts at `packages/cli/src/commands/plugin.ts:668`. NFR-1 says nothing about scanning.

- Plugin setup hooks have no requirement. `packages/core/src/plugins/plugin-loader.ts:1278`, `:1305` and `:1333` implement the check, install and uninstall setup hooks, `packages/engine/src/plugins/plugin-runner.ts:752-778` exposes them, `packages/dashboard/src/routes/register-plugins-automation.ts:1386`, `:1431` and `:1459` serve `GET /plugins/:id/setup-status`, `POST /plugins/:id/setup/install` and `POST /plugins/:id/setup/uninstall`, and `packages/cli/src/bin.ts:2223-2239` registers `fn plugin setup-status` and `fn plugin setup`.

- Plugin activation analytics have no requirement. `packages/core/src/plugins/plugin-activation-analytics.ts:11` counts activation rows per plugin in a date range, `packages/core/src/postgres/schema/project.ts:2040` defines the `plugin_activations` table, and `packages/core/src/store.ts:2995` records each activation. The loader writes the row at `packages/core/src/plugins/plugin-loader.ts:350`.

- Plugin-owned PostgreSQL tables have no requirement. `packages/core/src/postgres/schema/plugin.ts:72`, `:93`, `:181`, `:240` and `:352` declare the roadmap, even-realities, compound-engineering, reports and cli-printing-press table name registries. The tables materialize through the plugin schema-init hook declared at `packages/core/src/plugins/plugin-types.ts:1174-1175`, and `packages/core/src/postgres/schema-applier.ts:835` refuses to apply a baseline whose project-owned tables lack the required isolation.

- Plugin prompt contributions have no requirement. `packages/core/src/plugins/plugin-prompt-condition.ts:1` defines the condition grammar, and `packages/engine/src/plugins/plugin-runner.ts:877` (`getPromptContributionsForSurface`) returns the contributions that apply to a given prompt surface.

- Plugin MCP server contributions have no requirement. `packages/core/src/plugin-mcp-servers.ts:33` (`createProjectScopedPluginMcpProvider`) is the only provider, and `packages/engine/src/plugins/plugin-runner.ts:422` (`getPluginMcpServers`) exposes the contributions. FR-7 and NFR-3 describe the isolation rule but not the contribution surface itself.

- Plugin workflow step contributions and step templates have no requirement. `packages/engine/src/plugins/plugin-runner.ts:429` and `:718` expose them, and `packages/core/src/task-store/project-store-ops.ts:862-873` resolves a `plugin:` step id back to the contributing plugin.

- Plugin CLI provider contributions have no requirement. `packages/engine/src/plugins/plugin-runner.ts:394` (`getCliProviderContributions`) collects them, and the type is exported at `packages/plugin-sdk/src/index.ts:73-78`.

- Bundled plugin auto-install and version refresh have no requirement. `packages/core/src/plugins/bundled-plugin-install.ts:32` lists the seventeen bundled plugin ids, and `packages/core/src/plugins/bundled-plugin-install.ts:106` (`ensureBundledPluginInstalled`) registers a missing bundled plugin, and `packages/core/src/plugins/bundled-plugin-install.ts:148` updates the stored path and version when the bundle changed. The CLI runs it at startup from `packages/cli/src/commands/dashboard.ts:1556`, `packages/cli/src/commands/serve.ts:701` and `packages/cli/src/commands/daemon.ts:609`.

- The curated plugin registry catalog has no requirement. `packages/dashboard/src/plugin-routes.ts:88` loads `packages/dashboard/src/registry-manifest.json`, `packages/dashboard/src/plugin-routes.ts:168` (`buildRegistryPluginEntries`) applies the search and category filters and annotates the installed state, and `packages/dashboard/src/plugin-routes.ts:357` serves `GET /plugins/registry`. The CLI has a separate builtin catalog at `packages/cli/src/commands/plugin.ts:29` served by `fn plugin available` at `packages/cli/src/commands/plugin.ts:585`.

- The plugin authoring CLI has no requirement. `fn plugin create` and `fn plugin new` scaffold a plugin at `packages/cli/src/commands/plugin-scaffold.ts:358` and `:407`, `fn plugin dev` runs a watch loop at `packages/cli/src/commands/plugin-dev.ts:89`, and `fn plugin publish` publishes one at `packages/cli/src/commands/plugin-publish.ts:231`. The subcommands are registered at `packages/cli/src/bin.ts:2241-2280`. FR-6 says only that the CLI exposes plugin management.

### Stale requirements

- NFR-3 says MCP discovery must be isolated per plugin. The code isolates per project root, not per plugin. `packages/core/src/plugin-mcp-servers.ts:36-47` keys the cache on the normalized project root and on the enabled plugin id and update timestamp, and `packages/core/src/plugin-mcp-servers.ts:64` and `:76` return the entries of every enabled plugin in that project together. The engine test at `packages/engine/src/__tests__/in-process-runtime-plugin-mcp-discovery-isolation.test.ts:34` asserts the project-level behavior. FR-7 words this correctly as isolation for in-process runtime plugins, so only NFR-3 is wrong.

- NFR-1 says plugins must not be force-installed without user action. The code registers and enables bundled plugins with no user action. `packages/core/src/plugins/bundled-plugin-install.ts:106-178` installs on startup, and `packages/core/src/async-stores/async-plugin-store.ts:283-289` writes the per-project state with `enabled: true`. The requirement needs to say which plugins are exempt, or the startup path needs to change.

- FR-1 lists update as a plugin manager action. There is no user-facing update action. The dashboard offers reload at `packages/dashboard/src/routes/register-plugins-automation.ts:1285` and rescan at `packages/dashboard/src/routes/register-plugins-automation.ts:1350`, and `packages/cli/src/bin.ts:2171-2286` registers no update subcommand. `docs/plugin-management.md:222` states that update is done by reinstalling. The only version refresh is the silent bundled-plugin path at `packages/core/src/plugins/bundled-plugin-install.ts:148`.

- NFR-2 says plugin interop drift is checked at lint time. The check is a separate script and a separate CI step. `package.json:48` defines lint as `eslint .` and `package.json:30` defines the interop check as its own script, and `.github/workflows/pr-checks.yml:89-90` runs it as a named step inside the job named Lint. A local `pnpm lint` does not run it.

- Open question 1 is partly answered but the answer is inconsistent. The code now holds four plugin inventories. `packages/core/src/plugins/bundled-plugin-install.ts:32` lists seventeen bundled ids, `packages/dashboard/src/routes/plugin-bundled-runtimes.ts:39` lists a different set of sixteen, `packages/cli/src/commands/plugin.ts:29` lists seven builtins, and `packages/dashboard/src/registry-manifest.json` lists sixteen registry entries, three of which (`fusion-plugin-slack-bridge`, `fusion-plugin-github-insights`, `fusion-plugin-local-llm-runtime`) have no package under `plugins/`. The question should be replaced by the inventory the product actually ships.
