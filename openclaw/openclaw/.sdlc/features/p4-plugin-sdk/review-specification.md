---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Plugin SDK and Extension System specification

## Sync drift: 2026-10-19

### Blocking: the SDK is a set of narrow subpaths, not four barrel modules

- Artifact says (specification.md:10): "The plugin system uses a facade pattern: plugins import only from `@openclaw/plugin-sdk` barrels (e.g., `api.ts`, `runtime-api.ts`)."
- Artifact shows (specification.md:18-23) a facade with exactly four children: `api.ts`, `runtime-api.ts`, `channel-contract.ts`, `plugin-types.ts`.
- Code: `scripts/lib/plugin-sdk-entrypoints.json` lists 380 public subpaths, including `core`, `plugin-entry`, `provider-entry`, `channel-entry-contract`, `provider-auth`, `secret-input`, `agent-core`, `llm`, and `memory-host-core`.
- Code: `package.json:491-1160` publishes one `./plugin-sdk/<name>` export per subpath.
- Code: `src/plugin-sdk/AGENTS.md:24` states "New surface: small versioned host/kernel seam + narrow purpose-built documented subpath; no broad convenience barrels or re-exports."
- Code: `docs/plugins/sdk-overview/imports.md:15-23` states "Each subpath is a small, self-contained module. This keeps startup fast and prevents circular dependency issues."
- Code: `api.ts` and `runtime-api.ts` exist per plugin package under `extensions/<id>/`, not as SDK barrels, for example `extensions/telegram/runtime-api.ts:1-3`.
- Impact: the architecture diagram is the primary mental model a reader gets for the SDK, and it is now inverted: the SDK is narrow-subpath-first, and `api.ts`/`runtime-api.ts` are plugin-local barrels.
- Classification: blocking.

### Blocking: the PluginManifest data model no longer matches the code

- Artifact says (specification.md:36-43):

  | Field | Type | Constraints | Description |
  |---|---|---|---|
  | id | string | PK | Unique plugin identifier |
  | name | string | not null | Human-readable name |
  | version | string | not null | Semver version |
  | type | string | not null | channel, provider, tool, etc. |
  | entry | string | not null | Main entry point |
  | configSchema | JSON | nullable | Zod schema for plugin config |

- Code: `src/plugins/manifest-types.ts:434-436` declares `id: string;` and `configSchema: JsonSchemaObject;`, where `configSchema` is required, not nullable.
- Code: `src/plugins/manifest-types.ts:434-560` has no `type` field; the kind discriminator is `kind?: PluginKind | PluginKind[]` (`src/plugins/manifest-types.ts:449`).
- Code: `src/plugins/manifest-types.ts:434-560` has no `entry` field; the entry point is the package's own module layout.
- Code: `src/plugins/manifest-types.ts:434-560` declares `name?` and `version?` as optional, not `not null`.
- Code: `src/plugins/manifest-types.ts` shows roughly 90 further optional fields, including `requiresPlugins`, `legacyPluginIds`, `autoEnableWhenConfiguredProviders`, `providerCatalogEntry`, `capabilityCatalogEntry`, `modelCatalog`, `secretProviderIntegrations`, `cliCommands`, `doctorContract`, `dashboard`, `controlUi`, `mcpServers`, `skills`, and `contracts`.
- Code: `src/plugins/manifest-types.ts:8` types `configSchema` as `JsonSchemaObject` from `../shared/json-schema.types.js`, not as a Zod schema.
- Impact: the table names four fields that no longer exist as described and omits the fields that now drive activation, discovery, and configuration.
- Classification: blocking.

### Blocking: the plugin installation sequence omits the gates and source prefixes the CLI implements

- Artifact says (specification.md:49-55):

  ```
  User → CLI: openclaw plugins install <package>
  CLI → npm: resolve and download package
  CLI → Plugin Registry: register plugin
  CLI → Config: add plugin entry to openclaw.json
  Gateway → Plugin Registry: activate on next start
  ```

- Code: `src/cli/plugins-cli.ts:144-176` accepts source prefixes and gates the install with `--accept-capabilities`, `--acknowledge-install-policy-warning`, and a deprecated `--dangerously-force-unsafe-install` no-op.
- Code: `src/security/install-policy.ts:1-40` can refuse an install outright through the operator's `security.installPolicy`.
- Code: `src/plugins/loader-provenance.ts:243` states that a plugin from an unverified source stays untrusted until it is reinstalled "from its official npm package or its official ClawHub listing", and `src/plugins/plugin-trust.ts:51-56` gates hook agent-turn authority on provenance.
- Code: `src/plugins/installed-plugin-index-store-write.ts:575` refuses a registry refresh that cannot verify npm install ownership inside the selected state directory.
- Code: `src/plugins/loader.ts` and `src/plugins/lifecycle.ts` support hot activation and plugin drain, so "activate on next start" is not the only activation path.
- Impact: the sequence omits the trust, capability, and policy gates that decide whether an install is admitted at all.
- Classification: blocking.

### Advisory: the import boundary scripts are named and typed differently

- Artifact says (specification.md:10): "Import boundary scripts (`check-*-extension-import-boundary.mjs`) enforce this at build time".
- Code: the scripts are `scripts/check-plugin-extension-import-boundary.mts` and `scripts/check-test-helper-extension-import-boundary.mts`, with the shared logic in `scripts/lib/extension-import-boundary-checker.mts`.
- Code: `package.json:1940` runs the check as `lint:plugins:no-extension-imports`.
- Impact: the described glob does not resolve to any file.
- Classification: advisory.

### Advisory: ClawHub now also acts as a publishing CLI and a first-class OpenClaw command family

- Artifact says (specification.md:64): "Marketplace | ClawHub (separate service) | Decoupled from core, community-owned".
- Code: `src/cli/plugins-authoring-command.test.ts:803-808` shows the publishing path `npm exec clawhub -- login` and `npm exec clawhub -- package publish .`, plus a generated `.github/workflows/clawhub-publish.yml`.
- Code: `src/cli/program/core-command-descriptors.ts:35-37` registers a top-level `claws` command ("Author and add OpenClaw Claws").
- Code: `src/cli/program/subcli-command-metadata.ts:20` registers `promos` ("Discover and claim promotional model offers from ClawHub").
- Impact: ClawHub participates in the core CLI surface, not only as a remote marketplace.
- Classification: advisory.
