---
title: "Control Plane and Agent Tool"
status: done
---

# Specification: Control Plane and Agent Tool

## Overview

`openchamber-control` owns the typed control contract shared by the CLI and the managed `openchamber` OpenCode tool. `service.js` validates and executes the fixed action allowlist; `routes.js` is the authenticated CLI HTTP adapter; `agent-tool/runtime.js` is the managed-tool adapter that wraps results in the versioned native-tool envelope. Domain operations for sessions and scheduled tasks are owned by `openchamber-sessions` and `scheduled-tasks` and composed into the service.

## Architecture

```
CLI `openchamber control` ──HTTP POST /api/openchamber/control──> routes.js ─┐
                                                                             v
Managed OpenCode `openchamber` tool ──POST /api/openchamber/agent-tool──> agent-tool/runtime.js
                                                                             |
                                                                             v
                                                          createOpenChamberControlService() (service.js)
                                                                             |
                                   +-----------------------------------------+---------+
                                   v                     v                            v
                           openchamber-sessions     scheduled-tasks              (models/projects)
```

## Data Models

### Action allowlist

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | e.g. `session.dispatch`, `session.wait`, `session.status`, `schedule.list`, `schedule.toggle` |
| agentExposed | boolean | — | `false` for CLI-only actions (currently `schedule.status`) |

## API Contracts

### POST /api/openchamber/control

Authenticated CLI adapter. Forwards one action, preserves service status and partial-result details, and propagates request cancellation.

### POST /api/openchamber/agent-tool

Managed-tool adapter. Takes the typed tool input plus OpenCode's authoritative session directory, wraps results in the versioned native-tool envelope, and uses a separate ephemeral loopback credential.

## Sequences

### Inject and call the agent tool

```
1. OpenChamber binds HTTP listener and publishes its authoritative port.
2. prepareManagedOpenCodeEnv() materializes the plugin under <data-dir>/agent-tool/
   and appends its file:// URL to OPENCODE_CONFIG_CONTENT.
3. A random per-child token + loopback callback URL are added only to the child env.
4. The plugin POSTs /api/openchamber/agent-tool with typed input + session directory.
5. The route delegates the fixed allowlist to the shared control service.
6. Results return in the versioned native-tool envelope.
```

### Dispatch with wait

```
Agent/CLI: session.dispatch -> resolves scope (explicit > managed fallback) -> dispatches
Agent/CLI: session.wait -> polls observed activity / completed assistant message until timeout
Timeout/cancel -> failure, never authoritative idle completion.
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Single service | Both adapters call createOpenChamberControlService() | One owner for ordering, wait, partial failures, schedule contracts |
| Fixed allowlist | service.js validates actions; CLI-only flagged | Safety; agents see only a filtered contract |
| Scope precedence | Explicit projectId/directory wins over current-session fallback | Fallback never creates a conflicting second scope |
| Auth | CLI HTTP authenticated; agent tool uses ephemeral loopback credential | No shared secrets between adapters |
| Context budget | One shared parameter object; terse per-action descriptions | Small agent context footprint |

## Risks and Unknowns

1. Growing the allowlist adds surface for agents; each new action must be reviewed for safety.
2. Native-tool envelope versioning must be maintained across OpenCode SDK changes.

## Out of Scope

- Destructive session/worktree deletion and project-path registration
- Directly exposing the service over the public network (loopback only)
