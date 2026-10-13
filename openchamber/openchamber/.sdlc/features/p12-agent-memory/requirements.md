---
title: "Agent Memory"
status: done
---

# Requirements: Agent Memory

## Overview

Agent memory gives the agent a persistent store for what it learns across sessions, split into a global scope about the user and a project scope about each codebase, written by the agent through the `openchamber_memory` tool and reviewed by the user in the Memory panel.
The feature ships dark behind the `OPENCHAMBER_MEMORY_ENABLE` build flag and is further gated at runtime by the `agentMemoryToolEnabled` setting, so with either switch off there is no tool, no routes, no session index, and no settings row.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agents | Persist stable facts, preferences, and references across sessions without re-learning them |
| Users | Review, correct, and delete what the agent stored about them and their projects |
| Operators | Keep the feature fully hidden until it is deliberately enabled |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall hide the entire feature unless the `OPENCHAMBER_MEMORY_ENABLE` environment variable holds a truthy value. |
| FR-2 | Must | The system shall gate the tool, the HTTP routes, and the session index on the `agentMemoryToolEnabled` setting. |
| FR-3 | Must | The system shall store memory in two scopes, global in `<userConfigRoot>/memory.json` and project in `<projectsDir>/<bounded-stem>/memory.json`. |
| FR-4 | Must | The system shall let the agent save entries with a title, a body, and a type of `fact`, `preference`, or `reference` through the `memory.save` action. |
| FR-5 | Must | The system shall replace an existing entry when a save restates it, using exact title match or token-overlap matching, instead of storing a duplicate. |
| FR-6 | Must | The system shall cap global memory at 60 entries and project memory at 200 entries, refusing further saves with a consolidation instruction. |
| FR-7 | Must | The system shall require a non-empty title of at most 60 characters and a non-empty body of at most 2000 characters, rejecting over-limit bodies instead of truncating them. |
| FR-8 | Must | The system shall let the agent read an entry by `memoryId` or by title through the `memory.read` action, preferring the project store when both scopes hold the same title. |
| FR-9 | Must | The system shall list memory summaries carrying `memoryId`, title, type, and scope, never bodies, through the `memory.list` action. |
| FR-10 | Must | The system shall delete an entry by `memoryId` within its scope through the `memory.delete` action. |
| FR-11 | Must | The system shall expose panel read, correct, and delete operations over HTTP without any create route, since creation belongs to the agent tool. |
| FR-12 | Must | The system shall flag entries matching injection patterns, store them, withhold them from sessions, and surface them in the panel. |
| FR-13 | Must | The system shall derive project scope from the session directory through the project resolver, so every worktree of a repository shares one project memory. |
| FR-14 | Should | The system shall announce successful writes through the `onMemoryChanged` listener without ever letting a listener failure fail the write. |
| FR-15 | Should | The system shall serialize writes per scope and persist them atomically via temporary-file rename. |
| FR-16 | Must | The system shall reject a project-scoped request without a project id instead of silently falling back to global scope. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | A project memory id containing unsupported characters is rejected, and a session directory never becomes a storage path unchecked. |
| NFR-2 | Must | Correctness | A missing store reads as authoritative empty, while malformed storage fails loudly instead of reading as empty. |
| NFR-3 | Must | Correctness | A scope that fails to load is reported as unavailable, never rendered as an empty store. |
| NFR-4 | Should | Reliability | A full store still accepts a correction to an entry it already holds, since replacement does not grow the store. |
| NFR-5 | Should | Usability | Usage errors name the missing or offending input so the agent can correct the call without an upfront manual. |

## Constraints

- Memory entries are agent-written for the agent; user notes stay a separate surface and are never mixed into the store
- The session index carries entry titles only, never bodies, to bound standing context cost
- Reads stay tolerant of legacy over-limit entries while writes enforce the current limits
- The panel client resolves no storage paths and only speaks HTTP

## Acceptance Criteria

```gherkin
# FR-1
Given the process started without OPENCHAMBER_MEMORY_ENABLE set
When any memory surface is probed
Then no tool, route, index, or settings row exists
```

```gherkin
# FR-2
Given memory switched off in settings
When the agent calls any memory action or the panel calls any route
Then the action is refused and the route answers disabled without touching the store
```

```gherkin
# FR-3
Given global and project scopes
When entries are stored in each
Then they land in separate memory.json files keyed by scope
```

```gherkin
# FR-4
Given the openchamber_memory tool
When memory.save is called with title, body, and type
Then the entry is stored and confirmed without echoing the text back
```

```gherkin
# FR-5
Given a stored entry
When the agent saves the same fact phrased differently
Then the stored entry is updated in place and reported as replaced
```

```gherkin
# FR-6
Given a full scope store
When a genuinely new entry is saved
Then the save is refused with the current titles and a consolidation instruction
```

```gherkin
# FR-7
Given a save with an over-limit body
When it is submitted
Then it is rejected as a usage error and nothing is truncated silently
```

```gherkin
# FR-8
Given the same title in both scopes
When memory.read is called without a scope
Then the project entry is returned
```

```gherkin
# FR-9
Given stored entries
When memory.list is called
Then summaries carry identifiers, titles, types, and scopes with no bodies
```

```gherkin
# FR-10
Given a stored entry id and scope
When memory.delete is called
Then the entry is removed and the deletion is confirmed
```

```gherkin
# FR-11
Given the HTTP surface
When the panel reads, patches, or deletes
Then no create route exists and corrections update entries in place
```

```gherkin
# FR-12
Given text matching an injection pattern
When it is saved
Then it is stored, flagged, withheld from sessions, and shown in the panel with a warning
```

```gherkin
# FR-13
Given a session running in a worktree
When the agent saves project memory
Then the entry lands in the shared repository project store
```

```gherkin
# FR-16
Given a project-scoped request without a project id
When it reaches scope resolution
Then it is rejected instead of writing into global memory
```

```gherkin
# NFR-2
Given a corrupt memory.json file
When it is read
Then the read fails instead of reporting an empty store
```

```gherkin
# NFR-3
Given one scope failing to load
When both scopes are read together
Then the failed scope is flagged unavailable while the other scope still returns
```

## Conflicts

None identified yet.

## Open Questions

1. Should global memory gain its own consolidation guidance distinct from the project wording, given its higher blast radius?
2. Should the client title clamp (120) be aligned with the server clamp (60) so the editor stops exactly where storage cuts?
