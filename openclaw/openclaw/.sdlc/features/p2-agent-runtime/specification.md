---
title: "Agent Runtime"
status: draft
---

# Specification: Agent Runner

## Overview

The Agent Runtime implements a turn-based conversation loop. Each turn: receive user message, build prompt with context, call model provider, execute any tool calls, stream response. Context compaction uses LLM-based summarization of older turns. Provider integration is abstracted through transport streams and payload policies.

## Architecture

```
Channel Plugin → Agent Runtime → Model Provider Transport
                      │                    │
                      ▼                    ▼
                Tool Executor          Stream Handler
                      │                    │
                      ▼                    ▼
                Policy Enforcer      Response Composer
                      │
                      ▼
               SQLite Store (Transcripts)
```

## Data Models

### TranscriptTurn

| Field | Type | Constraints | Description |
|---|---|---|---|
| turnId | string | PK | Unique turn identifier |
| sessionId | string | FK, not null | Parent session |
| role | string | not null | user, assistant, or tool |
| content | JSON | not null | Message content blocks |
| timestamp | timestamp | not null | Turn timestamp |
| tokenCount | number | nullable | Token usage for this turn |

## Sequences

### Conversation Turn

```
Channel → Runtime: user message
Runtime → Store: load session history
Runtime → Model: build prompt with context
Model → Runtime: stream response (text + tool calls)
Runtime → Tool: execute each tool call
Tool → Runtime: tool results
Runtime → Model: submit tool results for continued generation
Runtime → Store: persist turn transcript
Runtime → Channel: final response
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider abstraction | Transport stream + payload policy | Uniform interface across different model APIs |
| Compaction strategy | LLM-based summarization | Preserves conversation quality while reducing tokens |
| Tool execution | Configurable policy pipeline | Allows per-deployment sandboxing and approval rules |
| Subagent spawning | Managed subagent registry | Isolated state lifecycle for delegated tasks |
| Response streaming | Incremental chunk delivery | Low-latency user experience on all channels |

## Risks and Unknowns

1. Provider API changes may break transport compatibility; each provider has its own SDK
2. Compaction can lose information if summarization degrades conversation quality
3. Long-running tool execution (e.g. background scripts) needs timeout management

## Out of Scope

- Fine-tuning or training of models
- Custom model hosting
- Multi-modal model support beyond text, images, and audio
