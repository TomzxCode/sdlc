---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### Overview and the `/templatename` contract use a `{{var}}` syntax that does not exist
- **Evidence:** `packages/coding-agent/src/core/prompt-templates.ts:76-108` — `substituteArgs` implements shell-style positional substitution; the regex at `prompt-templates.ts:80` matches `${N:-default}`, `${@:-default}`, `${@:N}`, `${@:N:L}`, `$ARGUMENTS`, `$@`, `$N`. `packages/coding-agent/src/core/prompt-templates.ts:309-325` — `expandPromptTemplate` parses the command name and arguments and calls `substituteArgs`. `packages/coding-agent/docs/prompt-templates.md:38-48` documents the same table.
- **Artifact says:** Overview: "prompt templates (`{{var}}` Markdown)". API Contracts: "### /templatename — Expands `{{variable}}` placeholders in the Markdown template into a user message."
- **Required change:** Replace `{{var}}` / `{{variable}}` with the real substitution syntax (`$1`, `$@`, `$ARGUMENTS`, `${N:-default}`, `${@:-default}`, `${@:N}`, `${@:N:L}`) and note that arguments use shell-like quoting.

### The specification counts three resource types; the code has four
- **Evidence:** `packages/coding-agent/src/core/resource-loader.ts:153-165` — `ResourceLoader` exposes `getExtensions`, `getSkills`, `getPrompts`, `getThemes`, and `getAgentsFiles`. `packages/coding-agent/src/core/package-manager.ts:88-93` — `ResolvedPaths` = `{ extensions, skills, prompts, themes }`.
- **Artifact says:** Overview: "Three resource types extend pi: extensions (TypeScript modules), skills (`SKILL.md` packages), and prompt templates (`{{var}}` Markdown)." The architecture diagram and the data models have no theme model.
- **Required change:** State four resource types and add a theme data model (JSON theme, `name`, `appearance`, `vars`, `colors`, `export`; see `packages/coding-agent/src/modes/interactive/theme/theme-schema.ts` and `packages/coding-agent/docs/themes.md:70-81`).

### The `/skill:name` contract says the body is injected into the system prompt
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:2177-2201` — `_expandSkillCommand` returns a `<skill name="..." location="...">...</skill>` block that is queued as a user message (`agent-session.ts:2221-2227`). The system prompt only carries the skill catalogue from `formatSkillsForPrompt` (`packages/coding-agent/src/core/skills.ts:358-388`). `packages/coding-agent/docs/skills.md:43-51` documents the same split, including that arguments after `/skill:name` are appended as a user request.
- **Artifact says:** "### /skill:name — Injects the skill's `SKILL.md` body into the system prompt context for the session." Architecture diagram: "Skills & Prompt Templates — loaded on demand (/skill:name, /templatename) -> injected into system prompt or expanded into user message."
- **Required change:** State that `/skill:name` expands the `SKILL.md` body into a **user message** as a `<skill>` block (frontmatter stripped, `location` and base directory included), with trailing arguments appended as a user request; the system prompt advertises only name, description, and location. Also note the `disable-model-invocation` frontmatter flag and the `enableSkillCommands` setting that controls whether skill commands appear in interactive command discovery (`packages/coding-agent/src/core/settings-defaults.ts:34`, `packages/coding-agent/src/modes/interactive/interactive-mode.ts:807-816`).

### The Skill data model lists fields the `Skill` type does not have
- **Evidence:** `packages/coding-agent/src/core/skills.ts:74-81` — `interface Skill { name: string; description: string; filePath: string; baseDir: string; sourceInfo: SourceInfo; disableModelInvocation: boolean }`. There is no `path`, `frontmatter`, or `body` member. `SkillFrontmatter` (`skills.ts:67-72`) is a separate parse-time type, and the body is read from disk at expansion time (`agent-session.ts:2188`).
- **Artifact says:** "### Skill — | name | string | from `/skill:` invocation | ... | path | string | file path | ... | frontmatter | object | optional | Metadata | body | string | not null | Markdown injected into prompt |"
- **Required change:** Replace the table with the real `Skill` members (`name`, `description`, `filePath`, `baseDir`, `sourceInfo`, `disableModelInvocation`) and note that the body and frontmatter are not retained on the object.

### The package manager contract names an API and a resource type that do not exist
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:1592-1918` — the `ExtensionAPI` interface has no `install`, `remove`, or `update` method. The package manager is CLI-only: `packages/coding-agent/src/package-manager-cli.ts:46` — `PackageCommand = "install" | "remove" | "update" | "list"`, plus `pi uninstall` (alias, `package-manager-cli.ts:400`) and `pi config` (`handleConfigCommand`, `package-manager-cli.ts:813`). `packages/coding-agent/src/core/package-manager.ts:88-93` — `ResolvedPaths` has no `models` member; there is no `models` resource type anywhere in the package manager.
- **Artifact says:** "### pi.install(name) / pi.remove(name) / pi.update(name) — Package manager operations over npm or git sources, resolving to resource directories (extensions, skills, prompts, themes, models)."
- **Required change:** Describe the CLI surface (`pi install` with a source argument, `pi remove`/`pi uninstall`, `pi update` with an optional source or `self`, `pi list`, `pi config`) and the `PackageManager` interface (`packages/coding-agent/src/core/package-manager.ts:120-136`); drop `models` from the resolved resource types. State that sources are npm (`npm:` prefix), git (`git:` prefix), URL, and local path.

### The tool-call sequence misstates the `tool_result` event and the overridable fields
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:653-725` — the `tool_call` event is emitted from the agent's `beforeToolCall` hook (`_beforeToolCall`, `agent-session.ts:659-682`) and the `tool_result` event is emitted from the `afterToolCall` hook (`_afterToolCall`, `agent-session.ts:685-725`), so `tool_result` is the after-stage, not a step after it. `packages/coding-agent/src/core/extensions/types.ts:1454-1463` — `ToolCallEventResult` = `{ block?, reason?, terminate? }`. `packages/coding-agent/src/core/extensions/types.ts:1483-1489` — `ToolResultEventResult` = `{ content?, details?, structuredContent?, isError?, usage? }`; there is no `terminate` field there.
- **Artifact says:** "agent -> tool_call event -> beforeToolCall (extension can {block: true}) -> if not blocked: tool.execute(args) -> tool_execution_update events (extensions observe) -> afterToolCall (extension can override content/details/isError/terminate) -> tool_result event"
- **Required change:** Move `tool_result` into the after-stage, list `terminate` as a `tool_call` result field, and use the real `tool_result` result fields (`content`, `details`, `structuredContent`, `isError`, `usage`).

### The resource-discovery sequence calls a method that does not exist
- **Evidence:** `packages/coding-agent/src/core/resource-loader.ts:153-165` — the `ResourceLoader` interface has no `discover()` method. The entry points are `reload(options?: ResourceLoaderReloadOptions)` (`resource-loader.ts:513`) and `loadProjectTrustExtensions()` (`resource-loader.ts:505`). The pre-trust pass is `loadProjectTrustExtensions()`, which forces `projectTrusted = false` before the trust decision is resolved (`resource-loader.ts:505-511`).
- **Artifact says:** "### Resource discovery (trust-gated) — `DefaultResourceLoader.discover()` — for each source (global, project, package): if project source and not trusted: skip — collect extensions, skills, prompts, themes, context files — -> resources_discover event (extensions may augment) -> registry populated"
- **Required change:** Rename the call to `reload()` and describe the two-pass flow (`loadProjectTrustExtensions()` -> trust decision -> `reload()`), and state that the `resources_discover` event lets extensions contribute **skill, prompt, and theme paths only** (`packages/coding-agent/src/core/extensions/runner.ts:1479-1522` returns `skillPaths`, `promptPaths`, `themePaths`).

### The event surface table omits 16 of the 41 event names
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:1597-1664` — 41 distinct event names. The specification's table lists 25 and omits `context_with_system`, `cache_warming_decision`, `before_provider_headers`, `provider_stream_event`, `agent_before_settle`, `agent_settled`, `ui_prompt_start`, `ui_prompt_end`, `tool_execution_start`, `tool_execution_update`, `tool_execution_end`, `model_select`, `thinking_level_select`, `mcp_servers_change`, `session_info_changed`, and `session_compact_failed`.
- **Artifact says:** "### Event surface (categories) — | Input | `input` | | Agent lifecycle | `before_agent_start`, `agent_start/end`, `turn_start/end` | | Messages | `message_start/update/end` | | Tools | `tool_call`, `tool_result` | | Sessions | `session_start/shutdown`, `session_before_compact/compact/fork/switch/tree` | | Provider | `before_provider_request`, `after_provider_response` | | Context | `context`, `resources_discover`, `project_trust`, `user_bash` |"
- **Required change:** Extend the table with the tool-execution, UI-prompt, boundary, provider-stream, and selection event families, or label the table as a partial view of the 41 event names.

### The `ExtensionContextActions` row assigns the wrong methods to the wrong type
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:2189-2205` — `ExtensionActions` (the `pi.*` API) holds `setActiveTools` and `setModel`. `packages/coding-agent/src/core/extensions/types.ts:2211-2233` — `ExtensionContextActions` (the `ctx.*` API) holds `abort`, `compact`, `shutdown`, `getContextUsage`, `getSystemPrompt`, and `executeTool`. `packages/coding-agent/src/core/extensions/types.ts:2239-2259` — `ExtensionCommandContextActions` holds `waitForIdle`, `newSession`, `fork`, `navigateTree`, `switchSession`, and `reload`.
- **Artifact says:** "| Session control | `ExtensionContextActions` | setActiveTools, setModel, compact, fork, abort |"
- **Severity:** advisory
- **Required change:** Split the row: `setActiveTools`/`setModel` under `ExtensionActions`; `abort`/`compact` under `ExtensionContextActions`; `fork` under `ExtensionCommandContextActions`.

### The specification has no data model for the tool contract or the context tiers
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:516` (`ToolExposure` = `direct | model-only | codemode | deferred | hidden`), `:522-531` (`ToolAnnotations` = `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), `:534-549` (`ToolNamespace`), `:552-563` (`ToolLoadout`), `:566-574` (`ToolLoadoutChanges`), `:579-660` (`ToolDefinition`, including `prepareLoadout` at `:638`), and the four context tiers `ExtensionContext` (`:325`), `ExtensionToolContext` (`:383`), `ExtensionCommandContext` (`:401`), `ReplacedSessionContext` (`:442`). None of these appear in the specification's Data Models section.
- **Artifact says:** The Data Models section holds only an `ExtensionAPI` excerpt table and the `Skill` table.
- **Severity:** advisory
- **Required change:** Add data models for `ToolDefinition` (including `exposure`, `namespace`, `annotations`, `defaultActive`, `prepareLoadout`, `reachesTools`, `outputSchema`), `ToolLoadout`/`ToolLoadoutChanges`, and the four context types, since they are the primary extension-facing contracts.

## Open questions
- The specification's architecture diagram shows discovery sources as "global (~/.pi/agent, ~/.agents)". `~/.agents/skills` is a skills-only location (`packages/coding-agent/src/core/package-manager.ts:2464`, `packages/coding-agent/src/core/trust-manager.ts:181-197`); whether the diagram should say so is a wording decision, not a code conflict.
- The specification does not name the resource-collision and diagnostic surface (`ResourceCollision` / `ResourceDiagnostic` in `packages/coding-agent/src/core/diagnostics.ts:1-15`, re-exported from `resource-loader.ts:9`). Whether the spec should document it is a scope decision.
- The specification's "Risks and Unknowns" item 1 ("the `ExtensionAPI` is large and evolving") is confirmed by the code (41 events, 30+ API methods at `types.ts:1592-1918`), but no API version constant exists in the codebase, so a stabilization version cannot be cited.
