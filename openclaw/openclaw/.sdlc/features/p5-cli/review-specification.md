---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Command-Line Interface specification

## Sync drift: 2026-10-19

### Blocking: the CLI is built on Commander 15, not yargs

- Artifact says (specification.md:10): "The CLI is built using yargs for command parsing with nested subcommands. ... Each command is a module under `src/cli/` that registers its subcommand with yargs."
- Artifact repeats it in the data model (specification.md:39): "| options | yargs.Options | nullable | Command flags and arguments |".
- Artifact repeats it in the decisions table (specification.md:57): "| Command parsing | yargs | Mature, feature-rich, TypeScript-friendly |".
- Code: `package.json:2364` declares `"commander": "15.0.0"`; `yargs` does not appear in `package.json`.
- Code: `src/cli/program/build-program.ts:13-15` constructs `new OpenClawCommand()`, a Commander subclass, and `src/cli/program/build-program.ts:16` calls `program.enablePositionalOptions()`.
- Code: `src/cli/program/openclaw-command.ts` implements the Commander `Command` subclass used by the root program.
- Code: `src/cli/program/command-group-descriptors.ts:1` types every registrar as `(program: Command, ...)`, with `Command` imported from `commander`.
- Code: `src/plugins/cli.ts:1` and `src/plugins/cli-callback-binding.ts:3` also import `Command`, `Option`, and `Argument` from `commander`.
- Impact: every framework-dependent statement in the artifact is wrong, and a reader would look for yargs-style `.command()`/`.option()` registration that does not exist.
- Classification: blocking.

### Blocking: interactive prompts use `@clack/prompts`, not Inquirer

- Artifact says (specification.md:60): "| Interactive flow | Inquirer-based prompts | Consistent user experience for wizards |".
- Code: `package.json:2340` declares `"@clack/prompts": "1.8.1"`; neither `inquirer` nor `@inquirer/prompts` is a dependency.
- Code: `src/wizard/clack-prompter.ts:1-15` implements the wizard prompter on `@clack/prompts` (`confirm`, `select`, `multiselect`, `password`, `text`, `intro`, `outro`), and `src/wizard/` also owns `navigation-prompter.ts`, `command-choice.ts`, and `plugin-capability-consent.ts`.
- Code: `src/secrets/configure.ts` and `src/flows/doctor-health-startup.ts` also drive their interactive flows through `@clack/prompts`, and `src/cli/prompt.ts` provides the small TTY yes/no helper used by `src/cli/clawhub-install-confirmation.ts`.
- Code: `src/cli/help-cold-imports.test.ts:165-166` mocks `@clack/prompts` and asserts the module stays unloaded on the cold help path, which shows it is the prompt library in use.
- Impact: the wizard implementation choice in the artifact names a library the project does not use, and it also misses the `src/wizard/` layer that owns the interactive flows.
- Classification: blocking.

### Blocking: the architecture tree omits the program layer, the command-handler layer, and the TUI

- Artifact shows (specification.md:14-28) only `program.ts`, `gateway-cli.ts`, `plugins-cli.ts`, `config-cli.ts`, `channels-cli.ts`, `models-cli.ts`, `secrets-cli.ts`, and `onboard (wizard)` under `src/cli/`.
- Code: `src/cli/program/` is a separate layer of 89 files with a descriptor-driven registration model: `src/cli/program/core-command-descriptors.ts:16-78` holds the core command catalog, `src/cli/program/subcli-command-metadata.ts:13-74` holds the sub-CLI catalog, `src/cli/program/subcli-descriptors.ts:50-186` maps each name to a lazy registrar, `src/cli/program/register-command-groups.ts:56-113` registers lazy placeholders, and `src/cli/command-catalog.ts:34` holds the pre-Commander fast-path routing catalog.
- Code: `src/commands/` is a 1002-file command-handler layer (for example `src/commands/agents.commands.add.ts`, `src/commands/agents.commands.bind.ts`, `src/commands/agents.commands.delete.ts`, `src/commands/agents.commands.identity.ts`, `src/commands/agents.commands.list.ts`, `src/commands/agents.commands.team.ts`, `src/commands/agents.providers.ts`, `src/commands/agents.roles.test.ts`) that the artifact does not mention at all.
- Code: `src/tui/` is a 158-file terminal UI with its own `AGENTS.md`, `embedded-backend.ts`, and `gateway-chat.ts`, registered as `tui`, `terminal`, and `chat` in `src/cli/program/subcli-command-metadata.ts:46-51`.
- Code: `src/cli/` itself holds 611 files, including dedicated families such as `src/cli/gateway-cli/`, `src/cli/daemon-cli/`, `src/cli/cron-cli/`, `src/cli/nodes-cli/`, `src/cli/plugins-cli.ts`, `src/cli/secrets-cli.ts`, and `src/cli/telemetry-cli.ts`.
- Impact: the architecture section is the artifact's model of how the CLI is put together, and it omits the three layers that actually own registration, handlers, and the interactive surface.
- Classification: blocking.

### Blocking: plugin-owned commands are a first-class registration path the artifact does not describe

- Artifact says (specification.md:10): "Each command is a module under `src/cli/` that registers its subcommand with yargs."
- Code: `src/plugins/cli.ts:29-60` exports `registerPluginCliCommandsFromValidatedConfig`, which loads plugin CLI registration entries and registers them onto the same Commander program.
- Code: `src/plugins/register-plugin-cli-command-groups.ts:1` types its registrar as `(program: Command)`, and `src/plugins/cli-callback-binding.ts:3` binds `Argument`, `Command`, and `Option`.
- Code: `src/cli/program/subcli-descriptors.ts:153-158` shows the `plugins` group calling `registerPluginCliCommandsFromValidatedConfig` after registering the core group, and `src/cli/program/subcli-descriptors.ts:24-35` shows the shared `registerPluginCommandsIfNeeded` helper used by `pairing` and `plugins`.
- Code: `src/cli/program/root-command-descriptions.test.ts:26-28` asserts that `memory`, `memory search`, and `memory status` are "registered and covered by the memory-core plugin", and `src/cli/workboard-owner.test.ts:17-20` shows `workboard` as a bundled plugin that registers a CLI owner.
- Impact: the command surface is not closed over `src/cli/`, so the artifact's model of the CLI misses where commands come from.
- Classification: blocking.

### Advisory: the CLICommand data model does not match the descriptor model

- Artifact says (specification.md:32-39): a `CLICommand` has `name`, `description`, `handler`, and `options` of type `yargs.Options`.
- Code: `src/cli/program/command-group-descriptors.ts:5-17` defines `NamedCommandDescriptor` with `name`, `description`, `hasSubcommands`, optional `machineOutput`, optional `hidden`, optional `parentDefaultHelp`, and `RegisteredCommandDescriptor` with a `register` function.
- Code: `src/cli/command-catalog-types.ts` defines a separate `CliCommandCatalogEntry` with `commandPath`, `route`, and a `policy` describing `configGuard`, `loadPlugins`, `networkProxy`, and `ensureCliPath`.
- Impact: the data model needs the descriptor, the catalog policy entry, and the two-tier registration (placeholder plus lazy load) to be accurate.
- Classification: advisory.

## Sync drift: 2026-11-16

### Blocking: the command framework and prompt library claims remain wrong

- Artifact says (specification.md:10, 39, 57): the CLI is built on yargs and uses `yargs.Options`.
- Code: `package.json:2468` declares `"commander": "15.0.0"`, and there is no yargs dependency.
- Code: `src/cli/program/build-program.ts:12-14` constructs `new OpenClawCommand()`, a Commander subclass defined in `src/cli/program/openclaw-command.ts`.
- Artifact says (specification.md:60): interactive flows use Inquirer.
- Code: `package.json:2443` declares `"@clack/prompts": "1.8.1"`, and there is no Inquirer dependency.
- Code: `src/wizard/clack-prompter.ts` implements wizard prompts on `@clack/prompts`, and `src/wizard/` now holds 75 files.
- Both discrepancies were recorded on 2026-10-19 and remain unresolved.

### Blocking: the architecture tree still omits the dominant layers

- Artifact shows (specification.md:14-28) eight files under `src/cli/` and no command-handler, program, wizard, system-agent, or TUI layer.
- Code: `src/cli/program/` holds 81 files, `src/commands/` holds 1560 files, `src/tui/` holds 184 files, `src/wizard/` holds 75 files, and `src/system-agent/` holds 144 files.
- Code: `src/cli/` itself holds 1402 files, up from 611 on 2026-10-19.
- The descriptor-driven program layer and the `src/commands/` handler layer are the largest parts of the CLI and are still absent from the diagram.

### Advisory: the registration entry points changed since the earlier review

- Code: `src/cli/program/build-program.ts:2` imports `registerCoreCliCommands` from `command-registry-core.js`, and line 8 imports `registerSubCliCommands` from `register.subclis.js`.
- Code: `src/cli/program/build-program.ts:17-20` calls `program.exitOverride(...)` to preserve Commander exit codes.
- The 2026-10-19 review described registration through `core-command-descriptors.ts`, `subcli-command-metadata.ts`, `subcli-descriptors.ts`, `register-command-groups.ts`, and `command-catalog.ts`.
- Those files still exist, but the builder now delegates to the two registry modules above, so the earlier description is incomplete.

### Advisory: the plugin-owned command registration file was renamed

- The 2026-10-19 review cited `src/plugins/register-plugin-cli-command-groups.ts`.
- Code: that path no longer exists.
- Code: the responsibility now lives in `src/plugins/cli-backend-registration.ts`, `src/plugins/cli-registry-loader.ts`, and `src/plugins/cli-root-descriptors.ts`, alongside `src/plugins/cli.ts`.
- The plugin-owned command path itself still exists and is still absent from the artifact.

### Advisory: the CLICommand data model still does not match the descriptor model

- Artifact says (specification.md:32-39): a `CLICommand` has `name`, `description`, `handler`, and `options` of type `yargs.Options`.
- Code: `src/cli/program/command-group-descriptors.ts` defines `NamedCommandDescriptor` and `RegisteredCommandDescriptor`.
- Code: `src/cli/command-catalog-types.ts` defines `CliCommandCatalogEntry` with a policy describing `configGuard`, `loadPlugins`, `networkProxy`, and `ensureCliPath`.

## Sync drift: 2026-11-23

### Blocking: the framework claim is still yargs instead of Commander

- Artifact says (specification.md:10, 39, 57) the CLI is built on yargs and uses `yargs.Options`.
- Code: `package.json:2473` declares `"commander": "15.0.0"`, and no yargs dependency exists.
- Code: `src/cli/program/build-program.ts:12-19` constructs `new OpenClawCommand()`, calls `enablePositionalOptions()`, and calls `exitOverride(...)`.
- Code: `src/cli/program/openclaw-command.ts:23` defines `OpenClawCommand` as a `Command` subclass.
- Code: `src/cli/program/command-group-descriptors.ts:1-17` types every registrar as `(program: Command, ...)`.

### Blocking: the prompt library claim is still Inquirer instead of @clack/prompts

- Artifact says (specification.md:60): "Interactive flow | Inquirer-based prompts".
- Code: `package.json:2448` declares `"@clack/prompts": "1.8.1"`, and no Inquirer dependency exists.
- Code: `src/wizard/clack-prompter.ts:1-16` imports `confirm`, `select`, `multiselect`, `password`, `text`, `intro`, and `outro` from `@clack/prompts`.

### Blocking: the architecture tree still omits the dominant layers

- Artifact shows (specification.md:14-28) eight files under `src/cli/` and no program, handler, wizard, system-agent, or TUI layer.
- Code: `src/cli/program/build-program.ts:2-8` delegates registration to `command-registry-core.js` and `register.subclis.js`.
- Code: `src/cli/program/command-group-descriptors.ts:4-17` defines the descriptor contract, `src/cli/program/core-command-descriptors.ts:16-78` defines the core catalog, and `src/cli/program/subcli-command-metadata.ts:15-76` defines the sub-CLI catalog.
- Code: `src/plugins/cli.ts:76` exports the plugin-owned registration path, which the artifact never mentions.
- Code: `src/cli/` holds 1426 tracked files, `src/commands/` holds 1570, `src/tui/` holds 185, `src/wizard/` holds 76, `src/system-agent/` holds 147, and `src/cli/program/` holds 81.

### Advisory: the CLICommand data model still does not match the descriptor model

- Artifact says (specification.md:32-39): a `CLICommand` has `name`, `description`, `handler`, and `options` of type `yargs.Options`.
- Code: `src/cli/program/command-group-descriptors.ts:4-17` defines `NamedCommandDescriptor` and `RegisteredCommandDescriptor`, with `register`, `hasSubcommands`, `machineOutput`, and `hidden` fields.
- Code: `src/cli/command-catalog-types.ts:35-38` defines `CliCommandCatalogEntry` with `commandPath`, `exact`, `policy`, and `route`.
