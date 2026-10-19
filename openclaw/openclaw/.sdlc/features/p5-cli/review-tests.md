---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Command-Line Interface test plan

## Sync drift: 2026-10-19

### Blocking: the test infrastructure section names yargs, which the project does not use

- Artifact says (tests.md:39): "- Mock yargs for command parsing tests".
- Code: `package.json:2364` declares `commander` 15.0.0; `yargs` is not a dependency and is not imported anywhere under `src/`.
- Code: `src/cli/program/build-program.ts:13-15` builds the program on `OpenClawCommand`, a Commander `Command` subclass.
- Code: `src/cli/program/command-tree.test.ts`, `src/cli/program/build-program.test.ts`, `src/cli/program/routes.test.ts`, and `src/cli/program/root-help.test.ts` all exercise the Commander program.
- Impact: a reader would look for a yargs harness that does not exist, and would not know that the CLI tests drive a Commander program with an `exitOverride` and a lazy placeholder registration model.
- Classification: blocking.

### Blocking: the onboarding requirement is mapped to a test that covers a different command

- Artifact says (tests.md:49): "FR-5 (Onboarding wizard) | `commands/agent.test.ts`".
- Artifact also lists (tests.md:25): "| `src/commands/agent.test.ts` | Agent command handler |", which contradicts the coverage row.
- Code: `src/cli/program/core-command-descriptors.ts:19-23` registers `onboard` as its own top-level command ("Guided setup for auth, models, Gateway, workspace, channels, and skills").
- Code: `src/cli/program/register.onboard.ts` and `src/cli/program/register.onboard.test.ts` own the onboard command registration.
- Code: the onboarding flow itself lives in `src/commands/onboard-*.ts` with dedicated suites such as `src/commands/onboard-agent.test.ts`, `src/commands/onboard-auth.test.ts`, `src/commands/onboard-channels.e2e.test.ts`, `src/commands/onboard-config.test.ts`, and `src/commands/onboard-custom.test.ts`.
- Code: `src/cli/program/register.setup.ts` and `src/cli/program/register.setup.test.ts` own the `setup` command, and `src/cli/program/register.configure.ts` and `src/cli/program/register.configure.persistence.test.ts` own `configure`.
- Impact: FR-5's coverage points at a test for a different feature, so the wizard requirement is effectively uncovered in the plan.
- Classification: blocking.

### Blocking: the startup performance coverage row points at a test that measures nothing

- Artifact says (tests.md:51): "NFR-2 (Startup performance) | `run-main.test.ts`".
- Artifact says (tests.md:55): "Given the CLI, when the user runs `openclaw --version`, then the output appears within 500ms".
- Code: `src/cli/run-main.test.ts` contains no timing assertion; it mocks startup admission and asserts routing behavior.
- Code: `src/cli/command-startup-timing.test.ts:16-58` records a `cli.command-startup` span in the diagnostics timeline and asserts the span shape, not a duration.
- Code: `config/` has a `control-ui-startup-budget-baseline.json` but no CLI startup budget baseline, so nothing enforces a 500ms ceiling.
- Impact: the artifact claims coverage for a performance budget that no test enforces.
- Classification: blocking.

### Advisory: the doctor and plugin coverage rows point at sources instead of test files

- Artifact says (tests.md:47): "FR-2 (Plugin management) | `plugins-cli.ts` (co-located tests)" and (tests.md:50): "FR-6 (Doctor command) | `commands/doctor.ts` (co-located tests)".
- Code: `src/cli/plugins-cli.ts` has no co-located `plugins-cli.test.ts`; the plugin CLI suites are split into `src/cli/plugins-cli.install.test.ts`, `src/cli/plugins-cli.list.test.ts`, `src/cli/plugins-cli.inspect.test.ts`, `src/cli/plugins-cli.update.test.ts`, `src/cli/plugins-cli.uninstall.test.ts`, `src/cli/plugins-cli.policy.test.ts`, `src/cli/plugins-cli.marketplace-entries.test.ts`, and `src/cli/plugins-cli.clawhub-install.e2e.test.ts`.
- Code: `src/commands/doctor.ts` does have a co-located `src/commands/doctor.test.ts`, plus `src/commands/doctor/` (for example `auth-alias-import-recovery.test.ts`, `repair-sequencing.test.ts`) and `src/flows/doctor-*.test.ts` for the health-check layer.
- Impact: the FR-2 row is not resolvable to a concrete suite, and the FR-6 row hides the size of the doctor surface.
- Classification: advisory.

### Advisory: notable test areas the artifact does not list

- Code: `src/cli/program/command-registry.test.ts`, `src/cli/program/subcli-descriptors.test.ts`, and `src/cli/program/command-tree.test.ts` cover the descriptor-driven registration catalog that replaced a static command list.
- Code: `src/cli/program/register.*.test.ts` covers each core group, for example `register.agent.test.ts`, `register.onboard.test.ts`, `register.storage.test.ts`, `register.database.import-boundary.test.ts`, `register.maintenance.lazy.test.ts`, and `register.backup.product-path.test.ts`.
- Code: `src/cli/program/help.test.ts`, `src/cli/program/parent-default-help.test.ts`, `src/cli/program/root-help.test.ts`, `src/cli/program/error-output.test.ts`, `src/cli/program/action-reparse.test.ts`, and `src/cli/program/route-args.test.ts` cover help, error, and lazy-reparse behavior.
- Code: `src/cli/program/preaction.test.ts` and `src/cli/program/config-guard.test.ts` cover the pre-action and config-guard policies.
- Code: `src/cli/completion-cli.test.ts`, `src/cli/completion-cli.bash.test.ts`, `src/cli/completion-fish.test.ts`, `src/cli/completion-command-tree.test.ts`, and `src/cli/completion-runtime.test.ts` cover the FR-10 shell completion surface, which the plan does not mention.
- Code: `src/cli/run-main.command-dispatch.test.ts`, `src/cli/run-main.exit.test.ts`, `src/cli/run-main.cleanup.test.ts`, `src/cli/run-main.gateway-startup.test.ts`, and `src/cli/run-main.bare-root.test.ts` cover the dispatch and cleanup behavior of the main runner.
- Code: `src/tui/commands.test.ts`, `src/tui/gateway-chat.test.ts`, and `src/tui/embedded-backend.test.ts` cover the TUI that FR-11 depends on.
- Code: `src/cli/workboard-owner.test.ts` and `src/cli/plugins-authoring-command.test.ts` cover plugin-owned command registration.
- Impact: the plan covers the original small command surface and misses the registration, completion, dispatch, and TUI areas that dominate the CLI today.
- Classification: advisory.
