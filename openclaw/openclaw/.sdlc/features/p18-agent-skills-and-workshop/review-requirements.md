---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### FR-13 and the Workshop constraint omit the propose mode and the draft flow

- Status: BLOCKING
- Evidence:
  - FR-13 describes an autonomous review that runs when the Workshop autonomous mode is `auto`, with no other non-off mode named.
  - The constraint "The Workshop path applies changes immediately and makes them undoable. It does not route changes through a proposal approval flow" rules out any draft-based path.
  - `extensions/skill-workshop/openclaw.plugin.json` declares `autonomous.mode` with the enum `off`, `propose`, and `auto`, and its help text says `propose` saves what background reviews would change as drafts for review with `/learn drafts`.
  - `extensions/skill-workshop/src/gateway-methods.ts` registers `skills.workshop.applyDraft` at line 224 and `skills.workshop.discardDraft` at line 239, alongside the documented `skills.workshop.undo` and the other Workshop methods.
  - `extensions/skill-workshop/src/drafts.ts` and `extensions/skill-workshop/src/drafts.test.ts` implement and test the draft lifecycle.
- Artifact currently says: the Workshop loop applies changes immediately with an undo-only reversal path, and the only autonomous mode named is `auto`.
- What the code actually does: the plugin adds a `propose` mode that writes review changes as drafts instead of applying them, with two new RPC methods and a `/learn drafts` command for accepting or discarding those drafts.
- Needed change: add a requirement for the `propose` mode and the draft lifecycle, and qualify the immediate-apply constraint so it applies to `auto` mode rather than to every Workshop path.
