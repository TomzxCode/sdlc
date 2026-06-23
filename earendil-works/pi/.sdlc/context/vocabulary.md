# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Pi | The project: a minimal, self-extensible terminal coding agent harness and its libraries. |
| Harness | The coding agent runtime that wires the agent loop, tools, sessions, and UI together. |
| Extension | A TypeScript module with a default export `function (pi: ExtensionAPI)` that augments the agent with tools, commands, events, UI, or providers. |
| Skill | An on-demand capability package following the Agent Skills standard (`SKILL.md` + optional frontmatter), invoked as `/skill:name`. |
| Prompt template | A Markdown file with `{{variable}}` expansion invoked as `/templatename`. |
| pi package | A distributable bundle (npm or git) of extensions, skills, prompts, themes, or custom providers, installed via `pi install`. |
| Session | A persistent, branchable conversation log stored as JSONL (`SessionHeader`, messages, compaction summaries, branch summaries). |
| Branching | Tree-structured session forking (`/fork`, `/clone`, `/tree`) where each entry has `id`/`parentId`. |
| Compaction | Lossy summarization of older session messages to reclaim context; original JSONL is preserved. |
| Steering | A queued message delivered to a streaming agent after the current tool batch completes. |
| Follow-up | A queued message delivered after the agent fully stops. |
| Project trust | A per-folder decision (`~/.pi/agent/trust.json`) gating whether project settings, resources, and extensions execute. |
| Scope (model) | A scoped model set selected with `--models pat1,pat2` for Ctrl+P cycling. |
| Faux provider | An in-memory scripted provider (`providers/faux.ts`) used for deterministic tests with no real API calls. |
| Core | The deliberately minimal set of built-in capabilities (four tools); features outside core must be extensions. |

## Technical Terms

| Term | Definition |
|---|---|
| Provider | The runtime unit owning a model catalog, auth, and stream behavior (e.g. `anthropic`, `openai`). |
| API implementation | A wire-protocol backend shared by providers (e.g. `anthropic-messages`, `openai-responses`, `openai-completions`, `google-generative-ai`, `bedrock-converse-stream`). |
| `Models` collection | pi-ai's provider registry that routes model lookups and streams by owning provider. |
| `streamFn` / `StreamFn` | The injectable function the agent calls to reach the LLM; `streamSimple` is the default. |
| `AssistantMessageEventStream` | pi-ai's async-iterable event queue (push queue + result promise) carrying `start`/`*_delta`/`done`/`error` events. |
| `Agent` | pi-agent-core's stateful class owning the transcript and lifecycle (`prompt`, `continue`, `abort`). |
| `AgentHarness` | pi-agent-core's higher-level orchestrator wrapping `Agent` with sessions, compaction, skills, and provider hooks. |
| `agentLoop` | The low-level prompt-stream-tool-continue loop in pi-agent-core. |
| `AgentMessage` | pi-agent-core's app-extensible message union (via declaration merging); `convertToLlm` bridges to pi-ai `Message`. |
| TypeBox | The schema library used for tool parameter definitions (serializable JSON, self-validating). |
| Differential rendering | pi-tui's technique of diffing a new line array against the previous frame and writing minimal escape sequences. |
| Synchronized output | Terminal escape sequence (`\x1b[?2026h..l`) used by pi-tui for atomic, flicker-free rendering. |
| Kitty keyboard protocol | Terminal input protocol pi-tui negotiates for richer key reporting. |
| Lockstep versioning | All packages share one version and release together. |
| Trusted publishing | npm publish via GitHub Actions OIDC (environment `npm-publish`); no local credentials required. |
| Shrinkwrap | `packages/coding-agent/npm-shrinkwrap.json`, generated from the root lockfile to pin transitive deps for npm users. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| TUI | Terminal User Interface (the interactive mode, and the `pi-tui` library). |
| CLI | Command-Line Interface (the `pi` binary). |
| LLM | Large Language Model. |
| MCP | Model Context Protocol (not built into core; extensions may add it). |
| SDK | Software Development Kit (the embeddable programmatic API). |
| RPC | Remote Procedure Call (the JSONL stdin/stdout protocol mode). |
| OAuth | Open Authorization (used for subscription-based provider login: Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot). |
| PKCE | Proof Key for Code Exchange (OAuth flow used by pi-ai). |
| API key | Application Programming Interface key (ambient provider authentication). |
| AC | Acceptance Criterion / Acceptance Criteria. |
| FR | Functional Requirement. |
| NFR | Non-Functional Requirement. |
| ADR | Architecture Decision Record. |
| RICE | Reach, Impact, Confidence, Effort (issue prioritization scoring). |
| SLO / SLI | Service Level Objective / Service Level Indicator. |
| OIDC | OpenID Connect (used for npm trusted publishing identity). |
| CVE | Common Vulnerabilities and Exposures. |
| IME | Input Method Editor (pi-tui positions the hardware cursor for IME candidate windows). |
| CJK | Chinese, Japanese, Korean (terminal width handling for wide characters). |
| WASM | WebAssembly (photon-node used for image resizing). |
| AGENTS.md | Project-specific rules file for humans and agents, read automatically from the repo root. |
