---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Plugin SDK and Extension System requirements

## Sync drift: 2026-10-19

### Blocking: the public import specifier is `openclaw/plugin-sdk/<subpath>`, not `@openclaw/plugin-sdk`

- Artifact says (requirements.md:43): "Plugins must not import from core `src/` directories; only `@openclaw/plugin-sdk` is allowed".
- Artifact says (requirements.md:49): "**FR-1**: Given a plugin project, when the developer imports from `@openclaw/plugin-sdk`, then all required types are available".
- Code: `packages/plugin-sdk/package.json:2-4` declares `"name": "@openclaw/plugin-sdk"`, `"version": "0.0.0-private"`, `"private": true`.
- Code: `package.json:493-496` exposes the published surface as `"./plugin-sdk/core"`, and `package.json:491-492` maps `"."` to the CLI entry `./dist/index.js`.
- Code: `scripts/lib/plugin-sdk-entrypoints.json` lists 380 public subpaths under the `openclaw` package.
- Code: `docs/plugins/sdk-overview/imports.md:22-25` instructs plugin authors to "Always import from a specific subpath" with `import { defineChannelPluginEntry } from "openclaw/plugin-sdk/channel-core";`.
- Code: `extensions/telegram/index.ts:1` imports `openclaw/plugin-sdk/channel-entry-contract`.
- Impact: a third-party plugin author following the artifact would import a private, unpublished package name and would not learn that the SDK is a set of narrow subpaths.
- Classification: blocking.

### Blocking: NFR-2 asserts a semver-style compatibility guarantee the code explicitly does not provide

- Artifact says (requirements.md:39): "**NFR-2**: The SDK public API shall maintain backward compatibility within a major version".
- Artifact leaves it open (requirements.md:60): "What is the plugin API stability guarantee (semver policy)?".
- Code: `docs/plugins/sdk-overview.md`, section "API stability", states "All OpenClaw plugin APIs are **experimental**. This includes every `openclaw/plugin-sdk/*` subpath, registration and runtime APIs, channel and provider contracts, hooks, and native Control UI APIs. These contracts can change between OpenClaw releases."
- Code: `src/plugin-sdk/plugin-entry.ts:1` states "All public plugin SDK contracts are experimental; see docs/plugins/sdk-overview.md#api-stability."
- Code: `src/plugin-sdk/AGENTS.md:49` says third-party-visible breaking removals need "an announced stable-release deprecation window, and explicit maintainer approval", which is a deprecation policy, not a major-version compatibility promise.
- Impact: NFR-2 and the acceptance criteria in the artifact promise stability that the code does not offer, and the open question has already been answered in the code.
- Classification: blocking.

### Blocking: the install-source constraint is narrower than the shipped install surface

- Artifact says (requirements.md:44): "Bundled plugins ship with core; external plugins are installed from npm".
- Artifact says (requirements.md:25): "**FR-2**: The system shall support installing plugins from npm packages".
- Code: `docs/plugins/manage-plugins.md:230-245` documents `openclaw plugins install <package>`, `npm:<package>`, `npm-pack:<path.tgz>`, `git:github.com/acme/openclaw-plugin@v1.0.0`, `./my-plugin`, and `--link ./my-plugin`.
- Code: `src/plugins/install-provenance.ts:13-20` classifies install sources as `git`, `local-archive`, `local-path`, `marketplace`, `npm`, `npm-pack`.
- Code: `docs/plugins/manage-plugins.md:393` documents `openclaw plugins install clawhub:<package> --force`.
- Impact: FR-2 remains true, but the constraint that external plugins come from npm is false, and ClawHub archive installs are not covered by any requirement.
- Classification: blocking.

### Blocking: the SDK boundary rules that govern the public surface are absent from the artifact

- Artifact (requirements.md:38-39, requirements.md:43) describes only "import boundary enforcement" and a single allowed import path.
- Code: `src/plugin-sdk/AGENTS.md:22-31` defines the boundary rules: new surface is "a small versioned host/kernel seam + narrow purpose-built documented subpath; no broad convenience barrels or re-exports"; "Public SDK entrypoints: cheap module load"; "SDK facades: acyclic. No back-edge re-exports routing lightweight contract file through heavier policy/runtime modules"; "Never mix static/dynamic imports for same runtime surface".
- Code: `src/plugin-sdk/AGENTS.md:33-38` defines "Versioned Required Capabilities": "Always: shipped Plugin SDK parameter contract gains required host authority → versioned type requiring it", "Never: legacy optionality as capability-free runtime path".
- Code: `src/plugin-sdk/AGENTS.md:50` requires the process for adding a subpath: update `docs/plugins/*`, `scripts/lib/plugin-sdk-entrypoints.json`, `scripts/lib/plugin-sdk-entries.mts`, then run `pnpm plugin-sdk:sync-exports`, `pnpm plugin-sdk:check-exports`, `pnpm plugin-sdk:api:diff`.
- Impact: a maintainer or plugin author reading the artifact gets no rule for how SDK surface grows, no subpath discipline, and no deprecation window, so the artifact cannot be used to review SDK changes.
- Classification: blocking.

### Advisory: permission and capability gating is implemented but ranked May

- Artifact says (requirements.md:32): "**FR-9** | May | The system shall support plugin permissions and capability gating".
- Code: `docs/plugins/plugin-permission-requests.md` documents the shipped `plugin.approval.*` runtime approval flow.
- Code: `src/security/install-policy.ts:1-20` implements an operator-configurable install policy that can refuse an install.
- Code: `src/cli/plugins-cli.ts:158-168` exposes `--accept-capabilities` and `--acknowledge-install-policy-warning` gates.
- Impact: the requirement is listed but its priority understates a shipped security boundary.
- Classification: advisory.
