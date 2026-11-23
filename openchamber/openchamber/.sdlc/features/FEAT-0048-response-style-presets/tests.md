---
title: "Response Style Presets"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Response Style Presets

## Scope

This plan records the tests that exist for preset instruction resolution, per-session instruction entry writes, and local settings persistence.
Preset selection UI, preview copy, custom preset creation in the UI, and the model's resulting response style are outside the recorded test coverage.

## Unit tests

| ID | Test file | Behavior covered |
|---|---|---|
| TC-1 | `packages/ui/src/lib/responseStyle.test.ts` | A style changed on another device is picked up after the settings read cache expires. |
| TC-2 | `packages/web/server/lib/settings/settings-helpers.test.js` | `responseStyleEnabled`, `responseStylePreset`, and `responseStyleCustomInstructions` are accepted as valid persistable registry values. |

## Integration tests

| ID | Test file | Behavior covered |
|---|---|---|
| TC-3 | `packages/ui/src/lib/sessionKnowledgeApi.test.ts` | The VS Code transport writes, changes, and clears the `openchamber.response-style` instruction entry for a session, and includes the style in isolated-space knowledge sync. |
| TC-4 | `packages/web/server/lib/session-knowledge/routes.test.js` | The sync route trims a style string, preserves null, and drops an invalid style object before calling the runtime. |
| TC-5 | `packages/web/server/lib/session-knowledge/runtime.test.js` | The runtime writes the style under its own session instruction key, leaves an omitted style alone, clears an empty style, and preserves a long custom instruction without increasing knowledge budgets. |

## End-to-end tests

No end-to-end tests exist for this feature.

## Edge cases and failure scenarios

| ID | Scenario | Expected behavior |
|---|---|---|
| TC-6 | A style changes on another device while this window still holds a cached settings document. | The old instruction is used until the read cache expires, then the new instruction is used. |
| TC-7 | A session sync omits the response style. | The existing instruction entry stays in place. |
| TC-8 | A session sync sends an empty response style. | The instruction entry is removed. |
| TC-9 | A custom instruction is longer than the pinned knowledge budget. | The full custom instruction is kept and only pinned content is truncated. |
| TC-10 | The sync route receives a style that is not a string. | The route normalizes it to undefined without failing the request. |

## Test infrastructure

- `bun:test` runs all five test files.
- Fetch spies and `invalidateSettingsCache` isolate the settings read cache test.
- A VS Code `window` stub and the real SDK transport exercise session instruction writes.
- Express and Supertest exercise the session knowledge sync route.
- Runtime stubs stand in for instruction entries, metadata, memory, and project context.

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-01 | Partial: TC-1 exercises the concise and detailed preset instructions. Gap: no test enumerates every built-in preset or checks each preset's text. |
| FR-02 | TC-3 |
| FR-03 | Gap: no test observes an AI response and checks that it follows the active style. |
| FR-04 | Partial: TC-2 and TC-5 persist and preserve custom instructions. Gap: no UI test creates a custom preset. |
| FR-05 | Gap: no test covers the preset description shown in the selector. |
| FR-06 | TC-3, TC-4, TC-5 |
| FR-07 | Partial: TC-2 confirms local settings persistence. Gap: no test asserts the absence of sharing or marketplace UI. |

## Gaps

No test renders the preset selector in the chat input or the preset controls in Behavior settings.
No test covers the `getResponseStylePreview` behavior behind the preset description.
