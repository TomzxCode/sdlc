---
issue: ""
title: "Permission / Edit Mode"
status: draft
---

# Existing Solutions: Permission / Edit Mode

## Overview

OpenChamber has a mature permission system with PermissionCards in chat, a Zustand permissionStore with auto-accept (per-session, tree-scoped), toast notifications for pending permissions, SSE event handling (permission.asked, permission.replied), and edit mode controls with visual color coding (allow/ask/deny/full). The requirements formalize existing behavior (FR-01 through FR-07 are mostly implemented) and add auto-accept defaults for new agents (FR-08) and OpenCode config-layer persistence (FR-09). The recommendation is to build the remaining gaps within the existing architecture.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | PermissionCard.tsx, permissionStore.ts, sync-context.tsx, session-ui-store.ts, permission types, editModeColors, editPermissionDefaults, contextStore.ts |
| Open-source | Yes | npm for AI approval card components |
| Commercial / SaaS | No | Not applicable |
| Standards / protocols | No | OpenCode SDK defines the permission protocol |
| Reference material | Yes | agent-approval-card, shadcn AI confirmation, Tool UI ApprovalCard, Vercel AI SDK confirmation |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07 | FR-08 (new agent default), FR-09 (config-layer persistence) |
| agent-approval-card | Library | MIT | Early (0.1.x) | FR-01, FR-02 | FR-03 through FR-09; architecture mismatch, no OpenCode integration |
| shadcn AI Confirmation | UI Pattern | MIT | Reference | FR-01, FR-02 | Same — UI only, no backend integration |
| Tool UI ApprovalCard | UI Pattern | MIT | Reference | FR-01, FR-02 | Same — UI only, no backend integration |

## Evaluation

### Existing Internal Implementation

- **Strengths:** Full permission lifecycle handled: PermissionCard renders tool-specific content (bash/edit/write/webfetch) with syntax-highlighted previews and diff views. PermissionStore manages auto-accept per session with tree-scoped inheritance, local persistence (localStorage), and server-side notification suppression. Edit mode has three permission axes (edit, bash, webfetch) with allow/ask/deny/full states, visual color coding, per-session/per-agent overrides. Pending permissions trigger toasts when the session is not in view.
- **Weaknesses:** New agent default is not explicitly set to 'allow' (FR-08). Permission persistence uses local storage only, not OpenCode config layers (FR-09). No explicit unit tests for permission edge cases.
- **Integration effort:** Low — FR-08 is a one-line default change; FR-09 requires writing to the OpenCode config API
- **Cost:** Already maintained
- **Risks:** Local storage can be cleared; moving to OpenCode config layers ensures cross-device persistence

### agent-approval-card

- **Strengths:** Polished approval card with risk-level styling, inline JSON editing, rationale support, TypeScript-first
- **Weaknesses:** No auto-accept, no edit mode, no backend integration, no toast notifications, no OpenCode protocol awareness, early-stage (0.1.x)
- **Integration effort:** High — would need to replace the entire permission system
- **Cost:** Free
- **Risks:** Immature, no clear migration path, no OpenCode SDK integration

## Recommendation

**Direction:** Build (extend existing internal implementation)

The existing permission system covers all functional requirements except FR-08 (new agent defaults to 'allow') and FR-09 (config-layer persistence). These are straightforward additive changes: set `defaultEditMode` to 'allow' in `editPermissionDefaults.ts` and write a server-side API route to persist auto-accept settings via OpenCode config layers (similar to existing settings-runtime patterns). External libraries offer no advantage over what is already built.

## Sources of Information

- `packages/ui/src/components/chat/PermissionCard.tsx`: Permission card with tool-specific rendering
- `packages/ui/src/components/chat/PermissionRequest.tsx`: Legacy permission request component
- `packages/ui/src/stores/permissionStore.ts`: Zustand store with auto-accept, tree-scoped inheritance, persistence
- `packages/ui/src/lib/permissions/editPermissionDefaults.ts`: Default edit mode computation per agent
- `packages/ui/src/lib/permissions/editModeColors.ts`: Visual color coding for edit modes
- `packages/ui/src/stores/contextStore.ts`: Per-session/per-agent edit mode overrides
- `packages/ui/src/sync/sync-context.tsx`: SSE event handling for permission.asked/replied, toast notifications
- `packages/ui/src/types/permission.ts`: Permission request/response type definitions
- `packages/web/server/lib/opencode/settings-runtime.js`: Pattern for OpenCode config-layer persistence
- `packages/web/server/lib/opencode/settings-helpers.js`: Config merge helpers
- `agent-approval-card` on npm: Reference for approval card UX patterns
- `shadcn AI Confirmation` on shadcn.io: Reference for confirmation dialog patterns
- `Tool UI ApprovalCard` on tool-ui.com: Reference for binary confirmation patterns

## Open Questions

1. Should FR-08 apply only to newly created agents or also retroactively to existing agents that have no explicit rules?
2. Does the OpenCode SDK's config API support writing agent-level permission defaults or only reading them?
3. Should the config-layer persistence for auto-accept be scoped to a directory, project, or global?
