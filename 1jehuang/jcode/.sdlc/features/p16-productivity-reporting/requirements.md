---
title: "Productivity Reporting"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Productivity Reporting

## Overview

jcode already stores every session transcript on the local disk, but that history is not visible to the user in any form. This feature turns the local history into a report the user can read and share, without sending anything to a server. A scan pass reads the local transcript store and produces one compact summary per session, an aggregation pass folds those summaries into a single report of sessions, prompts, tool calls, tokens, projects, and activity patterns, and two renderers turn the report into Markdown for the chat transcript and into a PNG dashboard saved with the other generated images. The report is reachable from the `/productivity` slash command, from the `/wrapped` and `/stats` aliases, and from the runtime `productivity` command used by non-terminal clients. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | A readable summary of their own usage history that they can copy, paste, and share outside the terminal. |
| Maintainer | A deterministic report pipeline that reads only local data and can be exercised from unit tests. |
| Non-terminal clients | A machine-readable report and dashboard image over the runtime command surface. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall scan the local session transcript store under the jcode home directory and produce one compact summary per transcript file. |
| FR-2 | Must | The system shall reuse an incremental scan cache keyed by transcript file length and modification time so unchanged transcripts are not re-parsed on later runs. |
| FR-3 | Must | The system shall aggregate the per-session summaries into a single report covering sessions, prompts, assistant messages, tool calls, images, token usage, typed characters, and active days. |
| FR-4 | Must | The system shall tally tool calls per canonical tool name, expanding batched invocations so each inner tool call is counted, and normalizing legacy tool aliases to their canonical names. |
| FR-5 | Must | The system shall render the report as Markdown suitable for display in the chat transcript. |
| FR-6 | Must | The system shall render the report as a PNG dashboard image and save it to `generated-images/productivity-<timestamp>.png` under the jcode home directory. |
| FR-7 | Must | The system shall expose the report through the `/productivity` slash command, with `/wrapped` and `/stats` accepted as aliases. |
| FR-8 | Should | The system shall generate the report off the user-interface thread and deliver the result to the session that requested it. |
| FR-9 | Should | The system shall copy the dashboard image to the system clipboard and open it in the default image viewer, and report which of those actions succeeded. |
| FR-10 | Should | The system shall derive activity buckets (code edits, commands run, searches, web actions) and shareable flavor (archetype, power score, badges) from the aggregated tallies. |
| FR-11 | Should | The system shall expose the same report to non-terminal clients through the runtime `productivity` command, returning the structured report, the PNG path, and the PNG as base64. |
| FR-12 | May | The system shall record the activity calendar (hour of day, weekday, active dates) and the current and longest consecutive-day streaks. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Privacy | The system shall perform every step locally, with no network request, no account, and no upload of transcript content. |
| NFR-2 | Must | Performance | The system shall complete a repeated run over an unchanged transcript store without re-parsing any file. |
| NFR-3 | Must | Performance | The system shall hold only a compact per-session summary in memory while scanning, not the full transcript content. |
| NFR-4 | Should | Reliability | The system shall count an unreadable or malformed transcript as a parse error and continue the scan. |
| NFR-5 | Should | Availability | The system shall keep the user interface responsive while the report is generated. |
| NFR-6 | Should | Portability | The system shall rasterize the dashboard locally, without a headless browser and without downloading fonts over the network. |

## Constraints

- The report is derived only from transcripts that already exist on the local disk.
- Transcripts are read with a tolerant partial deserializer rather than the canonical session types, so the crate stays independent of the transcript schema.
- The dashboard is built as an SVG string in process and rasterized with a local SVG renderer.
- The scan cache lives beside the other jcode cache files and is keyed by a per-file fingerprint.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Scan produces one summary per transcript
      Given a jcode home directory containing three transcript files under sessions
      When the scan runs
      Then three session summaries are produced and the report records three scanned files
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Unchanged transcripts are not re-parsed
      Given a scan cache holding a fingerprint for every transcript
      When a second scan runs over the same unchanged transcripts
      Then every file is served from the cache and the cache hit count equals the number of transcripts
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Totals are folded across sessions
      Given three sessions with ten user prompts, ten assistant messages, and twenty-three tool calls in total
      When the report is built
      Then the report records three sessions, ten prompts, ten assistant messages, and twenty-three tool calls
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Batched calls are credited to the inner tools
      Given a session whose transcript contains one batch call wrapping two inner tool calls
      When the session is summarized
      Then the batch tool and each inner tool are each counted once
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Markdown report contains the headline numbers
      Given a report built from one populated session
      When the Markdown is rendered
      Then the output contains the report title and the power score line
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Dashboard is rasterized and saved
      Given a report built from one populated session
      When the report is generated
      Then the PNG bytes carry the PNG signature and a file named productivity-<timestamp>.png exists under generated-images in the jcode home directory
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Command and its aliases start a report
      Given the local slash-command dispatcher
      When each of /productivity, /wrapped, and /stats is dispatched
      Then each is claimed by the dispatcher and starts a report generation without starting an agent turn
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Result is delivered to the requesting session
      Given a report result addressed to session A
      When a session with a different id receives the result event
      Then the event is ignored and the report is not displayed
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Clipboard failure is reported without losing the report
      Given the system clipboard is unavailable
      When the report result is handled
      Then the Markdown report is still displayed and the footer states that the image could not be copied
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Activity buckets and flavor are derived
      Given a report with two edits, one apply patch, four bash calls, seven agentgrep calls, and one browser call
      When the report is built
      Then the code edit count is three, the command count is four, the search count is seven, the web action count is one, and the archetype and power score are populated
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Runtime command returns the report and the image
      Given a runtime host with local transcripts
      When the productivity runtime command runs
      Then the response carries the serialized report, the saved PNG path, and the PNG as base64 with media type image/png
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Activity calendar and streaks are recorded
      Given one session active on four distinct calendar dates including a run of three consecutive days
      When the report is built
      Then the report records four active days, the first and last active dates, and a longest streak of three days
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Report generation makes no network call
      Given a machine with no network connectivity
      When the report is generated
      Then the report is produced and the dashboard is written to disk
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Repeat run is served from the cache
      Given a transcript store that has already been scanned once
      When the report is generated a second time
      Then no transcript is re-parsed and the run completes faster than the first run
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Only compact summaries are held in memory
      Given a large transcript store
      When the scan runs
      Then each transcript is reduced to a compact summary before it is retained and the full transcript is not kept
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Malformed transcript does not abort the scan
      Given one transcript file that is not valid JSON
      When the scan runs
      Then the parse error count is one and the report is still produced from the remaining transcripts
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Interface stays responsive during generation
      Given a report generation in flight
      When the user keeps typing
      Then the input is accepted while the generation continues in the background
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Dashboard renders without a browser
      Given a host with a system font database and no network access
      When the dashboard is rasterized
      Then a PNG is produced from the locally built SVG
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should the report support a selectable time window (today, last 7 days, all time) instead of always covering all time?
