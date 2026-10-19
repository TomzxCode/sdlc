---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The "Tool sets" table omits `powershell` and every built-in extension tool
- **Evidence:** `packages/coding-agent/src/core/tools/index.ts:95` — `export type ToolName = "read" | "bash" | "powershell" | "edit" | "write" | "grep" | "find" | "ls"`. `packages/coding-agent/src/core/settings-manager.ts:85` — `DEFAULT_TOOL_NAMES = ["read", "bash", "edit", "write"]`. `packages/coding-agent/src/core/tools/index.ts:195-202` — `createCodingTools` returns the four; `:204-211` — `createReadOnlyTools` returns `read`, `grep`, `find`, `ls`. Built-in extensions register more: `codemode` (`packages/coding-agent/src/extensions/codemode/index.ts:44`, `defaultActive: false`, exposure `model-only` at `src/extensions/codemode/tool.ts:383`), `tool_search` (`packages/coding-agent/src/extensions/tool-search/index.ts:14`, `defaultActive: false`, exposure `model-only` at `src/extensions/tool-search/tool.ts:227`), MCP tools `mcp__<server>__<tool>` (`packages/coding-agent/src/extensions/mcp/tools.ts`, default exposure `codemode` (`src/core/mcp-servers.ts:52`, `src/extensions/mcp/config.ts:158`)), and the MCP resource tools `list_mcp_resources`, `list_mcp_resource_templates`, `read_mcp_resource` (`packages/coding-agent/src/core/mcp-servers.ts:28-30`). The exposure vocabulary is `ToolExposure = "direct" | "model-only" | "codemode" | "deferred" | "hidden"` (`packages/coding-agent/src/core/extensions/types.ts:516`).
- **Artifact says:** The "Tool sets" table has two rows: "| Default (4) | `read`, `bash`, `edit`, `write` |" and "| Read-only | `read`, `grep`, `find`, `ls` |". The Technical Decisions table says "Core tools | Four only | Minimal core; more tools via extensions".
- **Required change:** Add the full built-in tool list, state that `grep`, `find`, `ls`, `powershell` are registered but off by default, describe `createReadOnlyTools` as an SDK helper rather than a CLI mode, and add the built-in extension tools with their `defaultActive` and exposure values. Update the "Core tools / Four only" decision. Blocking.

### The CLI flag table names a flag that does not exist (`--prompt`)
- **Evidence:** `packages/coding-agent/src/cli/args.ts:177` — `else if (arg === "--print" || arg === "-p")`. The help text at `packages/coding-agent/src/cli/args.ts:307` reads "--print, -p  Non-interactive mode: process prompt and exit". `--prompt-template` is a different, unrelated flag (`packages/coding-agent/src/cli/args.ts:196`).
- **Artifact says:** "| `-p` / `--prompt` | Print mode (single-shot) |".
- **Required change:** Write "`-p` / `--print`". Blocking.

### The settings excerpt has the wrong shapes for three fields
- **Evidence:** `packages/coding-agent/src/core/settings-schema.ts:218-223` — `transport` is `auto | sse | websocket | websocket-cached` (default `auto`, `src/core/settings-defaults.ts:4`). `packages/coding-agent/src/core/settings-schema.ts:266-271` — the trust setting is the scalar `defaultProjectTrust: "ask" | "always" | "never"`, not a `projectTrust` object; the trust **store** is a separate file managed by `ProjectTrustStore` (`packages/coding-agent/src/core/trust-manager.ts`). `packages/coding-agent/src/core/settings-schema.ts:287-296` — the telemetry and analytics flags are the top-level booleans `enableInstallTelemetry` (default `true`) and `enableAnalytics` (default `false`), not a `telemetry`/`analytics` object.
- **Artifact says:** "| transport | enum | `sse` / `websocket` / `auto` |", "| telemetry/analytics | object | Opt-in/out flags |", "| projectTrust | object | Trust defaults |".
- **Required change:** Add `websocket-cached` to the transport enum, replace `telemetry/analytics | object` with the two booleans `enableInstallTelemetry` and `enableAnalytics`, and replace `projectTrust | object` with the scalar `defaultProjectTrust` enum plus a pointer to `ProjectTrustStore` for per-project decisions. Blocking.

### The SDK contract lists a `fork` method that `AgentSession` does not have
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts` exposes `prompt` (`:2058`), `subscribe` (`:1373`), `get state` (`:1430`), `abort` (`:2464`), `setModel` (`:2507`), `setThinkingLevel` (`:2642`), `compact` (`:2794`), `exportToHtml` (`:4318`), `executeBash` (`:3871`), `navigateTree` (`:3994`) — there is no `fork` method. Forking lives on `SessionManager.forkFrom` (`packages/coding-agent/src/core/session-manager.ts:1815`) and on the extension command context `ExtensionCommandContext.fork(entryId, options)` (`packages/coding-agent/src/core/extensions/types.ts:416-420`).
- **Artifact says:** "Exposes `prompt`, `subscribe`, `state`, `abort`, `setModel`, `setThinkingLevel`, `compact`, `fork`."
- **Required change:** Remove `fork` from the `AgentSession` method list and state that forking is a `SessionManager.forkFrom` / `ExtensionCommandContext.fork` operation that produces a new session file. Advisory.

### The architecture diagram omits the built-in extension layer and the `pi` subcommands
- **Evidence:** `packages/coding-agent/src/main.ts:578` — `const extensionFactories = [...builtInExtensions, ...(options?.extensionFactories ?? [])]`, where `builtInExtensions` is `llama.cpp`, `codemode`, `tool-search`, `mcp` (`packages/coding-agent/src/extensions/index.ts:7-13`). The CLI also dispatches three subcommand families before the session starts: package commands (`packages/coding-agent/src/main.ts:600`), `pi config` (`:613`), and `pi mcp` (`:617`); `pi auth` runs even earlier (`:585`).
- **Artifact says:** The diagram shows `cli.ts -> main() -> AgentSession Runtime -> AgentSession -> Interactive/Print/RPC` with no extension runner and no subcommand entry points.
- **Required change:** Add the built-in extension layer (`builtInExtensions` plus the loaded project/global/package extensions) between `main()` and `AgentSession`, and the `pi install|remove|uninstall|update|list|config`, `pi auth`, and `pi mcp` subcommand paths as separate entry branches. Blocking.

### The "InteractiveMode is a very large module (~193KB)" risk understates the current size
- **Evidence:** `packages/coding-agent/src/modes/interactive/interactive-mode.ts` is 251,569 bytes over 7,127 lines.
- **Artifact says:** "Risks and Unknowns 1. `InteractiveMode` is a very large module (~193KB); changes there are high-churn and hard to review."
- **Required change:** Update the size to ~245KB / ~7,100 lines. Advisory.

### The run-mode dispatch sequence omits the mode-resolution inputs and the `--mode text` case
- **Evidence:** `packages/coding-agent/src/main.ts:112-123` — `resolveAppMode(parsed, stdinIsTTY, stdoutIsTTY)`: `--mode rpc` → rpc, `--mode json` → json, `--print` or a non-TTY stdin/stdout → print, otherwise interactive. `--mode text` is a valid value (`packages/coding-agent/src/cli/args.ts:96-105`) that keeps the interactive TUI when both stdin and stdout are terminals (`packages/coding-agent/docs/cli.md:41,46`).
- **Artifact says:** "main() -> resolveAppMode(args) / interactive -> ... / print -> runPrintMode (text or json) / rpc -> runRpcMode (JSONL stdin/stdout)".
- **Required change:** Give `resolveAppMode` its real signature and add the `--mode text` case (text output with the interactive TUI when the streams are terminals). Advisory.

## Open questions
- The "Out of Scope" section points at FEAT-0005 and FEAT-0006 by descriptive names; the actual directories are `FEAT-0005-extension-platform` and `FEAT-0006-session-persistence-branching`. The scope split itself is still correct: the extension API and the session format stay out of this feature.
- The specification does not state the session storage model, the compaction defaults (`enabled: true`, `reserveTokens: 16384`, `keepRecentTokens: 20000` at `packages/coding-agent/src/core/settings-defaults.ts:9-12`), or the extension API surface. The code answers these, but the first two belong to FEAT-0006 and the third to FEAT-0005, so the specification should link to those features rather than restate them.
