---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-08-03
---

# Review: Specification (Terminal and Browser Automation)

## Sync drift: 2026-08-03

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Environment list omits Vercel Sandbox.** The Architecture section's `Environment ABC` tree lists only `LocalEnvironment`, `DockerEnvironment`, `SSHEnvironment`, `ModalEnvironment`, `DaytonaEnvironment`, and `SingularityEnvironment`. The codebase adds `VercelSandbox` (`tools/environments/vercel_sandbox.py`).
2. **Overview says "local, Docker, SSH, Modal, Daytona, Singularity"** — should include Vercel Sandbox for the seven-backend set.

Resync `specification.md` to include the Vercel Sandbox environment, then re-review.

## Sync drift: 2026-09-20

Drift detected during `/sync-sdlc` reconciliation against the current codebase.
The 2026-08-03 items above still stand.
New items:

1. **CDP module filename is wrong.** The spec names `tools/browser_cdp_tool.py`; the actual file is `tools/browser_tool_cdp.py`. Fix the path reference.

Resync `specification.md` for the CDP path, then re-review.

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase. New items:

1. **Architecture names a browser tool file that is now a frozen stub.** The Browser tree names `tools/browser_tool.py` as the "Browser Tool". That file is a frozen old-updater compatibility stub; its docstring says "The built-in browser_* tools and agent-browser are gone; `browser_exec` (`tools/browser_use_cli.py`) is the browser." The active browser tool is `browser_exec` in `tools/browser_use_cli.py`. Point the architecture at `browser_exec`/`browser_use_cli.py`.
2. **`SingularityEnvironment` is no longer a built-in backend.** The Environment ABC tree lists `SingularityEnvironment` among the built-in environments. There is no `tools/environments/singularity.py`; Singularity moved out of core into the `singularity` catalog plugin (`plugin-catalog/singularity.yaml`, "Formerly built into Hermes core; existing users are migrated automatically"). `tools/terminal_tool.py` lists the built-ins as local, docker, modal, daytona, vercel_sandbox, ssh plus plugin-registered backends. Remove `SingularityEnvironment` from the built-in tree or mark it plugin-provided.

Resync `specification.md`, then re-review.
