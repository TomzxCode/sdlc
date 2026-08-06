# Vocabulary

<!--
This file defines domain-specific terms, acronyms, and abbreviations used across
the project. Keeping definitions here avoids ambiguity in requirements, specs,
and discussions. Add new terms as they are introduced.
-->

## Domain Terms

| Term | Definition |
|---|---|
| Loop | A scheduled behavior bound to one machine: a cron schedule, a task file, an optional workflow pre-stage, and an optional goal. |
| Loop folder | The on-machine directory the agent works in; its task file is the README and its contents live-sync to the server as artifacts. |
| Open loop | A loop with `goal = null` that runs indefinitely (monitor/digest); it never self-terminates. |
| Closed loop | A loop with a non-null `goal`; each exec run judges state against the goal and may call `loopany finish` when met, stamping `completedAt` and disabling the loop. |
| Exec run | A scheduled execution of a loop (role `exec`); only exec runs produce user-facing notifications. |
| Evolve run | A self-improvement pass (role `evolve`) that reviews run history and rewrites the loop's brief, state schema, and dashboard. |
| Edit run | An owner-requested change (role `edit`) that applies an instruction to the loop, then clears the request. |
| Run token / run credential | The per-run lease credential (`rk_…`) authorizing in-run `loopany` verbs and the final report. |
| Device token | The `dk_`-prefixed credential that fully impersonates a machine for owner verbs and polling. |
| Connect key | A one-time claim token minted by the dashboard that binds a newly connecting machine to its owner and team. |
| Task file | The loop's durable context+log document on the machine; its `## Spec` section is the standing brief. |
| Workflow | An optional zero-LLM async function body (validated, machine-run) that does cheap mechanical work before the agent; a failure falls back to the agent with context. |
| Generative dashboard | Loop-authored `ui` markup (with `loop-embed`/`loop-calendar`/`loop-kanban` primitives) rendered by the web UI from synced front-matter artifacts. |
| Front matter | An optional fenced `---` block of flat `key: value` scalars at the top of a markdown product; the indexed subset `{type?, title?, date?}` is parsed once at byte ingress. |
| Template | A canned loop intent (meta.json `description` paste-prompt, optional `reference.md`, `thumb.svg`, `story.md`, flow spec) under `src/skill/templates/`. |
| Bundle | A curated category of templates under `src/skill/bundles/`; every template belongs to exactly one bundle. |
| Machine | A teammate's daemon; the identity unit that owns loops and scopes the dashboard. |
| Team | The ownership/scope unit (every user gets a personal team); loops, machines, and channels are listed/authorized by team. |

## Technical Terms

| Term | Definition |
|---|---|
| Pending run | A run row in phase `pending`; it is the durable inbox a machine's poll claims. |
| Run lease | A durable row (`run_leases`) minted per delivery holding per-run caps; state machine `active` → `terminal-grace` → retired. |
| Terminal-grace | A swept run's lease state with a bounded expiry that allows exactly one reconciling late wake-report. |
| Long-poll | The opt-in server-held poll (`wait:true`, ~20s) an idle daemon uses for near-zero dispatch latency. |
| Watch set / watchDigest | The per-machine cache of loop folders to watch, digest-echoed so an unchanged client omits the payload. |
| Manifest | The full sha256 manifest of a loop folder's files; hashing is incremental, the manifest always full. |
| Blob | Content-addressed bytes keyed by sha256 hash, stored in R2 or in-memory; referenced by `blobs`/`artifact_files` rows. |
| Oversize | A file exceeding the per-file byte cap (10MB); stored metadata-only with no bytes. |
| Run snapshot | The loop's full artifact manifest captured at each run's finalize, diffed against the prior run for the run page. |
| Sweep | The periodic server maintenance pass that reclaims stale runs, holds deferred pending runs, and runs retention/GC. |
| Circuit breaker | `notifyRunFailure` auto-pause of a loop after a configurable consecutive-exec-failure streak. |
| Misfire catch-up | Boot-time reconstruction of a missed cron occurrence inside a deploy window, firing one compensating tick. |
| TOON | The axi-shaped text output rendered by `gateway/toon.ts` for every `/api/machine/cli` verb. |
| BYOA | Bring-your-own-agent: execution runs with the user's own coding agent and credentials on their own machine. |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| BYOA | Bring-Your-Own-Agent |
| R2 | Cloudflare R2 object storage |
| TTL | Time-to-live |
| GC | Garbage collection |
| LLM | Large Language Model |
| WS | WebSocket |
| UI | User interface |
| PR | Pull Request |
| npm OIDC | npm OpenID Connect trusted publishing |
| Fly / Fly.io | Fly.io app hosting |
| pglite | Embedded WASM Postgres by ElectricSQL |
| MCP | Model Context Protocol |
