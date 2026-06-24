# Open Questions: Workspaces & Runtime

## Sync drift (2026-06-24)

The following items were identified during codebase reconciliation and reflect functionality present in the code but not documented in the current requirements.md or specification.md.

1. **Projects subsystem** — Projects have their own full CRUD route (`server/src/routes/projects.ts`, 724 lines), service (`server/src/services/projects.ts`, 1215 lines), schema tables (`projects`, `project_workspaces`, `project_memberships`, `project_goals`), shared types, and UI pages (`Projects.tsx`, `ProjectDetail.tsx`, `ProjectWorkspaceDetail.tsx`). Projects carry status, lead agent, target date, env, execution workspace policy, budget summaries, and plugin-managed project support. The workspace/runtime spec treats workspaces as execution-git-worktrees but misses the broader Projects entity.

2. **Environments subsystem** — `server/src/services/environments.ts`, `environment-config.ts`, `environment-execution-target.ts`, `environment-probe.ts`, `environment-run-orchestrator.ts`, `environment-runtime.ts` plus route `environments.ts` and schema `environments`, `environment_leases` form a complete secret-aware environment binding system. Not documented in the spec.

3. **Workspace operations** — `server/src/services/workspace-operations.ts`, `workspace-operation-log-store.ts`, `workspace-file-resources.ts`, route `workspace-command-authz.ts` provide CLI command execution, file uploads, diffs, and git operations within workspaces. The spec mentions these in passing but does not describe the implementation.

4. **Workspace runtime services** — `server/src/services/workspace-runtime.ts`, `workspace-runtime-read-model.ts`, `project-workspace-runtime-config.ts`, route `workspace-runtime-service-authz.ts` provide runtime service lifecycle management (dev servers, preview URLs). Not fully documented.

5. **File resources** — `server/src/services/workspace-file-resources.ts` and `server/src/routes/file-resources.ts` provide file resource management within workspaces. Not documented.

6. **Sandbox provider runtime** — `server/src/services/sandbox-provider-runtime.ts` supports sandbox-provider-based execution workspaces (e.g., Daytona). Not documented.

7. **Local service supervisor** — `server/src/services/local-service-supervisor.ts` manages local runtime services. Not documented.

## Sync drift (2026-06-24) — update

Item 1 (Projects subsystem) has been partially addressed: Projects now has its own feature file at `.sdlc/features/FEAT-0014-projects/`. The FEAT-0008 spec should be updated to reflect the boundary between workspaces (execution worktrees, runtime services) and projects (organizational grouping with workspaces).
