# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Agent | The AI runtime (AIAgent class) that drives conversation, tool calling, and memory |
| Board | The hard isolation boundary of the kanban system — workers are spawned with a pinned board and cannot see others |
| Bot Mode | The desktop roster where each bot is a profile with one canonical hidden forever-chat titled Bot Chat |
| Gateway | The asyncio-based service that manages messaging platform adapters and routes messages to the agent core |
| Kanban | A durable multi-agent work queue (SQLite-backed board) for distributing tasks across profiles/workers |
| Plugin | A Python package that extends the agent via hooks, tools, CLI subcommands, or provider profiles |
| Profile | An isolated agent instance with its own config, credentials, skills, and sessions, stored under ~/.hermes/profiles/ |
| Prompt cache | A cached system prompt reused across conversation turns — invalidating it mid-conversation is costly |
| Session | A single conversation history stored in SQLite with FTS5 search |
| Skill | A markdown document (SKILL.md) that guides the agent on how to perform a specific task or workflow |
| Skill lifecycle | The curator system that tracks agent-created skill usage and auto-archives stale skills |
| Toolset | A named grouping of tools that can be enabled/disabled per platform (e.g., hermes-telegram, web, browser) |
| Trajectory | A saved record of an agent run (messages, tool calls, and results) used for batch data generation and training tool-calling models |

## Technical Terms

| Term | Definition |
|---|---|
| ACP | Agent Communication Protocol — a protocol for agent-to-editor integration (VS Code, Zed, JetBrains) |
| check_fn | A callable on a tool registration that gates tool availability based on prerequisites (e.g., API key presence) |
| Footprint Ladder | The ranked hierarchy for where to add new capability: extend code > CLI + skill > service-gated tool > plugin > MCP server > new core tool (last resort) |
| FTS5 | Full-Text Search version 5 — SQLite extension for full-text search across session history |
| HERMES_DESKTOP | An environment marker meaning this backend was spawned by the Electron desktop app, not that a GUI session is watching |
| HERMES_HOME | The base directory for an agent instance's config, state, skills, logs, etc. (profile-aware) |
| Ink | A React renderer for terminals, used for the TUI |
| JSON-RPC | A remote procedure call protocol encoded in JSON, used between the TUI frontend and Python backend |
| MCP | Model Context Protocol — an open protocol for connecting LLMs with external tools and data sources |
| MoA | Mixture of Agents — running a prompt through an ensemble of models |
| NeMo Relay / Langfuse | Observability backends consuming the observer-hook contract for traces and metrics |
| Observer hooks | Backend-neutral telemetry callbacks (pre/post API request, tool call) reconstructing execution without changing runtime behavior |
| Prompt_toolkit | A Python library for building interactive command-line applications, used by the classic CLI |
| SDLC | The .sdlc/ lifecycle system tracking features, requirements, specifications, decisions, and progress |
| wine2e | The on-demand live Windows E2E CI lane that runs windows-venv-e2e.yml only on pushes to wine2e/** branches |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ABC | Abstract Base Class |
| ACP | Agent Communication Protocol |
| CDP | Chrome DevTools Protocol |
| CLI | Command-Line Interface |
| FTS | Full-Text Search |
| IDE | Integrated Development Environment |
| MCP | Model Context Protocol |
| MoA | Mixture of Agents |
| PTY | Pseudo-terminal |
| SDLC | Software Development Life Cycle |
| SPA | Single-Page Application |
| STT | Speech-to-Text |
| TTS | Text-to-Speech |
| TUI | Terminal User Interface |
| VPS | Virtual Private Server |
