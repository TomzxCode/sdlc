# Conventions

## Naming

- **Files:** snake_case for Python modules (run_agent.py, hermes_constants.py, model_tools.py). Test files: test_<module_name>.py.
- **Variables:** snake_case (config_path, session_id, tool_schemas). Private: underscore prefix (_logging_initialized).
- **Constants:** UPPER_SNAKE_CASE (DEFAULT_CONFIG, COMMAND_REGISTRY, OPTIONAL_ENV_VARS, _HERMES_CORE_TOOLS).
- **Functions / Methods:** snake_case (get_hermes_home(), handle_function_call(), run_conversation()). Private: underscore prefix.
- **Classes:** PascalCase (AIAgent, HermesCLI, SessionDB, SkinConfig, CommandDef).
- **Directories:** snake_case (hermes_cli/, tui_gateway/, acp_adapter/).

## Directory Structure

The project organizes code into purpose-driven directories at the repo root:
- Root-level Python files for core entry points and facades (run_agent.py, cli.py, model_tools.py, toolsets.py, hermes_constants.py, hermes_state.py, hermes_logging.py, hermes_time.py, batch_runner.py, utils.py)
- `agent/` — Agent internals: provider adapters, memory manager, context compressor, prompt builder, curator
- `hermes_cli/` — CLI subsystem: commands, config, plugins, skins, setup, profile management, web server, curses UI
- `tools/` — Tool implementations, auto-discovered via tools/registry.py. Subdirectory `environments/` for terminal backends.
- `gateway/` — Messaging gateway: run.py, session.py, plus platforms/ for the base adapter and support modules; canonical per-platform adapters migrated to plugins/platforms/ (22 adapters, back-compat re-exports retained)
- `plugins/` — Plugin system: memory/ (8 providers), model-providers/ (38 backends), platforms/ (22 adapters), kanban/, image_gen/, context_engine/, observability/, plus individual plugins
- `cron/` — Scheduler: jobs.py, scheduler.py, lifecycle_guard.py
- `skills/` — Built-in skills organized by category directory (13 categories)
- `optional-skills/` — Heavier/niche skills shipped but inactive by default (23 categories)
- `ui-tui/` — Ink (React) terminal UI frontend (TypeScript)
- `tui_gateway/` — Python JSON-RPC backend for the TUI
- `apps/desktop/` — Electron desktop app
- `apps/shared/` — Shared JSON-RPC client package
- `acp_adapter/` — ACP server for IDE integration
- `web/` — Dashboard SPA (xterm.js + PTY bridge)
- `website/` — Docusaurus documentation site
- `tests/` — Pytest test suite mirroring source structure
- `scripts/` — Development and release scripts
- `providers/` — Legacy provider discovery (backward-compat)
- `optional-mcps/` — Optional MCP server catalogs

## Coding Standards

- **Use type hints** on all function signatures and class attributes
- **Use `get_hermes_home()`** from hermes_constants for all HERMES_HOME paths, `display_hermes_home()` for user-facing text, never hardcode `~/.hermes`, with the sole exception that profile operations stay HOME-anchored (`_get_profiles_root()` under `Path.home()/.hermes/profiles`) by design
- **Explicit encoding** on all file operations: use `encoding=` in open(), read_text(), write_text() calls (enforced by ruff rule PLW1514)
- **No blocking calls in `async def`** (sync HTTP, subprocess, `time.sleep`): use `await asyncio.to_thread(...)`, `asyncio.create_subprocess_exec`, or `await asyncio.sleep` (enforced by ruff rules ASYNC210/220/221/251)
- **Every model tool schema is sent on every API call** — new core tools are the last resort for new capability
- **All tool handlers must return JSON strings**
- **Prefer service-gated tools** (with `check_fn`) over always-available tools when the capability depends on external credentials
- **Prefer small nanostores over component state** for shared/reused state in TypeScript UI code
- **No `simple_term_menu`** — new interactive menus must use the curses UI module
- **No `\033[K`** (ANSI erase-to-EOL) in spinner/display code — use space-padding instead
- **Do not write change-detector tests** — tests should assert invariants (how data must relate), not freeze current values (model lists, version numbers, enumeration counts)
- **Run tests via `scripts/run_tests.sh`, never bare `pytest`** (it enforces CI parity: credential vars unset, `TZ=UTC`, temp `HERMES_HOME`, per-file subprocess isolation)
- **Pin dependencies exactly** (`==X.Y.Z` plus regenerated `uv.lock`): version ranges are rejected, so every version change arrives as an intentional reviewed pin bump
- **Former god files are facades plus `<stem>_<topic>.py` siblings** (e.g. `hermes_state*.py`, `gateway/run_*.py`): new behavior goes in a topical sibling, never appended to a facade
- **Plugins must NOT modify core files** — expand the generic plugin surface (new hook, new ctx method) instead

## Commit Messages

Conventional Commits format: `type(scope): short description`
- Types observed: test, fix, feat, refactor, chore, docs
- Scopes reference the subsystem (e.g. codex-picker, memory, gateway)
- The short description is imperative, present tense, lowercase

## Branching

The canonical branch is `main`. Feature/bugfix branches follow the project's workflow conventions. Branch naming is not explicitly restricted but should reference the subsystem and issue when applicable.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review
- Use bullet lists over prose paragraphs for enumerations
- Use tables for structured data (requirements, terms, components)
- Feature directories follow the `N-<slug>` convention where N is a GitHub issue number or `p<seq>` for pending features
- Feature IDs use the `FEAT-N` form in cross-references (e.g., FEAT-42)