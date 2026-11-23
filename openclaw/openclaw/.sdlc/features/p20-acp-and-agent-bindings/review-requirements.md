---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-23
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-23

Fresh comparison against current code.
Both findings from the 2026-11-16 section still hold.
No new requirement discrepancies were found.

### The pinned ACP SDK version is still stale

- Status: BLOCKING
- Evidence:
  - requirements.md:65 says the Agent Client Protocol SDK is pinned at version 1.8.0.
  - package.json:2442 declares "@agentclientprotocol/sdk": "2.1.0".
  - pnpm-lock.yaml:3408 resolves @agentclientprotocol/sdk@2.1.0.
- Artifact currently says: the pinned version is 1.8.0.
- What the code actually does: the pinned version is 2.1.0.
- Needed change: update the constraint line to name version 2.1.0.

### FR-13 still lists fewer ACP chat actions than the code exposes

- Status: ADVISORY
- Evidence:
  - requirements.md:48 lists twelve `/acp` actions.
  - src/auto-reply/reply/commands-acp.ts:16-34 registers those twelve plus reset-options, doctor, and install in ACP_ACTION_LOADERS.
  - src/auto-reply/reply/commands-acp.ts:36 includes doctor and install in ACP_PUBLIC_ACTIONS.
- Artifact currently says: FR-13 covers the `/acp` action set.
- What the code actually does: three more actions are reachable on the same surface.
- Needed change: add reset-options, doctor, and install to FR-13, or state that FR-13 covers only the session driving subset.
