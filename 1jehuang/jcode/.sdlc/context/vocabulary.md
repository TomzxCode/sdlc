# Vocabulary

<!--
Terms within each table are sorted alphabetically by the first column.
-->

## Domain Terms

| Term | Definition |
|---|---|
| Account failover | Automatic retry of a turn on the next pool account when the active one hits a usage limit. |
| Account router | The startup surface that lists saved accounts, cached quotas, and available quota resets. |
| Ambient mode | Proactive background agent (OpenClaw-style) with work cycles, garden/scout tasks, and overnight processing. |
| Applet | An agent-mounted UI instance, persisted per session under `~/.jcode/agent_applets/`. |
| Canary | A session or build used to test new code against real usage. |
| Codemode | Opt-in mode where the model writes a short JavaScript program that orchestrates tool calls instead of issuing them one turn at a time. |
| Comm channel | A message channel between swarm members (direct message, broadcast). |
| Compaction | Reducing accumulated context (and the KV cache) when a session grows too large. |
| Consolidation | Background process that merges and strengthens memories over time. |
| Content block / part | A typed piece of a message (text, reasoning, thinking, tool use, tool result, image, compaction). |
| Custom web search | A user-configured HTTP JSON search engine declared under `[websearch.custom]` in `~/.jcode/config.toml`. |
| Effort / reasoning | The configured reasoning depth for a model. |
| Embedding | A numeric vector representing text, computed locally with an ONNX MiniLM model. |
| Harness API / API bridge | The stable versioned client API (`jcode api-bridge`) and the SDKs that consume it. |
| Hibernation | Evicting an idle session from memory, with transparent wake on the next interaction. |
| Memory graph | The persistent graph of extracted memories, skills, and relationships. |
| Message | A single exchange in a session, carrying a role (User/Assistant) and a list of content blocks. |
| Pairing / gateway | QR-code pairing of the iOS app to the desktop daemon through a gateway. |
| Pinned todo | A todo pinned in the TUI todo list, kept collapsed with the overall progress display. |
| Plan DAG / plan item | The directed acyclic graph of tasks a swarm coordinator builds. |
| Productivity report | A scan of local session transcripts rendered as Markdown plus a shareable PNG dashboard. |
| Provider | A source of model completions (Anthropic, OpenAI, Gemini, Bedrock, OpenRouter, etc.). |
| Recall / injection | Retrieving relevant memories and inserting them into the prompt. |
| Reload | Hot-reloading the server into a new binary without dropping clients or sessions. |
| Restart snapshot | A saved snapshot of sessions and state used to resume after a reboot. |
| Resume target | An external session source that can be resumed (jcode, Claude Code, Codex, Pi, OpenCode, Cursor). |
| Self-dev | Canary self-development mode that runs a freshly built binary on a shared server. |
| Session | A unit of interaction with the agent: a persisted conversation with an id, title, and status. |
| Soft interrupt | Queueing a follow-up message mid-run without discarding the in-flight turn. |
| Sponsored discovery | Catalog-based tool discovery that reports privacy-safe funnel telemetry per discover_tools attempt. |
| Swarm | Multi-agent coordination where a coordinator delegates tasks to worker agents. |
| Tool / tool call / tool result | A capability the agent can invoke; the request and its outcome. |
| Transcript sharing | Optional opt-in program that uploads full session transcripts with secret redaction to a private store. |
| Transport | The connection mode to a provider (HTTPS, WebSocket, or Claude CLI). |
| Turn | One pass through the agent loop (assistant output, tool execution, provider round-trips). |
| Ultrafast | The OpenAI speed tier above Fast, applied through the speed picker or a hotkey. |
| user_response | The tool that returns a Markdown response to a Desktop-capable client. |

## Technical Terms

| Term | Definition |
|---|---|
| Background task | Server-side job running independently of the current turn. |
| Budget ratchet | CI-enforced limits (warnings, panics, code size, etc.) in `scripts/`. |
| consent_version | Version of the explicit transcript-sharing consent carried on transcript uploads. |
| Debug socket | A secondary socket that broadcasts TUI state for debugging/automation. |
| External credential source | Reusing credentials from other CLIs (e.g. `~/.codex/auth.json`, `~/.claude/.credentials.json`). |
| Failover / fallback / route | Provider selection, fallback on failure, and routing between providers/models. |
| Hooks | User-defined scripts fired at lifecycle points (turn start/end, pre-tool gate, session start/end). |
| Info widget | A TUI panel (session info, model, provider, usage) shown in the interface. |
| JCodeKit | Platform-free Swift client core for the iOS app owning gateway pairing, transport, and wire codecs. |
| JCodeMobile | SwiftUI iOS app shell built on JCodeKit for pairing, chat, sessions, and settings views. |
| Jev | Typed Decisions transport used for bring-your-own-key memory, browser, and voice calls. |
| KV cache | Provider-side key-value cache for repeated prompt prefixes. |
| Mermaid | Diagram rendering inside the terminal. |
| Mil / Bil | Compact abbreviations for million and billion token counts shown in usage cards. |
| NDJSON | Newline-delimited JSON used as the client-server wire framing. |
| OAuth / API key / device code | Authentication methods supported by the login flows. |
| Overnight | Scheduled background processing performed while the user is away. |
| QuickJS | The embedded JavaScript engine that runs the Codemode sandbox. |
| Service tier / premium mode | Provider-specific access tiers (e.g. priority/flex, copilot one/zero). |
| Session journal | Append-only JSONL log of a session plus a snapshot JSON file under `~/.jcode/sessions/`. |
| Session reducer | Pure state-machine function mapping server events plus local intents to transcript and app state. |
| Side panel | A collapsible TUI panel (e.g. session list, usage overlay). |
| Spawn hook | Hook that runs when a new session is spawned. |
| Telemetry | Anonymous minimal usage statistics with explicit opt-out plus optional versioned transcript uploads. |
| Token usage | Counting and limits for tokens consumed against provider subscriptions. |
| TUI | Terminal user interface. |
| Unix socket / named pipe | Local IPC transport (Unix sockets, or Windows named pipes behind the same API). |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ACP | Agent Client Protocol |
| APNs | Apple Push Notification service |
| BYOK | Bring Your Own Key |
| CI | Continuous Integration |
| D1 | Cloudflare D1 SQLite database |
| DAU | Daily Active Users |
| IPC | Inter-Process Communication |
| JWT | JSON Web Token |
| NDJSON | Newline-Delimited JSON |
| OAuth | Open Authorization |
| ONNX | Open Neural Network Exchange |
| R2 | Cloudflare R2 object storage |
| SDK | Software Development Kit |
| STT | Speech-to-Text |
| TUI | Terminal User Interface |
