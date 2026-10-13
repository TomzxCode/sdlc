# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Create a scheduled loop | Loop owner | The owner describes a recurring task once (via the dashboard compose modal, a template card, or `loopany new`), and the server stores the loop with its cron schedule, bound machine, task file, and optional workflow and dashboard UI. |
| UC-2 | Execute loops on their own machine | Loop operator | The operator runs `loopany up` on a machine they control, and the daemon polls the server, claims pending runs, spawns the local coding agent (Claude Code, Codex, or Grok), and reports results back with a run lease. |
| UC-3 | Monitor loops and runs on the dashboard | Team member | Team members browse loops, run history, the cross-loop timeline, and per-run diffs at `/t/<team>` and the loop/run detail pages, with team-scoped visibility. |
| UC-4 | Receive run and failure notifications | Team member | The loop's bound notification channel (Slack, Telegram, or Feishu) pushes success and failure alerts, with streak-based anti-spam and auto-pause after a configurable consecutive-failure streak. |
| UC-5 | Persist loop output as synced artifacts | Coding agent (in run) | Files the agent writes in the loop folder sync to durable content-addressed storage (manifest plus blob PUT), and render on the loop's generative dashboard with front-matter typing. |
| UC-6 | Improve a loop over time | Loop owner | Evolve passes periodically refine the loop's config and dashboard, and owner-requested edits apply a single agent pass or a pasted prompt, both through the run-token surface. |
| UC-7 | Run a deterministic pre-stage workflow | Loop owner | The owner attaches an async-function-body workflow to a loop, and the daemon runs it on local MCP tools before the agent, falling back to the agent with failure context when it fails. |
| UC-8 | Onboard a first loop end to end | New user | The onboarding wizard at `/onboarding` walks machine connect, loop creation from the Housekeeper template, the live first run, and notification binding, advancing only on detected reality. |
| UC-9 | Browse and share loop templates | Visitor / loop owner | The public template market at `/templates` (SSR, no auth) presents bundles with flow diagrams and verbatim paste-prompts, and each card deep-links into the dashboard compose flow. |
| UC-10 | Manage teams, machines, and channels | Team admin | Admins create teams, invite members, register machines via per-team connect keys, and bind notification channels with a live test ping. |
| UC-11 | Operate and self-host the control plane | Server operator | The operator deploys one scheduler-owning process (embedded pglite or hosted Postgres plus R2), with forward-only migrations, health endpoints, and rate-limited machine routes. |

## Wanted

No wanted use cases are recorded yet.
New entries go here with a signal (an issue, feature, or roadmap item) when a real need is identified.

## Out of scope

- Running LLMs or executing user code on the server (zero-exec invariant).
- Credentials or tools leaving the user's machine without the loop choosing to sync bytes back.
- WebSocket-based machine connectivity (stateless HTTP long-poll by design).
- Cross-machine fallback for a bound loop (execution is machine-pinned at creation).
