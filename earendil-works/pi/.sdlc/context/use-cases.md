<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Work with a model on a codebase from the terminal | developer | The developer runs `pi` in a project folder and iterates with the model in the fullscreen TUI, with a transcript, editor, thinking levels, and a footer that shows the folder, session, model, context usage, and accumulated cost. |
| UC-2 | Get one answer from the model without a live session | developer | The developer runs `pi --print` with a prompt, piped stdin, or `@file` arguments, reads the final answer, and lets the process exit for shell automation. |
| UC-3 | Consume a run as a structured event stream | operator | The operator runs `pi --mode json` and reads a JSONL stream of session events on stdout for machine-consumed automation. |
| UC-4 | Drive a long-lived agent session from another program | developer | The developer runs `pi --mode rpc` and sends JSONL commands, and receives responses and session events, from any language, IDE, or custom client. |
| UC-5 | Embed the agent in an application | SDK consumer | The SDK consumer creates an `AgentSession` through `createAgentSession()` in Node.js or Bun for direct TypeScript access to prompting, sessions, tools, models, and events. |
| UC-6 | Have the agent read, change, and run things in the project | developer | The developer lets the model work on the checkout through the `read`, `bash`, `edit`, `write`, `grep`, `find`, and `ls` tools, of which `read`, `bash`, `edit`, and `write` are active by default. |
| UC-7 | Let the model orchestrate many tool calls in one pass | developer | The developer enables the `codemode` tool so the model runs JavaScript in a QuickJS sandbox that calls other tools in parallel, filters large output before it reaches the context, and keeps values between calls. |
| UC-8 | Return to earlier work and try a different path | developer | The developer continues, names, forks, clones, and navigates sessions with `/new`, `/resume`, `/tree`, `/fork`, `/clone`, and `--continue` while the session file keeps every branch. |
| UC-9 | Keep a long conversation inside the context window | developer | The developer reclaims context with automatic or manual `/compact` summarization while the original session entries stay in the file. |
| UC-10 | Review or hand off what happened in a session | developer | The developer copies the last reply, exports the session as HTML or JSONL, imports a session from a JSONL file, or shares a link through `/copy`, `/export`, `/import`, and `/share`. |
| UC-11 | Choose a model and connect its credentials | developer | The developer picks among 42 built-in providers with `/model`, `--model`, `--provider`, `--thinking`, and `/login`, using a stored credential, an environment variable, or OAuth for the 9 providers that support it, and restricts which models the cycle key reaches with `/scoped-models`. |
| UC-12 | Use tools and data that live in other systems | developer | The developer connects stdio or HTTP MCP servers with `pi mcp add` and `mcp.json` so the model reaches their tools directly, through codemode, or after a deferred search, and reads their resources. The standalone `@earendil-works/pi-mcp` client is published for applications that need the same servers without the CLI. |
| UC-13 | Give the agent behavior of my own | extension author | The extension author registers tools, slash commands, flags, shortcuts, event handlers, providers, MCP servers, and terminal UI through a TypeScript extension module that loads at startup and reloads with `/reload`. |
| UC-14 | Load specialized instructions only when a task needs them | developer | The developer relies on Agent Skills directories that advertise name and description in the system prompt and load the full instructions only when the task matches. |
| UC-15 | Reuse a prompt I have written before | developer | The developer invokes Markdown prompt templates with `{{variable}}` expansion as `/templatename` commands. |
| UC-16 | Make the terminal match my own setup | developer | The developer installs JSON themes and selects them with `--use-theme` to restyle the interactive terminal. |
| UC-17 | Share my setup with other people | extension author | The extension author bundles extensions, skills, prompts, and themes into a pi package and distributes it via npm, git, URL, or local path with `pi install`. |
| UC-18 | Connect a model service the project does not ship | extension author | The extension author adds a model service integration with `pi.registerProvider()` or per-request routing with `pi.registerVirtualModel()`. |
| UC-19 | Run the agent's tools on another machine | operator | The operator runs an agent's tools on another machine over SSH through the pi-env daemon while the Durable worker, its storage, and credentials stay local. |
| UC-20 | Keep what the agent can reach inside a boundary I control | operator | The operator routes tool execution into an isolated or remote environment using extension-provided sandboxing such as the Gondolin micro-VM, plain Docker, OpenShell, or the pi-env daemon. |
| UC-21 | Keep conversations, tasks, and documents across restarts | SDK consumer | The SDK consumer persists conversations, executable tasks, and JSON documents as atomic storage commits through the pi-durable runtime, on memory, JSONL, or SQLite storage. |
| UC-22 | Compose an application out of plugins that share state | SDK consumer | The SDK consumer composes hot-reloadable plugins with singleton or keyed services and replicated state through the standalone chord runtime, over in-memory, IPC, or WebSocket links. |
| UC-23 | Instrument the agent without committing to a vendor | operator | The operator collects typed spans and events against versioned telemetry contracts through pi-telemetry adapters, which ship a conformance suite for any adapter. |
| UC-24 | Measure how the agent actually behaves | developer | The developer measures end-to-end agent behavior with model-backed evals that run real `AgentSession` instances through the pi-evals harness in isolated containers. |
| UC-25 | Run project-local code only in folders I trust | developer | The developer approves or rejects project-local configuration, resources, and extensions per folder so untrusted checkouts cannot execute code silently. |
| UC-26 | Call a model provider from my own code | SDK consumer | The SDK consumer calls `createModels()` in `@earendil-works/pi-ai` to stream from 42 built-in providers through one API, with auth resolved from stored credentials, environment variables, or OAuth, a generated model catalog, tool calls, and image and classifier models. |
| UC-27 | Run an agent loop of my own over my own tools | SDK consumer | The SDK consumer uses `@earendil-works/pi-agent-core` to run the agent loop, hold the transcript and state, emit lifecycle events, and execute tools in parallel or sequentially with hooks before and after each call. |
| UC-28 | Build a terminal application without writing a renderer | SDK consumer | The SDK consumer uses `@earendil-works/pi-tui` for the component set, keybindings, and differential rendering over the main or alternate screen, with synchronized output so frames do not flicker. |
| UC-29 | Run the model on my own machine | developer | The developer points Pi at a local llama.cpp router server through the built-in llama extension, loads a GGUF model with `/llama`, and pulls model files from Hugging Face, so no cloud account or API key is needed. |
| UC-30 | Keep the cost and token use of a session under control | developer | The developer sees accumulated tokens and cost in the footer and `/session`, can turn on notices for significant cache misses, and lets Pi keep the prompt cache warm when the model advertises a cache lifetime, which lowers the cost of an idle session. |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|

No wanted use cases are currently tracked with in-repo signals.
Longer-term plans live in the RFC index linked from the README and CONTRIBUTING guides.

## Out of scope

- Sub-agents and plan mode in the core, which stay minimal by design and belong in extensions or user-built workflows.
- A built-in permission system for restricting filesystem, process, network, or credential access, which is delegated to external sandboxes and containerization.
- Permission popups in the core, which extensions may provide instead.
- Chat and Slack automation, which lives in the separate pi-chat repository.
- A full IDE, since Pi is a terminal harness that IDEs integrate with through RPC, JSON mode, or the SDK.
- Backward compatibility that the maintainer did not explicitly request.
