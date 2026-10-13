---
title: "Session Knowledge"
status: done
---

# Requirements: Session Knowledge

## Overview

Session Knowledge is the server-owned subsystem that decides what a session must be told about the project (that session's pinned notes and plans, the index of remembered agent memory, and applicable agent guidance) and whether it has been told yet.
The client used to assemble the text, decide when to send it, and remember what it sent in a module-scoped map, which meant sessions started without a UI (scheduled tasks, agent-dispatched sessions) got nothing and a tab's sent-memory wrongly survived compaction.
The subsystem records a content-revision signature in the session's own metadata, resolves pending text through dedicated routes, and delivers it at three moments (UI message, server-built prompt, post-compaction re-send) without ever failing the send that carries it.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Chat users | See pinned notes, plans, and memory index reach the agent exactly once per revision |
| Agents in headless sessions | Receive pinned context and memory index in scheduled and dispatched prompts without a browser |
| Memory users | Have the save-guidance and title index delivered while memory is on, even when the store is empty |
| Work-status panel users | See pin counts and names per session without paying plan-body read costs |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall assemble the knowledge block on the server from pinned notes, pinned plan bodies, the memory title index, link guidance, and worktree-move guidance. |
| FR-2 | Must | The system shall store per-session pins in `session.metadata.openchamber.project_context_pins` as note and plan id lists isolated to that session. |
| FR-3 | Must | The system shall record what a session carries as a signature in `session.metadata.openchamber.knowledge_context_delivered` so delivery state survives tab close and compaction. |
| FR-4 | Must | The system shall cover content revisions in the signature (note id plus `updatedAt`, plan id plus title, memory id plus `updatedAt`, memory/link/worktree flags) and owe nothing when the signature matches or is empty. |
| FR-5 | Must | The system shall expose a pending-resolution endpoint that returns the text to attach and the signature to report back, with empty text when the session already carries it. |
| FR-6 | Must | The system shall record delivery only after the carrying send is accepted and never fail that send because of knowledge handling. |
| FR-7 | Must | The system shall deliver knowledge on a UI message as a synthetic part, on a server-built prompt as a synthetic part, and after compaction as its own synthetic turn combined with obligatory pinned messages. |
| FR-8 | Must | The system shall index memory by title only, state save guidance in every session while memory is on, and state "nothing is stored yet" only when both memory scopes loaded. |
| FR-9 | Must | The system shall isolate source failures so an unreadable store never blanks the rest, a failed memory scope is omitted rather than indexed as empty, an unreadable plan is marked rather than dropped, and flagged memory entries are withheld but kept. |
| FR-10 | Must | The system shall resolve directories beneath the managed chats root to that root before reading project context and memory. |
| FR-11 | Must | The system shall truncate an oversized block at 8000 characters with an explicit truncation marker. |
| FR-12 | Should | The system shall expose a summary endpoint returning pin notes, plan names, and memory counts without reading plan bodies. |
| FR-13 | Should | The system shall let the client deduplicate in-flight delivery reports, cache summaries briefly, and never throw on knowledge fetch or report. |
| FR-14 | Must | The system shall include session-link guidance and the ask/auto worktree-move rule only in sessions whose agent has the managed `openchamber` tool and ride them on the signature. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Knowledge handling never fails a message send, prompt dispatch, or panel render. |
| NFR-2 | Must | Correctness | A failed send never records delivery, so the block is carried again on retry. |
| NFR-3 | Should | Performance | Summary reads avoid plan-body disk reads and share one request across simultaneous panel callers for a few seconds. |
| NFR-4 | Should | Security | Flagged memory entries are withheld from every assembled block while remaining visible in the store for user judgment. |

## Constraints

- Pins never come from project-wide note or plan state, only from the session metadata record
- Memory bodies never enter the block, only titles plus read-before-acting instructions
- The pending-text and delivered-record calls stay separate because only the sender knows whether the send went out
- The worktree-move wording must stay identical to the agent-tool description text and both change together
- Agent memory stays dark unless `OPENCHAMBER_MEMORY_ENABLE` is set and its setting is on

## Acceptance Criteria

```gherkin
# FR-1: server assembly
Given a session with pinned notes, pinned plans, and memory entries
When pending knowledge is resolved
Then the text contains the pinned note bodies, the pinned plan titles and bodies, and the memory titles without memory bodies
```

```gherkin
# FR-2: per-session pins
Given two sessions with different pins in their metadata
When each session resolves pending knowledge
Then each session owes only its own pinned set
```

```gherkin
# FR-3: metadata signature
Given a session whose delivered signature matches the freshly computed signature
When pending knowledge is resolved
Then the returned text is empty
```

```gherkin
# FR-4: revision coverage
Given a pinned note edited after delivery
When the signature is recomputed
Then it differs from the delivered signature and the block is owed again
```

```gherkin
# FR-5: pending endpoint
Given a draft session that does not exist yet
When the pending endpoint is called without a session id
Then everything is reported as still owed
```

```gherkin
# FR-6: delivery recording
Given a send carrying the knowledge block that is rejected
When delivery reporting is attempted
Then no delivery is recorded and the next send carries the block again
```

```gherkin
# FR-7: three moments
Given a completed compaction that removed previously delivered context
When the obligatory-context tick runs
Then knowledge is re-sent on its own synthetic turn combined with the pinned messages
```

```gherkin
# FR-8: memory index rules
Given memory on with both scopes loaded and empty
When pending knowledge is resolved
Then the text states when to save and that nothing is stored yet
```

```gherkin
# FR-9: failure isolation
Given an unreadable memory store with pinned notes present
When pending knowledge is resolved
Then the pinned notes are still delivered
```

```gherkin
# FR-10: chats root
Given a session directory beneath the managed chats root
When project context and memory are read
Then they resolve to the chats root owner instead of a per-directory store
```

```gherkin
# FR-11: truncation
Given a pinned note body exceeding the budget
When the block is assembled
Then the text is cut within budget and marked as truncated
```

```gherkin
# FR-12: summary
Given a session with pinned plans
When the summary endpoint is called
Then it returns plan names without reading plan bodies
```

```gherkin
# FR-14: tool-gated guidance
Given a session whose agent lacks the managed tool
When pending knowledge is resolved
Then the text contains neither link guidance nor the worktree-move rule
```

## Conflicts

None identified yet.

## Open Questions

1. Should the plan signature cover plan body revisions (like note `updatedAt`) instead of id plus title, so a plan edit without a retitle re-sends the block?
