---
title: "Configuration and Multi-Profile System"
status: done
---

# Specification: Configuration and Multi-Profile System

## Overview

Config loading follows a three-path system: load_cli_config() for CLI mode (includes CLI-specific defaults), load_config() for tools/setup (merges DEFAULT_CONFIG + user YAML), and direct YAML load for the gateway. All three use deep-merge to combine defaults with user overrides without requiring users to include the entire config.

## Architecture

```
Profile-aware path resolution:
    get_hermes_home() → ~/.hermes (default) or ~/.hermes/profiles/<name> (profile)
                        ↑
                _apply_profile_override() sets HERMES_HOME before any module imports

Config loaders:
    ├── load_cli_config() — CLI mode (cli.py)
    │   └── merges CLI-specific defaults + user config.yaml
    ├── load_config() — tools/setup (hermes_cli/config.py)
    │   └── merges DEFAULT_CONFIG + user config.yaml
    └── Direct YAML — gateway runtime (gateway/run.py)
        └── reads config.yaml raw

Config sections (non-exhaustive):
    model, agent, terminal, compression, display, stt, tts,
    memory, security, delegation, smart_model_routing, checkpoints,
    auxiliary, curator, skills, gateway, logging, cron, profiles,
    plugins, honcho
```

## Data Models

### Config structure (config.yaml)

No fixed schema — sections are added to DEFAULT_CONFIG as dictionaries. New keys are auto-merged without version bumps. A _config_version field tracks schema migration needs.

### Profile structure (filesystem)

```
~/.hermes/
    ├── config.yaml       # Default profile
    ├── .env              # Secrets (default profile)
    ├── sessions.db       # Session store
    ├── logs/
    ├── skills/
    ├── plugins/
    ├── skins/
    └── profiles/
        ├── personal/
        │   ├── config.yaml
        │   ├── .env
        │   ├── sessions.db
        │   └── ...
        └── work/
            └── ...
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Profile isolation | Independent directories | No coupling between profiles; clean separation of state |
| Config merge | Deep-merge from defaults | Users only specify overrides, not the entire config |
| Version bumps | Only for migrations | Adding a key is backward compatible without a version bump |
| Secrets location | .env only (never config.yaml) | Keeps secrets out of version control and prevents accidental exposure |
| .env vars | Secrets only | Behavioral settings go in config.yaml — env vars are reserved for API keys and tokens |

## Risks and Unknowns

1. Three config loaders can drift — a key may work in CLI but not in gateway or vice versa
2. Gateway reads raw YAML without DEFAULT_CONFIG merge — new keys added to DEFAULT_CONFIG may not appear in gateway without explicit work
3. Deep-merge may produce unexpected results for nested structures (lists are replaced, not merged)

## Out of Scope

- Cloud-synced profiles
- GUI config editor