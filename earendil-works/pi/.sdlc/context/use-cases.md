# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Interactive terminal coding session | developer | The developer runs `pi` in a project folder and iterates with the model through the fullscreen TUI with transcript, editor, thinking levels, and usage footer. |
| UC-2 | One-shot scripted prompt | developer | The developer runs `pi --print` with a prompt, piped stdin, or `@file` arguments to get a single final answer and exit for shell automation. |
| UC-3 | JSON event stream automation | operator | The operator runs `pi --mode json` to receive a JSONL session event stream on stdout for machine-consumed automation. |
| UC-4 | RPC control from another process | developer | The developer drives a long-lived `pi --mode rpc` subprocess with JSONL commands, responses, and session events from any language, IDE, or custom client. |
| UC-5 | In-process SDK embedding | SDK consumer | The SDK consumer creates an `AgentSession` via `createAgentSession()` in Node.js or Bun for direct TypeScript access to prompting, sessions, tools, models, and events. |
| UC-6 | File and shell operations via built-in tools | developer | The developer lets the model read, create, edit, search, and list files and run shell commands through the `read`, `bash`, `edit`, `write`, `grep`, `find`, and `ls` tools. |
| UC-7 | Parallel scripted tool orchestration | developer | The developer enables the `codemode` tool so the model runs JavaScript that calls other tools in parallel and filters large output before it reaches context. |
| UC-8 | Session persistence and branching | developer | The developer continues, resumes, names, forks, clones, and navigates sessions with `/new`, `/resume`, `/tree`, `/fork`, `/clone`, and `--continue` without losing alternative branches. |
| UC-9 | Context compaction | developer | The developer reclaims context with automatic or manual `/compact` summarization while original session entries stay preserved. |
| UC-10 | Session export and sharing | developer | The developer copies, exports as HTML or JSONL, or shares a session link via `/copy`, `/export`, and `/share` for review and collaboration. |
| UC-11 | Model and provider selection | developer | The developer picks among 30+ providers and models with `/model`, `--model`, `--provider`, `--thinking`, and `/login` using stored or override credentials. |
| UC-12 | MCP server tools and resources | developer | The developer connects stdio or HTTP MCP servers via `pi mcp add` and `mcp.json` so the model reaches their tools through direct, codemode, or deferred exposure and reads their resources. |
| UC-13 | Custom extension behavior | extension author | The extension author registers tools, slash commands, flags, shortcuts, event handlers, providers, MCP servers, and terminal UI through a TypeScript extension module. |
| UC-14 | On-demand skill instructions | developer | The developer relies on Agent Skills directories that advertise name and description in the system prompt and load full instructions only when the task matches. |
| UC-15 | Reusable prompt templates | developer | The developer invokes Markdown prompt templates with `{{variable}}` expansion as `/templatename` commands. |
| UC-16 | Custom terminal themes | developer | The developer installs JSON themes and selects them with `--use-theme` to restyle the interactive terminal. |
| UC-17 | Shareable pi packages | extension author | The extension author bundles extensions, skills, prompts, and themes into a pi package and distributes it via npm, git, URL, or local path with `pi install`. |
| UC-18 | Custom model providers | extension author | The extension author adds a model service integration with `pi.registerProvider()` or per-request routing with `pi.registerVirtualModel()`. |
| UC-19 | Remote tool execution over SSH | operator | The operator runs an agent's tools on another machine over SSH through the pi-env daemon while the Durable worker, its storage, and credentials stay local. |
| UC-20 | Sandboxed and remote execution | operator | The operator routes tool execution into an isolated or remote environment using extension-provided sandboxing such as the Gondolin micro-VM, plain Docker, OpenShell, or the pi-env daemon. |
| UC-21 | Durable conversation, task, and document state | SDK consumer | The SDK consumer persists conversations, executable tasks, and JSON documents as atomic storage commits through the pi-durable runtime. |
| UC-22 | Composable app runtime with facets and services | SDK consumer | The SDK consumer composes hot-reloadable plugins with singleton or keyed services and replicated state through the standalone chord runtime. |
| UC-23 | Vendor-neutral telemetry | operator | The operator collects typed spans and events against versioned telemetry contracts through pi-telemetry adapters. |
| UC-24 | Behavioral workflow evals | developer | The developer measures end-to-end agent behavior with model-backed evals that run real `AgentSession` instances via the pi-evals harness. |
| UC-25 | Project trust gating | developer | The developer approves or rejects project-local configuration, resources, and extensions per folder so untrusted checkouts cannot execute code silently. |

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
