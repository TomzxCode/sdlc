<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->
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
| UC-1 | Get interactive coding help in the terminal | Developer | The developer launches `opencode` or `opencode mini` from `packages/cli`, switches between the build and plan agents, and iterates with the session runtime in `packages/core/src/session`. |
| UC-2 | Get coding help in a browser or native app | Developer | The developer uses the `packages/app` web UI through `opencode serve` or `opencode pair`, or the `packages/desktop` Electron app, with shared timeline components from `packages/session-ui`. |
| UC-3 | Automate coding tasks from scripts and pipelines | Developer, Operator | The developer runs `opencode run` with a prompt and the `--model`, `--agent`, `--format`, `--session`, and `--continue` flags, or drives the HTTP API through `opencode api` for scripting and CI. |
| UC-4 | Use the right model for a task without vendor lock-in | Developer | The developer discovers models with `opencode models`, connects accounts with `opencode auth login/logout/list`, and uses the provider clients in `packages/ai` with the models.dev catalog. |
| UC-5 | Keep a coding conversation across restarts and branches | Developer | The developer creates, resumes, forks, archives, and searches sessions through the `session` and `message` API groups and the durable inbox and message rows in `packages/core/src/session`. |
| UC-7 | Let the agent edit files and run commands with controls | Developer | The model calls Location-scoped tools from `packages/core/src` for files, shell, search, and web, while the developer gates side effects with permission config and the `permission` API group. |
| UC-8 | Reuse project instructions and repeatable workflows | Developer | The developer adds skills and slash commands read from `packages/core/src/skill*` and `command.ts`, exposed through the `skill` and `command` API groups. |
| UC-9 | Extend the agent with custom behavior and external tools | Plugin author | The author ships plugins with namespaced hooks through `@opencode/plugin` in `packages/plugin`, and adds external tools and context through MCP servers via the `mcp` and `plugin` API groups. |
| UC-10 | Embed the agent in another application | Developer, Integrator | The developer hosts the in-process SDK through `OpenCode.create()` in `packages/sdk` or calls the typed HTTP API with the generated `@opencode/client`. |
| UC-11 | Drive the agent from an editor or another agent client | Developer | External editors and tools use the Agent Client Protocol server in `opencode acp` (`packages/cli/src/acp`) to manage sessions and turns. |
| UC-13 | Run OpenCode as a private service | Operator | The operator runs the Effect HttpApi server in `packages/server` with `opencode serve`, publishes OpenAPI at `/openapi.json`, and manages the background service with `opencode service start/stop/restart/status`. |
| UC-15 | Keep separate codebases and worktrees available to the agent | Developer | The developer registers projects, directories, worktrees, and VCS info through the `project`, `worktree`, and `vcs` API groups backed by the project and worktree tables. |
| UC-16 | Find documentation and release notes | Developer, Contributor | Readers use the docs under `services/site/src/docs` and the changelog pages in `services/site`, and contributors extend them in the same service. |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| UC-17 | Run coding sessions and get replies from Slack | Developer | A first-party Slack bot is absent from this repo, and the in-repo code only watches Slack threads and connects an external Console MCP gateway. | FEAT-0012 (stale, under review) |

## Out of scope

- Training or fine-tuning models (OpenCode consumes existing providers).
- Hosting or managing the user's code repositories (OpenCode operates on local directories only).
- General-purpose chat outside a coding or project context.
