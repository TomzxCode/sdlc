---
title: "Configuration and Multi-Profile System"
status: draft
---

# Requirements: Configuration and Multi-Profile System

## Overview

Hermes uses a layered configuration system: config.yaml for behavioral settings (deep-merged from DEFAULT_CONFIG), .env for secrets only, and profile support for fully isolated agent instances. Each profile has its own HERMES_HOME directory (config, credentials, skills, sessions, logs). The model catalog, provider registry, and toolset configuration complete the setup story.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Want to customize agent behavior through config.yaml without editing source files |
| Multi-identity users | Want separate profiles for work vs. personal use with different models, credentials, and skills |
| Self-hosters | Want to configure terminal backends, memory providers, and gateway platforms |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | All behavioral settings shall be configurable via config.yaml |
| FR-2 | Must | Secrets (API keys, tokens, passwords) shall be stored in .env only |
| FR-3 | Must | Configuration shall use a deep-merge from DEFAULT_CONFIG to user config.yaml |
| FR-4 | Must | The system shall support multiple fully isolated profiles |
| FR-5 | Must | Each profile shall have its own HERMES_HOME directory |
| FR-6 | Must | Profiles shall support the --clone option to copy an existing profile's config |
| FR-7 | Must | The system shall support a model catalog with provider-specific model lists |
| FR-8 | Must | The system shall support toolset enable/disable per platform |
| FR-9 | Should | Config version bumps shall support migrating/transforming existing user config |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Compatibility | config.yaml changes should be backward compatible (new keys merged automatically) |
| NFR-2 | Must | Security | .env must never be committed or logged |
| NFR-3 | Should | Performance | Config loading should complete in under 500ms |

## Constraints

- No new HERMES_* env vars for non-secret config (behavioral settings go in config.yaml)
- _config_version is bumped ONLY when migration/transformation is needed, not for new keys
- Profiles are fully independent — no live config inheritance between profiles

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a user sets display.skin: ares in config.yaml
    - **When** the CLI starts
    - **Then** the ares skin is applied
- [ ] **FR-4**
    - **Given** two profiles created with hermes -p personal and hermes -p work
    - **When** the user runs hermes -p personal
    - **Then** the personal profile's config, sessions, and skills are used
- [ ] **FR-6**
    - **Given** the user runs hermes profile clone --from personal --name personal2
    - **Then** a new profile with the same config as personal is created

## Conflicts

None identified yet.

## Open Questions

1. Should profile configs support a !include directive for shared sections?