# Project Overview

## Purpose

Loopany is infrastructure for recurring agent work: a multi-user, scheduled-loop manager where a server schedules, stores, authenticates, and notifies, while execution is bring-your-own-agent (BYOA) on each user's own machine. A user describes a recurring task once (a daily health check, a weekly digest, or a closed goal like "follow up until it's fixed"), and a small daemon on a machine they control runs it on schedule using their local coding agent (Claude Code, Codex, or Grok). The server enforces a zero-exec invariant: it runs no LLM and executes no user code, only storing/reading bytes and computing pure functions. The product's value is the structure that makes agent loops trustworthy at scale: durable cross-run state, self-improving (evolve) passes, a shared team dashboard with notifications, vendor-neutral BYOA execution, and a safe cheap control plane.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Loop owner | Developer or team lead who creates loops | Reliable scheduled agent runs, visible results on a dashboard, failure alerts, confidence to walk away |
| Loop operator | User who runs the daemon on their own machine | Low overhead daemon, BYOA with their own credentials, nothing leaves the box without consent |
| Team members | Users who see the shared dashboard and channel notifications | Results and failure alerts in the team surface, no need to operate machines |
| Server operator | Self-hoster or the hosted deployment operator | One-process deploy, embedded or hosted Postgres, zero-LLM control plane, secure auth |

## Scope

**In scope:**
- Cron and one-shot scheduling of agent runs bound to a machine.
- Open loops (indefinite monitors/digests) and closed loops (goal-bound, self-finishing).
- BYOA execution via the `@crewlet/loopany` daemon on user machines, spawning Claude Code, Codex, or Grok.
- Self-improvement (evolve) and owner-requested edit runs.
- Optional deterministic pre-stage workflows that run on the machine before the agent.
- Multi-user teams with per-team push notification channels (Telegram, Slack, Feishu).
- Live artifact sync from loop folders to durable content, rendered as a generative dashboard.
- A public template market with bundles and per-template flow specs.
- Guided onboarding with a live first-run and notification-binding flow.
- Self-hosting on one process with embedded pglite or hosted Postgres plus object storage.

**Out of scope:**
- Running LLMs or executing user code on the server (zero-exec invariant).
- Credentials or tools leaving the user's machine without the loop choosing to sync bytes back.
- WebSocket-based machine connectivity (stateless HTTP long-poll by design).
- Cross-machine fallback for a bound loop (execution is machine-pinned at creation).

## Key Constraints

- The server must never run an LLM and never execute user code; it only stores/reads bytes and computes pure functions.
- Machine identity derives from a device token; the device token fully impersonates its machine and must serialize owner-only.
- Run credentials are durable run leases so a deploy or long machine sleep never breaks an in-flight run's finalize.
- A run that no machine claims must be deferred or skipped, never falsely failed; a genuinely offline machine gets one calm notification.
- The single-scheduler invariant: exactly one process must own the cron loop against a given database, or runs double-fire.
- Migrations are forward-only; an image rollback does not roll back schema.
- Machine routes are rate-limited; blob byte-ingress routes are exempt because they require a valid device token and are handshake-bounded.
- Daemon machine identity is jailed to `LOOPANY_ROOTS`; child processes get an allowlisted environment.
- The daemon npm package must never ship internal run prompts or bootstrap content (selective skill sync whitelist).
