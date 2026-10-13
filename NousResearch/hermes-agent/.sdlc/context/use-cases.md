<!-- session_link: http://localhost:10000/?session=ses_ecc2d9293ffep2FRMT4uWHsaeb -->
# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Converse with a persistent personal assistant from any surface | Individual user | The same agent core runs across CLI, TUI, Electron desktop, web dashboard, and a messaging gateway covering Telegram, Discord, Slack, Signal, WhatsApp, and about 20 more platforms, with cross-platform conversation continuity and voice memo transcription. |
| UC-2 | Recall past conversations and accumulated knowledge across sessions | Individual user | Full-text FTS5 session search with LLM summarization, agent-curated memory with periodic nudges, autonomous skill creation and self-improvement, and Honcho dialectic user modeling preserve context between sessions. |
| UC-3 | Execute real terminal and browser actions through the agent | Power user | Seven terminal backends (local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox) plus browser automation let the agent run commands, manipulate files, and drive the web on the user's behalf. |
| UC-4 | Automate recurring work on a schedule | Individual user | The built-in cron scheduler accepts natural-language schedules and delivers results unattended to any messaging platform, covering daily reports, nightly backups, and weekly audits. |
| UC-5 | Delegate parallel work to isolated subagents | Power user | The agent spawns isolated subagents for parallel workstreams and exposes RPC-callable Python scripts that collapse multi-step pipelines into zero-context-cost turns. |
| UC-6 | Coordinate distributed work across agents and people | Team operator | Multi-agent kanban task boards provide shared work queues reachable from messaging platforms for assigning, tracking, and completing tasks. |
| UC-7 | Extend the agent without modifying the core | Plugin and skill developer | Plugins (tools, memory providers, model providers, platform adapters), skills following the agentskills.io open standard, and MCP client support for external tool servers add capability at the edges. |
| UC-8 | Self-host the agent and switch models without lock-in | Self-hoster | A single install runs on a VPS, GPU cluster, or hibernating serverless backends, works with any OpenAI-compatible provider via `hermes model`, isolates instances via multi-profile support, and keeps secrets in `.env` with behavior in `config.yaml`. |
| UC-9 | Generate training trajectories for tool-calling models | Researcher | Batch trajectory generation with trajectory compression produces reusable traces for training the next generation of tool-calling models. |
| UC-10 | Customize the interactive experience | Individual user | The data-driven skin and theme system, slash-command autocomplete, multiline editing, conversation history, interrupt-and-redirect, and streaming tool output adapt the CLI and TUI to user preference. |

## Wanted

No additional actor goals with supporting evidence in code, issues, or roadmap were found during this pass.

## Out of scope

- Outbound telemetry or usage attribution without explicit user opt-in.
- New `HERMES_*` environment variables for non-secret configuration (behavioral settings go in `config.yaml`).
- New core model tools when the capability can be expressed as a CLI command + skill, service-gated tool, plugin, or MCP server.
- Third-party product plugins integrated into the core tree (observability backends, vendor SaaS, analytics dashboards must ship as standalone plugin repos).
- New in-tree memory providers (the set of built-in providers under `plugins/memory/` is closed; new ones must ship as standalone repos).
