---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **The gateway is no longer described accurately as a raw/direct YAML loader.** The Overview says "direct YAML load for the gateway" and the Architecture diagram says "Direct YAML — gateway runtime (gateway/run.py) — reads config.yaml raw". In the code, `gateway/run.py::_load_gateway_config()` (around lines 2839-2851) delegates to `hermes_cli.config_effective.load_user_config_effective()`, which applies `${VAR}` expansion, a managed-config overlay, model-key canonicalization, and last-known-good recovery before returning the mapping. It is not a raw read. The underlying intent recorded in Risk #2, that the gateway does not merge `DEFAULT_CONFIG`, still holds, and `gateway/config.py` still uses `fast_safe_load` for platform settings, but the `gateway/run.py` path named in the spec must be described as the effective-config loader.
- **The profile-structure diagram names the wrong session-store file.** It shows `sessions.db` as the "Session store" in both the default home and each named profile home. The code uses `state.db`: `hermes_state.DEFAULT_DB_PATH = get_hermes_home() / "state.db"`, and `hermes_constants._HERMES_HOME_MARKERS` includes `state.db`. `sessions/` is a directory of per-session JSONL pending-message files, not a database file. Both occurrences of `sessions.db` should be `state.db`.

Resync the loader description and the profile-structure diagram, then re-review.
