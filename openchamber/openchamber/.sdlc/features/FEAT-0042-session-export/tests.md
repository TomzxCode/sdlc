---
title: "Session Export"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Session Export

## Scope

This plan records the tests that exist for formatting a session as Markdown and nesting sub-agent sessions.
Browser download, desktop save dialogs, file reveal, and runtime-specific export UI are outside the recorded test coverage.

## Unit tests

| ID | Test file | Behavior covered |
|---|---|---|
| TC-1 | `packages/ui/src/lib/exportSession.test.ts` | Attached context is exported as a Context section while server prompt plumbing is dropped. |
| TC-2 | `packages/ui/src/lib/exportSession.test.ts` | The thinking level appears beside the model for the main agent and for a sub-agent. |
| TC-3 | `packages/ui/src/lib/exportSession.test.ts` | An absent, default, or none variant leaves the model name alone. |
| TC-4 | `packages/ui/src/lib/sessionTitle.test.ts` | A quoted reply appears once with paragraph separation when a child session is included in the export. |
| TC-5 | `packages/ui/src/lib/sessionTitle.test.ts` | Browser, PR, code, and terminal contexts are formatted as quotes with user comments kept separate. |
| TC-6 | `packages/ui/src/lib/sessionTitle.test.ts` | Legacy terminal context and malformed metadata remain readable in the export. |

## Integration tests

No integration tests exist for this feature.

## End-to-end tests

No end-to-end tests exist for this feature.

## Edge cases and failure scenarios

| ID | Scenario | Expected behavior |
|---|---|---|
| TC-7 | A session contains synthetic record plumbing without an attached context part. | The plumbing record is omitted from the Markdown. |
| TC-8 | A session contains a child session with a thinking variant. | The child's model and thinking level appear in its nested section. |
| TC-9 | An assistant message has no variant or has default or none. | No thinking suffix is added to the model. |
| TC-10 | A terminal context uses the legacy `<terminal_context>` shape. | The text is preserved instead of being parsed as a structured context. |

## Test infrastructure

- `bun:test` runs both test files.
- Fixtures build `Message` and `Part` records directly.
- `createContextPart` supplies attached chat-quote data.
- The tests call `formatSessionAsMarkdown` in process and do not use DOM, fetch, or runtime mocks.

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-01 | TC-1, TC-4, TC-5, TC-6 |
| FR-02 | Partial: TC-1 covers Context and Assistant role markers, and TC-2 and TC-3 cover model info. Gap: no test asserts a formatted timestamp. |
| FR-03 | TC-2, TC-4 |
| FR-04 | Gap: no test covers `downloadAsMarkdown` or `saveAsMarkdownDesktop`. |
| FR-05 | Gap: no test covers `revealExportedMarkdown`. |
| FR-06 | Gap: no test checks the export dialog across web, desktop, and VS Code runtimes. |

## Gaps

No test renders the export action in the session header or sidebar menu and verifies a downloaded file.
No test asserts a formatted timestamp in the exported Markdown.
