---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### The nine documented src/skills/workshop test paths no longer exist

- Status: BLOCKING
- Evidence:
  - The plan names `src/skills/workshop/skill-lint.test.ts` (TC-8), `changes.kernel.test.ts` (TC-9), `tool-policy-diagnostic.test.ts` (TC-10), `library.test.ts` (TC-38), `review-undo.test.ts` (TC-39), `unused-archive.test.ts` (TC-40), `experience-review.test.ts` (TC-41), `experience-review-scheduler.test.ts` (TC-42), and `review-outcome.test.ts` (TC-43) under `src/skills/workshop/`.
  - `src/skills/` has no `workshop/` directory, so all nine paths are absent.
  - Six suites moved to the plugin: `extensions/skill-workshop/src/skill-lint.test.ts`, `tool-policy-diagnostic.test.ts`, `library.test.ts`, `experience-review.test.ts`, `experience-review-scheduler.test.ts`, and `review-outcome.test.ts`.
  - `changes.kernel.test.ts` moved to `src/skills/workshop-changes/changes.kernel.test.ts`.
  - There is no `review-undo.test.ts` anywhere. Undo behavior is covered in `extensions/skill-workshop/src/review-service.test.ts`, `review-outcome.test.ts`, `gateway-methods.test.ts`, and `library.test.ts`.
  - There is no `unused-archive.test.ts` anywhere. Unused-skill archive behavior is covered in `extensions/skill-workshop/src/library.test.ts` and `review-service.test.ts`.
- Artifact currently says: the Workshop suites live in `src/skills/workshop/`, with one dedicated file per case row.
- What the code actually does: the suites live in the `skill-workshop` plugin or in `src/skills/workshop-changes/`, and undo and unused-archive cases share other files rather than having a dedicated file.
- Needed change: repoint TC-8, TC-9, TC-10, TC-38, and TC-41 through TC-43 at the plugin paths, repoint TC-9 at `workshop-changes/`, and split TC-39 and TC-40 across the files that now carry those cases.

### Three other documented test paths no longer exist

- Status: BLOCKING
- Evidence:
  - TC-31 and TC-67 name `src/skills/library/mutations-worker.test.ts`, which is absent and has no file with the same name elsewhere in the repository.
  - TC-12, TC-54, and TC-55 name `src/skills/loading/skill-root-discovery.test.ts`, which is absent and has no file with the same name elsewhere in the repository.
  - TC-47 names `src/cli/skills-cli.workshop.test.ts`, which is absent. The surviving file is `src/cli/skills-cli.workshop-contract.test.ts`.
- Artifact currently says: these three files still carry the named cases.
- What the code actually does: two files are gone and one was renamed.
- Needed change: find the current owners of the library worker and root-discovery cases and repoint TC-12, TC-31, TC-54, TC-55, and TC-67, and rename the source for TC-47.

### New plugin-owned suites are not documented

- Status: ADVISORY
- Evidence:
  - `extensions/skill-workshop/` has suites absent from the plan, including `src/drafts.test.ts`, `src/gateway-methods.test.ts`, `src/review-service.test.ts`, `src/cli.test.ts`, `src/tool.test.ts`, `src/skill-diet.test.ts`, `src/library.record-failure.test.ts`, and `doctor-health-api.test.ts`.
  - `src/cli/skills-cli.formatting.test.ts` and `src/skills/discovery/status.test.ts` are also present without being named in the plan.
- Artifact currently says: the plan covers the pipeline suites in `src/skills/` and the operator command suites in `src/cli/`.
- What the code actually does: the plugin owns a substantial set of Workshop suites, and the plan's Scope section does not mention them.
- Needed change: extend the Scope section to name the `skill-workshop` plugin suites and add case rows for the draft lifecycle and the Workshop gateway methods.
