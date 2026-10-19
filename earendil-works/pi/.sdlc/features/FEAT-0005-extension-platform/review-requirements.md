---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### FR-09 states a `{{variable}}` template syntax that does not exist
- **Evidence:** `packages/coding-agent/src/core/prompt-templates.ts:76-108` — `substituteArgs(content, args)` implements shell-style positional substitution only. The regex at `prompt-templates.ts:80` matches `${N:-default}`, `${@:-default}`, `${@:N}`, `${@:N:L}`, `$ARGUMENTS`, `$@`, and `$N`. There is no `{{` handling anywhere in `src/core/prompt-templates.ts`, and `docs/prompt-templates.md:38-48` documents exactly the shell-style forms. `.sdlc/context/vocabulary.md:46` already states the correct behaviour ("whose body receives shell-style argument substitution (`$1`, `$@`, `$ARGUMENTS`)").
- **Artifact says:** FR-09: "The system shall load prompt templates (Markdown with `{{variable}}` expansion) invoked as `/templatename`."
- **Required change:** Replace `{{variable}}` with the real syntax: positional `$1`, `$2`, ..., all-args `$@` / `$ARGUMENTS`, defaults `${N:-default}` and `${@:-default}`, and slices `${@:N}` / `${@:N:L}`. Arguments are parsed with shell-like quoting (`parseCommandArgs`, `prompt-templates.ts:25-61`).

### FR-08 and the FR-08 acceptance criterion claim skill content is injected into the system prompt
- **Evidence:** `packages/coding-agent/src/core/agent-session.ts:2177-2201` — `_expandSkillCommand` reads `skill.filePath`, strips the frontmatter, and returns a `<skill name="..." location="...">...</skill>` block that is queued as a **user message** (`agent-session.ts:2221-2227`), not as a system prompt. The system prompt only carries the skill catalogue (name, description, location) built by `formatSkillsForPrompt` (`packages/coding-agent/src/core/skills.ts:358-388`). `docs/skills.md:43-45` describes the same split.
- **Artifact says:** FR-08: "...invoked as `/skill:name`, injected into the system prompt on demand." Acceptance criterion FR-08: "**Then** the skill content is injected into the system prompt for that session."
- **Required change:** State that the system prompt advertises each skill by name, description, and location, and that `/skill:name` expands the `SKILL.md` body into a user message wrapped in a `<skill>` block, with any trailing arguments appended as a user request (`docs/skills.md:47-51`).

### No requirement covers themes, which the code implements as a first-class resource type
- **Evidence:** `packages/coding-agent/src/core/resource-loader.ts:157` — `getThemes(): { themes: Theme[]; diagnostics: ResourceDiagnostic[] }`; `packages/coding-agent/src/core/package-manager.ts:88-93` — `ResolvedPaths` carries a `themes` resource; `packages/coding-agent/src/core/package-manager.ts:2464-2582` collects theme directories from global, project, and package sources; `packages/coding-agent/src/modes/interactive/theme/theme.ts:789-809` hot-reloads the active user theme; `packages/coding-agent/src/cli/args.ts:202-207` — `--use-theme <name[/name]>`; `packages/coding-agent/src/modes/interactive/theme/theme.ts:578-628` (`parseAutoThemeSetting`, `resolveThemeSetting`, `detectColorFgBgTheme`, `detectTerminalTheme`) implements the light/dark auto mode. `packages/coding-agent/docs/themes.md` documents it.
- **Artifact says:** The requirement table has no theme requirement. FR-10 says only "resources", and the Overview names extensions, skills, and prompt templates.
- **Required change:** Add a requirement (Must) for themes: JSON theme files discovered from global, project, and package sources, project themes gated by project trust, selection through `/settings` and the `theme` setting, `--use-theme` for a single run, the `light/dark` automatic mode, and hot reload of the active user theme.

### FR-04 lists a subset of the event surface
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:1597-1664` — 41 distinct `on(...)` event overloads, including `tool_execution_start`, `tool_execution_update`, `tool_execution_end`, `ui_prompt_start`, `ui_prompt_end`, `agent_before_settle`, `agent_settled`, `model_select`, `thinking_level_select`, `provider_stream_event`, `before_provider_headers`, `context_with_system`, `cache_warming_decision`, `mcp_servers_change`, `session_info_changed`, and `session_compact_failed`. None appear in FR-04.
- **Artifact says:** FR-04 names "input, tool_call, tool_result, message lifecycle, turn/agent lifecycle, session lifecycle, compaction, provider request/response, project_trust, and resources_discover".
- **Severity:** advisory
- **Required change:** Either extend FR-04 to cover the tool-execution, UI-prompt, boundary, and selection event families, or state explicitly that FR-04 names a representative subset of the 41 event names.

### FR-11 understates the package manager surface
- **Evidence:** `packages/coding-agent/src/package-manager-cli.ts:46` — `export type PackageCommand = "install" | "remove" | "update" | "list"`, with `pi uninstall` as an alias (`package-manager-cli.ts:400`) and `pi config` as a separate handler (`package-manager-cli.ts:813`, `handleConfigCommand`). `packages/coding-agent/src/core/package-manager.ts:148-162` — source kinds are `npm`, `git`, and `local`; `packages/coding-agent/docs/packages.md:31-37` also documents URL sources (a URL is treated as a git source).
- **Artifact says:** FR-11: "The system shall support a package manager (`pi install/remove/update/list`) for distributing extensions, skills, prompts, and themes via npm or git."
- **Severity:** advisory
- **Required change:** Add `pi uninstall` (alias), `pi config`, and the URL and local-path source kinds to FR-11.

### FR-12 does not cover virtual models
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:1911-1914` — `pi.registerVirtualModel(model)` and `pi.unregisterVirtualModel(provider, id)`; `packages/coding-agent/src/core/virtual-models.ts` defines `VirtualModelDefinition`; `packages/coding-agent/docs/virtual-models.md` documents the feature.
- **Artifact says:** FR-12 covers only custom providers via `~/.pi/agent/models.json` or extensions.
- **Severity:** advisory
- **Required change:** Extend FR-12 (or add a requirement) to cover extension-registered virtual models that route each request to a physical model.

### FR-06 omits entry renderers and markdown transformers
- **Evidence:** `packages/coding-agent/src/core/extensions/types.ts:1715-1724` — `registerMessageRenderer`, `registerMarkdownTransformer`, `registerEntryRenderer`, `registerToolRenderer` are four separate registration points.
- **Artifact says:** FR-06: "The system shall allow extensions to define keyboard shortcuts, CLI flags, autocomplete providers, and message renderers."
- **Severity:** advisory
- **Required change:** Name entry renderers and markdown transformers alongside message renderers in FR-06.

### The artifact's own acceptance-criteria rule is not met
- **Evidence:** `requirements.md:63` states "Every FR and NFR shall have at least one acceptance criterion", but the Acceptance Criteria section covers only FR-02, FR-04, FR-08, FR-10, NFR-01, and NFR-03. FR-01, FR-03, FR-05, FR-06, FR-07, FR-09, FR-11, FR-12, FR-13, NFR-02, NFR-04, and NFR-05 have none.
- **Artifact says:** "Every FR and NFR shall have at least one acceptance criterion."
- **Severity:** advisory
- **Required change:** Add acceptance criteria for the uncovered requirements, or relax the stated rule to name the requirements that are covered.

## Open questions
- The feature title is `"Extension and Skills Platform"` in `requirements.md:2`, matching the goals.md alignment table (`.sdlc/context/goals.md:70`); the directory name uses "Extension Platform". No code conflict, but the directory and artifact titles differ.
- The `pi` package gallery (`pi.image`, `pi.video` manifest fields, `packages/coding-agent/docs/packages.md:74`) is not mentioned in the requirements and is not required by any code path in `packages/coding-agent/src/`; its ownership (this feature or the website) is unresolved.
