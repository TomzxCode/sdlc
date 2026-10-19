---
title: "Productivity Reporting"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Productivity Reporting

## Scope

Covers the aggregation, rendering, and failure-handling behavior of the productivity report.
The unit tests build reports from in-memory `SessionSummary` values, so they exercise the aggregation and both renderers without touching the transcript store.
The integration test covers the TUI side of the report lifecycle, the delivery of the result event, and the failure path.
Out of scope: the disk scan and the incremental cache, which have no automated test and are exercised through the crate example harness.
Coverage gaps: no automated test covers the scan, the cache, the command aliases, the clipboard integration, or the runtime `productivity` command.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Aggregate per-session summaries into report totals, activity buckets, project count, power score, and archetype | `crates/jcode-productivity-core/src/tests.rs`, test `aggregates_basic_totals`, three sessions with ten prompts, ten assistant messages, twenty-three tool calls, and five code edits | Report records three sessions, ten prompts, ten assistant messages, twenty-three tool calls, five code edits, four commands, seven searches, one web action, two distinct projects, a power score above zero, and a non-empty archetype |
| TC-2 | Rank the top-N lists by count in descending order | `crates/jcode-productivity-core/src/tests.rs`, test `top_lists_sorted_desc`, two `alpha` sessions and one `gamma` session | The first project is `alpha` with count two, and the first tool is `read` with count fifteen |
| TC-3 | Deduplicate active dates and compute the longest consecutive-day streak | `crates/jcode-productivity-core/src/tests.rs`, test `streaks_and_active_days_dedup`, one session active on 2026-05-10, 2026-05-11, 2026-05-12, and 2026-05-20 | Report records four active days, a longest streak of three days, a first day of 2026-05-10, and a last day of 2026-05-20 |
| TC-4 | Render the Markdown, the SVG, and the PNG for a populated report | `crates/jcode-productivity-core/src/tests.rs`, test `renders_markdown_and_png`, one session with four prompts and ten tool calls | The Markdown contains the report title and the power score, the SVG starts with `<svg` and contains a text element, and the PNG is larger than 1000 bytes and carries the PNG signature |
| TC-5 | Render an empty report without failing | `crates/jcode-productivity-core/src/tests.rs`, test `empty_report_is_safe`, an empty summary list | The report records zero sessions, the Markdown still contains the report title, and the PNG is produced and carries the PNG signature |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Handle a failed report result delivered over the remote bus event path | `crates/jcode-tui/src/tui/app/tests/remote_events_reload_01/part_01.rs`, test `test_remote_bus_productivity_failure_clears_refresh_state`, a test app with the in-flight flag set and a result event carrying the error `generation failed` | The event is handled, the in-flight flag is cleared, the status notice reads `Productivity report failed`, and the last display message contains the error text |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-7 | Manual end-to-end run of the full pipeline against the real transcript store, through the crate example harness | Run `cargo run -p jcode-productivity-core --example run` (`crates/jcode-productivity-core/examples/run.rs`) on a machine with transcripts under the jcode home directory | The harness prints the scan counters (`scanned`, `parse_errors`, `cache_hits`, `scan_secs`) and the Markdown report, and a dashboard PNG is written under `generated-images` in the jcode home directory. A second run reports a cache hit for every transcript and a shorter scan time |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | One transcript file is not valid JSON | The file is counted as a parse error, the scan continues over the remaining transcripts, and the report is still produced |
| TC-9 | The scan cache file is missing or corrupted | The cache read and parse failure is ignored, the scan starts from an empty cache, and the report is still produced |
| TC-10 | The scan cache was written by an older cache format | The version mismatch discards the cached entries and the transcripts are re-parsed |
| TC-11 | There are no transcripts at all | The report records zero sessions, the Markdown still renders, and the PNG is still produced |
| TC-12 | The system clipboard is unavailable | The Markdown report is still displayed and the footer states that the image could not be copied |
| TC-13 | A second report is requested while one is already generating | The second request is refused with a status notice and no second generation is started |
| TC-14 | A report result arrives for a different session | The event is ignored and nothing is displayed |
| TC-15 | A report result carries an error instead of a payload | The in-flight flag is cleared, an error message is displayed, and the status notice reports the failure (covered by TC-6) |
| TC-16 | A dashboard label contains emoji the system font cannot render | The emoji are stripped before the SVG is built so the PNG shows no tofu boxes |

## Test Infrastructure

- `crates/jcode-productivity-core/src/tests.rs` is the crate's `#[cfg(test)]` module and runs with `cargo test -p jcode-productivity-core`.
- All unit tests build their inputs as in-memory `SessionSummary` values, so they need no fixtures, no transcript files, and no network access.
- The PNG assertions check the PNG signature and a minimum byte size, because the exact bytes depend on the system font database of the test machine.
- The TUI integration test uses the shared `create_test_app()` helper and a dummy remote connection from `crates/jcode-tui/src/tui/backend/`.
- `crates/jcode-productivity-core/examples/run.rs` is a manual harness rather than an automated test; it exercises the real scan, the real cache, and the real PNG write.
- No productivity test file exists under the repository-level `tests/` directory.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-7, TC-8 |
| FR-2 | TC-7, TC-9, TC-10 |
| FR-3 | TC-1, TC-3 |
| FR-4 | TC-1, TC-2 |
| FR-5 | TC-4, TC-5 |
| FR-6 | TC-4, TC-5, TC-7 |
| FR-7 | TC-7 |
| FR-8 | TC-6, TC-14 |
| FR-9 | TC-6, TC-12, TC-13 |
| FR-10 | TC-1, TC-2 |
| FR-11 | TC-7 |
| FR-12 | TC-3 |
| NFR-1 | TC-4, TC-7 |
| NFR-2 | TC-7, TC-9, TC-10 |
| NFR-3 | TC-1, TC-3 |
| NFR-4 | TC-8 |
| NFR-5 | TC-6, TC-13 |
| NFR-6 | TC-4, TC-16 |
