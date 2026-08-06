# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| Session | A unit of interaction with the agent: a persisted conversation with an id, title, and status. |
| Message | A single exchange in a session, carrying a role (User/Assistant) and a list of content blocks. |
| Content block / part | A typed piece of a message (text, reasoning, thinking, tool use, tool result, image, compaction). |
| Turn | One pass through the agent loop (assistant output, tool execution, provider round-trips). |
| Tool / tool call / tool result | A capability the agent can invoke; the request and its outcome. |
| Compaction | Reducing accumulated context (and the KV cache) when a session grows too large. |
| Provider | A source of model completions (Anthropic, OpenAI, Gemini, Bedrock, OpenRouter, etc.). |
| Transport | The connection mode to a provider (HTTPS, WebSocket, or Claude CLI). |
| Effort / reasoning | The configured reasoning depth for a model. |
| Swarm | Multi-agent coordination where a coordinator delegates tasks to worker agents. |
| Plan DAG / plan item | The directed acyclic graph of tasks a swarm coordinator builds. |
| Comm channel | A message channel between swarm members (direct message, broadcast). |
| Memory graph | The persistent graph of extracted memories, skills, and relationships. |
| Embedding | A numeric vector representing text, computed locally with an ONNX MiniLM model. |
| Recall / injection | Retrieving relevant memories and inserting them into the prompt. |
| Consolidation | Background process that merges and strengthens memories over time. |
| Ambient mode | Proactive background agent (OpenClaw-style) with work cycles, garden/scout tasks, and overnight processing. |
| Self-dev | Canary self-development mode that runs a freshly built binary on a shared server. |
| Canary | A session or build used to test new code against real usage. |
| Reload | Hot-reloading the server into a new binary without dropping clients or sessions. |
| Restart snapshot | A saved snapshot of sessions and state used to resume after a reboot. |
| Resume target | An external session source that can be resumed (jcode, Claude Code, Codex, Pi, OpenCode, Cursor). |
| Pairing / gateway | QR-code pairing of the iOS app to the desktop daemon through a gateway. |
| Harness API / API bridge | The stable versioned client API (`jcode api-bridge`) and the SDKs that consume it. |

## Technical Terms

| Term | Definition |
|---|---|
| NDJSON | Newline-delimited JSON used as the client-server wire framing. |
| Unix socket / named pipe | Local IPC transport (Unix sockets, or Windows named pipes behind the same API). |
| Debug socket | A secondary socket that broadcasts TUI state for debugging/automation. |
| Session journal | Append-only JSONL log of a session plus a snapshot JSON file under `~/.jcode/sessions/`. |
| KV cache | Provider-side key-value cache for repeated prompt prefixes. |
| Token usage | Counting and limits for tokens consumed against provider subscriptions. |
| Failover / fallback / route | Provider selection, fallback on failure, and routing between providers/models. |
| Service tier / premium mode | Provider-specific access tiers (e.g. priority/flex, copilot one/zero). |
| OAuth / API key / device code | Authentication methods supported by the login flows. |
| External credential source | Reusing credentials from other CLIs (e.g. `~/.codex/auth.json`, `~/.claude/.credentials.json`). |
| TUI | Terminal user interface. |
| Info widget | A TUI panel (session info, model, provider, usage) shown in the interface. |
| Mermaid | Diagram rendering inside the terminal. |
| Side panel | A collapsible TUI panel (e.g. session list, usage overlay). |
| Hooks | User-defined scripts fired at lifecycle points (turn start/end, pre-tool gate, session start/end). |
| Spawn hook | Hook that runs when a new session is spawned. |
| Background task | Server-side job running independently of the current turn. |
| Overnight | Scheduled background processing performed while the user is away. |
| Budget ratchet | CI-enforced limits (warnings, panics, code size, etc.) in `scripts/`. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| TUI | Terminal User Interface |
| OAuth | Open Authorization |
| ONNX | Open Neural Network Exchange |
| STT | Speech-to-Text |
| ACP | Agent Client Protocol |
| SDK | Software Development Kit |
| D1 | Cloudflare D1 SQLite database |
| IPC | Inter-Process Communication |
| NDJSON | Newline-Delimited JSON |
| DAU | Daily Active Users |
| CI | Continuous Integration |
| QE | Quality Engineering |
