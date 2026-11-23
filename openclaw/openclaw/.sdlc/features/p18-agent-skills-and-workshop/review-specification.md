---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-11-16

### Workshop is a plugin, not a stage of the src/skills pipeline

- Status: BLOCKING
- Evidence:
  - The Overview says `workshop/` owns the change feed, experience review, usage tracking, lint, archive, restore, and undo inside the `src/skills/` staged pipeline.
  - The Architecture diagram places `WS` inside the `Pipeline[src/skills/]` subgraph and draws `WS --> T6`, `WS --> TOOL`, and `WS --> RT`.
  - The Technical Decisions row "One owner per pipeline stage" lists `workshop/` among the `src/skills/` stages.
  - `src/skills/` has no `workshop/` directory. It has `workshop-changes/` with `changes.kernel.ts`, `changes.ts`, and `changes.worker.ts`, which own the change feed kernel and worker only.
  - The experience review, review undo, lint, unused-skill archive, library, tool policy diagnostic, and Workshop CLI live in `extensions/skill-workshop/src/`, registered as the `skill-workshop` plugin with `enabledByDefault: true`.
- Artifact currently says: the Workshop is the seventh owner stage in the `src/skills/` pipeline.
- What the code actually does: the change feed kernel stays in core under `src/skills/workshop-changes/`, and the rest of the Workshop behavior is a bundled plugin under `extensions/skill-workshop/`.
- Needed change: move the Workshop stage out of the `src/skills/` pipeline description and diagram, show it as a plugin that consumes the change feed tables and the `skill_workshop` tool, and update the Technical Decisions row.

### The bundled skill count is 52, not 50

- Status: BLOCKING
- Evidence:
  - The Overview says the `skills/` directory holds 50 bundled skills, and the Architecture diagram labels the bundled root as `bundled skills/ (50)`.
  - `find skills -name SKILL.md` returns 52 files, and `skills/` has 52 immediate subdirectories.
  - `custodian-skills/` has 4 `SKILL.md` files, which still matches the stated playbook count.
- Artifact currently says: 50 bundled skills.
- What the code actually does: 52 bundled skills ship in `skills/`.
- Needed change: update the Overview and the diagram to 52, or state the count as a dynamic value rather than a fixed number.

### The API contract omits the draft methods

- Status: BLOCKING
- Evidence:
  - The API Contracts table lists the `skills.workshop.*` methods through `skills.workshop.undo` and does not name any draft method.
  - `api.yaml` has no `draft`, `applyDraft`, or `discardDraft` entry.
  - `extensions/skill-workshop/src/gateway-methods.ts:224` and `:239` register `skills.workshop.applyDraft` and `skills.workshop.discardDraft`, and `extensions/skill-workshop/src/drafts.test.ts` covers them.
  - The plugin config declares a `propose` autonomous mode that produces those drafts, which the specification does not describe.
- Artifact currently says: the Workshop RPC surface ends at list, changes, read, archive, restore, and undo.
- What the code actually does: two additional Workshop methods create and discard drafts for the `propose` mode.
- Needed change: add `skills.workshop.applyDraft` and `skills.workshop.discardDraft` to the API Contracts table and to `api.yaml` with their request and response schemas, and describe the `propose` mode in the sequences.

## Sync drift: 2026-11-23

Fresh analysis against current code confirms the three blocking items from 2026-11-16 remain open, because specification.md and api.yaml are unchanged.

### Blocking: Workshop is still described as a `src/skills/` pipeline stage

- `specification.md:11`, `:37`, and `:332` still place `workshop/` inside the `src/skills/` staged pipeline and name it as one of the owner stages.
- `src/skills/` has no `workshop/` directory. It has `src/skills/workshop-changes/changes.kernel.ts`, `changes.ts`, and `changes.worker.ts`, which own the change feed kernel and worker only.
- `src/skills/workshop-changes/changes.ts:1-8` imports the kernel and state worker helpers and holds the change store, so this directory owns persistence, not the full Workshop loop.
- `extensions/skill-workshop/` holds the experience review, undo, lint, unused-skill archive, library, tool policy diagnostic, and CLI sources, and `extensions/skill-workshop/openclaw.plugin.json:6` sets `enabledByDefault: true`, so it ships as a bundled plugin.

### Blocking: the bundled skill count is still stated as 50

- `specification.md:11` still says the `skills/` directory holds 50 bundled skills, and `:25` still labels the diagram root `bundled skills/ (50)`.
- `find skills -name SKILL.md` returns 52 files, and `skills/` has 52 immediate subdirectories.
- `custodian-skills/` still has 4 `SKILL.md` files, which matches the stated playbook count.

### Blocking: the API contract still omits the draft methods

- `specification.md:231-236` still ends the Workshop API table at `skills.workshop.undo`.
- `api.yaml` has no occurrence of `draft`, `applyDraft`, or `discardDraft`.
- `extensions/skill-workshop/src/gateway-methods.ts:220` and `:235` still register `skills.workshop.applyDraft` and `skills.workshop.discardDraft`.
- `extensions/skill-workshop/src/drafts.test.ts` still covers the draft lifecycle, and `extensions/skill-workshop/openclaw.plugin.json:24` still documents the `propose` mode that produces those drafts.
