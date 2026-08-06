---
title: "Loopany Daemon & CLI"
status: done
---

# Specification: Loopany Daemon & CLI

## Overview

The daemon is one Node ESM binary (`dist/cli.js`) with two roles: the poll-loop daemon and the in-run `loopany` callback. Routing is a pure, side-effect-free classifier in `route.ts`; `cli.ts` maps a `Route` to a lazily-imported handler. All server verbs converge on `cli-client.ts` `postCli`, which picks the credential by env (run token wins), inlines file flags, and POSTs to the unified `/api/machine/cli` with a legacy fallback for old servers.

## Architecture

```
loopany <args>
   └─ route.ts classify(argv, env) → Route
        ├─ LOOPANY_RUN_TOKEN set → callback (in-run; bare → "home")
        ├─ help/version fast-paths
        ├─ <verb> --help → per-verb usage (before handler)
        ├─ up / up --foreground / --server-url re-exec → daemon
        ├─ new/skill/setup/update/status/down/log/show/progress → handlers
        ├─ loops/edit → interactive
        ├─ report/finish/complete out-of-run → forward (device-cred 403)
        └─ bare → home (device cred, content-first)
```

The daemon poll loop (`daemon.ts`) builds the poll body with `wait:true` only while no run is in flight; the runner (`runner.ts`) spawns the coding agent via `buildAgentSpawn` and classifies crashes to decide transient resume.

## Data Models

The daemon persists local-only state, none of which is shared schema:

- `~/.loopany/daemon.pid` — `<pid>:<startTime>` for down/status/up idempotency.
- `~/.loopany/` device token file — read for device verbs.
- `~/.loopany/skill/` — generated public skill bundle (gitignored, never committed).
- Loop folders on disk — each loop's worktree/task file, watched by `watcher.ts`.

## API Contracts

The daemon consumes the server's machine API:

- `POST /api/machine/poll` — claim runs, fetch watch set + config.
- `POST /api/machine/sync` + `PUT /api/machine/blob/:hash` — artifact sync (device token).
- `POST /api/machine/cli` — all owner + run verbs, body `{argv, token}`; response `{text, exitCode, loops?, runs?}`.
- `POST /agent-api/loop` — legacy run transport fallback on a 404 from the unified CLI.
- `POST /api/claim/progress` — creation milestone reporting (`progress` verb).

## Sequences

### Detached up (idempotent)

```
loopany up → runEnsure({force?})
  ├─ consult pidfile (reused pid never reads as live)
  ├─ ensureBinShim (durable PATH shim, never clobbers foreign)
  ├─ refreshHooks (best-effort, durable command only)
  ├─ install skill for SKILL_TARGET_AGENTS (best-effort)
  └─ spawn detached daemon with token via ENV, re-exec --server-url/--api-key
```

### In-run callback

```
agent: loopany report --status resolved …
  → classify → callback → postCli(argv, run token)
  → POST /api/machine/cli → print body.text + exitCode
  → 404 (old server) → legacyRun → POST /agent-api/loop
```

### Transient-failure resume

```
claude exits non-zero → classifyFailure
  ├─ auth/quota > poisoned > transient > task precedence
  └─ transient (API error/ECONNRESET/5xx/rate limit) →
       claude --resume <sessionId> + buildResumeTask continuation prompt
       (max LOOPANY_TRANSIENT_RETRIES, backoff LOOPANY_TRANSIENT_RETRY_BASE_MS ×4 + jitter)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Routing | Pure `classify(argv, env)` in `route.ts` | Unit-testable without hanging a subprocess; `<verb> --help` inherits no-side-effect |
| Credential selection | Run token from env wins over device token | One client behind both CLI worlds (`cli-client.ts`) |
| Server-verb output | Print `body.text` + `exitCode`; text-less server → `SERVER_TOO_OLD` | Daemon is a pure text sink; batch 7 retired the structured fallback |
| Agent spawn | Branch on `loops.agent` (claude/codex/grok) with per-agent flags + env | BYOA and vendor-neutral execution |
| Resume | `--resume` forks the session id; spend summed across attempts | Recovers from provider blips without redoing work |
| Jail | `LOOPANY_ROOTS` resolve-normalized prefix check | Server-sent roots can only narrow the local jail |
| Installers | Best-effort skill install + shared JSON SessionStart hook merge | Never blocks `up`; each agent has a concrete installer |
| PATH shim | Version-consistent re-exec wrapper; `SHIM_MARKER` detection | Never clobbers a foreign `loopany`; ephemeral npx entries skipped |

## Risks and Unknowns

1. The daemon executes the user's coding agent with their credentials; it is the highest-permission surface and the security hardening focus.
2. Non-Claude telemetry is degraded: grok and codex streams are not Claude stream-json, so live progress/cost/transcript parse awaits per-agent stream adapters.
3. The daemon npm release and server deploy must be coordinated when wire-format changes ship (batch gating).

## Out of Scope

- Server-side scheduling and storage (server features cover those).
- Multi-agent stream adapters for grok/codex live progress (a noted follow-up).
