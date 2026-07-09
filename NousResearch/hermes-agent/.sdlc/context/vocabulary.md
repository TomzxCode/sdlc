# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Agent | The AI runtime (AIAgent class) that drives conversation, tool calling, and memory |
| Skill | A markdown document (SKILL.md) that guides the agent on how to perform a specific task or workflow |
| Plugin | A Python package that extends the agent via hooks, tools, CLI subcommands, or provider profiles |
| Toolset | A named grouping of tools that can be enabled/disabled per platform (e.g., hermes-telegram, web, browser) |
| Profile | An isolated agent instance with its own config, credentials, skills, and sessions, stored under ~/.hermes/profiles/ |
| Gateway | The asyncio-based service that manages messaging platform adapters and routes messages to the agent core |
| Session | A single conversation history stored in SQLite with FTS5 search |
| Skill lifecycle | The curator system that tracks agent-created skill usage and auto-archives stale skills |
| Prompt cache | A cached system prompt reused across conversation turns — invalidating it mid-conversation is costly |

## Technical Terms

| Term | Definition |
|---|---|
| MCP | Model Context Protocol — an open protocol for connecting LLMs with external tools and data sources |
| ACP | Agent Communication Protocol — a protocol for agent-to-editor integration (VS Code, Zed, JetBrains) |
| FTS5 | Full-Text Search version 5 — SQLite extension for full-text search across session history |
| JSON-RPC | A remote procedure call protocol encoded in JSON, used between the TUI frontend and Python backend |
| Ink | A React renderer for terminals, used for the TUI |
| Prompt_toolkit | A Python library for building interactive command-line applications, used by the classic CLI |
| MoA | Mixture of Agents — running a prompt through an ensemble of models |
| Footprint Ladder | The ranked hierarchy for where to add new capability: extend code > CLI + skill > service-gated tool > plugin > MCP server > new core tool (last resort) |
| check_fn | A callable on a tool registration that gates tool availability based on prerequisites (e.g., API key presence) |
| HERMES_HOME | The base directory for an agent instance's config, state, skills, logs, etc. (profile-aware) |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| MCP | Model Context Protocol |
| ACP | Agent Communication Protocol |
| FTS | Full-Text Search |
| TUI | Terminal User Interface |
| CLI | Command-Line Interface |
| STT | Speech-to-Text |
| TTS | Text-to-Speech |
| MoA | Mixture of Agents |
| CDP | Chrome DevTools Protocol |
| ABC | Abstract Base Class |
| IDE | Integrated Development Environment |
| VPS | Virtual Private Server |
| PTY | Pseudo-terminal |
| SPA | Single-Page Application |