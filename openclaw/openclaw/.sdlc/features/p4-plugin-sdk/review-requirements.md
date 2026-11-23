---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-16

Fresh analysis confirms the discrepancies recorded on 2026-10-19 remain, since requirements.md was not edited.

### Blocking: requirements.md:43 and requirements.md:49 point authors at a private package name.

- `packages/plugin-sdk/package.json` still declares `@openclaw/plugin-sdk` as private with version `0.0.0-private`.
- `docs/plugins/sdk-overview/imports.md:22` directs authors to specific subpaths such as `openclaw/plugin-sdk/channel-core`.
- `scripts/lib/plugin-sdk-entrypoints.json` lists 389 public subpaths, up from 380 at the prior review.
- FR-1 acceptance criteria still tell developers to import from the private name.

### Blocking: NFR-2 still promises compatibility the code disclaims.

- `docs/plugins/sdk-overview.md:27` states all plugin APIs are experimental and may change between releases.
- requirements.md:60 still lists the semver policy as an open question.

### Blocking: FR-2 and requirements.md:44 still limit installs to npm.

- `src/plugins/install-provenance.ts` classifies install sources as git, local-archive, local-path, marketplace, npm, and npm-pack.
- ClawHub, git, and local installs have no matching requirement.

### Blocking: the SDK boundary rules are still absent from the artifact.

- `src/plugin-sdk/AGENTS.md:22-38` defines narrow subpaths, cheap acyclic facades, and versioned required capabilities with a deprecation window.
- A reader cannot use requirements.md to review SDK surface changes.

### Advisory: FR-9 is still ranked May despite shipped permission gates.

- `docs/plugins/plugin-permission-requests.md` and `src/security/install-policy.ts` implement shipped approval and install-policy gates.

## Sync drift: 2026-11-23

Fresh analysis against current code confirms the four blocking items and the advisory item from 2026-10-19 and 2026-11-16 remain open, because requirements.md is unchanged.

### Blocking: requirements.md:43 and requirements.md:49 still point authors at the private package name

- `packages/plugin-sdk/package.json:2-4` still declares `@openclaw/plugin-sdk` as `0.0.0-private` and private.
- `package.json:522` starts the published `./plugin-sdk/*` export map, which now has 368 subpath exports.
- `scripts/lib/plugin-sdk-entrypoints.json` lists 389 public subpaths.
- `docs/plugins/sdk-overview/imports.md:22-25` still requires imports from a specific subpath such as `openclaw/plugin-sdk/channel-core`.

### Blocking: NFR-2 still promises compatibility the code disclaims

- `docs/plugins/sdk-overview.md:25-30` still states all plugin APIs are experimental and may change between releases.
- `src/plugin-sdk/plugin-entry.ts:1` still marks every public SDK contract experimental.
- `requirements.md:60` still leaves the semver policy as an open question.

### Blocking: FR-2 and requirements.md:44 still narrow installs to npm

- `src/plugins/install-provenance.ts:13-20` still classifies sources as git, local-archive, local-path, marketplace, npm, and npm-pack.
- `docs/plugins/manage-plugins.md:247-265` documents `npm:`, `npm-pack:`, `git:`, `--link`, and `clawhub:` sources.
- `docs/plugins/manage-plugins.md:422` documents `openclaw plugins install clawhub:<package> --force`.

### Blocking: the SDK boundary rules are still absent from the artifact

- `src/plugin-sdk/AGENTS.md:24-31` still requires narrow documented subpaths, cheap acyclic facades, and no broad convenience barrels.
- `src/plugin-sdk/AGENTS.md:33-38` still requires versioned required capabilities with a documented deprecation window.
- `src/plugin-sdk/AGENTS.md:50` still requires docs, entrypoint JSON, entry list, and the three SDK export checks when adding a subpath.

### Advisory: FR-9 is still ranked May despite shipped permission gates

- `src/cli/plugins-cli.ts:158-168` still exposes `--accept-capabilities`, `--acknowledge-install-policy-warning`, and the deprecated `--dangerously-force-unsafe-install` no-op.
