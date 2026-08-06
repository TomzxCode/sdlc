---
title: "Loopany Daemon & CLI"
status: done
---

# Test Plan: Loopany Daemon & CLI

## Scope

Testing the daemon's CLI routing, poll loop, agent spawning, transient resume, callback transport, cwd jail, pidfile, bin shim, skill/hook installers, watcher, and workflow execution. All external touches are injectable seams; no test needs a real process or network.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | CLI routing classifies every verb | argv matrix incl. bare, `up --foreground`, run-token callback | Correct `Route` kind per case |
| TC-2 | `<verb> --help` short-circuits before the handler | `up --foreground --help` | Per-verb help, no daemon launch |
| TC-3 | In-run bare `loopany` posts `home` | `LOOPANY_RUN_TOKEN` set, no args | Route `callback` with `home` |
| TC-4 | Out-of-run report/finish forward on the device credential | `loopany report …` outside a run | Route `forward`; server's run-only 403 reaches the agent |
| TC-5 | Unknown verb errors exit 2 | `loopany frobnicate` | Exit 2, never a backgrounded daemon |
| TC-6 | Poll loop builds the poll body | In-flight run vs idle | `wait:true` only while idle; heartbeat cadence otherwise |
| TC-7 | Poll delay after a server hold vs a fast answer | Consumed vs instant interval | 250ms breather vs sleep out `POLL_MS` |
| TC-8 | Agent spawn branches on the coding agent | Loop with `agent` claude-code / codex / grok | Correct binary, flags, and env per agent |
| TC-9 | Transient-failure classification and resume | Crashes of each class | Only transient retries, `--resume` + continuation prompt, attempt cap |
| TC-10 | Spend is summed across resume attempts | Multi-attempt run | Report carries summed cost; `attempts` only when > 1 |
| TC-11 | Cwd jail narrows server-sent roots | Root outside `LOOPANY_ROOTS` | Resolve-normalized prefix check rejects |
| TC-12 | Child env is allowlisted | Spawned process | Only allowlisted keys pass through |
| TC-13 | Pidfile records pid+startTime and survives a reused pid | Fresh pidfile / stale pid | `down`/`status`/`up` idempotency correct |
| TC-14 | Bin shim writes only our own shim | Foreign `loopany` present | Never clobbers; `{path,onPath,written}` accurate |
| TC-15 | Skill install covers every target agent | `SKILL_TARGET_AGENTS` set | `npx skills add … -a claude-code -a codex -g` invoked per agent |
| TC-16 | SessionStart hook install merges per agent | Claude/Codex/Grok installers | Shared JSON merge routine; codex surfaces the trust step |
| TC-17 | Server verbs print text + exitCode | Stub server returning TOON body | Non-empty stdout via callback boundary |
| TC-18 | Text-less old server surfaces `SERVER_TOO_OLD` | Stub returning no `text` | Definitive error, exit 1 (home prints `tooOldHome` exit 0) |
| TC-19 | `progress` posts creation milestones | `progress <step> --connect-key <key>` | Best-effort POST, always exit 0 |
| TC-20 | Workflow subprocess runs the async function body | Valid body / `export` body | Executes; a `/SyntaxError/` body is a user-fix case |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-21 | Timeout crash (wall-clock guard) | Never retries; our guard, not a provider blip |
| TC-22 | No captured session to resume | Run stops immediately, no retry |
| TC-23 | Abort during a run | Stops immediately |
| TC-24 | Workflow failure | Falls back to the agent with the original task + failure context; cursor never advances |
| TC-25 | Report after lease already retired | `report()` logs a clear 401 line, never silently drops |
| TC-26 | `ensureBinShim`/`refreshHooks` under test | Inject seams; never writes the real `~/.claude/settings.json` or `~/.local/bin` |

## Test Infrastructure

- vitest with injected fs/env/process/network seams (no real processes or network).
- Stub servers for the callback/CLI transport boundaries.
- `ensure.test.ts` `seams()` no-ops bin-shim/hook writers; every setup/bin-shim test injects seams.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-6, TC-7 |
| FR-3 | TC-3 |
| FR-4 | TC-8 |
| FR-5 | TC-9, TC-10 |
| FR-6 | TC-17, TC-18 |
| FR-7 | TC-11, TC-12 |
| FR-8 | TC-15 |
| FR-9 | TC-16 |
| FR-10 | TC-13 |
| FR-11 | TC-14 |
| FR-12 | TC-4 |
| FR-13 | TC-19 |
| NFR-1 | TC-12 (env-only credential) |
| NFR-2 | TC-18 |
| NFR-3 | TC-26 |
| NFR-4 | all seam-injected tests |
| NFR-5 | TC-7 |
| NFR-6 | bounded home fetch covered by `home.test.ts` |
