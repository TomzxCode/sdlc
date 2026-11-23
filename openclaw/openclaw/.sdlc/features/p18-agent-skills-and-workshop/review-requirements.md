---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-23

Fresh analysis against current code confirms the blocking item from 2026-11-16 remains open, because requirements.md is unchanged.

### Blocking: the `propose` mode and the draft lifecycle are still absent

- `requirements.md:38` (FR-13) still names only the `auto` mode and omits `propose`.
- `requirements.md:59` still says the Workshop path applies changes immediately and does not route changes through a proposal approval flow.
- `extensions/skill-workshop/openclaw.plugin.json:24` still describes a `propose` mode that saves background review changes as drafts for `/learn drafts`, and `:46-49` still lists `off`, `propose`, and `auto` in the config enum.
- `extensions/skill-workshop/src/gateway-methods.ts:220` and `:235` still register `skills.workshop.applyDraft` and `skills.workshop.discardDraft`.
- `extensions/skill-workshop/src/drafts.ts:91`, `:112`, `:151`, `:178`, and `:202` still implement the list, save, view, discard, and apply draft lifecycle.
- `extensions/skill-workshop/src/cli.ts:84` still renders the `Drafts (review with /learn drafts)` heading.
- Needed change is unchanged: add a requirement for `propose` and the draft lifecycle, and scope the immediate-apply constraint to `auto` mode.
