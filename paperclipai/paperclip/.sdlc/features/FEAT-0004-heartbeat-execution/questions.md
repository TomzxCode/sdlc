# Open Questions: Heartbeat Execution & Adapters

## Sync drift (2026-06-24)

The following items were identified during codebase reconciliation and reflect functionality present in the code but not documented in the current requirements.md or specification.md.

1. **External adapter plugin loading** — The adapter plugin loader (`server/src/adapters/plugin-loader.ts`, `server/src/services/adapter-plugin-store.ts`) dynamically loads external adapters from `~/.paperclip/adapter-plugins.json` with zero hardcoded core imports. This is a significant capability not reflected in the feature docs.

2. **Adapter management API** — A full adapter management route exists at `server/src/routes/adapters.ts` (693 lines) for installing/configuring/listing adapters. Not documented in the spec.

3. **Agent instructions system** — `server/src/services/agent-instructions.ts`, `server/src/services/default-agent-instructions.ts`, and schema `agent_config_revisions` manage per-agent system prompt instructions. Not documented.

4. **Skills selection at runtime** — `server/src/services/runtime-skill-selections.ts` resolves which skills are active per agent at heartbeat time. Not documented.

5. **Agent runtime state and wakeup** — `agent_runtime_state`, `agent_wakeup_requests`, `agent_task_sessions` schema tables plus corresponding services provide execution state tracking. Not documented.

6. **Run session management** — `run-continuations.ts`, `run-liveness.ts`, `session-workspace-cwd.ts` provide session continuity and liveness tracking. Not documented.

7. **Heartbeat run watchdog decisions** — Schema `heartbeat_run_watchdog_decisions` and service `heartbeat-run-summary.ts` provide watchdog decision tracking for runs. Not documented.

8. **Run log store** — `server/src/services/run-log-store.ts` provides structured log storage for heartbeat runs. Not documented.
