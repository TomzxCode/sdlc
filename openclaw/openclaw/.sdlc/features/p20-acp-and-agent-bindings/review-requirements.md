---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### The pinned ACP SDK version is stale

- Status: BLOCKING
- Evidence:
  - The Constraints section line 65 says: "The Agent Client Protocol SDK is pinned at version 1.8.0."
  - `package.json:2437` declares `"@agentclientprotocol/sdk": "2.1.0"`.
  - No manifest in the repository pins 1.8.0.
- Artifact currently says: the SDK is pinned at version 1.8.0.
- What the code actually does: the dependency is pinned at 2.1.0 in the root manifest.
- Needed change: update the constraint line to name version 2.1.0 as the pinned SDK.

### FR-13 lists fewer ACP chat actions than the code exposes

- Status: ADVISORY
- Evidence:
  - FR-13 names the actions spawn, cancel, steer, close, sessions, status, set-mode, set, cwd, permissions, timeout, and model.
  - `src/auto-reply/reply/commands-acp.ts:16-35` registers all twelve of those plus reset-options, doctor, and install in `ACP_ACTION_LOADERS`.
  - The three extra actions are reachable through the same `/acp` command surface.
- Artifact currently says: the `/acp` command exposes exactly the twelve listed actions.
- What the code actually does: the command also exposes reset-options, doctor, and install, which drive option reset and backend diagnostics.
- Needed change: either add the three extra actions to FR-13 or state that FR-13 covers only the session driving subset.
