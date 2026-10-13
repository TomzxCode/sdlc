<!-- session_link: http://localhost:10000/?session=ses_sync_sdlc_2026_10_13 -->
# Use Cases

<!--
This file records why actors use the project, so requirements, specifications,
and prioritization can reason about the goals behind a change. An entry is a
reason an actor has for reaching for the project, not an operation the project
exposes: "read a conversation offline" is a use case, "run the cache status
command" is not. Each entry names the actor, the goal, and how the project
serves it today. Keep IDs stable: reuse an existing UC-N for the same goal, and
only add a new one for a genuinely new goal. Put not-yet-built goals under
"Wanted", each with a signal (an issue, feature, or roadmap item). Record
deliberate non-goals under "Out of scope".
-->

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Chat with an AI coding agent | Developer | The developer opens a session and exchanges messages with streaming responses, with undo/redo, forking, and multi-session management (FEAT-0001, FEAT-0017). |
| UC-2 | Manage Git work and GitHub PRs | Developer | The developer commits, branches, views diffs, and opens AI-described PRs without leaving the app (FEAT-0002, FEAT-0005, FEAT-0034). |
| UC-3 | Isolate work in worktrees | Developer | The developer runs sessions and multi-agent runs in isolated git worktrees (FEAT-0016, FEAT-0015). |
| UC-4 | Use an integrated terminal | Developer | The developer runs shell commands in a PTY-backed terminal panel (FEAT-0003). |
| UC-5 | Browse and edit files | Developer | The developer navigates the project tree and edits files with syntax highlighting (FEAT-0004). |
| UC-6 | Review and approve agent actions | Developer | The developer approves permissions, answers agent questions, and controls edit mode (FEAT-0018, FEAT-0019). |
| UC-7 | Search conversation history | Developer | The developer full-text searches past conversations on the server (p11). |
| UC-8 | Preview a running dev server | Developer | The developer previews a local dev server in an embedded browser with console overlay and inspect mode (FEAT-0047). |
| UC-9 | Let the agent act in the browser | Developer | The developer lets the agent perform browser actions through the in-app browser view (p14). |
| UC-10 | Dictate and listen | Developer | The developer dictates messages via streaming speech-to-text and hears responses via TTS (FEAT-0029). |
| UC-11 | Track AI usage and cost | Developer | The developer monitors token usage and quota across providers (FEAT-0031). |
| UC-12 | Organize sessions and projects | Developer | The developer groups sessions in folders, pins them, exports them, and manages multiple projects (FEAT-0032, FEAT-0044, FEAT-0042, FEAT-0035). |
| UC-13 | Automate with scheduled tasks | Developer | The developer schedules prompts that run agents on a cron schedule (FEAT-0040). |
| UC-14 | Drive goals autonomously | Developer | The developer sets a session goal the agent works toward across turns with audit (p5). |
| UC-15 | Review agent output automatically | Developer | The developer runs a reviewer agent that sends findings back for revision (p4). |
| UC-16 | Walk through a diff | Developer | The developer gets an AI-ordered tour of a diff's stops and chapters (p6). |
| UC-17 | Customize the workspace | Developer | The developer themes, fonts, locales, commands, skills, prompts, and response styles (FEAT-0006, FEAT-0046, FEAT-0045, FEAT-0012, FEAT-0013, FEAT-0039, FEAT-0048). |
| UC-18 | Manage agent memory | Developer | The developer views and controls what the agent has learned and kept, per project and globally (p12). |
| UC-19 | Pin project knowledge | Developer | The developer pins notes and plans that the server injects into session prompts (p13, FEAT-0038). |
| UC-20 | Access remotely | Developer | The developer reaches a remote instance via tunnel, SSH host management, or the private E2EE relay (FEAT-0014, FEAT-0037). |
| UC-21 | Work from mobile or VS Code | Developer | The developer uses the Capacitor mobile app, the PWA, or the VS Code extension sidebar (FEAT-0024, FEAT-0021, FEAT-0010). |
| UC-22 | Work on the desktop app | Developer | The developer runs the Electron desktop app with mini chat and native integrations (FEAT-0043, FEAT-0049). |
| UC-23 | Deploy self-hosted | Operator | The operator runs OpenChamber via Docker, systemd, or npm with Caddy TLS (FEAT-0036). |
| UC-24 | Script agent runs | Operator | The operator drives projects, sessions, and tasks via the control-plane CLI and agent tool (p9). |
| UC-25 | Extend with MCP and plugins | Developer | The developer connects MCP servers and manages OpenCode plugins (FEAT-0033, p2). |
| UC-26 | Edit diagrams | Developer | The developer edits DrawIO diagrams in the built-in editor (p7). |
| UC-27 | Manage agent groups | Developer | The developer organizes agents into groups and launches multi-runs from them (p8). |
| UC-28 | See live PR/MR status | Developer | The developer sees live GitHub, GitLab, and Linear item states on sidebar rows and worktree headers (tracked in code under `packages/web/server/lib/tracked-items/`, currently folded into FEAT-0002). |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| UC-29 | Run dev apps in a built-in browser | Developer | A full built-in browser for running dev apps, beyond the current preview browser | project-overview.md Out of scope note (on roadmap) |

## Out of scope

- The OpenCode server itself (separate project at opencode.ai)
