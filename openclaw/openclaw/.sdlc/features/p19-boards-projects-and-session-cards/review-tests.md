---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-23
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-11-23

Fresh reconciliation against current test code found one documented case whose input and expected output do not match the named test file.
No review findings file existed for this artifact before this sync.

### TC-14 documents a step count that the channel summary suite does not exercise

- Status: BLOCKING
- Evidence:
  - `src/session-cards/progress-card-channel-summary.test.ts:5-55` is the channel summary suite named by TC-14 and TC-15.
  - The suite's checklist cases at `src/session-cards/progress-card-channel-summary.test.ts:6-13` and `src/session-cards/progress-card-channel-summary.test.ts:41-49` use one completed step and expect `1/1 complete`.
  - No case in that file uses three steps with two completed, and no case expects `2/3 complete`.
  - The production formatter in `src/session-cards/progress-card-channel-summary.ts` is not part of this test file's assertions for the documented TC-14 input.
- Artifact currently says: TC-14 at line 39 describes two of three steps completed and expects the summary to report `2/3 complete` together with the normalized steps.
- What the test code actually does: the suite proves the completed-step counter with a single completed step and reports `1/1 complete`.
- Needed change: add a three-step case with two completed steps to the channel summary suite, or change TC-14 to describe the one-of-one case that the suite already covers.

### TC-16 claims pull request and archived match coverage in the shared contract suite

- Status: ADVISORY
- Evidence:
  - `packages/workboard-contract/src/sessions-board.test.ts:39-51` normalizes only `health` and `run` match rules.
  - `packages/workboard-contract/src/sessions-board.ts:187,193-197` accepts `pullRequest` and `archived` match keys in addition to `health` and `run`.
  - `extensions/workboard/src/sessions-board.test.ts:256` exercises a combined `health`, `run`, `pullRequest`, and `archived` match, but that file belongs to the plugin suite, not the pure contract suite named in the Test Infrastructure section.
- Artifact currently says: TC-16 at line 16 describes a column match over observer health, run state, pull request state, and the archived flag.
- What the test code actually does: the shared contract suite covers health and run normalization, while pull request and archived normalization is covered only in the plugin suite.
- Needed change: split TC-16 into the contract cases and the plugin case, or move the combined match case into the shared contract suite.
