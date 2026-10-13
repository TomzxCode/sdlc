<!-- session_link: http://localhost:10000/?session=ses_sync_sdlc_20261013 -->
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
| UC-1 | Get coding work done with an AI agent in the terminal | Developer | Starts a TUI, REPL, or single-shot `run` session against the local daemon, which runs the agent turn loop with 30+ tools through the selected provider. |
| UC-2 | Use existing LLM subscriptions instead of a dedicated API key | Developer | Authenticates once via `jcode login` (Claude Max, ChatGPT Pro, Gemini, Copilot device flow, Azure Entra ID, or API keys) and routes turns across 40+ providers (FEAT-p1). |
| UC-3 | Keep long-running work going while away | Developer | Schedules ambient background work, overnight processing, and background tasks on the always-on daemon, then checks results on return (FEAT-p6). |
| UC-4 | Split large work across coordinated agents | Developer | Builds a plan DAG and delegates to swarm workers with comm channels, tracking progress in the session (FEAT-p3). |
| UC-5 | Carry preferences and decisions across sessions | Developer | Stores memories in the local graph (ONNX embeddings) with recall, injection, and consolidation, plus session search (FEAT-p2). |
| UC-6 | Pick up where a previous session left off | Developer | Persists sessions as JSON snapshots plus JSONL journals under `~/.jcode/sessions`, and resumes, replays, or imports them including foreign formats (FEAT-p5). |
| UC-7 | Stay productive in very large sessions | Developer | Compacts accumulated context (and the KV cache) inside the turn loop when a session grows too large (FEAT-p10). |
| UC-8 | Drive the agent from companion surfaces | Developer | Pairs the iOS app or desktop panels through the versioned harness API and SDKs over the `api-bridge` (FEAT-p7). |
| UC-9 | Install once and stay current with minimal friction | Developer | Installs via `jcode.sh/install` or `install.ps1`, then auto-updates in the background with hot reload that preserves sessions (FEAT-p9). |
| UC-10 | Understand product health without compromising privacy | Maintainer | Reads opt-out telemetry funnels (install, auth, onboarding, session, turn, discovery, todo, transcript program) from the D1 pipeline documented in `TELEMETRY.md` (FEAT-p8). |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| — | No evidenced wanted goals at this time | — | New goals are added here only when the codebase or a linked issue, feature, or roadmap item gives evidence. | — |

## Out of scope

- A hosted or managed cloud agent service (the local daemon is the product).
- Model training or fine-tuning.
- A non-terminal UI as the primary interface (desktop and iOS are companions).
