---
title: "ACP and Agent Bindings"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: ACP and Agent Bindings

## Scope

This plan covers the ACP bridge, the translator family, the ACP control plane, the ACP runtime registry, the ACP replay ledger, the ACP policy gates, the configured ACP bindings, the route binding resolution, and the session key forms.
It lists the existing test files that prove each requirement, so the coverage matrix maps a requirement onto the files that already exercise it.

Out of scope:

- The ACP runtime backend plugins themselves, including the `acpx` plugin and the Codex harness.
- The IDE clients that speak ACP, such as Zed.
- The channel adapters and their pairing, allowlist, and account policies.
- The Control UI agent roster screens.
- The `sessions_spawn` sub-agent path and the multi-agent orchestration rules.
- Live end-to-end tests through a real IDE; the ACP surface is exercised through the translator and control-plane layers instead.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | ACP policy treats ACP and ACP dispatch as enabled by default | A config with no `acp` block | The feature gate is open and the dispatch gate is open |
| TC-2 | ACP policy reports the disabled state when `acp.enabled` is false | A config with `acp.enabled: false` | The gate is closed and the message names `acp.enabled=false` |
| TC-3 | ACP policy allows explicit turns when only dispatch is disabled | A config with `acp.dispatch.enabled: false` | The feature gate stays open and the dispatch gate closes |
| TC-4 | ACP policy blocks explicit turns when ACP itself is disabled | A config with `acp.enabled: false` | The explicit-turn error carries the `ACP_DISPATCH_DISABLED` code |
| TC-5 | ACP policy applies the allowlist for ACP agents | A config with `acp.allowedAgents` set | A target outside the list is refused with `ACP_SESSION_INIT_FAILED` |
| TC-6 | Runtime registry throws a typed missing-backend error | An empty registry | `requireAcpRuntimeBackend` raises `ACP_BACKEND_MISSING` |
| TC-7 | Runtime registry resolves the first healthy backend when no id is given | Two registered backends, one unhealthy | The healthy backend is returned |
| TC-8 | Runtime registry throws a typed unavailable error for an unhealthy backend | One registered, unhealthy backend | `requireAcpRuntimeBackend` raises `ACP_BACKEND_UNAVAILABLE` |
| TC-9 | Runtime registry unregisters a backend by id | A registered backend | A later lookup no longer finds it |
| TC-10 | Runtime registry keeps the backend state on a global registry | A registry populated from another module loader | The backend is visible across loaders in the same process |
| TC-11 | ACP session store tracks an active run and clears it on cancel | A session with a bound run | The run is tracked and the abort controller fires on cancel |
| TC-12 | ACP session store deletes a session and aborts its active run | A session with a bound run | The session is removed and the run is aborted |
| TC-13 | ACP session store reports false when deleting a missing session | An unknown session id | The delete call returns false |
| TC-14 | ACP session store refreshes an existing session id instead of creating a duplicate | The same session id created twice | One session exists and its fields are updated |
| TC-15 | ACP session store evicts the oldest idle session when full | A store at its cap with one idle and one active session | The idle session is evicted and the active one is kept |
| TC-16 | ACP session store refuses to create a session when nothing is evictable | A store at its cap with every session active | The creation is refused with the session limit message |
| TC-17 | ACP session store reports every removal path through the callback | Delete, idle reap, capacity eviction, and dispose | The callback fires for each removed session id |
| TC-18 | Interaction mode reports a persistent session without parent linkage as interactive | A persistent ACP session with no parent | The interaction mode is interactive |
| TC-19 | Interaction mode matches the requester against the parent session | A background ACP session with `spawnedBy` and `parentSessionKey` | The requester is recognized as the parent, and a different requester is not |
| TC-20 | Replay helpers map plain user and assistant text into replay chunks | A transcript with user and assistant text | The text is mapped into user and agent message chunks |
| TC-21 | Replay helpers drop unsupported roles, empty text, and non-text content | A transcript with an unknown role and an empty message | The unsupported entries are dropped |
| TC-22 | Route binding account helpers keep the account order and the agent scope | A config with several bindings on one channel | The bound account ids are deduplicated and sorted, and the agent scope is preserved |
| TC-23 | Session key keeps a legacy agent id absent until a configured default resolves it | A legacy session key and a configured default agent | The key stays unscoped until the default resolves |
| TC-24 | Session key classifies an absent session key as missing | An empty session key | The key is classified as missing rather than malformed |
| TC-25 | Session key honors the configured main-key alias when scoping legacy keys | A config with a custom main key | The scoped key uses the configured main key |
| TC-26 | Session key does not double-prefix an already qualified agent key | A key that already carries the agent prefix | The key is returned unchanged |
| TC-27 | Session key preserves a conversation id that embeds a topic marker | A Feishu conversation id with `:topic:` | The stored key keeps the full id |
| TC-28 | Session key parses mixed-case thread and run markers without lowercasing | A key with a mixed-case `:thread:` marker | The stored key keeps its case and the marker is recognized |
| TC-29 | Session key does not strip a `:run:` segment from a non-cron key | A key with a `:run:` segment that is not a cron key | The segment is preserved |
| TC-30 | ACP command list advertises the thinking levels | The ACP command help text | The advertised thinking command includes the Ultra level |
| TC-31 | Channel route targets suppress the default targets covered by a channel route | A config with a channel-wide binding | The default target is suppressed for that channel |
| TC-32 | Channel route targets sample the configured accounts through the route resolver | A config with several accounts on one channel | Each configured account is resolved to its agent |
| TC-33 | Channel route targets do not treat a route binding channel alias as coverage | A binding that names a channel alias | The alias does not count as channel coverage |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-34 | ACP client rejects an unresolved Windows wrapper without running a shell | A server command that cannot be resolved on Windows | The client fails without executing a shell |
| TC-35 | ACP client cancels a pending permission when the interactive session closes | A pending permission request and a closed session | The permission is cancelled and the client exits cleanly |
| TC-36 | ACP client extracts text and resources within the byte budget | A prompt with text and embedded resources | The content is mapped within the budget |
| TC-37 | ACP client escapes separators and control characters in the extracted content | A prompt whose text carries separators and C0 and C1 control characters | The content is escaped so the mapping stays parseable |
| TC-38 | ACP client extracts only the nonempty image blocks into attachments | A prompt with a valid image block and an empty image block | Only the nonempty image becomes an attachment |
| TC-39 | ACP client escapes inline control characters in a tool title | A tool title with a newline | The title is escaped before it reaches the protocol |
| TC-40 | Translator session updates join the admitted ledger work and block reads and writes after shutdown starts | A running translator and a shutdown | The pending ledger work is joined and later reads and writes are refused |
| TC-41 | Translator session updates preserve the ledger order without waiting for ACP delivery | A slow ACP delivery and a fast ledger | The ledger order is preserved and the ledger does not wait for the client |
| TC-42 | Translator session updates do not let a stalled ledger session block another session | One stalled ledger session and one healthy session | The healthy session still records its updates |
| TC-43 | Translator lifecycle paginates the cwd-filtered sessions with lineage and a filter-bound cursor | Several ACP sessions across working directories | The list is filtered, paginated, and carries the lineage and safe timestamps |
| TC-44 | Translator lifecycle rejects a relative cwd filter for the session list | A relative working directory filter | The request is rejected |
| TC-45 | Translator lifecycle rejects a resume for a missing Gateway session | A resume for a session that does not exist on the Gateway | The resume is rejected and no bridge state is created |
| TC-46 | Translator lifecycle drains only its own pending work and sessions during shutdown | Two translators sharing a process | One shutdown does not drain the other's work |
| TC-47 | Permission relay relays a raw approval request once before the later agent approval event | A tool call that produces both events | The raw request is relayed once and the later event is not relayed again |
| TC-48 | Permission relay correlates concurrent approvals by the unique execute tool call and fails closed otherwise | Two concurrent approvals and one ambiguous approval | The unique call is correlated and the ambiguous one fails closed |
| TC-49 | Permission relay retries the recorded decision on a duplicate approval event | A duplicate approval event after a decision | The stored decision is replayed instead of asking again |
| TC-50 | Permission relay replays the user decision on a Gateway reconnect | A decided approval followed by a reconnect | The decision is replayed after the reconnect |
| TC-51 | Permission relay does not retry a stored decision after the prompt cleanup revokes the relay | A decided approval whose prompt was cleaned up | The decision is not retried |
| TC-52 | Permission relay does not allow execution when the prompt is cancelled during the client permission UI | A cancellation during the permission prompt | The execution is not allowed |
| TC-53 | Cancel scoping settles the shutdown when a superseded prompt abort never returns | A prompt whose abort never resolves | The shutdown still settles |
| TC-54 | Cancel scoping interrupts a blocked final snapshot | A blocked final snapshot | The shutdown interrupts it |
| TC-55 | Cancel scoping submits only the latest of three overlapping prompts | Three overlapping prompts | Only the latest is submitted |
| TC-56 | Cancel scoping does not replay a superseded prompt after a delayed provenance rejection | A superseded prompt rejected late | The superseded prompt is not replayed |
| TC-57 | Cancel scoping does not let a stale cancel completion remove a newer prompt | A stale cancel completion | The newer prompt is kept |
| TC-58 | Cancel scoping drops stale text from a final snapshot after a replacement | A replacement during thought delivery | The stale text is dropped from the snapshot |
| TC-59 | Cancel scoping routes only the matching run events when session keys are shared | Two runs under the same session key | Each run receives only its own events |
| TC-60 | Event ledger persists the replay through metadata changes and rejected replay bindings | A session whose metadata changes and a rejected binding | The replay survives the metadata change and the rejected binding is not replayed |
| TC-61 | Event ledger serializes appends from separate ledger handles | Two ledger handles appending to the same session | Both appends are committed and each committed replay is visible |
| TC-62 | Event ledger preserves the prompt history when a provisional ACP key becomes the canonical Gateway key | A session first written under a provisional key and then under the canonical key | The prompt history is preserved across the rename |
| TC-63 | Persistent bindings resolve a Discord ACP binding from the top-level typed bindings | A config with a typed ACP binding for a Discord conversation | The binding resolves to its spec and session key |
| TC-64 | Persistent bindings prefer an exact account binding over a wildcard | Two bindings for the same conversation, one exact and one wildcard | The exact account binding wins |
| TC-65 | Persistent bindings return no binding when no top-level ACP binding matches | A config with an unrelated ACP binding | The resolution returns nothing |
| TC-66 | Persistent bindings apply the agent runtime ACP defaults for bound conversations | A binding with no explicit model or backend | The agent runtime defaults fill the missing options |
| TC-67 | Persistent bindings return no spec for an unknown session key | A session key that matches no binding | The resolution returns nothing |
| TC-68 | Session manager marks an ACP-shaped session without metadata as stale | An ACP-shaped session key with no ACP metadata | The resolution reports the session as stale with an error |
| TC-69 | Session manager canonicalizes the main alias before the ACP rehydrate after a restart | A session stored under the main alias | The rehydrate resolves the canonical key |
| TC-70 | Session manager marks liveness during the runtime initialization | A session whose runtime is initializing | The session is reported as live before the turn streams start |
| TC-71 | Session manager clears liveness when the retry setup throws before the terminal publication | A failing retry setup | The liveness marker is cleared |
| TC-72 | Session manager cancels a queued turn promptly when the caller aborts before the actor is free | A queued turn and an aborted caller | The queued turn is cancelled promptly |
| TC-73 | Session manager times out a hung persistent turn after partial progress without closing the session | A turn that hangs after partial output | The turn times out, the session stays open, and the queued work continues |
| TC-74 | Session manager caps the ACP runtime option turn timeout before arming the watchdog | A runtime option timeout above the cap | The timeout is capped before the watchdog starts |
| TC-75 | Session manager uses the metadata backend when the global `acp.backend` is unset | A session whose metadata names a backend | The metadata backend is used |
| TC-76 | Session manager treats an unsupported close control as recoverable during the discard cleanup | A backend that does not support a close control | The cleanup still completes |
| TC-77 | Session manager surfaces a backend failure raised after a done event | A backend that fails after reporting done | The failure is surfaced rather than swallowed |
| TC-78 | Session manager surfaces a metadata clear error during the close | A failing metadata clear | The error is surfaced |
| TC-79 | Session manager turn delivery preserves the queued output behind a slow delivery after a backend failure | A backend failure with a slow delivery | The queued output is preserved |
| TC-80 | Session manager turn delivery cancels the delivery failure before the prompt is ready and holds the queued work until cleanup | A delivery failure before prompt readiness | The failure is cancelled and the queued work is held until the cleanup |
| TC-81 | Actor epoch fencing rejects a stale discard token without removing the successor runtime | A runtime replaced by a newer actor | The successor runtime survives the stale token |
| TC-82 | Actor epoch fencing captures the expected owner before waiting for the session actor | A session whose owner changes while the actor is busy | The expected owner is captured before the wait |
| TC-83 | Route resolution matches a peer binding ahead of an account binding | A peer binding and an account binding for the same channel | The peer binding wins and the route reports the peer match |
| TC-84 | Route resolution inherits a binding from the parent peer for a thread | A thread whose parent peer matches a binding | The parent peer binding is used and the route reports the parent match |
| TC-85 | Route resolution keeps the legacy peer-kind aliases working | A binding that uses a legacy peer kind alias | The binding still matches |
| TC-86 | Route resolution applies a role-based binding inside a guild | A guild binding with roles and a member holding one of them | The guild-and-roles binding wins |
| TC-87 | Route resolution reports the required agent selection for an unknown direct message | A multi-agent setup with no matching binding and no default owner | The route reports `AGENT_SELECTION_REQUIRED` and names the channel and the account |
| TC-88 | Route resolution applies a wildcard peer binding | A binding whose peer id is a wildcard | The wildcard binding matches |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-89 | Live ACP bind drives a conversation into a persistent ACP session | Send a chat message on a live channel that supports thread binding, then `/acp spawn <harness> --bind here`, then send another message | The second message reaches the bound ACP session and the reply comes back on the same channel |
| TC-90 | Live Gateway ACP bind verifies the Gateway-side binding path | Bind a live conversation to an ACP session and inspect the Gateway | The session key resolves to the bound conversation and the route reports the bound agent |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-91 | An ACP client attaches to a session key that does not exist with `--require-existing` | The bridge exits with a failure that names the missing session |
| TC-92 | The ACP bridge starts with a provenance mode that is not `off`, `meta`, or `meta+receipt` | The bridge fails with an error naming the valid modes |
| TC-93 | The ACP startup input exceeds the 1 MiB buffer | The bridge fails with a startup buffer error and both streams are cancelled |
| TC-94 | The Gateway connection drops while an ACP prompt is in flight | The bridge handles the disconnect and the prompt is not left hanging |
| TC-95 | A backend is unregistered while a session is bound to it | A later backend lookup reports the backend as missing |
| TC-96 | The replay ledger exceeds the per-session event cap | The oldest events in that session are trimmed |
| TC-97 | The replay ledger exceeds the total serialized byte budget | The oldest events are trimmed until the ledger fits the budget |
| TC-98 | A stored replay event has a malformed shape | The event is skipped rather than returned as a valid entry |
| TC-99 | A configured ACP binding names a session whose backend changed | The session is closed and recreated for the configured backend |
| TC-100 | A configured ACP binding names a session whose working directory changed | The session is closed and recreated for the configured working directory |
| TC-101 | A configured ACP binding names a session in the error state | The session is not reused and a new one is created |
| TC-102 | A route binding names an account the channel never accepts | The binding does not route anything, and the route falls through to the next rule |
| TC-103 | A route binding names a peer kind with a wildcard id | The wildcard peer binding is applied when no exact peer binding matched |
| TC-104 | A route binding carries a guild constraint that does not match | The binding is skipped and the next candidate is evaluated |
| TC-105 | A route binding carries a role constraint and the member holds none of the roles | The binding is skipped |
| TC-106 | A route binding points at an agent id that is not configured | The route falls back to the first existing agent id and does not fail |
| TC-107 | A direct-message conversation uses the default `main` scope | The conversation shares the agent main session key |
| TC-108 | An identity link maps two direct peer ids to the same person | The session key uses the linked peer id under a per-peer scope |
| TC-109 | A session key carries a cron run marker that is not terminal | The marker is preserved and the key is not treated as a run scope |
| TC-110 | The in-memory ACP session store is disposed while sessions hold active runs | Every active run is aborted and every removal is reported |

## Test Infrastructure

- Vitest is the test runner for every file listed here; the suites live next to the code they cover.
- The ACP control-plane suites use a fake runtime backend and a fake Gateway, so the turn delivery, cancellation, and fencing behavior is exercised without a real ACP server.
- `src/acp/translator.*.test.ts` uses a stub ACP connection and a stub Gateway client, so the translation is exercised at the protocol boundary.
- The event ledger suite uses a real SQLite state database through the state worker helpers, so the schema constraints and the byte estimate in the SQL are exercised directly.
- `src/acp/policy.test.ts` is a pure unit suite over a config object, with no Gateway and no database.
- `packages/acp-core` suites are pure unit suites, so the shared core is proven to run without a transport.
- The routing suites build a config with bindings and assert both the resolved agent and the reported match reason.
- The live suites in `src/gateway/gateway-acp-bind.live.test.ts` and the channel e2e skills need a real Gateway, a real channel account, and a real ACP runtime plugin; they are not part of the default test run.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-91, TC-92, TC-93, TC-34, TC-35, TC-36, TC-37, TC-38, TC-39, TC-89 |
| FR-2 | TC-40, TC-41, TC-42, TC-43, TC-44, TC-45, TC-46, TC-47, TC-48, TC-49, TC-50, TC-51, TC-52, TC-94 |
| FR-3 | TC-11, TC-12, TC-13, TC-14, TC-53, TC-54, TC-55, TC-56, TC-57, TC-58, TC-59, TC-68, TC-69, TC-70, TC-71, TC-72, TC-73, TC-74, TC-75, TC-76, TC-77, TC-78, TC-79, TC-80, TC-81, TC-82 |
| FR-4 | TC-1, TC-2, TC-4 |
| FR-5 | TC-1, TC-3, TC-4 |
| FR-6 | TC-5 |
| FR-7 | TC-6, TC-7, TC-8, TC-9, TC-10, TC-95 |
| FR-8 | TC-20, TC-21, TC-60, TC-61, TC-62, TC-96, TC-97, TC-98 |
| FR-9 | TC-63, TC-64, TC-65, TC-66, TC-67, TC-89, TC-90, TC-99, TC-100, TC-101 |
| FR-10 | TC-83, TC-84, TC-85, TC-86, TC-87, TC-88, TC-102, TC-103, TC-104, TC-105, TC-106 |
| FR-11 | TC-87, TC-102, TC-22, TC-31, TC-32, TC-33 |
| FR-12 | TC-23, TC-24, TC-25, TC-26, TC-27, TC-28, TC-29, TC-107, TC-108, TC-109 |
| FR-13 | TC-30, TC-43, TC-45, TC-68, TC-75 |
| FR-14 | TC-22, TC-31, TC-32, TC-33, TC-83, TC-84, TC-86, TC-88 |
| NFR-1 | TC-91, TC-92, TC-34, TC-36, TC-37, TC-39 |
| NFR-2 | TC-35, TC-47, TC-48, TC-49, TC-50, TC-51, TC-52 |
| NFR-3 | TC-53, TC-57, TC-59, TC-68, TC-81, TC-82, TC-99, TC-100 |
| NFR-4 | TC-11, TC-12, TC-13, TC-14, TC-15, TC-16, TC-17, TC-62, TC-96, TC-97, TC-110 |
| NFR-5 | TC-18, TC-19, TC-20, TC-21, TC-23, TC-25 |
