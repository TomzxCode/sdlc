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
| Provider | An AI model provider (OpenAI, Anthropic, Google, etc.) |
| Model Catalog | The registry of available AI models and their capabilities |
| Auth Profile | A named set of credentials for a provider (API keys, OAuth tokens) |
| Plugin SDK | The `@openclaw/plugin-sdk` package for building extensions |
| Gateway Protocol | Custom WebSocket/HTTP RPC protocol for gateway-to-node communication |
| Facilitator | A pattern for delegating work to subagents |
| MCP | Model Context Protocol — a standard for tool and resource provisioning |
| LSP | Language Server Protocol — used for code-aware agent interactions |
| Transcript | The persisted record of a conversation, including tool calls and results |
| Trajectory | A session recording that captures agent actions for replay/debugging |
| Env Vars | Environment variables used for configuration (OPENAI_API_KEY, etc.) |
| Kysely | The SQLite query builder used for database access |
| Zod | The schema validation library used for configuration validation |
| Lit | The web component library used for the Control UI |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ACP | Agent Content Protocol |
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
