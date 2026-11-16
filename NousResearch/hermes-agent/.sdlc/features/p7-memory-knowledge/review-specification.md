---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **Architecture diagram places all eight providers under `plugins/memory/<name>/`.** Only `plugins/memory/byterover/` and `plugins/memory/retaindb/` exist in the tree. Honcho, Mem0, Supermemory, Hindsight, Holographic and OpenViking moved out of core to `plugin-catalog/<name>.yaml` (confirmed: `honcho.yaml`, `mem0.yaml`, `supermemory.yaml`, `hindsight.yaml`, `holographic.yaml`, `openviking.yaml`) and are auto-installed by `hermes_cli/memory_provider_migration.py`. The diagram's eight in-tree paths are stale for six of the providers.

- **MemoryProvider ABC data model records the wrong `sync_turn` signature.** The table lists `sync_turn(turn_messages)`. The implemented signature in `agent/memory_provider.py` is `sync_turn(self, user_content, assistant_content, *, session_id="", messages=None, turn_author=None)`.

Resync the provider locations in the Architecture diagram and the ABC data model.
