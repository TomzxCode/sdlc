---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

## Sync drift: 2026-11-16

### FR-4 omits the declared data queries capability that the code validates

- Status: BLOCKING
- Evidence:
  - `packages/gateway-protocol/src/schema/board.ts:94-111` defines `BoardWidgetDeclaredSchema` with a `queries` array, max 8 items, for named live GitHub Actions queries shared with session readers using the agent's credentials.
  - `src/boards/board-capabilities.ts:62-99` normalizes `queries` alongside `netOrigins` and `tools`, and lines 104-118 include `queries` in the granted subset check.
  - `src/boards/github-actions-capability.ts:9-11` defines `GITHUB_ACTIONS_BINDING_ID = "github.actions.runs"` and the guidance for declaring a query.
- Artifact currently says: FR-4 at line 36 enumerates only network origins and tools as the declared widget capabilities, and the FR-4 acceptance criteria at lines 141-159 cover only origins and tools.
- What the code actually does: a widget may declare named data queries with fixed selectors, result limits, and response fields, and a changed query definition requires renewed approval before its results are shared with session readers.
- Needed change: extend FR-4 and its acceptance criteria to cover the `queries` declaration, its normalization and count bound, the renewed-approval rule, and its inclusion in the grant subset check.

### No requirement covers the GitHub Actions grant capability

- Status: BLOCKING
- Evidence:
  - `src/boards/github-actions-capability.ts` validates the `github.actions.runs` grant, its repository and workflow selectors, and its field selection.
  - `src/boards/board-host-capability-ids.ts` includes `GITHUB_ACTIONS_BINDING_ID` in the shared host capability namespace.
  - Gateway tests exist at `src/gateway/server-methods/board.github-actions.test.ts` and `src/gateway/server-methods/board.github-actions-session-reader.test.ts`.
  - The specification's Risks and Unknowns at line 418 already notes that a GitHub Actions grant shares private repository data with the session audience.
- Artifact currently says: the requirements describe network-origin grants and tool grants, with no requirement for the GitHub Actions grant, its credential handling, or its wrong-repository and no-redirect rules.
- What the code actually does: an operator can grant a widget the `github.actions.runs` binding, and the Gateway enforces repository scoping, credential isolation, and no-redirect behavior.
- Needed change: add a functional requirement and acceptance criteria for the GitHub Actions grant capability, its operator approval, and its repository and redirect safety rules.

## Sync drift: 2026-11-23

Fresh reconciliation against current code confirms that the two blocking gaps recorded on 2026-11-16 remain open.
No new discrepancy was found in the requirements artifact.

### FR-4 still omits declared data queries

- Status: BLOCKING
- Evidence:
  - `packages/gateway-protocol/src/schema/board.ts:103-109` defines `queries` in `BoardWidgetDeclaredSchema` with `maxItems: 8` and a fixed GitHub Actions query selector contract.
  - `src/boards/board-capabilities.ts:79-99` normalizes `queries` and returns it in the resulting declaration.
  - `src/boards/board-capabilities.ts:103-114` includes `queries` in the grant subset check, which requires an exact JSON match on every query edit.
  - `src/boards/github-actions-capability.ts:9-12` defines `GITHUB_ACTIONS_BINDING_ID = "github.actions.runs"` and the author guidance for declaring a query.
- Artifact currently says: FR-4 at line 36 enumerates only network origins and tools, and its acceptance criteria at lines 141-159 cover only those two categories.
- What the code actually does: a widget declaration has three capability categories, and a changed query definition requires renewed operator approval.
- Needed change: extend FR-4 and its acceptance criteria to cover the `queries` declaration, its normalization, its count bound, and its exact-match grant rule.

### No requirement still covers the GitHub Actions grant capability

- Status: BLOCKING
- Evidence:
  - `src/boards/github-actions-capability.ts:9-12` defines the `github.actions.runs` binding and the author guidance.
  - `src/boards/board-host-capability-ids.ts:1,18` includes `GITHUB_ACTIONS_BINDING_ID` in the shared board host capability namespace.
  - `src/gateway/server-methods/board.github-actions.test.ts` and `src/gateway/server-methods/board.github-actions-session-reader.test.ts` exercise repository scoping, credential isolation, and no-redirect behavior.
- Artifact currently says: the functional requirements describe only network-origin and tool grants, with no requirement for the GitHub Actions grant or its safety rules.
- What the code actually does: an operator can grant a widget the `github.actions.runs` binding, and the Gateway enforces repository scoping, credential isolation, and no-redirect behavior before sharing results with session readers.
- Needed change: add a functional requirement and acceptance criteria for the GitHub Actions grant, its operator approval, and its repository and redirect safety rules.
