# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Branching | Tree-structured session forking (`/fork`, `/clone`, `/tree`) where each entry has `id`/`parentId`. |
| Byte transport | The minimal ordered byte-stream interface (`send`/`close`, inbound `onData`/`onClose`/`onError`) that `PiClient` uses; keeps pi-client Node-agnostic. |
| Chord | The facet/service composition runtime (`packages/chord`) where facets declare, provide, and consume singleton or keyed services with replicated state. |
| Compaction | Lossy summarization of older session messages to reclaim context; original JSONL is preserved. |
| Core | The deliberately minimal set of built-in capabilities (four tools); features outside core must be extensions. |
| Durable runtime | The Pico storage contract separating transcript scope (`conversation`), executable work (`task`), and persisted JSON (`document`) with monotonic commit sequences. |
| Evals | Behavioral, model-backed checks for pi workflows run via `vitest-evals` with a real `AgentSession`. |
| Extension | A TypeScript module with a default export `function (pi: ExtensionAPI)` that augments the agent with tools, commands, events, UI, or providers. |
| Facet | A setup unit with an `id` and `setup(env)` that declares service dependencies, provides implementations, and owns lifecycle callbacks in a Chord host. |
| Faux provider | An in-memory scripted provider (`providers/faux.ts`) used for deterministic tests with no real API calls. |
| Follow-up | A queued message delivered after the agent fully stops. |
| FTS | Full-Text Search (optional SQLite projection in pi-storage-sqlite-node). |
| Harness | The coding agent runtime that wires the agent loop, tools, sessions, and UI together. |
| Materialized view (SQLite) | Precomputed session projections (e.g. branch tips, session summaries) maintained by pi-storage-sqlite-node. |
| MemoryStorage | The detached in-memory `Storage` implementation used for tests and reference Pico behavior with no persistence. |
| Pi | The project: a minimal, self-extensible terminal coding agent harness and its libraries. |
| pi package | A distributable bundle (npm or git) of extensions, skills, prompts, themes, or custom providers, installed via `pi install`. |
| Pico | The durable agent harness (`packages/durable`, spec `pico-v5.md`) persisting conversations, tasks, and documents as atomic storage commits. |
| PiServer | The experimental token-authenticated session server in pi-server (`createUnixServer` preset, `LiveSessionManager`). |
| Plugin | A versioned bundle identity (`FacetBundlePlugin` with `id`/`version`) packaging one or more Chord facets for distribution and loading. |
| Project trust | A per-folder decision (`~/.pi/agent/trust.json`) gating whether project settings, resources, and extensions execute. |
| Prompt template | A Markdown file with `{{variable}}` expansion invoked as `/templatename`. |
| Remote session | A pi session driven over a transport (e.g. Unix socket) via the pi protocol instead of a local JSONL file. |
| Replicated state | An immutable-value shared state handle (`ReplicatedState`/`MutableReplicatedState`) mutated via a tracked proxy and published to subscribers with hydrate/update delivery. |
| Scope (model) | A scoped model set selected with `--models pat1,pat2` for Ctrl+P cycling. |
| Service (singleton/keyed) | A stable typed contract identity (`Service<T>` with string `id`) provided once (`singleton`) or per-key (`keyed`) and consumed via `use`/`observe`. |
| Session | A persistent, branchable conversation log stored as JSONL (`SessionHeader`, messages, compaction summaries, branch summaries). |
| Session lease | A remote-session ownership handle (`exclusive` or `shared`) granted by `PiClient.acquireSession()`/`createSession()`; gates who may mutate or observe a session. |
| Skill | An on-demand capability package following the Agent Skills standard (`SKILL.md` + optional frontmatter), invoked as `/skill:name`. |
| Snapshot (protocol) | An authoritative server or session state payload in the pi protocol; progress events are transient and never mutated optimistically. |
| Steering | A queued message delivered to a streaming agent after the current tool batch completes. |

## Technical Terms

| Term | Definition |
|---|---|
| `Agent` | pi-agent-core's stateful class owning the transcript and lifecycle (`prompt`, `continue`, `abort`). |
| `AgentHarness` | pi-agent-core's higher-level orchestrator wrapping `Agent` with sessions, compaction, skills, and provider hooks. |
| `agentLoop` | The low-level prompt-stream-tool-continue loop in pi-agent-core. |
| `AgentMessage` | pi-agent-core's app-extensible message union (via declaration merging); `convertToLlm` bridges to pi-ai `Message`. |
| API implementation | A wire-protocol backend shared by providers (e.g. `anthropic-messages`, `openai-responses`, `openai-completions`, `google-generative-ai`, `bedrock-converse-stream`). |
| `AssistantMessageEventStream` | pi-ai's async-iterable event queue (push queue + result promise) carrying `start`/`*_delta`/`done`/`error` events. |
| `ByteTransportFactory` | A factory creating a fresh connected, authenticated `ByteTransport` from `ByteTransportHandlers`, with exactly one terminal handler expected. |
| CBOR | Concise Binary Object Representation, the payload format for pi protocol messages. |
| Differential rendering | pi-tui's technique of diffing a new line array against the previous frame and writing minimal escape sequences. |
| Framing | The pi protocol's wire layout: four-byte big-endian payload length followed by one definite-length CBOR item. |
| `hello` | The first message a pi-client sends, carrying `PROTOCOL_VERSION` and a bearer token. |
| Kitty keyboard protocol | Terminal input protocol pi-tui negotiates for richer key reporting. |
| Lockstep versioning | All packages share one version and release together. |
| `Models` collection | pi-ai's provider registry that routes model lookups and streams by owning provider. |
| Provider | The runtime unit owning a model catalog, auth, and stream behavior (e.g. `anthropic`, `openai`). |
| Shrinkwrap | `packages/coding-agent/npm-shrinkwrap.json`, generated from the root lockfile to pin transitive deps for npm users. |
| Span/Event taxonomy | The versioned telemetry schema (`defineTelemetrySchema`) declaring allowed span names, parents, start/end attributes, and events for typed telemetry. |
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
| MCP | Model Context Protocol (not built into core; extensions may add it). |
| NFR | Non-Functional Requirement. |
| OAuth | Open Authorization (used for subscription-based provider login: Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot). |
| OIDC | OpenID Connect (used for npm trusted publishing identity). |
| PKCE | Proof Key for Code Exchange (OAuth flow used by pi-ai). |
| RICE | Reach, Impact, Confidence, Effort (issue prioritization scoring). |
| RPC | Remote Procedure Call (the JSONL stdin/stdout protocol mode). |
| SDK | Software Development Kit (the embeddable programmatic API). |
| SLO / SLI | Service Level Objective / Service Level Indicator. |
| TUI | Terminal User Interface (the interactive mode, and the `pi-tui` library). |
| WASM | WebAssembly (photon-node used for image resizing). |
