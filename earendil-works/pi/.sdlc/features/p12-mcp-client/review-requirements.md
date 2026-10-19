---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The `pi mcp` command is not a requirement
- **Evidence:** `packages/coding-agent/src/extensions/mcp/cli.ts:185-259` implements `pi mcp` with the subcommands `add`, `remove`, `list`, `login`, `logout` and `help`, and `packages/coding-agent/src/extensions/mcp/cli.ts:33-73` documents their options.
- **Evidence:** `packages/coding-agent/src/main.ts:617` dispatches `pi mcp`, `packages/coding-agent/src/extensions/mcp/cli.lazy.ts:1` loads it lazily, and `packages/coding-agent/src/cli/args.ts:297` lists it in the CLI help.
- **Artifact says:** FR-17 covers only the `/mcp` manager inside a session. No requirement mentions the out-of-session command.
- **Required change:** Add a requirement for the `pi mcp` command: add, remove, list, login, and logout, with the `--local`, `--url`, `--env`, `--cwd`, `--header`, `--bearer-token-env-var`, `--oauth-*`, `--exposure`, `--description`, `--json` and `--timeout` options, and the behaviour that a running session picks up new credentials on its next turn.
- **Blocking:** yes, the requirement set does not cover a shipped, tested user-facing command.

### The extension's OAuth configuration and credential store are not stated
- **Evidence:** `packages/coding-agent/src/core/mcp-servers.ts:91-126` defines `McpOAuthConfig` with `clientId`, `clientSecret`, `callbackPort`, `callbackUrl`, `scope`, `clientName`, `clientRegistration` (`dcr` or `cimd`) and `authServerMetadataUrl`, and `packages/coding-agent/src/core/mcp-servers.ts:137-148` defines `auth: { provider }` for HTTP servers.
- **Evidence:** `packages/coding-agent/src/extensions/mcp/oauth.ts:141-224` stores per-server OAuth state in `<agent-dir>/mcp-auth.json` under the key `mcp__<server>|<url>`, with a cross-process refresh lock (`packages/coding-agent/src/extensions/mcp/oauth.ts:175-196`).
- **Artifact says:** FR-12 describes only the OAuth subset inside the client package, and FR-17 mentions signing in from the manager.
- **Required change:** State the extension's OAuth configuration surface (including `clientRegistration: "cimd"`, which selects pi's Client ID Metadata Document at `packages/coding-agent/src/extensions/mcp/oauth.ts:251-271`) and the persisted credential store, keyed by server name and URL.
- **Blocking:** yes, it changes the requirement contract for FR-12 and FR-17.

### The project `mcp.json` override mechanism and `autoEnableCodemode` are not stated
- **Evidence:** `packages/coding-agent/src/extensions/mcp/config.ts:9-12` and `packages/coding-agent/src/extensions/mcp/config.ts:74` define that a project entry without `command`, `url` or `type` overrides only `enabled`, `exposure` and `toolExposure` of the global server with the same name, and `packages/coding-agent/src/extensions/mcp/config.ts:105-106` reads the top-level `autoEnableCodemode`.
- **Artifact says:** FR-13 states only that `mcp.json` entries take precedence over extension-registered servers.
- **Required change:** State the global and trusted-project `mcp.json` layering, the three override keys, and `autoEnableCodemode`, which decides whether the codemode tool is activated for `codemode` servers.
- **Blocking:** yes, FR-13 describes a different precedence rule than the one implemented.

### NFR-3's 30 second default does not hold end to end
- **Evidence:** `packages/mcp/src/client.ts:38` sets `DEFAULT_REQUEST_TIMEOUT_MS = 30_000`, the client core default.
- **Evidence:** `packages/coding-agent/src/extensions/mcp/runtime.ts:48` sets `DEFAULT_TIMEOUT_SECONDS = 60`, and `packages/coding-agent/src/extensions/mcp/runtime.ts:211` and `packages/coding-agent/src/extensions/mcp/runtime.ts:363` always pass that value as `requestTimeoutMs`, so the core default is never used through the coding agent.
- **Artifact says:** NFR-3 states that the system shall default every request to a 30 second timeout.
- **Required change:** Scope NFR-3 to the client package and state the extension's own default, 60 seconds per server, configurable through the `timeout` field of the server entry (`packages/coding-agent/src/core/mcp-servers.ts:76-77`).
- **Blocking:** yes, the stated default contradicts the shipped behaviour of the coding agent.

### The client package is stateless and defines no telemetry
- **Evidence:** `packages/mcp/package.json` declares `cross-spawn` as its only runtime dependency, and `packages/mcp/src/` contains no database, SQL or telemetry code.
- **Evidence:** Token persistence is delegated to a host-supplied `McpOAuthStateStore` (`packages/mcp/src/oauth/provider.ts:21-24`), and the package ships only `MemoryOAuthStateStore` (`packages/mcp/src/oauth/provider.ts:40-50`).
- **Artifact says:** Nothing about persistence or telemetry.
- **Required change:** State that the package keeps no state, defines no telemetry facility, and leaves credential persistence to the host.
- **Blocking:** no, advisory.

### `toolExposure` accepts wildcard patterns
- **Evidence:** `packages/coding-agent/src/core/mcp-servers.ts:234-242` resolves an exact tool name first, then the first matching `*` pattern, and `packages/coding-agent/src/core/mcp-servers.ts:21-25` builds the matcher where `*` matches any characters.
- **Artifact says:** FR-15 mentions per-tool `toolExposure` without patterns.
- **Required change:** Mention that `toolExposure` keys are exact tool names or `*` patterns, and that an exact name wins over a pattern.
- **Blocking:** no, advisory.

### The server log file is not stated
- **Evidence:** `packages/coding-agent/src/extensions/mcp/log.ts:1-5` and `packages/coding-agent/src/extensions/mcp/log.ts:35-61` append the `notifications/message` payloads of MCP servers to `<agent-dir>/mcp.log`, rotating the file at 5 MiB, and `packages/coding-agent/src/extensions/mcp/runtime.ts:367` wires the log into the client.
- **Artifact says:** FR-7 mentions the generic notification subscription API only, and no requirement mentions a log file.
- **Required change:** Add the server log file to the requirements.
- **Blocking:** no, advisory.

### Open question 1 is answered by the code
- **Evidence:** `packages/coding-agent/src/core/mcp-servers.ts:270` rejects a server entry with `type: "sse"` with `legacy SSE transport is not supported; use the streamable HTTP URL`.
- **Artifact says:** Open question 1 asks whether any supported server will require the legacy HTTP+SSE transport.
- **Required change:** Close or reword open question 1: the coding agent refuses such entries outright, so the question now only concerns the client core.
- **Blocking:** no, advisory.

## Open questions

- Whether the client core should ever gain a legacy HTTP+SSE transport, now that the coding agent rejects `type: "sse"` entries.
- Whether the client should ever act as an MCP server (sampling), which open question 2 still asks and the code does not answer.
