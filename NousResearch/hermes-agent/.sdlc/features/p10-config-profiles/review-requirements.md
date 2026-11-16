---
artifact: requirements.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: requirements.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **FR-6 acceptance criterion names a command that does not exist.** It says "Given the user runs `hermes profile clone --from personal --name personal2` / Then a new profile with the same config as personal is created". The `profile` parser in `hermes_cli/subcommands/profile.py` defines these subcommands: `list`, `use`, `create`, `delete`, `describe`, `show`, `alias`, `rename`, `purge-identity`, `migrate-identity`, `export`, `import`, `install`, `update`, `info`. There is no `clone` subcommand. Cloning is done through `hermes profile create <NAME> --clone-from <SOURCE>` (or `--clone` / `--clone-all`) on the `create` subcommand. The target profile name is a positional argument (`profile_name`), and `--name` is only accepted by `import` and `install`, not by the clone path (`hermes_cli/profile_cmd.py`, `hermes_cli/profiles.py::create_profile`). The acceptance criterion should be rewritten to the implemented `profile create ... --clone-from` form.

Resync the FR-6 acceptance criterion to the implemented CLI, then re-review.
