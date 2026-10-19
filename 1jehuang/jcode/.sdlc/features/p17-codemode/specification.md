---
title: "Codemode"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Specification: Codemode

## Overview

Codemode is implemented in two places.
`crates/jcode-codemode` is the sandbox crate, and it holds the embedded QuickJS runtime, the `Host` trait that bridges the sandbox to the harness, the `Limits` type, and the `run` entry point.
`crates/jcode-app-core/src/tool/codemode.rs` is the harness side, and it holds the `codemode` tool, the `RegistryHost` implementation that routes script calls through `Registry::execute`, the per-session store on disk, and the report renderer.
The script is evaluated as the body of an async function, a prelude installs the `tools` proxy and the discovery helpers, and every tool call is marshalled back to the caller's Tokio runtime through the `Host` trait.
This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
model turn
   │ tool call: codemode { code }
   ▼
crates/jcode-app-core/src/tool/codemode.rs   (CodemodeTool)
   │  ├─ loads the session tool definitions (Registry::definitions_for_session)
   │  │    └─ drops "codemode" and "batch"
   │  ├─ loads the session store (~/.jcode/codemode/<session>.json)
   │  └─ calls jcode_codemode::run(code, host, tools, store, limits)
   ▼
crates/jcode-codemode/src/engine.rs   (QuickJS engine)
   │  ├─ dedicated thread "jcode-codemode" plus a current-thread Tokio runtime
   │  ├─ QuickJS runtime: heap limit, 1 MB stack, interrupt handler (deadline and cancel flag)
   │  ├─ prelude: console, tools proxy, callTool, listTools, describeTool, store/load/storedKeys
   │  └─ __callTool → Host::call_tool → spawn on the caller's runtime
   ▼
Host::call_tool  (RegistryHost)
   │  └─ Registry::execute(name, args, sub_ctx)
   ▼
built-in tools, MCP tools, tool hooks, session allow and deny policy
```

The script runs inside the harness process, not inside the process that `bash` runs in.
It has no filesystem, network, timer, or process API.
The only way out of the sandbox is a tool call, and the harness routes that call through its normal registry and session policy.

## Data Models

### `Host` trait (`crates/jcode-codemode/src/lib.rs`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| call_tool | `fn(&self, name: String, args: Value) -> BoxFuture<'static, Result<Value, String>>` | required | Executes a tool on behalf of the script. `Ok` carries the decoded result and `Err` becomes a thrown `Error` inside the script. |

The trait is `Send + Sync + 'static`, so the harness can hold it across threads even though the JavaScript engine is not `Send`.

### `ToolInfo`

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | not null | The name the script uses to call the tool. |
| description | string | not null | The full tool description, returned by `describeTool`. |
| input_schema | JSON value | not null | The JSON Schema of the tool arguments, returned by `describeTool`. |

`listTools` returns only the name and the first non-empty line of the description, capped at 200 characters.

### `Limits`

| Field | Type | Constraints | Description |
|---|---|---|---|
| memory_bytes | usize | not null | The QuickJS heap limit in bytes. The default is 64 MB. |
| timeout | Duration | not null | The wall-clock limit for the whole script, including awaited tool calls. The default is 300 s. |
| max_tool_calls | usize | not null | The maximum number of tool calls per run. The default is 2000. |
| max_log_bytes | usize | not null | The maximum number of bytes of captured `console` output. The default is 64 KB. |

### `RunOutput`

| Field | Type | Constraints | Description |
|---|---|---|---|
| result | optional JSON value | not null | The JSON value the script returned, and `None` for `undefined`. |
| error | optional string | not null | The error message when the script threw, timed out, or was cancelled. |
| logs | list of strings | not null | The captured console lines. |
| logs_truncated | bool | not null | Whether log capture hit `max_log_bytes`. |
| tool_calls | usize | not null | The number of tool calls the script made. |
| store | map of string to JSON value | not null | The session store after the run, persisted by the caller between runs. |
| elapsed | Duration | not null | The wall-clock duration of the run. |

### `CodemodeInput` (`crates/jcode-app-core/src/tool/codemode.rs`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| code | string | required, aliases `script`, `source`, and `js` | The body of the async JavaScript function to run. |

## API Contracts

This feature defines no HTTP API, so there is no `api.yaml` alongside this document.
The contract is the tool schema the model sees and the script API that the prelude installs.

### `codemode` tool schema

| Field | Type | Required | Description |
|---|---|---|---|
| code | string | yes | The body of an async JavaScript function. Use `await` and `return`. |
| intent | string | no | The shared per-call intent string that every jcode tool accepts. |

### Script API

| Global | Kind | Description |
|---|---|---|
| `tools` | Proxy | `tools.<name>(args)` calls a tool. The `in` operator reports whether a tool exists, and `Object.keys(tools)` lists the tool names. |
| `callTool(name, args)` | async function | Calls a tool whose name is not a valid identifier. |
| `listTools(filter?)` | function | Returns `[{name, description}]`, optionally filtered by a case-insensitive substring of the name or the description. |
| `describeTool(name)` | function | Returns `{name, description, input_schema}` for one tool, or `undefined` when the tool is unknown. |
| `store(key, value)` | function | Writes a JSON value into the session store and returns it. |
| `load(key)` | function | Reads a JSON value from the session store, or `undefined` when the key is absent. |
| `storedKeys()` | function | Returns the keys currently in the session store. |
| `console.log`, `console.info`, `console.warn`, `console.error`, `console.debug` | functions | Appends to the captured console buffer. |

### Failure modes

| Condition | Code | Description |
|---|---|---|
| Empty script | `code is empty` | The `code` argument was blank. |
| Unknown tool | `unknown tool '<name>'` | The script called a tool that is not exposed to the session. The message lists similar names and points at `listTools()`. |
| Tool call limit | `tool call limit reached (N per run)` | The run made more tool calls than `max_tool_calls`. |
| Invalid arguments | `arguments are not JSON` or `arguments must be an object, got <value>` | The script passed arguments the harness could not dispatch. |
| Tool failure | `<tool>: <error>` | The host tool returned an error, and the script sees a thrown `Error`. |
| Timeout | `timed out after <N>s` | The wall-clock limit was reached. |
| Cancelled | `cancelled` | The run future was dropped. |
| Out of memory | `<message> (memory limit reached)` | The QuickJS heap limit was reached. |
| Unsupported platform | `codemode is not available on FreeBSD builds` | The build has no QuickJS engine. |

## Sequences

### The model writes a script and the harness runs it

```
Model → codemode { code }
  → CodemodeTool::execute
      → load the session tool definitions, minus "codemode" and "batch"
      → load the session store
      → jcode_codemode::run
          → spawn the thread "jcode-codemode"
              → build a current-thread Tokio runtime
              → create the QuickJS runtime and apply the heap and stack limits
              → install the globals and evaluate the prelude
              → evaluate "(async () => { <code> })()"
          → await the thread's result
      → save the session store
      → render the report
  → ToolOutput { report, title "codemode: N calls" }
```

### A script calls a tool

```
Script → tools.<name>(args)
  → __callTool(name, JSON.stringify(args))
      → check that the tool is exposed to the session
      → check the tool call limit
      → Host::call_tool(name, args)
          → RegistryHost → Registry::execute(name, args, sub_ctx)
              → the built-in or MCP tool, under session policy and hooks
      → spawn the host future on the caller's runtime
  → { ok: true, value } or { ok: false, error }
  → the prelude throws an Error when ok is false
```

### The script returns a value

```
Script → return value
  → the async function promise resolves
  → JSON.stringify(value)
  → serde_json parse
  → RunOutput.result
  → render_report
      → the console lines
      → the result, pretty printed, with strings kept raw
      → the footer: tool call count, elapsed seconds, stored keys
  → the report is truncated to the report budget
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Own workspace crate for the sandbox | `crates/jcode-codemode` | The QuickJS C build compiles once and is cached, and app-core edits do not recompile it. |
| Embedded QuickJS through `rquickjs` | rquickjs 0.14 with the `futures` feature | A small embeddable engine with no external runtime to install. |
| Thread-confined engine with a spawned host bridge | A dedicated thread plus a current-thread runtime, and host calls spawned on the caller's runtime | QuickJS runtimes are not `Send`, but host futures only need to be `Send`. |
| Only the harness registry is reachable | `RegistryHost` calls `Registry::execute` | Session policy, hooks, and MCP routing keep working inside a script. |
| `codemode` and `batch` are not reachable from a script | The `EXCLUDED` list | It avoids recursion, and `Promise.all` already covers what `batch` does. |
| Per-session store on disk | `~/.jcode/codemode/<session>.json`, written to a temp file and then renamed | The store survives a restart, and the rename keeps the file from being left half written. |
| A report budget with an explicit truncation marker | 60 000 characters, plus a message telling the model to return a smaller value | A single tool result has to stay inside the model context. |
| The engine is an optional dependency per target | `cfg(not(target_os = "freebsd"))` | rquickjs-sys ships no prebuilt FreeBSD bindings, and building them needs libclang. |
| Opt-in by default | `[tools] codemode = false` in the default config | The mode is experimental and it changes how the model spends its turns. |

## Risks and Unknowns

1. The per-run limits and the report budget are hard-coded, so there is no way to tune them without a rebuild.
2. A script can still call any tool the session allows, including destructive ones, so the tool-level permission model is the only guard.
3. The store file is named after a sanitized session id, so two sessions whose ids sanitize to the same string would share one store file.
4. QuickJS interruption is polled, so a script stuck in a single long-running operation may only be stopped at the next interrupt point.
5. The QuickJS C build lengthens the build for every new contributor, and it is the reason the engine cannot be enabled on FreeBSD today.
6. The sandbox runs in the harness process, so a script that drives many expensive tools can consume the same resources as the harness itself.

## Out of Scope

- A remote or networked sandbox.
- Adding filesystem, network, timer, or process APIs to the script environment.
- Streaming partial results from a running script back into the transcript.
- Configuring the per-run limits or the report budget through the config file.
- Making the `codemode` tool available by default.
- Replacing the `batch` tool, which keeps its own behavior.
