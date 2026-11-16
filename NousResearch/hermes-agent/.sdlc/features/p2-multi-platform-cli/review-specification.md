---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Specification — Multi-Platform CLI

## Sync drift: 2026-11-16

- CommandDef data model lists 8 fields. `hermes_cli/commands.py::CommandDef` now defines 15, adding `subcommands`, `busy_policy`, `busy_handler`, `execute`, `argument_mode`, `desktop`, and `desktop_subcommands`.
- SkinConfig data model lists 6 fields. `hermes_cli/skin_engine.py::SkinConfig` now also carries `description`, `light_colors`, `dark_colors`, `banner_logo`, `banner_hero`, `custom_css`, and `palette`.
- Architecture diagram routes text input through `process_text()`, which no longer exists in `cli.py` or the `hermes_cli/cli_*_mixin.py` modules. The runtime input loop calls `process_command()` directly for slash commands.
