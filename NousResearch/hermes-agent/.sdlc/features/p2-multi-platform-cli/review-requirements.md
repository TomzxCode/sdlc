---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Requirements — Multi-Platform CLI

## Sync drift: 2026-11-16

- Overview states the central slash-command registry supports "~70 commands", but `hermes_cli/commands.py::COMMAND_REGISTRY` now defines 105 `CommandDef` entries. The documented command count is stale.
- Overview states the CLI "serves as the embedding target for the web dashboard via PTY bridge". The dashboard actually embeds the TUI (`hermes --tui`) with its own PTY-backed terminal, and specification.md lists the TUI as a separate surface out of scope for the classic CLI. The classic CLI is not the embedding target.
