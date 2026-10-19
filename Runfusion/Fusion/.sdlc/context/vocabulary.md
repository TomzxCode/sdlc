# Vocabulary

This file defines domain-specific terms, acronyms, and abbreviations used across the project.
Keeping definitions here avoids ambiguity in requirements, specs, and discussions.
Add new terms as they are introduced.
Terms within each table are sorted alphabetically by the first column.

## Domain Terms

| Term | Definition |
|---|---|
| Active-session lease | A path-keyed, in-memory claim that a worktree path is held by one task's running session, used both for mutual exclusion and as proof that the task is alive |
| Agent slot | A unit of a project's concurrent-agent capacity, drawn from one shared pool by planning, execution, and merge alike, so a project cannot exceed its operator-facing limit by spending capacity in a different lane |
| Approval request | A durable hold that blocks a task from advancing until a human approves, recorded with who approved and when |
| Artifact | A registry entry for a deliverable produced by an agent, chat, workflow, or task, with a type, an author, and optional task linkage |
| Auto-merge | Automated promotion of finished branches into the default branch (squash/rebase/PR paths) |
| Autopilot | The named process that watches an active mission and activates the next pending slice once the current slice completes |
| Branch assignment mode | The strategy by which a task acquires its working branch and merge target, such as a shared branch group or the project default branch |
| Chat | Persistent chat sessions and rooms for operator and agent conversation, backed by the chat store |
| Checkout lease | Exclusive execution ownership of a task, held through a claim row plus lease metadata and validated on every heartbeat |
| Claim | The authoritative ownership row for a task in the central database, keyed by project and task, used to fence out stale owners |
| Column | A workflow-defined unit of task state with an id, a display name, and a set of traits, where a task's board position is its current column |
| Column agent | A permanent agent binding on a workflow-defined column that staffs the session-running work attributable to that column |
| Command Center | The operator "mission control" dashboard for the agent fleet, signals, and usage |
| Compound engineering session | A single interactive run of a compound engineering stage, where an agent drives a question-and-answer flow and produces the stage artifact |
| Contamination | Foreign commits from other tasks that appear on a task's branch beyond its recorded fork point |
| Contract assertion | A checkable acceptance criterion on a mission feature, judged by an AI validator to decide whether the feature is genuinely done |
| Custom task field | A workflow-declared typed task field whose values live in `tasks.customFields` and are validated against the resolving workflow's schema |
| Default workflow | The built-in workflow `builtin:coding` that reproduces the legacy pipeline, with six columns whose ids match the historical status names |
| Distributed task ID | A task identifier allocated from shared reservations so that concurrent nodes never mint the same id |
| Durable agent | A persistent agent that runs on a heartbeat and can be auto-recovered from error states |
| Effective agent | The agent identity that runs a piece of work after column-agent precedence resolves, and the principal that identity-keyed subsystems consult |
| Effective settings | The per-task settings map the engine reads at runtime, where stored workflow values fall back to declaration defaults and invalid values are dropped |
| Evals | Canonical 0–100 scoring of agent performance, task outcome quality, and process compliance |
| Fork point | The commit on the integration branch from which a task's branch was created, the lower bound of the changes that task owns |
| Global settings | User-level settings that apply across every surface and every project, validated at the write boundary |
| Goals | Measurable objectives tracked in the dashboard with a refinement gate |
| Group promotion | The gated, repeatable act of merging a complete shared branch group toward the project default branch, creating or reusing the group's single managed pull request |
| Heartbeat run | A short permanent-agent wake triggered by a timer, assignment, message, or on demand, which takes one coordination action and exits |
| Hold node | A workflow node kind expressing passive dwell, where a card rests in its column until a release condition fires |
| Ideation | A bounded project-scoped session that collects ideas and candidates, which converge into the mission hierarchy |
| In-review | The column between execution and completion, where work is done and the branch awaits merging |
| Integration branch | The local branch, by default the project default branch, where the merger lands task branches and from which new task worktrees fork |
| Lane | A horizontal row on the board, one per workflow in use by visible cards, each rendering that workflow's columns |
| Loop state | A mission feature's position in the execution loop, distinct from its board column, and possibly stale or contradictory |
| Manual-required | The merge-request state for a task whose merge needs an explicit human go-ahead |
| Memory | Pluggable persistent recall of task shots, transcripts, and recall hits (Stash backend) |
| Merge queue | The ordered line of in-review tasks awaiting auto-merge, with a single merge active at a time |
| Mission / milestone / slice / feature | The product-hierarchy layers (mission to milestone to slice to feature) that drive task work |
| Patchnode | Dashboard feed rendered from denormalized ledger entries, durable across archive cleanup |
| Plan Review | The workflow gate that judges a task's plan before execution, returning APPROVE, APPROVE_WITH_NOTES, REVISE, or CLOSE_NO_OP |
| Planner overseer | Automated oversight of planning work across `off` / `observe` / `steer` / `autonomous` levels with human-confirmation gates |
| Planning mode | A dedicated human-in-the-loop planning chat and Plan Review node for shaping a task before execution |
| PR entity | The single first-class record of a pull request Fusion manages, whether it came from one task or a shared branch group |
| Project | A registered workspace Fusion can operate on, with a canonical local path, project-scoped settings, and a usable git work tree |
| Research | Cited search-and-synthesis pipeline that runs bounded investigations into actionable task context |
| Review-response loop | The process where an agent acts on pull request review feedback, either by pushing a fix and replying to the thread or by posting its reasoning and leaving the thread open |
| Routine | A recurring task automation with a trigger mode (cron, webhook, API, or manual) plus execution and catch-up policies |
| Run audit | Append-only structured event log of engine/task lifecycle events (ids/counts-outcomes metadata only) |
| Self-healing | Engine sweeps that reconcile stranded, orphaned, or stale task/agent/worktree state |
| Signals connector | HMAC-signed external ingest (Sentry/Datadog/PagerDuty/webhooks) into Fusion |
| Slice | A vertically-scoped, independently completable chunk of a milestone that holds features and is complete only when all of them are done |
| Split / join | Parallel-branch workflow node kinds, where a split launches its outgoing edges concurrently and a join synchronizes them with an all, any, or quorum mode |
| Step instance | One runtime expansion of a `foreach` template subgraph, bound to a single planned step and identified deterministically |
| Task board | The kanban surface of workflow columns (planning/todo/in-progress/in-review/done or graph-driven variants) that tracks AI-orchestrated work items |
| Task document | A persisted, revision-tracked document attached to a task, such as its plan or its PROMPT.md |
| Task lifecycle | The domain state machine modeling a task's progression and its status values |
| Task lineage | The durable identity a task carries in its commit trailers, so commits can be attributed back to the task that produced them |
| Trait | Composable column configuration made of declarative flags plus optional lifecycle hooks, registered through one registry |
| Transition pending | A persisted marker written with a column change that records the post-commit hooks still owed, so a crash re-runs them |
| Validator run | A single execution that evaluates a mission feature's contract assertions and yields a pass, fail, blocked, error, or inconclusive outcome |
| Workflow extension | A plugin-contributed workflow capability registered through the engine, such as column metadata, movement policies, or node handlers |
| Workflow graph | A DAG of nodes (plan/code/review/gate/merge) a task traverses; replaces the fixed legacy lifecycle columns |
| Workflow node | A unit in the workflow graph (e.g. plan, code, review, gate, merge, exit-gate) with its own runner |
| Workflow setting | A typed setting declared by a workflow, whose values persist per workflow and project through a validating store |
| Workflow work item | A durable row for one unit of workflow-graph work, with a state, an attempt count, and a lease |
| Workspace | Multi-repository project variant with one task worktree per sub-repository and a per-repository land loop |

## Technical Terms

| Term | Definition |
|---|---|
| Boot smoke | The gate's "the app starts and serves" proof, where the CLI answers its help command and a server boots on a throwaway port, answers its health endpoint, and shuts down cleanly |
| Bounded run-audit emitter | The engine and core seam that records a run-audit row without letting telemetry delay, abort, or wedge the owning branch, by absorbing absent, throwing, rejecting, and hanging sinks |
| Deletion ratchet | The standing policy that a test observed failing without a corresponding bug is quarantined on sight and then deleted two weeks later, never appeased with widened timeouts or retries |
| Drizzle ORM | The typed SQL schema layer that defines Fusion's PostgreSQL tables under `packages/core/src/postgres/schema/` |
| Embedded PostgreSQL | The locally launched PostgreSQL 15 instance that backs the project, central, and archive schemas in local and development runs |
| File-scope | The set of files a task is allowed/expected to touch; enforced on squash merges |
| File-scope lease | A durable claim that a task owns a set of files, used to block overlapping work on the same paths |
| Knowledge graph | Deterministic LLM-free structure graph of the codebase, built incrementally from fingerprints |
| Merge gate | The minimal set of pull-request checks that block a merge: lint, typecheck, build, boot smoke, and a curated engine test suite, with membership held by an explicit allow-list |
| Merger | Engine component that lands branches via squash/rebase/PR with conflict resolution and guards |
| Mesh | Distributed coordination across multiple Fusion nodes sharing a PostgreSQL backend, with a central schema holding project registration, claims, and nodes |
| Node runner | Per-node implementation (code-runner, gate-runner, merge-runner, exit-gate-runner, review) |
| pi extension | A first-party carrier that routes Fusion's agent commands into a specific coding-agent CLI |
| Plugin | First-party extension unit contributing custom tools, routes, settings, and lifecycle hooks |
| Plugin entry | The single loadable file persisted as a plugin's path and dynamically imported by the loader, which is never a package directory |
| Sandbox | Pluggable executor command isolation (bubblewrap, macOS `sandbox-exec`, native) with a fail-hard or fallback-native failure mode |
| Schema-version sweep | The repo-wide hunt for hard-coded assertions of the old schema version, performed in the same commit as any bump of the version counter |
| SDLC artifact | A produced SDLC artifact instance (requirements, specification, plan, tests, etc.) under `.sdlc/features/<N>-<slug>/` |
| Secrets | Encrypted-at-rest credential storage with project and global scopes and per-key access policies |
| Smart pull | The one-shot pull workflow that advances the checked-out integration branch while keeping local work safe, by fast-forwarding directly or by stashing and restoring |
| Symbol lock | A durable, project-scoped claim on a normalized code symbol key, held by a task to keep later scheduling phases from conflicting over the same symbol |
| Task store / task-advisory lock | The domain persistence layer and per-task advisory locking used for lifecycle moves |
| Tool surface | The set of `fn_`-prefixed tools an agent may call, whose availability depends on the lane, the column, and the agent's permission policy |
| Triple-proof liveness | The canonical proof that a task/session is contended before backward moves |
| Workflow graph executor | Engine component that drives the workflow graph through its node runners |
| Workflow IR | The declarative intermediate representation of a workflow, holding its columns, traits, nodes, edges, and settings declarations |
| Worktree | An isolated git working tree used for branch-scoped task work, keeping the primary checkout on main |
| Worktrunk | External git-worktree manager CLI (`wt`) used for branch-scoped worktrees |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ACP | Agent Client Protocol |
| API | Application programming interface |
| CLI | Command-line interface |
| DAG | Directed acyclic graph |
| FEAT | Feature identifier in SDLC artifacts (`FEAT-N`) |
| FN-XXXX | Fusion task/issue tracker identifier |
| FNXC | Source comment stamp that encodes a requirement (`FNXC:<Area> <yyyy-MM-dd-hh:mm>`) |
| FR / NFR | Functional / non-functional requirement |
| HMAC | Hash-based message authentication code |
| HTTP | Hypertext Transfer Protocol |
| IR | Intermediate representation |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| L10n / i18n | Localization / internationalization |
| LLM | Large language model |
| MCP | Model Context Protocol |
| OIDC | OpenID Connect |
| PR | Pull request |
| PTY | Pseudo-terminal |
| PWA | Progressive web app |
| REST | Representational State Transfer |
| SDLC | Software development lifecycle |
| SLA / SLO / SLI | Service-level agreement / objective / indicator |
| SQL | Structured Query Language |
| SSE | Server-sent events |
| TUI | Terminal user interface |
| UI | User interface |
| YAML | YAML Ain't Markup Language |
