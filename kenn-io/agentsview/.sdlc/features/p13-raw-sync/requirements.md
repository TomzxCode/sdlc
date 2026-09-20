---
title: "Raw Sync Mesh"
status: done
---

# Requirements: Raw Sync Mesh

## Overview

The raw sync mesh preserves original provider session files into a durable local outbox and uploads them to an operator-managed server for multi-device custody.
It transports bytes without parsing them, so later server-side derivation can reconstruct browsable sessions from retained source files.
It is separate from the parsed-session remote sync in `p1-session-sync` (SSH and S3 sources), which moves already-parsed archive data rather than original provider files.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Original session files from every device end up in hosted custody without manual steps |
| Operator | Provisions device credentials, runs the raw-sync server, and inspects custody metadata |
| Developer | Extends capture to new providers and builds derivation on top of retained generations |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall capture original provider files into a durable local outbox without parsing their content |
| FR-2 | Must | The system shall record device identity and per-source acknowledged heads (manifest, receipt, generation) in a local SQLite checkpoint database |
| FR-3 | Must | The system shall negotiate missing objects with the server before uploading, so already-held bytes are never re-sent |
| FR-4 | Must | The system shall upload objects resumably with content verification by exact SHA-256 and byte length |
| FR-5 | Must | The system shall commit one complete logical generation per manifest with expected-parent receipt fencing, monotonic generation assignment, and a durable receipt |
| FR-6 | Must | The system shall authenticate devices via provisioned credentials exchanged for short-lived scoped tokens, with revocation that blocks issuance and invalidates outstanding tokens |
| FR-7 | Must | The system shall provide a `raw-sync watch` daemon that performs an initial bounded audit, reacts to filesystem changes, repeats the audit every 15 minutes by default, and retries uploads every minute by default |
| FR-8 | Must | The system shall provide a `raw-sync status` command that prints path-free JSON describing the local checkpoint, pending work, retry state, failures, and coverage |
| FR-9 | Should | The system shall claim server parse jobs, reconstruct their source files, parse them, and retry failures through an internal worker library |
| FR-10 | Should | The system shall serve the raw-sync HTTP control plane from `pg serve` only when the PostgreSQL role holds every required raw-sync privilege |
| FR-11 | Should | The system shall scope custody by tenant, reject unrecognized or excluded providers before bytes enter custody, and exclude S3 roots from laptop capture |
| FR-12 | Should | The system shall expose an authenticated tenant-scoped status route reporting source heads, parse-job counts, devices, and open uploads |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall accept the device credential from the environment only, never from CLI arguments |
| NFR-2 | Must | Security | The system shall require HTTPS for the raw-sync server URL except for loopback hosts with an explicit insecure flag |
| NFR-3 | Must | Security | The system shall store only SHA-256 digests of device credentials and tokens in PostgreSQL, never clear values |
| NFR-4 | Must | Reliability | The system shall resume interrupted uploads and survive client restarts via durable checkpoints and persisted upload offsets |
| NFR-5 | Should | Reliability | The system shall fail closed on stale parents, reused capture identities with different content, and conflicting object content |
| NFR-6 | Should | Performance | The system shall bound per-provider audit work (default 128 sources) and cap the local outbox (default 1 GiB) |

## Constraints

- Raw sync transports original files only and never writes the normal local SQLite session archive.
- Hosted raw sync is not end-to-end encrypted because the server must read retained files to parse them.
- Device enrollment and revocation are operator-managed; no public enrollment command or endpoint exists.
- S3 roots are excluded from laptop capture.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).

- [ ] **FR-1**
    - **Given** a supported provider root with session files on disk
    - **When** the watcher or audit captures the source
    - **Then** the files land in the local outbox as an unpublished generation with no parsing applied
- [ ] **FR-2**
    - **Given** a fresh data directory and a provisioned device ID
    - **When** `raw-sync watch` starts
    - **Then** the checkpoint database records the device and advances per-source heads only after server receipts are durable
- [ ] **FR-3**
    - **Given** a generation whose objects partly exist in server custody
    - **When** the uploader drains the generation
    - **Then** only the missing object references are uploaded
- [ ] **FR-4**
    - **Given** an interrupted object upload with a persisted server offset
    - **When** the uploader retries
    - **Then** the upload resumes from the accepted offset and the object verifies by SHA-256 and length
- [ ] **FR-5**
    - **Given** a generation whose objects all exist and verify in custody
    - **When** the manifest commits against the current source head
    - **Then** the server records the manifest, assigns the next generation and receipt, creates a parse job, and advances the source head
- [ ] **FR-5**
    - **Given** a manifest commit carrying a stale expected parent receipt
    - **When** the server evaluates it
    - **Then** the commit is rejected and the source head is unchanged
- [ ] **FR-6**
    - **Given** a provisioned device with an active credential
    - **When** the client requests a token with `upload` scope and uses it on an upload route
    - **Then** the request succeeds, and after revocation both issuance and outstanding tokens fail
- [ ] **FR-7**
    - **Given** configured provider roots and valid device credentials
    - **When** `raw-sync watch` runs
    - **Then** it audits once at startup, captures filesystem changes within the debounce window, re-audits on the interval, and retries uploads on the retry tick
- [ ] **FR-8**
    - **Given** a checkpoint database with pending generations and a failure
    - **When** `raw-sync status` runs
    - **Then** it prints JSON with checkpoint state, pending work, retry time, failures, and coverage, with no filesystem paths
- [ ] **FR-9**
    - **Given** a ready parse job in PostgreSQL
    - **When** the derivation worker claims it
    - **Then** it reconstructs the source files, parses them, and marks the job complete or records a retryable failure
- [ ] **FR-10**
    - **Given** a `pg serve` deployment whose role lacks a raw-sync privilege
    - **When** the server starts
    - **Then** it logs the exact missing requirement, omits the raw-sync routes, and keeps serving the normal session UI
- [ ] **FR-11**
    - **Given** an upload declaring an unrecognized or excluded provider
    - **When** the custody service evaluates it
    - **Then** the bytes are rejected before entering custody
- [ ] **FR-11**
    - **Given** configured roots including an `s3://` source
    - **When** `raw-sync watch` resolves capture roots
    - **Then** the S3 source is excluded from capture
- [ ] **FR-12**
    - **Given** a device token with the `status` scope
    - **When** the client calls the status route
    - **Then** it receives source heads, parse-job counts, devices, and open-upload metadata for its tenant only
- [ ] **NFR-1**
    - **Given** a device credential set in the environment
    - **When** `raw-sync watch --help` is inspected
    - **Then** no flag or argument accepts the credential
- [ ] **NFR-2**
    - **Given** an `http://` server URL for a non-loopback host
    - **When** `raw-sync watch` starts
    - **Then** it refuses to run unless the loopback-only insecure allowance applies
- [ ] **NFR-3**
    - **Given** enrolled devices and issued tokens
    - **When** the PostgreSQL device and token tables are inspected
    - **Then** they contain digests only and no clear credentials or tokens
- [ ] **NFR-4**
    - **Given** a client killed mid-upload and mid-generation
    - **When** `raw-sync watch` restarts
    - **Then** uploads resume from persisted offsets and unacknowledged generations drain without loss or duplication
- [ ] **NFR-5**
    - **Given** a repeated capture identity with different content
    - **When** the manifest commits
    - **Then** the commit fails closed and returns the existing receipt only for byte-identical retries
- [ ] **NFR-6**
    - **Given** a provider with more changed sources than the audit limit and an outbox near capacity
    - **When** the audit and capture run
    - **Then** the audit defers excess sources to later passes and capture reports outbox exhaustion instead of growing unbounded

## Conflicts

None identified yet.

## Open Questions

1. When will public device enrollment and revocation endpoints replace the current operator-managed provisioning?
2. When will server-side derivation be connected to `pg serve` startup so retained generations become browsable sessions?
3. What are the retention, garbage-collection, and disaster-rebuild policies for the raw object repository?
