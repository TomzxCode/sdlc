---
title: "Security, Audit, and Secrets"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Security, Audit, and Secrets

## Overview

Operators need three connected trust surfaces in one installation. First, a local static audit (`openclaw security audit`) that inspects configuration, filesystem permissions, channel metadata, exec approvals, sandbox configuration, and plugin manifests on the operator's own machine, and can apply a bounded set of safe remediations. Second, a durable runtime activity ledger (`openclaw audit`) that records what the Gateway did as identity, ordering, provenance, action, status, and normalized outcome codes, and never records content. Third, credential indirection: a `SecretRef` contract with `env`, `file`, `exec`, and `store` providers, a shared secret store persisted in the shared SQLite state database, and an egress proxy that injects store-bound secrets at request time behind a host allowlist. A separate channel pairing surface lets an operator approve inbound DM senders with a short human-friendly code.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator running the installation | A single command that shows which security foot-guns are present and fixes the ones that are safe to fix |
| Security reviewer | A durable, content-free record of agent runs, tool actions, and message delivery that supports incident reconstruction without retaining user data |
| Application developer | Credentials referenced indirectly so that plaintext secrets never land in config, logs, or prompts |
| Platform integrator | One secret store and one egress allowlist that apply across channels, models, and plugins |
| Channel administrator | A way to admit a DM sender without opening a channel to everyone |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall run a local static security audit over configuration, filesystem permissions, channel metadata, exec approvals, sandbox configuration, and plugin manifests, and shall emit each finding with a stable `checkId`, a severity of `info`, `warn`, or `critical`, a detail, and an optional remediation |
| FR-2 | Must | The system shall support a deep audit mode that additionally probes the running Gateway and runs plugin-owned and skill code-safety collectors, and shall record the probe outcome on the report |
| FR-3 | Must | The system shall apply only bounded remediations when a fix is requested, limited to tightening filesystem permissions and default settings, and shall skip symbolic links, already-correct targets, and targets whose type does not match the expectation, reporting each action as applied, skipped, or failed |
| FR-4 | Must | The system shall keep a durable activity ledger in the shared SQLite state database that records only identity, ordering, provenance, action, status, and normalized outcome codes, and shall never store prompts, message bodies, tool arguments, tool results, attachments, filenames, URLs, command output, or raw error text |
| FR-5 | Must | The system shall record agent run, tool action, and inbound and outbound message events, each carrying a stable `sourceId` and `sourceSequence` for local replay deduplication, and shall tag every returned record as `metadata_only` redaction |
| FR-6 | Must | The system shall pseudonymise sensitive audit identifiers for accounts, actors, conversations, messages, and targets using a per-database HMAC key held in `audit_identity_keys`, and shall fail loudly rather than fall back to an unkeyed digest when the persisted key material is damaged |
| FR-7 | Must | The system shall bind an admitted agent run to an execution identity context that carries a context id, an execution id, a run id, and a coverage state, and shall record decision receipts that name the decision owner, the source reference, the action family, the decision outcome, and the reason code |
| FR-8 | Must | The system shall retain audit events for 30 days and shall cap the ledger at 100,000 rows, pruning rows outside the retention window in batches |
| FR-9 | Must | The system shall expose a bounded operator query surface over the ledger with filters for agent id, session key, run id, execution id, kind, status, direction, channel, and a time range, and shall support cursor-based continuation of a page |
| FR-10 | Must | The system shall support a `SecretRef` indirection contract with the `env`, `file`, `exec`, and `store` sources, each reference identified by a provider alias and an id, and shall validate the reference shape once at its trust boundary before any resolution |
| FR-11 | Must | The system shall provide a shared secret store persisted in the shared SQLite state database, supporting `team` and `identity` scopes, `secret` and `env` entry kinds, soft deletion, and a per-entry host allowlist, and shall treat `secret`-kind values as write-only |
| FR-12 | Must | The system shall provide a secrets egress proxy that injects store-bound secrets at request time and shall reject any request whose destination host is outside both the configured traffic allowlist and the allowlist of a secret bound to that host |
| FR-13 | Must | The system shall audit the installation for plaintext secret residue, unresolved references, placeholder values, shadowed references, store plaintext residue, and legacy residue, and shall report each finding with a stable code |
| FR-14 | Should | The system shall support a plan and apply flow for secrets configuration, where a serialized plan carries a version, a list of targets, and expected revisions, and where apply refuses a plan that fails validation |
| FR-15 | Should | The system shall support channel DM pairing that issues an 8-character human-friendly code, expires pending requests after 1 hour, keeps at most 3 pending requests per channel account, derives an opaque request id from a SHA-256 digest, and persists an approved allow list per channel and account |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The activity ledger shall not grow a content-bearing column, and the ledger writer shall not accept a content payload as an input field |
| NFR-2 | Must | Security | Secret values shall never be returned by a read of a `secret`-kind store entry, and every printed or logged representation of a credential shall be masked |
| NFR-3 | Must | Performance | An operator ledger query shall return at most 500 records per page, and a decision receipt query shall return at most 100, and both shall page through a cursor rather than by re-reading the ledger |
| NFR-4 | Must | Portability | A permission fix shall use POSIX `chmod` on Unix-like platforms and `icacls` on Windows, and shall never follow a symbolic link when changing a mode |
| NFR-5 | Should | Availability | A failure to persist an audit event shall not fail the operation being audited, and shall be observable through a diagnostic event rather than by breaking the caller |
| NFR-6 | Should | Usability | Every security audit finding shall carry a remediation that names the configuration key or the filesystem path the operator must change |

## Constraints

- The local static audit (`src/security/`) and the durable activity ledger (`src/audit/`) are separate subsystems with separate command surfaces (`openclaw security audit` and `openclaw audit`) and no shared tables.
- The Gateway protocol is a WebSocket and HTTP JSON-RPC surface, not a REST API, so the RPC method names are the stable contract.
- All durable state for the ledger, the secret store, the pairing tables, and the capture store lives in the shared SQLite state database defined by `src/state/openclaw-state-schema.sql`.
- The local debug proxy in `src/proxy-capture/` is a separate operator tool and is not the secrets egress proxy in `src/secrets/egress-proxy/`.
- The audit identity key is a per-database singleton row. Rotation would change every pseudonym, so the key is created once and never silently replaced.
- Execution identity recording is off by default and must be enabled explicitly through configuration.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Audit reports findings with stable identifiers
      Given a config whose Gateway binds to a non-loopback address without shared auth
      When the operator runs "openclaw security audit"
      Then the report contains a finding with checkId "gateway.bind_no_auth" and severity "critical"
      And the report contains a "summary" object with critical, warn, and info counts
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Deep mode records the live Gateway probe outcome
      Given a running Gateway that the audit process can reach
      When the operator runs "openclaw security audit --deep"
      Then the report contains a "deep" object whose "gateway" member reports attempted true and ok true
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Fix tightens permissions and skips symbolic links
      Given a state directory whose mode is world writable
      And a config path that is a symbolic link
      When the operator runs "openclaw security audit --fix"
      Then the state directory action is reported as applied
      And the symbolic link action is reported as skipped with reason "symlink"
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Ledger stores metadata only
      Given an agent run that executes a tool and receives a reply
      When the run finishes and the ledger is queried
      Then every returned record carries redaction "metadata_only"
      And no returned record contains a prompt, message body, tool argument, tool result, file name, or URL
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Agent run events are recorded with replay deduplication
      Given an agent run that starts and then succeeds
      When the run lifecycle events are written to the ledger
      Then the ledger contains an "agent.run.started" record and an "agent.run.finished" record with status "succeeded"
      And re-writing the same sourceId and sourceSequence does not create a second record
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Sensitive identifiers are pseudonymised with a keyed digest
      Given an inbound message from a channel sender
      When the message record is written to the ledger
      Then the account, conversation, message, and target references match the pattern "hmac-sha256:v1:KEY_ID:DIGEST"
      And the plain identifier is absent from the record
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Damaged identity key material fails loudly
      Given a persisted audit identity key whose key length is not 32 bytes
      When a pseudonym is derived
      Then the operation fails with an error naming a corrupt audit identity key
      And no unkeyed digest is returned
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Run inspection reports identity and decision receipts
      Given an admitted run with execution identity collection enabled
      And a recorded decision fact for that run
      When the operator runs "openclaw audit --run RUN_ID --explain"
      Then the result names the execution identity context and the execution id
      And the result lists the decision receipt with its owner, source reference, and reason code
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Ledger is bounded by age and row count
      Given ledger rows older than 30 days and more than 100,000 rows in total
      When retention runs
      Then rows older than 30 days are removed
      And the ledger row count is brought back under the 100,000 row cap
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Operator filters the ledger with a cursor
      Given more ledger records than fit in one page
      When the operator runs "openclaw audit --agent AGENT_ID --limit 10"
      Then at most 10 records are returned
      And the result carries a cursor that continues the same query
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: SecretRef is validated at its trust boundary
      Given a config value that is an object with source "env", provider "default", and id "OPENAI_API_KEY"
      When the value is validated as a SecretRef
      Then it is accepted
      And an object whose source is "vault" is rejected
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Store entries are scoped, soft deleted, and write only
      Given a team-scoped store entry of kind "secret" named OPENAI_API_KEY
      When the operator lists the store
      Then the entry name and its metadata are listed
      And reading the value of a "secret" kind entry does not return the value
      And removing the entry leaves the row in place with a deletion timestamp
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Egress proxy rejects hosts outside the allowlist
      Given a secrets egress proxy whose allowed hosts do not include api.example.com
      When a request is made to api.example.com that would inject a store secret
      Then the proxy rejects the request
      And the rejection names the allowedHosts configuration key and the "openclaw secrets store set --allow-host" command
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Secrets audit reports stable finding codes
      Given a config that contains a plaintext API key and an unresolvable file reference
      When the operator runs "openclaw secrets audit"
      Then the output contains a finding with code "PLAINTEXT_FOUND"
      And the output contains a finding with code "REF_UNRESOLVED"
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Apply refuses a plan that fails validation
      Given a serialized secrets plan whose version is not 1
      When the operator runs "openclaw secrets apply"
      Then the plan is rejected before any config file is written
      And the rejection names the plan version
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Pairing code is short lived, capped, and opaque
      Given a channel account with 3 pending pairing requests
      When a 4th pending request is created
      Then the oldest pending request is pruned
      And the pending request id is a 32 character opaque value that is not the human code
      And a request created more than 1 hour ago is treated as expired
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Ledger schema carries no content column
      Given the shared state database schema
      When the "audit_events" table columns are listed
      Then no column holds a prompt, message body, tool argument, tool result, attachment, file name, URL, command output, or raw error text
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Credentials are masked in output
      Given a credential value of 32 characters
      When it is masked for display
      Then the first 8 characters and the last 8 characters are shown
      And the middle characters are replaced by an ellipsis
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Page size is bounded
      Given a ledger with more than 500 matching records
      When the operator requests activity records
      Then no more than 500 records are returned
      And a decision receipt request returns no more than 100 receipts
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Permission fix uses the platform mechanism
      Given a state directory on a POSIX host
      When the fix runs
      Then the action reports kind "chmod" with the target mode
      And a Windows host reports kind "icacls" with a displayable command
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Ledger write failure does not fail the audited operation
      Given the ledger store is unavailable
      When an agent tool action is performed
      Then the tool action still completes
      And the write failure is reported through a diagnostic event
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Findings name the thing to change
      Given a config whose Gateway auth token is the placeholder value
      When the operator runs "openclaw security audit"
      Then the finding names "gateway.auth.token" in its remediation
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should the `openclaw secrets audit` plaintext scanner cover the operator's shell history and dotfiles, or stay scoped to OpenClaw-owned config, state, and auth-profile locations.
2. Should `outbound_message_progress` rows share the 30 day retention window of `audit_events`, or be retained for the longer window that message delivery forensics needs.
3. Should the pairing allow list expose a per-entry expiry, or continue to be a permanent allow list that the operator edits by hand.
