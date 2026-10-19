<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| AgentSession | The coding agent's session object (`packages/coding-agent/src/core/agent-session.ts`): it owns the pi-agent-core `Agent`, the session file, the tool loadout, compaction, and the event stream the interactive, print, JSON, and RPC modes consume. |
| AgentSessionRuntime | The wrapper around `AgentSession` (`src/core/agent-session-runtime.ts`) that holds the session services, the model fallback message, and the factory that rebuilds a runtime after a session switch. |
| Branch summary | A `branch_summary` session entry (`src/core/compaction/branch-summarization.ts`) holding a summary of an abandoned branch, attached when `/tree` navigation leaves that branch. |
| Branching | Tree-structured session forking (`/fork`, `/clone`, `/tree`) where each JSONL entry carries `id` and `parentId` (`src/core/session-manager.ts`). |
| Chord | The typed host runtime in `packages/chord`: facets declare the contract tokens they consume (`uses`) and serve typed contracts (`remote` or `local`), and state travels between hosts as replicated state over links. |
| Codemode | The model-facing `codemode` tool (a coding-agent built-in extension, inactive by default) that runs model-written JavaScript in a QuickJS sandbox whose only capability is calling injected tools. |
| Compaction | Lossy summarization of older session messages to reclaim context; the original JSONL entries stay on disk and the `compaction` entry records the summary and the first kept entry. |
| Context edit | A `context_edit` session entry (`src/core/session-manager.ts`) that appends a replacement for, or an omission of, an earlier entry's model-visible content without rewriting history. |
| Contract | A chord type definition (`remote(name, def)` or `local(name, def)` in `packages/chord/src/contract.ts`) with TypeBox input and output schemas, a fingerprint, and a placement rule (`hostNamed` or `hostFamily`). |
| Conversation | A durable transcript scope in `packages/durable` (`Conversation` in `src/harness/types.ts`): it owns entries, admits submissions, forks, compacts, and resolves the agent that serves it. |
| Core | The deliberately minimal set of built-in capabilities (four tools: `read`, `bash`, `edit`, `write`); features outside core must be extensions. |
| Delta | The chord operation vocabulary (`Op` in `packages/chord/src/delta/index.ts`): tuples such as `["r", value]`, `["s", path, value]`, and `["p", path, start, end, items]` that describe a change to a JSON value so the change can be stored, sent, and replayed. |
| Document | A versioned JSON value in `packages/durable` addressed by a `DocumentAddress` (kind, scope, and an optional family key) and stored as a base plus deltas. The built-in kinds are `pi.agent`, `pi.inbox`, `pi.live`, `pi.provider`, `pi.usage`, and `pi.tool.nested-call`. |
| Durable runtime | The `packages/durable` runtime that separates transcript scope (`conversation`), executable work (`task`), and persisted JSON (`document`) behind a `Storage` contract with monotonic commit sequences. |
| Entry record | An immutable transcript event in `packages/durable` (`EntryRecord` in `src/types.ts`) holding optional model-facing messages, an app-facing JSON payload, context overrides of earlier entries, and the `head` marker that starts the active context. |
| Evals | Behavioral, model-backed checks for pi workflows run with `vitest-evals` and a real `AgentSession` (`packages/evals`). |
| Execution environment | The `ExecutionEnv` contract in `packages/durable/src/env/index.ts` that a harness uses for file, shell, and watcher operations, independent of where the work runs. |
| Extension | A TypeScript module with a default export `function (pi: ExtensionAPI)` that augments the agent with tools, commands, events, UI, or providers. |
| Extension context | The `ExtensionContext` object (`src/core/extensions/types.ts`) passed to every extension handler: it carries the UI surface, the run mode, the working directory, the model, the scoped models, and the abort signal. |
| Extension runner | `ExtensionRunner` (`src/core/extensions/runner.ts`): it binds the shared runtime to the session, emits extension events to the loaded handlers, and reports extension errors. |
| Facet | A chord plugin unit (`defineFacet` in `packages/chord/src/host.ts`) whose `setup(api)` registers served types on one host kind and whose `uses` list names the contract tokens it consumes. |
| Faux provider | The scripted in-memory provider in `packages/ai/src/providers/faux.ts` (`fauxProvider()`), used for deterministic tests with no real API calls. |
| Follow-up | A queued message delivered after the agent would otherwise stop, checked only when no tool calls and no steering messages remain. |
| Harness | The durable runtime entry point in `packages/durable` (`Harness.open(storage, options, context)`), which owns the scheduler, the task registry, the settings, and the conversations derived from a storage backend. |
| Hot reload | Chord's `runReload` (`packages/chord/src/reload.ts`): a host swaps facet code while running, letting in-flight work finish on the code version it started with. |
| JsonlStorage | The durable storage backend that appends commits to a `main.jsonl` file plus sidecar files (`packages/durable/src/storage/jsonl/storage.ts`). |
| Link | An ordered, bidirectional frame channel between two chord hosts (`Link` in `packages/chord/src/link.ts`); `memoryLinkPair`, `ipcLink`, and `webSocketLink` are the shipped transports. |
| MCP exposure | The per-server setting `McpExposure` (`codemode`, `deferred`, `direct`, `hidden`) in `src/core/mcp-servers.ts` that decides how an MCP server's tools reach the model. |
| MCP extension | The coding-agent built-in extension that connects configured MCP servers and registers their tools as `mcp__<server>__<tool>`. |
| MemoryStorage | The in-memory `Storage` implementation in `packages/durable/src/storage/memory.ts`, the reference implementation of the storage contract with no persistence. |
| Model | One catalog entry in pi-ai (`Model<TApi>` in `packages/ai/src/types.ts`): a provider-scoped id with its api, context window, cost rates, and thinking capabilities. |
| Model registry | `ModelRegistry` (`src/core/model-registry.ts`): the synchronous facade over `ModelRuntime` that extensions use to list and look up models. |
| Model runtime | `ModelRuntime` (`src/core/model-runtime.ts`): the canonical model and auth runtime that owns the pi-ai `Models` collection, the credential store, and catalog refresh. |
| Models | The pi-ai provider registry (`Models` in `packages/ai/src/models.ts`) that routes model lookups, auth checks, and streams by owning provider. |
| Pi | The project: a minimal, extensible agent harness that you can make your own, shipped as the `pi` CLI and the `@earendil-works/pi-*` libraries. |
| pi package | A distributable bundle (npm or git) of extensions, skills, prompts, themes, or custom providers, installed via `pi install`. |
| pi-env daemon | The small Rust program (`pi-env serve --token <hex>`) that runs on a remote machine and performs file operations and commands there over a framed protocol on stdin/stdout. |
| Project trust | A per-folder decision (`~/.pi/agent/trust.json`) gating whether project settings, resources, and extensions execute. |
| Prompt template | A Markdown file invoked as `/<name>` whose body receives shell-style argument substitution (`$1`, `$@`, `$ARGUMENTS`). |
| Provider | The pi-ai runtime unit (`Provider<TApi>` in `packages/ai/src/models.ts`) that owns a model catalog, an auth configuration, and the stream, image, and classifier implementations for its models. |
| Remote execution environment | A durable `ExecutionEnv` whose tools run on another machine through the pi-env daemon while storage and credentials stay local. |
| Replicated state | An immutable JSON value with ordered change notifications (`replicatedState` in `packages/chord/src/state.ts`): subscribers get a `hydrate` delivery first and an `update` delivery for each published change. |
| Resource loader | `ResourceLoader` (`src/core/resource-loader.ts`): the component that discovers extensions, skills, prompt templates, themes, and `AGENTS.md` context files, and reloads them on demand. |
| Scope (model) | A scoped model set selected with `--models pat1,pat2` for Ctrl+P cycling; each entry is a `ScopedModel` (a model plus an optional thinking level). |
| Service | A served type in chord (`Service` in `packages/chord/src/object.ts`): a contract plus the factory that builds its objects, with a lifetime of `referenced` or `host`. |
| Session | A persistent, branchable conversation log stored as JSONL (`SessionHeader`, messages, compaction summaries, branch summaries) under `~/.pi/agent/sessions/<encoded-cwd>/`. |
| Session entry | One line of a session file (`SessionEntry` in `src/core/session-manager.ts`): a typed record such as `message`, `thinking_level_change`, `model_change`, `usage`, `compaction`, `branch_summary`, `custom`, `custom_message`, `context_edit`, `label`, or `session_info`. |
| Session manager | `SessionManager` (`src/core/session-manager.ts`): the reader and writer for session files, with factories to create, open, continue, fork, and list sessions and to build the tree and the model context. |
| Skill | An on-demand capability package following the Agent Skills standard (`SKILL.md` plus optional frontmatter), invoked as `/skill:name`. |
| SQLite storage | The durable `Storage` backend that persists conversations, tasks, and documents in SQLite (`packages/durable/src/storage/sqlite`), with a Node adapter (`node:sqlite`) and a Cloudflare Durable Object adapter. |
| Steering | A queued message delivered to a streaming agent after the current tool batch completes. |
| Storage | The atomic persistence boundary in `packages/durable` (`Storage` in `src/types.ts`): `commit(writes)` returns a commit sequence, and every later read observes it. |
| Submission | A durably admitted user input or passive write (`SubmissionRecord` in `packages/durable`), which either runs at once or queues in `pi.inbox` while the conversation is busy. |
| Task record | The durable state of one executable unit of work (`TaskRecord` in `packages/durable`): input, checkpoint, owner, background flag, abort mark, restarts, and timestamps. |
| Telemetry schema | A versioned contract (`defineTelemetrySchema` in `packages/telemetry`) that declares allowed span names, parents, start and end attributes, events, and metrics. The repo ships `AI_TELEMETRY_SCHEMA` and `DURABLE_TELEMETRY_SCHEMA`. |
| Tool exposure | How a tool reaches the model and the runtime. `direct` and `model-only` tools are activated when they are registered; `codemode`, `deferred`, and `hidden` tools are not. |
| Virtual model | A model registered by an extension with a context-aware `route()` function (`VirtualModelDefinition` in `src/core/virtual-models.ts`) that picks the real provider and model for each request. |

## Technical Terms

| Term | Definition |
|---|---|
| `Agent` | pi-agent-core's stateful class owning the transcript and lifecycle (`prompt`, `continue`, `abort`). |
| `AgentEvent` | The pi-agent-core lifecycle event union (`agent_start`, `turn_start`, `message_start`, `tool_execution_start`, and their matching end events). |
| `agentLoop` | The low-level prompt-stream-tool-continue loop in pi-agent-core. |
| `AgentMessage` | pi-agent-core's app-extensible message union (via declaration merging); `convertToLlm` bridges to pi-ai `Message`. |
| `AgentTool` | pi-agent-core's tool contract (`packages/agent/src/types.ts`): a pi-ai `Tool` plus `label`, `execute`, and optional `prepareArguments`, `outputSchema`, and `executionMode`. |
| `ALL_TOOLS` | The codemode script global listing every callable tool as `{ name, description }`, including tools omitted from the model-facing description. |
| `Alternate screen` | pi-tui's `TuiAltScreen` renderer: a fixed-height viewport that owns its own scrolling and layout root. |
| `API implementation` | A wire-protocol backend shared by providers (e.g. `anthropic-messages`, `openai-responses`, `openai-completions`, `google-generative-ai`, `bedrock-converse-stream`). |
| `AssistantMessageEvent` | The pi-ai streaming event union (`start`, `text_start`/`text_delta`/`text_end`, `thinking_*`, `toolcall_*`, `done`, `error`). |
| `AssistantMessageEventStream` | pi-ai's async-iterable event queue (push queue + result promise) carrying `start`/`*_delta`/`done`/`error` events. |
| `AutocompleteProvider` | The pi-tui completion interface (`getSuggestions`, `applyCompletion`) that the editor consults for completions. |
| `BM25` | The Okapi BM25 ranking function used to search deferred tools in `tool_search` and in codemode's `searchTools()`. |
| `CodemodeSandbox` | The Node/Bun codemode sandbox running each script in a worker thread with a fresh QuickJS VM. |
| `Connection` | A pi-env handle to a running daemon process (over SSH or a local command) that multiplexes framed requests; owned by the caller and closed at shutdown. |
| `Constrained sampling` | Provider-side schema enforcement of a tool's parameters, declared as `constrainedSampling` on a pi-ai `Tool` and converted per API to a strict JSON schema or a grammar. |
| `Context` | The caller-facing request shape in pi-ai (`Context` in `packages/ai/src/types.ts`): a system prompt, a message list, and optional tool declarations. |
| `createInMemoryTransportPair` | The `@earendil-works/pi-mcp/testing` helper returning a linked client/server transport pair for protocol tests without I/O. |
| `credential store` | The pi-ai `CredentialStore` interface (`read`, `list`, `modify`, `delete`) and its file-backed implementation in `packages/coding-agent/src/core/auth-storage.ts` over `~/.pi/agent/auth.json`. |
| `Differential rendering` | pi-tui's technique of diffing a new line array against the previous frame and writing minimal escape sequences. |
| `Dynamic client registration` | The MCP OAuth flow where the client registers itself with the authorization server (`registerClient` in `packages/mcp/src/oauth/flow.ts`). |
| `Erasable TypeScript` | The subset of TypeScript enforced via `erasableSyntaxOnly` so types strip without code generation (no enums, namespaces, or parameter properties). |
| `Focusable` | The pi-tui marker interface for components that own a text cursor and emit the zero-width `CURSOR_MARKER` sequence. |
| `InlineCodemodeSandbox` | The codemode sandbox running scripts on the calling thread for runtimes without worker threads, when blocking the caller is acceptable. |
| `iTerm2 inline images` | The iTerm2 image protocol pi-tui encodes (`encodeITerm2`); in alternate-screen mode it falls back to text placeholders. |
| `Jiti` | The runtime TypeScript transpiler (`jiti` 2.7.0) that loads TypeScript extensions on the fly in the coding agent. |
| `JSON mode` | The coding agent's `--mode json` run mode, which streams `AgentSession` events as JSON lines. |
| `JSON-RPC` | The JSON-RPC 2.0 message format MCP uses on the wire, parsed in `packages/mcp/src/protocol/jsonrpc.ts`. |
| `Keybinding` | A named action bound to a key id (`packages/tui/src/keybindings.ts`); defaults live in `TUI_KEYBINDINGS` and `APP_KEYBINDINGS`. |
| `KeyId` | The normalized key identifier string pi-tui parses from terminal input (`ctrl+c`, `shift+tab`, `alt+left`). |
| `Kitty graphics protocol` | The terminal image protocol pi-tui encodes for Kitty-compatible terminals (`encodeKitty` in `packages/tui/src/terminal-image.ts`). |
| `Kitty keyboard protocol` | Terminal input protocol pi-tui negotiates for richer key reporting. |
| `LaTeX rendering` | pi-tui's `renderLatex` (`packages/tui/src/latex.ts`), which converts LaTeX math into ANSI text. |
| `lazy SDK loading` | The `.lazy.ts` wrappers in `packages/ai/src/api/` that defer a provider SDK import until the first request (`lazyApi` in `src/api/lazy.ts`). |
| `LocalExecutionEnv` | A `NodeExecutionEnv` that adds `listFiles` through a pi-env daemon on the same machine (`packages/env/src/list-files.ts`). |
| `Lockstep versioning` | All published packages share one version and release together. |
| `Main screen` | pi-tui's `TuiMainScreen` renderer: a linear document that grows and leaves terminal scrollback intact. |
| `McpClient` | The transport-neutral client in `@earendil-works/pi-mcp` owning request correlation, initialization, timeouts, cancellation, and tool helpers. |
| `McpTransport` | The pi-mcp transport contract (`send`, `close`, message/error/close listeners), implemented by `StdioTransport` and `StreamableHttpTransport`. |
| `ModelsStore` | The pi-ai seam that persists a provider's dynamic catalog (`models`, `lastModified`, `checkedAt`, `etag`), with `InMemoryModelsStore` as the default. |
| `node:sqlite` | The Node built-in SQLite driver behind `openNodeSqliteDatabase` and `openNodeSqliteStorage`. |
| `@options` | The optional first line of a codemode script (`// @options: {...}`) carrying `max_output_tokens` and `timeout_ms`, interpreted by the caller rather than the sandbox. |
| `pi-env protocol` | The versioned framed protocol between pi-env client and daemon (big-endian length-prefixed JSON plus raw payload frames for requests, results, errors, events, cancel, and ping). |
| `PKCE` | Proof Key for Code Exchange, the OAuth flow used by pi-ai providers and the MCP client (`packages/ai/src/auth/oauth/pkce.ts`). |
| `print mode` | The coding agent's non-interactive `-p` run mode, which prints the final answer to stdout. |
| `QuickJS` | The JavaScript engine compiled to WebAssembly that hosts codemode scripts (`quickjs-wasi` 3.6.2). |
| `RemoteCodemodeSandbox` | The portable codemode sandbox running the VM in a separately deployed Cloudflare Durable Object so computing scripts do not block the session isolate. |
| `RemoteExecutionEnv` | The durable `ExecutionEnv` talking to the pi-env daemon through a `Connection`, matching `NodeExecutionEnv` semantics on the remote machine. |
| `renderDeclarations` | The pi-codemode helper turning tool and global schemas into TypeScript declarations for a model-facing tool description. |
| `roots` | The filesystem roots an `McpClient` advertises so servers can request `roots/list`. |
| `RPC mode` | The coding agent's `--mode rpc` run mode, which speaks newline-delimited JSON commands and events over stdin/stdout. |
| `scanHostKey` / `acceptHostKey` | The pi-env SSH trust flow: show a host key fingerprint for out-of-band verification, then persist it to the application's own known-hosts file. |
| `Span/Event taxonomy` | The versioned telemetry schema (`defineTelemetrySchema`) declaring allowed span names, parents, start/end attributes, and events for typed telemetry. |
| `SQLite migration` | An ordered, versioned set of SQL statements applied by chord's `applySqliteMigrations`; the durable schema sits at `CURRENT_SQLITE_SCHEMA_VERSION = 2`. |
| `SQLITE_MIGRATIONS` | The ordered durable SQLite schema migrations in `packages/durable/src/storage/sqlite/migrations.ts`. |
| `SqliteStorage` | The portable SQLite implementation of the durable storage contract, opened via `openNodeSqliteStorage` on Node or `openDurableObjectSqliteStorage` on Cloudflare. |
| `SSE` | Server-Sent Events, the server-to-client stream of the MCP Streamable HTTP transport (`consumeSseStream` in `packages/mcp/src/transports/streamable-http.ts`). |
| `sshConnection` / `connectSsh` | The pi-env SSH entry points: a lazy connection that detects, deploys, and dials on first use, and an eager variant that does so immediately. |
| `StdioTransport` | The pi-mcp transport spawning an MCP server as a child process and speaking JSON-RPC over its stdin/stdout. |
| `StreamableHttpTransport` | The pi-mcp transport for remote MCP servers over Streamable HTTP with session resumption via `Last-Event-ID`. |
| `streamFn` / `StreamFn` | The injectable function the agent calls to reach the LLM; `streamSimple` is the default. |
| `STRICT` tables | SQLite `STRICT` tables, used for every durable table so column types are enforced. |
| `Synchronized output` | Terminal escape sequence (`\x1b[?2026h..l`) used by pi-tui for atomic, flicker-free rendering. |
| `TelemetryCarrier` | The opaque `Record<string, string>` that carries a telemetry parent across process boundaries. |
| `TelemetryContext` / `TelemetrySpan` | The span-creation scope (`TelemetryContext.startSpan`) and its active unit (`TelemetrySpan`, itself a context) carrying attributes, events, and status. |
| `ThinkingLevel` | The reasoning budget of a request: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max`. |
| `tool_search` | The built-in extension tool that finds deferred tools with BM25 and loads the matches for the next model call. |
| `ToolCall` | A model-emitted tool invocation (`ToolCall` in `packages/ai/src/types.ts`) with an id, a name, and arguments. |
| `ToolExposure` | The coding-agent tool exposure type: `direct`, `model-only`, `codemode`, `deferred`, or `hidden`. |
| `ToolResultMessage` | The transcript message carrying a tool's output (`role: "toolResult"`) back to the model. |
| `TranscriptContext` | The branded message-only context produced by `normalizeContext()` in pi-ai, the only form the agent loop hands to a provider. |
| `Trusted publishing` | npm publish via GitHub Actions OIDC (environment `npm-publish`); no local credentials required. |
| `TypeBox` | The schema library used for tool parameter definitions (serializable JSON, self-validating). |
| `WASM` | WebAssembly, the compilation target of the QuickJS sandbox (`quickjs-wasi`) and the Photon image library. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| AC | Acceptance Criterion / Acceptance Criteria. |
| ADR | Architecture Decision Record. |
| AGENTS.md | Project-specific rules file for humans and agents, read automatically from the repo root. |
| API key | Application Programming Interface key (ambient provider authentication). |
| BM25 | Best Matching 25, the Okapi term-weighting ranking function used by `tool_search`. |
| CI | Continuous Integration (the `ci` GitHub workflow). |
| CJK | Chinese, Japanese, Korean (terminal width handling for wide characters). |
| CLI | Command-Line Interface (the `pi` binary). |
| CVE | Common Vulnerabilities and Exposures. |
| DBML | Database Markup Language (the schema notation of `.sdlc/context/schema.dbml`). |
| FR | Functional Requirement. |
| HTTP | Hypertext Transfer Protocol. |
| HTTPS | Hypertext Transfer Protocol over TLS. |
| IME | Input Method Editor (pi-tui positions the hardware cursor for IME candidate windows). |
| JSON-RPC | JSON-RPC 2.0, the MCP request and notification format. |
| JSONL | JSON Lines (one JSON value per line; the session file and the RPC protocol). |
| LLM | Large Language Model. |
| MCP | Model Context Protocol (standalone client in `pi-mcp`; built-in coding-agent extension). |
| NFR | Non-Functional Requirement. |
| Nix | The Nix package manager, used to build the `pi` package offline from a pinned model catalog. |
| OAuth | Open Authorization (used for subscription-based provider login: Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot). |
| OIDC | OpenID Connect (used for npm trusted publishing identity). |
| PKCE | Proof Key for Code Exchange (OAuth flow used by pi-ai). |
| RFC | Request for Comments (Earendil publishes longer-term Pi proposals as RFCs). |
| RPC | Remote Procedure Call (the JSONL stdin/stdout protocol mode). |
| SDK | Software Development Kit (the embeddable programmatic API). |
| SLO / SLI | Service Level Objective / Service Level Indicator. |
| SQL | Structured Query Language (the durable SQLite schema and chord's migration runner). |
| SSE | Server-Sent Events (the server-to-client stream of MCP Streamable HTTP). |
| SSH | Secure Shell (transport pi-env uses to start its daemon on remote machines). |
| TUI | Terminal User Interface (the interactive mode, and the `pi-tui` library). |
| WASM | WebAssembly (the QuickJS sandbox and the Photon image library). |
| WS | WebSocket (chord's `webSocketLink` transport). |
