---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### Constraints: "no built-in MCP" is false; MCP ships as a replaceable built-in extension
- **Evidence:** `packages/coding-agent/src/extensions/index.ts:7-13` — `builtInExtensions` lists `{ name: "mcp", factory: mcpExtension, replaceable: true, builtin: true }` alongside `codemode`, `tool-search`, and `llama.cpp`. The implementation lives in `packages/coding-agent/src/extensions/mcp/` (`index.ts`, `config.ts`, `runtime.ts`, `tools.ts`, `resources.ts`, `oauth.ts`, `cli.ts`, `ui.ts`, `log.ts`). The CLI entry point is `packages/coding-agent/src/main.ts:788` — `disabledBuiltinExtensions: parsed.noMcp ? ["mcp"] : undefined`, so MCP is **on by default**. The opt-out is `packages/coding-agent/src/cli/args.ts:191-192` (`--no-mcp`, help text at `:328`: "Disable built-in MCP support: no servers connect and no MCP tools"). The subcommand `pi mcp add|remove|list|login|logout` is implemented in `packages/coding-agent/src/extensions/mcp/cli.ts:34-39` and dispatched from `packages/coding-agent/src/main.ts:617-621`. The client itself is the standalone package `@earendil-works/pi-mcp` (`packages/coding-agent/package.json` dependencies), not the core agent loop.
- **Artifact says:** Constraints: "Core is minimal: no built-in MCP, sub-agents, plan mode, or permission popups (extensions provide these)."
- **Required change:** Delete the "no built-in MCP" clause. State that MCP support ships as the replaceable built-in `mcp` extension, on by default, disabled with `--no-mcp`, implemented over the standalone `@earendil-works/pi-mcp` client, and configured through the `pi mcp add|remove|list|login|logout` subcommands. The "sub-agents / plan mode / permission popups are extension-provided" part stays correct (`examples/extensions/subagent/`, `examples/extensions/plan-mode/`, `examples/extensions/permission-gate.ts`). Blocking.

### FR-02 understates the shipped built-in tool surface
- **Evidence:** `packages/coding-agent/src/core/tools/index.ts:95` — `export type ToolName = "read" | "bash" | "powershell" | "edit" | "write" | "grep" | "find" | "ls"`: eight built-in tools exist, not the four the artifact names plus the read-only helper. `packages/coding-agent/src/core/settings-manager.ts:85` — `DEFAULT_TOOL_NAMES = ["read", "bash", "edit", "write"]` is the default **active** set; `grep`, `find`, `ls`, and `powershell` are registered but off by default (`packages/coding-agent/docs/cli.md:128`: "Default enabled tools are `read`, `bash`, `edit`, and `write`"). The "read-only tool set" is an SDK helper, not a CLI mode: `packages/coding-agent/src/core/tools/index.ts:204-211` — `createReadOnlyTools` returns `read`, `grep`, `find`, `ls`, exported from `packages/coding-agent/src/core/sdk.ts:139` and `packages/coding-agent/src/index.ts:273`. Four built-in extensions register further tools: `codemode` (`packages/coding-agent/src/extensions/codemode/index.ts:44`, `defaultActive: false`), `tool_search` (`packages/coding-agent/src/extensions/tool-search/index.ts:14`, `defaultActive: false`), MCP tools `mcp__<server>__<tool>` (`packages/coding-agent/src/extensions/mcp/tools.ts`), and the MCP resource tools `list_mcp_resources`, `list_mcp_resource_templates`, `read_mcp_resource` (`packages/coding-agent/src/core/mcp-servers.ts:28-30`).
- **Artifact says:** FR-02 (Must): "The system shall provide four default built-in tools: `read`, `bash`, `edit`, `write`, and a read-only tool set (`read`, `grep`, `find`, `ls`)." Acceptance criterion FR-02: "**Then** `read`, `bash`, `edit`, `write` are available, and the read-only set restricts to `read`, `grep`, `find`, `ls`."
- **Required change:** State that eight built-in tools ship and that the default active set is `read`, `bash`, `edit`, `write` (`DEFAULT_TOOL_NAMES`), with `grep`, `find`, `ls`, `powershell` available but off by default. Describe `createReadOnlyTools` as an SDK helper for the read-only set, not a CLI mode (`pi --tools read,grep,find,ls` is the CLI equivalent). Name the built-in extension tools and their `defaultActive: false` status. Blocking.

### FR-05 lists a stale subset of the slash commands and omits the extension and resource sources
- **Evidence:** `packages/coding-agent/src/core/slash-commands.ts:20-43` — `BUILTIN_SLASH_COMMANDS` has 24 entries: `settings`, `model`, `tree`, `thinking`, `scoped-models`, `export`, `import`, `share`, `bug`, `copy`, `name`, `session`, `changelog`, `hotkeys`, `fork`, `clone`, `trust`, `login`, `logout`, `new`, `compact`, `resume`, `reload`, `quit`. Built-in extensions add `/mcp` (`packages/coding-agent/src/extensions/mcp/index.ts:1260`) and `/llama` (`packages/coding-agent/src/extensions/llama/index.ts:183`). Resources add prompt-template commands and `skill:<name>` when `enableSkillCommands` is true (`packages/coding-agent/src/modes/interactive/interactive-mode.ts:804-817`; default `enableSkillCommands: true` at `packages/coding-agent/src/core/settings-defaults.ts:34`).
- **Artifact says:** FR-05 (Must): "The system shall provide built-in slash commands (`settings`, `model`, `export`, `fork`, `tree`, `login`, `logout`, `new`, `compact`, `resume`, `reload`, `quit`, and others)."
- **Required change:** Replace the partial list with the 24 built-in commands, and state that the interactive command set also contains commands registered by built-in extensions (`/mcp`, `/llama`), by loaded extensions, by prompt-template resources, and `skill:<name>` when `enableSkillCommands` is on. Blocking.

### NFR-05 names a "npm shrinkwrap" that does not exist
- **Evidence:** The real artifact is `packages/coding-agent/install-lock/`, a two-file npm project (`package.json` named `@earendil-works/pi-coding-agent-install`, plus `package-lock.json`) that pins the CLI runtime tree for the pi.dev installer. It is generated by `scripts/generate-coding-agent-install-lock.mjs` (`outputDir` at `:10`, lifecycle-script allowlist `allowedInstallScriptPackages` at `:19-22`) and is checked by `npm run check:install-lock:coding-agent` (`package.json:26`). It is consumed by `nix/package.nix:23` and `scripts/release.mjs:290`. It is **not** part of the published npm package: `packages/coding-agent/package.json` `files` lists only `dist`, `docs`, `examples`, `schemas`, `containerization.md`, `CHANGELOG.md`.
- **Artifact says:** NFR-05 (Should, Maintainability): "The published CLI shall include a generated npm shrinkwrap pinning transitive deps."
- **Required change:** Say that the repository keeps a generated two-file install-lock npm project at `packages/coding-agent/install-lock/` (package.json + package-lock.json) that pins the CLI's runtime dependency tree for the pi.dev installer and the Nix build, regenerated by `scripts/generate-coding-agent-install-lock.mjs` and verified in CI. Remove "shrinkwrap" and remove "published CLI shall include", since the file is not in the package `files` list. Blocking.

### NFR-03 "shall not include an in-process sandbox" is contradicted by the codemode QuickJS sandbox
- **Evidence:** `packages/coding-agent/src/extensions/codemode/execute.ts:512` loads the QuickJS WASM runtime (`loadQuickJSWasm`); `packages/coding-agent/src/extensions/codemode/execute.ts:52-56` states "The worker shares pi's process" and caps the VM heap at 256 MiB. The tool description says the script "run[s] as an async function body in a QuickJS sandbox ... No Node, file system, network, or timers" (`packages/coding-agent/src/extensions/codemode/tool.ts:118`), documented in `packages/coding-agent/docs/codemode.md:7`. The `quickjs-wasi` runtime dependency is declared in `packages/coding-agent/package.json`.
- **Artifact says:** NFR-03 (Must, Security): "The system shall not include an in-process sandbox; containerization is delegated to external sandboxes (documented)."
- **Required change:** Qualify the requirement. The file and shell tools still rely on the OS/container boundary (`packages/coding-agent/docs/security.md`, `packages/coding-agent/docs/containerization.md`), but the package now ships an in-process QuickJS WASM sandbox for `codemode` scripts, which has no Node APIs, file system, network, or timers and reaches the outside world only through injected tools and models. Blocking.

### No requirement covers the `pi auth` and `pi mcp` subcommands
- **Evidence:** `packages/coding-agent/src/cli/auth-command.ts:39-43` implements `pi auth check`, `pi auth print-api-key`, `pi auth print-bearer-token`; dispatched from `packages/coding-agent/src/main.ts:585-588` (`runAuthCommand`). `packages/coding-agent/src/extensions/mcp/cli.ts:34-39` implements `pi mcp add|remove|list|login|logout`; dispatched from `packages/coding-agent/src/main.ts:617-621`. The package-manager subcommands are `install`, `remove`, `uninstall` (alias of `remove`, `packages/coding-agent/src/package-manager-cli.ts:400`), `update`, `list`, `config` (`packages/coding-agent/src/package-manager-cli.ts:289-296,818`).
- **Artifact says:** FR-14 (May): "The system shall provide a `pi install/remove/update/list/config` package manager for pi packages (npm/git)." No requirement mentions `pi auth` or `pi mcp`.
- **Required change:** Add a requirement for the credential subcommands (`pi auth check|print-api-key|print-bearer-token`) and one for the MCP subcommands (`pi mcp add|remove|list|login|logout`), and add the `uninstall` alias to FR-14. Blocking.

### Overview omits two runtime dependencies
- **Evidence:** `packages/coding-agent/package.json` dependencies include `@earendil-works/pi-codemode` and `@earendil-works/pi-mcp` alongside `pi-agent-core`, `pi-ai`, `pi-tui`.
- **Artifact says:** Overview: "It wires `pi-ai`, `pi-agent-core`, and `pi-tui` into an `AgentSession`."
- **Required change:** Name `pi-codemode` and `pi-mcp` as well. Advisory.

### Acceptance criteria cover only 5 of the 19 requirements
- **Evidence:** `requirements.md:63` states "Every FR and NFR shall have at least one acceptance criterion", but the Acceptance Criteria section (lines 67-86) contains criteria only for FR-02, FR-03, FR-06, FR-08, and NFR-02. FR-01, FR-04, FR-05, FR-07, FR-09 through FR-14, NFR-01, NFR-03, NFR-04, and NFR-05 have none.
- **Artifact says:** "Every FR and NFR shall have at least one acceptance criterion."
- **Required change:** Add the missing criteria or relax the statement so the artifact matches its own contents. Advisory.

### FR-13 does not name the experimental flag or its other preconditions
- **Evidence:** `packages/coding-agent/src/core/experimental.ts:1-3` — `areExperimentalFeaturesEnabled()` returns `process.env.PI_EXPERIMENTAL === "1"`. `packages/coding-agent/src/cli/startup-ui.ts:131-150` — `shouldRunFirstTimeSetup()` requires the official Pi distribution, `PI_EXPERIMENTAL=1`, no `PI_CODING_AGENT_DIR` override (`src/config.ts:585`), and no existing `settings.json`; `showFirstTimeSetup` (`:182-197`) persists the chosen theme and `setEnableAnalytics(result.shareAnalytics)`. Wired at `packages/coding-agent/src/main.ts:677-680`.
- **Artifact says:** FR-13 (Should): "The system shall support first-time setup flow (theme + analytics opt-in) behind an experimental flag."
- **Required change:** Name the flag as the `PI_EXPERIMENTAL=1` environment variable and note the other three preconditions. Advisory.

## Open questions
- The artifact's Open Question 1 ("Should the experimental first-time setup flow graduate to default behavior") is still open; the code keeps it behind `PI_EXPERIMENTAL=1`.
- Open Question 2 (promotion policy for extensions) is not answered by the code. The `builtInExtensions` list marks `codemode`, `tool-search`, and `mcp` as `replaceable` and `llama.cpp` as not, which shows a replacement policy in practice but not a promotion policy.
- MCP, codemode, and the extension API have their own feature directories (`p12-mcp-client`, `p10-codemode-sandbox`, `FEAT-0005-extension-platform`); this artifact should link to them rather than restating their contracts.
