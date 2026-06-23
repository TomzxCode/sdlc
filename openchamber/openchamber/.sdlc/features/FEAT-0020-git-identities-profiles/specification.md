---
title: "Git Identities / Profiles"
status: draft
---

# Specification: Git Identities / Profiles

## Overview

Git identities are managed via `useGitIdentitiesStore.ts` with a settings page at `sections/git-identities/GitPage.tsx`. Credential discovery reads from `~/.gitconfig` and `~/.ssh/`. Gitmojis are cached locally from the gitmoji API.

## Architecture

```
GitPage (packages/ui/src/components/sections/git-identities/)
    +---> Identity CRUD (name, email, auth type, SSH key)
    +---> Per-project selection
    +---> Gitmoji picker
    |
useGitIdentitiesStore.ts (identity profiles)
    |
Server (credential discovery from git/ssh config)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Discovery | Read existing git/ssh config | Reduces manual setup; leverages existing developer config |
| Gitmoji | Local cache with TTL | Avoids API call on every commit; gitmoji list changes rarely |

## Out of Scope

- GPG signing per identity
- Identity sync across devices
