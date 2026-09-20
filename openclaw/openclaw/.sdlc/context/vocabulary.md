# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Channel | A messaging platform integration (WhatsApp, Telegram, Discord, etc.) that the assistant communicates through |
| Gateway | The core server process that handles HTTP/WebSocket connections, auth, and message routing |
| Agent | The AI assistant instance that processes conversations and executes tools |
| Session | A conversation between a user and an agent, persisted across messages |
| Tool | A capability the agent can invoke (bash, file I/O, web search, code execution, etc.) |
| Compaction | The process of summarizing old conversation turns to manage context window limits |
| Subagent | A child agent spawned by the parent agent to handle a subtask |
| Extension | A plugin package under `extensions/` that adds functionality (channels, providers, tools) |
| Plugin | Synonym for extension; a self-contained package installable via the plugin system |
| Manifest | Plugin metadata file describing capabilities, dependencies, and configuration |
| Control UI | The web-based dashboard for interacting with the assistant and managing the gateway |
| Onboard | The CLI setup wizard that guides first-time configuration |
| Doctor | The `openclaw doctor` command that diagnoses and fixes configuration issues |
| ClawHub | The community plugin marketplace at https://clawhub.ai |
| Crabbox | Remote validation infrastructure for CI testing across platforms |

## Technical Terms

| Term | Definition |
|---|---|
| A2UI | Agent-to-UI protocol for dynamic agent-driven interfaces |
| ACP | Agent Client Protocol — a protocol for agent-to-agent and agent-to-gateway communication |
| Auth Profile | A named set of credentials for a provider (API keys, OAuth tokens) |
| Canvas | Agent-driven visual workspace rendered in the Control UI for rich interactive content |
| ClawSweeper | Automated issue/PR triage and maintenance bot for the OpenClaw repository |
| DM Policy | Direct Message pairing policy controlling who can message the assistant |
| Env Vars | Environment variables used for configuration (OPENAI_API_KEY, etc.) |
| Facilitator | A pattern for delegating work to subagents |
| Gateway Protocol | Custom WebSocket/HTTP RPC protocol for gateway-to-node communication |
| Kysely | The SQLite query builder used for database access |
| Lit | The web component library used for the Control UI |
| LSP | Language Server Protocol — used for code-aware agent interactions |
| MCP | Model Context Protocol — a standard for tool and resource provisioning to AI models |
| Model Catalog | The registry of available AI models and their capabilities |
| Plugin SDK | The `@openclaw/plugin-sdk` package for building extensions |
| Provider | An AI model provider (OpenAI, Anthropic, Google, etc.) |
| QA Lab | Internal testing framework using YAML-based scenario packs for regression and behavior testing |
| Sandbox | Execution isolation mode for agent tools (configurable as main, non-main, or off) |
| Talk | Voice conversation runtime supporting full-duplex audio sessions |
| Trajectory | Session recording capturing agent actions for replay and debugging |
| Transcript | The persisted record of a conversation, including tool calls and results |
| Zod | The schema validation library used for configuration validation |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ACP | Agent Client Protocol |
| ADR | Architecture Decision Record |
| CI | Continuous Integration |
| CLI | Command-Line Interface |
| E2E | End-to-End (testing) |
| ESM | ECMAScript Modules |
| FR | Functional Requirement |
| JSON | JavaScript Object Notation |
| LSP | Language Server Protocol |
| MCP | Model Context Protocol |
| NFR | Non-Functional Requirement |
| OAuth | Open Authorization |
| PR | Pull Request |
| RBAC | Role-Based Access Control |
| RPC | Remote Procedure Call |
| SDK | Software Development Kit |
| SQL | Structured Query Language |
| SQLite | Embedded SQL database engine |
| SSO | Single Sign-On |
| TUI | Terminal User Interface |
| UI | User Interface |
| WS | WebSocket |
