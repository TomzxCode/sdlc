# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Session | A durable conversational unit tied to a project directory that preserves replayable history and runtime context. |
| System Context | The structured collection of contextual facts presented to the model as initial instructions and chronological updates (avoid: "system prompt"). |
| Session History | The projected chronological conversation selected for a provider turn after applying compaction and context epoch cutoffs (avoid: "session context"). |
| Context Source | One independently observed typed value within the System Context, identified by a stable key, codec, and pure renderers (avoid: "prompt fragment"). |
| Context Epoch | The span during which one initially rendered System Context remains the immutable provider-cache baseline, ending at compaction, session movement, or an incompatible transition. |
| Baseline System Context | The full System Context rendered at the start of a Context Epoch (avoid: "live system prompt"). |
| Mid-Conversation System Message | A durable chronological instruction telling the model the newly effective state of a changed Context Source (avoid: "system update"). |
| Context Snapshot | The overwriteable model-hidden JSON state used to compare each Context Source with the value last admitted to a provider turn. |
| Provider Turn | One request to a model provider and the response projected from that request. |
| Session Drain | One process-local execution span that promotes eligible input and runs required provider turns until no immediate continuation remains; it has no durable identity. |
| Admitted Prompt | A durable user input accepted into the session inbox but not yet included in Session History. |
| Prompt Promotion | The durable transition that removes an Admitted Prompt from pending input and appends its user message to Session History. |
| Safe Provider-Turn Boundary | The point immediately before a provider call, after input promotion and tool settlement, where context changes may be admitted chronologically. |
| Model Tool Output | The bounded projection of a tool result persisted in session history and replayed to the model. |
| Managed Tool Output File | A temporary file retaining complete output too large for session history. |
| Agent | A named configuration of system instructions, model, and permissions (e.g. `build`, `plan`). |
| Location | The filesystem/workspace scope that bounds sessions, tools, model resolution, and permissions. |
| Catalog | The provider-neutral registry of models, request options, and generation controls. |

## Technical Terms

| Term | Definition |
|---|---|
| models.dev | The upstream data source for provider/model metadata; new providers are added there first. |
| opentui | The terminal UI framework (SolidJS-based) used by the TUI. |
| Effect | The functional effect system used pervasively in the core runtime. |
| Drizzle | The ORM used for SQLite schemas (snake_case field names). |
| SST | The IaC framework used for cloud infra (`sst.config.ts`). |
| Hono | The web framework used for the HTTP API server. |
| MCP | Model Context Protocol; external tool/context servers the agent can call. |
| ACP | Agent Client Protocol; interoperable agent communication protocol implemented in OpenCode. |
| Plugin | A package extending OpenCode via the `@opencode-ai/plugin` SDK and namespaced hooks. |
| Compaction | The operation that folds the current complete System Context into a fresh baseline and starts a new Context Epoch. |
| Generation Controls | Provider-neutral sampling/output controls partitioned from provider wire semantics. |
| Model Request Options | Provider-semantic model settings resolved from the Catalog before LLM protocol encoding. |
| PTY Environment | The host-supplied environment overlay applied when creating a PTY. |
| CodeMode | A confined execution runtime that lets a model write small JavaScript programs calling only host-supplied tools, with no ambient filesystem, process, network, or application authority. |
| Managed Tool Output File | A temporary file retaining complete tool output too large for session history. |
| Snapshot | State snapshots mechanism for saving and restoring session state. |
| Worktree | Git worktree management utilities for parallel branch contexts. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| TUI | Terminal User Interface |
| SDK | Software Development Kit |
| API | Application Programming Interface |
| CLI | Command-Line Interface |
| MCP | Model Context Protocol |
| LLM | Large Language Model |
| LSP | Language Server Protocol |
| ACP | Agent Client Protocol |
| ADR | Architecture Decision Record |
| PTY | Pseudo-Terminal |
| PR | Pull Request |
| FR / NFR | Functional Requirement / Non-Functional Requirement |
| AC | Acceptance Criterion |
| CI | Continuous Integration |
| RICE | Reach, Impact, Confidence, Effort (prioritization) |
