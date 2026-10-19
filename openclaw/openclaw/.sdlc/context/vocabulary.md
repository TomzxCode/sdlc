# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Active Memory | Deep conversation-history recall that escalates to a blocking recall sub-agent only when rule-based memory recall finds no strong trusted trigger match |
| Agent | The AI assistant instance that processes conversations and executes tools |
| Agent Binding | A routing rule that names the agent that owns conversations matching channel facts such as account, peer, guild, team, or Discord role |
| Audit Ledger | The durable, content-free record of Gateway activity stored in `audit_events` and read back with `openclaw audit` |
| Board (Workboard) | An optional Kanban-style board of agent-sized work cards in the Control UI, plus a Sessions board that groups sessions by rules over Gateway-owned facts |
| Channel | A messaging platform integration (WhatsApp, Telegram, Discord, etc.) that the assistant communicates through |
| ClawHub | The community plugin marketplace at https://clawhub.ai |
| Cloud Worker | A disposable remote machine, provisioned and owned by the Gateway, that runs a session's coding work while the transcript and accepted workspace changes stay with the Gateway |
| Compaction | The process of summarizing old conversation turns to manage context window limits |
| Context Engine | The plugin-selected component that assembles prompt context, owns compaction, and replays provider checkpoints |
| Control UI | The web-based dashboard for interacting with the assistant and managing the gateway |
| Crabbox | Remote validation infrastructure for CI testing across platforms |
| Doctor | The `openclaw doctor` command that diagnoses and fixes configuration issues |
| Dreaming | The background memory consolidation system in `memory-core` that promotes strong short-term signals into durable memory through light, deep, and REM phases |
| Extension | A plugin package under `extensions/` that adds functionality (channels, providers, tools) |
| Gateway | The core server process that handles HTTP/WebSocket connections, auth, and message routing |
| Logbook | The bundled plugin that turns periodic screen snapshots from a paired node into a timestamped work journal, standup notes, and day recall |
| Managed Worktree | An OpenClaw-owned git branch and checkout for a task, snapshotted before removal and recorded in the shared state database |
| Manifest | Plugin metadata file describing capabilities, dependencies, and configuration |
| Memory | The durable store of curated, episodic, and prospective knowledge, owned by the selected memory plugin |
| Memory Index | The SQLite index of memory chunks and their embeddings that backs recall and search |
| Onboard | The CLI setup wizard that guides first-time configuration |
| Plugin | Synonym for extension; a self-contained package installable via the plugin system |
| Project | A registered or cloned repository that groups sessions and the worktrees made for them |
| Session | A conversation between a user and an agent, persisted across messages |
| Session Card | The per-session progress summary that a user or agent updates with Markdown and checklist steps |
| Session Placement | The decision and durable record of where a session runs, from the local Gateway to a remote worker environment |
| Standing Intent | An event-conditioned instruction that fires when a trigger appears, stored as prospective memory in the owning agent's database |
| Subagent | A child agent spawned by the parent agent to handle a subtask |
| Team Report | A daily, weekly, or monthly report of GitHub organization activity and optional Discord discussion |
| Tool | A capability the agent can invoke (bash, file I/O, web search, code execution, etc.) |
| Worker Turn | One agent turn executed on a remote node worker, claimed by a single owner and recorded in `node_worker_turns` |
| Worktree | An isolated git checkout used for a task, either managed by OpenClaw or created by hand |

## Technical Terms

| Term | Definition |
|---|---|
| A2UI | Agent-to-UI protocol for dynamic agent-driven interfaces |
| ACP | Agent Client Protocol for agent-to-agent, agent-to-editor, and agent-to-gateway communication |
| Auth Profile | A named set of credentials for a provider (API keys, OAuth tokens) |
| Canvas | Agent-driven visual workspace rendered in the Control UI for rich interactive content |
| ClawSweeper | Automated issue/PR triage and maintenance bot for the OpenClaw repository |
| Compactions | The number of times a session's context has been summarized, reported in `/status` |
| DM Policy | Direct Message pairing policy controlling who can message the assistant |
| Env Vars | Environment variables used for configuration (OPENAI_API_KEY, etc.) |
| Gateway Protocol | Custom WebSocket/HTTP RPC protocol for gateway-to-node communication |
| Kysely | The SQL query builder used for database access on both the SQLite and PostgreSQL engines |
| LSP | Language Server Protocol used for code-aware agent interactions |
| MCP | Model Context Protocol, a standard for tool and resource provisioning to AI models |
| Model Catalog | The registry of available AI models and their capabilities |
| Placement Generation | The monotonic counter that fences a session placement transition, so a replaced placement can no longer act |
| Plugin SDK | The `@openclaw/plugin-sdk` package for building extensions |
| Provider | An AI model provider (OpenAI, Anthropic, Google, etc.) |
| Provider Registry | The plugin registry index that collects and indexes provider, tool, and route contributions from loaded plugins |
| QA Lab | Internal testing framework using YAML-based scenario packs under `qa/scenarios` for regression and behavior testing |
| Sandbox | Execution isolation mode for agent tools (configurable as main, non-main, or off) |
| SecretRef | A reference to a secret held by a provider (env, file, exec, or store) that the Gateway resolves at the point of use |
| Session Key | The stable, agent-scoped identifier the Gateway uses to route, store, and reconcile a session |
| Slot | A mutually exclusive plugin selection, such as `plugins.slots.memory` or `plugins.slots.contextEngine`, that picks exactly one plugin for a role |
| Solid | The reactive UI library used for the Control UI and its plugin views (Solid 2) |
| Spawn Broker | The process layer that owns child process creation, cleanup, and diagnostics for command execution |
| State Event Stream | The append-only log of durable session state changes in `session_state_events`, capped by a per-session head in `session_state_heads` |
| Talk | Voice conversation runtime supporting full-duplex audio sessions |
| Team deployment | One shared Gateway configured for a whole team (shared sessions, roles, workspace chat); same product as personal setup, not a separate edition |
| Telemetry check | Daily version-check request plus opt-in anonymous feature statistics, controlled by `telemetry.enabled` and `update.checkOnStart` |
| Trajectory | Session recording capturing agent actions for replay and debugging |
| Transcript | The persisted record of a conversation, including tool calls and results |
| Workboard Contract | The shared status, priority, and event vocabulary that the Workboard plugin and its database port agree on (`packages/workboard-contract`) |
| Worker Launch Descriptor | The description of a worker process to launch, including its bundle, environment, and tool surface |
| Worker Task Pool | The pool of database worker threads that run storage operations off the main process |
| Zod | The schema validation library used for configuration validation |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| A2UI | Agent-to-UI |
| ACP | Agent Client Protocol |
| ADR | Architecture Decision Record |
| CI | Continuous Integration |
| CLI | Command-Line Interface |
| E2E | End-to-End (testing) |
| ESM | ECMAScript Modules |
| FR | Functional Requirement |
| HMAC | Hash-based Message Authentication Code |
| JSON | JavaScript Object Notation |
| LSP | Language Server Protocol |
| MCP | Model Context Protocol |
| NFR | Non-Functional Requirement |
| OAuth | Open Authorization |
| OTel | OpenTelemetry |
| OTLP | OpenTelemetry Protocol |
| PR | Pull Request |
| R2 | Cloudflare R2 object storage |
| RBAC | Role-Based Access Control |
| RPC | Remote Procedure Call |
| RSS | Resident Set Size |
| SARIF | Static Analysis Results Interchange Format |
| SDK | Software Development Kit |
| SLO | Service Level Objective |
| SQL | Structured Query Language |
| SQLite | Embedded SQL database engine |
| SSH | Secure Shell |
| SSO | Single Sign-On |
| TLS | Transport Layer Security |
| TUI | Terminal User Interface |
| UI | User Interface |
| URI | Uniform Resource Identifier |
| WASM | WebAssembly |
| WS | WebSocket |
