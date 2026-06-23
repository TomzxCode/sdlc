---
issue: ""
title: "Custom Slash Commands"
status: draft
---

# Existing Solutions: Custom Slash Commands

## Overview

The codebase already has a comprehensive custom slash command system with full CRUD, user/project scope, chat autocomplete integration, and server-side storage in `.opencode/commands/` or `~/.config/opencode/commands/`. The implementation is distributed across `useCommandsStore`, `CommandsPage`, `CommandsSidebar`, and the `ChatInput` slash-command dispatch logic. The recommendation is to adopt the existing implementation with refinements rather than build from scratch or adopt external libraries.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useCommandsStore.ts`, `packages/ui/src/components/sections/commands/`, `packages/ui/src/components/chat/ChatInput.tsx` |
| Open-source | Yes | tiptap slash-command extensions, cmdk, prosemirror-slash-menu-react, Slack/Discord slash command patterns |
| Commercial / SaaS | Yes | Slack Slash Commands, Discord Slash Commands, Linear command menu |
| Standards / protocols | Yes | Notion-style slash commands, terminal shell command patterns |
| Reference material | Yes | OpenCode command semantics documentation |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing useCommandsStore + ChatInput dispatch | Internal | MIT | Mature | FR-01 through FR-07 | None significant |
| tiptap slash-command extension | Library | MIT | Mature | FR-03 | Rich-text editor only; not plain textarea |
| cmdk (⌘K command menu) | Library | MIT | Mature | FR-03, FR-05 | General command palette; no `/` trigger |
| prosemirror-slash-menu-react | Library | MIT | Active | FR-03 | ProseMirror-specific; not suitable for chat input |
| Slack / Discord slash commands | Reference | Proprietary | Mature | FR-01, FR-02, FR-03 | Reference pattern only; not a library |

## Evaluation

### Existing useCommandsStore + ChatInput Dispatch

- **Strengths:** Full CRUD (`createCommand`, `updateCommand`, `deleteCommand`, `loadCommands`) with retry logic and config sync. `/` autocomplete integration in chat input. User/project scope support backed by server file storage. Built-in commands (`/summary`, `/explore`, `/debug`, `/weigh`, `/undo`, `/redo`, `/timeline`, `/compact`) with magic prompt templates. Settings page with `CommandsPage`, `CommandsSidebar`, and `AgentSelector`. Commands are stored as plain markdown templates per spec. Scope detection via file sources. Localized i18n for all command settings labels.
- **Weaknesses:** Autocomplete rendering uses a custom implementation rather than a standard library. No explicit test suite for the autocomplete surface.
- **Integration effort:** Low. All requirements are met. The main refinement is polish on the autocomplete UI.
- **Cost:** Free (MIT).
- **Risks:** Low. Already shipping in production.

### tiptap slash-command extension (and similar)

- **Strengths:** Well-established pattern for rich-text editors. Keyboard navigation, filtering, and command execution built in.
- **Weaknesses:** Designed for rich-text editors (ProseMirror/TipTap), not plain-text textareas. OpenChamber chat input uses a `<textarea>`. Switching to a rich-text editor would be a massive architectural change with no benefit for this use case.
- **Integration effort:** High. Would require replacing the chat input component.
- **Cost:** Free (MIT).
- **Risks:** Architectural mismatch. Risk of breaking existing chat input features (autocomplete, file mentions, attachments, shell mode, mobile).

## Recommendation

**Direction:** Adopt

The existing custom slash command implementation meets all functional requirements. The command system is already integrated with the OpenCode config filesystem (`/api/config/commands/`), supports user/project scope, appears in chat autocomplete, and uses plain markdown templates with no variable interpolation. No external library adoption is warranted.

## Sources of Information

- `packages/ui/src/stores/useCommandsStore.ts`: Full CRUD store with OpenCode config API integration.
- `packages/ui/src/components/sections/commands/CommandsPage.tsx`, `CommandsSidebar.tsx`: Settings UI for command management.
- `packages/ui/src/components/sections/commands/AgentSelector.tsx`: Agent selection within command config.
- `packages/ui/src/components/chat/ChatInput.tsx:1846-1909`: Slash command dispatch in chat input.
- `packages/ui/src/lib/i18n/messages/en.settings.ts:458,1691-1703`: Localized command and magic prompt labels.
- `packages/ui/src/constants/sidebar.ts:30`: Navigation entry for commands settings.
- `packages/docs/content/docs/commands-snippets.mdx`: Documentation for commands and snippets.

## Open Questions

1. Should the autocomplete dropdown visually distinguish built-in commands, custom commands, and skills with distinct badges or icons?
2. Should there be a keyboard shortcut reference panel visible when typing `/`?
