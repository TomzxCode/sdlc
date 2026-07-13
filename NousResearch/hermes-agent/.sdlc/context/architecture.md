# Architecture

## System Overview

```
User ──┐
       ├── CLI (prompt_toolkit + Rich) ───┐
       ├── TUI (Ink/React, JSON-RPC stdio)─┤
       ├── Gateway (asyncio + adapters) ───┤
       ├── Desktop (Electron + React) ─────┤
       └── API Server (HTTP) ──────────────┘
                                              │
                                              v
                               ┌──────────────────────────┐
                               │     AIAgent             │
                               │  (run_agent.py)         │
                               │  conversation loop      │
                               │  tool-calling loop      │
                               │  budget/iter tracking   │
                               └──────────┬───────────────┘
                                          │
                      ┌───────────────────┼───────────────────┐
                      v                   v                   v
              ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
              │ Tool Registry │  │ Model Client │  │ Provider     │
              │ (tools/*.py)  │  │ (OpenAI API) │  │ Adapters     │
              │ + MCP servers │  │              │  │ (Anthropic,  │
              └──────────────┘  └──────────────┘  │ Gemini, ...) │
                                                  └──────────────┘
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| AIAgent (run_agent.py) | Core conversation loop — manages chat completions API calls, tool-calling iterations, interrupt handling, budget tracking, subagent spawning | Python, OpenAI SDK |
| HermesCLI (cli.py) | Interactive CLI orchestrator with prompt_toolkit REPL, Rich panels, skin engine, slash command dispatch (~70 commands) | Python, prompt_toolkit, Rich |
| Tool Registry (tools/registry.py) | Central registry for tool schemas and handlers; auto-discovers tools from tools/*.py via AST scan | Python |
| Tool Implementations (tools/*.py) | ~93 tool modules — terminal, file, web, browser, vision, delegation, cron, kanban, etc. Each self-registers at import time | Python |
| Toolset Definitions (toolsets.py) | Composable tool groupings for platforms and scenarios (hermes-cli, hermes-telegram, web, browser, file, etc.) | Python |
| Model Tools (model_tools.py) | Orchestration layer — tool discovery, schema collection, function call dispatch, gating, MCP integration, approval gates | Python |
| Gateway Runner (gateway/run.py) | Async runtime for all messaging platforms — session lifecycle, stream dispatch, approval flow, slash command dispatch | Python, asyncio |
| Platform Adapters (gateway/platforms/) | Adapter per messaging platform (Telegram, Discord, Slack, Signal, WhatsApp, email, SMS, Matrix, Mattermost, etc.) | Python |
| TUI Frontend (ui-tui/) | Ink (React) terminal UI with composer, transcript, session picker, slash commands | TypeScript, Ink, React |
| TUI Gateway (tui_gateway/) | Python JSON-RPC backend over stdio serving the TUI frontend | Python |
| Electron Desktop (apps/desktop/) | Standalone Electron desktop app with its own React composer and slash-command pipeline | TypeScript, Electron, React, nanostores |
| Plugin Manager (hermes_cli/plugins.py) | Discovers and manages plugins (hooks, tools, CLI subcommands) from ~/.hermes/plugins/ and pip entry points | Python |
| Memory Manager (agent/memory_manager.py) | Orchestrates pluggable memory backends via MemoryProvider ABC | Python |
| Cron Scheduler (cron/scheduler.py) | Tick loop for scheduled jobs — duration, cron expressions, ISO timestamps | Python |
| Curator (agent/curator.py) | Background skill lifecycle maintenance — tracks usage, auto-archives stale agent-created skills | Python |
| Configuration System (hermes_cli/config.py) | config.yaml with deep-merge from DEFAULT_CONFIG, profile-aware paths, .env for secrets only | Python |
| Session Store (hermes_state.py) | SQLite database with FTS5 full-text search for conversation history | Python, SQLite |

## Data Flow

1. **Message arrives** via any surface (CLI, messaging platform, TUI, desktop, API server)
2. **System prompt is built** from config, skills, memory, personality — built once per session for prompt caching stability
3. **Conversation loop** in AIAgent.run_conversation():
   - Sends messages (system + history + user) with tool schemas to LLM provider via OpenAI-compatible API
   - If response has tool calls: dispatches each to handle_function_call() via the registry, appends tool results, repeats
   - If response is text: returns it as the final response
4. **Tool dispatch** routes through model_tools.py → registry.dispatch() → handler (each returns JSON string)
5. **Agent-level interception** in run_agent.py handles memory and todo calls before reaching registry
6. **Response delivered** back through the originating surface (CLI prints it, gateway sends platform message, TUI streams delta)
7. **Post-turn** — memory providers sync_turn(), title generation fires, trajectory may be saved

## Infrastructure

- **Testing:** pytest with hermetic runner (scripts/run_tests.sh). ~17k tests across ~900 files. Integration tests excluded by default (marker-gated). Subprocess-per-test-file isolation. Per-test temp HERMES_HOME.
- **Packaging:** uv for dependency management, exact pinning with upper bounds. Docker images, pip install, managed install via hermes update.
- **Logging:** profile-aware structured logging to agent.log, errors.log, gateway.log under ~/.hermes/logs/.
- **CI/CD:** Scripts for CI parity testing, release automation.
- **Deployment:** Multi-backend terminal environments (local, Docker, SSH, Modal, Daytona, Singularity). Gateway supports restart, scale-to-zero, drain control.

## Architecture Decisions

Key decisions are documented in the AGENTS.md file and the convention is to avoid adding new core tools when capability can live at the edges. Formal ADRs live under `.sdlc/knowledge/decisions/` once created.