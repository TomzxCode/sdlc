<!-- session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019 -->
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
| UC-1 | Get coding work done with an AI agent in the terminal | Developer | Starts a TUI, REPL, or single-shot `run` session against the local daemon, which runs the agent turn loop with 30+ tools through the selected provider (FEAT-p4). |
| UC-2 | Use existing LLM subscriptions instead of a dedicated API key | Developer | Authenticates once via `jcode login` (Claude Max, ChatGPT Pro, Gemini, Copilot device flow, Azure Entra ID, or API keys) and routes turns across 50+ providers (FEAT-p1). |
| UC-3 | Keep long-running work going while away | Developer | Schedules ambient background work, background tasks, and supervised overnight runs on the always-on daemon, then checks results on return (FEAT-p6). |
| UC-4 | Split large work across coordinated agents | Developer | Builds a plan DAG and delegates to swarm workers with comm channels, tracking progress in the session (FEAT-p3). |
| UC-5 | Carry preferences and decisions across sessions | Developer | Stores memories in the local graph under `~/.jcode/memory` and recalls them through Jev relevance decisions, with memory injection and ambient consolidation, plus session search (FEAT-p2). |
| UC-6 | Pick up where a previous session left off | Developer | Persists sessions as JSON snapshots plus JSONL journals under `~/.jcode/sessions`, and resumes, replays, or imports them including foreign formats (FEAT-p5). |
| UC-7 | Stay productive in very large sessions | Developer | Compacts accumulated context (and the KV cache) inside the turn loop when a session grows too large (FEAT-p10). |
| UC-8 | Drive the agent from companion surfaces | Developer | Pairs the iOS app over the server's WebSocket gateway, or drives desktop panels through the server protocol, while embedding programs use the versioned harness API and its Rust and TypeScript SDKs over the `api-bridge` (FEAT-p7). |
| UC-9 | Install once and stay current with minimal friction | Developer | Installs via `jcode.sh/install` or `install.ps1`, then auto-updates in the background with hot reload that preserves sessions (FEAT-p9). |
| UC-10 | Understand product health without compromising privacy | Maintainer | Reads opt-out telemetry funnels (install, auth, onboarding, session, turn, discovery, todo, transcript program) from the D1 pipeline documented in `TELEMETRY.md` (FEAT-p8). |
| UC-11 | Let the agent operate a real browser and hand off a whole web task | Developer | Calls the `browser` tool, whose default path hands the task to the fast browser agent in an explicit tab through an observation, action, and results loop (FEAT-p11). |
| UC-12 | Extend the agent with external tools and data through MCP servers | Developer | Configures stdio, Streamable HTTP, or HTTP and SSE servers, signs into remote servers with OAuth, and lets the agent call their tools (FEAT-p11). |
| UC-13 | Have the agent extend and repair jcode itself | Developer | Enters self-dev mode, where the agent edits, builds, and tests jcode's own source, then hot-reloads the new binary into the running server and continues the session (FEAT-p11). |
| UC-14 | Work on a remote machine from a local terminal | Developer | Runs `jcode --ssh <host>` to keep the TUI local while the workspace, tools, credentials, and agent execution stay on the SSH host (FEAT-p11). |
| UC-15 | Continue a session on a cloud host and bring it back | Developer | Runs `jcode cloud move` to hand a live session (transcript, git state, environment notes) to a cloud host, works there, then merges the cloud snapshot back into the local checkout (FEAT-p20). |
| UC-16 | Use metered hosted models with a spending limit | Developer | Signs in with `jcode account login`, then picks a monthly spending limit in `/hosted` and watches usage and billing status (FEAT-p21). |
| UC-17 | Drive the agent by voice | Developer | Uses `jcode dictate` or `jcode transcript` to turn speech into a prompt in the focused TUI, with the desktop companion providing the global microphone listener (FEAT-p12). |
| UC-18 | Extend the agent with reusable project procedures | Developer | Installs and manages skills that give the agent repeatable procedures for a repository (FEAT-p11). |
| UC-19 | Keep the agent from destroying the machine | Developer | Relies on the command-risk gate that classifies shell commands by blast radius and forces a justification for destructive ones (FEAT-p14). |
| UC-20 | Orchestrate many tool calls in one step | Developer | Lets the model write a short JavaScript program that drives harness tools inside a sandbox, so only the result reaches the transcript (FEAT-p17). |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| UC-21 | Sync worktrees and build state across devices | Developer | Carries a working tree and its build artifacts between the desktop and the paired mobile client without manual transfer. | `docs/proposals/CROSS_DEVICE_WORKTREE_SYNC.md` (Proposed, design only) |

## Out of scope

- A first-party hosted account, billing, and hosted-model router (already shipped through `jcode account` and `/hosted`).
- A fully managed per-user cloud agent host (planned in `docs/JCODE_CLOUD_AWS.md` but not deployed; self-hosted use keeps the local daemon as the runtime).
- Model training or fine-tuning.
- A non-terminal UI as the primary interface (desktop and iOS are companions).
