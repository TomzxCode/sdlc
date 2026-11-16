---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
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
