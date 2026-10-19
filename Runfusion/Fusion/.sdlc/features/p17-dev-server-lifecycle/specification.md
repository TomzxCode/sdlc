---
title: "Dev Server Lifecycle Management"
status: done
---

# Specification: Dev Server Lifecycle Management

## Overview

The dev-server feature is a dashboard-owned subsystem in `@fusion/dashboard` with two layers.
The server layer is the canonical `dev-server-*` family under `packages/dashboard/src`: `dev-server-detect.ts` ranks candidate scripts, `dev-server-store.ts` persists state and configuration to `.fusion/dev-server.json`, `dev-server-port-detect.ts` parses preview URLs and probes fallback ports, `dev-server-process.ts` owns the child process lifecycle, and `dev-server-routes.ts` exposes the `/api/dev-server/*` routes including the server-sent events log stream.
The client layer is the React Dev Server view, lazy-loaded into the right dock behind the `devServerView` flag, with `useDevServer` for session and status, `useDevServerLogs` for paginated live logs, `usePreviewEmbed` for iframe embed detection, `DevServerLogViewer` for the log panel, and `PreviewIframe` for the live preview.
A second module family (`devserver-detect.ts`, `devserver-manager.ts`, `devserver-persistence.ts`, `devserver-types.ts`) exists in the same package with multi-server session types and a second persistence file, but nothing in the production import graph reaches it.

## Architecture

```
                        ┌──────────────────────────────────────────────┐
   Dashboard SPA        │  Right dock (overflowViewRegistry)           │
   (React 19)           │    └── DevServerView      [devServerView]    │
                        │          ├── DevServerLogViewer               │
                        │          └── PreviewIframe                    │
                        │    hooks: useDevServer / useDevServerLogs /   │
                        │           usePreviewEmbed / useDevServerConfig│
                        └───────────────┬──────────────────────────────┘
                                        │ HTTP + SSE  (/api/dev-server/*)
                        ┌───────────────▼──────────────────────────────┐
   @fusion/dashboard    │  dev-server-routes.ts  (createDevServerRouter)
   (Express 5)         │    GET  /detect      GET  /config  PUT /config│
                        │    GET  /status      POST /start  POST /stop  │
                        │    POST /restart      PUT  /preview-url        │
                        │    GET  /logs/stream  (text/event-stream)      │
                        └───────────────┬──────────────────────────────┘
                                        │
              ┌─────────────────────────┼──────────────────────────┐
              │                         │                          │
   ┌──────────▼─────────┐   ┌───────────▼───────────┐   ┌──────────▼─────────┐
   │ dev-server-detect  │   │ dev-server-process    │   │ dev-server-store   │
   │ .ts                │   │ .ts                   │   │ .ts                │
   │ script ranking     │   │ child process, logs,  │   │ .fusion/           │
   │ (confidence score) │   │ URL detection, stop   │   │ dev-server.json    │
   └──────────┬─────────┘   │ escalation            │   └──────────┬─────────┘
              │             └───────────┬───────────┘              │
              │                         │                          │
              │             ┌───────────▼───────────┐              │
              │             │ dev-server-port-detect│              │
              │             │ .ts                   │              │
              │             │ Vite/Next/Storybook/  │              │
              │             │ Angular parsers,      │              │
              │             │ fallback port probe   │              │
              │             └───────────────────────┘              │
              │                                                    │
              └────────────────┐              ┌────────────────────┘
                                │              │
                    ┌───────────▼──────────────▼───────────┐
                    │ @fusion/core  superviseSpawn         │
                    │ (detached process group, max 24 h)    │
                    └──────────────────────────────────────┘

  Disconnected family (no production importer):
    devserver-detect.ts, devserver-manager.ts,
    devserver-persistence.ts, devserver-types.ts
    -> .fusion/devserver.json, unit tests only
```

## Data Models

### DetectedScript

Produced by `detectDevServerScripts` and returned by `GET /api/dev-server/detect`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | not empty, one of `DEV_SERVER_SCRIPT_NAMES` | Script name from the manifest, for example `dev` |
| command | string | not empty | Full command string from the manifest `scripts` block |
| source | string | `root` or a project-relative directory path | Where the manifest was found |
| packageName | string | optional | The `name` field of the owning manifest |
| confidence | number | 0 to 1 | Rank score from script-name priority, framework dependency indicator, and the `private`/missing-`main` heuristic |

### DevServerState

The persisted runtime state. Stored under `state` in `.fusion/dev-server.json`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | may be empty | Server entry identifier |
| name | string | defaults to `default` | Display name |
| status | string | one of `starting`, `running`, `stopped`, `failed` | Current process status, normalized on load |
| command | string | may be empty | Command to execute |
| cwd | string | may be empty | Working directory of the command |
| scriptId | string | optional | Manifest script name the run was started from |
| packagePath | string | optional | Path of the manifest that owns the script |
| pid | number | optional | OS process id while running, cleared on stop and failure |
| startedAt | string | ISO timestamp, optional | When the process started |
| stoppedAt | string | ISO timestamp, optional | When the process stopped |
| exitCode | number | optional | Process exit code |
| detectedUrl | string | optional | Preview URL detected from output or probing |
| manualUrl | string | optional | Operator-set preview URL override |
| detectedPort | number | optional | Port detected from output or probing |
| logHistory | string[] | at most 500 entries, strings only | Ring buffer of recent output lines |

### DevServerConfig

The persisted operator configuration. Stored under `config` in `.fusion/dev-server.json`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| selectedScript | string | null or non-empty string | Selected script name |
| selectedSource | string | null or non-empty string | Source of the selected script, `root` or a relative path |
| selectedCommand | string | null or non-empty string | Full command of the selected script |
| previewUrlOverride | string | null or an `http://` or `https://` URL | Manual preview URL |
| detectedPreviewUrl | string | null or an `http://` or `https://` URL | Last auto-detected preview URL |
| selectedAt | string | null or ISO timestamp | When the selection was made |

### DevServerStatusResponse

The body returned by `GET /api/dev-server/status`. The `DevServerState` fields plus three resolved fields.

| Field | Type | Constraints | Description |
|---|---|---|---|
| previewUrl | string | null | Manual override when set, otherwise the detected URL |
| detectedPort | number | null | Detected port |
| manualPreviewUrl | string | null | The manual override on its own |
| isRunning | boolean | not null | Whether the manager holds a live child process |

### PortDetectionResult

Produced by `detectPortFromLogLine` and `probeFallbackPorts`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| url | string | `http://` or `https://`, host `localhost` or `127.0.0.1` | Normalized preview URL |
| port | number | 1 to 65535, never 4040 | The preview port |
| source | string | `vite`, `nextjs`, `storybook`, `angular`, `generic-url`, `generic-port`, or `fallback-probe` | Which parser or probe produced the result |

### DevServerUrlDetectedEvent

The payload of the `dev-server:url-detected` server-sent event.

| Field | Type | Constraints | Description |
|---|---|---|---|
| url | string | not null | The detected preview URL |
| port | number | not null | The detected preview port |
| source | string | not null | The detection source |
| detectedAt | string | ISO timestamp | When detection happened |

### DetectedDevServerCommand (client model)

The fields the dashboard client maps the backend candidates into.

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | not null | Script name |
| command | string | not null | Command to run |
| cwd | string | not null, `.` for the project root | Working directory to start in |
| scriptName | string | not null | Script name, equal to `name` |
| packagePath | string | not null | Manifest path, the cwd when the backend omits it |
| framework | string | optional | Framework matched from the command text |

### DevServerSession (client model)

The fields the dashboard client uses for a running server. It is produced by mapping the legacy state and is the target of the not-yet-registered `/api/devserver` session endpoints.

| Field | Type | Constraints | Description |
|---|---|---|---|
| config.id | string | not null | Session identifier, `default` for the mapped legacy state |
| config.name | string | not null | Session display name |
| config.command | string | not null | Command to run |
| config.cwd | string | not null | Working directory |
| status | string | one of `stopped`, `starting`, `running`, `failed`, `stopping` | Session status |
| runtime.pid | number | optional | OS process id |
| runtime.startedAt | string | ISO timestamp, optional | When the process started |
| runtime.exitCode | number | optional | Process exit code |
| runtime.previewUrl | string | optional | Preview URL known at start time |
| previewUrl | string | optional | Resolved preview URL |
| logHistory | array | at most 500 entries | Log entries with `timestamp`, `stream`, and `text` |

### DevServerConfig (secondary family, disconnected)

The config fields of the disconnected `devserver-*` family, persisted to `.fusion/devserver.json`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | branded `DevServerId`, not null | Config identifier |
| name | string | not null | Display name |
| command | string | not null | Command to run |
| cwd | string | not null | Working directory |
| env | object | optional, string values only | Extra environment variables |
| autoStart | boolean | optional | Whether the server starts with the dashboard |

## API Contracts

The normative contract is in [`api.yaml`](api.yaml) (OpenAPI 3.1).
The table below is a summary; request and response schemas and error response bodies are in `api.yaml`.
All routes are mounted under `/api/dev-server` by the `registerIntegratedDevServerRouter` registrar.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/dev-server/detect` | List ranked dev-server script candidates for the project |
| GET | `/api/dev-server/config` | Read the persisted dev-server configuration |
| PUT | `/api/dev-server/config` | Update part of the persisted dev-server configuration |
| GET | `/api/dev-server/status` | Read the current dev-server state and resolved preview URL |
| POST | `/api/dev-server/start` | Start the dev server in a working directory |
| POST | `/api/dev-server/stop` | Stop the running dev server |
| POST | `/api/dev-server/restart` | Restart the dev server with the stored command |
| PUT | `/api/dev-server/preview-url` | Set or clear the manual preview URL override |
| GET | `/api/dev-server/logs/stream` | Stream dev-server output as server-sent events |

Error responses use the shared dashboard error body, `{ "error": string, "details"?: object }`.
The body carries no machine-readable code, so the code column below names the condition.

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | A required field is missing, a field has the wrong type, or a URL is not `http://` or `https://` |
| 409 | CONFLICT | A dev server is already running |
| 500 | INTERNAL_ERROR | The command could not be started, stopped, or restarted |

The client additionally calls `/api/devserver`, `/api/devserver/:id`, `/api/devserver/:id/start`, `/api/devserver/:id/stop`, `/api/devserver/:id/restart`, `/api/devserver/:id/logs`, `/api/devserver/:id/preview`, `/api/devserver/detect`, `/api/devserver/:id/logs/stream`, `/api/dev-server/candidates`, and `/api/dev-server/logs/history`.
No router serves those paths today, so the client falls back to the canonical `/api/dev-server/*` routes.

## Sequences

### Detect

```
Client                Routes               dev-server-detect          Manifests
  |                      |                          |                      |
  | GET /detect          |                          |                      |
  |--------------------->|                          |                      |
  |                      | detectDevServerScripts   |                      |
  |                      |------------------------->|                      |
  |                      |                          | read package.json    |
  |                      |                          |--------------------->|
  |                      |                          |<-- root scripts ----|
  |                      |                          |                      |
  |                      |                          | glob packages/*     |
  |                      |                          |   and apps/*        |
  |                      |                          |--------------------->|
  |                      |                          |<-- workspace pkgs --|
  |                      |                          |                      |
  |                      |                          | score each script   |
  |                      |                          | (priority +         |
  |                      |                          |  framework +        |
  |                      |                          |  private heuristic) |
  |                      |                          | sort by confidence  |
  |                      |<----- candidates --------|                      |
  |                      |                          |                      |
  |<-- { candidates } ---|                          |                      |
```

### Start

```
Client        Routes          Process manager        Store            Child
  |             |                    |                 |               |
  | POST /start |                    |                 |               |
  |------------>|                    |                 |               |
  |             | validate command   |                 |               |
  |             | and cwd            |                 |               |
  |             | reject $() ` <()  |                 |               |
  |             | reject control ch  |                 |               |
  |             |                    |                 |               |
  |             | check isRunning -> 409 conflict      |               |
  |             |                    |                 |               |
  |             | manager.start()    |                 |               |
  |             |------------------->|                 |               |
  |             |                    | state = starting |               |
  |             |                    |---------------->|               |
  |             |                    |                 |               |
  |             |                    | superviseSpawn (shell: true)     |
  |             |                    |--------------------------------->|
  |             |                    |                 |  pid, status = running
  |             |                    |---------------->|               |
  |             |                    | emit "started"  |               |
  |             |<------- state -----|                 |               |
  |<-- 200 state|                    |                 |               |
  |             |                    |                 |               |
  |             |                    |<---- stdout ----|               |
  |             |                    | appendLog(line) |               |
  |             |                    |---------------->|               |
  |             |                    | detectPortFromLogLine(line)     |
  |             |                    |   -> detectedUrl, detectedPort   |
  |             |                    |---------------->|               |
  |             |                    | emit "url-detected"              |
  |             |                    |                 |               |
  |             |                    | (after grace period, if no URL)  |
  |             |                    | probeFallbackPorts()             |
  |             |                    |---------------->|               |
```

### Stop

```
Client        Routes          Process manager        Store            Child
  |             |                    |                 |               |
  | POST /stop  |                    |                 |               |
  |------------->|                    |                 |               |
  |             | if not running:    |                 |               |
  |             |   return state     |                 |               |
  |             |<-- 200 state -----|                 |               |
  |             |                    |                 |               |
  |             | manager.stop()     |                 |               |
  |             |------------------->|                 |               |
  |             |                    | SIGTERM to the process group    |
  |             |                    |-------------------------------->|
  |             |                    |                 |               |
  |             |                    | (stop timeout, 5 s)              |
  |             |                    | SIGKILL to the process group     |
  |             |                    |-------------------------------->|
  |             |                    | await close event                |
  |             |                    |<--------------------------------|
  |             |                    | clear probe timer                |
  |             |                    | state = stopped, exitCode,      |
  |             |                    | stoppedAt, pid cleared           |
  |             |                    |---------------->|               |
  |             |                    | emit "stopped"  |               |
  |             |<------- state -----|                 |               |
  |<-- 200 state|                    |                 |               |
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Canonical module family | The hyphenated `dev-server-*` family | It is the only family on the production import graph, mounted by `registerIntegratedDevServerRouter` and torn down by `stopAllDevServers` in `packages/dashboard/src/server.ts` |
| Persistence file | `.fusion/dev-server.json` with a `{ state, config }` payload | It is the file the canonical store writes and the only one the dashboard reads back |
| Child process launch | `superviseSpawn` with `shell: true` and a 24 hour maximum lifetime | The supervisor creates a detached process group, so a stop can tear down the shell wrapper and its descendants, and the lifetime caps a forgotten server |
| Command validation | Reject command substitution and control characters before spawning | The command is a project setting spawned through a shell, so substitution is the main payload of a settings-file compromise |
| Stop escalation | `SIGTERM` to the process group, then `SIGKILL` after 5 seconds | A dev server spawns grandchildren, so a single PID signal would leave the tree running |
| Preview URL discovery | Framework parsers first, generic parsers second, TCP probe last | Framework output is the most reliable source, the probe covers servers that print nothing |
| Reserved port | 4040 excluded from every detected and probed port | The dashboard itself serves on 4040 |
| Log history bound | 500 lines in the store and 500 entries in the client | Keeps the persisted file and the rendered panel bounded |
| Log transport | Server-sent events on `GET /logs/stream` with a 30 second heartbeat | The dashboard already uses server-sent events, and a long-lived HTTP stream avoids a polling loop |
| View placement | Right dock, lazy-loaded, gated by `devServerView` | Keeps the panel out of the main bundle and out of the way when the operator does not want it |
| Narrow dock preview | A modal launcher below 480 pixels of dock width | The inline preview crowds the configuration and log panels in a narrow dock |
| Preview sandbox | `allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox` | The preview renders a developer-controlled local app, and the fallback path lets the operator open it outside the frame |

## Risks and Unknowns

1. The client calls `/api/devserver/*` and `/api/dev-server/candidates` and `/api/dev-server/logs/history`, which no backend route serves. The client always takes its fallback path, so the intended owner of the session endpoint family is unresolved.
2. The `devserver-*` family and `dev-server-manager.ts` both carry capabilities the canonical path lacks, namely event buffering with replay and stale process id recovery. A fix can land in the wrong family and miss production.
3. The two families write two different files, `.fusion/dev-server.json` and `.fusion/devserver.json`, and they can drift.
4. The dev-server command is spawned with a shell, so a command with `&&` or a pipe is accepted, and the command substitution guard is a pattern check rather than a parser.
5. The preview iframe runs a developer-controlled local app with `allow-same-origin`, so a hostile page served on the preview origin could reach the dashboard origin. The blast radius is limited to a local development port.
6. The status response resolves the preview URL from the manual override, so a stale override can shadow a freshly detected URL until the operator clears it.
7. The Dev Server view hard-codes its manual-override flag to false, so the preview badge reports "Auto" even when the backend holds a manual override.

## Out of Scope

- Multi-server dev-server sessions. The `devserver-*` family models them but is not wired to the runtime.
- The engine mission verification app harness and the CLI dev-source restart command, which reuse the port-detection rules for their own purposes.
- A non-shell dev-server launcher, and any port other than 4040 being reserved.
- The preview embed restrictions of a specific framework, which the embed detector only reports.
