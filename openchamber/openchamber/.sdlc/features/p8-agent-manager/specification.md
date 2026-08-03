---
title: "Agent Manager"
status: done
---

# Specification: Agent Manager

## Overview

The Agent Manager is a client-side view (`packages/ui/src/components/views/agent-manager/AgentManagerView.tsx`) backed by `useAgentGroupsStore`. It composes a sidebar (group list), a detail pane, and an empty state, and launches multi-runs by delegating to the existing multi-run store.

## Architecture

```
AgentManagerView.tsx
    |
    +--> AgentManagerSidebar.tsx      (group list, selection)
    +--> AgentGroupDetail.tsx         (agents in selected group, launch action)
    +--> AgentManagerEmptyState.tsx   (no groups)
    |
    +--> useAgentGroupsStore.ts       (groups CRUD, selection)
    +--> useMultiRunStore.ts          (createMultiRun for selected group)
    +--> useConfigStore / useDirectoryStore / useRuntimeAPIs (connection, directory)
```

## Data Models

### AgentGroup

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | Group name |
| agents | array | not null | Agent identifiers/refs in the group |

## API Contracts

No dedicated endpoints; the feature composes existing stores and the multi-run runtime. Group persistence uses whatever persistence the agents-groups store already has (per-installation storage).

## Sequences

### Launch a multi-run from a group

```
User selects group -> AgentManagerView reads selectedGroupName
User clicks launch -> createMultiRun(group agents) -> multi-run store spawns sessions
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| State | useAgentGroupsStore | Single source of truth for groups, shared with other surfaces |
| Launch path | reuse useMultiRunStore | Multi-run machinery already owns worktrees/sessions |
| UI structure | sidebar + detail + empty state | Familiar manager pattern, scales to many groups |

## Risks and Unknowns

1. Group persistence is client-side; no cross-device sync unless the store is later backed by the server.
2. Behavior differences across runtimes (VS Code vs desktop) must stay explicit in the shared UI.

## Out of Scope

- Agent CRUD/editing inside the manager beyond group membership
- Cross-device group sync
