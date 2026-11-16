---
artifact: requirements.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

Drift found by `/sync-sdlc` comparing this artifact against the current code. Not yet reconciled.

- **FR-8 toolset inventory is incomplete.** FR-8 lists show, complete, block, heartbeat, comment, create, link, attach, attachments. `tools/kanban_tools.py` `_TOOLS` registers 15 tools. Missing from FR-8: `kanban_list`, `kanban_unblock`, `kanban_attach_url`, `kanban_schedule`, `kanban_request_review`, `kanban_request_changes`.
