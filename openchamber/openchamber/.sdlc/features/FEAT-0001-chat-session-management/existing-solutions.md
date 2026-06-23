---
issue: ""
title: "Chat & Session Management"
status: draft
---

# Existing Solutions: Chat & Session Management

## Overview

OpenChamber's chat and session management is already substantially implemented using `@opencode-ai/sdk/v2` for core session/message types, Zustand for store splitting (session-ui-store, messageQueueStore, etc.), and a custom SSE event pipeline for real-time streaming. The recommendation is to extend this existing architecture rather than adopt an external chat library, because the custom implementation is tightly coupled to OpenCode's event model. The key gap is formal undo/redo and branching, which can be addressed by adopting the immutable conversation pattern from `conversationalist` or by building a lightweight checkpoint tree on top of the existing session store.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/sync/` (session-ui-store, session-actions, event-pipeline, event-reducer, sync-context, input-store), `packages/ui/src/stores/` (useGlobalSessionsStore, session folders, pinned, display, multi-select, messageQueueStore), `packages/ui/src/components/chat/` (50+ components), `packages/web/server/lib/opencode/` (session-runtime), `packages/ui/src/lib/opencode/client.ts` |
| Open-source | Yes | conversationalist, LangChain branching chat, Ably AI Transport, Vercel AI SDK useBranchingChat PR, ai-chatbot-tree |
| Commercial / SaaS | Yes | ChatGPT (branching), Claude (edit/regenerate), Cursor, GitHub Copilot Chat, Ably AI Transport |
| Standards / protocols | Yes | SSE (EventSource), WebSocket, OpenCode SDK event format |
| Reference material | Yes | Zustand docs, @opencode-ai/sdk docs, SSE reconnect best practices |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal (Zustand stores + OpenCode SDK + event pipeline) | Internal | MIT | Ship-ready | FR-01, FR-04, FR-05, FR-06, FR-07, FR-08, NFR-01, NFR-02, NFR-03, NFR-04, NFR-05, NFR-06 | FR-02 (undo/redo), FR-03 (formal branching) |
| conversationalist (`stevekinney/conversationalist`) | Library | MIT | Active | FR-02 (undo/redo), FR-03 (branching with ConversationHistory) | No streaming support, no OpenCode SDK integration, no server-side persistence |
| LangChain branching chat | Product (LangGraph) | MIT | Mature | FR-03 (checkpoint-based branching) | Requires LangGraph Agent Server, not portable |
| Ably AI Transport | Product/SDK | Custom | Mature | FR-03 (tree-structured conversation), multi-device sync | Requires Ably service, heavy for single-user use |
| Vercel AI SDK `useBranchingChat` | Library (PR) | MIT | Experimental | FR-02, FR-03 (wrapper around useChat) | Unmerged PR, tied to Vercel AI SDK |
| ai-chatbot-tree (`TongDucThanhNam/ai-chatbot-tree`) | Library | MIT | Active | FR-03 (tree-based SSOT with D3 visualization) | Heavy (D3 + React Flow), opinionated architecture |

## Evaluation

### Existing Internal Architecture

- **Strengths:** Already production-ready. Tight integration with OpenCode SDK event model (message.delta, part.updated at 60/sec). Zustand store splitting prevents render cascades. Virtualized rendering via `@tanstack/react-virtual`. Message queue with FIFO auto-send. Session persistence and bootstrap. 50+ chat components with tool output rendering, markdown, mermaid, diff preview.
- **Weaknesses:** Undo/redo (FR-02) and branching (FR-03) are gaps. The current session model is a flat timeline rather than a tree. Multi-branch UI not implemented.
- **Integration effort:** Low for incremental branching; Medium for formal undo/redo tree.
- **Cost:** Zero (already built).
- **Risks:** Adding tree/branching on top of existing flat store could introduce data model conflicts. The existing store assumes a linear message array.

### conversationalist

- **Strengths:** Immutable conversation state with built-in undo/redo via `ConversationHistory` class. Supports branching, branch count, and named branches. Emits typed events for mutations. TypeScript-first.
- **Weaknesses:** Does not handle streaming (no concept of partial deltas). No server-side persistence. Would need adapter layer between conversationalist events and OpenCode SDK. No tool output rendering.
- **Integration effort:** Medium to high. Would need to map conversationalist's immutable state to Zustand stores and sync with OpenCode SSE events.
- **Cost:** MIT (free).
- **Risks:** Immutable state model may conflict with the current Mutative-driven store updates. Streaming delta model (60 updates/sec) would need careful adapter design.

### LangChain branching chat

- **Strengths:** Production-grade checkpoint-based branching. Clean fork-from-checkpoint API. Used by LangSmith.
- **Weaknesses:** Requires LangGraph Agent Server. OpenChamber wraps OpenCode CLI, not LangGraph. Cannot adopt without replacing the AI backend.
- **Integration effort:** Very high (would require OpenCode → LangGraph backend migration).
- **Cost:** Self-hosted (server), LangSmith (optional paid tier).
- **Risks:** Complete backend dependency change. Not aligned with OpenCode-first architecture.

## Recommendation

**Direction:** Adopt and extend

Continue using the existing internal architecture as the foundation. For undo/redo and branching (FR-02, FR-03), adopt the immutable conversation tree concept from `conversationalist` — specifically its `ConversationHistory` branching model — but implement directly on top of the existing `session-ui-store` rather than importing the library as a dependency. The existing store already manages session state; adding a checkpoint/parent pointer field to each message and a `branchChildren` map provides the tree structure. This avoids the integration overhead of an external library while borrowing its proven pattern.

## Sources of Information

- `conversationalist` GitHub: `stevekinney/conversationalist` — immutable conversation history with undo/redo and branching via `ConversationHistory` class
- LangChain branching chat docs: `docs.langchain.com/oss/javascript/langchain/frontend/branching-chat` — checkpoint-based fork from any message
- Ably AI Transport branching: `ably.com/docs/ai-transport/features/branching` — tree-structured conversation with `forkOf`/`parent` headers
- Vercel AI SDK PR #5085: `github.com/vercel/ai/pull/5085` — `useBranchingChat` hook for tree-structured conversations
- ai-chatbot-tree: `github.com/TongDucThanhNam/ai-chatbot-tree` — Conversation Tree SSOT with D3/React Flow visualization
- Existing `event-pipeline.ts` reconnect logic: exponential backoff respecting `navigator.onLine` and visibility state
- Existing `sync-context.tsx` `handleDirectoryEvent`: targeted Zustand store updates during streaming (60/sec)

## Open Questions

1. Should the branching model use parent pointers on each message (simpler) or a separate checkpoint store indexed by `checkpointId` (cleaner but more complex)?
2. How should the tree visualization work in the UI — a fork indicator per message, a timeline dialog, or both?
