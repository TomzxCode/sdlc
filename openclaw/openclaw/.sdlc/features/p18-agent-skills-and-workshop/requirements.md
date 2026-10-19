---
title: "Agent Skills and Workshop"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Agent Skills and Workshop

## Overview

Skills are how the assistant carries reusable procedures. A skill is a directory whose `SKILL.md` carries YAML frontmatter with a name and a description, plus optional supporting files. OpenClaw discovers skills from several roots at once, resolves name collisions by a fixed precedence, and hands the surviving set to the model in three ways: the available-skills prompt catalog, the `/skill` slash command, and a per-skill chat command derived from the skill name. The operator governs that set. They install skills from ClawHub, Git, or a local directory, update and roll them back, and check which are ready. They publish their own reusable procedures to a personal and team skill library where every save creates a new revision. And the assistant improves its own procedures through a Workshop loop: it records each change it makes, lints the result, reviews its own work against real usage, and can archive, restore, or undo what it wrote. A separate release-versioned Custodian skill library holds operator-only playbooks that load only for the configured Custodian agent.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Assistant user | The assistant knows the procedures it has been taught and can invoke them by name |
| Operator | Control over which skills are installed, which are visible to which agent, and which are published to the team |
| Skill author | A contract for writing a skill that loads, reads well in the prompt catalog, and can be shared |
| Platform integrator | One place that owns discovery, precedence, installation, publication, and the Workshop change feed |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall discover skills from the workspace `skills` directory, the workspace `.agents/skills` directory, the personal `~/.agents/skills` directory, the managed state skills directory, the per-agent Workshop directory, the bundled directory, the Custodian directory, and the configured extra and plugin directories, and shall bound the discovery work per root and per source |
| FR-2 | Must | The system shall read a skill's YAML frontmatter to derive its name, description, and invocation policy, shall report an invalid frontmatter block as a load error without losing valid siblings, and shall materialize the skill into a runtime record carrying a display name, a content hash, a source label, and a file host |
| FR-3 | Must | The system shall resolve a name that appears in more than one root by precedence, keeping one winner, and shall report one summary per winning and losing root pair with the skill count and up to three example names, warning when a workspace or project source shadows a bundled or Custodian skill and staying silent when the content is identical |
| FR-4 | Must | The system shall filter skill visibility by the effective agent allowlist and by a per-session sparse overlay, and shall keep prompt visibility and user invocability as two independent properties |
| FR-5 | Must | The system shall surface the admitted skills to the assistant in the available-skills prompt catalog, through the `/skill` slash command, and through one chat command per skill whose name is derived from the skill name and de-duplicated across agents |
| FR-6 | Must | The system shall record per-skill usage counts and last-used timestamps keyed by the canonical absolute path of the `SKILL.md`, so that a same-named skill in another workspace does not inherit usage |
| FR-7 | Must | The system shall install a skill from ClawHub, from Git, or from a local directory, shall record the install metadata, and shall support updating, uninstalling, and rolling back an installed skill |
| FR-8 | Must | The system shall scan a skill bundle for literal secrets before the bundle is installed and before it is published to the library, and shall refuse the operation when the scan reports a critical finding |
| FR-9 | Must | The system shall maintain a personal and team skill library in which every save creates a new revision, every mutation is applied against an expected revision, and a lost race is rejected rather than overwritten |
| FR-10 | Must | The system shall record every Workshop change with its action, actor, summary, version id, session key, run id, and creation time, and shall list the changes newest-first with a bounded limit and a portable cursor |
| FR-11 | Must | The system shall let the operator archive a learned skill, restore an archived skill or a saved version, and undo a whole review run, and shall refuse an undo whose recorded changes are no longer available |
| FR-12 | Should | The system shall lint a `SKILL.md` on write and report advisory findings about the description length, the description opening, the body length, the guidance density, and the presence of hype words, without ever blocking the write |
| FR-13 | Should | The system shall schedule an autonomous experience review of the Workshop changes when the Workshop autonomous mode is `auto`, shall skip incognito sessions, and shall announce the changes that were committed even when the review run itself fails |
| FR-14 | Should | The system shall load the release-versioned Custodian skills only for the configured Custodian agent, and shall keep them out of every other agent's catalog |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Discovery shall stay bounded: at most 300 candidates per root, at most 200 skills loaded per source, at most 256,000 bytes per skill file, and a grouped scan depth of 6 levels, with the raw directory scan itself bounded |
| NFR-2 | Must | Security | A skill bundle shall never carry a literal credential, and the scanner shall cover the bundle files, report bounded evidence, and refuse a bundle with a critical finding |
| NFR-3 | Must | Compatibility | A library bundle shall hold at most 256 files, at most 1 MiB per file, at most 8 MiB per bundle, and a session shall hold at most 64 selected revisions, and a Workshop write shall be capped between 1,024 and 200,000 bytes |
| NFR-4 | Should | Usability | The skill lint output shall be advisory, capped at 3 findings, and shall report only the rules that the current write introduced |
| NFR-5 | Should | Availability | Workshop changes shall be recorded in the shared SQLite state database, and a lost acknowledgement shall not lose a committed change or cause a local replay |
| NFR-6 | Should | Performance | The available-skills prompt catalog shall respect the configured per-agent prompt character budget, and compaction shall shorten descriptions without changing the admitted skill identities |

## Constraints

- The Gateway protocol is a WebSocket and HTTP JSON-RPC surface, not a REST API, so the RPC method names are the stable contract.
- Skill files are plain files under the operator's filesystem. The state database holds usage counters, library revisions, library events, uploads, and the Workshop change feed, not skill content.
- The skill name and the chat command come from the `name` frontmatter field, or from the directory name when `name` is absent.
- A skill installed into the workspace is a filesystem write owned by the Gateway; the CLI never replays a mutation locally after dispatching it.
- The `skills.proposals.*` and `skills.curator.*` RPC methods are retired. They stay registered so old clients receive guidance, and they answer with an `INVALID_REQUEST` error that points at the Workshop methods.
- The Workshop path applies changes immediately and makes them undoable. It does not route changes through a proposal approval flow.
- A bundled skill and a Custodian skill share the same precedence tier, but a Custodian skill is only visible to the configured Custodian agent.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: A skill is discovered under a grouped root
      Given a workspace with "skills/research/SKILL.md"
      When discovery runs for the workspace
      Then the skill is discovered with the name "research"
    ```

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Discovery stays inside its budget
      Given a root that contains more candidates than the per-root cap
      When discovery runs
      Then discovery stops at the cap and reports that the scan was truncated
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Frontmatter drives the skill identity
      Given a SKILL.md whose frontmatter declares name "research" and a description
      When the skill is loaded
      Then the skill name is "research"
      And the materialized record carries a display name and a content hash
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: An invalid skill does not lose its valid siblings
      Given a directory with one invalid SKILL.md and one valid SKILL.md
      When discovery runs
      Then the invalid file is reported and skipped
      And the valid sibling is still loaded
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The highest precedence source wins
      Given a skill named "research" in the workspace and in the bundled directory
      When discovery runs
      Then the workspace copy is the winner
      And one summary names the winning root, the losing root, the skill count, and up to three example names
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Identical content across roots stays silent
      Given a skill named "research" with identical content in two roots
      When discovery runs twice
      Then no collision summary is emitted
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: The agent allowlist narrows the visible set
      Given an agent whose skills allowlist names only "research"
      And a workspace with skills "research" and "writing"
      When the agent catalog is built
      Then "writing" is not in the catalog
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Prompt visibility and user invocability are independent
      Given a skill whose invocation policy disables model invocation but allows user invocation
      When the catalog and the command set are built
      Then the skill is absent from the prompt catalog
      And the skill is still reachable as a user command
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The assistant sees the skill catalog and the commands
      Given a visible skill named "research"
      When the agent prompt and the chat command set are built
      Then the prompt contains an available-skills entry for "research"
      And a chat command named after the skill is registered once
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Usage is keyed by the file identity
      Given a skill used twice from one workspace path
      When the usage is read
      Then the use count for that canonical path is 2
      And a same-named skill in another workspace has its own count
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A local skill is installed
      Given a local directory with a valid SKILL.md
      When the operator runs "openclaw skills install ./my-skill"
      Then the skill is installed and its install metadata is recorded
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A tracked skill is rolled back
      Given an installed skill with a recorded previous version
      When the operator requests a rollback
      Then the previous version is restored
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: A bundle with a literal secret is refused
      Given a skill bundle whose script contains a hardcoded API key
      When the bundle is installed
      Then the install is refused
      And the finding names the file and the line
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A save creates a new revision
      Given a library skill at revision A
      When the operator saves a changed SKILL.md with expected revision A
      Then the library entry points at a new revision B
      And a library event records the save
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A racing writer is rejected
      Given a library skill whose revision changed after the writer read it
      When the writer saves with the stale expected revision
      Then the save is rejected
      And the existing revision is unchanged
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A Workshop change is recorded
      Given the agent wrote a new skill file
      When the change is recorded
      Then the change feed holds an entry with the action, the actor, the summary, the session key, the run id, and the creation time
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A review run is undone
      Given a review run that edited a skill
      When the operator undoes the review
      Then the skill is restored to its pre-review content
      And a second undo reports that the review was already undone
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: An undo with no recorded changes is refused
      Given a review id with no recorded changes
      When the operator undoes the review
      Then the undo is refused before any write
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Lint findings never block a write
      Given a SKILL.md whose description exceeds the advisory length
      When the skill is written
      Then the write succeeds
      And the lint output reports the description length finding
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: An autonomous review announces committed changes
      Given the Workshop autonomous mode is "auto" and a change was committed before the review run failed
      When the review finishes
      Then the committed change is still announced
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: An incognito session is not reviewed
      Given a Workshop change from an incognito session
      When the review scheduler runs
      Then the candidate is skipped
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Custodian skills are invisible to a normal agent
      Given a configured Custodian agent and a normal agent
      When each agent's catalog is built
      Then the Custodian playbook appears only in the Custodian agent's catalog
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: A skill file above the size cap is rejected
      Given a SKILL.md larger than 256,000 bytes
      When discovery runs
      Then the file is not loaded
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: The scanner reports bounded evidence
      Given a skill source with a suspicious pattern
      When the source is scanned
      Then the finding carries the rule, the file, the line, and bounded evidence
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: An oversized library bundle is refused
      Given a library bundle larger than 8 MiB
      When the bundle is uploaded
      Then the upload is refused
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Lint output is capped
      Given a SKILL.md that violates several authoring rules
      When the lint runs
      Then at most 3 advisories are reported
      And only the rules the write introduced are reported
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: A lost acknowledgement does not lose a change
      Given a Workshop change whose acknowledgement is lost after the commit
      When the change feed is read
      Then the committed change is present
      And no local replay is performed
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: The prompt catalog respects the character budget
      Given a per-agent skills prompt character budget
      When the catalog is rendered
      Then the catalog fits the budget
      And the admitted skill identities are unchanged
    ```

## Conflicts

None identified yet.

## Open Questions

1. The Workshop change feed keeps at most 500 rows per agent, which is the same bound an undo uses to hold one whole review run. Whether that bound should be a per-run bound, a per-agent bound, or both is still open.
2. Should a skill installed from a local directory be scanned by the literal-secret scanner before the install, or only the ClawHub and library paths.
3. Should the personal library entries be readable by other agents of the same owner profile, or stay private to the session that pinned them.
