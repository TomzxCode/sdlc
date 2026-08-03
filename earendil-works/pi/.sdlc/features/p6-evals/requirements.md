---
title: "Evals"
status: done
---

# Requirements: Evals

## Overview

`@earendil-works/pi-evals` provides behavioral, model-backed evals for Pi workflows.
Evals adapt a real `AgentSession` to `vitest-evals`, run it in isolated temporary project and agent directories, and attach native Pi session artifacts.
They measure end-to-end behavior to compare prompts, tools, skills, models, or other harness configurations.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Maintainers | Behavioral regression signals for Pi workflows across model/harness configurations |
| Contributors | A harness for validating extensions, prompts, skills, and tools |
| Model/tool researchers | Apples-to-apples comparisons of prompt/model/tool configs |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall adapt a real `AgentSession` to the `vitest-evals` harness interface. |
| FR-02 | Must | The system shall run each eval in an isolated temporary project directory and agent directory. |
| FR-03 | Must | The system shall attach native Pi session artifacts to eval results. |
| FR-04 | Must | The system shall be runnable from the repo root via `npm run eval` with a provider/model default. |
| FR-05 | Should | The system shall support filtering evals by file or by test name (Vitest forwarding). |
| FR-06 | Should | The system shall ship a set of core evals (e.g. smoke, extensions). |
| FR-07 | Should | The system shall allow harnesses to configure their own model, overriding the default. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Evals shall be isolated (temp dirs) so runs do not touch the real workspace. |
| NFR-02 | Must | Security | Evals shall not require real provider keys beyond the user's normal Pi auth. |
| NFR-03 | Should | Maintainability | Results shall include session artifacts so failures are diagnosable. |

## Constraints

- Requires a configured provider/model (CLI values or `PI_PROVIDER`/`PI_MODEL`).
- Requires the normal Pi `ModelRuntime` auth (subscription credentials or API-key env vars).
- Evals are model-backed; they cost tokens and are not part of the default `test.sh` suite.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a working Pi installation with a provider configured
    - **When** `npm run eval` runs
    - **Then** an `AgentSession` runs inside the `vitest-evals` harness in an isolated temp dir.
- [ ] **FR-02**
    - **Given** an eval run
    - **When** it executes
    - **Then** the project and agent directories are temporary and isolated.
- [ ] **FR-04**
    - **Given** a repo with a provider/model configured
    - **When** `npm run eval -- --provider openai --model gpt-5.6-sol` runs
    - **Then** evals execute with that default.
- [ ] **FR-05**
    - **Given** many evals
    - **When** `npm run eval -- src/extensions.eval.ts` or `-t "<name>"` is used
    - **Then** only the matching evals run.

## Conflicts

None identified yet.

## Open Questions

1. Should evals be integrated into CI with a pinned model, or stay local/on-demand only?
