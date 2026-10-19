---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Command-Line Interface requirements

## Sync drift: 2026-10-19

### Blocking: the supported Node range is `>=24.16.0 <25 || >=26.1.0`, not 22.19+

- Artifact says (requirements.md:46): "Must work with Node.js 22.19+ (Node 24 recommended)".
- Code: `package.json:2474-2476` declares `"engines": { "node": ">=24.16.0 <25 || >=26.1.0" }`.
- Code: `openclaw.mjs:40-41` sets `RECOMMENDED_NODE_MAJOR = 26` and `SUPPORTED_NODE_RANGE = ">=24.16.0 <25, or >=26.1.0"`.
- Code: `docs/install/index.md:13` states "**Node 24.16+ or 26.1+** - Node 26 is recommended".
- Code: `docs/install/installer.md:144` and `docs/install/installer.md:518` state "Node 24.16+ and Node 26.1+ are supported; Node 22, 23, and 25 are unsupported."
- Code: `src/infra/runtime-guard.ts:1-22` enforces the supported range at startup and imports `isSqliteWalResetSafeVersion` from `src/infra/sqlite-runtime-version.ts`.
- Impact: the constraint admits a runtime the product refuses to start on, and names the wrong recommended major.
- Classification: blocking.

### Blocking: the acceptance criterion names a command that does not exist

- Artifact says (requirements.md:51): "**FR-1**: Given the CLI, when the user runs `openclaw gateway start`, then the gateway process starts".
- Code: `src/cli/gateway-cli/register.ts:340` registers `gateway run` ("Run the WebSocket Gateway (foreground)"); the other registered `gateway` subcommands are `auth-token`, `call`, `suspend`, `resume`, `usage-cost`, `health`, `stability`, `diagnostics`, `export`, `probe`, and `discover`.
- Code: `src/cli/daemon-cli/register-service-commands.ts:78-176` registers `daemon status`, `daemon install`, `daemon stop`, and `daemon restart`; there is no `gateway start` and no `daemon start`.
- Code: `src/cli/program/subcli-command-metadata.ts:16` describes `daemon` as "Manage the Gateway service (launchd/systemd/schtasks)".
- Impact: the only acceptance criterion for the gateway lifecycle requirement cannot be executed.
- Classification: blocking.

### Blocking: the overview command inventory omits most of the shipped top-level command surface

- Artifact says (requirements.md:10): "It provides commands for managing plugins, channels, models, sessions, configurations, credentials, and the gateway process itself."
- Code: `src/cli/program/core-command-descriptors.ts:16-78` registers 24 core commands, including `setup`, `onboard`, `configure`, `config`, `claws`, `backup`, `database`, `migrate`, `storage`, `doctor`, `triage`, `dashboard`, `reset`, `uninstall`, `message`, `mcp`, `transcripts`, `agent`, `agents`, `status`, `health`, `audit`, and `sessions`.
- Code: `src/cli/program/subcli-command-metadata.ts:13-74` registers 45 more top-level groups, including `acp`, `gateway`, `daemon`, `logs`, `system`, `models`, `promos`, `telemetry`, `infer`, `capability`, `approvals`, `exec-approvals`, `exec-policy`, `nodes`, `devices`, `users`, `node`, `connect`, `worker`, `sandbox`, `worktrees`, `attach`, `tui`, `resume`, `terminal`, `chat`, `cron`, `automations`, `dns`, `docs`, `qa`, `proxy`, `hooks`, `webhooks`, `qr`, `clawbot`, `pairing`, `plugins`, `channels`, `directory`, `security`, `secrets`, `skills`, `update`, and `completion`.
- Code: `src/plugins/cli.ts:29-60` and `src/cli/program/subcli-descriptors.ts:24-35` also register plugin-owned top-level commands, so `memory` and `workboard` are not in the core lists.
- Impact: a reader of the artifact would not know the CLI has 69 core and sub-CLI top-level command groups, and would not know that part of the command surface is plugin-owned.
- Classification: blocking.

### Advisory: the TUI is listed at May priority but ships as a first-class command family

- Artifact says (requirements.md:33): "**FR-11** | May | The CLI shall provide a TUI for interactive sessions".
- Code: `src/tui/` holds 158 files including `embedded-backend.ts`, `gateway-chat.ts`, `commands.ts`, and `theme/`.
- Code: `src/cli/program/subcli-command-metadata.ts:46-51` registers `tui`, `terminal`, and `chat` as top-level commands, and `src/cli/program/subcli-descriptors.ts:112-117` maps all three to the same registrar.
- Code: `src/cli/program/subcli-command-metadata.ts:47` also registers `resume` ("Resume a recent Gateway session in the TUI").
- Code: `src/tui/AGENTS.md:3-4` documents the PTY and watch-mode test lanes.
- Impact: the priority understates a shipped, separately-tested terminal UI.
- Classification: advisory.

### Advisory: no test enforces the 500ms startup budget

- Artifact says (requirements.md:40): "**NFR-2**: Performance | CLI startup time shall be under 500ms for simple commands".
- Artifact claims coverage (tests.md:51): "NFR-2 (Startup performance) | `run-main.test.ts`".
- Code: `src/cli/run-main.test.ts` mocks startup admission and never measures elapsed time.
- Code: `src/cli/command-startup-timing.test.ts:15-57` only asserts that a startup span is recorded in the diagnostics timeline; it asserts no duration.
- Code: `config/` holds a `control-ui-startup-budget-baseline.json` but no CLI startup budget baseline.
- Impact: the requirement has no automated guard, so the coverage claim is unsupported.
- Classification: advisory.
