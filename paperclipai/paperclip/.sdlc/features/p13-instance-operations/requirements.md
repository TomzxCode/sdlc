---
title: "Instance Operations and Settings"
status: done
---

# Requirements: Instance Operations and Settings

## Overview

Instance operations and settings expose the singleton instance configuration, controlled task drain, Cloud lifecycle readback, manual and scheduled database backups, and server load metrics to the actors that operate a Paperclip instance.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board member | Read general, experimental, and combined instance settings through the board UI. |
| Instance administrator | Change instance settings, start and stop task drains, trigger manual backups, and read server metrics. |
| Cloud control plane | Read body-bound task drain status and inspect or restore the Cloud-pinned primary company. |
| Hosting operator | Pin selected settings through hidden-setting and managed-config policies. |
| Server operator | Configure backup retention and observe process health without exposing data to company members. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall let authenticated board members read combined, general, and experimental instance settings. |
| FR-02 | Must | The system shall let local implicit board actors and instance administrators update combined and general settings. |
| FR-03 | Must | The system shall let Cloud tenant board actors with the experimental settings permission update experimental settings. |
| FR-04 | Must | The system shall validate every settings patch with the shared Zod schemas before it reaches the service. |
| FR-05 | Must | The system shall normalize stored settings, apply schema defaults, and overlay read-time operator defaults and Cloud managed flags. |
| FR-06 | Must | The system shall report Cloud managed keys in experimental settings responses on managed instances. |
| FR-07 | Must | The system shall reject changes to operator-hidden settings while allowing exact same-value echoes from full-object forms. |
| FR-08 | Must | The system shall reject executionMode changes on Cloud-managed instances and reject manual backups on Cloud-managed instances. |
| FR-09 | Must | The system shall validate default environment selection and agent readiness before it persists an instance default environment. |
| FR-10 | Must | The system shall write an activity record for every company when settings or task drain state changes. |
| FR-11 | Must | The system shall expose task drain status and restrict upgrade-readiness and idle-safety reports to instance operators and verified Cloud authority. |
| FR-12 | Must | The system shall serialize task drain start and stop transitions so audit order and live state order always agree. |
| FR-13 | Must | The system shall resume queued runs after a task drain stops when the prior drain was active. |
| FR-14 | Must | The system shall provide Cloud lifecycle readback and idempotent primary company restore for Cloud-managed instances. |
| FR-15 | Must | The system shall let instance administrators trigger a manual database backup on self-hosted instances. |
| FR-16 | Must | The system shall serve a no-store server metrics snapshot to instance administrators only when the metrics switch is enabled. |
| FR-17 | Should | The system shall run automatic logical database backups on a configured interval and apply retention presets. |
| FR-18 | Should | The system shall keep a restart marker for idle backup wake-ups until a fresh verified backup completes. |
| FR-19 | Should | The system shall render general and experimental settings pages that read, patch, hide, and disable controls according to the API response. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Every route shall enforce board, instance-admin, Cloud-control, or local-implicit authority before it reads or mutates instance state. |
| NFR-02 | Must | Auditability | Every settings mutation and task drain transition shall produce an activity record for every company in the instance. |
| NFR-03 | Must | Reliability | A task drain audit transaction shall commit for all companies or for none before live drain state changes. |
| NFR-04 | Must | Safety | Malformed managed configuration and hidden-setting changes shall fail closed. |
| NFR-05 | Should | Performance | The settings service shall serve repeated hot reads from a process cache and invalidate that cache on writes. |
| NFR-06 | Should | Compatibility | Deprecated settings keys shall keep parsing while server-managed write fields stay protected. |

## Constraints

- The settings row is a singleton keyed by `default`.
- General settings schemas are strict, and experimental patch schemas strip server-managed activation fields.
- Task drain TTL is a positive integer up to 24 hours, and idle holds require 5,000 to 300,000 milliseconds.
- Cloud-managed instances pin execution mode, experimental flags, backups, and Cloud lifecycle state through platform policy.
- The metrics route is mounted only when `PAPERCLIP_SERVER_METRICS=true`.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first, then NFRs.

- [ ] **FR-01**

    ```gherkin
    @FR-01
    Scenario: Board members read instance settings
      Given a board member with company access
      When they request combined, general, or experimental settings
      Then the API returns the normalized settings for that surface
    ```

- [ ] **FR-02**

    ```gherkin
    @FR-02
    Scenario: Local and admin actors update settings
      Given a local implicit board actor or an instance administrator
      When they patch combined or general settings with valid fields
      Then the service persists the patch and returns the updated settings
    ```

- [ ] **FR-03**

    ```gherkin
    @FR-03
    Scenario: Cloud tenant admin updates experimental settings
      Given a Cloud tenant board actor with the experimental settings permission
      When they patch an allowed experimental flag
      Then the API persists the patch and records an experimental settings activity
    ```

- [ ] **FR-04**

    ```gherkin
    @FR-04
    Scenario: Invalid settings patches are rejected
      Given a patch with an unknown general field or an invalid retention preset
      When the route validates the request body
      Then the API returns a validation error before any service write
    ```

- [ ] **FR-05**

    ```gherkin
    @FR-05
    Scenario: Settings reads apply defaults and overlays
      Given stored settings with missing or legacy values and an operator default configured
      When the service reads general and experimental settings
      Then responses contain schema defaults, operator defaults, and Cloud managed values without persisting overlays
    ```

- [ ] **FR-06**

    ```gherkin
    @FR-06
    Scenario: Managed keys are reported
      Given a Cloud-managed instance with an overlaid experimental flag
      When a client reads experimental settings
      Then the response lists that flag in managedKeys with the Paperclip Cloud manager
    ```

- [ ] **FR-07**

    ```gherkin
    @FR-07
    Scenario: Hidden settings cannot change
      Given an operator-hidden general or experimental field
      When an actor patches that field with a different value
      Then the API returns 403 with settings_operator_managed
      When an actor echoes the current value
      Then the API accepts the write
    ```

- [ ] **FR-08**

    ```gherkin
    @FR-08
    Scenario: Platform-managed values stay pinned
      Given a Cloud-managed instance
      When an actor changes executionMode or triggers a manual backup
      Then the API returns 403 with execution_mode_platform_managed or database_backups_platform_managed
    ```

- [ ] **FR-09**

    ```gherkin
    @FR-09
    Scenario: Default environment is validated
      Given an instance default environment patch
      When the environment is unknown or inheriting agents are not ready
      Then the API rejects the patch before persisting it
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Settings mutations are audited
      Given a company list with two companies
      When an instance administrator patches general settings
      Then the API writes an instance.settings.general_updated activity for both companies
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Task drain reports require authority
      Given a company member and an instance administrator
      When each requests upgradeReadiness or idleSleepSafety reports
      Then only the instance administrator receives instance-wide reports
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Overlapping drain transitions stay ordered
      Given a start request whose audit transaction is still pending
      When a delete request arrives concurrently
      Then the delete queues behind the start and the audit order matches the live drain order
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Stopping an active drain resumes queued work
      Given an active task drain and queued runs
      When an administrator stops the drain
      Then the API reports wasActive true and queued runs are dispatched again
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Cloud lifecycle readback and restore
      Given a Cloud-managed instance with an archived primary company
      When Cloud control reads lifecycle state and then unarchives the primary
      Then the read reports the primary status and the restore changes the company to active
      When the primary is already active
      Then the restore reports changed false
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Manual backup on a self-hosted instance
      Given an instance administrator on a self-hosted instance
      When they trigger a database backup
      Then the API returns 201 with the backup file, size, retention, and timing metadata
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Metrics are admin-only and no-store
      Given the server metrics switch is enabled
      When an instance administrator requests server metrics
      Then the response contains the process snapshot with Cache-Control no-store
      When a company member requests the same route
      Then the API returns 403
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Automatic backups follow the schedule
      Given automatic backups configured with an interval
      When the backup deadline arrives
      Then the coordinator runs one backup and applies retention to older files
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Idle backup wake marker survives restart
      Given a marker written before process replacement
      When a fresh verified backup completes
      Then the marker is cleared
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Settings pages reflect API policy
      Given settings with hidden and managed fields
      When the general and experimental pages render
      Then hidden controls are absent and managed controls are disabled with a badge
    ```

- [ ] **NFR-01**

    ```gherkin
    @NFR-01
    Scenario: Unauthorized callers are rejected
      Given an agent credential or a board member without instance admin rights
      When they call a mutation or admin-only instance route
      Then the API returns 403 before reading or mutating instance state
    ```

- [ ] **NFR-02**

    ```gherkin
    @NFR-02
    Scenario: Audit records span all companies
      Given several companies in the instance
      When a settings mutation commits
      Then every company has a matching activity record
    ```

- [ ] **NFR-03**

    ```gherkin
    @NFR-03
    Scenario: Failed drain audit leaves no drain
      Given one company audit write that fails
      When a start or stop transition runs
      Then the transaction commits no activity rows and live drain state is unchanged
    ```

- [ ] **NFR-04**

    ```gherkin
    @NFR-04
    Scenario: Malformed managed config fails closed
      Given an invalid managed configuration value
      When the settings service is constructed
      Then construction throws instead of returning unmanaged settings
    ```

- [ ] **NFR-05**

    ```gherkin
    @NFR-05
    Scenario: Hot settings reads share one statement
      Given repeated settings reads in one process with no writes
      When clients read the settings row
      Then the cache serves them from one database statement
    ```

- [ ] **NFR-06**

    ```gherkin
    @NFR-06
    Scenario: Deprecated keys remain loadable
      Given stored settings with retired compatibility flags
      When the service normalizes and returns settings
      Then retired values parse without resetting current flags
    ```

## Conflicts

None identified.

## Open Questions

1. Which negotiated idle-safety report fields should be documented outside `doc/idle-sleep-safety.md` when new Cloud catalogs land?
2. Should the automatic backup scheduler be split into its own feature as the backup subsystem grows?
3. Which client should own the migration guide when a deprecated experimental flag is finally removed?
