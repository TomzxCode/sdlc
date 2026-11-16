---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### The pinned ACP SDK version is stale

- Status: BLOCKING
- Evidence:
  - The Overview line 14 says the bridge speaks the protocol "using `@agentclientprotocol/sdk` 1.8.0".
  - The Technical Decisions table line 357 says "NDJSON over stdio, using `@agentclientprotocol/sdk` 1.8.0".
  - `package.json:2437` declares `"@agentclientprotocol/sdk": "2.1.0"`.
- Artifact currently says: the SDK is pinned at 1.8.0.
- What the code actually does: the dependency resolves to 2.1.0 in the root manifest.
- Needed change: update both references to name version 2.1.0.

### The route binding index file does not exist

- Status: BLOCKING
- Evidence:
  - The Overview line 22 names `src/routing/route-binding-index.ts` as the module that buckets bindings for lookup.
  - The Architecture diagram line 53 defines node `IDX[route-binding-index.ts]`.
  - The inbound routing sequence lines 339 and 344 declare a `route-binding-index` participant and send `getEvaluatedBindingsForChannelAccount` to it.
  - No file named `route-binding-index.ts` exists under `src/routing/`.
  - `getEvaluatedBindingsForChannelAccount` is defined inline in `src/routing/resolve-route.ts:209`, with `buildEvaluatedBindingsIndex` and a `WeakMap` cache in the same file.
- Artifact currently says: lookup bucketing lives in a separate `route-binding-index.ts` module.
- What the code actually does: `resolve-route.ts` owns both the ordered candidate list and its lookup index in one cache generation.
- Needed change: remove the separate module from the overview, diagram, and sequence, and attribute the index to `resolve-route.ts`.

### The ledger budget constants are in the worker, not the types module

- Status: ADVISORY
- Evidence:
  - The Replay ledger budgets heading line 150 cites `src/acp/event-ledger.types.ts` as the source.
  - `src/acp/event-ledger.types.ts` defines ledger types and replay helpers, but no budget constants.
  - `src/acp/event-ledger.worker.ts:28-30` defines `MAX_SESSIONS = 200`, `MAX_EVENTS_PER_SESSION = 5_000`, and `MAX_SERIALIZED_BYTES = 16 * 1024 * 1024`.
- Artifact currently says: the budget defaults are declared in `event-ledger.types.ts`.
- What the code actually does: the budgets are declared in `event-ledger.worker.ts` and the values match the documented defaults.
- Needed change: repoint the heading citation at `src/acp/event-ledger.worker.ts`.

### The API summary omits three ACP chat actions

- Status: ADVISORY
- Evidence:
  - The API Contracts table line 244 lists twelve `/acp` actions.
  - `src/auto-reply/reply/commands-acp.ts:16-35` also registers reset-options, doctor, and install.
- Artifact currently says: the `/acp` chat surface has exactly the twelve listed actions.
- What the code actually does: reset-options, doctor, and install are available on the same surface.
- Needed change: add the three actions to the summary row or note that the row is a subset.
