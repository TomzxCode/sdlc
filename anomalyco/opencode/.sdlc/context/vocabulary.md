<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->
# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Admitted Prompt | A durable user input accepted into the session inbox but not yet delivered into Session History. |
| Agent | A named configuration of system instructions, model, and permissions (for example `build`, `plan`). |
| Baseline System Context | The full System Context rendered from epoch-initial instruction values at the start of a Context Epoch (avoid: "live system prompt"). |
| Catalog | The provider-neutral registry of models and their settings, rebuilt from replayable Location-scoped transforms contributed by config, models.dev, auth, and plugins. |
| Context Epoch | The span during which epoch-initial instruction values form the immutable baseline for model requests, ended by completed compaction while session movement retains state and emits chronological updates. |
| Context Source | One independently observed instruction value within the System Context, identified by a stable source key, with a content-addressed value and optional rendered update text (avoid: "prompt fragment"). |
| Control Item | An inbox item requesting compaction or Session movement instead of a user message, forming a delivery boundary so later steers do not cross it. |
| Inbox Admission | The durable `session.inbox.enqueued` fact and projection that insert one `session_inbox` row before advisory execution starts; delivery publishes `session.inbox.delivered` and consumes the row atomically with the visible message. |
| Instruction Blob | The machine-local content-addressed store holding canonical JSON bodies for instruction values referenced by state hashes. |
| Instruction State | The overwriteable per-Session row holding current and epoch-initial instruction values used at safe boundaries and to seed forks. |
| Location | The filesystem and workspace scope, a directory plus an optional `workspaceID`, that bounds sessions, tools, model resolution, permissions, and plugin services. |
| Managed Tool Output File | A temporary file retaining complete tool output too large for session history. |
| Mid-Conversation System Message | A durable chronological instruction telling the model the newly effective state of a changed Context Source (avoid: "system update"). |
| Model Tool Output | The bounded canonical model content of a tool result persisted in Session History and replayed to the model. |
| Physical Attempt | One try within a Step, where generic retry, continuation-state rejection, incomplete-stream continuation, or overflow-triggered compaction may create another attempt without promoting input again. |
| Prompt Promotion | The durable transition that delivers an Admitted Prompt from pending input and appends its user message to Session History. |
| Queue Delivery | The inbox delivery mode that keeps an item pending while the Session can continue, so steers take priority at an idle boundary and otherwise one queued item delivers before the runner reevaluates continuation. |
| Safe Step Boundary | The point immediately before a Step's model call, after input promotion and tool settlement, where steers and instruction changes may be admitted chronologically. |
| Session | A durable conversational unit tied to a project directory that preserves replayable history and runtime context. |
| Session Drain | One process-local execution span that promotes eligible input and runs required Steps until no immediate continuation remains; it has no durable identity and its wakeups are coalesced by `SessionRunCoordinator`. |
| Session History | The projected chronological conversation reloaded before each Step after applying compaction and instruction epoch cutoffs (avoid: "session context"). |
| Steer | The default inbox delivery mode in which an item delivers in enqueue order at the next Safe Step Boundary, stopping before a compaction or move Control Item. |
| Step | One logical LLM call in a Session drain whose durable record covers only the model-visible span, reloaded from history before the call (not "provider turn"). |
| System Context | The structured collection of instruction values presented to the model as an epoch baseline and chronological updates (avoid: "system prompt"). |
| Turn | The reserved future unit containing all Steps from prompt promotion until the Session would go idle, never a name for a single LLM call. |

## Technical Terms

| Term | Definition |
|---|---|
| ACP | Agent Client Protocol; interoperable agent communication protocol implemented in OpenCode. |
| CodeMode | A confined execution runtime that lets a model write small JavaScript programs calling only host-supplied tools, with no ambient filesystem, process, network, or application authority. |
| Compaction | The operation that stores a structured rolling summary plus bounded recent context as active model history when a request exceeds the model's context window, while the full transcript remains durable. |
| Drizzle | The ORM used for SQLite schemas, with snake_case field names defined in a vendored Effect SQLite adapter. |
| Durable Object | A stateful Cloudflare Worker instance with its own injected `DurableObjectStorage` SQLite, used as a Workerd persistence boundary. |
| Effect | The functional effect system used pervasively in the core runtime. |
| Effect Schema | The Effect schema library used for typed validation, encoding, and decoding of shared contracts across Schema, Protocol, and Server. |
| Experimental Endpoint | An API route under `/api/experimental/<group>/...` with an `experimental.<group>.<method>` identifier, documented as changeable without compatibility guarantees. |
| Feature Flag | A key from `packages/schema/src/config/flag.ts` that gates risky or unfinished behavior, read with `Flag.enabled("<key>")` and set through `OPENCODE_FLAGS` or `experimental.<key>`. |
| Hono | The web framework used by the legacy Worker in `services/legacy`; the current API uses Effect HttpApi. |
| HttpApi | Effect's declarative HTTP API definition assembled in `packages/protocol` to define public endpoints, drive OpenAPI, and generate the client SDK. |
| LocationServiceMap | The process-local map from `Location.Ref` to Location-scoped instance services, used to resolve and cache placement services when a drain starts. |
| MCP | Model Context Protocol; external tool and context servers the agent can call. |
| models.dev | The upstream data source for provider and model metadata, added there first when new providers are supported. |
| OpenTUI | The terminal UI framework used by the TUI. |
| PTY Environment | The host-supplied environment overlay applied when creating a PTY. |
| Plugin | A package extending OpenCode via the `@opencode/plugin` SDK and namespaced hooks. |
| SessionExecution | The process-global, Session-ID keyed service that resumes, wakes, and interrupts process-local drains and routes them to the selected Location's runner. |
| SessionRunCoordinator | The local ownership primitive that serializes execution per Session ID, joins explicit resumes, coalesces wakes, allows different Sessions to run concurrently, and tracks process-local busy periods. |
| Snapshot | The Core service that stages and clears revert points for a Session using projected state. |
| Workerd | Cloudflare's Workers runtime, where OpenCode runs inside a Durable Object with injected storage. |
| Worktree | Git worktree management utilities for parallel branch contexts. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| AC | Acceptance Criterion |
| ACP | Agent Client Protocol |
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| CDP | Chrome DevTools Protocol |
| CI | Continuous Integration |
| CLI | Command-Line Interface |
| FR / NFR | Functional Requirement / Non-Functional Requirement |
| HTTP | Hypertext Transfer Protocol |
| IaC | Infrastructure as Code |
| JSON | JavaScript Object Notation |
| LLM | Large Language Model |
| LSP | Language Server Protocol |
| MCP | Model Context Protocol |
| PR | Pull Request |
| PTY | Pseudo-Terminal |
| RICE | Reach, Impact, Confidence, Effort (prioritization) |
| SDK | Software Development Kit |
| TUI | Terminal User Interface |
| UI | User Interface |
| VM | Virtual Machine |
