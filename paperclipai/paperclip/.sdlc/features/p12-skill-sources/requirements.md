---
title: "Skill Sources"
status: done
---

# Requirements: Skill Sources

## Overview

Board users and agents need to install skills from GitHub repositories into a company and keep those skills current without manual file handling.
This feature covers repository discovery, audited scanning, selection, versioned installation, automatic refresh, repair, and disconnect behavior for repository-backed skills.
It also covers the Skill Sources page and the Skill Studio surfaces used to inspect, copy, edit, and version installed skills.
Implementation evidence: `server/src/services/skill-sources.ts`, `server/src/services/skill-source-sync.ts`, `server/src/services/github-skill-source.ts`, `server/src/routes/company-skills.ts`, `packages/db/src/schema/company_skill_sources.ts`, `ui/src/pages/SkillSources.tsx`, `ui/src/pages/SkillStudio.tsx`.
This feature is distinct from FEAT-0012 company skills catalog, which owns the general company skill library and catalog surfaces.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Import, select, refresh, repair, and disconnect GitHub skill sources from the Skill Sources page |
| Agent author | Use Skill Studio to inspect installed skills, make editable copies, edit files, and manage versions |
| Company policy administrator | Control which import, update, edit, remove, and create actions are allowed for a principal |
| Automated worker | Apply due refreshes and project imports with bounded batches and durable retry state |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall scan an authorized GitHub repository and return audited skill candidates with package metadata, warnings, and a pinned commit. |
| FR-2 | Must | The system shall stream scan progress and candidates over newline-delimited JSON when the client requests `application/x-ndjson`. |
| FR-3 | Must | The system shall preview an audited package file at an immutable commit after authorization. |
| FR-4 | Must | The system shall import selected skills into a company as source entries with versions, snapshots, provenance metadata, and activity records in one transaction. |
| FR-5 | Must | The system shall list and detail company sources with entries, selection state, sync state, repair action, and visible project bindings. |
| FR-6 | Must | The system shall refresh a tracked source, skip work when commit or tree is unchanged, and publish only changed skill versions. |
| FR-7 | Must | The system shall save skill selection, excluded folders, package mode, and connection with per-skill authorization and revision checks. |
| FR-8 | Must | The system shall update automatic updates, new skill imports, connection, and tracking ref through a revision-checked settings operation. |
| FR-9 | Must | The system shall disconnect a source by copying installed skills into editable personal copies or deleting them, and shall retain project access provenance where required. |
| FR-10 | Must | The system shall import skills from accessible project workspaces through durable project repository bindings. |
| FR-11 | Must | The system shall enforce company scoping and actor authorization on every source operation and log each mutation to the activity log. |
| FR-12 | Should | The system shall run automatic refreshes and project imports from scheduled worker sweeps with leases, bounded batches, retry backoff, and graceful shutdown. |
| FR-13 | Should | The system shall meter automatic refresh and initial import work against byte budgets and refund unused capacity for small repositories. |
| FR-14 | Should | The system shall use repository package mode for shared files and dependencies, with a bounded per-skill package fallback. |
| FR-15 | Should | The system shall expose Skill Studio flows for creating, forking, editing, copying, and versioning skills, including conflict handling for stale edits. |
| FR-16 | May | The system shall list authorized repository branches with the default branch included and results bounded. |
| FR-17 | May | The system shall accept legacy GitHub URLs and adopt legacy GitHub imports without changing installed identity. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Source reads shall use the requesting actor's authorized GitHub connection, and provider bodies, tokens, and credentials shall not be persisted or returned in errors. |
| NFR-2 | Must | Reliability | Source creation, refresh, settings, selection, and disconnect shall guard stale and concurrent writes with revision numbers and short-lived leases. |
| NFR-3 | Must | Integrity | A failed activity write, policy denial, or authorization failure shall roll back the source publication and keep previously installed content. |
| NFR-4 | Should | Performance | Scanning shall apply process-local limits of one active scan per caller, two per company, 30 and 60 scans per minute, and 6 and 12 downloads per minute. |
| NFR-5 | Should | Availability | Automatic work shall use a five-minute cadence, ten-minute leases, batches of ten imports and ten refreshes per sweep, and exponential retry delay capped at one hour. |
| NFR-6 | Should | Capacity | Automatic work shall default to 512 MiB byte budgets and refill unused measured capacity for small packages. |

## Constraints

- Every source, entry, binding, and budget row is company-scoped and cascades on company deletion.
- Repository and file paths are validated before use, including HTTPS GitHub repository checks and rejection of absolute, traversal, and null-byte paths.
- Selection and settings requests carry the source revision, and a mismatch returns a conflict before publication.
- Automatic reads require a stored setup identity with current company and project access, or explicit repair with a new connection.
- Repository package mode is enforced for project-bound sources and for sources that outgrow the supported package size.
- Skill Studio version conflicts require the client to keep unsaved text and confirm a reload from the latest file.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.

Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).

Write each criterion as a fenced `gherkin` block with a tag matching its requirement ID, so the criteria are parseable and later executable via BDD tooling (pytest-bdd, cucumber).

Multiple scenarios per requirement are allowed; tag each with the requirement ID.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Discover audited skills
      Given an authorized GitHub repository with SKILL.md files
      When an operator submits a discovery request
      Then the response contains candidates with paths, names, file counts, warnings, a pinned commit, and no file bodies
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Stream discovery progress
      Given a client that accepts application/x-ndjson
      When a repository scan runs
      Then the client receives progress and candidate events followed by a complete event or a sanitized error event
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Preview a package file
      Given a discovery result with a pinned commit and skill path
      When an authorized client previews a package file
      Then the response contains the audited file content at that commit with truncation metadata
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Import selected skills
      Given a scanned repository and a set of selected paths
      When an operator imports the source
      Then the company gains a source row, source entries, installed skills with versions, and an activity record
    ```

    ```gherkin
    @FR-4
    Scenario: Atomic publication failure
      Given required activity persistence fails during import
      When the transaction attempts to publish
      Then no source, skill, version, or entry from that import remains
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Detail sync state
      Given a source that is enabled, has automatic updates, and has a completed refresh
      When a client requests source detail
      Then the response reports sync state ready, lists visible entries and projects, and reports no repair action
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Skip an unchanged tree
      Given a tracked source with a recorded last scan tree
      When an automatic refresh finds a new commit with the same tree
      Then no skill version is replaced and the source records the new commit and a successful check
    ```

    ```gherkin
    @FR-6
    Scenario: Publish a changed skill
      Given a tracked source whose selected skill content changed
      When a refresh runs
      Then only the changed skill receives a new version and the source revision advances
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Save a stale selection
      Given a source revision that changed since the client loaded it
      When a client saves a selection with the old revision
      Then the API returns a conflict and installed skills are kept
    ```

    ```gherkin
    @FR-7
    Scenario: Deselect with policy denial
      Given a policy that denies the edit action for an installed skill
      When a client saves a selection that deselects that skill
      Then the API denies the request before any publication
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Change tracking ref
      Given a source that is not bound to a project
      When an operator selects an available branch in settings
      Then the source validates the branch commit and stores the new tracking ref with an incremented revision
    ```

    ```gherkin
    @FR-8
    Scenario: Invalid branch settings
      Given a branch that no longer resolves to a commit
      When settings save is attempted
      Then the source and its installed content are unchanged
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Disconnect with copies
      Given a connected source with installed skills
      When an operator disconnects with the copy option
      Then each installed skill becomes an editable personal copy and the source is removed or retained as removed by access scope
    ```

    ```gherkin
    @FR-9
    Scenario: Disconnect with assigned skill
      Given an installed skill assigned to an agent
      When an operator disconnects with the delete option
      Then the deletion is denied and the source remains linked
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Adopt a project repository
      Given an accessible project workspace with a repository
      When an operator adopts that repository
      Then a durable pending binding is created and a worker imports the repository into the company
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Cross-company source access
      Given an actor without access to company B
      When they request company B source detail or mutation
      Then the route denies access before calling the source service
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Recover after shutdown
      Given an automatic refresh interrupted by shutdown
      When a worker starts again
      Then the held lease is recoverable and the source is retried from its saved deadline
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Refund unused automatic capacity
      Given an automatic refresh whose measured scan is smaller than the reserved bytes
      When the job settles
      Then the unused bytes return to the company budget
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Preserve shared dependencies
      Given a repository whose skills reference shared scripts
      When the repository package mode is selected and imported
      Then shared files are stored once and installed versions retain their file mapping
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Preserve unsaved Studio edits on conflict
      Given a Studio editor with unsaved markdown and a newer saved version on the server
      When the conflict is confirmed
      Then unsaved text is kept until the client reloads the latest file
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: List branches with identity check
      Given a source whose repository identity changed at its URL
      When branches are requested
      Then the API rejects the listing instead of returning branches for the new repository
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Import from a legacy folder URL
      Given a pasted GitHub folder URL with a slash-containing ref
      When the URL importer resolves it
      Then the source is created or refreshed with the correct tracking ref and skill paths and no duplicate skills
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Sanitize provider failures
      Given a provider response containing credentials or response bodies
      When a refresh fails
      Then the stored last error is a sanitized message and the audit details contain no credential text
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Concurrent refresh conflict
      Given a refresh lease held by one worker
      When a second refresh starts
      Then the second request receives a conflict and does not alter the source
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Preserve content on access failure
      Given a refresh that loses GitHub access after acquiring a lease
      When the refresh fails
      Then the lease is cleared, a retry deadline is saved, and installed skill versions remain available
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Bound concurrent scans
      Given a caller with one active scan and a company with two active scans
      When another scan starts
      Then the request is limited with a retry hint before any provider download
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Bound automatic sweep work
      Given more than ten due sources and more than ten pending project imports
      When a sweep runs
      Then only ten of each are attempted in that sweep and remaining deadlines stay persisted
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Meter company byte budget
      Given a company budget of 512 MiB
      When an oversized automatic import runs
      Then the reserved bytes are consumed and later automatic work is deferred until capacity is available
    ```

## Conflicts

None identified yet.

## Open Questions

1. Whether the 512 MiB default byte budget is intended as a product limit or a conservative deployment default.
2. Whether removed project sources have a defined retention period for their provenance rows.
3. Whether the Studio update-diff surface is intended for every source entry or only for entries with complete snapshots.
