---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Architecture

- The Architecture block names `register-plugin-routes` as a route registrar. No such file exists. The plugin management router is `packages/dashboard/src/plugin-routes.ts`, exported as `createPluginRouter` at `packages/dashboard/src/plugin-routes.ts:333` and mounted at `/plugins` from `packages/dashboard/src/routes.ts:2071-2093`. The registrar that carries the plugin endpoints is `packages/dashboard/src/routes/register-plugins-automation.ts`, exported as `registerPluginsAutomationRoutes` and mounted from `packages/dashboard/src/routes.ts:1026`.

- The Architecture block names `plugin-skill-integration` as an engine module. No such module exists. `packages/engine/src/__tests__/plugin-skill-integration.test.ts` is a test file. The skill body delivery code lives in `packages/core/src/plugins/plugin-skill-paths.ts:36` (`resolvePluginSkillBodyPath`) and `packages/engine/src/cli-runtime/session-skill-context.ts:165-169`.

### API contracts

- The `GET /api/plugins` response shape is wrong. The spec says the response body holds a `plugins` array. The code returns a bare array. `packages/dashboard/src/routes/register-plugins-automation.ts:857-868` calls `pluginStore.listPlugins(filter)` and sends the result directly, and `packages/dashboard/src/plugin-routes.ts:348-351` does the same. The `{ plugins: [...] }` envelope appears only on `GET /plugins/registry` at `packages/dashboard/src/plugin-routes.ts:368`.

- The `POST /api/plugins/:id/enable` error contract is wrong. The spec says an unknown plugin returns 404. The code returns 500. `packages/dashboard/src/routes/register-plugins-automation.ts:1216-1254` and `packages/dashboard/src/plugin-routes.ts:453-488` both call `pluginStore.enablePlugin(id)` with no try and catch, and `packages/core/src/async-stores/async-plugin-store.ts:328` throws a plain Error with `code: "ENOENT"`. `packages/dashboard/src/api-error.ts:154-156` turns any plain Error into a 500. The sibling `GET /plugins/:id` route does map ENOENT to 404 at `packages/dashboard/src/plugin-routes.ts:381-384`, so the enable route is the odd one out.

- The API contracts section omits `POST /api/plugins`. `packages/dashboard/src/routes/register-plugins-automation.ts:1031-1208` implements it with a `mode` discriminator of `register` or `install`, returns 201 on success, 400 on a validation failure and 409 on a duplicate registration, and accepts an `aiScanOnLoad` flag on install.

- The API contracts section omits the rest of the plugin surface. The code also serves `GET /plugins/registry` (`packages/dashboard/src/plugin-routes.ts:357`), `GET /plugins/ui-slots` (`packages/dashboard/src/routes/register-plugins-automation.ts:875`), `GET /plugins/ui-contributions` (`:901`), `GET /plugins/dashboard-views` (`:934`), `GET /plugins/runtimes` (`:946`), `GET /plugins/:id/settings` (`:999`), `PUT /plugins/:id/settings` (`:1486`), `PATCH /plugins/:id` (`:1324`), `POST /plugins/:id/reload` (`:1285`), `POST /plugins/:id/rescan` (`:1350`), `POST /plugins/:id/setup/install` (`:1431`), `POST /plugins/:id/setup/uninstall` (`:1459`) and `DELETE /plugins/:id` (`:1553`).

- The API contracts section omits the plugin-defined route surface. `packages/dashboard/src/plugin-routes.ts:857-869` mounts plugin-contributed routes under `/plugins/:pluginId/*` for the GET, POST, PUT, PATCH and DELETE methods.

### Data models

- The specification has no Data models section. The code persists plugin state in three places that the specification does not describe. `packages/core/src/postgres/schema/central.ts:202-217` defines the global `plugin_installs` table, `packages/core/src/postgres/schema/central.ts:219-232` defines the per-project `project_plugin_states` table, and `packages/core/src/postgres/schema/project.ts:2040-2051` defines the project-scoped `plugin_activations` table. `packages/core/src/postgres/schema/project.ts:1875-1893` also keeps a legacy project-scoped `plugins` table that `packages/core/src/postgres/schema/project.ts:1873` marks as compatibility only.

- The specification does not describe plugin-owned project tables. `packages/core/src/postgres/schema/plugin.ts:26-360` declares the tables and the per-plugin table name registries, and `packages/core/src/postgres/plugin-schema-hook.ts:5` explains that they materialize through a schema-init hook rather than the baseline migration.

### Sequences

- The Plugin run sequence omits the two gates that decide whether a plugin ever loads. The real order in `packages/core/src/plugins/plugin-loader.ts:441-531` is: optional security scan (`:447-457`), module import and manifest validation (`:461-470`), version compatibility check (`:474-484`), dependency resolution (`:486-487`), the schema contract and its DDL (`:489-496`), the `started` state (`:498-499`), then the `onLoad` hook (`:507-527`). A plugin that fails the scan or the schema contract never reaches `onLoad`, so the documented sequence is misleading.

### Technical decisions

- The Technical decisions table does not record the plugin-owned table contract, the trait and workflow extension registration, the gate verdict contract or the security scan. The code treats each as a load-bearing decision: `packages/core/src/postgres/schema-applier.ts:835` refuses a baseline whose plugin-owned tables lack isolation, `packages/engine/src/plugins/plugin-trait-adapter.ts:145` and `packages/engine/src/plugins/plugin-workflow-extension-adapter.ts:7` own the registration, `packages/core/src/task-store/moves.ts:768-784` owns the in-lock gate check, and `packages/core/src/plugins/plugin-loader.ts:447-457` owns the scan gate.

### Risks and unknowns

- Risk 1 still asks to confirm the canonical plugin inventory, and the code now holds four divergent inventories. `packages/core/src/plugins/bundled-plugin-install.ts:32` lists seventeen bundled ids, `packages/dashboard/src/routes/plugin-bundled-runtimes.ts:39` lists a different set of sixteen, `packages/cli/src/commands/plugin.ts:29` lists seven builtins, and `packages/dashboard/src/registry-manifest.json` lists sixteen registry entries whose three non-shipped ids are `fusion-plugin-slack-bridge`, `fusion-plugin-github-insights` and `fusion-plugin-local-llm-runtime`.
