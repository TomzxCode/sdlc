---
title: "Custom Slash Commands"
status: done
---

# Test Plan: Custom Slash Commands

## Scope

Tests cover the composer slash-command submission path and the command autocomplete items used by the chat composer, plus the commands store state.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Slash command submission builds the outgoing message correctly | Composer input with `/command ...` | Outgoing message with the resolved command/args |
| TC-2 | Slash command variants produce expected message parts | `buildOutgoingMessage` inputs | Correct parts for slash vs free-text |
| TC-3 | Command autocomplete items resolve commands/aliases | Query text in composer | Correct autocomplete item list |
| TC-4 | Commands store manages command state | Store actions | State updated per action |

## Test Files

- `packages/ui/src/components/chat/composer/submit/__tests__/slashCommands.test.ts`
- `packages/ui/src/components/chat/composer/submit/__tests__/buildOutgoingMessage.test.ts`
- `packages/ui/src/components/chat/__tests__/commandAutocompleteItems.test.ts`
- `packages/ui/src/stores/useCommandsStore.test.ts`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR (slash command execution) | TC-1, TC-2 |
| FR (autocomplete) | TC-3 |
| FR (custom command management) | TC-4 |
