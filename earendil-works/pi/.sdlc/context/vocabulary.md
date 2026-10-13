# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Branching | Tree-structured session forking (`/fork`, `/clone`, `/tree`) where each entry has `id`/`parentId`. |
| Chord | The facet/service composition runtime (`packages/chord`) where facets declare, provide, and consume singleton or keyed services with replicated state. |
| Codemode | The model-facing `codemode` tool (a coding-agent built-in extension, inactive by default) that runs model-written JavaScript in a QuickJS sandbox whose only capability is calling injected tools. |
| Compaction | Lossy summarization of older session messages to reclaim context; original JSONL is preserved. |
| Core | The deliberately minimal set of built-in capabilities (four tools); features outside core must be extensions. |
| Durable runtime | The Pico storage contract separating transcript scope (`conversation`), executable work (`task`), and persisted JSON (`document`) with monotonic commit sequences. |
| Evals | Behavioral, model-backed checks for pi workflows run via `vitest-evals` with a real `AgentSession`. |
| Extension | A TypeScript module with a default export `function (pi: ExtensionAPI)` that augments the agent with tools, commands, events, UI, or providers. |
| Facet | A setup unit with an `id` and `setup(env)` that declares service dependencies, provides implementations, and owns lifecycle callbacks in a Chord host. |
| Faux provider | An in-memory scripted provider (`providers/faux.ts`) used for deterministic tests with no real API calls. |
| Follow-up | A queued message delivered after the agent fully stops. |
| Harness | The coding agent runtime that wires the agent loop, tools, sessions, and UI together. |
| MCP extension | The coding-agent built-in extension that connects configured MCP servers and registers their tools as `mcp__<server>__<tool>` with per-server exposure (`direct`, `deferred`, `codemode`, `hidden`). |
| MemoryStorage | The detached in-memory `Storage` implementation used for tests and reference Pico behavior with no persistence. |
| Pi | The project: a minimal, self-extensible terminal coding agent harness and its libraries. |
| pi package | A distributable bundle (npm or git) of extensions, skills, prompts, themes, or custom providers, installed via `pi install`. |
| pi-env daemon | The small Rust program (`pi-env serve`) running on a remote machine that performs file operations and commands there over a framed JSON protocol on stdin/stdout. |
| Pico | The durable agent harness (`packages/durable`) persisting conversations, tasks, and documents as atomic storage commits. |
| Plugin | A versioned bundle identity (`FacetBundlePlugin` with `id`/`version`) packaging one or more Chord facets for distribution and loading. |
| Project trust | A per-folder decision (`~/.pi/agent/trust.json`) gating whether project settings, resources, and extensions execute. |
| Prompt template | A Markdown file with `{{variable}}` expansion invoked as `/templatename`. |
| Remote execution environment | A Durable `ExecutionEnv` whose tools run on another machine through the pi-env daemon while storage and credentials stay local. |
| Replicated state | An immutable-value shared state handle (`ReplicatedState`/`MutableReplicatedState`) mutated via a tracked proxy and published to subscribers with hydrate/update delivery. |
| Scope (model) | A scoped model set selected with `--models pat1,pat2` for Ctrl+P cycling. |
| Service (singleton/keyed) | A stable typed contract identity (`Service<T>` with string `id`) provided once (`singleton`) or per-key (`keyed`) and consumed via `use`/`observe`. |
| Session | A persistent, branchable conversation log stored as JSONL (`SessionHeader`, messages, compaction summaries, branch summaries). |
| Skill | An on-demand capability package following the Agent Skills standard (`SKILL.md` + optional frontmatter), invoked as `/skill:name`. |
| SQLite storage | The portable Pico `Storage` backend persisting conversations, tasks, and documents in SQLite, with a Node adapter (`node:sqlite`) and a Cloudflare Durable Object adapter. |
| Steering | A queued message delivered to a streaming agent after the current tool batch completes. |
| Tool exposure | How an MCP server's tools reach the model: `direct` (declared immediately), `deferred` (via `tool_search`), `codemode` (scripts only), or `hidden` (unreachable). |

## Technical Terms

| Term | Definition |
|---|---|
| `Agent` | pi-agent-core's stateful class owning the transcript and lifecycle (`prompt`, `continue`, `abort`). |
| `AgentHarness` | pi-agent-core's higher-level orchestrator wrapping `Agent` with sessions, compaction, skills, and provider hooks. |
| `agentLoop` | The low-level prompt-stream-tool-continue loop in pi-agent-core. |
| `AgentMessage` | pi-agent-core's app-extensible message union (via declaration merging); `convertToLlm` bridges to pi-ai `Message`. |
| `ALL_TOOLS` | The codemode script global listing every callable tool as `{ name, description }`, including tools omitted from the model-facing description. |
| API implementation | A wire-protocol backend shared by providers (e.g. `anthropic-messages`, `openai-responses`, `openai-completions`, `google-generative-ai`, `bedrock-converse-stream`). |
| `AssistantMessageEventStream` | pi-ai's async-iterable event queue (push queue + result promise) carrying `start`/`*_delta`/`done`/`error` events. |
| `CodemodeSandbox` | The Node/Bun codemode sandbox running each script in a worker thread with a fresh QuickJS VM. |
| `Connection` | A pi-env handle to a running daemon process (over SSH or a local command) that multiplexes framed requests; owned by the caller and closed at shutdown. |
| `createInMemoryTransportPair` | The `@earendil-works/pi-mcp/testing` helper returning a linked client/server transport pair for protocol tests without I/O. |
| Differential rendering | pi-tui's technique of diffing a new line array against the previous frame and writing minimal escape sequences. |
| Erasable TypeScript | The subset of TypeScript enforced via `erasableSyntaxOnly` so types strip without code generation (no enums, namespaces, or parameter properties). |
| `InlineCodemodeSandbox` | The codemode sandbox running scripts on the calling thread for runtimes without worker threads, when blocking the caller is acceptable. |
| Kitty keyboard protocol | Terminal input protocol pi-tui negotiates for richer key reporting. |
| `LocalExecutionEnv` | A `RemoteExecutionEnv`-compatible execution environment backed by a daemon on the same machine, adding `listFiles`. |
| Lockstep versioning | All packages share one version and release together. |
| `McpClient` | The transport-neutral client in `@earendil-works/pi-mcp` owning request correlation, initialization, timeouts, cancellation, and tool helpers. |
| `Models` collection | pi-ai's provider registry that routes model lookups and streams by owning provider. |
| `@options` | The optional first line of a codemode script (`// @options: {...}`) carrying `max_output_tokens` and `timeout_ms`, interpreted by the caller rather than the sandbox. |
| pi-env protocol | The versioned framed protocol between pi-env client and daemon (big-endian length-prefixed JSON plus raw payload frames for requests, results, errors, events, cancel, and ping). |
| Provider | The runtime unit owning a model catalog, auth, and stream behavior (e.g. `anthropic`, `openai`). |
| `RemoteCodemodeSandbox` | The portable codemode sandbox running the VM in a separately deployed Cloudflare Durable Object so computing scripts do not block the session isolate. |
| `RemoteExecutionEnv` | The Durable `ExecutionEnv` talking to the pi-env daemon through a `Connection`, matching `NodeExecutionEnv` semantics on the remote machine. |
| `renderDeclarations` | The pi-codemode helper turning tool and global schemas into TypeScript declarations for a model-facing tool description. |
| `roots` | The filesystem roots an `McpClient` advertises so servers can request `roots/list`. |
| `scanHostKey` / `acceptHostKey` | The pi-env SSH trust flow: show a host key fingerprint for out-of-band verification, then persist it to the application's own known-hosts file. |
| Span/Event taxonomy | The versioned telemetry schema (`defineTelemetrySchema`) declaring allowed span names, parents, start/end attributes, and events for typed telemetry. |
| `SQLITE_MIGRATIONS` | The ordered SQLite schema migrations for durable storage with `CURRENT_SQLITE_SCHEMA_VERSION` marking the latest version. |
| `SqliteStorage` | The portable SQLite implementation of the Pico storage contract, opened via `openNodeSqliteStorage` on Node or `openDurableObjectSqliteStorage` on Cloudflare. |
| `sshConnection` / `connectSsh` | The pi-env SSH entry points: a lazy connection that detects, deploys, and dials on first use, and an eager variant that does so immediately. |
| `StdioTransport` | The pi-mcp transport spawning an MCP server as a child process and speaking JSON-RPC over its stdin/stdout. |
| `StreamableHttpTransport` | The pi-mcp transport for remote MCP servers over Streamable HTTP with session resumption via `Last-Event-ID`. |
| `streamFn` / `StreamFn` | The injectable function the agent calls to reach the LLM; `streamSimple` is the default. |
| Synchronized output | Terminal escape sequence (`\x1b[?2026h..l`) used by pi-tui for atomic, flicker-free rendering. |
| `TelemetryContext` / `TelemetrySpan` | The span-creation scope (`TelemetryContext.startSpan`) and its active unit (`TelemetrySpan`, itself a context) carrying attributes, events, and status. |
| Trusted publishing | npm publish via GitHub Actions OIDC (environment `npm-publish`); no local credentials required. |
| TypeBox | The schema library used for tool parameter definitions (serializable JSON, self-validating). |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| AC | Acceptance Criterion / Acceptance Criteria. |
| ADR | Architecture Decision Record. |
| AGENTS.md | Project-specific rules file for humans and agents, read automatically from the repo root. |
| API key | Application Programming Interface key (ambient provider authentication). |
| CJK | Chinese, Japanese, Korean (terminal width handling for wide characters). |
| CLI | Command-Line Interface (the `pi` binary). |
| CVE | Common Vulnerabilities and Exposures. |
| FR | Functional Requirement. |
| IME | Input Method Editor (pi-tui positions the hardware cursor for IME candidate windows). |
| LLM | Large Language Model. |
| MCP | Model Context Protocol (standalone client in `pi-mcp`; built-in coding-agent extension). |
| NFR | Non-Functional Requirement. |
| OAuth | Open Authorization (used for subscription-based provider login: Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot). |
| OIDC | OpenID Connect (used for npm trusted publishing identity). |
| PKCE | Proof Key for Code Exchange (OAuth flow used by pi-ai). |
| RICE | Reach, Impact, Confidence, Effort (issue prioritization scoring). |
| RPC | Remote Procedure Call (the JSONL stdin/stdout protocol mode). |
| SDK | Software Development Kit (the embeddable programmatic API). |
| SLO / SLI | Service Level Objective / Service Level Indicator. |
| SSH | Secure Shell (transport pi-env uses to start its daemon on remote machines). |
| TUI | Terminal User Interface (the interactive mode, and the `pi-tui` library). |
| WASM | WebAssembly (photon-node used for image resizing). |
