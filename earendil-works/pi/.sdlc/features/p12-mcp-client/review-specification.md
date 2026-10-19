---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The error contract omits the HTTP and OAuth error classes
- **Evidence:** `packages/mcp/src/transports/streamable-http.ts:132-142` defines `McpHttpError` with a `status` and a `body`, `:144-152` defines `McpAuthRequiredError` (401, carrying the `www-authenticate` header), and `:154-159` defines `McpSessionExpiredError` (404). All three are exported from `packages/mcp/src/index.ts:59-65`.
- **Evidence:** `packages/mcp/src/oauth/errors.ts:1-55` defines `OAuthError`, `OAuthIssuerMismatchError`, `OAuthInsecureEndpointError` and `OAuthRegistrationError`, all exported from `packages/mcp/src/oauth/index.ts:16-22`.
- **Artifact says:** The "Error codes shared across endpoints" table lists only `McpError`, `McpTimeoutError`, `McpAbortError`, `McpConnectionClosedError` and `McpOAuthAuthorizationRequiredError`.
- **Required change:** Add the missing classes to the contract table, with the HTTP status each one carries and the role it plays in the retry and sign-in paths (`packages/mcp/src/transports/streamable-http.ts:295-317` and `packages/mcp/src/oauth/flow.ts:452-482`).
- **Blocking:** yes, the error surface is part of the contract and callers branch on it.

### The `pi mcp` command and the extension's OAuth, log and manager modules are missing
- **Evidence:** `packages/coding-agent/src/extensions/mcp/` holds eleven modules: `index.ts` (1347 lines), `cli.ts` (594), `cli.lazy.ts` (2), `config.ts` (242), `log.ts` (69), `oauth.ts` (558), `resources.ts` (339), `runtime.ts` (454), `runtime.lazy.ts` (2), `tools.ts` (391) and `ui.ts` (259).
- **Evidence:** `packages/coding-agent/src/extensions/mcp/cli.ts:185-259` implements the `pi mcp` command, and `packages/coding-agent/src/extensions/mcp/ui.ts` implements the manager view used by `/mcp` in the TUI.
- **Artifact says:** The architecture diagram lists only `index.ts`, `tools.ts`, `resources.ts`, `config.ts` and `runtime.ts`, and the API Contracts table has no row for the command-line surface.
- **Required change:** Add the `pi mcp` command to the API Contracts table and the `cli.ts`, `oauth.ts`, `log.ts` and `ui.ts` modules to the architecture diagram, and record that the extension is a replaceable built-in (`packages/coding-agent/src/extensions/index.ts:13`).
- **Blocking:** yes, a shipped public surface is missing from the normative contract.

### `McpServerConfig` is not modeled
- **Evidence:** `packages/coding-agent/src/core/mcp-servers.ts:80-88` defines `McpStdioServerConfig` with `type`, `command`, `args`, `env` and `cwd`, `:137-148` defines `McpHttpServerConfig` with `type`, `url`, `headers`, `oauth` and `auth`, and `:59-78` defines the shared base fields `exposure`, `toolExposure`, `description`, `enabled` and `timeout`.
- **Evidence:** `packages/coding-agent/src/extensions/mcp/config.ts:65-72` defines `LoadedMcpConfig` with `servers`, `autoEnableCodemode`, `errors` and `projectConfig`.
- **Artifact says:** The `McpServerEntry.config` row says only "Command or URL plus enabled, exposure, toolExposure, timeout, and description".
- **Required change:** Model the server config, the stdio and HTTP shapes and their fields, and `LoadedMcpConfig`, so the contract covers `env`, `cwd`, `headers`, `oauth`, `auth` and `type`.
- **Blocking:** yes, the configuration contract is incomplete.

### The stateless and telemetry-free position is not stated
- **Evidence:** `packages/mcp/package.json` declares `cross-spawn` as its only runtime dependency, and `packages/mcp/src/` contains no database, SQL or telemetry code.
- **Evidence:** Persistence is delegated to a host-supplied `McpOAuthStateStore` (`packages/mcp/src/oauth/provider.ts:21-24`), and the package ships only `MemoryOAuthStateStore` (`packages/mcp/src/oauth/provider.ts:40-50`).
- **Artifact says:** Nothing about state, persistence or telemetry.
- **Required change:** State that the client core keeps no state and defines no telemetry facility, and that credential persistence is the host's responsibility.
- **Blocking:** no, advisory.

### The request timeout default differs between the core and the extension
- **Evidence:** `packages/mcp/src/client.ts:38` sets the core default to 30 000 ms, but `packages/coding-agent/src/extensions/mcp/runtime.ts:48` sets `DEFAULT_TIMEOUT_SECONDS = 60` and `packages/coding-agent/src/extensions/mcp/runtime.ts:363` always passes that value, so the core default never applies through the coding agent.
- **Artifact says:** The `McpClientOptions.requestTimeoutMs` row says "optional, defaults to 30000".
- **Required change:** Note that the coding agent always sets an explicit timeout, 60 seconds per server by default, configurable through the server entry's `timeout` field.
- **Blocking:** no, advisory, but it is the same gap as NFR-3 in `requirements.md`.

### `McpClientOptions` omits the client `title`
- **Evidence:** `packages/mcp/src/client.ts:47-52` extends `Implementation`, which carries `name`, `version` and an optional `title` (`packages/mcp/src/protocol/types.ts:12-16`), and `packages/mcp/src/client.ts:228` sends that `title` in `clientInfo`.
- **Artifact says:** The `McpClientOptions` table lists `name`, `version`, `capabilities`, `protocolVersion`, `requestTimeoutMs` and `roots`.
- **Required change:** Add the optional `title` field to the `McpClientOptions` table.
- **Blocking:** no, advisory.

## Open questions

- None. The code settles the open points the artifact leaves implicit: the OAuth error family, the HTTP error statuses, and the extension's module split.
