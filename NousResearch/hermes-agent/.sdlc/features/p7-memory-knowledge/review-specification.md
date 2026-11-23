---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-23
---

# Review: specification.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **Architecture diagram places all eight providers under `plugins/memory/<name>/`.** Only `plugins/memory/byterover/` and `plugins/memory/retaindb/` exist in the tree. Honcho, Mem0, Supermemory, Hindsight, Holographic and OpenViking moved out of core to `plugin-catalog/<name>.yaml` (confirmed: `honcho.yaml`, `mem0.yaml`, `supermemory.yaml`, `hindsight.yaml`, `holographic.yaml`, `openviking.yaml`) and are auto-installed by `hermes_cli/memory_provider_migration.py`. The diagram's eight in-tree paths are stale for six of the providers.

- **MemoryProvider ABC data model records the wrong `sync_turn` signature.** The table lists `sync_turn(turn_messages)`. The implemented signature in `agent/memory_provider.py` is `sync_turn(self, user_content, assistant_content, *, session_id="", messages=None, turn_author=None)`.

Resync the provider locations in the Architecture diagram and the ABC data model.

## Sync drift: 2026-11-23

New discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run, beyond the 2026-11-16 drift recorded above.

- **Overview and Architecture name `hermes_state.py` as the live session store.** Both the Overview ("The session store (hermes_state.py) provides local FTS5 search") and the Architecture diagram ("Session Store (hermes_state.py)") point at a module that is now a deprecated compatibility shim. `hermes_state.py` opens with "Compatibility module for outside plugins that still import `hermes_state`; removed in v0.27.0" and holds no SQL, database connection or state of its own. Session storage now lives in `persistence/` with `persistence_assembly.py` as the entry point and the SQLite backend in `persistence/sqlite/` (FTS5 schema in `persistence/sqlite/_schema.py`). `website/docs/developer-guide/session-storage.md` documents those source files.

Resync the session-store path in the Overview and the Architecture diagram.
