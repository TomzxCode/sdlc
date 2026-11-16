---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Specification for Node Host and Device Execution

## Sync drift: 2026-11-16

### The API contract table omits node.runnerInventory.update (non-blocking)

- Evidence: `src/gateway/methods/core-descriptors.ts:291` registers `node.runnerInventory.update` with scope `node`, group `nodes`, version `2026.8`, and `UNADVERTISED`.
- Evidence: `src/node-host/runner.inventory.test.ts` and `src/gateway/server-methods/nodes.runner-inventory.test.ts` cover publication of the inventory.
- Artifact says: the API Contracts table at specification.md:184-203 lists 18 node methods and does not include `node.runnerInventory.update`.
- Code: the node publishes its runner inventory and negotiated worker slots over this method, and `api.yaml` has no entry for it.
- Impact: a reader of the specification cannot discover this method from the documented contract.

### The CLI surface and connection model omit the OpenClaw ID path (non-blocking)

- Evidence: `src/cli/node-cli/register.ts` registers `node join` with an `openclaw-node://` invitation argument and `--service`, `--discovery-url`, and `--display-name` options.
- Evidence: `src/node-host/openclaw-id-*.ts` implement enrollment, transport, target, and relay connection with a backoff capped by `RELAY_DENIAL_BACKOFF_MAX_MS` from `packages/openclaw-id-protocol`.
- Artifact says: specification.md:209 lists the CLI as `openclaw node run|status|identity|install` and specification.md:11 and :64 describe a single Gateway WebSocket connection using the paired device token.
- Code: the node supports an additional enrollment and relay transport alongside the WebSocket path.
- Impact: the documented CLI list and connection model are incomplete.

### Data models and core behavior match the code (no drift)

- Evidence: the `node_worker_launches`, `node_worker_turns`, `node_worker_launch_boots`, `node_worker_launch_containers`, `node_worker_launch_cleanup`, `node_worker_launch_process_scopes`, and `node_worker_prepared_workspaces` tables in `src/state/openclaw-state-schema.sql` match the field lists and constraints in specification.md:68-165.
- Evidence: the approval plan, allowlist evaluation, exec policy modes, environment hardening, worker supervision, and auto-update timing are present in the paths named in specification.md:11.
- Code: no documented data model or technical decision was found to be removed or contradicted.
