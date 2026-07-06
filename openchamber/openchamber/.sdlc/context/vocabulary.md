# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| OpenCode | The AI coding assistant CLI that OpenChamber wraps with a GUI. It handles LLM interactions, tool execution, and session management on the backend. |
| OpenChamber | This project; a multi-runtime GUI client for OpenCode providing web, desktop (Electron), and VS Code extension interfaces. |
| Session | A conversation with an AI agent in OpenCode, containing messages, tool calls, file edits, and permission requests. Sessions are scoped to a git repository directory. |
| Multi-run | Running multiple AI agents in parallel from a single prompt, each in an isolated git worktree. Results are collected and presented side by side. |
| Agent | An AI model configuration with specific provider, model, system prompt, skills, and tool access. Agents execute within sessions. |
| Skills | Reusable automation packages that extend agent behavior, defining tools, prompts, and workflows. Skills are installed from a registry or local sources. |
| Worktree | A git worktree providing an isolated working directory for multi-run sessions, preventing file conflicts between concurrent agent operations. |
| Tunnel | A Cloudflare tunnel providing secure remote access to a local OpenChamber instance without exposing ports or configuring DNS. |
| Mini Chat | A compact Electron window for focused conversations without the full workspace UI, supporting quick prompts and responses. |
| Global Hub | Shared upstream SSE hub that fans out OpenCode events to server-side and browser subscribers. It holds a bounded replay buffer keyed by SSE event ID. |
| Event Pipeline | Client-side SSE/WebSocket processing layer that transforms raw events into store-friendly patches and dispatches them to Zustand stores. |
| Upstream Reader | Reusable SSE reader with event-id tracking, stall detection, and automatic reconnect. When an upstream stream stalls, it aborts the fetch and reconnects with `Last-Event-ID`. |
| Directory Ws Bridge | Per-directory WebSocket bridge that owns one scoped upstream SSE reader per connection, since directory event streams are scoped to a repository. |
| Global Ws Bridge | Browser-facing global WebSocket bridge that subscribes clients to the global hub and fans out events. |
| Bootstrap | The initial data-loading phase on app startup where the UI fetches existing sessions, permissions, and questions from the server. |
| Sync Layer | Client-side infrastructure for real-time state synchronization between the server and UI via SSE/WebSocket, including reconnect logic, coalescing, and store dispatch. |
| Provider | An AI model provider (OpenAI, Anthropic, Google, etc.) configured with API keys and base URLs. OpenChamber proxies requests through OpenCode. |
| Permission | A security gate where the AI requests user approval before executing an operation (file write, command run, etc.). Permissions can be approved once or permanently. |
| Quota | Usage tracking per provider, monitoring token counts, costs, and rate limits. Quota providers are pluggable for different backends. |
| Plan View | A structured UI view that visualizes the AI's step-by-step plan for completing a task, showing files to modify, commands to run, and their dependencies. |
| Context Panel | A sidebar panel showing the current session's context files, directory structure, and relevant information the AI is aware of. |
| Reasoning Display | The UI presentation of an AI model's chain-of-thought or reasoning tokens during generation, shown in a collapsible section within messages. |
| Response Style Preset | Reusable configurations for how the AI formats responses (concise, detailed, code-first, etc.), applied at the session or agent level. |
| Preview Browser | An embedded browser view for previewing locally running web applications during development, accessible from within OpenChamber. |
| Session Folders | A grouping mechanism for organizing sessions into folder hierarchies, similar to chat folder organization in messaging apps. |
| Session Timeline | A chronological view of session history supporting undo/redo of actions and browsing past states of a session. |
| Question Cards | Structured UI cards that present AI-generated questions to the user during a session, supporting multi-choice and free-text answers. |
| Inline Comments/Annotations | User annotations on specific lines of files within session messages, used for review and collaboration. |
| Text Selection Context Menu | A context menu that appears on text selection in messages and editors, providing actions like copy, explain, refactor, or fix. |
| Git Identity Profile | A named git author configuration (name + email) that can be switched between projects or sessions, stored as reusable profiles. |
| Git Worktree Management | UI for creating, switching, and removing git worktrees as isolated environments for parallel agent runs. |
| External Apps | Integration points for opening files, directories, or URLs in external applications (editor, browser, terminal) from within OpenChamber. |
| Onboarding/Auth | The first-run experience including provider API key setup, code signing, and initial configuration wizard. |
| PWA | Progressive Web App; the browser-based runtime that supports offline access, installation, and push notifications. |
| Skills Catalog | A registry of available skills that users can browse, install, and configure to extend agent capabilities. |
| Project Management | Tools for tracking issues, todo lists, and project status within OpenChamber, integrating with Linear and other PM systems. |
| Snippets | Reusable text templates that can be expanded in the chat input via autocomplete, supporting global and project-level scopes with aliases. |
| Plugins | OpenCode plugin scripts (JS/TS) that extend agent behavior, installable as npm packages or local files with configurable options. |
| Session Assist | Server-side feature that generates a short recap of the agent's last reply and one suggested user follow-up using a small model after a session goes idle. |
| Auto Review | Automated iterative review flow where a reviewer agent examines a session's output, generates findings, and passes them back to the original agent for revision. |
| Capacitor | Cross-platform native runtime for building iOS and Android apps from web code; used by OpenChamber Mobile. |
| AI-Generated Commits/PR | Automatic git commit message generation and pull request creation from session changes, with human review before submission. |
| Docker Self-Hosted | Docker deployment support with Dockerfile and docker-compose.yml for running OpenChamber on a server. |
| MCP | Model Context Protocol integration for connecting AI agents to external tools and data sources through a standardized protocol. |
| Internationalization/i18n | Multi-language support using Lingui, with locale files for English, Polish, Chinese, and other languages. |
| Event Bus | The layered backend-to-frontend communication system using SSE from OpenCode to Express, then WebSocket from Express to the browser. |
| Global Synthetic Events | Server-generated events (not from OpenCode) including openchamber:session-status, openchamber:session-activity, openchamber:notification, and openchamber:heartbeat. |
| Zone | A keyboard navigation region in the settings UI, defining which section or panel receives keyboard focus. Zones are navigated via arrow keys and each zone shows a numbered indicator. |

## Technical Abbreviations

| Term | Definition |
|---|---|
| SSE | Server-Sent Events; HTTP-based push protocol used for streaming session events from OpenCode to the server and from the server to the UI. |
| WS | WebSocket; bidirectional communication protocol used for terminal PTY streams and event bus connections. |
| PWA | Progressive Web App; a web application that can be installed on a device and work offline. |
| PTY | Pseudo-terminal; used for spawning interactive shell sessions in the integrated terminal. |
| HMR | Hot Module Replacement; Vite's development feature for updating modules without full page reload. |
| HOC | Higher-Order Component; a React pattern for component composition. |
| IPC | Inter-Process Communication; used in Electron between main and renderer processes. |
| MCP | Model Context Protocol; a protocol for connecting AI models to external tools and data sources. |
| TTS | Text-to-Speech; converting text responses to audible speech output. |
| STT | Speech-to-Text; converting voice input to text for prompts (local Whisper). |
| CLI | Command-Line Interface; the terminal-based entry point for starting, stopping, and configuring the server. |
| LRU | Least Recently Used; a cache eviction policy used for in-memory caches. |
| TTL | Time-To-Live; a cache expiration policy used to prevent redundant fetches. |

## State Stores

| Term | Definition |
|---|---|
| useSessionStore | Zustand store containing the active session's messages, status, and metadata. Updated frequently during streaming. |
| useGlobalSessionsStore | Zustand store for the sidebar's cold/global session list. Updated infrequently. |
| usePermissionStore | Zustand store tracking pending and resolved permission requests across sessions. |
| useQuestionStore | Zustand store for pending question cards that require user input. |
| useGitStore | Zustand store for git status, branch info, and worktree state for the active directory. |
| useSessionFoldersStore | Zustand store for session folder hierarchy and assignments. |
| useActiveNowStore | Zustand store tracking actively running sessions (those currently streaming or executing). |
| useSettingsStore | Zustand store for user preferences, provider config, theme selection, and app settings. |
| useTerminalStore | Zustand store for terminal session state, output buffers, and connection status. |
| useSkillsStore | Zustand store for installed skills and the skills catalog. |
| useUsageStore | Zustand store for quota usage data per provider. |
| useThemeStore | Zustand store for the active theme and theme configuration. |

## Projects and Packages

| Term | Definition |
|---|---|
| @openchamber/ui | The shared UI component library containing React components, hooks, Zustand stores, theme system, and sync layer. Consumed by all runtimes. |
| @openchamber/web | The web runtime package containing the Express server, API routes, Vite frontend build, and CLI. |
| @openchamber/electron | The Electron desktop shell package. Boots the web server in-process and provides native integrations (menu, dialog, notifications, updater, deep-links). |
| @openchamber/vscode | The VS Code extension package with extension host logic and a sidebar webview. |
| @openchamber/desktop | The legacy Tauri desktop shell (maintenance-only). Spawns the server as a sidecar binary. |
| @openchamber/docs | The documentation website source using MDX. |
