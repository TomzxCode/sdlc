---
title: "Installation and Auto-Update"
status: done
---

# Requirements: Installation and Auto-Update

## Overview

jcode distributes itself through a multi-platform installer plus GitHub Releases, and keeps itself current with an auto-update pipeline that downloads new binaries and hot-reloads the server without dropping sessions. Release automation covers Linux, macOS, and Windows (including signing) and posts release notes to Discord. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Simple one-command install, reliable updates, and painless uninstall on every platform |
| Maintainer | Reproducible releases, versioned immutable binaries, and safe hot-reload updates |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide one-command installers on Linux, macOS, and Windows (`https://jcode.sh/install` and `install.ps1`). |
| FR-2 | Must | The system shall provide uninstallers for each platform. |
| FR-3 | Must | The system shall check for updates against GitHub Releases and support stable and main update channels. |
| FR-4 | Must | The system shall download and install new versions into immutable versioned directories (`~/.jcode/builds/versions/<version>/`) and repoint launcher channels. |
| FR-5 | Must | The system shall support hot-reloading the server into the new binary without dropping sessions (exec into new binary, clients reconnect). |
| FR-6 | Should | The system shall support local quick releases (`quick-release.sh`) and CI release automation across platforms. |
| FR-7 | Should | The system shall handle divergence gracefully when the local clone and remote differ during a git-pull based update. |
| FR-8 | May | The system shall post release announcements to Discord. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Update must not corrupt the current install if interrupted. |
| NFR-2 | Must | Availability | Hot-reload must preserve active sessions and clients. |
| NFR-3 | Should | Security | Downloads must be validated (signed/hash-checked) before activation. |
| NFR-4 | Should | Usability | Updates should be non-intrusive and respect `--no-update`. |

## Constraints

- Version layout and launcher symlinks are documented in AGENTS.md install notes.
- Release channels: stable and main.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a clean machine on any supported OS
    - **When** the install command runs
    - **Then** jcode installs and runs
- [ ] **FR-2**
    - **Given** an installed jcode
    - **When** the uninstaller runs
    - **Then** jcode and its launcher are removed
- [ ] **FR-3**
    - **Given** an update channel configured
    - **When** a new release exists
    - **Then** the update is detected
- [ ] **FR-4**
    - **Given** an available update
    - **When** it downloads
    - **Then** the new binary lands in a versioned directory and the channel is repointed
- [ ] **FR-5**
    - **Given** an active server with clients
    - **When** the server reloads into the new binary
    - **Then** sessions persist and clients reconnect
- [ ] **FR-6**
    - **Given** release tooling
    - **When** a release is cut
    - **Then** the quick or CI flow produces a release
- [ ] **FR-7**
    - **Given** a divergent local clone
    - **When** a git-pull update runs
    - **Then** divergence is handled without breaking the install
- [ ] **FR-8**
    - **Given** a published release
    - **When** announcements are enabled
    - **Then** a Discord post is created
- [ ] **NFR-1**
    - **Given** an interrupted download
    - **When** the update retries
    - **Then** the current install remains usable
- [ ] **NFR-2**
    - **Given** a reload with open sessions
    - **When** the new binary starts
    - **Then** all sessions are preserved
- [ ] **NFR-3**
    - **Given** a downloaded binary
    - **When** it is activated
    - **Then** it is validated before use
- [ ] **NFR-4**
    - **Given** `--no-update`
    - **When** jcode starts
    - **Then** no update check runs

## Conflicts

None identified yet.

## Open Questions

1. Are release binaries signed for all platforms, or only Windows? `RELEASING.md` documents Windows signing; macOS/Linux coverage is inferred.
