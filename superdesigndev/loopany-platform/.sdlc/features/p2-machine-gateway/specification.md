---
title: "Machine Gateway & BYOA Execution"
status: done
---

# Specification: Machine Gateway & BYOA Execution

## Overview

`MachineGateway` (`gateway/index.ts`) is the run-lifecycle core and the machine wire boundary. It is decomposed into three gateway classes sharing one boot-time blob store and the leaf module `gateway/http.ts` for wire plumbing: `MachineGateway` (poll/report/sweep/owner verbs/presence), `CliGateway` (unified `/api/machine/cli` router + legacy dispatch), and `ArtifactSync` (byte ingress, covered by the artifact feature). `gateway/validate.ts` is the single validator both write surfaces import.

## Architecture

```
daemon ──POST /api/machine/poll──► MachineGateway.poll / pollWait (long-poll waiter)
daemon ──POST /machine/report────► MachineGateway.report (finalize, retire lease)
daemon ──POST /api/machine/sync──► ArtifactSync.sync (manifest reconcile)
daemon ──PUT /api/machine/blob──► ArtifactSync.putBlob
agent  ──POST /api/machine/cli──► CliGateway.cli (credential router → finalizeCli)
agent  ──POST /agent-api/loop───► CliGateway.agentApi (legacy dispatch)
```

All routes share `machineRouteLimit` (per-IP + per-token token buckets) except the byte-ingress routes (sync/blob), which require a valid device token and are handshake-bounded.

## Data Models

### machines

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | `m-sha256(deviceToken)[:16]` |
| userId | text | not null | Owning user |
| teamId | text | nullable | Owning team |
| tokenHash | text | not null | Hash of the device token |
| token | text | nullable | Plaintext device token (owner re-show, documented exception) |
| lastSeen | text (ISO) | nullable | Freshness stamp |
| online | boolean | default false | Presence flag |

### runLeases

| Field | Type | Constraints | Description |
|---|---|---|---|
| tokenHash | text | PK | sha256 hex of the wire token (`rk_…` or legacy bare UUID) |
| runId / loopId / machineId | text | not null | Run scope |
| role | enum | exec / evolve / edit | Run kind |
| allowControl / canSetUi / canSetSchema / canSetWorkflow / canFinish | boolean | default false | Per-run caps |
| state | enum | active / terminal-grace | Lease state machine |
| expiresAt | text | null while active | Terminal-grace bound |

## API Contracts

### POST /api/machine/poll

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| token | string | yes | `dk_` device token |
| wait | boolean | no | Opt into the server-held long-poll |
| watchDigest | string | no | Echoed watch cache digest |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| runs | Run[] | Pending runs to claim (each carrying its run token + instructions) |
| watch | LoopFolder[] | Loop folders to sync (omitted when the digest matches) |
| watchDigest | string | Current digest |
| machine | object | Presence + daemon-version config |

### POST /api/machine/cli

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| argv | string[] | yes | CLI verbs + flags |
| token | string | yes | `dk_` device token or `rk_` run credential |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| text | string | axi TOON render (the daemon prints this verbatim) |
| exitCode | number | 0/1/2 per verb outcome |
| loops / runs | array | Retained data channels for client-side resolution / `--json` |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | VALIDATION_ERROR | Invalid flags/status |
| 403 | — | Owner-only verb on a run credential; cross-loop retarget |
| 404 | — | Unknown machine / cross-scope log |
| 409 | — | Terminal-grace lease refusing mutations |
| 413 | — | Body over 2MB cap |
| 429 | — | Rate limited |

## Sequences

### Run lifecycle

```
tick → addRun(pending) → dispatcher.dispatch → wakeMachine (parked waiter resolves)
daemon poll (wait:true) → claims pending run, mints run lease (active)
daemon spawns agent → in-run verbs via CliGateway.dispatch (run credential)
agent report() → MachineGateway.report finalize → retireLease → push notify
```

### Sweep reclaim

```
sweep(): stale running run (RUN_TIMEOUT_MS silence) → reclaimRun → terminalizeLease (terminal-grace, 24h)
late wake-report: phase=="error" && lease.state=="terminal-grace" → honor ONE reconciling report
  success → flip back to done + retract via success push; real failure → replace generic reason
offline machine with pending → hold (deferred); DEFERRED_MAX_MS backstop → outcome skipped
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Run credential | Durable lease keyed by sha256(wire token) | Deploy/sleep-proof; a DB leak never exposes live credentials |
| Deferral vs failure | Hold pending; supersede on next fire | A sleeping laptop is the usual cause; catch-up on reconnect |
| Terminal-grace | One reconciling wake-report for swept runs | The sweep rarely means real failure; a late success must win |
| Stateless poll | HTTP short-poll + opt-in long-poll | No WS infra; near-zero dispatch latency when idle |
| Rate limiting | Per-IP + per-token token buckets | Forged-token floods share one IP bucket; per-machine fairness |
| CLI router | Credential-type-first branching (`dk_` prefix vs run-lease lookup) | Owner vs run authority is decided before any verb |
| Watch cache | Per-machine, digest-echoed, `WATCH_CACHE_TTL_MS` | Omission requires the echo; an absent `watch` means unchanged |
| Shared blob store | One instance across gateway/sync/cli | Two instances would let retention GC bytes sync never wrote |

## Risks and Unknowns

1. The device token fully impersonates its machine; plaintext storage is a documented trust-model exception for owner re-show.
2. Global `fetch` re-resolves DNS on connect for webhooks (no socket pinning); bounded by the host allowlist in `webhookGuard.ts`.
3. Per-owner machine/loop quotas are a noted follow-up, not yet implemented.

## Out of Scope

- Executing the agent (daemon-side).
- Artifact byte ingress (covered by the artifact sync feature).
- WebSocket connectivity (long-poll is the ceiling).
