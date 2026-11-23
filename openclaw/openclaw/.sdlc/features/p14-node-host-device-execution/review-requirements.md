---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Requirements for Node Host and Device Execution

## Sync drift: 2026-11-16

### An OpenClaw ID enrollment path is implemented but has no requirement (non-blocking)

- Evidence: `src/cli/node-cli/register.ts` registers `node join` with an `openclaw-node://` invitation argument and `--service`, `--discovery-url`, and `--display-name` options.
- Evidence: `src/node-host/openclaw-id-join.ts`, `openclaw-id-enrollment.ts`, `openclaw-id-connection.ts`, `openclaw-id-transport.ts`, and `openclaw-id-target.ts` implement enrollment and a relay transport with its own backoff.
- Artifact says: FR-3 lists only the paired device token, the saved node configuration, and environment credentials as sources of Gateway credentials.
- Code: the node can enroll through an OpenClaw ID invitation and connect through a dedicated relay path in addition to the Gateway WebSocket path.
- Impact: no FR or NFR currently covers enrollment, discovery, or the relay transport.
- Action: confirm whether this path belongs to this feature or a separate one before adding a requirement.

### Runner inventory publication is implemented but has no requirement (non-blocking)

- Evidence: `src/node-host/connection.ts`, `runtime.ts`, and `node-worker-capacity.ts` publish runner inventory, and `src/node-host/runner.inventory.test.ts` covers it.
- Artifact says: FR-5 covers advertising the command surface and FR-14 covers node events, but neither mentions publishing a runner inventory or negotiated worker slots.
- Code: the node republishes its approved surface and worker slots over `node.runnerInventory.update`.
- Impact: the documented required behavior is missing this capability.
- Action: decide whether a requirement line is needed.

### All documented requirements remain implemented (no drift)

- Evidence: the command allowlist intersection and startup failure, exec approval modes, environment hardening, launch and turn journal schema, auto-update timing, and CLI service lifecycle were each checked against the code.
- Artifact says: FR-1 through FR-14 and NFR-1 through NFR-6 describe behavior that is still present in `src/node-host/`, `src/cli/node-cli/`, and the shared state schema.
- Code: no documented requirement was found to be removed or contradicted.

## Sync drift: 2026-11-23

Fresh reconciliation against current code found the same two gaps recorded on 2026-11-16. No documented requirement was found to be removed or contradicted.

### OpenClaw ID enrollment still has no requirement

- Evidence: `src/cli/node-cli/register.ts:50` registers the `node join` command, with the `openclaw-node://` invitation argument at line 53 and the `--service`, `--discovery-url`, and `--display-name` options at lines 54 to 59.
- Evidence: `src/node-host/openclaw-id-join.ts`, `src/node-host/openclaw-id-enrollment.ts`, `src/node-host/openclaw-id-connection.ts`, `src/node-host/openclaw-id-transport.ts`, `src/node-host/openclaw-id-target.ts`, and `src/node-host/openclaw-id-discovery.ts` implement enrollment and a relay transport with its own backoff, capped by `RELAY_DENIAL_BACKOFF_MAX_MS` at `src/node-host/openclaw-id-connection.ts:74` and :122.
- Artifact says: FR-3 at requirements.md:31 lists only the paired device token, the saved node configuration, and environment credentials as Gateway credential sources.
- Code: the node can enroll through an OpenClaw ID invitation and connect over a dedicated relay path in addition to the Gateway WebSocket path.
- Impact: no FR or NFR covers enrollment, discovery, or the relay transport.
- Verdict: unchanged from the 2026-11-16 finding and still non-blocking.

### Runner inventory publication still has no requirement

- Evidence: `src/node-host/runner.inventory.test.ts` and `src/gateway/server-methods/nodes.runner-inventory.test.ts` cover publication of the approved surface and negotiated worker slots.
- Evidence: `src/gateway/methods/core-descriptors.ts:282` registers `node.runnerInventory.update`.
- Artifact says: FR-5 at requirements.md:33 covers the command surface intersection and FR-14 at requirements.md:42 covers node events, but neither mentions publishing a runner inventory.
- Code: the node publishes its approved surface and worker slots over `node.runnerInventory.update`.
- Impact: the documented required behavior omits this capability.
- Verdict: unchanged from the 2026-11-16 finding and still non-blocking.
