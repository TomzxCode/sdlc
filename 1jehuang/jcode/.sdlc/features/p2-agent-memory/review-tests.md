---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-2 | `crates/jcode-base/src/memory_agent_tests.rs`, described as "Agent produces valid memory candidates" | The file exists but the description is wrong. Its four tests are `extraction_transcript_omits_internal_system_reminders`, `missing_jev_access_clears_pending_without_fallback`, `manager_without_working_dir_does_not_infer_process_project`, and `retained_recall_pipeline_uses_jev_http_without_embeddings_or_sidecar`. None asserts that the agent produces memory candidates. | Reword the description to match the four real tests, and state that the automatic recall path is disabled. |
| TC-3 | `crates/jcode-session-types/src/session_search_tests.rs` | The file does not exist. The module was inlined as `mod session_search_tests` at `crates/jcode-session-types/src/lib.rs:984` with 7 test functions. | Point TC-3 at `crates/jcode-session-types/src/lib.rs` (the inline `session_search_tests` module) and, for p5, at `crates/jcode-app-core/src/tool/session_search_tests.rs`. |
| TC-6 | "Empty memory store" edge case, with no file | Covered by `crates/jcode-base/src/memory_jev_tests.rs:151` (`empty_and_zero_limit_never_call_transport`) and `:307` (`manager_scope_active_filter_and_storage_failures`). | Name the covering file. |
| TC-7 | "Very large session files / SIMD path", with no file | No dedicated test was found for large-file session search. The memchr path is `crates/jcode-session-types/src/lib.rs:555-575`. | Either drop the case or state explicitly that it is uncovered. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-base/src/memory_jev_tests.rs` (14 tests: Jev recall batch building, strict answer mapping, byte budgets, fail-closed thresholds, full-store scans, duplicate ids)
- `crates/jcode-memory-types/src/graph/graph_tests.rs` (16 tests: graph edges, tags, supersede, cascade retrieval, legacy migration)
- `src/cli/commands_tests.rs` (three memory CLI tests, including `memory_cli_semantic_requires_jev_but_keyword_search_remains_local`)

## Quality

The existing entries (TC-1 `crates/jcode-base/src/memory_tests.rs`, TC-4 the MiniLM embedding CI cohort, TC-5 `scripts/test_memory.py`) all still exist and remain accurate.

## Correctness

No issues found.

## Maintainability

No issues found.
